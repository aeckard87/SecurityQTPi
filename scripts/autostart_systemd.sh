#!/bin/bash
cp securityqtpi@pi.service /etc/systemd/system/securityqtpi@${SUDO_USER:-${USER}}.service
sed -i "s?/home/pi/SecurityQTPi?`pwd`?" /etc/systemd/system/securityqtpi@${SUDO_USER:-${USER}}.service
systemctl --system daemon-reload
systemctl enable securityqtpi@${SUDO_USER:-${USER}}.service
