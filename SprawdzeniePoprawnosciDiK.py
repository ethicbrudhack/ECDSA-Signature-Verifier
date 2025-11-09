import hashlib
from sympy import mod_inverse

# 🔹 PARAMETRY SECP256K1
n = ecdsa.SECP256k1.order
G = ecdsa.SECP256k1.generator

# 🔹 Oryginalne wartości r, s, z z transakcji
original_r = 30517446776921603025302355353044518586830452579220276958442399051475870431529
original_s = 75629812081400613504585207558174586814758543200330686585047140402941242250964
original_z = 106565664217024123360594287132333196670110176958573928561036895228156732642970

# 🔹 Klucz prywatny (d) i k, które znaleźliśmy
found_d = 104865245422780742317661698281795113237740491032990043284880468042140587361278
found_k = 19935933408528497393901827013443190286268196962253962161630081503206371081493

# 🔹 Funkcja generowania r i s
def generate_signature(z, k, d):
    R = k * G
    r_prime = R.x() % n
    if r_prime == 0:
        return None, None  # Błąd

    k_inv = mod_inverse(k, n)
    s_prime = (k_inv * (z + d * r_prime)) % n

    return r_prime, s_prime

# 🔹 Generujemy (r', s') dla znalezionego `d` i `k`
r_prime, s_prime = generate_signature(original_z, found_k, found_d)

# 🔹 Sprawdzamy, czy zgadza się z oryginalnymi danymi transakcji
if r_prime == original_r and s_prime == original_s:
    print("✅ `d` i `k` są poprawne!")
    print(f"🔑 Klucz prywatny (d): {found_d}")
    print(f"🔹 Wartość k: {found_k}")
else:
    print("❌ `d` i `k` są błędne, znalezione wartości nie pasują do transakcji.")
    print(f"🔍 Oczekiwane r: {original_r}, Obliczone r': {r_prime}")
    print(f"🔍 Oczekiwane s: {original_s}, Obliczone s': {s_prime}")