 # EC2 installation with node_exporter

 ## Prerequisites

 - An AWS account with permissions to create EC2.
 - AWS credentials configured in your environment (for example via AWS CLI or environment variables).
 - Python 3.6 or later installed.
 - Pulumi CLI already installed and logged in.
 - if you want to generate your own key cert :

        openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout node_exporter_conf/server.key -out node_exporter_conf/server.crt -subj "/C=US/ST=Indonesia/L=Yogyakarta"

   **Note :** Do not change `node_exporter_conf/server.key` and `node_exporter_conf/server.key`. If you do so, you need to reconfigure `node_exporter_conf/install_node_exporter.sh`.

 ## Step
1. Copy and configure environment variable in environment.example.sh :

      cp environment.example.sh environment.sh
      vi environment.sh

2. Export environment variable and run pulumi up

      ./environment.sh && pulumi up



 