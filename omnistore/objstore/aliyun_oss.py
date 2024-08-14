import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

from omnistore.objstore.objstore import ObjStore


class OSS(ObjStore):
    def __init__(self, endpoint: str, bucket: str):
        """
        Construct a new client to communicate with the provider.
        """

        # Make sure environments OSS_ACCESS_KEY_ID and OSS_ACCESS_KEY_SECRET are exist.
        auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
        self._bucket = oss2.Bucket(auth, endpoint, bucket)

    def upload(self, src: str, dest: str):
        """
        Upload will upload the obj to the provider.
        """

        oss2.resumable_upload(self._bucket, dest, src)

    def download(self, src: str, dest: str):
        """
        Download will download the required obj from the provider.
        """

        oss2.resumable_download(self._bucket, src, dest)

    def delete(self, filename: str):
        """
        Delete will delete the obj from the provider.
        """

        return self._bucket.delete_object(filename)

    def exists(self, filename: str):
        """
        Exists checks whether the obj exists in the provider.
        """

        return self._bucket.object_exists(filename)

    def accessible(self) -> bool:
        """
        Accessible checks whether the obj is visitable.
        """
        raise NotImplementedError("OSS not implemented")
