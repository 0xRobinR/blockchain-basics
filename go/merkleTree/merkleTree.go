package merkleTree

type MerkleTree struct {
	leafs []Merkleaf
	tree  [][]Merkleaf
}

func NewMerkleTree(elements []string) *MerkleTree {
	mt := &MerkleTree{}
	mt.buildTree(elements)
	return mt
}

func (mt *MerkleTree) buildTree(elements []string) {
	var leafs []Merkleaf
	for _, e := range elements {
		leafs = append(leafs, CreateMerkleLeaf(e))
	}
	mt.leafs = leafs

	var tree [][]Merkleaf
	tree = append(tree, leafs)

	for len(leafs) > 1 {
		var newLevel []Merkleaf
		if len(leafs)%2 != 0 {
			leafs = append(leafs, leafs[len(leafs)-1])
		}

		for i := 0; i < len(leafs)-1; i += 2 {
			combinedData := leafs[i].hash + leafs[i+1].hash
			newLevel = append(newLevel, CreateMerkleLeaf(combinedData))
		}
		tree = append(tree, newLevel)
		leafs = newLevel
	}
	mt.tree = tree
}

func (mt *MerkleTree) GetRoot() string {
	if len(mt.tree) == 0 {
		return ""
	}
	return mt.tree[len(mt.tree)-1][0].hash
}
