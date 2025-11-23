# YouTube Algorithmic Bias Dashboard

Interactive dashboards for analyzing racial distribution, view count disparities, and algorithmic patterns in YouTube search results and Shorts.

## Features

### Visualizations

1. **Racial Distribution Across Search Queries**
   - Bar charts showing distribution of content by race/ethnicity for each search query
   - Identifies which demographics are represented in search results

2. **View Count Disparities by Race/Ethnicity**
   - Box plots and bar charts comparing average view counts across different racial groups
   - Reveals potential algorithmic amplification or suppression patterns

3. **Shorts vs. Search Results Breakdown**
   - Pie charts and stacked bars comparing Shorts content to regular videos
   - Shows breakdown by race/ethnicity

4. **Algorithmic Pattern Heatmaps**
   - Heat maps revealing patterns in how YouTube's algorithm surfaces content
   - Cross-references search queries with race/ethnicity and view counts

5. **Summary Statistics**
   - Comprehensive tables and cards showing key metrics
   - Exportable data for further analysis

## Two Dashboard Options

### Option 1: Plotly Dashboard (Python)
**File:** `algorithmic_bias_dashboard.py`

**Pros:**
- Rich, interactive visualizations
- Statistical analysis built-in
- Easy to customize and extend
- Server-side processing for large datasets

**Installation:**
```bash
pip install -r requirements.txt
```

**Usage:**
```bash
# First, export your Numbers file to CSV
# Then run:
python algorithmic_bias_dashboard.py youtube_data.csv
```

This will generate `youtube_bias_dashboard.html` that you can open in your browser.

### Option 2: D3.js Dashboard (Pure HTML/JavaScript)
**File:** `d3_dashboard.html`

**Pros:**
- No installation required
- Works entirely in the browser
- Highly interactive and customizable
- Client-side processing (no server needed)

**Usage:**
1. Open `d3_dashboard.html` in your web browser
2. Click "Choose CSV File" and upload your YouTube data
3. Interact with the visualizations and filters

## Data Preparation

Your YouTube data is currently in Apple Numbers format (`Final YouTube Data Raw.numbers`).

### Converting to CSV

**Option A: Using Apple Numbers**
1. Open `Final YouTube Data Raw.numbers` in Apple Numbers
2. Go to File → Export To → CSV
3. Save as `youtube_data.csv` in this directory

**Option B: Online Converter**
1. Visit https://cloudconvert.com/numbers-to-csv
2. Upload your Numbers file
3. Download the CSV and save it in this directory

**Option C: Check for existing CSV**
```bash
python convert_numbers_to_csv.py
```

### Expected Data Format

The dashboards automatically detect column names, but work best with:

| Column Name (flexible) | Description |
|------------------------|-------------|
| Race/Ethnicity/Demographic | Racial or ethnic category |
| Query/Search/Keyword | Search term used |
| Views/View Count | Number of views |
| Type/Format/Short | Content type (Shorts vs Regular) |
| Position/Rank (optional) | Search result position |

**Example CSV:**
```csv
Race,Search Query,View Count,Content Type
Asian,makeup tutorial,1500000,Regular
Black,makeup tutorial,2300000,Shorts
Hispanic,cooking,890000,Regular
White,cooking,1200000,Shorts
```

## Running the Dashboards

### Plotly Dashboard

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run the dashboard generator
python algorithmic_bias_dashboard.py youtube_data.csv

# Open the generated file
open youtube_bias_dashboard.html  # macOS
xdg-open youtube_bias_dashboard.html  # Linux
start youtube_bias_dashboard.html  # Windows
```

### D3.js Dashboard

Simply open `d3_dashboard.html` in any modern web browser and upload your CSV file.

## Dashboard Features

### Interactive Controls

**Filters:**
- Filter by race/ethnicity
- Filter by search query
- Reset filters
- Export analysis

**Tooltips:**
- Hover over any chart element for detailed information
- View exact counts, percentages, and statistics

**Export:**
- Download individual charts as PNG images (Plotly)
- Export summary statistics as text file (D3.js)

## Analysis Insights

The dashboards help identify:

1. **Representation Gaps:** Which racial/ethnic groups are over or underrepresented in search results
2. **View Count Disparities:** Whether certain groups consistently get more or fewer views
3. **Content Type Bias:** If Shorts favor certain demographics over regular videos
4. **Search Query Patterns:** How different searches surface different racial distributions
5. **Position Bias:** Whether certain groups appear higher or lower in search results

## Customization

### Modifying the Plotly Dashboard

Edit `algorithmic_bias_dashboard.py`:

```python
# Change color schemes
color_discrete_sequence=px.colors.qualitative.Set3

# Adjust chart sizes
height=600  # Default is 500

# Add new visualizations
def create_custom_chart(self):
    # Your custom chart code
    pass
```

### Modifying the D3.js Dashboard

Edit `d3_dashboard.html`:

```javascript
// Change color schemes
const colorScheme = d3.schemeSet3;

// Modify chart dimensions
const height = 500;

// Add custom interactions
.on('click', function(event, d) {
    // Your custom code
});
```

## Troubleshooting

### Numbers file won't convert
- Ensure you have the latest version of Numbers
- Try the online converter option
- Check file permissions

### No data appears in dashboard
- Verify CSV format matches expected structure
- Check for column name variations
- Look at browser console for errors (F12)

### Plotly charts not rendering
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Try updating packages: `pip install --upgrade plotly pandas`

### D3.js dashboard blank
- Make sure JavaScript is enabled in your browser
- Check browser console for errors (F12)
- Try a different browser (Chrome, Firefox, Safari)

## Contributing

To add new visualizations or features:

1. Fork/clone this repository
2. Add your visualization function
3. Update the `generate_dashboard()` method to include it
4. Test with sample data
5. Submit a pull request

## Data Privacy

All analysis is performed locally:
- **Plotly version:** Data processed in Python, output to local HTML file
- **D3.js version:** All processing happens in your browser, no data sent to servers

## License

This dashboard is provided as-is for research and analysis purposes.

## References

- [Plotly Python Documentation](https://plotly.com/python/)
- [D3.js Documentation](https://d3js.org/)
- [YouTube Data API](https://developers.google.com/youtube/v3)

---

**Need help?** Check the troubleshooting section or open an issue in the repository.
