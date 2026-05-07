#!/usr/bin/env python3
import psutil
import json

import datetime


cpu_percent = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory()
disk = psutil.disk_usage('/')
users = len(psutil.users())
processes = len(psutil.pids())
boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat()
try:
  hostname=psutil.users()[0].host
except:
  hostname ="uknown"
data  = {
   "sondes ": {
       "python " : {
                "hostname" :hostname,
                 "timestamp": datetime.datetime.now().isoformat(),
                 "cpu_percent ": cpu_percent,
                  "memory_percent" : memory.percent,
                   "memory_available_mb" : memory.available //(1024 *1024),
                  "disk_percent" : disk.percent ,
                   "disk_free": disk.free // (1021*1024*1024) ,
                   "users_connected" : users,
                   "total_process": processes
        }
   }
}
print(json.dumps(data ,indent=2))

