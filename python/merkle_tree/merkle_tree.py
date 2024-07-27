from merkle_tree.merkle_leaf import MerkleLeaf


class MerkleTree:
    def __init__(self, elements) -> None:
        self.elements = elements
        self.tree = list()
        self.__create_tree()

    def __create_tree(self) -> None:
        nodes = list()
        
        e_hashes = [ MerkleLeaf(e) for e in elements ]
        
        if len(e_hashes) % 2 != 0:
            e_hashes.append(e_hashes[-1])
        
        nodes.append(e_hashes)

        while len(e_hashes) > 1:
            
            if len(e_hashes) % 2 != 0:
                e_hashes.append(e_hashes[-1])
            
            e_temp = []
            for x in range(0, len(e_hashes), 2):
                m_leaf = MerkleLeaf(
                    e_hashes[x].add(e_hashes[x+1])
                )
                e_temp.append(m_leaf)
            
            e_hashes = e_temp
            nodes.append(e_hashes)

        self.tree = nodes
    
    def get_tree(self):
        return self.tree

    def get_root(self):
        return self.tree[-1]



elements = [
    "why", "is", "it", "required", "to", "be", "a", "list"
]

# this will take the content as a whole, nice!
with open("../testfile.txt") as f:
    elements.append(f.read())

merkle_tree = MerkleTree(elements=elements)
print(merkle_tree.get_root()[0].hash)