#!/bin/bash

echo "${LOCAL_SSH_KEY}" >> /home/ubuntu/.ssh/authorized_keys
snap install docker
sudo python3 -m easy_install install pip
sudo pip3 install psycopg2-binary


# Create the docker-compose.yml file
cat > /home/ubuntu/docker-compose.yml <<-EOM
version: "3"
services:      
  postgres:
    container_name: postgres_container
    image: postgres
    environment:
      POSTGRES_USER: db_user
      POSTGRES_PASSWORD: ${DB_PASS}  # Replace with actual password or fetch securely.
      PGDATA: /data/postgres
    volumes:
       - postgres:/data/postgres
    ports:
      - "5432:5432"
    networks:
      - postgres
    restart: unless-stopped
networks:
  postgres:
    driver: bridge
volumes:
    postgres:
EOM

# Navigate to the directory containing the docker-compose.yml file and bring up the service
cd /home/ubuntu
sudo docker-compose up -d
