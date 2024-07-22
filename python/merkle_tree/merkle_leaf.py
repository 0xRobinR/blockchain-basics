
import hashlib


class MerkleLeaf:
    def __init__(self, data) -> None:
        self.hash = self.calc_hash(data)
    
    def calc_hash(self, data):
        return hashlib.sha256(data.encode()).hexdigest()