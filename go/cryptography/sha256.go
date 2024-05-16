package cryptography

import (
	"encoding/binary"
	"encoding/hex"
	"math"
)

func rotr(x uint32, n uint32) uint32 {
	return (x >> n) | (x << (32 - n))
}

func ch(x uint32, y uint32, z uint32) uint32 {
	return (x & y) ^ (^x & z)
}

func maj(x uint32, y uint32, z uint32) uint32 {
	return (x & y) ^ (x & z) ^ (y & z)
}

func sumRotr0(x uint32) uint32 {
	return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)
}

func sumRotr1(x uint32) uint32 {
	return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)
}

func sigRotr0(x uint32) uint32 {
	return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
}

func sigRotr1(x uint32) uint32 {
	return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)
}

func isPrime(x int) bool {
	if x <= 1 {
		return false
	}
	for f := 2; float64(f) <= math.Sqrt(float64(x)); f++ {
		if x%f == 0 {
			return false
		}
	}
	return true
}

func fracBin(f float64, n uint32) uint32 {
	return uint32((f - math.Floor(f)) * math.Pow(2, float64(n)))
}

func firstNPrimes(n int) []uint32 {
	primes := make([]uint32, 0, n)
	for i := 2; len(primes) < n; i++ {
		if isPrime(i) {
			primes = append(primes, uint32(i))
		}
	}
	return primes
}

func sha256Constants(n int) []uint32 {
	primes := firstNPrimes(n)
	constants := make([]uint32, n)
	for i, prime := range primes {
		constants[i] = fracBin(math.Pow(float64(prime), 1/3.0), 32)
	}
	return constants
}

func initialHashes() []uint32 {
	primes := firstNPrimes(8)
	hashes := make([]uint32, 8)
	for i, prime := range primes {
		hashes[i] = fracBin(math.Pow(float64(prime), 0.5), 32)
	}
	return hashes
}

func padMessage(m []byte) []byte {
	originalLength := len(m)
	m = append(m, 0x80) // Append the bit '1' to the message

	paddingLength := ((448 - (originalLength*8+1)%512) + 512) % 512
	padding := make([]byte, paddingLength/8)
	m = append(m, padding...)

	lengthBits := uint64(originalLength * 8)
	lengthBytes := make([]byte, 8)
	binary.BigEndian.PutUint64(lengthBytes, lengthBits)
	m = append(m, lengthBytes...)

	return m
}

func Sha256(message []byte) string {
	k := sha256Constants(64)
	H := initialHashes()

	pad := padMessage(message)
	var blocks [][]byte
	for i := 0; i < len(pad); i += 64 {
		blocks = append(blocks, pad[i:i+64])
	}

	for _, block := range blocks {
		var W [64]uint32
		for t := 0; t < 16; t++ {
			W[t] = binary.BigEndian.Uint32(block[t*4 : t*4+4])
		}
		for t := 16; t < 64; t++ {
			W[t] = sigRotr1(W[t-2]) + W[t-7] + sigRotr0(W[t-15]) + W[t-16]
		}

		a, b, c, d, e, f, g, h := H[0], H[1], H[2], H[3], H[4], H[5], H[6], H[7]

		for t := 0; t < 64; t++ {
			T1 := h + sumRotr1(e) + ch(e, f, g) + k[t] + W[t]
			T2 := sumRotr0(a) + maj(a, b, c)
			h, g, f, e, d, c, b, a = g, f, e, d+T1, c, b, a, T1+T2
		}

		H[0] += a
		H[1] += b
		H[2] += c
		H[3] += d
		H[4] += e
		H[5] += f
		H[6] += g
		H[7] += h
	}

	finalHash := make([]byte, 0, 32)
	for _, h := range H {
		finalHash = append(finalHash, byte(h>>24), byte(h>>16), byte(h>>8), byte(h))
	}

	hexString := hex.EncodeToString(finalHash)

	return hexString
}
