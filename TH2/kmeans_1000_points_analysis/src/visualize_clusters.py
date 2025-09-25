#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sys

def load_data_points(filename):
    """Load data points from file"""
    points = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                x, y = map(float, line.strip().split(','))
                points.append((x, y))
    return points

def load_centroids_from_json(filename):
    """Load centroids from JSON results file"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['final_centroids']

def assign_points_to_clusters(points, centroids):
    """Assign each point to nearest centroid"""
    clusters = {i: [] for i in range(len(centroids))}
    
    for point in points:
        min_dist = float('inf')
        closest_cluster = 0
        
        for i, centroid in enumerate(centroids):
            dist = ((point[0] - centroid[0]) ** 2 + (point[1] - centroid[1]) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest_cluster = i
        
        clusters[closest_cluster].append(point)
    
    return clusters

def visualize_clusters(points, centroids, clusters, title="K-Means Clustering"):
    """Create visualization of clusters"""
    plt.figure(figsize=(12, 8))
    
    # Colors for clusters
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    
    # Plot points by cluster
    for cluster_id, cluster_points in clusters.items():
        if cluster_points:
            x_coords = [p[0] for p in cluster_points]
            y_coords = [p[1] for p in cluster_points]
            plt.scatter(x_coords, y_coords, c=colors[cluster_id % len(colors)], 
                       alpha=0.6, s=20, label=f'Cluster {cluster_id} ({len(cluster_points)} points)')
    
    # Plot centroids
    centroid_x = [c[0] for c in centroids]
    centroid_y = [c[1] for c in centroids]
    plt.scatter(centroid_x, centroid_y, c='black', marker='x', s=200, linewidths=3, label='Centroids')
    
    # Add centroid labels
    for i, (x, y) in enumerate(centroids):
        plt.annotate(f'C{i}', (x, y), xytext=(5, 5), textcoords='offset points', 
                    fontsize=12, fontweight='bold')
    
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return plt

def main():
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, 'data')
    output_dir = os.path.join(project_dir, 'output')
    
    print("🎨 K-Means Cluster Visualization")
    print("=" * 40)
    
    # Load data
    data_file = os.path.join(data_dir, 'data_points_1000.txt')
    if not os.path.exists(data_file):
        print("❌ Data file not found:", data_file)
        return
    
    points = load_data_points(data_file)
    print(f"📊 Loaded {len(points)} data points")
    
    # Try to load results from different sources
    results_files = [
        (os.path.join(output_dir, 'hadoop_results.json'), 'Hadoop'),
        (os.path.join(output_dir, 'kmeans_results.json'), 'Local')
    ]
    
    for results_file, mode in results_files:
        if os.path.exists(results_file):
            print(f"📈 Creating visualization for {mode} results...")
            
            try:
                centroids = load_centroids_from_json(results_file)
                print(f"🎯 Found {len(centroids)} centroids")
                
                # Assign points to clusters
                clusters = assign_points_to_clusters(points, centroids)
                
                # Print cluster info
                print("\n📋 Cluster Information:")
                for i, cluster_points in clusters.items():
                    print(f"  Cluster {i}: {len(cluster_points)} points - Centroid: ({centroids[i][0]:.2f}, {centroids[i][1]:.2f})")
                
                # Create visualization
                plt = visualize_clusters(points, centroids, clusters, 
                                       f"K-Means Clustering Results ({mode} Mode)")
                
                # Save plot
                plot_file = os.path.join(output_dir, f'kmeans_clusters_{mode.lower()}.png')
                plt.savefig(plot_file, dpi=300, bbox_inches='tight')
                print(f"💾 Saved plot: {plot_file}")
                
                # Show plot (optional - comment out if running headless)
                # plt.show()
                
            except Exception as e:
                print(f"❌ Error processing {mode} results: {e}")
        else:
            print(f"⚠️  {mode} results file not found: {results_file}")
    
    print("\n✨ Visualization completed!")

if __name__ == "__main__":
    main()
