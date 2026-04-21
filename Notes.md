### Build the App as single executable in C
__System Prep__
```
sudo apt install gcc ccache patchelf 
pip install nuitka zstandard
```

<br>

__Build Commands__
```
nuitka \
  --onefile \
  --standalone \
  --follow-imports \
  --output-dir=build \
  --output-filename=dnsmasq-config-api \
  ./src/app.py


nuitka \
  --onefile \
  --standalone \
  --follow-imports \
  --include-package-data=* \
  --include-data-files=./config.yaml=config.yaml \
  --output-dir=build \
  --output-filename=dnsmasq-config-api \
  ./src/app.py

```

<br>

__Deploy via Systemd__
```
sudo install build/dnsmasq-config-api /usr/local/bin
sudo cp deploy/dnsmasq-config-api.service /etc/systemd/system/
sudo systemctl enable --now dnsmasq-config-api.service

```