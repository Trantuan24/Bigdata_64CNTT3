# Word Count Analysis với MapReduce

## 📋 Mô tả bài toán

Thống kê tần suất xuất hiện của các từ trong bài báo tiếng Việt, sử dụng kỹ thuật MapReduce với data cleaning pipeline hoàn chỉnh.

### Input Data:
- **raw_article.txt**: Bài báo gốc từ VnExpress 
- **cleaned_article.txt**: Text đã làm sạch 
- **Format**: Plain text tiếng Việt có dấu

### Output:
- Danh sách tần suất các từ sắp xếp theo thứ tự giảm dần
- Thống kê tổng quan về tần suất từ

## 🏗️ Kiến trúc MapReduce

### Map Phase:
- **Input**: Dòng text từ file đã làm sạch
- **Logic**: 
  - Tokenize text thành các từ riêng biệt
  - Loại bỏ từ ngắn hơn 2 ký tự
  - Emit `(word, 1)` cho mỗi từ
- **Output**: Key-Value pairs với từ làm key, count = 1

### Reduce Phase:
- **Input**: Tất cả cặp (word, 1) đã được group theo word
- **Logic**: 
  - Tính tổng count cho mỗi từ
  - Sắp xếp theo tần suất giảm dần
- **Output**: `(word, total_count)` đã sắp xếp

## 📁 Cấu trúc Project
```
word_count_analysis/
├── data/
│   ├── raw_article.txt           # Bài báo gốc từ VnExpress
│   ├── cleaned_article.txt       # Text đã làm sạch
│   └── article_metadata.json     # Metadata (URL, title, stats)
├── src/
│   ├── crawler.py               # Crawl bài báo từ VnExpress
│   ├── text_cleaner.py          # Vietnamese text cleaning pipeline
│   ├── mapper.py                # Map phase logic
│   └── reducer.py               # Reduce phase logic
├── output/                      # Kết quả output từ Hadoop
├── run_hadoop_wordcount.sh      # Script chạy MapReduce trên Hadoop
└── README.md                    # Tài liệu này
```

## 🚀 Cách sử dụng

### 1. Crawl bài báo mới:
```bash
cd src/
python3 crawler.py
```

### 2. Làm sạch text:
```bash
python3 text_cleaner.py
```

### 3. Chạy MapReduce trên Hadoop:
```bash
chmod +x run_hadoop_wordcount.sh
./run_hadoop_wordcount.sh
```

## 📊 Kết quả mẫu

```
Word            Count
----            -----
nvidia          16
điện         16
openai          13
trong           13
công           12
của           11
sẽ            11
và             10
có             9
tư             9

========================================
SUMMARY STATISTICS
========================================
Total unique words: 371
Total word occurrences: 846
Highest frequency: 16
Lowest frequency: 1
Average frequency: 2.28
```

## 🔧 Yêu cầu hệ thống

- Python 3.6+
- Hadoop 3.x (cho chế độ Hadoop)
- Bash shell
- requests, beautifulsoup4 (cho crawler)
- bc calculator (cho thống kê)

## 📈 Tính năng

- ✅ Crawl tự động bài báo từ VnExpress
- ✅ Data cleaning hoàn chỉnh cho tiếng Việt
- ✅ Chạy MapReduce trên Hadoop cluster
- ✅ Thống kê tần suất từ chi tiết
- ✅ Format output đẹp và dễ đọc
- ✅ Error handling và logging
- ✅ Tự động upload/download từ HDFS
- ✅ Xử lý text tiếng Việt có dấu
- ✅ Real-world data từ VnExpress

## 🐛 Troubleshooting

### Lỗi phổ biến:
1. **File input không tồn tại**: Chạy `crawler.py` và `text_cleaner.py` trước
2. **Permission denied**: `chmod +x run_hadoop_wordcount.sh`
3. **Hadoop not found**: Kiểm tra `HADOOP_HOME` và `PATH`
4. **requests/beautifulsoup4 not found**: `pip3 install requests beautifulsoup4`

### Logs:
- Hadoop: Check Hadoop logs tại `/opt/hadoop/logs/`
- YARN: Web UI tại `http://localhost:8088`

## 🗂️ Đường dẫn HDFS và Monitoring

### HDFS File System:
```
/user/ubuntu/wordcount/
├── input/
│   └── cleaned_article.txt       # Input data uploaded từ local
└── output/
    ├── _SUCCESS                  # Marker file báo job thành công
    └── part-00000               # Kết quả thực từ MapReduce
```

### Web UI Monitoring:
- **HDFS NameNode**: http://localhost:9870
  - Xem file system: Utilities → Browse the file system
  - Đường dẫn: `/user/ubuntu/wordcount/`
- **YARN ResourceManager**: http://localhost:8088
  - Theo dõi MapReduce jobs
  - Xem logs và metrics

### Cách Download Output từ Hadoop:
```bash
# Xem files trên HDFS
hdfs dfs -ls /user/ubuntu/wordcount/output

# Download kết quả về local
hdfs dfs -get /user/ubuntu/wordcount/output/part-00000 ./result.txt

# Hoặc xem trực tiếp trên HDFS
hdfs dfs -cat /user/ubuntu/wordcount/output/part-00000
```

## 📝 Ghi chú kỹ thuật

- Sử dụng plain text format cho input/output
- Data cleaning pipeline cho tiếng Việt có dấu
- Tokenization đơn giản: split by whitespace
- Hadoop Streaming API để chạy Python scripts
- Tự động upload input và download output
- Error handling cho text không hợp lệ



