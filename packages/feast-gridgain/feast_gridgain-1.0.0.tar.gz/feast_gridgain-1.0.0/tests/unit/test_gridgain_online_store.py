import pytest
from feast import RepoConfig
from feast.repo_config import RegistryConfig
from feast_gridgain.gridgain_online_store import (
    GridGainOnlineStore,
    GridGainOnlineStoreConfig,
    GridGainInvalidConfig,
)
from .base_test_online_store import BaseOnlineStoreTest

class TestGridGainOnlineStore(BaseOnlineStoreTest):
    """Unit tests for GridGain online store implementation"""
    
    store_class = GridGainOnlineStore
    config_class = GridGainOnlineStoreConfig
    client_path = 'feast_gridgain.gridgain_online_store.Client'
    invalid_config_exception = GridGainInvalidConfig

    def _get_mock_store_config(self):
        """Provides mock configuration - no real credentials needed for unit tests"""
        return GridGainOnlineStoreConfig(
            username="mock_user",
            password="mock_pass",
            host="mock.gridgain.com",
            port=10800
        )

    def test_get_conn_valid_config(self, valid_config, mock_client):
        """Tests connection with valid configuration"""
        store = self.store_class()
        conn = store._get_conn(valid_config)
        assert conn == mock_client
        mock_client.connect.assert_called_once_with(
            "mock.gridgain.com",
            10800
        )

    def test_get_conn_missing_username(self, valid_config, mock_client):
        """Tests connection with missing username"""
        store = self.store_class()
        valid_config.online_store.username = None
        conn = store._get_conn(valid_config)
        assert conn == mock_client
        mock_client.connect.assert_called_once_with(
            "mock.gridgain.com",
            10800
        )

    def test_get_conn_missing_password(self, valid_config, mock_client):
        """Tests connection with missing password"""
        store = self.store_class()
        valid_config.online_store.password = None
        conn = store._get_conn(valid_config)
        assert conn == mock_client
        mock_client.connect.assert_called_once_with(
            "mock.gridgain.com",
            10800
        )