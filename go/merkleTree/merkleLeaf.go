package merkleTree

import (
	"github.com/0xrobinr/blockchain-stack/go/cryptography"
)

type Merkleaf struct {
	data string
	hash string
}

func CreateMerkleLeaf(data string) (node Merkleaf) {
	hash := cryptography.Sha256([]byte(data))

	node = Merkleaf{
		data: data,
		hash: hash,
	}

	return node
}
