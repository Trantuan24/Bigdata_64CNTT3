# K-Means MapReduce Analysis - Bài 4 TH2

## Tổng quan
Hệ thống K-Means MapReduce phân cụm 1000 điểm dữ liệu 2D thành 5 cụm sử dụng Hadoop.

## Cấu trúc project
```
TH2/kmeans_1000_points_analysis/
├── data/
│   ├── data_points_1000.txt      # 1000 điểm (x,y)
│   ├── initial_centroids.txt     # 5 tâm cụm ban đầu
│   └── final_centroids.txt       # Kết quả cuối cùng
├── src/
│   ├── data_generator.py         # Tạo dữ liệu
│   ├── mapper.py                 # Hadoop Mapper
│   ├── reducer.py                # Hadoop Reducer
│   ├── utils.py                  # Hàm tiện ích
│   ├── kmeans_driver.py          # Driver local
│   └── visualize_clusters.py     # Tạo biểu đồ
├── output/
│   ├── hadoop_results.json       # Kết quả Hadoop
│   └── kmeans_clusters_hadoop.png # Biểu đồ
├── run_mapreduce.sh              # Script chính
├── visualize.sh                  # Script tạo biểu đồ
└── README.md
```

## Thuật toán K-Means MapReduce

### Map Phase
- Đọc điểm dữ liệu (x,y)
- Tìm tâm cụm gần nhất (Euclidean distance)
- Emit (centroid_id, x,y)

### Shuffle & Sort
- Hadoop gom điểm theo centroid_id

### Reduce Phase
- Tính tâm cụm mới = trung bình các điểm
- Emit tâm cụm mới

## Cách sử dụng

### Bước 1: Tạo dữ liệu
```bash
cd src
python3 data_generator.py
```

### Bước 2: Chạy K-Means
```bash
# Chạy trên Hadoop
./run_mapreduce.sh --hadoop -k 5 -i 10

# Chạy local (nếu cần)
./run_mapreduce.sh -k 5 -i 10 -v
```

### Bước 3: Tạo biểu đồ
```bash
./visualize.sh
```

### Bước 4: Xem kết quả
```bash
# Kết quả JSON
cat output/hadoop_results.json

# Tâm cụm cuối
cat data/final_centroids.txt

# Biểu đồ
open output/kmeans_clusters_hadoop.png
```

## Xem trên Hadoop UI

### HDFS Files
- **URL**: http://localhost:9870
- **Path**: `/user/ubuntu/kmeans/`
- **Files**: input/, output/, cache/

### YARN Jobs
- **URL**: http://localhost:8088
- **Xem**: MapReduce jobs đang chạy

### Job History
- **URL**: http://localhost:19888
- **Xem**: Lịch sử jobs hoàn thành

## Kết quả mẫu

### Cluster Information
```
Cluster 0: 184 points - Centroid: (213.07, 353.06)
Cluster 1: 196 points - Centroid: (291.45, 779.24)
Cluster 2: 271 points - Centroid: (637.68, 508.76)
Cluster 3: 183 points - Centroid: (520.35, 935.89)
Cluster 4: 166 points - Centroid: (900.39, 313.72)
```

### JSON Output
```json
{
  "mode": "hadoop",
  "converged": true,
  "iterations": 2,
  "final_centroids": [
    [213.07, 353.06],
    [291.45, 779.24],
    [637.68, 508.76],
    [520.35, 935.89],
    [900.39, 313.72]
  ]
}
```

## Scripts

### run_mapreduce.sh
- **Chức năng**: Chạy K-Means trên Hadoop/Local
- **Options**: `-k` (clusters), `-i` (iterations), `--hadoop`, `-v` (verbose)
- **Output**: Tự động tải kết quả từ HDFS về local

### visualize.sh
- **Chức năng**: Tạo biểu đồ scatter plot
- **Input**: hadoop_results.json
- **Output**: kmeans_clusters_hadoop.png

## Tính năng
- ✅ Hadoop MapReduce clustering
- ✅ 1000 điểm dữ liệu, 5 cụm
- ✅ Tự động download kết quả từ HDFS
- ✅ Visualization với matplotlib
- ✅ JSON output structured
- ✅ Error handling

## Đường dẫn
- **Project**: `/home/ubuntu/bigdata/TH2/kmeans_1000_points_analysis/`
- **HDFS**: `/user/ubuntu/kmeans/`
- **UI**: http://localhost:9870/explorer.html#/user/ubuntu/kmeans
