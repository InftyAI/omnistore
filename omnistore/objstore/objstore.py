from __future__ import annotations
from abc import abstractmethod

from omnistore.store import Store


class ObjStore(Store):
    @abstractmethod
    def __init__(self, endpoint: str, bucket: str):
        """
        Construct a new client to communicate with the provider.
        """
        pass
