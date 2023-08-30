from pytricia import PyTricia

# Define file paths
ris_path = "./apnic-whois/ris_lookup.txt"
# RIPE RIS bgp dump taken from here https://www.ris.ripe.net/dumps/riswhoisdump.IPv4.gz
# only taken routes seen by more than 250 peers
#cat riswhoisdump.IPv4 | awk '($3 > 250) { print $2"\t"$1}'  --> need to clean up lines on the top.

apnic_path = "./apnic-whois/apnic_route2.txt"  # Replace with your actual file path
#curl http://103.162.143.30/route-check/data/20230815/radb/apnic_to_radb4.json | jq -r '.[]|.prefix,.rir.origin,.rir.mnt,.rir.source,.rir."last-modified"' | paste - - - - -
#data required for this lookup is only prefix and asn

# Create PyTricia trees to store routes (prefix and origin ASN) from both files
ris_routes = PyTricia()
apnic_routes = PyTricia()

# Read routes from RIPE RIS File and populate the PyTricia tree
with open(ris_path, "r") as file1:
    for line in file1:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            prefix, origin_asn = parts[0], parts[1]
            ris_routes[prefix] = origin_asn

# Read routes from APNIC file and populate the PyTricia tree
with open(apnic_path, "r") as file2:
    for line in file2:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            prefix, origin_asn = parts[0], parts[1]
            apnic_routes[prefix] = origin_asn

# Iterate over routes in RIPE RIS File and check for matches in APNIC File

for prefix in ris_routes:
    origin_asn_file1 = ris_routes.get(prefix, None)
    origin_asn_file2 = apnic_routes.get(prefix, None)
    if origin_asn_file2 is None:
    #    print(f"Matching Route: Prefix {prefix}, Origin ASN (RIPE RIS): {origin_asn_file1}, Origin ASN (APNIC): {origin_asn_file2}")
    #else:
        print(f"Non-matching Route: Prefix {prefix}, Origin ASN (RIPE RIS): {origin_asn_file1}")
