#!bin/bash

aws route53 list-resource-record-sets --hosted-zone-id Z31RX3GZS94JZS --output json > my_records.json