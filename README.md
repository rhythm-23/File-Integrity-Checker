# File-Integrity-Checker
# 🔥File Integrity Checker

*COMPANY*: CODTECH IT SOLUTIONS

*NAME*: RHYTHM BAHUGUNA

*INTERN ID*: CT06DF2351

*DOMAIN*: CYBERSECURITY & ETHICAL HACKING

*DURATION*: 6 WEEKS

*MENTOR*: NEELA SANTOSH

A secure, OTP-authenticated web application that helps users **verify file integrity** by comparing the SHA-256 hash of uploaded files against previously stored values. Designed with a modern Material Design-inspired UI and a warm autumn-themed palette, it's a lightweight yet powerful utility for ensuring files remain unaltered.

---

## 📌 Features

- ✅ User Registration & Login (with email + OTP)
- 📧 Email-based OTP verification via Flask-Mail
- 🧾 Upload files and automatically compute SHA-256 hash
- 🔒 Compare file hashes for integrity (New / Unchanged / Modified)
- 🧠 Secure session handling with Flask
- 💾 Lightweight JSON storage (no database required)
- 🎨 Clean, modern UI with Material Design + warm tones

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.7+
- Flask
- Flask-Mail
- python-dotenv

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 📁 Project Structure

```
deephlare/
├── app.py
├── email_utils.py
├── users.json
├── hash_db.json
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── verify.html
│   └── result.html
├── static/
│   └── style.css
├── monitored_files/
├── .env
└── requirements.txt
```

---

## 🔐 .env Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_flask_secret_key
MAIL_SERVER=smtp.your-email.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
```

---

## ⚙️ Running the App

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## ✅ Hash Status Meanings

- **New File** – Uploaded for the first time.
- **Unchanged** – File has not been altered since last check.
- **Modified** – The file content has changed (hash mismatch).

---

## 🧠 Tech Stack

- Flask (Python)
- Flask-Mail
- HTML5, CSS3 (Material Design Inspired)
- JSON (for user and hash storage)

