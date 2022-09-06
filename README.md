# Azure SDK Assessment
This is an technical assessment for a role I've applied for that requires using Azure SDK

## Timeframe
- We expect that you should spend around 8 hours on this task. Don’t forget to spend some time on testing and documentation. If you can make it in 10 hours of work that is a good sign. If you need a little bit more that’s ok too. However, do not spend more than 14 hours. It’s better to deliver something simple than nothing at all.

## Context
The premise of this assessment is that:
- We’d like to give you a chance to demonstrate your skills, knowledge, and ability to learn.
- A team you work with asked for your help with automating backups of their virtual machines running on Azure. They want to use Azure’s snapshot functionality to make regular snapshots of the disks attached to their virtual machines, based on the labels of those virtual machines.
  - You are asked to automate this task using Python and the azure-mgmt-compute
  
 ### User Story #1
- List the VMs in a zone. Should print:
  - Name of the VM instance
  - If backups are enabled
  - Name of the first disk
  - Time of last backup (if enabled)
  
### User Story #2
- Create snapshots for all primary disks where backups are enabled
  - Should only create snapshot if previous snapshot was not made today

### User Story #3
- We want to remove old backups according to these rules:
  - No more than one backup per day for backups made in the last 7 days
  - No more than one backup per week for backups made prior to the last 7 days
- When removing backups, always keep the most recent one that still fits

## Documentation
Pages I found useful (saving here for easy access haha)
- Overview: https://docs.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-overview
- azure-mgmt-compute: https://docs.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute?view=azure-python
  - ComputeManagementClient: https://docs.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute.computemanagementclient?view=azure-python

## Learnings
- Digesting documentation - having never used Azure SDK or Azure API (or honestly Azure in general), reading the massive documentation and trying to find what I need was honestly a challenge, but as I got more used to finding the right pages and the sections that were most useful, that made it easier
