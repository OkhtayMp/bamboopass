# 🔐 BambooPass — Deterministic Password Generator (GUI)

<img alt="Version" src="https://img.shields.io/github/v/release/okhtaymp/bamboopass?style=for-the-badge&color=ff6fff">


BambooPass is a tiny, cross‑platform **GUI** tool that generates **strong, deterministic passwords**.

**Deterministic** means:
- If you enter the **same Key** + **same Seed (e.g., site/domain)** + the same settings (**Iterations / Length**),
  you will always get the **same password**.  
  (So you don’t need a password database.)

✅ **Privacy by design**
- BambooPass **does not store** your Key, Seed, or generated passwords.
- The password is created locally on your device and copied to your clipboard.
- The only thing BambooPass may save is **optional app settings** (like background color, iterations, length, clipboard timer) in a small `settings.json` file.
---


##  💻 Supported Platforms
<img alt="Windows" src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4OCA4OCI+PHJlY3QgeD0iMCIgeT0iMCIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBmaWxsPSIjRkZGRkZGIi8+PHJlY3QgeD0iNDgiIHk9IjAiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgZmlsbD0iI0ZGRkZGRiIvPjxyZWN0IHg9IjAiIHk9IjQ4IiB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiNGRkZGRkYiLz48cmVjdCB4PSI0OCIgeT0iNDgiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgZmlsbD0iI0ZGRkZGRiIvPjwvc3ZnPg==&logoColor=white">
<img alt="macOS" src="https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white">
<img alt="Linux" src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">


---

## ✨ Features
- **Deterministic password derivation** using PBKDF2-HMAC-SHA256 :contentReference[oaicite:3]{index=3}
- **Two-step input**: first **Key**, then **Seed (domain/site)** :contentReference[oaicite:4]{index=4}
- Password is **auto-copied to clipboard** :contentReference[oaicite:5]{index=5}
- App hides after copying, and **closes automatically when you copy something else**  
  (it also restores your previous clipboard content if it was replaced by the generated password) :contentReference[oaicite:6]{index=6}
- `/set` command opens settings window (iterations, length, colors, clipboard timer) :contentReference[oaicite:7]{index=7}
- **Single-file binaries** for downloads (no installer) :contentReference[oaicite:8]{index=8}

---

## 🚀 Downloads

| Platform       | Download | SHA256SUMS |
|----------------|----------|------------|
| ![Static Badge](https://img.shields.io/badge/-FCC624?style=plastic&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4OCA4OCI%2BPHJlY3QgeD0iMCIgeT0iMCIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBmaWxsPSIjRkZGRkZGIi8%2BPHJlY3QgeD0iNDgiIHk9IjAiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgZmlsbD0iI0ZGRkZGRiIvPjxyZWN0IHg9IjAiIHk9IjQ4IiB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiNGRkZGRkYiLz48cmVjdCB4PSI0OCIgeT0iNDgiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgZmlsbD0iI0ZGRkZGRiIvPjwvc3ZnPg%3D%3D&logoColor=white&color=blue) **Windows `x64`** | [⬇️ Download][dl-win-x64] | [SHA256][sha-win-x64] |
| ![Static Badge](https://img.shields.io/badge/-FCC624?style=plastic&logo=apple&color=black) **macOS `Intel`** | [⬇️ Download][dl-macos-x64] | [SHA256][sha-macos-x64] |
| ![Static Badge](https://img.shields.io/badge/-FCC624?style=plastic&logo=apple&color=black) **macOS `ARM64`** | [⬇️ Download][dl-macos-arm64] | [SHA256][sha-macos-arm64] |
| ![Static Badge](https://img.shields.io/badge/-FCC624?style=plastic&logo=linux&logoColor=black&color=green) **Linux `x64`** | [⬇️ Download][dl-linux-x64] | [SHA256][sha-linux-x64] |
| ![Static Badge](https://img.shields.io/badge/-FCC624?style=plastic&logo=linux&logoColor=black&color=green) **Linux `ARM64`** | [⬇️ Download][dl-linux-arm64] | [SHA256][sha-linux-arm64] |

> 💡 **Note:** All downloads are **single-file binaries**, ready to run.  
> No installation required. Compatible with modern versions of each platform.

<!-- Latest release (dynamic) -->
[dl-win-x64]: https://github.com/okhtaymp/bamboopass/releases/latest/download/bamboopass-win-x64.exe
[dl-macos-x64]: https://github.com/okhtaymp/bamboopass/releases/latest/download/bamboopass-macos-x64
[dl-macos-arm64]: https://github.com/okhtaymp/bamboopass/releases/latest/download/bamboopass-macos-arm64
[dl-linux-x64]: https://github.com/okhtaymp/bamboopass/releases/latest/download/bamboopass-linux-x64
[dl-linux-arm64]: https://github.com/okhtaymp/bamboopass/releases/latest/download/bamboopass-linux-arm64

<!-- Checksums (also latest) -->
[sha-win-x64]: https://github.com/okhtaymp/bamboopass/releases/latest/download/SHA256SUMS-win-x64.txt
[sha-macos-x64]: https://github.com/okhtaymp/bamboopass/releases/latest/download/SHA256SUMS-macos-x64.txt
[sha-macos-arm64]: https://github.com/okhtaymp/bamboopass/releases/latest/download/SHA256SUMS-macos-arm64.txt
[sha-linux-x64]: https://github.com/okhtaymp/bamboopass/releases/latest/download/SHA256SUMS-linux-x64.txt
[sha-linux-arm64]: https://github.com/okhtaymp/bamboopass/releases/latest/download/SHA256SUMS-linux-arm64.txt



---

## ✅ Verify Download (Recommended)

### Windows (PowerShell)
```powershell
Get-FileHash .\bamboopass-win-x64.exe -Algorithm SHA256
```

### macOS / Linux
```bash
shasum -a 256 ./bamboopass-*
# or
sha256sum ./bamboopass-*
```

Compare the output with the matching `SHA256SUMS-...txt` file from the release assets.

---

## 📚 How to Use (GUI)

### 1) Run BambooPass
- **Windows:** double-click the `.exe`
- **macOS/Linux:** make it executable and run:
```bash
chmod +x ./bamboopass-*
./bamboopass-*
```

### 2) Enter your Key
This is your secret (like a master key). BambooPass does **not** store it.

### 3) Enter your Seed
Example: `google.com`, `github.com`, `mybank`, etc.

### 4) Done ✅
BambooPass generates the password and **copies it to your clipboard**, then hides.

---

## ⚙️ Settings (What gets saved?)
BambooPass can save **only app preferences**, like:
- background color
- iterations
- password length
- clipboard check interval / timer

These are stored in a small JSON file (e.g., `.../BambooPass/settings.json`).  
It **does not** save Key/Seed/password.

---

## 🔐 How passwords are generated
BambooPass derives a password using:
- PBKDF2-HMAC-SHA256
- inputs: `key`, `seed`, `iterations`, `length`
- output: URL-safe Base64 (then trimmed to your chosen length)

---

## 🛡️ Security notes (important)
- Use a **strong Key** (long and secret). Anyone who knows your Key + Seed can reproduce your passwords.
- Choose a consistent Seed format (example: always use the domain name).
- If you change **iterations** or **length**, your generated password will change.
- Clipboard is convenient but sensitive:
  - paste your password, then consider copying something else to clear it.

---

## 🧩 Troubleshooting

### macOS: “App can’t be opened because the developer cannot be verified”
- Right-click the app → **Open** → **Open**
- Or enable it from **System Settings → Privacy & Security**

### Linux/macOS: “Permission denied”
```bash
chmod +x ./bamboopass-*
```

---

<!-- ## 🎥 Video Tutorial
Add your tutorial link here:
[![Watch Tutorial](https://img.shields.io/badge/Watch%20Tutorial-▶️-FF4500?style=for-the-badge)](https://github.com/okhtaymp/bamboopass#video)

--- -->

## 🤝 Contributing
Issues and pull requests are welcome.

---

## 📝 License
This project is licensed under the **GNU Affero General Public License v3.0 (AGPLv3)**.
See the [LICENSE](LICENSE) file for details.
