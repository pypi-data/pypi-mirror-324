from typing import Optional, Literal
from .base_online_store import BaseOnlineStore
from pygridgain import Client
from feast import RepoConfig
from feast.repo_config import FeastConfigBaseModel
from pydantic import StrictStr, StrictInt
import logging
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Exception messages
EXCEPTION_GRIDGAIN_UNEXPECTED_CONFIGURATION_CLASS = (
    "Unexpected configuration object (not a GridGainOnlineStoreConfig instance)"
)

EXCEPTION_GRIDGAIN_NO_USERNAME = (
    "Empty username"
)

EXCEPTION_GRIDGAIN_NO_PASSWORD = (
    "Empty password"
)

EXCEPTION_GRIDGAIN_NO_PORT = (
    "No port"
)

EXCEPTION_GRIDGAIN_NO_HOST = (
    "No host"
)

class GridGainInvalidConfig(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)

class GridGainOnlineStoreConfig(FeastConfigBaseModel):
    """
    Configuration for the GG online store.
    NOTE: The class *must* end with the `OnlineStoreConfig` suffix.
    """
    type: Literal["feast_gridgain.gridgain_online_store.GridGainOnlineStore"] = "feast_gridgain.gridgain_online_store.GridGainOnlineStore"

    username: Optional[StrictStr] = None
    password: Optional[StrictStr] = None
    host: Optional[StrictStr] = "localhost"
    port: Optional[StrictInt] = 10800
    cache_name: Optional[StrictStr] = None


class GridGainOnlineStore(BaseOnlineStore):
    """
    An online store implementation that uses gridgain.
    NOTE: The class *must* end with the `OnlineStore` suffix.
    """

    def _get_conn(self, config: RepoConfig):
        """
        Establishes a connection to the gridgain cluster.

        Args:
            config: The Feast repository configuration object containing gridgain connection details.

        Returns:
            An gridgain client instance connected to the cluster.
        """
        online_store_config = config.online_store
        if not isinstance(online_store_config, GridGainOnlineStoreConfig):
            raise GridGainInvalidConfig(
                EXCEPTION_GRIDGAIN_UNEXPECTED_CONFIGURATION_CLASS
            )

        client = Client()
        username = online_store_config.username
        password = online_store_config.password
        host = online_store_config.host or "localhost"  # Use default if None
        port = online_store_config.port or 10800       # Use default if None

        if host is None:
            raise GridGainInvalidConfig(
                EXCEPTION_GRIDGAIN_NO_HOST
            )
        elif port is None:
            raise GridGainInvalidConfig(
                EXCEPTION_GRIDGAIN_NO_PORT
            )
        
        if username is not None and password is not None:
            client = Client(username=username, password=password, use_ssl=True)

        start_time_connect = time.perf_counter_ns()   
        client.connect(host,port)
        self.log("get_online_features", "gridgain_online_store", "pygridgain.connect", time.perf_counter_ns()-start_time_connect)

        return client