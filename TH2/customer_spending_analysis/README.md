# Customer Spending Analysis với MapReduce

## 📋 Mô tả bài toán

Thống kê tổng số tiền đã chi của mỗi khách hàng từ cơ sở dữ liệu cửa hàng thể thao đa quốc gia, sử dụng kỹ thuật MapReduce.

### Input Data:
- **cust_details**: Thông tin chi tiết khách hàng (Cust ID, First Name, Last Name, Age, Profession)
- **transaction_details**: Thông tin giao dịch (Trans ID, Date, Cust ID, Amount, Game Type, Equipment, City, State, Mode)

### Output:
- Tổng số tiền đã chi của mỗi khách hàng
- Số lượng giao dịch của mỗi khách hàng

## 🏗️ Kiến trúc MapReduce

### Map Phase:
- **Input**: Records từ cả 2 bảng với prefix phân biệt (CUST: và TRANS:)
- **Logic**: 
  - Customer records → emit `(cust_id, "CUST:customer_name")`
  - Transaction records → emit `(cust_id, "TRANS:amount")`
- **Output**: Key-Value pairs với cust_id làm key

### Reduce Phase:
- **Input**: Tất cả records có cùng cust_id
- **Logic**: 
  - Tách customer info và transaction amounts
  - Tính tổng amount và đếm số giao dịch
- **Output**: `(cust_id, customer_name, total_spending, transaction_count)`

## 📁 Cấu trúc Project

```
customer_spending_analysis/
├── data/
│   ├── cust_details.csv          # Dữ liệu khách hàng (CSV format)
│   ├── transaction_details.csv   # Dữ liệu giao dịch (CSV format)
│   └── input_combined.txt        # Input kết hợp cho MapReduce
├── src/
│   ├── data_generator.py         # Tạo dữ liệu mẫu CSV
│   ├── mapper.py                 # Map phase logic
│   └── reducer.py                # Reduce phase logic
├── output/                       # Kết quả output CSV từ Hadoop
├── run_mapreduce.sh              # Script chạy MapReduce trên Hadoop
└── README.md                     # Tài liệu này
```

## 🚀 Cách sử dụng

### 1. Tạo dữ liệu mẫu:
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
Cust_ID    Customer_Name     Total_Spending    Transaction_Count
4000001    Kristina Chung    245.67           3
4000002    Paige Chen        189.23           2
4000003    Sherri Melton     567.89           4
...
```

## 🔧 Yêu cầu hệ thống

- Python 3.6+
- Hadoop 3.x (cho chế độ Hadoop)
- Bash shell
- bc calculator (cho thống kê)

## 📈 Tính năng

- ✅ JOIN 2 bảng dữ liệu trong MapReduce
- ✅ Tính tổng spending cho mỗi khách hàng
- ✅ Đếm số giao dịch của mỗi khách hàng
- ✅ Chạy MapReduce trên Hadoop cluster
- ✅ Thống kê tổng quan (tổng khách hàng, tổng doanh thu, trung bình)
- ✅ Format output CSV đẹp và dễ đọc
- ✅ Error handling và logging
- ✅ Tự động upload/download từ HDFS

## 🐛 Troubleshooting

### Lỗi phổ biến:
1. **File input không tồn tại**: Chạy `data_generator.py` trước
2. **Permission denied**: `chmod +x scripts/*.sh`
3. **Hadoop not found**: Kiểm tra `HADOOP_HOME` và `PATH`
4. **bc command not found**: `sudo apt install bc`

### Logs:
- Hadoop: Check Hadoop logs tại `/opt/hadoop/logs/`
- YARN: Web UI tại `http://localhost:8088`

## 🗂️ Đường dẫn HDFS và Monitoring

### HDFS File System:
```
/user/ubuntu/customer_spending/
├── input/
│   └── input_combined.txt        # Input data uploaded từ local
└── output/
    ├── _SUCCESS                  # Marker file báo job thành công
    └── part-00000               # Kết quả thực từ MapReduce
```

### Web UI Monitoring:
- **HDFS NameNode**: http://localhost:9870
  - Xem file system: Utilities → Browse the file system
  - Đường dẫn: `/user/ubuntu/customer_spending/`
- **YARN ResourceManager**: http://localhost:8088
  - Theo dõi MapReduce jobs
  - Xem logs và metrics

### Cách Download Output từ Hadoop:
```bash
# Xem files trên HDFS
hdfs dfs -ls /user/ubuntu/customer_spending/output

# Download kết quả về local
hdfs dfs -get /user/ubuntu/customer_spending/output/part-00000 ./result.csv

# Hoặc xem trực tiếp trên HDFS
hdfs dfs -cat /user/ubuntu/customer_spending/output/part-00000
```

## 📝 Ghi chú kỹ thuật

- Sử dụng CSV format cho input/output
- Prefix "CUST:" và "TRANS:" để phân biệt record types
- Sort phase quan trọng cho reducer hoạt động đúng
- Hadoop Streaming API để chạy Python scripts
- Tự động upload input và download output
