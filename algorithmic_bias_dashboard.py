#!/usr/bin/env python3
"""
YouTube Algorithmic Bias Dashboard
===================================
Interactive dashboard showing racial distribution, view count disparities,
and algorithmic patterns in YouTube search results and Shorts.

Features:
- Racial distribution across different search queries
- View count disparities by race/ethnicity
- Shorts vs. Search Results breakdown
- Heatmaps of algorithmic patterns
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import sys
import os
from datetime import datetime

class YouTubeAlgorithmicBiasDashboard:
    """Interactive dashboard for analyzing algorithmic bias in YouTube data"""

    def __init__(self, data_path):
        """Initialize dashboard with data"""
        self.data_path = data_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Load and prepare data"""
        try:
            print(f"Loading data from {self.data_path}...")
            self.df = pd.read_csv(self.data_path)
            print(f"Loaded {len(self.df)} rows")
            print(f"Columns: {', '.join(self.df.columns)}")

            # Clean column names
            self.df.columns = self.df.columns.str.strip()

            # Identify key columns (flexible column name matching)
            self.identify_columns()

            # Clean and prepare data
            self.prepare_data()

        except FileNotFoundError:
            print(f"Error: File '{self.data_path}' not found.")
            print("\nPlease export the Numbers file to CSV first.")
            print("Run: python convert_numbers_to_csv.py")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading data: {e}")
            sys.exit(1)

    def identify_columns(self):
        """Identify relevant columns from the dataset"""
        cols = [c.lower() for c in self.df.columns]

        # Common column name patterns
        self.race_col = None
        self.query_col = None
        self.views_col = None
        self.type_col = None

        # Find race/ethnicity column
        for pattern in ['race', 'ethnicity', 'demographic']:
            matches = [c for c in self.df.columns if pattern in c.lower()]
            if matches:
                self.race_col = matches[0]
                break

        # Find query column
        for pattern in ['query', 'search', 'keyword']:
            matches = [c for c in self.df.columns if pattern in c.lower()]
            if matches:
                self.query_col = matches[0]
                break

        # Find views column
        for pattern in ['view', 'count', 'views']:
            matches = [c for c in self.df.columns if pattern in c.lower()]
            if matches:
                self.views_col = matches[0]
                break

        # Find content type column (Shorts vs Regular)
        for pattern in ['type', 'format', 'short']:
            matches = [c for c in self.df.columns if pattern in c.lower()]
            if matches:
                self.type_col = matches[0]
                break

        print(f"\nIdentified columns:")
        print(f"  Race/Ethnicity: {self.race_col}")
        print(f"  Search Query: {self.query_col}")
        print(f"  View Count: {self.views_col}")
        print(f"  Content Type: {self.type_col}")

    def prepare_data(self):
        """Clean and prepare data for analysis"""
        # Convert views to numeric if needed
        if self.views_col and self.views_col in self.df.columns:
            self.df[self.views_col] = pd.to_numeric(
                self.df[self.views_col].astype(str).str.replace(',', '').str.replace('K', '000').str.replace('M', '000000'),
                errors='coerce'
            )

        # Fill NaN values
        self.df = self.df.fillna('Unknown')

        print(f"\nData prepared successfully")

    def create_racial_distribution_chart(self):
        """Create bar chart showing racial distribution across search queries"""
        if not self.race_col or not self.query_col:
            print("Warning: Missing race or query columns for racial distribution chart")
            return None

        # Group by query and race
        dist_data = self.df.groupby([self.query_col, self.race_col]).size().reset_index(name='count')

        fig = px.bar(
            dist_data,
            x=self.query_col,
            y='count',
            color=self.race_col,
            title='Racial Distribution Across Search Queries',
            labels={self.query_col: 'Search Query', 'count': 'Number of Videos'},
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(
            xaxis_tickangle=-45,
            height=500,
            hovermode='x unified',
            legend=dict(title='Race/Ethnicity')
        )

        return fig

    def create_view_count_disparity_chart(self):
        """Create box plot showing view count disparities by race/ethnicity"""
        if not self.race_col or not self.views_col:
            print("Warning: Missing race or views columns for disparity chart")
            return None

        # Filter out invalid view counts
        valid_data = self.df[self.df[self.views_col] > 0].copy()

        fig = go.Figure()

        races = valid_data[self.race_col].unique()
        colors = px.colors.qualitative.Set1

        for i, race in enumerate(races):
            race_data = valid_data[valid_data[self.race_col] == race][self.views_col]

            fig.add_trace(go.Box(
                y=race_data,
                name=race,
                marker_color=colors[i % len(colors)],
                boxmean='sd'
            ))

        fig.update_layout(
            title='View Count Disparities by Race/Ethnicity',
            yaxis_title='View Count',
            xaxis_title='Race/Ethnicity',
            height=500,
            showlegend=False
        )

        # Use log scale if there's high variance
        if valid_data[self.views_col].max() / valid_data[self.views_col].min() > 100:
            fig.update_yaxis(type='log', title='View Count (log scale)')

        return fig

    def create_shorts_vs_regular_breakdown(self):
        """Create pie and bar charts for Shorts vs Regular content breakdown"""
        if not self.type_col:
            print("Warning: Missing content type column")
            return None

        # Create subplot with pie chart and stacked bar
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Overall Distribution', 'By Race/Ethnicity'),
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],
            column_widths=[0.4, 0.6]
        )

        # Overall pie chart
        type_counts = self.df[self.type_col].value_counts()
        fig.add_trace(
            go.Pie(
                labels=type_counts.index,
                values=type_counts.values,
                marker=dict(colors=px.colors.qualitative.Pastel),
                textposition='inside',
                textinfo='label+percent'
            ),
            row=1, col=1
        )

        # Stacked bar by race
        if self.race_col:
            type_race_data = self.df.groupby([self.race_col, self.type_col]).size().unstack(fill_value=0)

            for content_type in type_race_data.columns:
                fig.add_trace(
                    go.Bar(
                        name=content_type,
                        x=type_race_data.index,
                        y=type_race_data[content_type],
                        text=type_race_data[content_type],
                        textposition='auto'
                    ),
                    row=1, col=2
                )

        fig.update_layout(
            title_text='Shorts vs. Search Results Breakdown',
            height=500,
            showlegend=True,
            barmode='stack'
        )

        fig.update_xaxes(title_text='Race/Ethnicity', row=1, col=2, tickangle=-45)
        fig.update_yaxes(title_text='Count', row=1, col=2)

        return fig

    def create_algorithmic_pattern_heatmap(self):
        """Create heatmap showing algorithmic patterns"""
        if not self.race_col or not self.query_col:
            print("Warning: Missing columns for heatmap")
            return None

        # Create pivot table for heatmap
        if self.views_col:
            heatmap_data = self.df.pivot_table(
                values=self.views_col,
                index=self.race_col,
                columns=self.query_col,
                aggfunc='mean'
            )
            title_suffix = '(Avg View Count)'
        else:
            heatmap_data = self.df.groupby([self.race_col, self.query_col]).size().unstack(fill_value=0)
            title_suffix = '(Video Count)'

        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdYlBu_r',
            text=heatmap_data.values,
            texttemplate='%{text:.0f}',
            textfont={"size": 10},
            colorbar=dict(title='Value')
        ))

        fig.update_layout(
            title=f'Algorithmic Pattern Heatmap {title_suffix}',
            xaxis_title='Search Query',
            yaxis_title='Race/Ethnicity',
            height=600,
            xaxis_tickangle=-45
        )

        return fig

    def create_position_bias_heatmap(self):
        """Create heatmap for position bias if position data exists"""
        position_cols = [c for c in self.df.columns if 'position' in c.lower() or 'rank' in c.lower()]

        if not position_cols or not self.race_col:
            return None

        position_col = position_cols[0]

        # Create position x race heatmap
        pos_race_data = self.df.groupby([self.race_col, position_col]).size().unstack(fill_value=0)

        fig = go.Figure(data=go.Heatmap(
            z=pos_race_data.values,
            x=pos_race_data.columns,
            y=pos_race_data.index,
            colorscale='Viridis',
            text=pos_race_data.values,
            texttemplate='%{text}',
            colorbar=dict(title='Count')
        ))

        fig.update_layout(
            title='Position Bias by Race/Ethnicity',
            xaxis_title='Search Result Position',
            yaxis_title='Race/Ethnicity',
            height=500
        )

        return fig

    def create_comprehensive_stats_table(self):
        """Create summary statistics table"""
        if not self.race_col:
            return None

        stats_list = []

        for race in self.df[self.race_col].unique():
            race_data = self.df[self.df[self.race_col] == race]

            stats = {
                'Race/Ethnicity': race,
                'Total Videos': len(race_data)
            }

            if self.views_col:
                stats['Avg Views'] = f"{race_data[self.views_col].mean():,.0f}"
                stats['Median Views'] = f"{race_data[self.views_col].median():,.0f}"
                stats['Total Views'] = f"{race_data[self.views_col].sum():,.0f}"

            if self.type_col:
                shorts_count = len(race_data[race_data[self.type_col].str.contains('Short', case=False, na=False)])
                stats['Shorts %'] = f"{(shorts_count / len(race_data) * 100):.1f}%"

            stats_list.append(stats)

        stats_df = pd.DataFrame(stats_list)

        fig = go.Figure(data=[go.Table(
            header=dict(
                values=list(stats_df.columns),
                fill_color='paleturquoise',
                align='left',
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=[stats_df[col] for col in stats_df.columns],
                fill_color='lavender',
                align='left',
                font=dict(size=11)
            )
        )])

        fig.update_layout(
            title='Summary Statistics by Race/Ethnicity',
            height=400
        )

        return fig

    def generate_dashboard(self, output_file='youtube_bias_dashboard.html'):
        """Generate complete interactive dashboard"""
        print("\nGenerating dashboard...")

        # Create all visualizations
        charts = []

        # 1. Racial Distribution
        fig1 = self.create_racial_distribution_chart()
        if fig1:
            charts.append(fig1)

        # 2. View Count Disparities
        fig2 = self.create_view_count_disparity_chart()
        if fig2:
            charts.append(fig2)

        # 3. Shorts vs Regular
        fig3 = self.create_shorts_vs_regular_breakdown()
        if fig3:
            charts.append(fig3)

        # 4. Algorithmic Pattern Heatmap
        fig4 = self.create_algorithmic_pattern_heatmap()
        if fig4:
            charts.append(fig4)

        # 5. Position Bias Heatmap
        fig5 = self.create_position_bias_heatmap()
        if fig5:
            charts.append(fig5)

        # 6. Stats Table
        fig6 = self.create_comprehensive_stats_table()
        if fig6:
            charts.append(fig6)

        if not charts:
            print("Error: Could not create any visualizations. Check your data format.")
            return

        # Combine all charts into one HTML file
        with open(output_file, 'w') as f:
            f.write(f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>YouTube Algorithmic Bias Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metadata {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metadata p {{
            margin: 5px 0;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>YouTube Algorithmic Bias Dashboard</h1>
        <p>Analysis of racial distribution, view count disparities, and algorithmic patterns</p>
    </div>

    <div class="metadata">
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Total Records:</strong> {len(self.df):,}</p>
        <p><strong>Data Source:</strong> {self.data_path}</p>
    </div>
''')

            for i, chart in enumerate(charts):
                f.write(f'    <div class="chart-container" id="chart{i}"></div>\n')

            f.write('    <script>\n')

            for i, chart in enumerate(charts):
                chart_json = chart.to_json()
                f.write(f'        Plotly.newPlot("chart{i}", {chart_json});\n')

            f.write('''
    </script>
</body>
</html>
''')

        print(f"\n✓ Dashboard created successfully: {output_file}")
        print(f"  Open the file in your browser to view the interactive dashboard")
        return output_file


def main():
    """Main function"""
    # Look for CSV files in current directory
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

    if not csv_files:
        print("Error: No CSV file found in current directory")
        print("\nPlease export the Numbers file to CSV format:")
        print("  1. Open 'Final YouTube Data Raw.numbers' in Apple Numbers")
        print("  2. File > Export To > CSV")
        print("  3. Save as 'youtube_data.csv' in this directory")
        print("\nOr run: python convert_numbers_to_csv.py for more options")
        sys.exit(1)

    # Use first CSV file found or specified file
    data_file = csv_files[0] if len(sys.argv) < 2 else sys.argv[1]

    print(f"Using data file: {data_file}")

    # Create dashboard
    dashboard = YouTubeAlgorithmicBiasDashboard(data_file)
    output_file = dashboard.generate_dashboard()

    print(f"\n{'='*60}")
    print("Dashboard generation complete!")
    print(f"{'='*60}")
    print(f"\nNext steps:")
    print(f"  1. Open {output_file} in your web browser")
    print(f"  2. Interact with the visualizations")
    print(f"  3. Export individual charts as needed (click camera icon)")
    print()


if __name__ == "__main__":
    main()
