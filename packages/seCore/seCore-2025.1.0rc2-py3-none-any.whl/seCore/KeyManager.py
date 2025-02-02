import json
import os
import pathlib
from seCore.CustomLogging import logger
from seCore.templates import Keys

BASE_PATH = pathlib.Path(__name__).resolve().parent


class KeyManager:
    def __init__(self):
        """
        Initializes the KeyManager by loading keys from a file or defaults.
        """
        self.keys = self._load_keys_from_file()
        # logger.info(json.dumps({"keys": {"count": len(self.keys)}}))

    @staticmethod
    def _load_keys_from_file() -> dict:
        """
        Loads keys from the default JSON file or uses default keys.
        """
        file_path = os.path.join(BASE_PATH, "app", "secret", "keys.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        return json.loads(Keys.create_default_keys())

    def get_all_keys(self) -> dict:
        """
        Returns all keys as a dictionary.
        """
        return self.keys

    @staticmethod
    def get_masked_keys():
        """
        Returns masked versions of all keys.
        """
        original_keys = keyManager.get_all_keys()
        masked_keys = {}
        for key, value in original_keys.items():
            masked_key = keyManager.mask_key(value["Key"])
            value["Key"] = masked_key
            masked_keys[masked_key] = value
        return masked_keys

    def validate_key(self, key: str) -> bool:
        """
        Checks if a given key is valid.
        """
        return key in self.keys

    def mask_key(self, key: str) -> str:
        """
        Masks a key by returning its last segment.
        :param key: The key to mask.
        :return: The masked key as a string.
        """
        return key.split("-")[-1] if self.validate_key(key) else ""

    def get_roles(self, key: str) -> list:
        """
        Returns the roles associated with a given key.
        :param key: The key to retrieve roles for.
        :return: A list of roles.
        """
        return self.keys.get(key, {}).get("Roles", [""])

    def validate_role(self, key: str, role: str) -> bool:
        """
        Validates if a role is associated with a key.
        """
        return role in self.get_roles(key)

    def validate_key_role(self, key: str, role: str) -> dict:
        """
        Validates a key and role combination and provides key details.
        :param key: The key to validate.
        :param role: The role to validate.
        :return: A dictionary with validation details.
        """
        return {
            "key": key,
            "role": role,
            "key_mask": self.mask_key(key),
            "roles": self.get_roles(key),
            "role_valid": self.validate_role(key, role),
        }


# Singleton instance of the KeyManager.
keyManager = KeyManager()
