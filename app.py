import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Credit Rating Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upgrade {
        color: #28a745;
        font-weight: bold;
    }
    .downgrade {
        color: #dc3545;
        font-weight: bold;
    }
    .stable {
        color: #6c757d;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_sample_data():
    """Generate realistic sample data for credit rating changes"""
    
    companies = [
        "Tata Steel Ltd", "Adani Ports & SEZ", "JSW Steel Ltd", "Vedanta Ltd",
        "Hindalco Industries", "UltraTech Cement", "Godrej Properties",
        "L&T Finance Holdings", "Shriram Transport", "Mahindra Finance",
        "NBCC India Ltd", "Jaiprakash Associates", "Reliance Industries",
        "ONGC Ltd", "Coal India Ltd", "Power Finance Corp", "REC Ltd",
        "Indian Railway Finance", "HUDCO Ltd", "LIC Housing Finance",
        "Bajaj Finance Ltd", "HDFC Ltd", "ICICI Bank Ltd", "Axis Bank Ltd"
    ]
    
    agencies = ["CRISIL", "CARE", "India Ratings", "ICRA", "Brickwork"]
    
    # Define rating scales and investment grade boundaries
    rating_scale = {
        "CRISIL": ["D", "C", "CC", "CCC", "B-", "B", "B+", "BB-", "BB", "BB+", "BBB-", "BBB", "BBB+", "A-", "A", "A+", "AA-", "AA", "AA+", "AAA"],
        "CARE": ["D", "C", "CC", "CCC", "B-", "B", "B+", "BB-", "BB", "BB+", "BBB-", "BBB", "BBB+", "A-", "A", "A+", "AA-", "AA", "AA+", "AAA"],
        "India Ratings": ["D", "C", "CC", "CCC", "B-", "B", "B+", "BB-", "BB", "BB+", "BBB-", "BBB", "BBB+", "A-", "A", "A+", "AA-", "AA", "AA+", "AAA"],
        "ICRA": ["D", "C", "CC", "CCC", "[ICRA]B-", "[ICRA]B", "[ICRA]B+", "[ICRA]BB-", "[ICRA]BB", "[ICRA]BB+", "[ICRA]BBB-", "[ICRA]BBB", "[ICRA]BBB+", "[ICRA]A-", "[ICRA]A", "[ICRA]A+", "[ICRA]AA-", "[ICRA]AA", "[ICRA]AA+", "[ICRA]AAA"],
        "Brickwork": ["BWR D", "BWR C", "BWR CC", "BWR CCC", "BWR B-", "BWR B", "BWR B+", "BWR BB-", "BWR BB", "BWR BB+", "BWR BBB-", "BWR BBB", "BWR BBB+", "BWR A-", "BWR A", "BWR A+", "BWR AA-", "BWR AA", "BWR AA+", "BWR AAA"]
    }
    
    # Generate sample data
    data = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(150):  # Generate 150 sample records
        company = np.random.choice(companies)
        agency = np.random.choice(agencies)
        scale = rating_scale[agency]
        
        # Focus on B, BB, BBB levels (indices 4-12 in most scales)
        if agency == "ICRA":
            target_indices = list(range(4, 13))  # B- to BBB+
        else:
            target_indices = list(range(4, 13))  # B- to BBB+
            
        old_rating_idx = np.random.choice(target_indices)
        
        # Determine if upgrade or downgrade
        change_type = np.random.choice(["Upgrade", "Downgrade", "Stable"], p=[0.4, 0.4, 0.2])
        
        if change_type == "Upgrade" and old_rating_idx < len(scale) - 1:
            new_rating_idx = min(old_rating_idx + np.random.randint(1, 3), len(scale) - 1)
        elif change_type == "Downgrade" and old_rating_idx > 0:
            new_rating_idx = max(old_rating_idx - np.random.randint(1, 3), 0)
        else:
            new_rating_idx = old_rating_idx
            change_type = "Stable"
        
        old_rating = scale[old_rating_idx]
        new_rating = scale[new_rating_idx]
        
        # Generate date within last 30 days
        date = base_date + timedelta(days=np.random.randint(0, 30))
        
        # Add outlook
        outlook = np.random.choice(["Stable", "Positive", "Negative", "Watch"], p=[0.5, 0.2, 0.2, 0.1])
        
        data.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Company": company,
            "Agency": agency,
            "Old_Rating": old_rating,
            "New_Rating": new_rating,
            "Change_Type": change_type,
            "Outlook": outlook,
            "Sector": np.random.choice(["Banking", "Steel", "Cement", "Power", "Infrastructure", "NBFC", "Oil & Gas", "Real Estate"]),
            "Rating_Change_Notches": new_rating_idx - old_rating_idx
        })
    
    return pd.DataFrame(data)

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Credit Rating Monitor</h1>', unsafe_allow_html=True)
    st.markdown("### Monitor credit rating changes near investment grade levels (B, BB, BBB)")
    
    # Load data
    df = generate_sample_data()
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(df['Date'].min().date(), df['Date'].max().date()),
        min_value=df['Date'].min().date(),
        max_value=df['Date'].max().date()
    )
    
    # Agency filter
    agencies = st.sidebar.multiselect(
        "Select Rating Agencies",
        options=df['Agency'].unique(),
        default=df['Agency'].unique()
    )
    
    # Change type filter
    change_types = st.sidebar.multiselect(
        "Select Change Types",
        options=df['Change_Type'].unique(),
        default=["Upgrade", "Downgrade"]
    )
    
    # Sector filter
    sectors = st.sidebar.multiselect(
        "Select Sectors",
        options=df['Sector'].unique(),
        default=df['Sector'].unique()
    )
    
    # Apply filters
    if len(date_range) == 2:
        df_filtered = df[
            (df['Date'].dt.date >= date_range[0]) &
            (df['Date'].dt.date <= date_range[1]) &
            (df['Agency'].isin(agencies)) &
            (df['Change_Type'].isin(change_types)) &
            (df['Sector'].isin(sectors))
        ]
    else:
        df_filtered = df[
            (df['Agency'].isin(agencies)) &
            (df['Change_Type'].isin(change_types)) &
            (df['Sector'].isin(sectors))
        ]
    
    # Main dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_changes = len(df_filtered)
        st.metric("Total Changes", total_changes)
    
    with col2:
        upgrades = len(df_filtered[df_filtered['Change_Type'] == 'Upgrade'])
        st.metric("Upgrades", upgrades, delta=f"+{upgrades}")
    
    with col3:
        downgrades = len(df_filtered[df_filtered['Change_Type'] == 'Downgrade'])
        st.metric("Downgrades", downgrades, delta=f"-{downgrades}")
    
    with col4:
        stable = len(df_filtered[df_filtered['Change_Type'] == 'Stable'])
        st.metric("Stable", stable)
    
    # Charts section
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Rating Changes by Agency")
        if not df_filtered.empty:
            agency_counts = df_filtered['Agency'].value_counts()
            fig_agency = px.bar(
                x=agency_counts.index,
                y=agency_counts.values,
                labels={'x': 'Rating Agency', 'y': 'Number of Changes'},
                color=agency_counts.values,
                color_continuous_scale='viridis'
            )
            fig_agency.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_agency, use_container_width=True)
    
    with col2:
        st.subheader("🔄 Change Types Distribution")
        if not df_filtered.empty:
            change_counts = df_filtered['Change_Type'].value_counts()
            colors = {'Upgrade': '#28a745', 'Downgrade': '#dc3545', 'Stable': '#6c757d'}
            fig_changes = px.pie(
                values=change_counts.values,
                names=change_counts.index,
                color=change_counts.index,
                color_discrete_map=colors
            )
            fig_changes.update_layout(height=400)
            st.plotly_chart(fig_changes, use_container_width=True)
    
    # Timeline chart
    st.subheader("📅 Rating Changes Timeline")
    if not df_filtered.empty:
        timeline_data = df_filtered.groupby(['Date', 'Change_Type']).size().reset_index(name='Count')
        fig_timeline = px.line(
            timeline_data,
            x='Date',
            y='Count',
            color='Change_Type',
            color_discrete_map={'Upgrade': '#28a745', 'Downgrade': '#dc3545', 'Stable': '#6c757d'}
        )
        fig_timeline.update_layout(height=400)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Detailed table
    st.markdown("---")
    st.subheader("📋 Detailed Rating Changes")
    
    if not df_filtered.empty:
        # Add styling to the dataframe
        def style_change_type(val):
            if val == 'Upgrade':
                return 'color: #28a745; font-weight: bold'
            elif val == 'Downgrade':
                return 'color: #dc3545; font-weight: bold'
            else:
                return 'color: #6c757d; font-weight: bold'
        
        # Display table with formatting
        display_df = df_filtered.copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        display_df = display_df.sort_values('Date', ascending=False)
        
        st.dataframe(
            display_df.style.applymap(style_change_type, subset=['Change_Type']),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"rating_changes_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No data matches the selected filters. Please adjust your filter criteria.")
    
    # Information section
    st.markdown("---")
    st.subheader("ℹ️ About This Demo")
    
    st.info("""
    **This is a demo application** showing how a credit rating monitoring system would work.
    
    **Key Features:**
    - Monitors rating changes in B, BB, BBB levels (near investment grade)
    - Tracks upgrades, downgrades, and stable ratings
    - Covers major Indian rating agencies (CRISIL, CARE, India Ratings, ICRA, Brickwork)
    - Provides filtering by date, agency, change type, and sector
    - Interactive visualizations and downloadable data
    
    **Investment Grade Levels:**
    - **BBB and above**: Investment Grade
    - **BB and below**: Non-Investment Grade (High Yield)
    - **Focus Area**: B, BB, BBB levels where companies transition between investment and non-investment grade
    
    **Next Steps for Production:**
    1. Integrate with real rating agency data sources
    2. Set up automated data collection
    3. Add email/SMS alerts for specific rating changes
    4. Include more detailed company fundamentals
    5. Add historical rating trend analysis
    """)

if __name__ == "__main__":
    main()
