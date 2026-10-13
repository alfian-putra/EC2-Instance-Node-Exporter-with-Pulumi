 # EC2 installation with node_exporter

 ## Prerequisites

 - An AWS account with permissions to create EC2.
 - AWS credentials configured in your environment (for example via AWS CLI or environment variables).
 - Python 3.6 or later installed.
 - Pulumi CLI already installed and logged in.
 - if you want to generate your own key cert , change `openssl` command in `__main__.py`.

 ## Step
1. Copy and configure environment variable in environment.example.sh :

      cp environment.example.sh environment.sh
      vi environment.sh

2. Export environment variable and run pulumi up

      ./environment.sh && pulumi up



 