import json
import pytest

from unittest.mock import patch, MagicMock
from seCore.KeyManager import KeyManager


@pytest.fixture
def mock_key_manager():
    with patch("seCore.KeyManager.KeyManager._load_keys_from_file", return_value={"da080af6-fcf1-4cc5-979a-0d83e6481776": {"Key": "da080af6-fcf1-4cc5-979a-0d83e6481776", "Roles": ["admin"]}}):
        yield KeyManager()


def test_initialization(mock_key_manager):
    """Test the initialization of KeyManager."""
    assert isinstance(mock_key_manager.keys, dict)
    assert len(mock_key_manager.keys) == 1


@patch("seCore.KeyManager.os.path.exists", return_value=True)
@patch("builtins.open", new_callable=MagicMock)
def test_load_keys_from_file(mock_open, mock_exists):
    """Test loading keys from file."""
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({"da080af6-fcf1-4cc5-979a-0d83e6481776": {"Key": "da080af6-fcf1-4cc5-979a-0d83e6481776", "Roles": ["admin"]}})
    keys = KeyManager._load_keys_from_file()
    assert "da080af6-fcf1-4cc5-979a-0d83e6481776" in keys
    assert keys["da080af6-fcf1-4cc5-979a-0d83e6481776"]["Key"] == "da080af6-fcf1-4cc5-979a-0d83e6481776"


def test_get_all_keys(mock_key_manager):
    """Test retrieving all keys."""
    keys = mock_key_manager.get_all_keys()
    assert isinstance(keys, dict)
    assert "da080af6-fcf1-4cc5-979a-0d83e6481776" in keys


def test_validate_key(mock_key_manager):
    """Test key validation."""
    assert mock_key_manager.validate_key("da080af6-fcf1-4cc5-979a-0d83e6481776") is True
    assert mock_key_manager.validate_key("invalid_key") is False


def test_mask_key(mock_key_manager):
    """Test masking keys."""
    masked_key = mock_key_manager.mask_key("da080af6-fcf1-4cc5-979a-0d83e6481776")
    assert masked_key == "0d83e6481776"
    invalid_mask = mock_key_manager.mask_key("invalid-key")
    assert invalid_mask == ""


def test_get_roles(mock_key_manager):
    """Test retrieving roles for a key."""
    roles = mock_key_manager.get_roles("da080af6-fcf1-4cc5-979a-0d83e6481776")
    assert isinstance(roles, list)
    assert "admin" in roles
    empty_roles = mock_key_manager.get_roles("invalid_key")
    assert empty_roles == [""]


def test_validate_role(mock_key_manager):
    """Test role validation."""
    assert mock_key_manager.validate_role("da080af6-fcf1-4cc5-979a-0d83e6481776", "admin") is True
    assert mock_key_manager.validate_role("da080af6-fcf1-4cc5-979a-0d83e6481776", "user") is False


def test_validate_key_role(mock_key_manager):
    """Test validation of key and role combination."""
    validation_result = mock_key_manager.validate_key_role("da080af6-fcf1-4cc5-979a-0d83e6481776", "admin")
    assert isinstance(validation_result, dict)
    assert validation_result["key"] == "da080af6-fcf1-4cc5-979a-0d83e6481776"
    assert validation_result["role"] == "admin"
    assert validation_result["key_mask"] == "0d83e6481776"
    assert validation_result["roles"] == ["admin"]
    assert validation_result["role_valid"] is True

def test_load_keys_from_file_default_keys():
    """Test _load_keys_from_file with no existing file (default keys)."""
    mock_file_path = "app/secret/keys.json"
    default_keys = {"default_key1": "default_value1"}
    key_manager = KeyManager()

    with patch("os.path.exists", return_value=False):
        with patch("seCore.templates.Keys.create_default_keys", return_value=json.dumps(default_keys)):
            with patch("os.path.join", return_value=mock_file_path):
                result = key_manager._load_keys_from_file()

    assert result == default_keys

@patch("seCore.KeyManager.KeyManager.get_all_keys")
@patch("seCore.KeyManager.KeyManager.mask_key")
def test_get_masked_keys(mock_mask_key, mock_get_all_keys):
    """Test if the get_masked_keys correctly masks keys."""
    # Mocking the return values
    mock_get_all_keys.return_value = {
        "key1": {"Key": "value1", "Role": "role1"},
        "key2": {"Key": "value2", "Role": "role2"}
    }
    mock_mask_key.side_effect = lambda key: f"masked_{key}"

    # Create instance of KeyManager and call the method
    key_manager = KeyManager()
    result = key_manager.get_masked_keys()

    # Check that the keys have been masked correctly
    expected_result = {
        "masked_value1": {"Key": "masked_value1", "Role": "role1"},
        "masked_value2": {"Key": "masked_value2", "Role": "role2"}
    }
    assert result == expected_result

    # Verify that the mocks were called as expected
    mock_get_all_keys.assert_called_once()
    assert mock_mask_key.call_count == 2
