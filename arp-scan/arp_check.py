# arp_check.py

import scapy.all as scapy
import netifaces as ni
import threading
import datetime

class ARPSpoofDetector:
    def __init__(self):
        self.known_devices = {}
        self.alerts = []
        self.spoofed = False
        self.interface = None
        self.ip_range = None

    def detect_network(self):
        # Automatically detect interface and subnet, skipping 'lo'
        interfaces = ni.interfaces()
        for interface in interfaces:
            if interface == 'lo':  # Skip loopback interface
                continue

            addrs = ni.ifaddresses(interface)
            if ni.AF_INET in addrs:  # Check for IPv4
                ip_info = addrs[ni.AF_INET][0]
                ip = ip_info['addr']
                netmask = ip_info['netmask']

                # Calculate the subnet (CIDR) based on IP and netmask
                ip_parts = ip.split('.')
                netmask_parts = netmask.split('.')
                subnet = '.'.join([str(int(ip_parts[i]) & int(netmask_parts[i])) for i in range(4)])

                # Set detected interface and subnet
                self.interface = interface
                self.ip_range = f"{subnet}/24"
                break

    def scan_network(self):
        arp_request = scapy.ARP(pdst=self.ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        for element in answered:
            self.known_devices[element[1].psrc] = element[1].hwsrc

    def sniff(self):
        scapy.sniff(iface=self.interface, store=False, prn=self.process_packet)

    def process_packet(self, packet):
        if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
            real_mac = self.known_devices.get(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac and response_mac != real_mac:
                alert = {
                    "timestamp": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                    "ip": packet[scapy.ARP].psrc,
                    "real_mac": real_mac,
                    "fake_mac": response_mac
                }
                self.alerts.append(alert)
                self.spoofed = True
                print(f"[!] ARP Spoofing detected! Fake MAC: {response_mac}")
                print(f"[!] Attack detected at {alert['timestamp']}")

    def start_sniffing(self):
        self.detect_network()
        if self.interface and self.ip_range:
            print(f"[*] Using Interface: {self.interface}, Subnet: {self.ip_range}")
            self.scan_network()
            sniff_thread = threading.Thread(target=self.sniff)
            sniff_thread.daemon = True
            sniff_thread.start()
        else:
            print("[-] No network detected.")

    def is_spoofed(self):
        return self.spoofed

    def get_alerts(self):
        return self.alerts
