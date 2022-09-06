import logging
import argparse
from tabulate import tabulate
import util

from sys import argv
from datetime import datetime, timedelta

# Logger
# logging.basicConfig(format='%(asctime)s %(levelname)s   %(message)s', level=logging.INFO)

# Constants
SUB_ID = "31169275-2308-4cdd-8d7a-f39ffd65bbf8"
RSRC_GROUP = "XCC-ASSESSMENT-JACQUELINE"

# List VMs by Zone
def list_vms(zone):
    client = util.create_client(SUB_ID)
    vms = client.virtual_machines.list_by_location(zone)
    dates = util.fetch_snapshot_dates(RSRC_GROUP, SUB_ID)
    print_data = []

    for vm in vms:
        print_data.append([
            vm.name,
            vm.tags['backup'],
            vm.storage_profile.os_disk.name,
            dates[vm.name].strftime('%Y-%m-%d %H:%M:%S.%f-%z') if vm.name in dates else 'Never'
        ])

    print(tabulate(print_data, headers=['Instance', 'Backup Enabled', 'Disk', 'Last Backup']))

# Create Snapshots for VMs where backup = true
    # Only if last backup was not done today
def create_snapshots():
    client = util.create_client(SUB_ID)
    disks = util.fetch_disks(RSRC_GROUP, SUB_ID)
    dates = util.fetch_snapshot_dates(RSRC_GROUP, SUB_ID)

    print('🚀 Starting backup process')

    # Iterate through disks, checking if a backup is necessary and creating snapshot if so
    for disk in disks:
        print(f'Instance: {disk.name}')

        # Only execute if backup tag is true
        if disk.tags['backup'] == 'true':
            print('Backup Enabled: True')
            print(f'Last backup was {dates[disk.name]}')
            
            # Check date of snapshot against today's date
            if dates[disk.name].date() != datetime.today().date():
                print(f'⏳ Backing up disk {disk.name}')
                
                # Delete old snapshot if one exists
                if (disk.name in dates):
                    async_snapshot_deletion = client.snapshots.begin_delete(RSRC_GROUP, str(disk.name) + '-snapshot')
                
                # Create new snapshot
                async_snapshot_creation = client.snapshots.begin_create_or_update(
                    RSRC_GROUP,
                    str(disk.name) + '-snapshot',
                    {
                        'location': disk.location,
                        'creation_data': {
                            'create_option': 'Copy',
                            'source_uri': disk.id
                        },
                    }
                )
                # snapshot = async_snapshot_creation.result()
                print('Backup completed')
            else:
                print('Skipping backup creation since the last backup is too recent')
        else:
            print('Backup Enabled: False')
            print('Skipping backup creation since backups are not enabled')
    print('✅ All snapshots done')

# Remove Old Backups
    # Retention Policy:
        # (1) no more than 1 per day for those made in the last 7 days
        # (2) no more than 1 per week for those made prior to the last 7 days
        # (3) always keep the most recent backup
def remove_old_backups():
    client = util.create_client(SUB_ID)
    snapshots = util.fetch_snapshots(RSRC_GROUP, SUB_ID)
    disks = {}

    for snapshot in snapshots:
        # Get disk id and date snapshot was created
        disk_id, date_created = str(snapshot.creation_data.source_unique_id), snapshot.time_created
        
        # Get the iso week and weekday number for the snapshot
        year, week, weekday = date_created.isocalendar()

        # Sort into either Older or Recent status
        if date_created.date() > datetime.today().date() + timedelta(days=7):
            disk_id = disk_id + '- Older'
            key = week
        else:
            disk_id = disk_id + '- Recent'
            key = weekday

        # Delete older snapshots according to retention policy
        if disk_id in disks:
            if key not in disks[disk_id]:
                disks[disk_id] = key
            elif snapshot.time_created > disks[disk_id][key].time_created:
                to_delete = disks[disk_id][key].name
            else:
                to_delete = snapshot.name
                disks[disk_id][key] = snapshot
            client.snapshots.begin_delete(RSRC_GROUP, to_delete)
            logging.info(f'Deleting snapshot {to_delete}')
        else:
            disks[disk_id] = { key: snapshot }





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run some functions')
    parser.add_argument('--list_vms', help='List VMs in a specified zone')
    parser.add_argument('--create_backups', action='store_true', help='Create snapshot for all primary disks')
    parser.add_argument('--tidy_backups', action='store_true', help='Remove old backups based on removal policies')

    args = parser.parse_args()

    if args.list_vms:
        list_vms(args.list_vms)

    if args.create_backups:
        create_snapshots()

    if args.tidy_backups:
        remove_old_backups()