from abc import ABC, abstractmethod


class Store(ABC):
    @abstractmethod
    def create_dir(self, dirname: str):
        """
        create_dir will create a dir in the provider.
        """
        pass

    @abstractmethod
    def delete_dir(self, dirname: str):
        """
        delete_dir will delete a dir from the provider, together with all the files under the directory.
        """
        pass

    @abstractmethod
    def upload(self, src: str, dest: str):
        """
        upload will upload the file from src to dest, both parameters are file names.
        """
        pass

    @abstractmethod
    def upload_dir(self, src_dir: str, dest_dir: str):
        """
        upload_dir will upload the folder from src_dir to dest_dir, both parameters are folder names.
        """
        pass

    @abstractmethod
    def download(self, src: str, dest: str):
        """
        download will download the file from src to dest, both parameters are file names.
        """
        pass

    @abstractmethod
    def download_dir(self, src_dir: str, dest_dir: str):
        """
        download_dir will download the folder from src_dir to dest_dir, both parameters are folder names.
        """
        pass

    @abstractmethod
    def delete(self, filename: str):
        """
        delete will delete the file from the provider.
        """
        pass

    @abstractmethod
    def exists(self, filename: str):
        """
        exists checks whether the file exists in the provider.
        """
        pass
