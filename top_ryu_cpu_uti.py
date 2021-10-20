#!/usr/bin/env python3
# coding=utf-8

# Author: $￥
# @Time: 2021/10/09 13:29

import threading
import os
import sys
import datetime
import psutil
import time

interval = 1
ratios = []

log_time = datetime.datetime.now().strftime("%y-%m-%d %H-%M-%S")
output_file_name = "top_ryu_uti %s.txt" % log_time


if __name__ == "__main__":
    cmd = "ps -ef | grep ryu-manager | grep -v grep | awk '{print $2}'"
    try:
        pid = int(os.popen(cmd).readlines()[0])
        print(pid)
        ryu_process = psutil.Process(pid)
    except Exception:
        print("no ryu pid")
        sys.exit(1)


    with open(file=output_file_name, mode="a+")as f:
        f.write(datetime.datetime.now().strftime("%y-%m-%d %H-%M-%S"))
        f.write("\n")

    while True:
        ratio = ryu_process.cpu_percent()
        print(ratio)
        ratios.append(ratio)

        if len(ratios) == 10:
            with open(file=output_file_name, mode="a+") as f:
                f.write("\n".join([str(num) for num in ratios]))
                f.write("\n")
            ratios.clear()

        time.sleep(1)

    
    # timer = threading.Timer(interval, write_utilization, args = (pid, ))

    # timer.start()


