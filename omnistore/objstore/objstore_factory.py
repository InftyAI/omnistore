from omnistore.objstore.aliyun_oss import OSS
from omnistore.objstore.constant import OBJECT_STORE_OSS, OBJECT_STORE_MINIO, OBJECT_STORE_S3
from omnistore.objstore.minio import MinIO
from omnistore.objstore.s3 import S3
from omnistore.store import Store


class StoreFactory:
    ObjStores = {
        OBJECT_STORE_OSS: OSS,
        OBJECT_STORE_MINIO: MinIO,
        OBJECT_STORE_S3: S3,
    }

    @classmethod
    def new_client(cls, provider: str, endpoint: str = None, bucket: str = None) -> Store:
        objstore = cls.ObjStores[provider]
        if not objstore:
            raise KeyError(f"Unknown object store provider {provider}")

        return objstore(endpoint=endpoint, bucket=bucket)
