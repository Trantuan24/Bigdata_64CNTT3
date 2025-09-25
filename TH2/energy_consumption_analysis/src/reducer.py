#!/usr/bin/env python3
"""
Energy Consumption Reducer
Output những năm có Average > 30 với format đẹp
"""

import sys

def main():
    """
    Main reducer function
    Nhận input từ mapper và format output
    """
    
    results = []
    
    try:
        # Đọc tất cả input từ mapper
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            try:
                # Parse key-value từ mapper: year\tavg
                year, avg = line.split('\t')
                year = int(year)
                avg = float(avg)
                
                results.append((year, avg))
                
            except ValueError as e:
                print(f"Reducer error parsing line: {line}", file=sys.stderr)
                continue
        
        # Sort kết quả theo năm
        results.sort(key=lambda x: x[0])
        
        # Output header
        print("Year\tAverage_Consumption")
        print("----\t-------------------")
        
        # Output từng năm
        for year, avg in results:
            print(f"{year}\t{avg}")
        
        # Thống kê tổng quan
        if results:
            print("\n" + "="*40)
            print("SUMMARY STATISTICS")
            print("="*40)
            print(f"Total years with Avg > 30: {len(results)}")
            print(f"Years: {', '.join(str(year) for year, _ in results)}")
            print(f"Highest consumption: {max(avg for _, avg in results)}")
            print(f"Lowest consumption (>30): {min(avg for _, avg in results)}")
            print(f"Average of filtered years: {sum(avg for _, avg in results) / len(results):.2f}")
        else:
            print("\nNo years found with Average > 30")
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Reducer fatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
