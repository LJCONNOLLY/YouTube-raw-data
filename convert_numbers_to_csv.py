#!/usr/bin/env python3
"""
Convert Apple Numbers file to CSV
This script helps extract data from the Numbers file for analysis.

Since Numbers is a proprietary format, you have two options:
1. Export the Numbers file to CSV manually in Apple Numbers (File > Export > CSV)
2. Use an online converter or other tool

Place the resulting CSV file in this directory as 'youtube_data.csv'
"""

import os
import sys

def check_for_csv():
    """Check if CSV file exists"""
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if csv_files:
        print(f"Found CSV files: {', '.join(csv_files)}")
        return csv_files[0]
    else:
        print("No CSV file found.")
        print("\nPlease export 'Final YouTube Data Raw.numbers' to CSV format:")
        print("1. Open the file in Apple Numbers")
        print("2. Go to File > Export To > CSV")
        print("3. Save as 'youtube_data.csv' in this directory")
        print("\nOr use an online converter at: https://cloudconvert.com/numbers-to-csv")
        return None

if __name__ == "__main__":
    csv_file = check_for_csv()
    if csv_file:
        print(f"\nGreat! You can now use '{csv_file}' with the dashboard.")
        print("Run: python algorithmic_bias_dashboard.py")
    else:
        sys.exit(1)
