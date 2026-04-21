import os
import uuid
import ipaddress

from settings import settings
from models import (
    HostRecord
)


#-Helpers--------------------------------------------------
def helper_check_conf_files():
    for fp in [settings.dns_config_file_path, settings.dhcp_config_file_path]:
        if not os.path.isfile(fp):
            with open(fp, "w", encoding="utf-8") as fl:
                fl.write("# Managed by DNSMasq Config Rest API\n")

#------
def helper_get_lines_from_file(filepath:str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as fl:
        lines = [line.rstrip("\n") for line in fl]
    return lines

#------
def helper_rm_ips_from_list(items:list) -> list:
    cleaned = []
    for x in items:
        try:
            ipaddress.ip_address(x)
            continue
        except ValueError:
            cleaned.append(x)
    return cleaned

#------
def helper_get_ipv4_from_list(items:list) -> ipaddress.IPv4Address:
    for x in items:
        try:
            ip = ipaddress.ip_address(x)
            if isinstance(ip, ipaddress.IPv4Address):
                return ip 
        except ValueError:
            pass
    return None

#------
def helper_get_ipv6_from_list(items:list) -> ipaddress.IPv6Address:
    for x in items:
        try:
            ip = ipaddress.ip_address(x)
            if isinstance(ip, ipaddress.IPv6Address):
                return ip 
        except ValueError:
            pass
    return None

#------
def helper_host_record_to_config_string(item:HostRecord) -> str:
    line = "host-record=" + ",".join(item.hostnames) + "," + str(item.ipv4_address)
    if item.ipv6_address:
        line = line + f",{item.ipv6_address}"
    line = line + f" # {item.id}"
    return line

#------

#------


#-DNS Functions--------------------------------------------
def dns_host_records_get() -> list[HostRecord]:
    lines = helper_get_lines_from_file(filepath=settings.dns_config_file_path)
    res = []
    for line in lines:
        if line.startswith("host-record=") and "#" in line:
            try:
                id = uuid.UUID(line.split("#")[1].replace(" ", ""))
                conf_str = line.split("#")[0].split("=")[1].replace(" ", "")
                conf_ary = conf_str.split(",")
            except Exception as e:
                # print(e)
                continue
            item = HostRecord(
                id=id,
                hostnames=helper_rm_ips_from_list(conf_ary),
                ipv4_address=helper_get_ipv4_from_list(conf_ary),
                ipv6_address=helper_get_ipv6_from_list(conf_ary)
            )
            res.append(item)
    return res

#------
def dns_get_all_hostnames() -> list[str]:
    res = []
    items = dns_host_records_get()
    for item in items:
        res = res + item.hostnames
    return res

#------
def dns_host_record_add(item:HostRecord):
    conf_str = helper_host_record_to_config_string(item=item)
    with open(settings.dns_config_file_path, "a", encoding="utf-8") as fl:
        fl.write(conf_str + "\n")

#------
def dns_host_record_change(id:uuid.UUID, item:HostRecord) -> HostRecord:
    if id != item.id:
        item.id = id
    lines = helper_get_lines_from_file(filepath=settings.dns_config_file_path)
    conf_file_str = ""
    for line in lines:
        if line.startswith("host-record=") and "#" in line and str(id) in line:
            new_line = helper_host_record_to_config_string(item=item)
            conf_file_str = conf_file_str + new_line + "\n"
        else:
            conf_file_str = conf_file_str + line + "\n"
    with open(settings.dns_config_file_path, "w", encoding="utf-8") as fl:
        fl.write(conf_file_str)
    return item

#------
def dns_host_record_delete(id:uuid.UUID):
    lines = helper_get_lines_from_file(filepath=settings.dns_config_file_path)
    conf_file_str = ""
    for line in lines:
        if line.startswith("host-record=") and "#" in line and str(id) in line:
            continue
        conf_file_str = conf_file_str + line + "\n"
    with open(settings.dns_config_file_path, "w", encoding="utf-8") as fl:
        fl.write(conf_file_str)

#------