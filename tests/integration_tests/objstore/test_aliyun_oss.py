import os
import shutil

import pytest

from omnistore.objstore.objstore_factory import OBJECT_STORE_OSS, StoreFactory


class TestOSS:
    @pytest.fixture(scope="module", autouse=True)
    def setup_and_teardown(self):
        print("Setting up the test environment.")
        try:
            os.makedirs("./test-tmp", exist_ok=True)
        except Exception as e:
            print(f"An error occurred: {e}")

        yield

        print("Tearing down the test environment.")
        shutil.rmtree("./test-tmp")

    def test_upload_and_download_files(self):
        endpoint = os.getenv("ENDPOINT")
        bucket = os.getenv("BUCKET")

        client = StoreFactory.new_client(
            provider=OBJECT_STORE_OSS, endpoint=endpoint, bucket=bucket
        )
        assert False == client.exists("foo.txt")

        with open("./test-tmp/foo.txt", "w") as file:
            file.write("test")

        client.upload("./test-tmp/foo.txt", "foo.txt")
        assert True == client.exists("foo.txt")

        client.download("foo.txt", "./test-tmp/bar.txt")
        assert True == os.path.exists("./test-tmp/bar.txt")

        client.delete("foo.txt")
        assert False == client.exists("foo.txt")

    def test_upload_and_download_dir(self):
        endpoint = os.getenv("ENDPOINT")
        bucket = os.getenv("BUCKET")

        client = StoreFactory.new_client(
            provider=OBJECT_STORE_OSS, endpoint=endpoint, bucket=bucket
        )
        assert False == client.exists("/test/foo.txt")

        os.makedirs("./test-tmp/test", exist_ok=True)
        with open("./test-tmp/test/foo.txt", "w") as file:
            file.write("test")

        client.upload_dir("./test-tmp/test", "test")
        assert True == client.exists("test/foo.txt")

        client.download_dir("test", "./test-tmp/test")
        assert True == os.path.exists("./test-tmp/test/foo.txt")

        client.delete_dir("test")
        assert False == client.exists("test/foo.txt")
