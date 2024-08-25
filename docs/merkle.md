## overview

merkle tree me ek tree hota hai jisme har node ke 2 children hote hain. ye tree binary tree hota hai. ye tree cryptographic hash values ko store karta hai

ye tree data integrity ko verify karne ke liye aur data structure me use hota hai. ye tree me root node hota hai jo ki sabse upar hota hai. root node ke children nodes ko leaf nodes kehte hain

leaf nodes me data hote hai joh data ka hash calculate karke parent node me store karte hain. parent node ke hash calculate karke grandparent node me store karte hain. is tarah se tree me upar ki taraf jate jate root node me pahuchte hain. root node ka hash calculate karke verify karte hain ki data me koi change to nahi hua hai

```
        Root
        /  \
     H12    H34
     / \    / \
   H1  H2  H3  H4
   |   |   |   |
 Tx1 Tx2 Tx3 Tx4
```

