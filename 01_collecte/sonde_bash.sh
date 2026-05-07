#!/bin/bash

HOSTNAME=$(hostname)
DATE=$(date -Iseconds)
LOAD=$(uptime )
# awk -F load average :  {print $2}') 
DISK=$(df / | awk  'NR==2 {print $5}') 
MEM_TOTAL=$(free -m | awk 'NR==2 {print $2}')
MEM_USED=$(free -m | awk 'NR==2 {print $3}')
MEM_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))



echo "{"
echo "   \"sondes\": {"
echo "     \"bash\":  {" 
echo "        \"hostname \": \"$HOSTNAME\","
echo "       \"timestamp \" : \"$DATE\" ,"
echo "        \"load_average \" : \"$LOAD\"," 
echo "        \"disk_usage_root\": \"$DISK\"," 
echo "          \"memory_used _mb \": $MEM_USED,"
echo "           \"memory_total_mb\": $MEM_TOTAL,"
echo "            \"memory_percent\": $MEM_PERCENT"
echo "     }"
echo "   }"
echo "}"
 
