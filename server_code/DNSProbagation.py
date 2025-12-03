import anvil.server
import dns.resolver
import dns.exception
import ipaddress
import time

RESOLVERS = [
    ("Google (US)",        "8.8.8.8",        ""),
    ("Google 2 (US)",      "8.8.4.4",        ""),
    ("Cloudflare (US)",    "1.1.1.1",        ""),
    ("Cloudflare 2 (US)",  "1.0.0.1",        ""),
    ("OpenDNS (US)",       "208.67.222.222", ""),
    ("OpenDNS 2 (US)",     "208.67.220.220", ""),
    ("Quad9 (CH)",         "9.9.9.9",        ""),
    ("CIRA (CA)",          "149.112.121.10", ""),
    ("GleSYS",             "178.73.210.182", ""),
    ("Tele2",              "217.119.160.99", ""),
    ("AliDNS (CN)",        "223.5.5.5",      ""),
    ("Quad101 (TW)",       "101.101.101.101",""),
]

def _get_authoritative_nameservers(domain: str):
    parts = domain.split('.')
    for i in range(len(parts)):
        zone = '.'.join(parts[i:])
        try:
            answers = dns.resolver.resolve(zone, 'NS')
            ns_list = [str(rdata.target).rstrip('.') for rdata in answers]
            return sorted(ns_list)
        except:
            continue
    return []

def _dns_query_a(name: str, server_ip: str | None, timeout: float = 2.0):
    resolver = dns.resolver.Resolver()
    if server_ip:
        resolver.nameservers = [server_ip]
    resolver.timeout = timeout
    resolver.lifetime = timeout * 2
    try:
        answer = resolver.resolve(name, "A")
        ips = [str(rr.address) for rr in answer]
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
def dns_propagation(target: str, num_checks: int = 2):
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

    auth_nameservers = _get_authoritative_nameservers(target)
    if not auth_nameservers:
        raise ValueError(f"Could not find authoritative nameservers for {target}")

    auth_ns_ip = None
    for ns in auth_nameservers:
        try:
            ns_answers = dns.resolver.resolve(ns, 'A')
            auth_ns_ip = str(ns_answers[0].address)
            break
        except:
            continue

    if not auth_ns_ip:
        raise ValueError(f"Could not resolve authoritative nameserver IP")

    baseline = _dns_query_a(target, server_ip=auth_ns_ip, timeout=timeout)

    if baseline["status"] != "OK" or not baseline["ips"]:
        raise ValueError(f"Authoritative DNS lookup failed: {baseline['status']} ({baseline['error']})")

    baseline_ips = baseline["ips"]
    baseline_ip_set = set(baseline_ips)
    display_target = f"Hostname: {target} → {', '.join(baseline_ips)} (via {auth_nameservers[0]})"

    results = []
    for name, server, country in RESOLVERS:
        ok_count = 0
        last_response = None

        for check_num in range(num_checks):
            r = _dns_query_a(target, server_ip=server, timeout=timeout)
            last_response = r
            if r["status"] == "OK" and set(r["ips"]) == baseline_ip_set:
                ok_count += 1
            if check_num < num_checks - 1:
                time.sleep(0.5)

        if ok_count == num_checks:
            overall_status = "OK"
        elif ok_count > 0:
            overall_status = "FLIPPING"
        else:
            overall_status = "FAILED"

        results.append(
            {
                "resolver_name": name,
                "server": server,
                "country": country,
                "status": overall_status,
                "dns_status": last_response["status"],
                "ttl": last_response["ttl"],
                "ips": last_response["ips"],
                "error": last_response["error"],
            }
        )

    return {
        "target": target,
        "display_target": display_target,
        "baseline_ips": baseline_ips,
        "results": results,
    }