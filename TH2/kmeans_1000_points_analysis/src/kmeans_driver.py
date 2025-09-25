#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import shutil
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import load_centroids, save_centroids, centroids_converged, calculate_wcss, parse_point

class KMeansDriver:
    def __init__(self, k=5, max_iterations=20, convergence_threshold=0.001):
        """
        Initialize K-Means driver
        
        Args:
            k: Number of clusters
            max_iterations: Maximum number of iterations
            convergence_threshold: Convergence threshold for centroids
        """
        self.k = k
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        
        # Setup paths
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.dirname(self.script_dir)
        self.data_dir = os.path.join(self.project_dir, 'data')
        self.output_dir = os.path.join(self.project_dir, 'output')
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Files
        self.data_file = os.path.join(self.data_dir, 'data_points_1000.txt')
        self.initial_centroids_file = os.path.join(self.data_dir, 'initial_centroids.txt')
        self.current_centroids_file = os.path.join(self.data_dir, 'current_centroids.txt')
        self.final_centroids_file = os.path.join(self.data_dir, 'final_centroids.txt')
        
        # MapReduce scripts
        self.mapper_script = os.path.join(self.script_dir, 'mapper.py')
        self.reducer_script = os.path.join(self.script_dir, 'reducer.py')
        
        # Results tracking
        self.iteration_history = []
        self.converged = False
        self.final_iteration = 0

    def run_local_mapreduce(self, iteration):
        """
        Run MapReduce locally using pipes
        
        Args:
            iteration: Current iteration number
        
        Returns:
            Path to output file
        """
        print(f"   🔄 Running MapReduce iteration {iteration}...")
        
        # Create iteration output directory
        iter_output_dir = os.path.join(self.output_dir, f'iteration_{iteration}')
        os.makedirs(iter_output_dir, exist_ok=True)
        
        # Set environment variable for centroids file
        env = os.environ.copy()
        env['CENTROIDS_FILE'] = self.current_centroids_file
        
        # Run mapper
        map_output_file = os.path.join(iter_output_dir, 'map_output.txt')
        with open(self.data_file, 'r') as input_file:
            with open(map_output_file, 'w') as output_file:
                mapper_process = subprocess.Popen(
                    ['python3', self.mapper_script],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.PIPE,
                    env=env
                )
                _, stderr = mapper_process.communicate()
                
                if mapper_process.returncode != 0:
                    raise Exception(f"Mapper failed: {stderr.decode()}")
        
        # Sort map output (simulate Hadoop shuffle & sort)
        sorted_output_file = os.path.join(iter_output_dir, 'sorted_output.txt')
        with open(map_output_file, 'r') as f:
            lines = f.readlines()
        
        # Sort by centroid_id (first part before tab)
        lines.sort(key=lambda x: int(x.split('\t')[0]) if '\t' in x else 0)
        
        with open(sorted_output_file, 'w') as f:
            f.writelines(lines)
        
        # Run reducer
        reduce_output_file = os.path.join(iter_output_dir, 'new_centroids.txt')
        with open(sorted_output_file, 'r') as input_file:
            with open(reduce_output_file, 'w') as output_file:
                reducer_process = subprocess.Popen(
                    ['python3', self.reducer_script],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.PIPE
                )
                _, stderr = reducer_process.communicate()
                
                if reducer_process.returncode != 0:
                    raise Exception(f"Reducer failed: {stderr.decode()}")
        
        return reduce_output_file

    def parse_reducer_output(self, output_file):
        """
        Parse reducer output to get new centroids
        
        Args:
            output_file: Path to reducer output file
        
        Returns:
            List of new centroids
        """
        new_centroids = [None] * self.k
        
        with open(output_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) == 2:
                    centroid_id = int(parts[0])
                    x, y = map(float, parts[1].split(','))
                    
                    if 0 <= centroid_id < self.k:
                        new_centroids[centroid_id] = (x, y)
        
        # Fill any missing centroids with previous values
        old_centroids = load_centroids(self.current_centroids_file)
        for i in range(self.k):
            if new_centroids[i] is None and i < len(old_centroids):
                new_centroids[i] = old_centroids[i]
        
        return [c for c in new_centroids if c is not None]

    def calculate_iteration_metrics(self, iteration):
        """
        Calculate metrics for current iteration
        
        Args:
            iteration: Current iteration number
        
        Returns:
            Dictionary with metrics
        """
        # Load current centroids
        centroids = load_centroids(self.current_centroids_file)
        
        # Load and assign points to clusters
        points_by_cluster = {i: [] for i in range(len(centroids))}
        
        with open(self.data_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    point = parse_point(line)
                    
                    # Find closest centroid
                    min_distance = float('inf')
                    closest_cluster = 0
                    
                    for i, centroid in enumerate(centroids):
                        distance = ((point[0] - centroid[0]) ** 2 + (point[1] - centroid[1]) ** 2) ** 0.5
                        if distance < min_distance:
                            min_distance = distance
                            closest_cluster = i
                    
                    points_by_cluster[closest_cluster].append(point)
        
        # Calculate WCSS
        wcss = calculate_wcss(points_by_cluster, centroids)
        
        # Calculate cluster sizes
        cluster_sizes = [len(points_by_cluster[i]) for i in range(len(centroids))]
        
        return {
            'iteration': iteration,
            'wcss': wcss,
            'cluster_sizes': cluster_sizes,
            'centroids': centroids
        }

    def run(self):
        """
        Run the complete K-Means algorithm
        
        Returns:
            Dictionary with results
        """
        print("🚀 Starting K-Means MapReduce Algorithm")
        print("=" * 50)
        print(f"   • Number of clusters (K): {self.k}")
        print(f"   • Max iterations: {self.max_iterations}")
        print(f"   • Convergence threshold: {self.convergence_threshold}")
        print(f"   • Data file: {os.path.basename(self.data_file)}")
        
        # Initialize with initial centroids
        if not os.path.exists(self.initial_centroids_file):
            raise FileNotFoundError(f"Initial centroids file not found: {self.initial_centroids_file}")
        
        # Copy initial centroids to current centroids
        shutil.copy2(self.initial_centroids_file, self.current_centroids_file)
        
        print(f"\n📍 Initial centroids loaded from {os.path.basename(self.initial_centroids_file)}")
        initial_centroids = load_centroids(self.current_centroids_file)
        for i, (x, y) in enumerate(initial_centroids):
            print(f"   • Centroid {i}: ({x:.2f}, {y:.2f})")
        
        # Main iteration loop
        print(f"\n🔄 Starting iterations...")
        
        for iteration in range(1, self.max_iterations + 1):
            print(f"\n--- Iteration {iteration} ---")
            
            # Save old centroids for convergence check
            old_centroids = load_centroids(self.current_centroids_file)
            
            # Run MapReduce
            try:
                output_file = self.run_local_mapreduce(iteration)
                
                # Parse new centroids
                new_centroids = self.parse_reducer_output(output_file)
                
                # Save new centroids
                save_centroids(new_centroids, self.current_centroids_file)
                
                # Calculate metrics
                metrics = self.calculate_iteration_metrics(iteration)
                self.iteration_history.append(metrics)
                
                print(f"   ✅ WCSS: {metrics['wcss']:.2f}")
                print(f"   📊 Cluster sizes: {metrics['cluster_sizes']}")
                
                # Check convergence
                if centroids_converged(old_centroids, new_centroids, self.convergence_threshold):
                    print(f"   🎯 Converged! Centroids moved less than {self.convergence_threshold}")
                    self.converged = True
                    self.final_iteration = iteration
                    break
                else:
                    # Calculate max movement
                    max_movement = 0
                    for old, new in zip(old_centroids, new_centroids):
                        movement = ((new[0] - old[0]) ** 2 + (new[1] - old[1]) ** 2) ** 0.5
                        max_movement = max(max_movement, movement)
                    print(f"   📏 Max centroid movement: {max_movement:.6f}")
                
            except Exception as e:
                print(f"   ❌ Error in iteration {iteration}: {e}")
                break
        
        # Finalize results
        self.final_iteration = iteration if not self.converged else self.final_iteration
        
        # Copy final centroids
        shutil.copy2(self.current_centroids_file, self.final_centroids_file)
        
        # Generate final results
        return self.generate_final_results()

    def generate_final_results(self):
        """
        Generate final clustering results
        
        Returns:
            Dictionary with complete results
        """
        print(f"\n🎉 K-Means Algorithm Completed!")
        print("=" * 50)
        
        # Load final centroids
        final_centroids = load_centroids(self.final_centroids_file)
        
        # Final metrics
        final_metrics = self.calculate_iteration_metrics(self.final_iteration)
        
        # Summary
        print(f"   • Converged: {'Yes' if self.converged else 'No'}")
        print(f"   • Total iterations: {self.final_iteration}")
        print(f"   • Final WCSS: {final_metrics['wcss']:.2f}")
        print(f"   • Final cluster sizes: {final_metrics['cluster_sizes']}")
        
        print(f"\n🎯 Final Centroids:")
        for i, (x, y) in enumerate(final_centroids):
            print(f"   • Cluster {i}: ({x:.2f}, {y:.2f}) - {final_metrics['cluster_sizes'][i]} points")
        
        # Save results to JSON
        results = {
            'algorithm': 'K-Means MapReduce',
            'parameters': {
                'k': self.k,
                'max_iterations': self.max_iterations,
                'convergence_threshold': self.convergence_threshold
            },
            'execution': {
                'converged': self.converged,
                'total_iterations': self.final_iteration,
                'timestamp': datetime.now().isoformat()
            },
            'final_results': {
                'wcss': final_metrics['wcss'],
                'cluster_sizes': final_metrics['cluster_sizes'],
                'centroids': final_centroids
            },
            'iteration_history': self.iteration_history
        }
        
        results_file = os.path.join(self.output_dir, 'kmeans_results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {os.path.basename(results_file)}")
        
        return results

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='K-Means MapReduce Driver')
    parser.add_argument('-k', '--clusters', type=int, default=5, help='Number of clusters')
    parser.add_argument('-i', '--iterations', type=int, default=20, help='Maximum iterations')
    parser.add_argument('-t', '--threshold', type=float, default=0.001, help='Convergence threshold')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        driver = KMeansDriver(
            k=args.clusters,
            max_iterations=args.iterations,
            convergence_threshold=args.threshold
        )
        
        results = driver.run()
        
        if args.verbose:
            print(f"\n📈 Iteration History:")
            for i, metrics in enumerate(results['iteration_history'], 1):
                print(f"   Iteration {i}: WCSS={metrics['wcss']:.2f}, Sizes={metrics['cluster_sizes']}")
        
        print(f"\n✨ K-Means clustering completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
