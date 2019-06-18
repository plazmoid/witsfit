from scapy.all import sniff
print(sniff(iface='wlp3s0', filter="tcp-rst != 0"))