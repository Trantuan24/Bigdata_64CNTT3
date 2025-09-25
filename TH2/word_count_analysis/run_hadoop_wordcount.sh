#!/bin/bash
set -e

# Paths
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HDFS_INPUT="/user/$(whoami)/wordcount/input"
HDFS_OUTPUT="/user/$(whoami)/wordcount/output"
INPUT_FILE="$PROJECT_DIR/data/cleaned_article.txt"
OUTPUT_FILE="$PROJECT_DIR/output/word_count_results.txt"
MAPPER="$PROJECT_DIR/src/mapper.py"
REDUCER="$PROJECT_DIR/src/reducer.py"

echo "🚀 Starting Word Count MapReduce on Hadoop"

# Check prerequisites
[ ! -f "$INPUT_FILE" ] && { echo "❌ Input file not found!"; exit 1; }
[ ! -f "$MAPPER" ] && { echo "❌ Mapper not found!"; exit 1; }
[ ! -f "$REDUCER" ] && { echo "❌ Reducer not found!"; exit 1; }
jps | grep -q "NameNode" || { echo "❌ Hadoop not running!"; exit 1; }

chmod +x "$MAPPER" "$REDUCER"
mkdir -p "$PROJECT_DIR/output"

# Setup HDFS
echo "🧹 Cleaning HDFS..."
hdfs dfs -rm -r -f "$HDFS_INPUT" "$HDFS_OUTPUT" 2>/dev/null || true
hdfs dfs -mkdir -p "$HDFS_INPUT"
hdfs dfs -put "$INPUT_FILE" "$HDFS_INPUT/"
echo "✅ Uploaded to HDFS"

# Run MapReduce
echo "🎯 Starting MapReduce job..."
START_TIME=$(date +%s)

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files "$MAPPER","$REDUCER" \
    -mapper "python3 $(basename "$MAPPER")" \
    -reducer "python3 $(basename "$REDUCER")" \
    -input "$HDFS_INPUT" \
    -output "$HDFS_OUTPUT"

DURATION=$(($(date +%s) - START_TIME))
echo "✅ Job completed in ${DURATION}s!"

# Download results
echo "⬇️ Downloading results..."
hdfs dfs -getmerge "$HDFS_OUTPUT/part-*" "$OUTPUT_FILE"

# Display results
echo "📈 Results Summary"
if [ -f "$OUTPUT_FILE" ]; then
    TOTAL_WORDS=$(wc -l < "$OUTPUT_FILE")
    TOTAL_COUNT=$(awk -F'\t' '{sum += $2} END {print sum}' "$OUTPUT_FILE")
    MAX_FREQ=$(head -1 "$OUTPUT_FILE" | cut -f2)
    
    echo "Total unique words: $TOTAL_WORDS"
    echo "Total occurrences: $TOTAL_COUNT"
    echo "Highest frequency: $MAX_FREQ"
    echo ""
    echo "Top 10 words:"
    head -10 "$OUTPUT_FILE" | while IFS=$'\t' read -r word count; do
        printf "%-15s %s\n" "$word" "$count"
    done
    echo ""
    echo "✅ Results: $OUTPUT_FILE"
else
    echo "❌ No output file!"
    exit 1
fi

# Optional cleanup
read -p "Cleanup HDFS? (y/N): " -n 1 -r
echo
[[ $REPLY =~ ^[Yy]$ ]] && hdfs dfs -rm -r "$HDFS_INPUT" "$HDFS_OUTPUT" && echo "🧹 HDFS cleaned"

echo "🎉 Word Count completed!"
