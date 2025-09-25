#!/bin/bash
# K-Means Visualization Script

echo "🎨 K-Means Cluster Visualization"
echo "================================"

cd "$(dirname "$0")"

# Check if results exist
if [ ! -f "output/hadoop_results.json" ]; then
    echo "❌ No results found. Run K-Means first:"
    echo "   ./run_mapreduce.sh --hadoop -k 5 -i 2"
    exit 1
fi

# Run visualization
python3 src/visualize_clusters.py

# Show results
echo ""
echo "📂 Generated files:"
ls -la output/*.png 2>/dev/null || echo "   No PNG files found"

echo ""
echo "🖼️  To view the plot:"
echo "   Open: output/kmeans_clusters_hadoop.png"
