# Description

An experimental client/python package to generate the authentication headers necessary to interact with Outerbounds apps. To use this, you need to have your outerbounds config, or a configuration token for an outerbounds machine user.

## Usage Instructions

```
from ob_app_client import OuterboundsAppClient

# Create a client instance with a name
client = OuterboundsAppClient("my-app")

# Initialize with a config file
client.init(metaflow_config_file_path="path/to/config.json")
# OR initialize with a config string
client.init(config_string="your-encoded-config-string")

# Get authentication headers
auth_headers = client.get_auth_headers()
```
