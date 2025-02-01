from typing import Optional, Literal
from .base_online_store import BaseOnlineStore
from pyignite import Client
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

EXCEPTION_IGNITE_NO_PORT = (
    "No port"
)

EXCEPTION_IGNITE_NO_HOST = (
    "No host"
)

# Exception messages
EXCEPTION_IGNITE_UNEXPECTED_CONFIGURATION_CLASS = (
    "Unexpected configuration object (not a IgniteOnlineStoreConfig instance)"
)

class IgniteInvalidConfig(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)

class IgniteOnlineStoreConfig(FeastConfigBaseModel):
    """
    Configuration for the GG online store.
    NOTE: The class *must* end with the `OnlineStoreConfig` suffix.
    """
    type: Literal["feast_gridgain.ignite_online_store.IgniteOnlineStore"] = "feast_gridgain.ignite_online_store.IgniteOnlineStore"

    host: Optional[StrictStr] = "localhost"
    port: Optional[StrictInt] = 10800
    cache_name: Optional[StrictStr] = None


class IgniteOnlineStore(BaseOnlineStore):
    """
    An online store implementation that uses Ignite.
    NOTE: The class *must* end with the `OnlineStore` suffix.
    """

    def _get_conn(self, config: RepoConfig):
        """
        Establishes a connection to the Ignite cluster.

        Args:
            config: The Feast repository configuration object containing Ignite connection details.

        Returns:
            An Ignite client instance connected to the cluster.
        """

        online_store_config = config.online_store
        if not isinstance(online_store_config, IgniteOnlineStoreConfig):
            raise IgniteInvalidConfig(
                EXCEPTION_IGNITE_UNEXPECTED_CONFIGURATION_CLASS
            )
        
        client = Client()
        host = online_store_config.host or "localhost"  # Use default if None
        port = online_store_config.port or 10800       # Use default if None

        if host is None:
            raise IgniteInvalidConfig(
                EXCEPTION_IGNITE_NO_HOST
            )
        elif port is None:
            raise IgniteInvalidConfig(
                EXCEPTION_IGNITE_NO_PORT
            )

        start_time_connect = time.perf_counter_ns()   
        client.connect(host,port)
        self.log("get_online_features", "ignite_online_store", "pyignite.connect", time.perf_counter_ns()-start_time_connect)

        return client