# Password Manager CLI

A secure password manager with storage and generation capabilities.

## Features

- 🔒 Secure password storage with AES-256 encryption
- 🔑 Master password protection with Argon2 hashing
- 🛠️ Password generation with customizable complexity
- 📂 Organized storage with website/email metadata
- 🔍 Filterable password entries
- 📊 Rich terminal interface for viewing entries

## Installation

1. Install Poetry (if not already installed):
```bash
pip install poetry
```

2. Clone the repository and install dependencies:
```bash
git clone https://github.com/huelight/password-cli.git
cd password-manager
poetry install
```

3. Make the CLI globally available:
```bash
poetry build
pip install dist/password_manager-*.whl
```


## Usage

Initialize the Password Manager
Before using the manager, you need to set up a master password:
```bash
pwdgen init
```

Save a New Password Entry
Save a new password with optional generation:
```bash
pwdgen save --website example.com --email user@example.com [--password "mypassword" | --generate]
```

List Password Entries
View stored passwords with filtering options:
```bash
pwdgen list [--website example.com] [--show-password]
```

Generate Secure Passwords
Generate passwords without saving:
```bash
pwdgen generate [--length 16] [--no-special]
```

## Command Reference
```
pwdgen init
```
Initialize the password manager with a master password.

Options:

- No additional options

Example:
```bash
pwdgen init
```

```
pwdgen save
```
Save a new password entry.

Options:

Option | Description
-------|------------
--website | Website or service name (required)
--email | Associated email (required)
--password | Password to store (optional)
--generate | Generate secure password (optional)

Examples:
```bash
# Save with manual password
pwdgen save --website example.com --email user@example.com --password "secure123!"

# Save with generated password
pwdgen save --website example.com --email user@example.com --generate
```

```
pwdgen list
```
List stored password entries.

Options:
Option | Description
-------|------------
--website | Filter by website name (optional)
--show-password | Show decrypted passwords (optional)

Examples:
```bash
# List all entries
pwdgen list

# Show passwords for specific website
pwdgen list --website example --show-password
```

```
pwdgen generate
```

Generate secure passwords.

Options:
Option | Description
-------|------------
--length | Password length (default: 16)
--no-special | Exclude special characters (optional)

Examples:
```bash
# Generate standard password
pm generate

# Generate 20-character password without special chars
pm generate --length 20 --no-special
```

## Security Features
- 🔐 AES-256 encryption for stored passwords
- 🔑 Argon2 hashing for master password
- 🧂 Unique salts for each password entry
- 🔄 600,000 PBKDF2 iterations for key derivation
- 🚫 No password storage in plaintext
- ⚠️ No recovery mechanism - lose master password = lose access


## Password Requirements

#### Master password must:
- Be at least 12 characters long
- Contain uppercase and lowercase letters
- Include at least one number
- Include at least one special character

#### Generated passwords:
- Default to 16 characters
- Include all character types by default
- Guarantee minimum complexity

## Contributing
1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a pull request