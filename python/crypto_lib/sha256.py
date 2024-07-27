# according to this book, https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf 
# we will follow to develop the sha256 algorithm

import math
from itertools import count, islice
import crypto_lib.bit_ops as ops

def ch(x, y, z):
    return ops.xor_op(ops.and_op(x, y), ops.and_op(ops.not_op(x), z))

def maj(x, y, z):
    return ops.xor_op(ops.xor_op(ops.and_op(x, y), ops.and_op(x, z)), ops.and_op(y, z))

def rotr(x,n):
    return ops.rotate_right_op(x, n)

def sum_rot_r_0(x):
    return ops.xor_op(ops.xor_op(rotr(x, 2), rotr(x, 13)), rotr(x, 22))

def sum_rot_r_1(x):
    return ops.xor_op(ops.xor_op(rotr(x, 6), rotr(x, 11)), rotr(x, 25))

def sig_rot_r_0(x):
    return ops.xor_op(ops.xor_op(rotr(x, 7), rotr(x, 18)), ops.shift_right_op(x, 3))

def sig_rot_r_1(x):
    return ops.xor_op(ops.xor_op(rotr(x, 17), rotr(x, 19)), ops.shift_right_op(x, 10))

def is_prime(n):
    return not any(f for f in range(2,int(math.sqrt(n))+1) if n%f == 0)

def b2i(b):
    return int.from_bytes(b, 'big')

def i2b(i):
    return i.to_bytes(4, 'big')

def first_n_primes(n):
    return islice(filter(is_prime, count(start=2)), n)

def frac_bin(f, n=32):
    f -= math.floor(f)
    f *= 2**n
    f = int(f)
    return f

def sha256_constants(n=8):
    return [ frac_bin(f ** (1/3.0)) for f in first_n_primes(n) ]

def initial_hashes():
    return [ frac_bin(f ** (1/2.0)) for f in first_n_primes(8) ]

# preprocessing the message, section 6

def pad_message(m):
    m = bytearray(m)
    m_len = len(m) * 8
    m.append(0b10000000)
    
    # padding till its in the multiple of 512
    while (len(m) * 8) % 512 != 448:
        m.append(0x00)

    m.extend(m_len.to_bytes(8, 'big'))

    return m

def sha256(m):
    pad = pad_message(m)
    k = sha256_constants(64)
    H = initial_hashes()

    blocks = [pad[i:i+64] for i in range(0, len(pad), 64)]

    for M in blocks:
        W = []

        for t in range(64):
            if t <= 15:
                W.append(
                    bytes(M[t*4: t*4+4])
                )
            else:
                t1 = sig_rot_r_1(b2i(W[t-2]))
                t2 = b2i(W[t-7])
                t3 = sig_rot_r_0(b2i(W[t-15]))
                t4 = b2i(W[t-16])

                t = (t1+t2+t3+t4) % 2**32
                W.append(i2b(t))
            
        a,b,c,d,e,f,g,h = H

        for t in range(64):
            T1 = (h + sum_rot_r_1(e) + ch(e, f, g) + k[t] + b2i(W[t])) % 2**32
            T2 = (sum_rot_r_0(a) + maj(a, b, c)) % 2**32

            h=g
            g=f
            f=e
            e=(d+T1) % 2**32
            d=c
            c=b
            b=a
            a=(T1+T2) % 2**32

        delta = [a, b, c, d, e, f, g, h]
        H = [(i1 + i2) % 2**32 for i1,i2 in zip(H, delta)]
    
    return b''.join(i2b(i) for i in H)
