# import boto3
#
# ec2 = boto3.resource('ec2')
# security_group = ec2.SecurityGroup('id')

# import boto3
# client = boto3.client('ec2')
#
# print([{"name": f_group['GroupName']}
#            for f_group in client.describe_security_groups()['SecurityGroups']])

# for sg in security_groups:
#     print(f'Security Group Name: {sg["GroupName"]}')
#     print(f'Description: {sg["Description"]}')
#     print(f'Inbound Rules: {sg["IpPermissions"]}')
#     print(f'Outbound Rules: {sg["IpPermissionsEgress"]}')
#     print('---')



import boto3
client = boto3.client('ec2')

security_groups = client.describe_security_groups()['SecurityGroups']
open_ports = []

for sg in security_groups:
    sg_id = sg['GroupId']
    for ingress in sg['IpPermissions']:
        for ip_range in ingress['IpRanges']:
            if ip_range['CidrIp'] == '0.0.0.0/0':
                open_ports.append(f"security group {sg_id} allows all ingress traffic")

print(open_ports)
