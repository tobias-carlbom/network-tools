import anvil.server
import dns.resolver
import dns.exception
import ipaddress

RESOLVERS = [
    ("Google Public DNS (US)",        "8.8.8.8",       ""),
    ("Google Public DNS 2 (US)",      "8.8.4.4",       ""),
    ("Cloudflare (US)",               "1.1.1.1",       ""),
    ("Cloudflare 2 (US)",             "1.0.0.1",       ""),
    ("OpenDNS (US)",                  "208.67.222.222",""),
    ("OpenDNS 2 (US)",                "208.67.220.220",""),
    ("Quad9 (CH)",                    "9.9.9.9",       ""),
    ("CIRA Canadian Shield (CA)",     "149.112.121.10",""),  # Anycast, CA-focused
    ("GleSYS", "178.73.210.182", ""),
    ("Tele2 DNS", "217.119.160.99", ""),
    ("AliDNS (CN)",                   "223.5.5.5",     ""),
    ("Quad101 (TW)",                  "101.101.101.101",""),
]



def _dns_query_a(name: str, server_ip: str, timeout: float = 2.0):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [server_ip]
    resolver.timeout = timeout
    resolver.lifetime = timeout * 2
    try:
        answer = resolver.resolve(name, "A")
        ips = sorted({str(rr.address) for rr in answer})
        ttl = answer.rrset.ttl if answer.rrset is not None else None
        return {"status": "OK", "ips": ips, "ttl": ttl, "error": None}
    except dns.resolver.NXDOMAIN:
        return {"status": "NXDOMAIN", "ips": [], "ttl": None, "error": "No such domain"}
    except dns.resolver.NoAnswer:
        return {"status": "NOANSWER", "ips": [], "ttl": None, "error": "No A record"}
    except dns.exception.Timeout:
        return {"status": "TIMEOUT", "ips": [], "ttl": None, "error": "Timeout"}
    except Exception as e:
        return {"status": "ERROR", "ips": [], "ttl": None, "error": str(e)}


@anvil.server.callable
def dns_propagation(target: str):
    timeout = 2.0
    target = (target or "").strip()
    if not target:
        raise ValueError("No target provided")
    try:
        ipaddress.ip_address(target)
    except ValueError:
        pass
    else:
        raise ValueError("Target must be a hostname, not an IP address")
    results = []
    for name, server, country in RESOLVERS:
        r = _dns_query_a(target, server_ip=server, timeout=timeout)
        results.append(
            {
                "resolver_name": name,
                "server": server,
                "country": country,
                "status": r["status"],
                "ttl": r["ttl"],
                "ips": r["ips"],
                "error": r["error"],
            }
        )
    return {
        "target": target,
        "results": results,
    }
