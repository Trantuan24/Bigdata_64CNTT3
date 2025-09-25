#!/usr/bin/env python3
"""
Data Generator for Customer Spending Analysis
Tạo dữ liệu mẫu dựa trên hình ảnh cung cấp
"""

import csv
import random
from datetime import datetime, timedelta

def generate_customer_data():
    """Tạo dữ liệu khách hàng dựa trên mẫu - Format CSV"""
    customers = [
        (4000001, "Kristina", "Chung", 55, "Pilot"),
        (4000002, "Paige", "Chen", 74, "Teacher"),
        (4000003, "Sherri", "Melton", 34, "Firefighter"),
        (4000004, "Gretchen", "Hill", 66, "Engineer"),
        (4000005, "John", "Smith", 45, "Doctor"),
        (4000006, "Mary", "Johnson", 38, "Lawyer"),
        (4000007, "David", "Brown", 52, "Manager"),
        (4000008, "Sarah", "Davis", 29, "Designer"),
        (4000009, "Michael", "Wilson", 41, "Analyst"),
        (4000010, "Lisa", "Garcia", 33, "Nurse")
    ]
    
    # Tạo file CSV với header đẹp
    with open('../data/cust_details.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Cust_ID', 'First_Name', 'Last_Name', 'Age', 'Profession'])
        for customer in customers:
            writer.writerow(customer)
    
    print(f"✅ Đã tạo {len(customers)} khách hàng trong cust_details.csv")
    return customers

def generate_transaction_data(customers):
    """Tạo dữ liệu giao dịch dựa trên mẫu"""
    game_types = ["Exercise & Fitness", "Gymnastics", "Team Sports", "Outdoor Recreation", "Puzzles"]
    equipments = [
        "Cardio Machine Accessories", "Weightlifting Gloves", "Weightlifting Machine Accessories",
        "Gymnastics Rings", "Field Hockey", "Camping & Backpacking & Hiking", "Jigsaw Puzzles"
    ]
    cities = ["Clarksville", "Long Beach", "Anaheim", "Milwaukee", "Nashville", "Chicago", "Charleston"]
    states = ["Tennessee", "California", "Wisconsin", "Illinois", "South Carolina"]
    
    transactions = []
    trans_id = 1
    
    # Tạo giao dịch cho mỗi khách hàng
    for cust_id, _, _, _, _ in customers:
        # Mỗi khách hàng có 2-5 giao dịch ngẫu nhiên
        num_transactions = random.randint(2, 5)
        
        for _ in range(num_transactions):
            date = (datetime(2011, 1, 1) + timedelta(days=random.randint(0, 364))).strftime('%m-%d-%Y')
            amount = round(random.uniform(5.00, 300.00), 2)
            game_type = random.choice(game_types)
            equipment = random.choice(equipments)
            city = random.choice(cities)
            state = random.choice(states)
            
            transactions.append([
                f"{trans_id:07d}",  # Trans_ID với format 7 chữ số
                date,
                cust_id,
                amount,
                game_type,
                equipment,
                city,
                state,
                "credit"
            ])
            trans_id += 1
    
    # Tạo file CSV với header đẹp
    with open('../data/transaction_details.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Trans_ID', 'Date', 'Cust_ID', 'Amount', 'Game_Type', 'Equipment', 'City', 'State', 'Mode'])
        for transaction in transactions:
            writer.writerow(transaction)
    
    print(f"✅ Đã tạo {len(transactions)} giao dịch trong transaction_details.csv")
    return transactions

def create_combined_input():
    """Tạo file input kết hợp cho MapReduce với prefix phân biệt"""
    combined_data = []
    
    # Đọc customer data từ CSV và thêm prefix CUST:
    with open('../data/cust_details.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            # Format: CUST:cust_id,first_name,last_name,age,profession
            combined_data.append(f"CUST:{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}")
    
    # Đọc transaction data từ CSV và thêm prefix TRANS:
    with open('../data/transaction_details.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            # Format: TRANS:trans_id,date,cust_id,amount,game_type,equipment,city,state,mode
            combined_data.append(f"TRANS:{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]},{row[8]}")
    
    # Shuffle dữ liệu để mô phỏng thực tế
    random.shuffle(combined_data)
    
    with open('../data/input_combined.txt', 'w', encoding='utf-8') as f:
        for line in combined_data:
            f.write(line + '\n')
    
    print(f"✅ Đã tạo file input_combined.txt với {len(combined_data)} records")

def main():
    print("🚀 Bắt đầu tạo dữ liệu cho Customer Spending Analysis...")
    
    # Tạo dữ liệu khách hàng
    customers = generate_customer_data()
    
    # Tạo dữ liệu giao dịch
    transactions = generate_transaction_data(customers)
    
    # Tạo file input kết hợp cho MapReduce
    create_combined_input()
    
    print("\n📊 Thống kê dữ liệu:")
    print(f"- Số khách hàng: {len(customers)}")
    print(f"- Số giao dịch: {len(transactions)}")
    print(f"- Tổng số records: {len(customers) + len(transactions)}")
    
    print("\n✅ Hoàn thành tạo dữ liệu!")

if __name__ == "__main__":
    main()
