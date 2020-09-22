import random
import threading
import os

interval = 1
switch_id = "s1"
rules_counts = []


def count_rules():
    res = os.popen("sudo ovs-ofctl dump-flows %s | wc -l" % switch_id).readline()
    try:
        value = int(res[0])-1  # 第一条内容是 NXST_FLOW reply (xid=0x4):
        # rules_counts.append(value)
        print(value)  # 输出流表数量
    except ValueError:
        print("error parsing entry counts")

    timer = threading.Timer(interval, count_rules)
    timer.start()


if __name__ == "__main__":
    timer = threading.Timer(interval, count_rules)
    timer.start()
