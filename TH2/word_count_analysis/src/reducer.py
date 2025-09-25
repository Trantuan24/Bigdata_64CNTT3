#!/usr/bin/env python3
import sys
from collections import defaultdict

word_counts = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if line:
        try:
            word, count = line.split('\t')
            word_counts[word] += int(count)
        except ValueError:
            continue

# Sort by count desc, then by word
for word, count in sorted(word_counts.items(), key=lambda x: (-x[1], x[0])):
    print(f"{word}\t{count}")
