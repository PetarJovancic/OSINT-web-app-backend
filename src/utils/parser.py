import re
from src.models.schemas import ScanResult


def parse_theharvester_output(output: str) -> ScanResult:
    try:
        target_match = re.search(r"\[\*\] Target: (.+)", output)
        target = target_match.group(1) if target_match else ""

        ips_section = re.search(r"\[\*\] IPs found: (\d+).*?(-{10,})(.+?)\n\n", output, re.DOTALL)
        total_ips = int(ips_section.group(1)) if ips_section else 0
        ips = ips_section.group(3).strip().split('\n') if ips_section else []

        emails_section = re.search(r"\[\*\] No emails found.", output)
        emails = [] if emails_section else re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', output)

        hosts_section = re.search(r"\[\*\] Hosts found: (\d+).*?(-{10,})(.+)", output, re.DOTALL)
        total_hosts = int(hosts_section.group(1)) if hosts_section else 0
        subdomains = re.findall(r'\b[\w\.-]+\.\w+\b', hosts_section.group(3)) if hosts_section else []

        return ScanResult(
            target=target,
            total_ips=total_ips,
            ips=ips,
            emails=emails,
            total_hosts=total_hosts,
            subdomains=subdomains
        )

    except Exception as e:
        return ScanResult(target="", total_ips=0, ips=[], emails=[], total_hosts=0, subdomains=[], error=str(e))