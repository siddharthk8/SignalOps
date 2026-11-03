import httpx

BLOCKLIST_URL = "https://raw.githubusercontent.com/disposable/disposable-email-domains/master/domains.txt"
disposable_domains: set[str] = set()


async def load_disposable_domains():
    global disposable_domains

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(BLOCKLIST_URL)
        response.raise_for_status()

    domains = {
        line.strip().lower().rstrip(".")
        for line in response.text.splitlines()
        if line.strip() and not line.startswith("#")
    }

    if not domains:
        raise RuntimeError("Disposable email blocklist is empty")

    disposable_domains = domains
    print(f"Loaded {len(disposable_domains)} disposable domains")


async def check_email(email: str):
    domain = email.rsplit("@", 1)[1].lower().rstrip(".")

    # 1. Disposable domain check
    parts = domain.split(".")

    if any(".".join(parts[i:]) in disposable_domains for i in range(len(parts))):
        return False, "Temporary email addresses are not allowed"

    # For now we are avoiding this since we are getting frequent exceptions by using it.
    # 2. DNS / MX check
    # try:
    #     answers = await dns.asyncresolver.resolve(
    #         domain,
    #         "MX",
    #         lifetime=5,
    #     )

    #     if any(str(answer.exchange) == "." for answer in answers):
    #         return False, "Email domain does not accept emails"

    # except dns.resolver.NXDOMAIN:
    #     return False, "Email domain does not exist"

    # except dns.resolver.NoAnswer:
    #     return False, "Email domain has no MX records"

    # except (
    #     dns.resolver.NoNameservers,
    #     dns.exception.Timeout,
    #     dns.exception.DNSException,
    # ) as exc:
    #     raise RuntimeError("Unable to verify email domain DNS") from exc

    return True, email
