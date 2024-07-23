mod cryptography;

fn main() {
    // let number = 16;
    let file_name = "../testfile.txt";
    let file = std::fs::read(file_name).unwrap();
    let hash = cryptography::sha256::sha256(&file);
    // let hash = cryptography::sha256::sha256_constants(8);
    println!("{:?}", hash);

    cryptography::symmetric::symmetric_aes("blockchain is a way, that keeps centralization away".to_string());
}
