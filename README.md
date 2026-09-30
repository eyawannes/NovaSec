# 🔐 NovaSec

### Secure Authentication & Cryptography Web Application

NovaSec is a cybersecurity web application developed with **Python and Flask**, designed to demonstrate secure authentication mechanisms and fundamental cryptographic operations through a modern and intuitive web interface.

The project combines **web security, authentication, password protection and cryptography** in a single educational application.

---

## 🎯 Project Overview

NovaSec provides a practical environment for experimenting with several security mechanisms:

* 🔐 Secure user authentication
* 🔑 Password hashing
* #️⃣ SHA-256 hashing
* 🔒 AES-256-GCM encryption and decryption
* 🔐 RSA-2048 encryption and decryption
* 🎲 Secure password generation
* 🗄️ User management with SQLite
* 🛡️ Protected application routes

The main objective is to understand how these security mechanisms can be integrated into a web application using Python.

---

## ✨ Features

### 🔐 User Authentication

NovaSec includes a complete authentication system with:

* User registration
* Login / logout
* Password confirmation
* Password hashing
* Protected dashboard
* Session management
* Unique email verification

Passwords are never stored as plaintext. They are processed using secure password hashing mechanisms provided by **Werkzeug**.

---

### #️⃣ SHA-256

The SHA-256 module allows users to generate the cryptographic hash of a text.

**Example:**

```text
Input:
Bonjour NovaSec

Output:
SHA-256 hexadecimal hash
```

SHA-256 is a cryptographic hash function commonly used for integrity verification and other security applications.

---

### 🔒 AES-256-GCM

NovaSec provides symmetric encryption using:

* AES-256
* GCM authentication mode
* PBKDF2-HMAC-SHA256
* Random salt
* Random nonce
* 600,000 PBKDF2 iterations

The application supports:

```text
Plaintext
    ↓
PBKDF2 key derivation
    ↓
AES-256-GCM encryption
    ↓
Base64 encoded ciphertext
```

The same password can then be used to decrypt the generated ciphertext.

---

### 🔐 RSA-2048

NovaSec also demonstrates asymmetric cryptography using:

* RSA-2048
* Public/private key pairs
* OAEP padding
* SHA-256
* MGF1

The application can:

1. Generate an RSA key pair
2. Encrypt data with the public key
3. Decrypt data with the private key

> **Note:** The current RSA implementation is primarily educational. RSA-OAEP is intended for relatively small data payloads. A production system would typically use hybrid encryption, combining AES for the data and RSA for protecting the AES key.

---

### 🎲 Secure Password Generator

NovaSec includes a secure password generator based on Python's `secrets` module.

Users can configure:

* Password length
* Lowercase letters
* Uppercase letters
* Numbers
* Symbols

The password length can be configured between **8 and 64 characters**.

---

## 🛠️ Technologies

### Backend

* **Python 3.12+**
* **Flask**
* **Flask-Login**
* **Flask-SQLAlchemy**
* **Werkzeug**

### Cryptography

* **cryptography**
* AES-256-GCM
* RSA-2048
* OAEP
* SHA-256
* PBKDF2-HMAC-SHA256
* Python `secrets`

### Database

* SQLite
* SQLAlchemy

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2

---

## 📁 Project Structure

```text
NovaSec/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── hash.html
│   ├── aes.html
│   ├── rsa.html
│   └── password_generator.html
│
└── instance/
    └── novasec.db
```

> The `instance/` directory and database are excluded from version control using `.gitignore`.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/eyawannes/NovaSec.git
cd NovaSec
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

### 4. Run the application

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## 🧪 Testing the Application

After starting NovaSec, the main workflow is:

### Registration

1. Open the application.
2. Create a new account.
3. Enter your first name, last name, email and password.
4. Confirm the password.

### Authentication

1. Go to the login page.
2. Enter your credentials.
3. Access the protected dashboard.

### SHA-256

Enter a text and generate its SHA-256 hash.

### AES

1. Enter plaintext.
2. Enter an encryption password.
3. Select **Encrypt**.
4. Copy the generated ciphertext.
5. Select **Decrypt**.
6. Enter the same password.
7. Verify that the original plaintext is recovered.

### RSA

1. Generate an RSA key pair.
2. Copy the public key.
3. Encrypt a small text.
4. Copy the ciphertext.
5. Use the private key to decrypt it.
6. Verify the original message.

### Password Generator

Select the desired character categories and generate a secure password.

---

## 🔐 Security Considerations

NovaSec is designed as an educational and portfolio cybersecurity project.

The application demonstrates several important security concepts:

* Password hashing instead of plaintext storage
* Authentication and protected routes
* Cryptographic hashing
* Symmetric encryption
* Asymmetric encryption
* Authenticated encryption with AES-GCM
* Password-based key derivation
* Random salts and nonces
* Secure random password generation
* Separation of application code and sensitive local data

### Important

This project is currently intended for **educational and demonstration purposes**.

Before using a similar architecture in a production environment, additional security controls should be implemented, including:

* Environment-based secret management
* CSRF protection
* Stronger input validation
* Secure cookie configuration
* HTTPS
* Rate limiting
* Security logging and monitoring
* Proper key management
* Secure private-key storage
* Production WSGI server configuration
* Security headers
* Dependency vulnerability management

---

## 🔑 Cryptographic Design

### Password Protection

```text
User Password
      │
      ▼
Password Hashing
      │
      ▼
Stored Password Hash
```

### AES Encryption

```text
Password
    │
    ▼
PBKDF2-HMAC-SHA256
    │
    ▼
256-bit AES Key
    │
    ▼
AES-256-GCM
    │
    ▼
Encrypted Data
```

### RSA Encryption

```text
                 RSA Key Generation
                        │
                ┌───────┴───────┐
                ▼               ▼
          Public Key        Private Key
                │               │
                ▼               │
             Encrypt            │
                │               │
                ▼               ▼
             Ciphertext ────► Decrypt
                                │
                                ▼
                             Plaintext
```

---

## 📌 Current Status

**Project status:** 🚧 Active development

Current modules:

* [x] User registration
* [x] User login/logout
* [x] Password hashing
* [x] Protected dashboard
* [x] SHA-256
* [x] AES-256-GCM
* [x] RSA-2048
* [x] Secure password generator
* [x] SQLite database
* [x] Responsive user interface
* [ ] CSRF protection
* [ ] Security headers
* [ ] Rate limiting
* [ ] Environment-based configuration
* [ ] Hybrid encryption
* [ ] Security audit

---

## 🎓 Project Context

NovaSec was developed as a cybersecurity-focused application to explore the practical integration of **authentication, cryptography and secure web development**.

The project is particularly focused on understanding how theoretical security concepts can be implemented in a functional Python web application.

---

## 👩‍💻 Author

**Wanes Eya**

Cybersecurity & Network Engineering Student
TEK-UP University — Tunisia

### Areas of Interest

* 🛡️ SOC / Blue Team
* 🔐 Cybersecurity
* ⚙️ DevSecOps
* ☁️ Cloud Security
* 🤖 AI for Cybersecurity
* 🔑 Cryptography

---

## 📄 License

This project is intended primarily for educational and portfolio purposes.

A specific open-source license can be added in a future version.

---

## ⭐ Acknowledgements

Built with:

* Python
* Flask
* Flask-Login
* Flask-SQLAlchemy
* Werkzeug
* Cryptography
* SQLite

---

**NovaSec — Secure by design, built to learn. 🔐**
