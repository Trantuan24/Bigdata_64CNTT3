#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import load_centroids, find_closest_centroid, parse_point

def main():
    # Load centroids
    paths = ['current_centroids.txt', 'initial_centroids.txt', '../data/initial_centroids.txt', '../data/current_centroids.txt']
    centroids = None
    for path in paths:
        try:
            if os.path.exists(path):
                centroids = load_centroids(path)
                break
        except:
            continue
    
    if not centroids:
        sys.exit(1)
    
    # Process input
    for line in sys.stdin:
        line = line.strip()
        if line:
            try:
                point = parse_point(line)
                closest_id = find_closest_centroid(point, centroids)
                print(f"{closest_id}\t{point[0]},{point[1]}")
            except:
                continue

if __name__ == "__main__":
    main()
