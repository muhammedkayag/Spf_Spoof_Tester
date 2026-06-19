#!/usr/bin/env python3
"""
SPF Spoofing Test Script
========================
FOR AUTHORIZED TESTING ONLY - Use only against domains you own.
"""

import smtplib
import socket
import argparse
import sys
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from termcolor import colored


def check_spf_record(domain):
    try:
        import dns.resolver
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in answers:
                txt_string = rdata.to_text()
                if 'v=spf1' in txt_string:
                    print(f"[!] Domain '{domain}' HAS an SPF record: {txt_string}")
                    return True
            print(f"[+] Domain '{domain}' has NO SPF record - vulnerable to spoofing.")
            return False
        except dns.resolver.NoAnswer:
            print(f"[+] Domain '{domain}' has NO SPF record - vulnerable to spoofing.")
            return False
        except dns.resolver.NXDOMAIN:
            print(f"[-] Domain '{domain}' does not exist.")
            return None
    except ImportError:
        print("[*] dnspython not installed. Skipping SPF check.")
        return None

def resolve_mx(domain):
    try:
        import dns.resolver
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            mx_records = []
            for rdata in answers:
                mx_records.append((rdata.preference, str(rdata.exchange)))
            mx_records.sort()
            print(f"[+] MX records for '{domain}':")
            for pref, mx in mx_records:
                print(f"    Priority {pref}: {mx}")
            return mx_records
        except dns.resolver.NoAnswer:
            print(f"[-] No MX records found for '{domain}'.")
            try:
                answers = dns.resolver.resolve(domain, 'A')
                print(f"[+] Using {domain} -> {answers[0]}")
                return [(10, domain)]
            except:
                return None
        except dns.resolver.NXDOMAIN:
            print(f"[-] Domain '{domain}' does not exist.")
            return None
    except ImportError:
        print("[*] dnspython not installed. Cannot resolve MX.")
        return None

def send_spoofed_email(
    spoofed_domain,
    spoofed_sender,
    recipient,
    smtp_server,
    smtp_port=25,
    subject=None,
    message_body=None,
    use_tls=False,
    use_ssl=False,
    username=None,
    password=None,
    timeout=30
):
    if not subject:
        subject = f"SPF Spoofing Test - {spoofed_domain}"
    
    if not message_body:
        message_body = f"""This is an SPF spoofing test email.

This email appears to come from {spoofed_sender}@{spoofed_domain},
but was actually sent from {socket.gethostname()}.

Why this works:
- The domain '{spoofed_domain}' has no SPF record
- Without SPF, receiving mail servers cannot verify the sender
- DMARC also cannot function without SPF or DKIM

Security recommendation:
- Add an SPF record to '{spoofed_domain}' 
- Add DKIM signing
- Add a DMARC policy (p=reject or p=quarantine)

This test was authorized on infrastructure owned by the test domain owner.
"""
    
    msg = MIMEMultipart('alternative')
    msg['From'] = spoofed_sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = f"<{spoofed_domain}-{int(time.time())}@{socket.gethostname()}>"
    msg['X-Mailer'] = 'SPF Test Script v1.0'
    
    part = MIMEText(message_body, 'plain', 'utf-8')
    msg.attach(part)
    
    print(f"\n[*] Attempting to send spoofed email...")
    print(f"    From:    {spoofed_sender}")
    print(f"    To:      {recipient}")
    print(f"    Subject: {subject}")
    print(f"    Server:  {smtp_server}:{smtp_port}")
    
    try:
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=timeout)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=timeout)
            if use_tls:
                server.starttls()
        
        server.set_debuglevel(1)
        
        if username and password:
            server.login(username, password)
        
        server.sendmail(spoofed_sender, [recipient], msg.as_string())
        server.quit()
        
        print(f"\n[✓] Email sent successfully!")
        print(f"[✓] Check {recipient}'s inbox/spam folder")
        return True
        
    except smtplib.SMTPConnectError as e:
        print(f"\n[✗] Connection failed: {e}")
        return False
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n[✗] Authentication failed: {e}")
        return False
    except smtplib.SMTPSenderRefused as e:
        print(f"\n[✗] Sender refused: {e}")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"\n[✗] Recipient refused: {e}")
        return False
    except socket.timeout:
        print(f"\n[✗] Connection timed out after {timeout} seconds.")
        return False
    except Exception as e:
        print(f"\n[✗] Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='SPF Spoofing Test - FOR AUTHORIZED TESTING ONLY')
    
    parser.add_argument('--domain', required=True,
                        help='The test domain to spoof (must be YOUR domain)')
    parser.add_argument('--sender', 
                        help='Full sender email (default: admin@DOMAIN)')
    parser.add_argument('--to', '--recipient', dest='recipient', required=True,
                        help='Recipient email address')
    parser.add_argument('--server', 
                        help='SMTP server to use (default: localhost)')
    parser.add_argument('--port', type=int, default=25,
                        help='SMTP port (default: 25)')
    parser.add_argument('--tls', action='store_true',
                        help='Use STARTTLS')
    parser.add_argument('--ssl', action='store_true',
                        help='Use SSL')
    parser.add_argument('--user', 
                        help='SMTP username for authentication')
    parser.add_argument('--pass', dest='password',
                        help='SMTP password')
    parser.add_argument('--subject',
                        help='Email subject')
    parser.add_argument('--message',
                        help='Email body text')
    parser.add_argument('--no-spf-check', action='store_true',
                        help='Skip SPF record check')
    parser.add_argument('--direct', action='store_true',
                        help='Deliver directly to recipient MX server')
    parser.add_argument('--timeout', type=int, default=30,
                        help='Connection timeout in seconds (default: 30)')
    
    args = parser.parse_args()
    text = r"""
    
                 (    (    (      (    (        )      )   (                  (                (     
                 )\ ) )\ ) )\ )   )\ ) )\ )  ( /(   ( /(   )\ )    *   )      )\ )  *   )      )\ )  
                (()/((()/((()/(  (()/((()/(  )\())  )\()) (()/(  ` )  /( (   (()/(` )  /( (   (()/(  
                 /(_))/(_))/(_))  /(_))/(_))((_)\  ((_)\   /(_))  ( )(_)))\   /(_))( )(_)))\   /(_)) 
                (_)) (_)) (_))_| (_)) (_))    ((_)   ((_) (_))_| (_(_())((_) (_)) (_(_())((_) (_))   
                / __|| _ \| |_   / __|| _ \  / _ \  / _ \ | |_   |_   _|| __|/ __||_   _|| __|| _ \  
                \__ \|  _/| __|  \__ \|  _/ | (_) || (_) || __|    | |  | _| \__ \  | |  | _| |   /  
                |___/|_|  |_|    |___/|_|    \___/  \___/ |_|      |_|  |___||___/  |_|  |___||_|_\  
                                       
                                       by Mucahit Arslan & Muhammed Kaya
                                                                                                     


        """
    print(colored(text, "red"))
    print("=" * 60)
    print("  SPF SPOOFING TEST - FOR AUTHORIZED TESTING ONLY")
    print("=" * 60)
    print(f"\n[!] Target domain: {args.domain}")
    print(f"[!] Recipient:     {args.recipient}")
    
    confirm = input(f"\n[?] Do you own '{args.domain}' and have authorization to test this? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("[-] Aborting.")
        sys.exit(1)
    
    spoofed_sender = args.sender or f"admin@{args.domain}"
    
    if args.direct:
        if '@' not in args.recipient:
            print("[-] Recipient must be a valid email address")
            sys.exit(1)
        recipient_domain = args.recipient.split('@')[1]
        print(f"\n[*] Resolving MX for recipient domain '{recipient_domain}'...")
        mx_records = resolve_mx(recipient_domain)
        if not mx_records:
            print("[-] Could not resolve MX records. Aborting.")
            sys.exit(1)
        smtp_server = str(mx_records[0][1])
        if smtp_server.endswith('.'):
            smtp_server = smtp_server[:-1]
        smtp_port = 25
        print(f"[*] Delivering directly to MX: {smtp_server}:{smtp_port}")
    else:
        smtp_server = args.server or "localhost"
        smtp_port = args.port
    
    if not args.no_spf_check:
        print("\n[*] Checking SPF record...")
        has_spf = check_spf_record(args.domain)
        if has_spf:
            print("[!] WARNING: Domain has SPF.")
            proceed = input("[?] Continue anyway? (yes/no): ")
            if proceed.lower() not in ['yes', 'y']:
                print("[-] Aborting.")
                sys.exit(1)
    
    success = send_spoofed_email(
        spoofed_domain=args.domain,
        spoofed_sender=spoofed_sender,
        recipient=args.recipient,
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        subject=args.subject,
        message_body=args.message,
        use_tls=args.tls,
        use_ssl=args.ssl,
        username=args.user,
        password=args.password,
        timeout=args.timeout
    )
    
    if success:
        print("\n" + "=" * 60)
        print("  TEST COMPLETE")
        print("=" * 60)
        print(f"\n  What happened:")
        print(f"  1. The email was sent with From: {spoofed_sender}")
        print(f"  2. Since {args.domain} has no SPF record,")
        print(f"     the receiving server couldn't verify the sender")
        print(f"  3. The email may have been delivered to inbox or spam")
        print(f"\n  To fix this vulnerability:")
        print(f"  - Add SPF record: v=spf1 mx ~all")
        print(f"  - Add DKIM signing")
        print(f"  - Add DMARC policy: v=DMARC1; p=reject;")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("  TEST FAILED")
        print("=" * 60)
        print("\n  Common issues:")
        print("  1. Port 25 blocked by ISP")
        print("  2. No SMTP server running on localhost")
        print("  3. Receiving server rejected the spoofed sender")
        print("  4. Need SMTP authentication (--user and --pass)")
        print("=" * 60)


if __name__ == '__main__':
    main()

