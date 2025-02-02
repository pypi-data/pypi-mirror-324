#!/bin/sh

set -eux

if [ ! -e "private_key.pem" ]; then
    openssl genrsa -out private_key.pem 2048
    openssl rsa -in private_key.pem  -pubout -out public_key.pem
fi

npm install
npx nodemon app.js