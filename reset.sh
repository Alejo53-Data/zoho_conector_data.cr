#!/bin/bash



# Parsea los argumentos de línea de comandos
if [[ $# -ne 1 ]]; then
  echo "Uso: $0 <Container ID>"
  exit 1
fi



container=$1



docker stop $container
docker system prune -a



docker build -t adnpayapp .
docker run -it -p 5000:5000 -d --restart unless-stopped adnpayapp
