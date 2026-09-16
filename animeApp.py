# ============================================
# 🎌 Anime Feature Extraction App
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from dateutil.relativedelta import relativedelta
from datetime import datetime

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Anime Feature Extraction",
    page_icon="🎌",
    layout="wide"
)

st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #7C3AED, #EC4899); border-radius: 15px; color: white; margin-bottom: 30px;'>
    <h1>🎌 Anime Feature Extraction</h1>
    <p>Extract Episodes, Time Periods & Duration from Titles</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# FUNCTIONS
# ============================================
def extract_episodes(txt):
    check = False
    data = ''
    
    for i in txt:
        if i == ')':
            break
        if check == True:
            data += i
        if i == '(':
            check = True
    return data

def extraction_time(txt):
    check = False
    data = ""
    
    for i in range(len(txt)):
        if txt[i] == ')':
            for j in range(i+1, i+20):
                data += txt[j]
            return data
    return ""

def calculate_total_months(period):
    try:
        start_str, end_str = period.split(' - ')
        start_date = datetime.strptime(start_str.strip(), '%b %Y')
        end_date = datetime.strptime(end_str.strip(), '%b %Y')
        r = relativedelta(end_date, start_date)
        total_months = r.years * 12 + r.months + 1
        return total_months
    except:
        return None

# ============================================
# LOAD & PROCESS DATA
# ============================================
@st.cache_data
def load_and_process():
    df = pd.read_csv('FeatureExtractionAnime.csv')
    
    # Extract Episodes
    df["Episodes"] = df["Title"].apply(extract_episodes)
    df['Episodes'] = df['Episodes'].str.replace(" eps", "", regex=False)
    df["Episodes"] = pd.to_numeric(df["Episodes"], errors='coerce').fillna(0).astype(int)
    
    # Extract Time Period
    df['Total Time'] = df['Title'].apply(extraction_time)
    
    # Calculate Months
    df['Months'] = df['Total Time'].apply(calculate_total_months)
    
    return df

df = load_and_process()

# ============================================
# TABS
# ============================================
tab1, tab2, tab3 = st.tabs(["📋 Data", "📊 Analysis", "🔍 Search"])

# ============================================
# TAB 1: DATA
# ============================================
with tab1:
    st.subheader("📋 Processed Data")
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Anime", df.shape[0])
    with col2:
        st.metric("Total Episodes", df['Episodes'].sum())
    with col3:
        st.metric("Avg Duration (Months)", f"{df['Months'].mean():.1f}")

# ============================================
# TAB 2: ANALYSIS
# ============================================
with tab2:
    st.subheader("📊 Episodes Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df['Episodes'], bins=30, kde=True, ax=ax, color='#7C3AED')
        ax.set_title('Episode Count Distribution')
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df['Months'].dropna(), bins=30, kde=True, ax=ax, color='#EC4899')
        ax.set_title('Duration (Months) Distribution')
        st.pyplot(fig)
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🏆 Top 10 Longest Running Anime")
        top_long = df.nlargest(10, 'Episodes')[['Title', 'Episodes']]
        st.dataframe(top_long, use_container_width=True)
    
    with col4:
        st.subheader("⏱️ Top 10 by Duration")
        top_duration = df.nlargest(10, 'Months')[['Title', 'Months']]
        st.dataframe(top_duration, use_container_width=True)

# ============================================
# TAB 3: SEARCH
# ============================================
with tab3:
    st.subheader("🔍 Search Anime")
    
    search_term = st.text_input("Type anime name...")
    
    if search_term:
        results = df[df['Title'].str.contains(search_term, case=False, na=False)]
        st.dataframe(results, use_container_width=True)
    else:
        st.info("Type to search an anime!")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    Built with ❤️ | Feature Extraction Project | © 2026 Suryansh Singh
</div>
""", unsafe_allow_html=True)