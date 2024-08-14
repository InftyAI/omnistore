from omnistore.objstore.aliyun_oss import OSS
from omnistore.store import Store

OBJECT_STORE_OSS = "OSS"


class StoreFactory:
    ObjStores = {
        OBJECT_STORE_OSS: OSS,
    }

    @classmethod
    def new_client(cls, provider: str, endpoint: str, bucket: str) -> Store:
        objstore = cls.ObjStores[provider]
        if not objstore:
            raise KeyError(f"Unknown object store provider {provider}")

        return objstore(endpoint=endpoint, bucket=bucket)
