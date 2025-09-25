#!/usr/bin/env python3
"""
Mapper for Customer Spending Analysis
Xử lý JOIN logic giữa customer data và transaction data
"""

import sys

def process_customer_record(data):
    """Xử lý record khách hàng"""
    try:
        # Format: cust_id,first_name,last_name,age,profession
        parts = data.split(',')
        if len(parts) >= 5:
            cust_id = parts[0].strip()
            first_name = parts[1].strip()
            last_name = parts[2].strip()
            full_name = f"{first_name} {last_name}"
            
            # Emit: cust_id -> CUST:full_name
            print(f"{cust_id}\tCUST:{full_name}")
        
    except Exception as e:
        # Log error to stderr
        print(f"Error processing customer record: {data} - {e}", file=sys.stderr)

def process_transaction_record(data):
    """Xử lý record giao dịch"""
    try:
        # Format: trans_id,date,cust_id,amount,game_type,equipment,city,state,mode
        parts = data.split(',')
        if len(parts) >= 9:
            cust_id = parts[2].strip()
            amount = float(parts[3].strip())
            
            # Emit: cust_id -> TRANS:amount
            print(f"{cust_id}\tTRANS:{amount}")
        
    except Exception as e:
        # Log error to stderr
        print(f"Error processing transaction record: {data} - {e}", file=sys.stderr)

def main():
    """Main mapper function"""
    for line in sys.stdin:
        line = line.strip()
        
        if not line:
            continue
            
        try:
            # Phân biệt loại record dựa trên prefix
            if line.startswith("CUST:"):
                # Loại bỏ prefix và xử lý customer data
                customer_data = line[5:]  # Bỏ "CUST:"
                process_customer_record(customer_data)
                
            elif line.startswith("TRANS:"):
                # Loại bỏ prefix và xử lý transaction data
                transaction_data = line[6:]  # Bỏ "TRANS:"
                process_transaction_record(transaction_data)
            
            else:
                # Log unknown format
                print(f"Unknown record format: {line}", file=sys.stderr)
                
        except Exception as e:
            print(f"Error processing line: {line} - {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
