#!/bin/bash
"""
Script chạy Energy Consumption Analysis trên Hadoop
Tìm những năm có giá trị Average > 30
"""

# Thiết lập đường dẫn
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
SRC_DIR="$PROJECT_DIR/src"
DATA_DIR="$PROJECT_DIR/data"

echo "🏭 Energy Consumption Analysis - Hadoop MapReduce"
echo "================================================"

# Kiểm tra Hadoop
if ! command -v hadoop &> /dev/null; then
    echo "❌ Hadoop không được tìm thấy. Kiểm tra HADOOP_HOME và PATH"
    exit 1
fi

# Kiểm tra file input
INPUT_FILE="$DATA_DIR/energy_data.csv"
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Không tìm thấy file input: $INPUT_FILE"
    echo "💡 Chạy data generator trước:"
    echo "   cd $SRC_DIR && python3 data_generator.py"
    exit 1
fi

# Thiết lập đường dẫn HDFS
HDFS_INPUT_DIR="/user/$(whoami)/energy_consumption/input"
HDFS_OUTPUT_DIR="/user/$(whoami)/energy_consumption/output"
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

# Hiển thị preview dữ liệu
echo ""
echo "📋 Preview dữ liệu input:"
head -6 "$INPUT_FILE" | column -t -s ','

# Chạy Hadoop MapReduce job
echo ""
echo "🔄 Chạy Hadoop MapReduce job..."

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files "$SRC_DIR/mapper.py","$SRC_DIR/reducer.py" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input "$HDFS_INPUT_DIR/energy_data.csv" \
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

hdfs dfs -get "$HDFS_OUTPUT_DIR/part-00000" "$LOCAL_OUTPUT_DIR/high_consumption_years.txt"

# Hiển thị kết quả
echo ""
echo "📊 KẾT QUẢ ENERGY CONSUMPTION ANALYSIS"
echo "====================================="
echo ""

# Hiển thị kết quả từ file
cat "$LOCAL_OUTPUT_DIR/high_consumption_years.txt"

echo ""
echo "📁 File kết quả: $LOCAL_OUTPUT_DIR/high_consumption_years.txt"

# Thống kê từ kết quả
RESULT_FILE="$LOCAL_OUTPUT_DIR/high_consumption_years.txt"
if [ -f "$RESULT_FILE" ]; then
    # Đếm số năm (bỏ qua header và summary lines)
    TOTAL_YEARS=$(grep -E "^[0-9]{4}" "$RESULT_FILE" | wc -l)
    
    if [ $TOTAL_YEARS -gt 0 ]; then
        echo ""
        echo "📈 THỐNG KÊ TỔNG QUAN"
        echo "==================="
        echo "• Tổng số năm có Average > 30: $TOTAL_YEARS"
        
        # Lấy danh sách năm
        YEARS_LIST=$(grep -E "^[0-9]{4}" "$RESULT_FILE" | awk '{print $1}' | tr '\n' ', ' | sed 's/,$//')
        echo "• Các năm: $YEARS_LIST"
        
        # Tính giá trị cao nhất và thấp nhất
        HIGHEST=$(grep -E "^[0-9]{4}" "$RESULT_FILE" | awk '{print $2}' | sort -nr | head -1)
        LOWEST=$(grep -E "^[0-9]{4}" "$RESULT_FILE" | awk '{print $2}' | sort -n | head -1)
        
        echo "• Mức tiêu thụ cao nhất: $HIGHEST"
        echo "• Mức tiêu thụ thấp nhất (>30): $LOWEST"
        
        # Tính trung bình
        AVG=$(grep -E "^[0-9]{4}" "$RESULT_FILE" | awk '{sum += $2; count++} END {printf "%.2f", sum/count}')
        echo "• Trung bình các năm được filter: $AVG"
    else
        echo ""
        echo "📈 THỐNG KÊ: Không có năm nào có Average > 30"
    fi
fi

echo ""
echo "✅ Hoàn thành Energy Consumption Analysis trên Hadoop!"

# Hiển thị HDFS info
echo ""
echo "🗂️  HDFS Paths:"
echo "• Input: $HDFS_INPUT_DIR"
echo "• Output: $HDFS_OUTPUT_DIR"

# Hiển thị Web UI links
echo ""
echo "🌐 Web UI Monitoring:"
echo "• HDFS NameNode: http://localhost:9870"
echo "• YARN ResourceManager: http://localhost:8088"

echo ""
echo "🎯 Bài toán: Tìm những năm có giá trị Average > 30"
echo "📊 Kết quả đã được lưu tại: $LOCAL_OUTPUT_DIR/high_consumption_years.txt"
