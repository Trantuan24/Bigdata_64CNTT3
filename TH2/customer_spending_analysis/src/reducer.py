#!/usr/bin/env python3
"""
Reducer for Customer Spending Analysis
Tính tổng số tiền đã chi của mỗi khách hàng - Output CSV format
"""

import sys
import csv

def main():
    """Main reducer function"""
    current_cust_id = None
    customer_name = None
    total_spending = 0.0
    transaction_count = 0
    
    for line in sys.stdin:
        line = line.strip()
        
        if not line:
            continue
            
        try:
            # Parse key-value pair
            cust_id, value = line.split('\t', 1)
            
            # Nếu là customer mới, output kết quả của customer trước
            if current_cust_id and current_cust_id != cust_id:
                if customer_name:
                    # Output CSV format
                    print(f"{current_cust_id},{customer_name},{total_spending:.2f},{transaction_count}")
                
                # Reset cho customer mới
                customer_name = None
                total_spending = 0.0
                transaction_count = 0
            
            current_cust_id = cust_id
            
            # Xử lý value dựa trên type
            if value.startswith("CUST:"):
                # Lấy tên khách hàng
                customer_name = value[5:]  # Bỏ "CUST:"
                
            elif value.startswith("TRANS:"):
                # Cộng dồn amount
                try:
                    amount = float(value[6:])  # Bỏ "TRANS:"
                    total_spending += amount
                    transaction_count += 1
                except ValueError as e:
                    print(f"Error parsing amount: {value} - {e}", file=sys.stderr)
            
        except Exception as e:
            print(f"Error processing line: {line} - {e}", file=sys.stderr)
    
    # Output customer cuối cùng
    if current_cust_id and customer_name:
        print(f"{current_cust_id},{customer_name},{total_spending:.2f},{transaction_count}")

if __name__ == "__main__":
    main()
