#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if line:
        for word in line.split():
            if len(word) >= 2:
                print(f"{word}\t1")
