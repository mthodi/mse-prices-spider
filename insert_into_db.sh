#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "[+] Usage $0 <SQL_FILE>"
    exit 1
fi

DB_NAME='security_master_dev'
USER='martin'


mysql -u $USER $DB_NAME < $1