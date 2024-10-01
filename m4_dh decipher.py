from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

mod = 991 
base = 6
a_public = 299 
b_public = 925 

def find_private_key(base, public_value, mod):
    for secret in range(1, 990):
        if pow(base, secret, mod) == public_value:
            return secret
    return None

a_secret = find_private_key(base, a_public, mod)

if a_secret is None:
    print("Failed to find A's private key!")
    exit()

shared_secret = pow(b_public, a_secret, mod)

key = SHA256.new(str(shared_secret).encode()).digest()[:16] 

cipher = AES.new(key, AES.MODE_ECB)

# flag = "CS2107{[REDACTED]}"

encrypted_flag_hex = "d94d278d914de2e1196e8d01e799afb451ef30dee5ce170e979c9dde930645be0fe078199219df47e7ffaf05e4605b80"
encrypted_flag = bytes.fromhex(encrypted_flag_hex)

print('=================')
# print('a secret = '+ str(a_secret))
print('Shared Secret = ' + str(shared_secret))
print('Encrypted Flag:', encrypted_flag.hex())

decrypted_flag = unpad(cipher.decrypt(encrypted_flag), AES.block_size)

print('Decrypted Flag:', decrypted_flag.decode())

# =================
# Shared Secret = 270
# Encrypted Flag: d94d278d914de2e1196e8d01e799afb451ef30dee5ce170e979c9dde930645be0fe078199219df47e7ffaf05e4605b80
