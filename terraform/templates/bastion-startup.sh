#!/bin/bash

echo "${SSH_KEY}" >> /home/ubuntu/.ssh/will_fell_mac_book.pem
chmod 400 /home/ubuntu/.ssh/will_fell_mac_book.pem
echo "${LOCAL_SSH_KEY}" >> /home/ubuntu/.ssh/authorized_keys
