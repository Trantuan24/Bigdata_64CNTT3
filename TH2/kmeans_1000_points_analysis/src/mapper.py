#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import load_centroids, find_closest_centroid, parse_point

def main():
    # Load centroids - check multiple possible paths
    paths = [
        'current_centroids.txt',           # Hadoop distributed cache
        'initial_centroids.txt',           # Hadoop distributed cache
        '../data/initial_centroids.txt',   # Relative from src/
        '../data/current_centroids.txt',   # Relative from src/
        'data/initial_centroids.txt',      # From project root
        'data/current_centroids.txt',      # From project root
        '/tmp/centroids.txt'               # Hadoop temp location
    ]
    
    centroids = None
    for path in paths:
        try:
            if os.path.exists(path):
                centroids = load_centroids(path)
                break
        except Exception as e:
            continue
    
    if not centroids:
        # Debug: print available files
        print(f"ERROR: No centroids found. Checked paths: {paths}", file=sys.stderr)
        print(f"Current working directory: {os.getcwd()}", file=sys.stderr)
        print(f"Files in current dir: {os.listdir('.')}", file=sys.stderr)
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
