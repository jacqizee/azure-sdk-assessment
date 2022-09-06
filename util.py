from sys import argv
from azure.mgmt.compute import ComputeManagementClient
from azure.identity import AzureCliCredential

SUB_ID = "31169275-2308-4cdd-8d7a-f39ffd65bbf8"
RSRC_GROUP = "XCC-ASSESSMENT-JACQUELINE"

def create_client(subscription_id):
    credential = AzureCliCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)

    return compute_client


def fetch_vms(resource_group, subscription_id):
    compute_client = create_client(subscription_id)
    instances = [vm for vm in compute_client.virtual_machines.list(resource_group_name=resource_group)]

    return instances


def fetch_disks(resource_group, subscription_id):
    compute_client = create_client(subscription_id)
    disks = [vm for vm in compute_client.disks.list_by_resource_group(resource_group)]

    return disks


def fetch_snapshots(resource_group, subscription_id):
    compute_client = create_client(subscription_id)
    snapshots = [snapshot for snapshot in compute_client.snapshots.list_by_resource_group(resource_group)]

    return snapshots


def fetch_snapshot_dates(resource_group, subscription_id):
    snapshots = fetch_snapshots(resource_group, subscription_id)
    date_extraction = {}

    for snapshot in snapshots:
        date_extraction[snapshot.creation_data.source_resource_id.split('/')[-1]] = snapshot.time_created

    return date_extraction