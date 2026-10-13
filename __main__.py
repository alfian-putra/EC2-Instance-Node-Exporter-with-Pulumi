"""An AWS Python Pulumi program"""

import os
import yaml
import subprocess
import bcrypt

#import pulumi
import pulumi_aws 

# Get local Variable
local_vars = os.environ

# create node_exporter yaml
command_generate_crt = 'openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout /etc/node_exporter/server.key -out /etc/node_exporter/server.crt -subj "/C=US/ST=Indonesia/L=Yogyakarta"'
node_exporter_config_dir = "/etc/node_exporter/"
node_exporter_cert_file = os.path.join(node_exporter_config_dir, "server.crt")
node_exporter_key_file = os.path.join(node_exporter_config_dir, "server.key")
node_exporter_web_config = "node_exporter_conf/web-config.yml" # this is a local path so it stored on node_exporter_conf

hashed_password = bcrypt.hashpw(local_vars["NODE_EXPORTER_PLAIN_PASSWORD"].encode("utf-8"), bcrypt.gensalt(rounds=12))

node_exporter_conf = {
    "tls_server_config" : {
        "cert_file" : node_exporter_cert_file,
        "key_file"  : node_exporter_key_file
    },
    "basic_auth_users" : {
        local_vars["NODE_EXPORTER_USER"] : hashed_password.decode("ascii").replace("$", "\\$")
    }
}

str_node_exporter_conf = yaml.dump(node_exporter_conf, default_flow_style=False, indent=4, width=80)

# storing configuration to user_data
user_data = f"""#!/usr/bin/bash

version={local_vars['NODE_EXPORTER_VERSION']}

# download copy configuration
sudo mkdir /etc/node_exporter/
sudo {command_generate_crt}

cat > /etc/node_exporter/web-config.yml << EOF
{str_node_exporter_conf}
EOF

# download and install from tarbal
tarbal=node_exporter-$version.linux-amd64.tar.gz
extracted_dir=node_exporter-$version.linux-amd64
url=https://github.com/prometheus/node_exporter/releases/download/v$version/$tarbal

wget $url

tar -xvf $tarbal 
sudo mv $extracted_dir/node_exporter /usr/local/bin/

cat > /etc/systemd/system/node_exporter.service <<EOF
[Unit]
Description=Node Exporter

[Service]
Type=simple
ExecStart=/usr/local/bin/node_exporter --web.config.file=/etc/node_exporter/web-config.yml
EOF

sudo systemctl daemon-reload 
sudo systemctl enable node_exporter --now
"""
print(user_data)

# Create an AWS resource (S3 Bucket)
imported_key_pair = pulumi_aws.ec2.KeyPair(
    "importedKeyPair",
    key_name="local user public key",
    public_key=local_vars["PUBLIC_KEY"]
)

#Security policy to allow port 22 (ssh) and 9100 (node_exporter)
security_group = pulumi_aws.ec2.SecurityGroup('security_group_ssh_node_exporter',
    description='Enable SSH access & node_exporter port',
    ingress=[
        {'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0']},
        {'protocol': 'tcp', 'from_port': 9100, 'to_port': 9100, 'cidr_blocks': ['0.0.0.0/0']}
    ],
    egress=[
            {'protocol': -1, 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0']}
    ]
)

# Create an EC2 instance. Replace ami with an AMI ID valid in your region.
ec2_instance = pulumi_aws.ec2.Instance(local_vars["AWS_EC2_INSTANCE_NAME"],
    ami=local_vars["AWS_EC2_AMI"],    # replace with a region-appropriate AMI
    instance_type=local_vars["AWS_EC2_INSTANCE_TYPE"],
    security_groups=[security_group.name],
    key_name=imported_key_pair.id,
    user_data=user_data,
    tags={
        "Name": "Example of EC2 deployment with Pulumi"
    }
)

# ec2_instance_user = local_vars["AWS_EC2_USER"]
# ec2_instance_public_ip = ec2_instance.public_ip

# print("EC2 instance created successfully. public IP : "+ str(ec2_instance_public_ip))
# print("executing ./ec2_node-exporter_setup.sh")
# setup_node_exporter = subprocess.run(["./ec2_node-exporter_setup.sh"], capture_output=True)
# print(f"Output : {setup_node_exporter.stdout.decode()}")
# print(f"Error : {setup_node_exporter.stderr.decode()}")

