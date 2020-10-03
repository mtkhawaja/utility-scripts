import nmap, argparse, sys, time


def discover_hosts(scanner, nmap_args):
    return scanner.scan(hosts='192.168.1.0/24', arguments=nmap_args)

def extract_hosts(all_hosts, partial_host_ident):
    entries = []
    for ip in all_hosts['scan']:
        host_name = all_hosts['scan'][ip]['hostnames'][0]['name']
        if partial_host_ident in host_name:
            entries.append(f'{host_name:<12}{ip:>12}')
    return entries
    
def main(scanner, partial_host_ident, nmap_args):
    all_hosts = discover_hosts(scanner, nmap_args)
    return extract_hosts(all_hosts, partial_host_ident)

# Parse Arguments 
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--partial", help = "Partial host identifier", type = str)
parser.add_argument("-a", "--nmap_arguments", help = "nmap Arguments", type = str)
args = parser.parse_args()
partial_host_ident = args.partial if args.partial else "mtk"
nmap_args = args.nmap_arguments if args.nmap_arguments else "-sn -PE -R -v"

# Nmap  
nmap_scanner = nmap.PortScanner()
start = time.time()
results = main(nmap_scanner, partial_host_ident, nmap_args)
end = time.time()

# Print Results
print(len(results[0])*'=')
print(f"Scan Time:\t{round(end - start,2)}s")
print(len(results[0])*'=')
print('\n'.join(map(str, results)))

sys.exit(0)