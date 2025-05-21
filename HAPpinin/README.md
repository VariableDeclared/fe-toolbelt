# HAPpinin'


## Quickstart

A tool to stress your nodes, catching hardware issues early on, and avoiding #pain later :)

To run the tool, create a virutalenv

```
$ python3 -m venv create happinin
$ source happinin/bin/activate
$ pip install psutil
```

### Run it!

```
python3 HAPpinin.py
```

## Examples

```
$ python3 HAPpinin.py

Gathering system information...
stress-ng is already installed.
Running stress-ng (10 seconds, 4 CPU stressor)...

--- System Report ---
Date: 2025-05-21 19:10:18.108122

CPU Cores: 2
Logical CPUs: 4
Total Memory: 15.49 GB
Memory Modules:
  - 	Size: 8 GB
  - 	Size: 8 GB
Connected Disks:
  - /dev/mapper/ubuntu--vg-root (/) - 1941.81 GB total
  - /dev/mapper/ubuntu--vg-root (/var/snap/firefox/common/host-hunspell) - 1941.81 GB total
  - /dev/sdb1 (/boot/efi) - 0.50 GB total

--- Stress Test Result ---
stress-ng: info:  [721715] setting to a 30 secs run per stressor
stress-ng: info:  [721715] dispatching hogs: 4 cpu
stress-ng: info:  [721715] note: /proc/sys/kernel/sched_autogroup_enabled is 1 and this can impact scheduling throughput for processes not attached to a tty. Setting this to 0 may improve performance metrics
stress-ng: metrc: [721715] stressor       bogo ops real time  usr time  sys time   bogo ops/s     bogo ops/s
stress-ng: metrc: [721715]                           (secs)    (secs)    (secs)   (real time) (usr+sys time)
stress-ng: metrc: [721715] cpu               72878     30.00     83.96      0.39      2429.11         864.05
stress-ng: info:  [721715] skipped: 0
stress-ng: info:  [721715] passed: 4: cpu (4)
stress-ng: info:  [721715] failed: 0
stress-ng: info:  [721715] metrics untrustworthy: 0
stress-ng: info:  [721715] successful run completed in 30.01 secs
```

