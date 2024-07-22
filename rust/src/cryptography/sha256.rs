fn rotr(x: i32, y: i32) -> i32 {
    return (x >> y) | (x << (32 - y));
}

fn ch(x: i32, y: i32, z: i32) -> i32 {
    return (x & y) ^ (!x & z);
}

fn maj(x: i32, y: i32, z: i32) -> i32 {
    return (x & y) ^ (y & z) ^ (x & z);
}

fn sum_rotr_0(x: i32) -> i32 {
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22);
}

fn sum_rotr_1(x: i32) -> i32 {
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25);
}

fn sig_rotr_0(x: i32) -> i32 {
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3);
}

fn sig_rotr_1(x: i32) -> i32 {
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10);
}

pub fn is_prime(x: i32) -> bool {
    if x <= 1 {
        return false;
    }
    for i in 2..x {
        if x % i == 0 {
            return false;
        }
    }

    return true;
}
