# K-Means Clustering Analysis với MapReduce

## 📋 Mô tả bài toán

Phân cụm 1000 điểm dữ liệu 2D thành 5 cụm sử dụng thuật toán K-Means với kỹ thuật MapReduce trên Hadoop.

### Input Data:
- **data_points_1000.txt**: 1000 điểm dữ liệu 2D với tọa độ (x,y) trong khoảng [100, 1000]
- **initial_centroids.txt**: 5 tâm cụm khởi tạo ngẫu nhiên

### Output:
- Tâm cụm cuối cùng sau khi hội tụ
- Phân bố điểm dữ liệu theo từng cụm
- Biểu đồ trực quan hóa kết quả phân cụm

## 🏗️ Kiến trúc MapReduce

### Map Phase:
- **Input**: Điểm dữ liệu (x,y) và danh sách tâm cụm hiện tại
- **Logic**: 
  - Tính khoảng cách Euclidean từ điểm đến tất cả tâm cụm
  - Tìm tâm cụm gần nhất
  - Emit `(centroid_id, "x,y")`
- **Output**: Key-Value pairs với centroid_id làm key

### Reduce Phase:
- **Input**: Tất cả điểm được gán cho cùng một centroid_id
- **Logic**: 
  - Tính trung bình tọa độ x và y của tất cả điểm
  - Tạo tâm cụm mới
- **Output**: Tâm cụm mới `(centroid_id, new_x, new_y)`

### Iterative Process:
- Driver điều khiển vòng lặp K-Means
- Kiểm tra điều kiện hội tụ (threshold < 0.001)
- Dừng khi hội tụ hoặc đạt số iteration tối đa

## 📁 Cấu trúc Project

```
kmeans_1000_points_analysis/
├── data/
│   ├── data_points_1000.txt      # 1000 điểm dữ liệu 2D
│   ├── initial_centroids.txt     # 5 tâm cụm ban đầu
│   └── final_centroids.txt       # Tâm cụm cuối cùng
├── src/
│   ├── data_generator.py         # Tạo dữ liệu ngẫu nhiên
│   ├── utils.py                  # Hàm tiện ích (distance, convergence)
│   ├── mapper.py                 # Map phase logic
│   ├── reducer.py                # Reduce phase logic
│   ├── kmeans_driver.py          # Driver điều khiển vòng lặp
│   └── visualize_clusters.py     # Trực quan hóa kết quả
├── output/                       # Kết quả output từ Hadoop
├── run_mapreduce.sh              # Script chạy MapReduce trên Hadoop
└── README.md                     # Tài liệu này
```

## 🚀 Cách sử dụng

### 1. Tạo dữ liệu ngẫu nhiên:
```bash
cd src/
python3 data_generator.py
```

### 2. Chạy MapReduce trên Hadoop:
```bash
chmod +x run_mapreduce.sh
./run_mapreduce.sh --hadoop -k 5 -i 10
```

### 3. Tạo biểu đồ trực quan:
```bash
python3 src/visualize_clusters.py
```

## 📊 Kết quả mẫu

```
========================================
K-MEANS CLUSTERING RESULTS
========================================
Mode: Hadoop MapReduce
Converged: True
Total Iterations: 2
Total Points: 1000
Number of Clusters: 5

Cluster Distribution:
Cluster 0: 184 points - Centroid: (213.07, 353.06)
Cluster 1: 196 points - Centroid: (291.45, 779.24)
Cluster 2: 271 points - Centroid: (637.68, 508.76)
Cluster 3: 183 points - Centroid: (520.35, 935.89)
Cluster 4: 166 points - Centroid: (900.39, 313.72)

WCSS (Within-Cluster Sum of Squares): 28,464,891.55
```

## 🔧 Yêu cầu hệ thống

- Python 3.6+
- Hadoop 3.x (cho chế độ Hadoop)
- Bash shell
- matplotlib, numpy (cho visualization)
- bc calculator (cho thống kê)

## 📈 Tính năng

- ✅ Thuật toán K-Means hoàn chỉnh với MapReduce
- ✅ Xử lý 1000 điểm dữ liệu, phân thành 5 cụm
- ✅ Chạy MapReduce trên Hadoop cluster
- ✅ Kiểm tra hội tụ tự động
- ✅ Trực quan hóa kết quả với matplotlib
- ✅ Tính toán WCSS (Within-Cluster Sum of Squares)
- ✅ Dual mode: Local pipes + Hadoop streaming
- ✅ Error handling và logging chi tiết
- ✅ Tự động upload/download từ HDFS
- ✅ JSON output structured với metadata

## 🐛 Troubleshooting

### Lỗi phổ biến:
1. **File input không tồn tại**: Chạy `data_generator.py` trước
2. **Permission denied**: `chmod +x run_mapreduce.sh`
3. **Hadoop not found**: Kiểm tra `HADOOP_HOME` và `PATH`
4. **matplotlib not found**: `pip3 install matplotlib numpy`
5. **Centroids file not found**: Kiểm tra distributed cache setup

### Logs:
- Hadoop: Check Hadoop logs tại `/opt/hadoop/logs/`
- YARN: Web UI tại `http://localhost:8088`
- Driver: Check console output cho convergence progress

## 🗂️ Đường dẫn HDFS và Monitoring

### HDFS File System:
```
/user/ubuntu/kmeans/
├── input/
│   └── data_points_1000.txt     # Input data uploaded từ local
├── cache/
│   └── centroids.txt            # Distributed cache cho tâm cụm
└── output/
    ├── _SUCCESS                 # Marker file báo job thành công
    └── part-00000              # Tâm cụm mới từ MapReduce
```

### Web UI Monitoring:
- **HDFS NameNode**: http://localhost:9870
  - Xem file system: Utilities → Browse the file system
  - Đường dẫn: `/user/ubuntu/kmeans/`
- **YARN ResourceManager**: http://localhost:8088
  - Theo dõi MapReduce jobs
  - Xem logs và metrics
- **Job History**: http://localhost:19888
  - Lịch sử các jobs đã hoàn thành

### Cách Download Output từ Hadoop:
```bash
# Xem files trên HDFS
hdfs dfs -ls /user/ubuntu/kmeans/output

# Download kết quả về local
hdfs dfs -get /user/ubuntu/kmeans/output/part-00000 ./new_centroids.txt

# Hoặc xem trực tiếp trên HDFS
hdfs dfs -cat /user/ubuntu/kmeans/output/part-00000
```

## 📝 Ghi chú kỹ thuật

- Sử dụng Euclidean distance cho tính toán khoảng cách
- Distributed cache để chia sẻ centroids cho tất cả mappers
- Convergence check dựa trên threshold 0.001
- Hadoop Streaming API để chạy Python scripts
- Iterative MapReduce với driver điều khiển vòng lặp
- WCSS calculation để đánh giá chất lượng clustering
- Reproducible results với random seed cố định
