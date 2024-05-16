
class MerkleLeaf:
    def __init__(self, data) -> None:
        self.hash = self.calc_hash(data)
    
    