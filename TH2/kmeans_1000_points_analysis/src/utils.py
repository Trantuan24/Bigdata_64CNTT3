#!/usr/bin/env python3
import math
import os

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def find_closest_centroid(point, centroids):
    min_distance = float('inf')
    closest_centroid = 0
    for i, centroid in enumerate(centroids):
        distance = euclidean_distance(point, centroid)
        if distance < min_distance:
            min_distance = distance
            closest_centroid = i
    return closest_centroid

def load_centroids(filename):
    centroids = []
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Centroids file not found: {filename}")
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                if '\t' in line:  # Hadoop format: "index\tx,y"
                    parts = line.split('\t')
                    if len(parts) == 2:
                        coord_parts = parts[1].split(',')
                        if len(coord_parts) == 2:
                            centroids.append((float(coord_parts[0]), float(coord_parts[1])))
                else:  # Regular formats
                    parts = line.split(',')
                    if len(parts) >= 3:  # Format: index,x,y
                        centroids.append((float(parts[1]), float(parts[2])))
                    elif len(parts) == 2:  # Format: x,y
                        centroids.append((float(parts[0]), float(parts[1])))
    return centroids

def save_centroids(centroids, filename):
    with open(filename, 'w') as f:
        for i, (x, y) in enumerate(centroids):
            f.write(f"{i},{x:.6f},{y:.6f}\n")

def calculate_wcss(points_by_cluster, centroids):
    total_wcss = 0.0
    for cluster_id, points in points_by_cluster.items():
        if cluster_id < len(centroids):
            centroid = centroids[cluster_id]
            for point in points:
                distance = euclidean_distance(point, centroid)
                total_wcss += distance ** 2
    return total_wcss

def centroids_converged(old_centroids, new_centroids, threshold=0.001):
    if len(old_centroids) != len(new_centroids):
        return False
    for old, new in zip(old_centroids, new_centroids):
        if euclidean_distance(old, new) > threshold:
            return False
    return True

def parse_point(line):
    parts = line.strip().split(',')
    if len(parts) != 2:
        raise ValueError(f"Invalid point format: {line}")
    return (float(parts[0]), float(parts[1]))

def format_point(point):
    x, y = point
    return f"{x:.6f},{y:.6f}"
