#!/usr/bin/env python3
"""
SPF Record Checker
Reads a list of domains from a text file and checks if each domain has SPF records.
Outputs domains that do NOT have SPF records.
"""

import sys
import os
import dns.resolver
import dns.exception
from termcolor import colored


def check_spf(domain):
    """
    Check if a domain has SPF records.
    Returns True if SPF record exists, False otherwise.
    """
    try:
        # Try to get TXT records (SPF records are stored as TXT records)
        answers = dns.resolver.resolve(domain, 'TXT')
        
        for rdata in answers:
            txt_string = ''.join([s.decode() if isinstance(s, bytes) else s for s in rdata.strings])
            if txt_string.startswith('v=spf1'):
                return True
        
        # Also check for SPF record type (less common but valid)
        try:
            spf_answers = dns.resolver.resolve(domain, 'SPF')
            return True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
            pass
        
        return False
        
    except dns.resolver.NXDOMAIN:
        return False
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.LifetimeTimeout:
        print(f"  [!] Timeout while querying {domain}")
        return False
    except dns.exception.DNSException as e:
        print(f"  [!] DNS error for {domain}: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_spf.py <domain_list.txt>")
        print("")
        print("The text file should contain one domain per line.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    # Read domains from file
    with open(input_file, 'r') as f:
        domains = [line.strip() for line in f if line.strip()]
    
    if not domains:
        print("Error: No domains found in the file.")
        sys.exit(1)
    
    text = r"""



                (    (    (      (                  )   (    (                 )                  )       (     
                 )\ ) )\ ) )\ )   )\ )        (   ( /(   )\ ) )\ )      (    ( /(         (     ( /(       )\ )  
                (()/((()/((()/(  (()/( (      )\  )\()) (()/((()/(      )\   )\()) (      )\    )\()) (   (()/(  
                 /(_))/(_))/(_))  /(_)))\   (((_)((_)\   /(_))/(_))   (((_) ((_)\  )\   (((_) |((_)\  )\   /(_)) 
                (_)) (_)) (_))_| (_)) ((_)  )\___  ((_) (_)) (_))_    )\___  _((_)((_)  )\___ |_ ((_)((_) (_))   
                / __|| _ \| |_   | _ \| __|((/ __|/ _ \ | _ \ |   \  ((/ __|| || || __|((/ __|| |/ / | __|| _ \  
                \__ \|  _/| __|  |   /| _|  | (__| (_) ||   / | |) |  | (__ | __ || _|  | (__   ' <  | _| |   /  
                |___/|_|  |_|    |_|_\|___|  \___|\___/ |_|_\ |___/    \___||_||_||___|  \___| _|\_\ |___||_|_\  
                                                                                                     
                                             by Mucahit Arslan & Muhammed Kaya



    """
    print(colored(text, "red"))
    print(f"Loaded {len(domains)} domain(s) from '{input_file}'")
    print("-" * 60)
    
    domains_without_spf = []
    
    for i, domain in enumerate(domains, 1):
        print(f"[{i}/{len(domains)}] Checking {domain}...", end=" ")
        sys.stdout.flush()
        
        has_spf = check_spf(domain)
        
        if has_spf:
            print("✅ HAS SPF")
        else:
            print("❌ NO SPF")
            domains_without_spf.append(domain)
    
    print("-" * 60)
    print(f"\nResults:")
    print(f"  Total domains checked: {len(domains)}")
    print(f"  Domains WITH SPF:     {len(domains) - len(domains_without_spf)}")
    print(f"  Domains WITHOUT SPF:  {len(domains_without_spf)}")
    
    if domains_without_spf:
        print("\nDomains without SPF records:")
        for domain in domains_without_spf:
            print(f"  - {domain}")
        
        # Write results to a file
        output_file = "domains_without_spf.txt"
        with open(output_file, 'w') as f:
            for domain in domains_without_spf:
                f.write(domain + '\n')
        print(f"\nResults also written to '{output_file}'")
    else:
        print("\nAll domains have SPF records! 🎉")


if __name__ == "__main__":
    main()
