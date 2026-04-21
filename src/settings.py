import os
from pydantic import BaseModel

class Settings(BaseModel):
    systemd_mgmt: str = os.environ.get("SYSTEMD_MGMT", "true")
    systemd_service_name: str = os.environ.get("SYSTEMD_SERVICE_NAME", "dnsmasq")
    dns_config_file_path: str = os.environ.get("DNS_CONFIG_FILE_PATH", "/etc/dnsmasq.d/local-dns.conf")
    dhcp_config_file_path: str = os.environ.get("DHCP_CONFIG_FILE_PATH", "/etc/dnsmasq.d/custom-dhcp.conf")
    app_port: int = int(os.environ.get("APP_PORT", "5000"))
    app_debug: bool = bool(os.environ.get("APP_DEBUG", "True"))
    static_html_folder: str = "static"

settings = Settings()