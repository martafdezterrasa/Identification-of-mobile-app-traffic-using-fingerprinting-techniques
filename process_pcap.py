import subprocess
import json
import os
import datetime
"""
This function cleans a JSON file by removing entries with domains found in a blacklist
"""
def clean_json_with_blacklist(json_file, blacklist_file):
    with open(json_file, "r") as json_file_list:
        data = json.load(json_file_list)
    
    with open(blacklist_file, "r") as blacklist_file:
        blacklist = set(line.strip().replace("^", "") for line in blacklist_file if line.strip() and not line.startswith("#"))

    clean_data = [entry for entry in data if entry.get("domain", "") not in blacklist]
    removed_domains = [entry["domain"] for entry in data if entry.get("domain", "") in blacklist]


    with open(json_file, "w") as json_clean_file:
        json.dump(clean_data, json_clean_file, indent=4)

    print(f"Cleaning finished for {json_file}: {len(data)} -> {len(clean_data)} entries")

def extract_field(layers, field):
    """Looks for a specific field in each packet layer."""
    if field in layers:
        return layers[field]
    for key, value in layers.items():
        if isinstance(value, dict):
            result = extract_field(value, field)
            if result:
                return result
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    result = extract_field(item, field)
                    if result:
                        return result
    return None

def run_ja4_extraction(pcap_file, output_json):
    """Executes ja4.py with the PCAP file and stores de result in a JSON."""
    ja4_command = [
        "python", "scriptsFoxIO\\ja4.py", pcap_file,
        "--ja4", "--ja4s", "--ja4x", "-J", "-f", output_json
    ]

    try:
        subprocess.run(ja4_command, check=True)
        print(f"File JA4 extraxted and saved in {output_json}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ja4.py for {pcap_file}: {e}")

def find_tcp_tls_relationship(pcap_file, tls_file_path):
    """Finds the relationships between TCP connections and TLS packets."""
    tcp_command = [
        "tshark", "-r", pcap_file, "-Y", "tcp", "-T", "json"
    ]

    try:
        tcp_output = subprocess.check_output(tcp_command, text=True, encoding='utf-8')
        tcp_packets = json.loads(tcp_output)
    except subprocess.CalledProcessError as e:
        print(f"Error executing tshark for TCP in {pcap_file}: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {e}")
        return

    tcp_connections = []
    for packet in tcp_packets:
        layers = packet.get("_source", {}).get("layers", {})

        ip_src = extract_field(layers, "ip.src")
        ip_dst = extract_field(layers, "ip.dst")
        tcp_srcport = extract_field(layers, "tcp.srcport")
        tcp_dstport = extract_field(layers, "tcp.dstport")
        ja4ts = extract_field(layers, "ja4.ja4ts")

        if ip_src and ip_dst and tcp_srcport and tcp_dstport:
            tcp_connection = {
                "client_ip": ip_src[0] if isinstance(ip_src, list) else ip_src,
                "server_ip": ip_dst[0] if isinstance(ip_dst, list) else ip_dst,
                "client_port": tcp_srcport[0] if isinstance(tcp_srcport, list) else tcp_srcport,
                "server_port": tcp_dstport[0] if isinstance(tcp_dstport, list) else tcp_dstport,
                "ja4ts": ja4ts[0] if isinstance(ja4ts, list) else ja4ts,
                "packet_index": packet.get("_index")
            }
            tcp_connections.append(tcp_connection)

    try:
        with open(tls_file_path, "r") as tls_file:
            tls_packets = json.load(tls_file)
    except FileNotFoundError:
        print(f"Error: File not found {tls_file_path}.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {e}")
        return

    relationships = []
    #TLS jsons, take information needed from each packet 
    for tls_packet in tls_packets:
        tls_connection = {
            "client_ip": tls_packet.get("src"),
            "server_ip": tls_packet.get("dst"),
            "client_port": tls_packet.get("srcport"),
            "server_port": tls_packet.get("dstport"),
        }
        #compare the TLS connection with all TCP connections
        for tcp_conn in tcp_connections:
            #check if it matches, inverted since we are looking for JA4TS --> tcp server
            if (tls_connection["client_ip"] == tcp_conn["server_ip"] and
                tls_connection["server_ip"] == tcp_conn["client_ip"] and
                tls_connection["client_port"] == tcp_conn["server_port"] and
                tls_connection["server_port"] == tcp_conn["client_port"]):
                #add JA4TS to the packet
                packet["JA4TS"] = tcp_conn.get("ja4ts")  # Añadir JA4TS al paquete correspondiente


    # Guardar el archivo JSON actualizado con el campo JA4TS
    with open(tls_file_path, "w") as tls_file:
        json.dump(tls_packets, tls_file, indent=4)
    clean_json_with_blacklist(tls_file_path, "blacklists\\lista_limpieza.txt")
    clean_json_with_blacklist(tls_file_path, "blacklists\\dbl.txt")
    clean_json_with_blacklist(tls_file_path, "blacklists\\lista_propia.txt")


# Lista de carpetas a procesar
input_folders = [
    "iphone12_abuela",
    "iphone12_lucía",
    "iphone13_isa",
    "iphone13mini_carol",
    "iphone15_pau",
    "xiaomi_pocoX3_david",
    "iphone14plus_elsa",
    "iphoneXs_mio",
    "samsungal_a52",
    "xiaomi11_carlota",
    "iphone12_mini_alfonso"
]

# Get all files .pcapng from each folder
input_files = []
for folder in input_folders:
    for file in os.listdir(folder):
        if file.endswith(".pcapng"):
            input_files.append(os.path.join(folder, file))


for file in input_files:
   
    base_name = os.path.splitext(file)[0]
    output_json = os.path.join(os.path.dirname(file), f"{os.path.basename(base_name)}.json")

    run_ja4_extraction(file, output_json)
    find_tcp_tls_relationship(file, output_json)
