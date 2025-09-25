#!/usr/bin/env python3
"""
Energy Consumption Mapper
Filter những năm có giá trị Average > 30
"""

import sys
import csv
from io import StringIO

def process_line(line):
    """
    Xử lý từng dòng dữ liệu
    Input format: year,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec,avg
    Output: Chỉ emit những năm có avg > 30
    """
    try:
        # Bỏ qua dòng trống
        line = line.strip()
        if not line:
            return
        
        # Bỏ qua header
        if line.startswith('year') or line.startswith('Year'):
            return
        
        # Parse CSV line
        csv_reader = csv.reader(StringIO(line))
        row = next(csv_reader)
        
        # Kiểm tra số lượng cột
        if len(row) < 14:
            return
        
        # Lấy year và avg
        year = int(row[0])
        avg = float(row[13])  # Cột cuối cùng là avg
        
        # Filter: Chỉ emit nếu avg > 30
        if avg > 30:
            # Emit key-value pair: (year, avg)
            print(f"{year}\t{avg}")
            
    except (ValueError, IndexError, StopIteration) as e:
        # Bỏ qua dòng lỗi, ghi log ra stderr
        print(f"Mapper error processing line: {line.strip()}", file=sys.stderr)
        print(f"Error details: {e}", file=sys.stderr)

def main():
    """
    Main mapper function
    Đọc từ stdin và xử lý từng dòng
    """
    try:
        for line in sys.stdin:
            process_line(line)
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Mapper fatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
