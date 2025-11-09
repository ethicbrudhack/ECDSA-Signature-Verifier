# ECDSA Signature Verifier — README (English)

**Purpose**  
This tiny script verifies whether a candidate private key `d` and nonce `k` reproduce an existing ECDSA signature `(r, s)` for a given message hash `z` on the SECP256k1 curve. It is a verification utility — useful in controlled research or defensive scenarios where you *already* possess or legally obtained candidate key material and want to confirm it matches a known transaction signature.

> ⚠️ **Ethics & legality:** Do **not** use this script to attempt to validate or recover keys from addresses or transactions you do not own or do not have explicit permission to test. Unauthorized key recovery or misuse may be illegal.

---

## What the script does (high-level)

1. Loads SECP256k1 group parameters `n` (group order) and `G` (generator point) from the `ecdsa` Python package.
2. Takes the original signature components `original_r`, `original_s`, and the message hash `original_z` (all integers).
3. Accepts candidate values `found_d` (private key) and `found_k` (nonce).
4. Recomputes the ECDSA signature:
   - Compute the curve point `R = k * G`.
   - `r' = R.x() mod n`.
   - `s' = k^{-1} * (z + d * r') mod n` (where `k^{-1}` is the modular inverse of `k` modulo `n`).
5. Compares the recomputed `(r', s')` with the original `(r, s)`.
6. Prints a clear success/failure message and the values when the match is found.

If the recomputed values match the original, the script confirms that the provided `d` and `k` are correct for the given transaction data.

---

## Why this matters (short note)

In ECDSA, if an attacker recovers the nonce `k` used for a signature, or if the same nonce is reused across signatures, the private key `d` can be trivially recovered. This script is a *verification tool* you can use in a lab or a forensic context to confirm whether a candidate `(d, k)` pair indeed explains a signature.

---

## Math (formulae)

- `R = k * G` (elliptic-curve scalar multiply)  
- `r = R.x mod n`  
- `s = k^{-1} * (z + d * r) mod n`  
- where `k^{-1}` is the modular inverse of `k` modulo `n`, and `z` is the integer message hash used when signing.

---

## Requirements

- Python 3.7+
- `ecdsa` (for SECP256k1 parameters and point arithmetic)  
  ```bash
  pip install ecdsa
sympy (for mod_inverse)

pip install sympy


The script uses sympy.mod_inverse to compute modular inverses. You can substitute any equivalent routine if preferred.

How to run

Put the script content into, e.g., verify_signature.py.

Ensure original_r, original_s, original_z, found_d and found_k are set to integers (the script already has example values).

Execute:

python verify_signature.py

Example expected output

If the provided d and k match:

✅ `d` and `k` are correct!
🔑 Private key (d): 104865245422780742317661698281795113237740491032990043284880468042140587361278
🔹 Nonce (k): 19935933408528497393901827013443190286268196962253962161630081503206371081493


If they do not match:

❌ `d` and `k` are incorrect; found values do not match the transaction.
🔍 Expected r: 305174467769216030...
🔍 Computed r': 123...
🔍 Expected s: 7562981208140061...
🔍 Computed s': 456...

Security & operational notes

Keep any private keys (d) and recovered nonces (k) strictly private. If they are valid, revealing them compromises funds.

This script does not attempt key recovery; it only verifies a candidate pair. Key recovery techniques require additional code and strong ethical justification — do not pursue without authorization.

Ensure integer inputs are exact — ECDSA arithmetic is sensitive to any change in the message hash z or signature components.

Extending the tool

Add DER/hex parsing to accept signatures in standard formats (DER or hex), or accept message preimages and compute z = HASH(message).

Replace sympy.mod_inverse with a faster algorithm or use built-in modular inverse available in recent Python versions: pow(k, -1, n).

Add unit tests to verify behavior on known test vectors.

Final remark

This is a small, focused utility: given a claimed private key and nonce, it tells you whether they reproduce a particular ECDSA signature on SECP256k1. Use it responsibly and only in contexts where you have explicit permission to handle or verify private key material.

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
