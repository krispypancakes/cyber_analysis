import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache_data
def load_data():
    xls_path = 'data/cve_final_daily_auto_day0_2024_11_15.xlsx'
    xls = pd.ExcelFile(xls_path)
    df = pd.read_excel(xls, sheet_name='Sheet1')
    return df

# Function to filter data by company and time range
def filter_data(df, company=None, start_date=None, end_date=None):
    if company:
        df = df[df['vendorProject'] == company]
    if start_date and end_date:
        df = df[(pd.to_datetime(df['published']) >= pd.to_datetime(start_date)) & (pd.to_datetime(df['published']) <= pd.to_datetime(end_date))]
    return df

# Load the dataset
df = load_data()

# Title
st.title("Cyber Vulnerability Trends Dashboard")

# Sidebar filters
company_list = df['vendorProject'].unique().tolist()
selected_company = st.sidebar.selectbox('Select Company', ['All'] + company_list)

start_date = st.sidebar.date_input('Start Date', min_value=pd.to_datetime(df['published'].min()), max_value=pd.to_datetime(df['published'].max()) - pd.Timedelta(days=1))
end_date = st.sidebar.date_input('End Date', max_value=pd.to_datetime(df['published'].max()), min_value=pd.to_datetime(df['published']).min())

# Filtering data
if selected_company != 'All':
    filtered_df = filter_data(df, company=selected_company, start_date=start_date, end_date=end_date)
else:
    filtered_df = filter_data(df, start_date=start_date, end_date=end_date)

# Frequency of attacks
st.subheader("Frequency of Attacks on Specific Company")
attack_counts = filtered_df['vendorProject'].value_counts().sort_values(ascending=False)
if selected_company != 'All':
    st.write(f"Number of attacks on {selected_company}: {attack_counts[selected_company]}")
else:
    st.bar_chart(attack_counts)

# Common Attacks
st.subheader("Most Common Attacks")
common_attacks = filtered_df['vulnerabilityName'].value_counts().head(10)
st.bar_chart(common_attacks)

# Impact of Attacks
st.subheader("Impact Analysis")
impact_scores = filtered_df.groupby('vulnerabilityName')['metrics_baseScore'].mean().sort_values(ascending=False).head(10)
st.write("Top 10 vulnerabilities by impact:")
st.bar_chart(impact_scores)

# Complexity and Severity Trends
st.subheader("Attack Severity and Complexity Over Time")
df['published'] = pd.to_datetime(df['published'])
df['year_month'] = df['published'].dt.to_period('M')
severity_trend = df.groupby('year_month')['metrics_baseScore'].mean()
st.line_chart(severity_trend)

# Correlation Analysis for Attack Impact, Complexity, and Severity
st.subheader("Correlation Analysis")
sns.heatmap(df[['metrics_baseScore', 'metrics_exploitabilityScore', 'metrics_impactScore']].corr(), annot=True, cmap='viridis')
st.pyplot(plt.gcf())

# Additional Analyses and Ideas for Future Research
st.subheader("Further Research Possibilities")
st.write("- Perform predictive analysis to estimate future trends in severity and complexity.")
st.write("- Investigate correlations between exploitability and attack frequency.")
st.write("- Compare attack types for specific companies over time to identify trends.")
