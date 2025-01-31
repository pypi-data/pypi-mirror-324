import json
import zlib
import base64
import time
from typing import Dict, Optional, Any, Union
from boto3 import client as boto3_client
import os


class OuterboundsAppClient:
    def __init__(
        self,
        token: Union[str, None] = None,
        metaflow_config_file_path: Union[str, None] = None,
    ):
        self._mfconfig: Dict[str, str] = {}
        self._remote_config_pointer: Optional[Dict[str, str]] = None
        self._initialized: bool = False

        # The order of precedence is:
        # 1. config_string
        # 2. metaflow_config_file_path
        # 3. default METALOW_HOME/config.json
        if token is not None:
            self.init(config_string=token)
        elif metaflow_config_file_path is not None:
            self.init(metaflow_config_file_path=metaflow_config_file_path)
        else:
            self.init()

    def _decode_jwt(self, jwt_token: str) -> Dict[str, Any]:
        base64_url = jwt_token.split(".")[1]
        if not base64_url:
            raise ValueError("JWT is not valid.")

        # Replace URL-safe characters
        base64_str = base64_url.replace("-", "+").replace("_", "/")

        # Add padding if necessary
        padding = len(base64_str) % 4
        if padding:
            base64_str += "=" * (4 - padding)

        decoded = base64.b64decode(base64_str)
        return json.loads(decoded)

    def _jwt_needs_refresh(self, token: str) -> bool:
        decoded_jwt = self._decode_jwt(token)
        if "exp" not in decoded_jwt:
            raise ValueError('JWT does not contain an "exp" field.')

        current_timestamp = int(time.time())
        return decoded_jwt["exp"] < current_timestamp + 5 * 60

    @staticmethod
    def remove_prefix(input_str: str) -> str:
        try:
            return input_str.split(":", 1)[1]
        except IndexError:
            return input_str

    def init(self, **settings) -> None:
        """Initialize the ObAppClient with either a config file path or config string."""
        self._initialized = True
        self._init_config(settings)

    def _init_config(self, settings: Dict[str, Any]) -> None:
        print(settings)
        if "config_string" in settings:
            mfconfig = self._decode_config(settings["config_string"])
        elif "metaflow_config_file_path" in settings:
            with open(settings["metaflow_config_file_path"], "r") as f:
                mfconfig = json.load(f)
        else:
            # Try reading metaflowconfig from METALOW_HOME/config.json
            metaflow_config_loc = os.path.join(
                os.getenv("METAFLOW_HOME", os.path.expanduser("~/.metaflowconfig")),
                "config.json",
            )
            if os.path.exists(metaflow_config_loc):
                with open(metaflow_config_loc, "r") as f:
                    mfconfig = json.load(f)
            else:
                raise ValueError("No config provided")

        # If config type is aws-secrets-manager, get actual config from AWS Secrets Manager
        if mfconfig.get("OB_CONFIG_TYPE") == "aws-secrets-manager":
            self._remote_config_pointer = mfconfig
            self._refresh_remote_config()
        else:
            self._mfconfig = mfconfig

    def _refresh_remote_config(self) -> None:
        if not self._initialized:
            raise RuntimeError("Not initialized. Call init() first.")

        if not self._remote_config_pointer:
            raise ValueError("No remote config pointer provided")

        secrets_manager = boto3_client(
            "secretsmanager",
            region_name=self._remote_config_pointer["AWS_SECRETS_MANAGER_REGION"],
        )

        secret_value = secrets_manager.get_secret_value(
            SecretId=self._remote_config_pointer["AWS_SECRETS_MANAGER_SECRET_ARN"]
        )

        if "SecretBinary" not in secret_value:
            raise ValueError("Secret value is not binary")

        secret_string = secret_value["SecretBinary"].decode("utf-8")
        self._mfconfig = json.loads(secret_string)

        if not self._mfconfig:
            raise ValueError("Failed to fetch remote config")

    def _is_config_remote(self) -> bool:
        return self._remote_config_pointer is not None

    def raw_config(self) -> Dict[str, Any]:
        return self._mfconfig

    def _decode_config(self, encoded_config: str) -> Dict[str, Any]:
        data = self.remove_prefix(encoded_config)
        decompressed = zlib.decompress(base64.b64decode(data)).decode("utf-8")
        return json.loads(decompressed)

    def get_auth_headers(self) -> Dict[str, str]:
        if not self._initialized or not self._mfconfig:
            raise RuntimeError("Not initialized. Call init() first.")

        if "METAFLOW_SERVICE_AUTH_KEY" not in self._mfconfig:
            raise ValueError("No auth key found")

        # Refresh config with auth token if needed
        if (
            self._jwt_needs_refresh(self._mfconfig["METAFLOW_SERVICE_AUTH_KEY"])
            and self._is_config_remote()
        ):
            self._refresh_remote_config()

        api_key = self._mfconfig["METAFLOW_SERVICE_AUTH_KEY"]

        return {
            "x-api-key": api_key,
        }
