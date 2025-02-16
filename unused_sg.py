import boto3

client = boto3.client('ec2')

def find_unused_sg():
    # Get all security groups
    security_groups = client.describe_security_groups()['SecurityGroups']
    all_sg = {sg['GroupId'] for sg in security_groups}  # Set of all SG IDs

    # Get all ENIs and extract attached security groups
    enis = client.describe_network_interfaces()['NetworkInterfaces']
    used_sg = set()

    for eni in enis:  # Loop through all ENIs
        for group in eni['Groups']:  # Correctly iterate over the security groups in ENI
            used_sg.add(group['GroupId'])  # Collect SG IDs in use

    # Find unused security groups
    unused_sgs = all_sg - used_sg  # Set difference operation

    return unused_sgs

print(find_unused_sg())
