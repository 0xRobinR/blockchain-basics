mod cryptography;

fn main() {
    let number = 17;
    let hash = cryptography::sha256::is_prime(number);
    println!("{}", hash);
    println!("{}", 1i32 - 2);
}
