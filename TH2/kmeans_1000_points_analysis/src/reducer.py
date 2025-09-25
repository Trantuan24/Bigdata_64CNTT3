#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import parse_point, format_point

def main():
    current_centroid = None
    points = []
    
    for line in sys.stdin:
        line = line.strip()
        if line:
            try:
                parts = line.split('\t')
                if len(parts) == 2:
                    centroid_id = int(parts[0])
                    point = parse_point(parts[1])
                    
                    if current_centroid is not None and centroid_id != current_centroid:
                        if points:
                            new_centroid = calculate_new_centroid(points)
                            print(f"{current_centroid}\t{format_point(new_centroid)}")
                        points = []
                    
                    current_centroid = centroid_id
                    points.append(point)
            except:
                continue
    
    if current_centroid is not None and points:
        new_centroid = calculate_new_centroid(points)
        print(f"{current_centroid}\t{format_point(new_centroid)}")

def calculate_new_centroid(points):
    if not points:
        return (0.0, 0.0)
    total_x = sum(p[0] for p in points)
    total_y = sum(p[1] for p in points)
    return (total_x / len(points), total_y / len(points))

if __name__ == "__main__":
    main()
