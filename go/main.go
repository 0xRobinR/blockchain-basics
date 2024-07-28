package main

import (
	"crypto/sha256"
	"encoding/hex"
	"io"
	"os"

	"github.com/0xrobinr/blockchain-stack/go/cryptography"
	"github.com/0xrobinr/blockchain-stack/go/merkleTree"
)

// check against the sha256 generator
func fileSHA256(filePath string) string {
	file, err := os.Open(filePath)
	if err != nil {
		return ""
	}
	defer file.Close()

	hasher := sha256.New()
	if _, err := io.Copy(hasher, file); err != nil {
		return ""
	}

	return hex.EncodeToString(hasher.Sum(nil))
}

func main() {

	// testing sha256 hash function
	dat, error := os.ReadFile("../testfile.txt")
	if error != nil {
		panic(error)
	}

	print(cryptography.Sha256(dat))
	print("\n")
	print(fileSHA256("../testfile.txt"))

	// tesitng symmetric key encryption
	cryptography.SymmetricAES("blockchain is a way, that keeps centralization away")

	// testing merkle tree
	elements := []string{"why", "is", "it", "required", "to", "be", "a", "list", "?"}
	print(merkleTree.NewMerkleTree(elements).GetRoot())
}
