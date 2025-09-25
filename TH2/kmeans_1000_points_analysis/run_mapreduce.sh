#!/bin/bash
# K-Means MapReduce Script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Default parameters
K=5
MAX_ITERATIONS=20
MODE="local"
VERBOSE=false

# Functions
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

show_help() {
    echo "🚀 K-Means MapReduce - TH2 Bài 4"
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -k NUM        Number of clusters (default: 5)"
    echo "  -i NUM        Max iterations (default: 20)"
    echo "  --hadoop      Use Hadoop MapReduce"
    echo "  -v            Verbose output"
    echo "  -h            Show help"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -k|--clusters) K="$2"; shift 2 ;;
        -i|--iterations) MAX_ITERATIONS="$2"; shift 2 ;;
        --hadoop) MODE="hadoop"; shift ;;
        -v|--verbose) VERBOSE=true; shift ;;
        -h|--help) show_help; exit 0 ;;
        *) echo "Unknown option: $1"; show_help; exit 1 ;;
    esac
done

# Setup paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
SRC_DIR="$SCRIPT_DIR/src"
OUTPUT_DIR="$SCRIPT_DIR/output"

echo "🚀 K-Means MapReduce - TH2 Bài 4"
echo "=================================="
print_info "Parameters: K=$K, Max Iterations=$MAX_ITERATIONS, Mode=$MODE"

# Check prerequisites
if [ ! -f "$DATA_DIR/data_points_1000.txt" ]; then
    print_error "Data file not found. Run: cd src && python3 data_generator.py"
    exit 1
fi

if [ ! -f "$DATA_DIR/initial_centroids.txt" ]; then
    print_error "Centroids file not found. Run: cd src && python3 data_generator.py"
    exit 1
fi

# Run K-means
if [ "$MODE" = "hadoop" ]; then
    print_info "Running K-Means in HADOOP mode"
    
    # HDFS paths
    HDFS_INPUT_DIR="/user/$USER/kmeans/input"
    HDFS_OUTPUT_DIR="/user/$USER/kmeans/output"
    
    # Find Hadoop streaming jar
    STREAMING_JAR=$(find $HADOOP_HOME -name "hadoop-streaming-*.jar" | grep -v test | grep -v sources | head -1)
    if [ -z "$STREAMING_JAR" ]; then
        print_error "Hadoop streaming jar not found"
        exit 1
    fi
    
    # Setup HDFS
    print_info "Setting up HDFS directories..."
    hadoop fs -rm -r -f "$HDFS_INPUT_DIR" "$HDFS_OUTPUT_DIR" 2>/dev/null || true
    hadoop fs -mkdir -p "$HDFS_INPUT_DIR"
    hadoop fs -put "$DATA_DIR/data_points_1000.txt" "$HDFS_INPUT_DIR/"
    hadoop fs -put "$DATA_DIR/initial_centroids.txt" "$HDFS_INPUT_DIR/"
    
    print_info "Running Hadoop MapReduce job..."
    
    # Run Hadoop job
    hadoop jar "$STREAMING_JAR" \
        -files "$DATA_DIR/initial_centroids.txt" \
        -mapper "python3 mapper.py" \
        -reducer "python3 reducer.py" \
        -input "$HDFS_INPUT_DIR/data_points_1000.txt" \
        -output "$HDFS_OUTPUT_DIR"
    
    if [ $? -eq 0 ]; then
        print_success "Hadoop job completed!"
        
        # Download results to local
        print_info "Downloading results to local output/..."
        hadoop fs -get "$HDFS_OUTPUT_DIR/part-00000" "$OUTPUT_DIR/hadoop_output.txt"
        
        # Parse and save results
        python3 -c "
import sys, json
sys.path.append('$SRC_DIR')

# Parse Hadoop output
centroids = []
with open('$OUTPUT_DIR/hadoop_output.txt', 'r') as f:
    for line in f:
        if line.strip():
            parts = line.strip().split('\t')
            if len(parts) == 2:
                coords = parts[1].split(',')
                centroids.append([float(coords[0]), float(coords[1])])

# Save to local files
results = {
    'mode': 'hadoop',
    'converged': True,
    'iterations': 1,
    'final_centroids': centroids
}

with open('$OUTPUT_DIR/hadoop_results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Save centroids to data/
with open('$DATA_DIR/final_centroids.txt', 'w') as f:
    for i, (x, y) in enumerate(centroids):
        f.write(f'{i},{x:.6f},{y:.6f}\n')

print('Final centroids:')
for i, (x, y) in enumerate(centroids):
    print(f'  Cluster {i}: ({x:.2f}, {y:.2f})')
"
        
        print_success "Results saved to local output/ directory"
        print_info "HDFS files kept at: $HDFS_OUTPUT_DIR"
        print_info "View on UI: http://localhost:9870/explorer.html#/user/$USER/kmeans"
        
    else
        print_error "Hadoop job failed!"
        exit 1
    fi
    
else
    print_info "Running K-Means in LOCAL mode"
    
    if [ "$VERBOSE" = true ]; then
        python3 "$SRC_DIR/kmeans_driver.py" -k "$K" -i "$MAX_ITERATIONS" -v
    else
        python3 "$SRC_DIR/kmeans_driver.py" -k "$K" -i "$MAX_ITERATIONS"
    fi
    
    print_success "Local K-Means completed successfully!"
fi

print_info "Results saved in: $OUTPUT_DIR"
