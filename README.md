# SPF Spoofing Test

SPF Spoofing Test is a Python-based utility designed to help security professionals assess whether a domain is vulnerable to email spoofing due to missing or improperly configured SPF (Sender Policy Framework) records.

The tool performs SPF validation checks, resolves MX records, and attempts to send a test email using a specified sender address. This allows administrators and security researchers to evaluate how recipient mail servers handle messages originating from domains without proper email authentication controls.

This project is intended for educational purposes, authorized security assessments, and defensive security research only.

---

# Features

* SPF record detection
* MX record resolution
* Direct delivery to recipient mail servers
* Custom sender address support
* Custom email subject and message body
* SMTP authentication support
* TLS and SSL support
* Detailed SMTP debugging output
* Security recommendations for domains lacking SPF protection

---

# Requirements

* Python 3.8 or later
* dnspython

---

# Installation

Install the required dependency:

```bash
pip install dnspython
```

Clone the repository:

```bash
git clone https://github.com/muhammedkayag/Spf_Spoof_Tester.git
cd Spf_Spoof_Tester
```

---

# Usage

First, create a file containing the email body:

```bash
cat > body.txt << 'EOF'
Hi there,

This is a test mail for SPF Spoof

See you!
EOF
```

Then execute the script:

```bash
python3 spf_spoof_test.py \
    --domain example.com \
    --to security@example.net \
    --direct \
    --subject "SPF Spoof" \
    --message "$(cat body.txt)"
```

Before performing any action, the tool will ask for confirmation:

```text
Do you own 'example.com' and have authorization to test this? (yes/no):
```

Proceed only if you own the domain or have explicit authorization to perform the assessment.

---

# Command Line Options

| Option           | Description                                   |
| ---------------- | --------------------------------------------- |
| `--domain`       | Domain to test                                |
| `--sender`       | Custom sender email address                   |
| `--to`           | Recipient email address                       |
| `--direct`       | Deliver directly to the recipient's MX server |
| `--server`       | SMTP server                                   |
| `--port`         | SMTP port                                     |
| `--tls`          | Enable STARTTLS                               |
| `--ssl`          | Enable SSL                                    |
| `--user`         | SMTP username                                 |
| `--pass`         | SMTP password                                 |
| `--subject`      | Email subject                                 |
| `--message`      | Email body                                    |
| `--timeout`      | Connection timeout                            |
| `--no-spf-check` | Skip SPF verification                         |

---

# Usage Examples

## Direct MX Delivery

This method resolves the recipient domain's MX records and attempts to deliver the message directly to the destination mail server.

```bash
python3 spf_spoof_test.py \
    --domain example.com \
    --to security@example.net \
    --direct \
    --subject "SPF Test" \
    --message "Authorized SPF security assessment."
```

---

## SMTP Relay Delivery

Use an authenticated SMTP server to send the test email.

```bash
python3 spf_spoof_test.py \
    --domain example.com \
    --to security@example.net \
    --server smtp.example.com \
    --port 587 \
    --tls \
    --user username \
    --pass password \
    --subject "SPF Test" \
    --message "Authorized SPF security assessment."
```

---

# How It Works

The tool begins by checking whether the target domain publishes an SPF record. If no SPF record is found, the domain may be susceptible to sender impersonation attacks because receiving mail servers have limited ability to verify whether a sender is authorized to send mail on behalf of that domain.

If direct delivery mode is enabled, the script resolves the recipient domain's MX records and connects directly to the mail server responsible for receiving messages for that domain.

The message is then sent using the specified sender address, allowing administrators and security professionals to observe how recipient mail systems process emails originating from domains without proper SPF protection.

The goal is to help identify weak email authentication configurations and encourage the implementation of industry-standard protections.

---

# Example Output

```text
============================================================
SPF SPOOFING TEST - FOR AUTHORIZED TESTING ONLY
============================================================

[!] Target domain: example.com
[!] Recipient: security@example.net

[*] Checking SPF record...

[+] Domain 'example.com' has NO SPF record - vulnerable to spoofing.

[*] Resolving MX for recipient domain 'example.net'...

[+] MX records for 'example.net':
    Priority 10: mail.example.net

[*] Delivering directly to MX: mail.example.net:25

[✓] Email sent successfully!
```

---

# Recommended Security Controls

To protect a domain against email spoofing and impersonation attacks, the following technologies should be deployed together.

## SPF

```txt
v=spf1 mx ~all
```

SPF specifies which mail servers are authorized to send email on behalf of your domain.

---

## DKIM

DKIM (DomainKeys Identified Mail) cryptographically signs outgoing emails, allowing receiving mail servers to verify message authenticity and integrity.

---

## DMARC

```txt
v=DMARC1; p=reject;
```

DMARC builds upon SPF and DKIM by defining how receiving mail servers should handle messages that fail authentication checks.

---

# Disclaimer

This software is provided for educational purposes, defensive security research, and authorized security testing only.

Users are solely responsible for ensuring they have proper authorization before conducting any assessment. Unauthorized testing of systems, domains, or infrastructure that you do not own or manage may violate applicable laws, regulations, and service provider policies.

The author assumes no responsibility for misuse, unauthorized activities, service disruptions, data loss, legal consequences, or any damages resulting from the use of this software.


