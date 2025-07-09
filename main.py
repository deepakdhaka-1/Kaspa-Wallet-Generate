from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip32Slip10Secp256k1
import hashlib

# --- Bech32m Implementation for Kaspa ---
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

def bech32_polymod(values):
    GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = (chk >> 25)
        chk = ((chk & 0x1ffffff) << 5) ^ v
        for i in range(5):
            if ((b >> i) & 1):
                chk ^= GEN[i]
    return chk

def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]

def bech32_create_checksum(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 0x2bc830a3
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

def bech32_encode(hrp, data):
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + ':' + ''.join([CHARSET[d] for d in combined])

def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    for value in data:
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad and bits:
        ret.append((acc << (tobits - bits)) & maxv)
    return ret

def kaspa_address(pub_key_bytes):
    blake = hashlib.blake2b(digest_size=20)
    blake.update(pub_key_bytes)
    pub_key_hash = blake.digest()
    data = convertbits(pub_key_hash, 8, 5)
    return bech32_encode('kaspa', data)

def generate_wallets(n):
    wallets = []
    for i in range(n):
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(24)
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        path = f"m/44'/111111'/0'/0/{i}"
        bip32_ctx = Bip32Slip10Secp256k1.FromSeed(seed_bytes)
        derived = bip32_ctx.DerivePath(path)
        priv_key = derived.PrivateKey().Raw().ToHex()
        pub_key_bytes = derived.PublicKey().RawCompressed().ToBytes()
        pub_key_hex = derived.PublicKey().RawCompressed().ToHex()
        address = kaspa_address(pub_key_bytes)

        wallets.append({
            "mnemonic": mnemonic,
            "private_key": priv_key,
            "public_key": pub_key_hex,
            "address": address
        })
    return wallets

def main():
    print("🔐 Kaspa Wallet Generator CLI")
    try:
        count = int(input("👉 Enter number of wallets to generate: "))
        if count <= 0:
            raise ValueError
    except ValueError:
        print("❌ Please enter a valid positive integer.")
        return

    print(f"\n⏳ Generating {count} Kaspa wallets...\n")
    wallets = generate_wallets(count)

    with open("wallets.txt", "w") as f:
        for idx, w in enumerate(wallets, 1):
            f.write(f"Wallet {idx}\n")
            f.write(f"Mnemonic: {w['mnemonic']}\n")
            f.write(f"Private Key (hex): {w['private_key']}\n")
            f.write(f"Public Key (compressed hex): {w['public_key']}\n")
            f.write(f"Kaspa Address: {w['address']}\n")
            f.write("-" * 60 + "\n")

    print(f"✅ {count} wallets saved to wallets.txt")

if __name__ == "__main__":
    main()
