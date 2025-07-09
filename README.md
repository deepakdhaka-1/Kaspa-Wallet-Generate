# 🧬 Kaspa Wallet Generator CLI

A simple yet powerful command-line tool to generate one or many **Kaspa-compatible wallets** using BIP39 mnemonics and BIP32 derivation with `secp256k1`. Generates full wallet details including **mnemonic**, **private key**, **compressed public key**, and **Kaspa address** using the correct **Bech32m** format.

---

## ⚙️ Features

- 🔐 Generates secure 24-word BIP39 mnemonics
- 📈 Supports custom number of wallets via CLI prompt
- 🧠 HD derivation using `m/44'/111111'/0'/0/i`
- ⚡ Fast and lightweight (under 2 seconds for 50 wallets)
- ✨ Kaspa Bech32m address encoding using custom BLAKE2b logic
- 💾 Outputs all wallet data to clean, readable `wallets.txt`
- 🧰 Easily extendable for batch sends, CSV exports, or QR code gen

---

## 📦 Installation

```bash
git clone https://github.com/deepakdhaka-1/kaspa-wallet-cli.git
cd kaspa-wallet-cli
pip install -r requirements.txt
````
---

## Main command
```bash
python3 main.py
# or
python main.py

