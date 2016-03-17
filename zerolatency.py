#!/usr/bin/env python
import time
fd = open("/dev/cpu_dma_latency", "w")
print >> fd, "0"

while True:
    time.sleep(5)
