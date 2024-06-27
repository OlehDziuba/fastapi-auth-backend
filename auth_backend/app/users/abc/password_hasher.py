import abc


class PasswordHasher(abc.ABC):
    @abc.abstractmethod
    def hash(self, raw_password: str) -> str:
        raise NotImplementedError
