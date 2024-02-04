# brise.cbbc


Sensores: 
Tin: 28-adeb0d1e64ff

Tg: 28-16dc0d1e64ff

Tout: 28-d9a50d1e64ff

Res1: 28-37c50d1e64ff

Res2: 28-d9c00d1e64ff


0x23 pode chamar de lux_in
0x5C pode chamar de lux_out


## Execucao automatica pelo systemd
Crie o servico:

    sudo nano /lib/systemd/system/brise.service

exemplo:

    [Unit]
    Description=Brise main
    After=network.target

    [Service]
    Type=idle
    ExecStart=/usr/bin/python3 /home/pi/brise.cbbc
    Restart=always
    RestartSec=2
    User=pi

    [Install]
    WantedBy=multi-user.target


Habilite e execute:

    sudo systemctl enable --now brise.service

## Inserir auto-commit na crontab

    00 01,13 * * * bash ~/auto-commit.sh

## Instal git-filter-repo

    python3 -m pip install --user git-filter-repo