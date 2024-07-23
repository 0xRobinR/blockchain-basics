package cryptography

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io"
)

func symmetricAES(msg string) {
	key := []byte("examplekey123456")
	plaintext := []byte(msg)

	ciphertext, err := encrypt(key, plaintext)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Encrypted: %s\n", base64.StdEncoding.EncodeToString(ciphertext))

	decrypted, err := decrypt(key, ciphertext)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Decrypted: %s\n", string(decrypted))
}

func encrypt(key, text []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	ciphertext := make([]byte, aes.BlockSize+len(text))
	iv := ciphertext[:aes.BlockSize]
	if _, err := io.ReadFull(rand.Reader, iv); err != nil {
		return nil, err
	}

	stream := cipher.NewCFBEncrypter(block, iv)
	stream.XORKeyStream(ciphertext[aes.BlockSize:], text)

	return ciphertext, nil
}

func decrypt(key, text []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	if len(text) < aes.BlockSize {
		return nil, fmt.Errorf("ciphertext too short")
	}
	iv := text[:aes.BlockSize]
	text = text[aes.BlockSize:]

	stream := cipher.NewCFBDecrypter(block, iv)
	stream.XORKeyStream(text, text)

	return text, nil
}
