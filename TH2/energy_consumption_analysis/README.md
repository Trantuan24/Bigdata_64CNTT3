# Energy Consumption Analysis với MapReduce

## 📋 Mô tả bài toán

Tìm những năm có giá trị năng lượng tiêu thụ trung bình (Average) lớn hơn 30, sử dụng kỹ thuật MapReduce trên dữ liệu năng lượng tiêu thụ hàng năm của một công ty.

### Input Data:
- **energy_data.csv**: Dữ liệu năng lượng tiêu thụ hàng tháng và trung bình 5 năm liên tiếp
- **Format**: year,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec,avg

### Output:
- Danh sách những năm có giá trị Average > 30
- Thống kê tổng quan về mức tiêu thụ năng lượng

## 🏗️ Kiến trúc MapReduce

### Map Phase:
- **Input**: Records từ file CSV với format: year,jan,feb,...,dec,avg
- **Logic**: 
  - Parse từng dòng CSV
  - Kiểm tra giá trị avg (cột cuối cùng)
  - Nếu avg > 30 → emit `(year, avg)`
  - Nếu avg ≤ 30 → bỏ qua (không emit)
- **Output**: Key-Value pairs chỉ chứa những năm thỏa mãn điều kiện

### Reduce Phase:
- **Input**: Tất cả cặp (year, avg) đã được filter từ Map phase
- **Logic**: 
  - Sắp xếp theo năm
  - Format output đẹp với header
  - Tính toán thống kê tổng quan
- **Output**: Danh sách năm và mức tiêu thụ, kèm summary statistics

## 📁 Cấu trúc Project

```
energy_consumption_analysis/
├── data/
│   ├── energy_data.csv          # Dữ liệu chính 
│   └── energy_data_extended.csv # Dữ liệu mở rộng để test
├── src/
│   ├── data_generator.py        # Tạo dữ liệu CSV từ hình ảnh
│   ├── mapper.py                # Map phase logic - filter avg > 30
│   └── reducer.py               # Reduce phase logic - format output
├── output/                      # Kết quả output từ Hadoop
├── run_mapreduce.sh             # Script chạy MapReduce trên Hadoop
└── README.md                    # Tài liệu này
```

## 🚀 Cách sử dụng

### 1. Tạo dữ liệu từ hình ảnh:
```bash
cd src/
python3 data_generator.py
```

### 2. Chạy MapReduce trên Hadoop:
```bash
chmod +x run_mapreduce.sh
./run_mapreduce.sh
```

## 📊 Kết quả mẫu

```
Year    Average_Consumption
----    -------------------
1981    34
1984    40
1985    45

========================================
SUMMARY STATISTICS
========================================
Total years with Avg > 30: 3
Years: 1981, 1984, 1985
Highest consumption: 45
Lowest consumption (>30): 34
Average of filtered years: 39.67
```

## 🔧 Yêu cầu hệ thống

- Python 3.6+
- Hadoop 3.x (cho chế độ Hadoop)
- Bash shell
- bc calculator (cho thống kê)

## 📈 Tính năng

- ✅ Filter dữ liệu theo điều kiện Average > 30
- ✅ Xử lý dữ liệu CSV format
- ✅ Chạy MapReduce trên Hadoop cluster
- ✅ Thống kê tổng quan (số năm, giá trị cao/thấp nhất, trung bình)
- ✅ Format output đẹp và dễ đọc
- ✅ Error handling và logging
- ✅ Tự động upload/download từ HDFS
- ✅ Dữ liệu mở rộng để test đầy đủ

## 🐛 Troubleshooting

### Lỗi phổ biến:
1. **File input không tồn tại**: Chạy `data_generator.py` trước
2. **Permission denied**: `chmod +x run_mapreduce.sh`
3. **Hadoop not found**: Kiểm tra `HADOOP_HOME` và `PATH`
4. **bc command not found**: `sudo apt install bc`

### Logs:
- Hadoop: Check Hadoop logs tại `/opt/hadoop/logs/`
- YARN: Web UI tại `http://localhost:8088`

## 🗂️ Đường dẫn HDFS và Monitoring

### HDFS File System:
```
/user/ubuntu/energy_consumption/
├── input/
│   └── energy_data.csv           # Input data uploaded từ local
└── output/
    ├── _SUCCESS                  # Marker file báo job thành công
    └── part-00000               # Kết quả thực từ MapReduce
```

### Web UI Monitoring:
- **HDFS NameNode**: http://localhost:9870
  - Xem file system: Utilities → Browse the file system
  - Đường dẫn: `/user/ubuntu/energy_consumption/`
- **YARN ResourceManager**: http://localhost:8088
  - Theo dõi MapReduce jobs
  - Xem logs và metrics

### Cách Download Output từ Hadoop:
```bash
# Xem files trên HDFS
hdfs dfs -ls /user/ubuntu/energy_consumption/output

# Download kết quả về local
hdfs dfs -get /user/ubuntu/energy_consumption/output/part-00000 ./result.txt

# Hoặc xem trực tiếp trên HDFS
hdfs dfs -cat /user/ubuntu/energy_consumption/output/part-00000
```

## 📝 Ghi chú kỹ thuật

- Sử dụng CSV format cho input/output
- Filter logic đơn giản: so sánh số với threshold
- Không cần JOIN như bài Customer Spending
- Hadoop Streaming API để chạy Python scripts
- Tự động upload input và download output
- Error handling cho dữ liệu CSV không hợp lệ
