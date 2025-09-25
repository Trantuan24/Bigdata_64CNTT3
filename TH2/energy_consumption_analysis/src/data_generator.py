#!/usr/bin/env python3
"""
Energy Consumption Data Generator
Tạo dữ liệu năng lượng tiêu thụ từ bảng hình ảnh cho MapReduce analysis
"""

import csv
import os
import sys

def create_energy_data():
    """
    Tạo file energy_data.csv từ dữ liệu trong hình ảnh
    Format: year,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec,avg
    """
    
    # Dữ liệu từ hình ảnh
    energy_data = [
        # year, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec, avg
        [1979, 23, 23, 2, 43, 24, 25, 26, 26, 26, 26, 25, 26, 25],
        [1980, 26, 27, 28, 28, 28, 30, 31, 31, 31, 30, 30, 30, 29],
        [1981, 31, 32, 32, 32, 33, 34, 35, 36, 36, 34, 34, 34, 34],
        [1984, 39, 38, 39, 39, 39, 41, 42, 43, 40, 39, 38, 38, 40],
        [1985, 38, 39, 39, 39, 39, 41, 41, 41, 0, 40, 39, 39, 45]  # Note: Sep có giá trị 00 trong ảnh
    ]
    
    # Tạo thư mục data nếu chưa có
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Đường dẫn file output
    output_file = os.path.join(data_dir, 'energy_data.csv')
    
    print("🔄 Tạo file energy_data.csv...")
    
    # Ghi dữ liệu ra CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header
        writer.writerow(['year', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                        'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'avg'])
        
        # Data rows
        for row in energy_data:
            writer.writerow(row)
    
    print(f"✅ Đã tạo file: {output_file}")
    
    # Hiển thị thống kê
    print("\n📊 Thống kê dữ liệu:")
    print(f"- Tổng số năm: {len(energy_data)}")
    
    # Tìm những năm có avg > 30
    high_consumption_years = []
    for row in energy_data:
        year, avg = row[0], row[-1]
        if avg > 30:
            high_consumption_years.append((year, avg))
    
    print(f"- Số năm có Avg > 30: {len(high_consumption_years)}")
    print("- Chi tiết các năm có Avg > 30:")
    for year, avg in high_consumption_years:
        print(f"  + {year}: {avg}")
    
    return output_file

def create_extended_data():
    """
    Tạo thêm dữ liệu mở rộng để test MapReduce đầy đủ hơn
    """
    
    # Dữ liệu mở rộng (thêm một số năm khác)
    extended_data = [
        [1975, 18, 19, 20, 21, 22, 23, 24, 25, 24, 23, 22, 21, 22],  # avg <= 30
        [1976, 20, 21, 22, 23, 24, 25, 26, 27, 26, 25, 24, 23, 24],  # avg <= 30
        [1977, 22, 23, 24, 25, 26, 27, 28, 29, 28, 27, 26, 25, 26],  # avg <= 30
        [1978, 21, 22, 23, 24, 25, 26, 27, 28, 27, 26, 25, 24, 25],  # avg <= 30
        [1982, 33, 34, 35, 36, 37, 38, 39, 40, 39, 38, 37, 36, 37],  # avg > 30
        [1983, 35, 36, 37, 38, 39, 40, 41, 42, 41, 40, 39, 38, 39],  # avg > 30
        [1986, 40, 41, 42, 43, 44, 45, 46, 47, 46, 45, 44, 43, 44],  # avg > 30
        [1987, 28, 29, 30, 31, 32, 33, 34, 35, 34, 33, 32, 31, 32],  # avg > 30
        [1988, 25, 26, 27, 28, 29, 30, 31, 32, 31, 30, 29, 28, 29],  # avg <= 30
        [1989, 27, 28, 29, 30, 31, 32, 33, 34, 33, 32, 31, 30, 31],  # avg > 30
    ]
    
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    output_file = os.path.join(data_dir, 'energy_data_extended.csv')
    
    print("\n🔄 Tạo file energy_data_extended.csv...")
    
    # Kết hợp dữ liệu gốc và mở rộng
    original_data = [
        [1979, 23, 23, 2, 43, 24, 25, 26, 26, 26, 26, 25, 26, 25],
        [1980, 26, 27, 28, 28, 28, 30, 31, 31, 31, 30, 30, 30, 29],
        [1981, 31, 32, 32, 32, 33, 34, 35, 36, 36, 34, 34, 34, 34],
        [1984, 39, 38, 39, 39, 39, 41, 42, 43, 40, 39, 38, 38, 40],
        [1985, 38, 39, 39, 39, 39, 41, 41, 41, 0, 40, 39, 39, 45]
    ]
    
    all_data = original_data + extended_data
    all_data.sort(key=lambda x: x[0])  # Sort by year
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header
        writer.writerow(['year', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                        'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'avg'])
        
        # Data rows
        for row in all_data:
            writer.writerow(row)
    
    print(f"✅ Đã tạo file mở rộng: {output_file}")
    
    # Thống kê extended data
    high_consumption_count = sum(1 for row in all_data if row[-1] > 30)
    print(f"📊 Extended data: {len(all_data)} năm, {high_consumption_count} năm có Avg > 30")
    
    return output_file

def main():
    """
    Main function để tạo dữ liệu
    """
    print("=" * 60)
    print("🏭 ENERGY CONSUMPTION DATA GENERATOR")
    print("=" * 60)
    
    try:
        # Tạo dữ liệu chính từ hình ảnh
        main_file = create_energy_data()
        
        # Tạo dữ liệu mở rộng
        extended_file = create_extended_data()
        
        print("\n" + "=" * 60)
        print("✅ HOÀN THÀNH TẠO DỮ LIỆU")
        print("=" * 60)
        print(f"📁 File chính: {main_file}")
        print(f"📁 File mở rộng: {extended_file}")
        print("\n🚀 Sẵn sàng chạy MapReduce!")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
