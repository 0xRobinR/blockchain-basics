extern crate hex;

use hex::encode;

fn rotr(x: u32, y: u32) -> u32 {
    (x >> y) | (x << (32 - y))
}

fn ch(x: u32, y: u32, z: u32) -> u32 {
    (x & y) ^ (!x & z)
}

fn maj(x: u32, y: u32, z: u32) -> u32 {
    (x & y) ^ (x & z) ^ (y & z)
}

fn sum_rotr_0(x: u32) -> u32 {
    rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)
}

fn sum_rotr_1(x: u32) -> u32 {
    rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)
}

fn sig_rotr_0(x: u32) -> u32 {
    rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
}

fn sig_rotr_1(x: u32) -> u32 {
    rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)
}

pub fn is_prime(x: u64) -> bool {
    if x <= 1 {
        return false;
    }
    for i in 2..=((x as f64).sqrt() as u64) {
        if x % i == 0 {
            return false;
        }
    }
    true
}

fn b2i(b: &[u8]) -> u32 {
    let mut res = 0;
    for &byte in b {
        res = (res << 8) | byte as u32;
    }
    res
}

fn i2b(x: u32) -> Vec<u8> {
    x.to_be_bytes().to_vec()
}

pub fn first_n_primes(n: usize) -> Vec<u64> {
    let mut res = Vec::new();
    let mut i = 2;
    while res.len() < n {
        if is_prime(i) {
            res.push(i);
        }
        i += 1;
    }
    res
}

fn frac_bin(f: f64, n: u32) -> u32 {
    let mut fractional_part = f - f.floor();
    fractional_part *= 2f64.powi(n as i32);
    fractional_part as u32
}

pub fn sha256_constants(n: usize) -> Vec<u32> {
    first_n_primes(n)
        .iter()
        .map(|&f| frac_bin((f as f64).powf(1.0 / 3.0), 32))
        .collect()
}

pub fn initial_hashes() -> Vec<u32> {
    first_n_primes(8)
        .iter()
        .map(|&x| frac_bin((x as f64).sqrt(), 32))
        .collect()
}

fn pad_message(msg: &[u8]) -> Vec<u8> {
    let mut res = Vec::new();
    res.extend_from_slice(msg);
    res.push(0x80);
    while (res.len() * 8) % 512 != 448 {
        res.push(0);
    }
    res.extend_from_slice(&(msg.len() as u64 * 8).to_be_bytes());
    res
}

pub fn sha256(msg: &[u8]) -> String {
    let k = sha256_constants(64);
    let mut h = initial_hashes();
    let padded_msg = pad_message(msg);
    for chunk in padded_msg.chunks(64) {
        let mut w = vec![0u32; 64];
        for (i, word) in chunk.chunks(4).enumerate() {
            w[i] = b2i(word);
        }
        for i in 16..64 {
            w[i] = sig_rotr_1(w[i - 2])
                .wrapping_add(w[i - 7])
                .wrapping_add(sig_rotr_0(w[i - 15]))
                .wrapping_add(w[i - 16]);
        }
        let mut a = h[0];
        let mut b = h[1];
        let mut c = h[2];
        let mut d = h[3];
        let mut e = h[4];
        let mut f = h[5];
        let mut g = h[6];
        let mut h7 = h[7];
        for i in 0..64 {
            let t1 = h7
                .wrapping_add(sum_rotr_1(e))
                .wrapping_add(ch(e, f, g))
                .wrapping_add(k[i])
                .wrapping_add(w[i]);
            let t2 = sum_rotr_0(a).wrapping_add(maj(a, b, c));
            h7 = g;
            g = f;
            f = e;
            e = d.wrapping_add(t1);
            d = c;
            c = b;
            b = a;
            a = t1.wrapping_add(t2);
        }
        h[0] = h[0].wrapping_add(a);
        h[1] = h[1].wrapping_add(b);
        h[2] = h[2].wrapping_add(c);
        h[3] = h[3].wrapping_add(d);
        h[4] = h[4].wrapping_add(e);
        h[5] = h[5].wrapping_add(f);
        h[6] = h[6].wrapping_add(g);
        h[7] = h[7].wrapping_add(h7);
    }
    let mut res = Vec::new();
    for &val in &h {
        res.extend_from_slice(&val.to_be_bytes());
    }
    encode(res)
}