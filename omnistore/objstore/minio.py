import io
import os
from abc import ABC
from pathlib import Path

import minio
from minio import credentials, S3Error

from omnistore.objstore.objstore import ObjStore


class MinIO(ObjStore):
    def __init__(self, endpoint: str, bucket: str):
        """
        Construct a new client to communicate with the provider.
        """
        auth = credentials.EnvMinioProvider()
        self.client = minio.Minio(endpoint, credentials=auth,secure=False)
        self.bucket_name = bucket

        # Make sure the bucket exists
        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)

    def create_dir(self, dirname: str):
        if not dirname.endswith("/"):
            dirname += "/"
        empty_stream = io.BytesIO(b"")
        self.client.put_object(self.bucket_name, dirname, empty_stream, 0)

    def delete_dir(self, dirname: str):
        if not dirname.endswith("/"):
            dirname += "/"
        objects = self.client.list_objects(
            self.bucket_name, prefix=dirname, recursive=True
        )
        for obj in objects:
            self.client.remove_object(self.bucket_name, obj.object_name)

    def upload(self, src: str, dest: str):
        self.client.fput_object(self.bucket_name, dest, src)

    def upload_dir(self, src_dir: str, dest_dir: str):
        for file in Path(src_dir).rglob("*"):
            if file.is_file():
                dest_path = f"{dest_dir}/{file.relative_to(src_dir)}"
                self.upload(str(file), dest_path)
            elif file.is_dir():
                self.create_dir(f"{dest_dir}/{file.relative_to(src_dir)}/")

    def download(self, src: str, dest: str):
        self.client.fget_object(self.bucket_name, src, dest)

    def download_dir(self, src_dir: str, dest_dir: str):
        if not src_dir.endswith("/"):
            src_dir += "/"
        path = Path(dest_dir)
        if not path.exists():
            path.mkdir(parents=True)
        objects = self.client.list_objects(
            self.bucket_name, prefix=src_dir, recursive=True
        )
        for obj in objects:
            file_path = Path(dest_dir, Path(obj.object_name).relative_to(src_dir))
            if not file_path.parent.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)
            if obj.object_name.endswith("/"):
                continue
            self.download(obj.object_name, str(file_path))

    def delete(self, filename: str):
        self.client.remove_object(self.bucket_name, filename)

    def exists(self, filename: str):
        try:
            self.client.stat_object(self.bucket_name, filename)
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            else:
                raise e
