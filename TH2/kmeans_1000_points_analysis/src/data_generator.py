#!/usr/bin/env python3
import random
import os

def main():
    print("🚀 K-Means Data Generator - TH2 Bài 4")
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(script_dir), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate 1000 points
    random.seed(42)
    points = [(random.randint(100, 1000), random.randint(100, 1000)) for _ in range(1000)]
    
    # Generate 5 centroids
    random.seed(123)
    centroids = [(random.randint(100, 1000), random.randint(100, 1000)) for _ in range(5)]
    
    # Save files
    with open(os.path.join(data_dir, 'data_points_1000.txt'), 'w') as f:
        for x, y in points:
            f.write(f"{x},{y}\n")
    
    with open(os.path.join(data_dir, 'initial_centroids.txt'), 'w') as f:
        for i, (x, y) in enumerate(centroids):
            f.write(f"{i},{x},{y}\n")
    
    print(f"✅ Generated 1000 points and 5 centroids")
    print(f"📁 Files saved in: {data_dir}")

if __name__ == "__main__":
    main()
