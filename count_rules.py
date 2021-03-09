import random
import threading
import os
import sys
import datetime

interval = 1
rules_counts = []
lock = threading.Lock()

log_time = datetime.datetime.now().strftime("%y-%m-%d %H:%M")
output_file_name = "count_rules %s.txt" % log_time


def count_rules(target_switch_id):
    global rules_counts

    # 获取target_switch_id对应的流表项count
    res = os.popen("sudo ovs-ofctl dump-flows %s | wc -l" % target_switch_id).readline()

    try:
        value = int(res[0])-1  # 第一条内容是 NXST_FLOW reply (xid=0x4):
        # rules_counts.append(value)
        print(value)  # 输出流表数量

        lock.acquire()
        rules_counts.append(value)
        lock.release()
    except ValueError:
        print("error parsing entry counts")
        return

    # 这里因为每1s获取一次，就不写Lock了
    inner_timer = threading.Timer(interval, count_rules, args=(target_switch_id, ))
    inner_timer.start()

    # 每10个时间单位，输出一次count 到 file 里
    lock.acquire()
    if len(rules_counts) == 10:
        with open(file=output_file_name, mode="a+")as f:
            f.write("\n".join([str(num) for num in rules_counts]))
            f.write("\n")
        rules_counts.clear()
    lock.release()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        switch_id = sys.argv[1]
    else:
        switch_id = "s1"

    timer = threading.Timer(interval, count_rules, args=(switch_id, ))
    timer.start()
