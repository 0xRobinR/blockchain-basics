
from crypto_lib.sha256 import sha256


class MerkleLeaf:
    def __init__(self, data: str) -> None:
        self.data = data
        self.hash = self.__gen_hash()
    
    def __gen_hash(self) -> str:
        return sha256(self.data.encode()).hex()
    
    def add(self, d) -> str:
        return self.hash + d.hash
