#!/bin/bash
TOTAL_PROC=$(ps aux | wc -l)
PROC_ROOT=$(ps aux  |grep  "^root"  | wc -l)
PROC_USER=$(ps aux   |grep "^$USER" | wc -l)
echo "{"
echo "    \"sonde\":  {"
echo "     \"processus\":  {"
echo "      \"timestamp\":  \"$(date -Iseconds)\","
echo "       \"total_processus\": $TOTAL_PROC, "
echo "        \"processus_root\":  $PROC_ROOT,"
echo "         \"processus_utulisateur\": $PROC_USER"
echo "      }"
echo "    }"
 echo "}"

