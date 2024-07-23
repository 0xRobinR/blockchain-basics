extern crate aes_gcm;
extern crate hex_literal;

use aes_gcm::aead::{Aead, KeyInit, OsRng};
use aes_gcm::{AeadCore, Aes256Gcm};

pub fn symmetric_aes(msg: String) {
    let key = Aes256Gcm::generate_key(&mut OsRng);
    let cipher = Aes256Gcm::new(&key);

    let plaintext = msg.into_bytes();
    let nonce = Aes256Gcm::generate_nonce(&mut OsRng);
    let ciphertext = cipher.encrypt(&nonce, plaintext.as_ref()).expect("encryption failure!");
    println!("Encrypted: {}", hex::encode(&ciphertext));
    let decrypted = cipher.decrypt(&nonce, ciphertext.as_ref()).expect("decryption failure!");
    println!("Decrypted: {}", String::from_utf8(decrypted).expect("invalid UTF-8"));
}
