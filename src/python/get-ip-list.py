import nmap, argparse, sys, time


def discover_hosts(scanner, nmap_args):
    return scanner.scan(hosts="192.168.1.0/24", arguments=nmap_args)


def extract_hosts(all_hosts, partial_host_ident):
    entries = []
    entries.append("{")
    for ip in all_hosts["scan"]:
        host_name = all_hosts["scan"][ip]["hostnames"][0]["name"]
        if partial_host_ident in host_name:
            entries.append(f'"{host_name}":"{ip}"')
            entries.append(",")
    entries.pop()
    entries.append("}")
    return "".join(entries)


def print_results(hosts, scan_time):
    result_list = []
    result_list.append("")
    max_len = 0
    for host_name in hosts:
        entry = f"{host_name:<12}{hosts[host_name]:>12}"
        max_len = max_len if max_len > len(entry) else len(entry)
        result_list.append(entry)
    line = max_len * "="
    result_list[0] = f"{line}\nScan Time: {scan_time}\n{line}"
    return "\n".join(result_list)


def main(args):
    nmap_scanner = nmap.PortScanner()
    start = time.time()
    all_hosts = discover_hosts(nmap_scanner, args.nmap_arguments)
    end = time.time()
    scan_time = f"{round(end - start,2)}s"
    req_hosts = extract_hosts(all_hosts, args.partial)
    return req_hosts if args.dict else print_results(req_hosts, scan_time)


# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--partial", help="Partial host identifier", type=str, default="mtk"
)
parser.add_argument(
    "-a", "--nmap_arguments", help="nmap Arguments", type=str, default="-sn -PE -R -v"
)
parser.add_argument(
    "-d", "--dict", help="Get dict with entry: {hostname: ip}", action="store_true"
)
parser.set_defaults(func=main)
args = parser.parse_args()
results = args.func(args)

print(results)

sys.exit(0)