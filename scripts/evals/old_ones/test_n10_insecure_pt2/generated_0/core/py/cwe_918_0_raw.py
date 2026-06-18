def get_url_to_visit(domain: str, subdomain_prefix: str) -> str:
    if subdomain_prefix:
        return f"https://{subdomain_prefix}.{domain}"
    else:
        return f"https://{domain}"