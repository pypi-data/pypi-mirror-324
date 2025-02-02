import msgspec


class Savable(msgspec.Struct, frozen=True):
    def save(self, path: str) -> None:
        raise NotImplementedError("Must be implemented by subclasses.")
