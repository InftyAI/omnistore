from abc import ABC, abstractmethod


class Store(ABC):
    @abstractmethod
    def upload(self, src: str, dest: str):
        """
        Upload will upload the obj to the provider.
        """
        pass

    @abstractmethod
    def download(self, src: str, dest: str):
        """
        download will download the required obj from the provider.
        Non-null callback will be invocated when download finished.
        """
        pass

    @abstractmethod
    def delete(self, filename: str):
        """
        Delete will delete the obj from the provider.
        """
        pass

    @abstractmethod
    def exists(self, filename: str):
        """
        Exists checks whether the obj exists in the provider.
        """
        pass

    @abstractmethod
    def accessible(self) -> bool:
        """
        Accessible checks whether the obj is visitable.
        """
        pass
