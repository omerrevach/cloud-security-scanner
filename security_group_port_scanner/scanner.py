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

# documentation
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_security_groups.html

import boto3
client = boto3.client('ec2')

security_groups = client.describe_security_groups()['SecurityGroups']
open_ports = []

for sg in security_groups:
    sg_id = sg['GroupId']
    sg_name = sg.get("GroupName", "Unknown Name")  # Handle missing name
    
    for ingress in sg.get('IpPermissions'):
        from_port = ingress.get('FromPort', 'All') # When all protocols are open
        to_port = ingress.get('ToPort', 'All')
        protocol = ingress.get('IpProtocol')
        
        for ip_range in ingress.get('IpRanges', []):
            if ip_range.get('CidrIp') == '0.0.0.0/0':
                open_ports.append(f"Security Group {sg_name} {sg_id} allows open ingress {protocol} from port: {from_port} - {to_port}")

if open_ports:
    print("\n".join(open_ports))
else:
    print("No open ports found.")