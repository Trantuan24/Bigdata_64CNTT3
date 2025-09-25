#!/bin/bash
"""
Script chạy Customer Spending Analysis trên Hadoop
"""

# Thiết lập đường dẫn
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
SRC_DIR="$PROJECT_DIR/src"
DATA_DIR="$PROJECT_DIR/data"

echo "🚀 Customer Spending Analysis - Hadoop MapReduce"
echo "==============================================="

# Kiểm tra Hadoop
if ! command -v hadoop &> /dev/null; then
    echo "❌ Hadoop không được tìm thấy. Kiểm tra HADOOP_HOME và PATH"
    exit 1
fi

# Kiểm tra file input
INPUT_FILE="$DATA_DIR/input_combined.txt"
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Không tìm thấy file input: $INPUT_FILE"
    echo "💡 Chạy data generator trước:"
    echo "   cd $SRC_DIR && python3 data_generator.py"
    exit 1
fi

# Thiết lập đường dẫn HDFS
HDFS_INPUT_DIR="/user/$(whoami)/customer_spending/input"
HDFS_OUTPUT_DIR="/user/$(whoami)/customer_spending/output"
LOCAL_OUTPUT_DIR="$PROJECT_DIR/output"

echo "📂 Chuẩn bị dữ liệu trên HDFS..."

# Xóa thư mục cũ nếu có
hdfs dfs -rm -r -f "$HDFS_INPUT_DIR" "$HDFS_OUTPUT_DIR"

# Tạo thư mục input trên HDFS
hdfs dfs -mkdir -p "$HDFS_INPUT_DIR"

# Upload file input lên HDFS
hdfs dfs -put "$INPUT_FILE" "$HDFS_INPUT_DIR/"

echo "✅ Đã upload dữ liệu lên HDFS"
echo "📊 Số records: $(wc -l < "$INPUT_FILE")"

# Chạy Hadoop MapReduce job
echo ""
echo "🔄 Chạy Hadoop MapReduce job..."

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files "$SRC_DIR/mapper.py","$SRC_DIR/reducer.py" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input "$HDFS_INPUT_DIR/input_combined.txt" \
    -output "$HDFS_OUTPUT_DIR"

if [ $? -ne 0 ]; then
    echo "❌ Hadoop MapReduce job thất bại!"
    exit 1
fi

echo "✅ Hadoop MapReduce job hoàn thành!"

# Tải kết quả về local
echo ""
echo "📥 Tải kết quả về local..."
mkdir -p "$LOCAL_OUTPUT_DIR"

hdfs dfs -get "$HDFS_OUTPUT_DIR/part-00000" "$LOCAL_OUTPUT_DIR/customer_spending_summary.csv.tmp"

# Thêm header CSV
{
    echo "Cust_ID,Customer_Name,Total_Spending,Transaction_Count"
    cat "$LOCAL_OUTPUT_DIR/customer_spending_summary.csv.tmp"
} > "$LOCAL_OUTPUT_DIR/customer_spending_summary.csv"

rm -f "$LOCAL_OUTPUT_DIR/customer_spending_summary.csv.tmp"

# Hiển thị kết quả
echo ""
echo "📊 KẾT QUẢ CUSTOMER SPENDING ANALYSIS"
echo "===================================="
echo ""

# Format output đẹp từ CSV
python3 -c "
import csv
import sys

with open('$LOCAL_OUTPUT_DIR/customer_spending_summary.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    # Print header
    print(f'{header[0]:<10} {header[1]:<20} {header[2]:<15} {header[3]:<18}')
    print('-' * 65)
    
    # Print data rows
    for row in reader:
        print(f'{row[0]:<10} {row[1]:<20} \${row[2]:<14} {row[3]:<18}')
"

echo ""
echo "📁 File kết quả: $LOCAL_OUTPUT_DIR/customer_spending_summary.csv"

# Thống kê tổng quan từ CSV
TOTAL_CUSTOMERS=$(($(wc -l < "$LOCAL_OUTPUT_DIR/customer_spending_summary.csv") - 1))  # Trừ header
TOTAL_SPENDING=$(awk -F',' 'NR>1 {sum += $3} END {printf "%.2f", sum}' "$LOCAL_OUTPUT_DIR/customer_spending_summary.csv")
TOTAL_TRANSACTIONS=$(awk -F',' 'NR>1 {sum += $4} END {print sum}' "$LOCAL_OUTPUT_DIR/customer_spending_summary.csv")

echo ""
echo "📈 THỐNG KÊ TỔNG QUAN"
echo "==================="
echo "• Tổng số khách hàng: $TOTAL_CUSTOMERS"
echo "• Tổng số giao dịch: $TOTAL_TRANSACTIONS"
echo "• Tổng doanh thu: \$${TOTAL_SPENDING}"
echo "• Trung bình chi tiêu/khách hàng: \$$(echo "scale=2; $TOTAL_SPENDING / $TOTAL_CUSTOMERS" | bc -l)"

echo ""
echo "✅ Hoàn thành Customer Spending Analysis trên Hadoop!"

# Hiển thị HDFS info
echo ""
echo "🗂️  HDFS Paths:"
echo "• Input: $HDFS_INPUT_DIR"
echo "• Output: $HDFS_OUTPUT_DIR"
