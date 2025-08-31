import ssl
import socket
from datetime import datetime

def get_ssl_info(domain):
    """
    Return a dict with SSL features:
    ssl_valid (1/0), ssl_days (int), ssl_issuer (string)
    """
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert['issuer'])
                
                # Calculate number of days SSL is valid
                not_after = cert.get("notAfter")
                if not_after:
                    expire_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                    ssl_days = max((expire_date - datetime.utcnow()).days, 0)
                else:
                    ssl_days = 0

                return {
                    "ssl_valid": 1,
                    "ssl_days": ssl_days,
                    "ssl_issuer": issuer.get("organizationName", "")
                }
    except Exception:
        return {"ssl_valid": 0, "ssl_days": 0, "ssl_issuer": ""}
