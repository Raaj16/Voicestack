import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time

# Set page config first
st.set_page_config(
    page_title="Dental Call Analytics", 
    layout="wide",
    page_icon="📞",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with animations
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        animation: fadeIn 1s ease-in;
    }
    .section-header {
        font-size: 1.4rem;
        color: #2c3e50;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3498db;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .chart-container {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #e1e8ed;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        animation: fadeIn 0.8s ease-out;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: pulse 2s infinite;
    }
    .front-desk-impact {
        background-color: #f8fff8;
        border-left: 4px solid #27ae60;
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        font-size: 0.9em;
    }
    .business-impact {
        background-color: #f0f8ff;
        border-left: 4px solid #2980b9;
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        font-size: 0.9em;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes fadeInUp {
        from { 
            opacity: 0;
            transform: translateY(20px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    @keyframes slideIn {
        from { 
            opacity: 0;
            transform: translateX(-20px);
        }
        to { 
            opacity: 1;
            transform: translateX(0);
        }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Progress bar for loading */
    .stProgress > div > div > div > div {
        background-color: #3498db;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# ------------------- Data Load -------------------
@st.cache_data
def load_data():
    try:
        # Show loading progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Loading data...")
        progress_bar.progress(30)
        
        sheet_url = "https://docs.google.com/spreadsheets/d/1Syrq5xPz9VZ6iBJ79TMtFGvT3w7ZGP4GpgbbQZv11Dk/export?format=csv"
        df = pd.read_csv(sheet_url)
        
        progress_bar.progress(60)
        status_text.text("Processing data...")
        
        # Clean column names
        df.columns = df.columns.str.strip().str.replace(" ", "_")
        
        # Convert Call_Time to datetime
        df["Call_Time"] = pd.to_datetime(df["Call_Time"], errors="coerce")
        
        # Create date features
        df["Date"] = df["Call_Time"].dt.date
        df["Hour"] = df["Call_Time"].dt.hour
        df["Day_Of_Week"] = df["Call_Time"].dt.day_name()
        
        # Fill missing values
        df.fillna("", inplace=True)
        
        # Convert duration columns to numeric
        duration_cols = ['Ring_Duration', 'Conversation_Duration', 'Voicemail_Duration', 'Total_Duration']
        for col in duration_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        progress_bar.progress(100)
        status_text.text("✅ Data loaded successfully!")
        time.sleep(0.5)  # Brief pause to show completion
        progress_bar.empty()
        status_text.empty()
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

# ------------------- Enhanced Classification -------------------
def classify_call(transcript, call_status):
    try:
        t = str(transcript).lower()
        status = str(call_status).lower()
        
        if "missed" in status:
            return "Missed Call"
        elif any(w in t for w in ["book", "appointment", "schedule", "availability"]):
            return "Appointment Booking"
        elif any(w in t for w in ["cancel", "reschedule", "postpone"]):
            return "Cancellation/Reschedule"
        elif any(w in t for w in ["insurance", "coverage", "benefit"]):
            return "Insurance Inquiry"
        elif any(w in t for w in ["bill", "payment", "price", "fee", "charge"]):
            return "Billing/Payment"
        elif any(w in t for w in ["pain", "tooth", "emergency", "hurt", "swelling", "broken"]):
            return "Emergency/Clinical"
        elif any(w in t for w in ["follow up", "check up", "cleaning", "exam"]):
            return "Follow-up/Routine Care"
        elif any(w in t for w in ["prescription", "medicine", "medication"]):
            return "Prescription Related"
        else:
            return "General Inquiry"
    except:
        return "General Inquiry"

# ------------------- Load Data -------------------
df = load_data()

if not df.empty:
    with st.spinner("🔄 Analyzing call patterns..."):
        df["Category"] = df.apply(lambda x: classify_call(x.get('transcript', ''), x.get('Call_Status', '')), axis=1)

# ------------------- Title -------------------
st.markdown('<h1 class="main-header">🦷 Dental Call Analytics</h1>', unsafe_allow_html=True)
st.markdown("### AI-Powered Insights for Practice Growth")

# ------------------- Quick Stats Overview -------------------
if not df.empty:
    total_calls = len(df)
    st.markdown(f"""
    <div class="insight-box">
        <h4 style='margin:0; color:white;'>📊 Quick Overview</h4>
        <p style='margin:5px 0; color:white; font-size:1.1em;'>
            Analyzing <strong>{total_calls:,} calls</strong> with AI-powered insights to help <strong>CareStack</strong> enhance 
            patient experience, scheduling efficiency, and front-desk performance.
        </p>
        <p style='margin:8px 0 0 0; color:#f0f0f0; font-size:0.95em;'>
            CareStack (<a href='https://carestack.com/en-GB' target='_blank' style='color:#fcd34d; text-decoration:none;'>carestack.com</a>) 
            provides an all-in-one cloud-based dental practice management platform used by modern dental practices globally.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ------------------- Sidebar Filters -------------------
st.sidebar.markdown("### 🎛️ Dashboard Controls")

filtered_df = df.copy()

if not df.empty:
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    st.sidebar.markdown("**📅 Date Range**")
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )

    st.sidebar.markdown("**📞 Call Direction**")
    call_direction = st.sidebar.multiselect(
        "Select call directions",
        options=df['Call_Direction'].unique(),
        default=df['Call_Direction'].unique(),
        label_visibility="collapsed"
    )

    st.sidebar.markdown("**🏷️ Call Categories**")
    call_categories = st.sidebar.multiselect(
        "Filter by category",
        options=df['Category'].unique(),
        default=df['Category'].unique(),
        label_visibility="collapsed"
    )

    # Apply filters
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['Date'] >= date_range[0]) & 
            (filtered_df['Date'] <= date_range[1])
        ]
    if call_direction:
        filtered_df = filtered_df[filtered_df['Call_Direction'].isin(call_direction)]
    if call_categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(call_categories)]

# ------------------- Key Metrics -------------------
st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    total_calls = len(filtered_df)
    answered_calls = len(filtered_df[filtered_df["Call_Status"].str.lower().str.contains("answered", na=False)])
    missed_calls = len(filtered_df[filtered_df["Call_Status"].str.lower().str.contains("missed", na=False)])
    missed_rate = round((missed_calls / total_calls) * 100, 2) if total_calls else 0
    avg_conv = round(filtered_df["Conversation_Duration"].mean(), 2) if 'Conversation_Duration' in filtered_df.columns else 0
    new_patient_calls = len(filtered_df[filtered_df["Contact_Type"] == "New Patient"]) if 'Contact_Type' in filtered_df.columns else 0
    appointment_bookings = len(filtered_df[filtered_df["Category"] == "Appointment Booking"])
    conversion_rate = round((appointment_bookings / total_calls) * 100, 2) if total_calls else 0
else:
    total_calls = answered_calls = missed_calls = missed_rate = avg_conv = new_patient_calls = appointment_bookings = conversion_rate = 0

# Metrics in two rows
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card" onclick="this.style.transform='scale(0.98)'">
        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">Total Calls</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #1f77b4;">{total_calls:,}</div>
        <div style="font-size: 0.8em; color: #888;">{answered_calls:,} answered</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">Missed Call Rate</div>
        <div style="font-size: 1.8em; font-weight: bold; color: {'#e74c3c' if missed_rate > 10 else '#27ae60'};">{missed_rate}%</div>
        <div style="font-size: 0.8em; color: #888;">{missed_calls:,} missed opportunities</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">Avg Call Duration</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #3498db;">{avg_conv}s</div>
        <div style="font-size: 0.8em; color: #888;">Conversation time</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    new_patient_percent = round((new_patient_calls/total_calls)*100, 1) if total_calls > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">New Patients</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #9b59b6;">{new_patient_calls:,}</div>
        <div style="font-size: 0.8em; color: #888;">{new_patient_percent}% of calls</div>
    </div>
    """, unsafe_allow_html=True)

# Second row of metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">Booking Rate</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #f39c12;">{conversion_rate}%</div>
        <div style="font-size: 0.8em; color: #888;">{appointment_bookings:,} bookings</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    emergency_calls = len(filtered_df[filtered_df["Category"] == "Emergency/Clinical"])
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">Emergency Calls</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #e74c3c;">{emergency_calls:,}</div>
        <div style="font-size: 0.8em; color: #888;">Urgent care needs</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    billing_calls = len(filtered_df[filtered_df["Category"] == "Billing/Payment"])
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">Billing Calls</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #2ecc71;">{billing_calls:,}</div>
        <div style="font-size: 0.8em; color: #888;">Payment discussions</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    insurance_calls = len(filtered_df[filtered_df["Category"] == "Insurance Inquiry"])
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">Insurance Calls</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #34495e;">{insurance_calls:,}</div>
        <div style="font-size: 0.8em; color: #888;">Coverage questions</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------- Interactive Charts Section -------------------
st.markdown('<div class="section-header">📊 Visual Analytics</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    # Create tabs for different chart types
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "📞 Call Types", "🕒 Patterns", "📋 Details"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("**Daily Call Volume**")
            
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            calls_per_day = filtered_df.groupby("Date").size()
            
            if not calls_per_day.empty:
                ax1.plot(calls_per_day.index, calls_per_day.values, 
                        marker="o", color="#3498db", linewidth=2, markersize=4)
                ax1.fill_between(calls_per_day.index, calls_per_day.values, alpha=0.2, color="#3498db")
                
                ax1.set_xlabel("Date")
                ax1.set_ylabel("Calls")
                ax1.grid(True, linestyle='--', alpha=0.3)
                ax1.tick_params(axis='x', rotation=45)
                
                plt.tight_layout()
                st.pyplot(fig1)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**📈 Trend Insights**")
            if not calls_per_day.empty:
                peak_day = calls_per_day.idxmax()
                peak_calls = calls_per_day.max()
                avg_daily = calls_per_day.mean()
                
                st.metric("Peak Day", f"{peak_calls} calls", f"on {peak_day}")
                st.metric("Daily Average", f"{avg_daily:.1f}", "calls per day")
                st.metric("Total Period", f"{calls_per_day.sum():,}", f"over {len(calls_per_day)} days")
    
    with tab2:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("**Call Status Distribution**")
            
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            status_counts = filtered_df["Call_Status"].value_counts()
            
            if not status_counts.empty:
                colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
                wedges, texts, autotexts = ax2.pie(
                    status_counts.values,
                    labels=status_counts.index,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors[:len(status_counts)],
                    textprops={'fontsize': 10}
                )
                
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                
                plt.tight_layout()
                st.pyplot(fig2)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("**Call Categories**")
            
            category_counts = filtered_df["Category"].value_counts().head(8)
            fig3, ax3 = plt.subplots(figsize=(8, 6))
            
            if not category_counts.empty:
                y_pos = np.arange(len(category_counts))
                colors = plt.cm.Set3(np.linspace(0, 1, len(category_counts)))
                
                bars = ax3.barh(y_pos, category_counts.values, color=colors, alpha=0.8)
                ax3.set_yticks(y_pos)
                ax3.set_yticklabels(category_counts.index, fontsize=10)
                ax3.set_xlabel("Number of Calls")
                
                plt.tight_layout()
                st.pyplot(fig3)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("**Hourly Call Pattern**")
            
            fig4, ax4 = plt.subplots(figsize=(10, 4))
            hourly_calls = filtered_df['Hour'].value_counts().sort_index()
            
            if not hourly_calls.empty:
                ax4.bar(hourly_calls.index, hourly_calls.values, alpha=0.7, color='#3498db')
                ax4.set_xlabel("Hour of Day")
                ax4.set_ylabel("Number of Calls")
                ax4.set_xticks(range(0, 24, 2))
                ax4.grid(True, alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig4)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🕒 Peak Hours**")
            if not hourly_calls.empty:
                peak_hour = hourly_calls.idxmax()
                peak_calls = hourly_calls.max()
                quiet_hour = hourly_calls.idxmin()
                
                st.metric("Busiest Hour", f"{peak_hour}:00", f"{peak_calls} calls")
                st.metric("Quietest Hour", f"{quiet_hour}:00")
                st.metric("Daily Range", f"{hourly_calls.min()}-{peak_calls}", "calls per hour")
    
    with tab4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("**Call Duration by Category**")
        
        avg_durations = filtered_df.groupby("Category")["Conversation_Duration"].mean().nlargest(10)
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        
        if not avg_durations.empty:
            y_pos = np.arange(len(avg_durations))
            colors = plt.cm.viridis(np.linspace(0, 1, len(avg_durations)))
            
            bars = ax5.barh(y_pos, avg_durations.values, color=colors, alpha=0.8)
            ax5.set_yticks(y_pos)
            ax5.set_yticklabels(avg_durations.index, fontsize=10)
            ax5.set_xlabel("Average Duration (seconds)")
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax5.text(width + 1, bar.get_y() + bar.get_height()/2, 
                        f'{width:.1f}s', ha='left', va='center', fontsize=9)
            
            plt.tight_layout()
            st.pyplot(fig5)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------- Business Insights -------------------
st.markdown('<div class="section-header">💡 Business Insights</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="front-desk-impact">
    <h4>🎯 Front Desk Optimization</h4>
    <ul>
    <li><strong>Staffing:</strong> Align breaks with low-call hours ({quiet_hour if 'quiet_hour' in locals() else '11'}:00-{quiet_hour+1 if 'quiet_hour' in locals() else '12'}:00)</li>
    <li><strong>Training:</strong> Focus on insurance and billing queries</li>
    <li><strong>Efficiency:</strong> Target under 30s average call duration</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="business-impact">
    <h4>💰 Revenue Opportunities</h4>
    <ul>
    <li><strong>Recovery:</strong> Implement call-back for {missed_calls} missed calls</li>
    <li><strong>Conversion:</strong> Improve booking rate from {conversion_rate}% to 25%+</li>
    <li><strong>Growth:</strong> Focus on {new_patient_calls} new patient acquisitions</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ------------------- Data Explorer -------------------
st.markdown('<div class="section-header">🔍 Data Explorer</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    # Add search and filter options for the data table
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Filter Data**")
        show_columns = st.multiselect(
            "Select columns to display:",
            options=['Call_Time', 'Call_Direction', 'Call_Status', 'Contact_Type', 'Category', 'Conversation_Duration'],
            default=['Call_Time', 'Call_Status', 'Category', 'Conversation_Duration']
        )
        
        rows_to_show = st.slider("Number of rows to display:", 10, 100, 20)
    
    with col2:
        st.markdown("**Call Details**")
        if show_columns:
            st.dataframe(
                filtered_df[show_columns].sort_values('Call_Time', ascending=False).head(rows_to_show),
                use_container_width=True,
                height=400
            )
            st.caption(f"Showing {min(rows_to_show, len(filtered_df))} of {len(filtered_df):,} total calls")
else:
    st.info("📊 No data available to display. Please check your filters or data source.")

# ------------------- Footer -------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Dental Call Analytics</strong> | Done by Raaj Kennedy</p>
    <small>Built for dental practices to optimize front desk operations and drive growth</small>
</div>
""", unsafe_allow_html=True)

# Clear figures
plt.close('all')
