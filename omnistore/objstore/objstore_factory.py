from omnistore.objstore.aliyun_oss import OSS
from omnistore.objstore.constant import OBJECT_STORE_OSS, OBJECT_STORE_MINIO
from omnistore.objstore.minio import MinIO
from omnistore.store import Store


class StoreFactory:
    ObjStores = {
        OBJECT_STORE_OSS: OSS,
        OBJECT_STORE_MINIO: MinIO,
    }

    @classmethod
    def new_client(cls, provider: str, endpoint: str, bucket: str) -> Store:
        objstore = cls.ObjStores[provider]
        if not objstore:
            raise KeyError(f"Unknown object store provider {provider}")

        return objstore(endpoint=endpoint, bucket=bucket)
