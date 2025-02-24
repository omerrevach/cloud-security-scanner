import boto3
import json


ec2 = boto3.client('ec2')
rds = boto3.client('rds')

def get_security_groups():
    security_groups = ec2.describe_security_groups()['SecurityGroups']
                    # SSH     RDP      MYSQL  POSTGRE   MongoDB    REDIS
    high_risk_ports = [22,    3389,    3306,    5432,    27017,    6379]
    open_ports = []
    
    for sg in security_groups:
        sg_id = sg["GroupId"]
        
        for rule in sg.get('IpPermissions', []):
            from_port = rule.get('FromPort')
            ip_ranges = rule.get('IpRanges', [])
            
            for ip_range in ip_ranges:
                cidr = ip_range.get('CidrIp', "")
                
                if cidr == '0.0.0.0/0':
                    if from_port in high_risk_ports:
                        open_ports.append({
                            "security_group": sg_id,
                            "port": from_port,
                            "risk": "HIGH",
                            "issue": f"Found port {from_port} exposed to the universe"
                        })

    return open_ports

vulnerabilities = get_security_groups()

json_filename = "security_findings.json"

# Save results to JSON file
with open(json_filename, "w") as json_file:
    json.dump(vulnerabilities, json_file, indent=4)

print(f"[✔] Security findings saved to {json_filename}")