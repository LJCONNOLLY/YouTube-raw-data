#!/bin/bash

# Quick Start Script for YouTube Algorithmic Bias Dashboard
# This script helps you get started with either dashboard option

echo "=========================================="
echo "YouTube Algorithmic Bias Dashboard"
echo "Quick Start Guide"
echo "=========================================="
echo ""

# Check for Python
if command -v python3 &> /dev/null; then
    echo "✓ Python3 found"
else
    echo "✗ Python3 not found. Please install Python 3.7 or higher"
    exit 1
fi

echo ""
echo "Choose your dashboard option:"
echo "1. Plotly Dashboard (Python - requires installation)"
echo "2. D3.js Dashboard (HTML - no installation needed)"
echo "3. Test with sample data first"
echo ""
read -p "Enter your choice (1, 2, or 3): " choice

case $choice in
    1)
        echo ""
        echo "Setting up Plotly Dashboard..."
        echo ""

        # Install dependencies
        echo "Installing dependencies..."
        pip3 install -r requirements.txt

        # Check for CSV files
        csv_files=$(find . -maxdepth 1 -name "*.csv" ! -name "sample_data.csv" | wc -l)

        if [ $csv_files -eq 0 ]; then
            echo ""
            echo "No CSV file found (other than sample_data.csv)"
            echo ""
            echo "Please export your Numbers file to CSV:"
            echo "  1. Open 'Final YouTube Data Raw.numbers' in Apple Numbers"
            echo "  2. File → Export To → CSV"
            echo "  3. Save as 'youtube_data.csv' in this directory"
            echo ""
            read -p "Press Enter to continue with sample data, or Ctrl+C to exit and convert your file first..."
            python3 algorithmic_bias_dashboard.py sample_data.csv
        else
            data_file=$(find . -maxdepth 1 -name "*.csv" ! -name "sample_data.csv" | head -1)
            echo ""
            echo "Found data file: $data_file"
            echo "Generating dashboard..."
            python3 algorithmic_bias_dashboard.py "$data_file"
        fi

        echo ""
        echo "Opening dashboard in browser..."
        if command -v open &> /dev/null; then
            open youtube_bias_dashboard.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open youtube_bias_dashboard.html
        else
            echo "Please manually open youtube_bias_dashboard.html in your browser"
        fi
        ;;

    2)
        echo ""
        echo "Opening D3.js Dashboard..."
        echo ""
        echo "The D3.js dashboard will open in your browser."
        echo "Click 'Choose CSV File' to upload your data."
        echo ""

        if command -v open &> /dev/null; then
            open d3_dashboard.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open d3_dashboard.html
        else
            echo "Please manually open d3_dashboard.html in your browser"
        fi
        ;;

    3)
        echo ""
        echo "Testing with sample data..."
        echo ""

        # Install dependencies
        echo "Installing dependencies..."
        pip3 install -r requirements.txt

        # Generate dashboard with sample data
        echo ""
        echo "Generating dashboard with sample data..."
        python3 algorithmic_bias_dashboard.py sample_data.csv

        echo ""
        echo "Opening dashboard in browser..."
        if command -v open &> /dev/null; then
            open youtube_bias_dashboard.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open youtube_bias_dashboard.html
        else
            echo "Please manually open youtube_bias_dashboard.html in your browser"
        fi

        echo ""
        echo "You can also try the D3.js version by opening d3_dashboard.html"
        echo "and uploading sample_data.csv through the web interface."
        ;;

    *)
        echo "Invalid choice. Please run the script again and choose 1, 2, or 3."
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Dashboard Ready!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  - Interact with the visualizations"
echo "  - Use filters to explore the data"
echo "  - Export charts or analysis as needed"
echo ""
echo "For more information, see README.md"
echo ""
