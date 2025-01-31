# Description

An experimental client/python package to generate the authentication headers necessary to interact with Outerbounds apps. To use this, you need to have your outerbounds config, or a configuration token for an outerbounds machine user.

## Usage Instructions

Install using: `pip install outerbounds-app-client`

```
from ob_app_client import OuterboundsAppClient

# Create a client instance if you have a metaflow config at ~/.metaflowconfig/config.json or METAFLOW_HOME/config.json
client = OuterboundsAppClient()
# OR explicitly provide a config file path
client = OuterboundsAppClient(metaflow_config_file_path="path/to/config.json")
# OR explicitly provide a config string
client = OuterboundsAppClient(config_string="your-encoded-config-string")

# Get authentication headers
auth_headers = client.get_auth_headers()
```
