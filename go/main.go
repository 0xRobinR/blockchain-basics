package main

import (
	"crypto/sha256"
	"encoding/hex"
	"io"
	"os"

	"github.com/0xrobinr/blockchain-stack/go/cryptography"
)

func main() {
	dat, error := os.ReadFile("../testfile.txt")
	if error != nil {
		panic(error)
	}

	print(cryptography.Sha256(dat))
	print("\n")
	print(fileSHA256("../testfile.txt"))

	cryptography.SymmetricAES("blockchain is a way, that keeps centralization away")
}

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
