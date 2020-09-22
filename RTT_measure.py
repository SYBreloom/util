# coding=utf-8

# Author: $￥
# @Time: 2020/09/22 19:57
import os
import re
import threading

interval = 1
address = "www.baidu.com"


def get_RTT():
    res = os.popen("ping %s -c 1" % address).readlines()
    # print (len(res))
    for i in res:
        a = re.findall("time=(.+?) ms", i)  # 只有一行会输出 icmp_seq=3 ttl=128 time=54.4 ms
        if len(a) != 0:
            print(a[0])  # 使用ping-c的时候，只有一个time的匹配，直接输出了
    timer = threading.Timer(interval, get_RTT)
    timer.start()


if __name__ == "__main__":
    timer = threading.Timer(interval, get_RTT)
    timer.start()
