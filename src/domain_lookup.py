import whois
import socket
import dns.resolver
import csv
from datetime import datetime

def get_domain_info(domain):
    data = {
        "domain": domain,
        "registrar": None,
        "creation_date": None,
        "expiration_date": None,
        "country": None,
        "ip_address": None,
        "mx_records": None,
        "ns_records": None,
        "error": None
    }

    try:
        # WHOIS data
        w = whois.whois(domain)
        data["registrar"] = w.registrar
        data["creation_date"] = str(w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date)
        data["expiration_date"] = str(w.expiration_date[0] if isinstance(w.expiration_date, list) else w.expiration_date)
        data["country"] = w.country

        # IP address
        try:
            data["ip_address"] = socket.gethostbyname(domain)
        except:
            data["ip_address"] = None

        # MX records
        try:
            mx_records = dns.resolver.resolve(domain, "MX")
            data["mx_records"] = ";".join([str(r.exchange) for r in mx_records])
        except:
            data["mx_records"] = None

        # NS records
        try:
            ns_records = dns.resolver.resolve(domain, "NS")
            data["ns_records"] = ";".join([str(r.target) for r in ns_records])
        except:
            data["ns_records"] = None

    except Exception as e:
        data["error"] = str(e)

    return data


def save_to_csv(domains, filename="domain_info.csv"):
    fieldnames = ["domain", "registrar", "creation_date", "expiration_date", "country",
                  "ip_address", "mx_records", "ns_records", "error"]

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for domain in domains:
            print(f"🔍 Checking {domain} ...")
            info = get_domain_info(domain)
            writer.writerow(info)

    print(f"\n✅ Domain info saved to {filename}")


# 🔹 Example usage
if __name__ == "__main__":
    domains = ["google.com", "sbi.co.in", "g00gle.com", "paypal.com", "faceb00k.com"]
    save_to_csv(domains)
