"""
MIT License

Copyright (c) 2025 Alae-Eddine Dahane

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_or_generate_data, get_kpis, get_time_series_data
from utils.forecasting_tools import BusinessForecaster, create_forecast_dashboard, analyze_business_trends
from utils.ai_recommender import MultiAIRecommender

# Page configuration
st.set_page_config(
    page_title="CEO Dashboard - Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Dark mode styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00d4aa;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px rgba(0, 212, 170, 0.3);
    }
    
    .metric-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #00d4aa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .positive-growth {
        color: #00d4aa;
        font-weight: bold;
    }
    
    .negative-growth {
        color: #ff4b4b;
        font-weight: bold;
    }
    
    /* Improved tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #0e1117;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: nowrap;
        background-color: #262730;
        border-radius: 6px;
        gap: 1px;
        padding: 8px 16px;
        margin: 2px;
        border: 1px solid #4a4a4a;
        transition: all 0.3s ease;
        font-weight: 500;
        color: #fafafa;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #363840;
        border-color: #00d4aa;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00d4aa;
        color: #0e1117;
        border-color: #00d4aa;
        box-shadow: 0 2px 8px rgba(0, 212, 170, 0.3);
        font-weight: 600;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem 0;
        border-top: 1px solid #4a4a4a;
        margin-top: 3rem;
    }
    
    .footer p {
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    /* General dark mode improvements */
    .stApp {
        background-color: #0e1117;
    }
    
    .stMarkdown {
        color: #fafafa;
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        background-color: #262730;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache business data"""
    return load_or_generate_data()

@st.cache_data
def calculate_kpis(sales_df):
    """Calculate and cache KPIs"""
    return get_kpis(sales_df)

def create_kpi_cards(kpis):
    """Create KPI metric cards"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Revenue (30d)",
            value=f"${kpis['total_revenue_30d']:,.0f}",
            delta=f"{kpis['revenue_growth']:+.1f}%"
        )
    
    with col2:
        st.metric(
            label="💵 Total Profit (30d)",
            value=f"${kpis['total_profit_30d']:,.0f}",
            delta=f"{kpis['profit_growth']:+.1f}%"
        )
    
    with col3:
        st.metric(
            label="🛒 Transactions (30d)",
            value=f"{kpis['total_transactions_30d']:,}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="📈 Avg Order Value",
            value=f"${kpis['avg_order_value_30d']:.0f}",
            delta=None
        )

def create_revenue_chart(sales_df):
    """Create revenue trend chart"""
    
    # Daily revenue data
    daily_revenue = sales_df.groupby('date')['revenue'].sum().reset_index()
    
    fig = px.line(
        daily_revenue,
        x='date',
        y='revenue',
        title='📈 Daily Revenue Trend',
        labels={'revenue': 'Revenue ($)', 'date': 'Date'}
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig

def create_product_performance_chart(sales_df):
    """Create product performance chart"""
    
    # Top 10 products by revenue
    product_performance = sales_df.groupby('product').agg({
        'revenue': 'sum',
        'total_profit': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    top_products = product_performance.nlargest(10, 'revenue')
    
    fig = px.bar(
        top_products,
        x='revenue',
        y='product',
        orientation='h',
        title='🏆 Top 10 Products by Revenue',
        labels={'revenue': 'Revenue ($)', 'product': 'Product'}
    )
    
    fig.update_layout(height=400)
    
    return fig

def create_category_performance_chart(sales_df):
    """Create category performance chart"""
    
    category_performance = sales_df.groupby('category').agg({
        'revenue': 'sum',
        'total_profit': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    
    category_performance['profit_margin'] = (category_performance['total_profit'] / category_performance['revenue'] * 100)
    
    fig = px.scatter(
        category_performance,
        x='revenue',
        y='profit_margin',
        size='transaction_id',
        color='category',
        title='📊 Category Performance: Revenue vs Profit Margin',
        labels={'revenue': 'Revenue ($)', 'profit_margin': 'Profit Margin (%)', 'transaction_id': 'Transactions'},
        hover_data=['category', 'revenue', 'profit_margin', 'transaction_id']
    )
    
    fig.update_layout(height=400)
    
    return fig

def create_marketing_channel_chart(sales_df):
    """Create marketing channel performance chart"""
    
    channel_performance = sales_df.groupby('marketing_channel').agg({
        'revenue': 'sum',
        'total_profit': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    
    channel_performance['avg_order_value'] = channel_performance['revenue'] / channel_performance['transaction_id']
    
    fig = px.bar(
        channel_performance,
        x='marketing_channel',
        y='revenue',
        title='📢 Marketing Channel Performance',
        labels={'revenue': 'Revenue ($)', 'marketing_channel': 'Marketing Channel'},
        color='avg_order_value',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(height=400)
    
    return fig

def create_forecast_charts(forecaster, forecasts):
    """Create forecast visualization charts"""
    
    if not forecasts:
        st.warning("No forecast data available. Please check your data.")
        return None
    
    # Get the first metric from forecasts (should be the selected one)
    metric = list(forecasts.keys())[0]
    forecast_data = forecasts[metric]['forecast']
    
    fig = go.Figure()
    
    # Historical data (where y is not null)
    historical = forecast_data[forecast_data['y'].notna()]
    if not historical.empty:
        fig.add_trace(go.Scatter(
            x=historical['ds'],
            y=historical['y'],
            mode='markers+lines',
            name='Historical',
            line=dict(color='#00d4aa', width=2),
            marker=dict(size=4)
        ))
    
    # Forecast (where y is null)
    future = forecast_data[forecast_data['y'].isna()]
    if not future.empty:
        fig.add_trace(go.Scatter(
            x=future['ds'],
            y=future['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='#ff6b6b', width=2, dash='dash')
        ))
        
        # Confidence intervals
        if 'yhat_upper' in future.columns and 'yhat_lower' in future.columns:
            fig.add_trace(go.Scatter(
                x=future['ds'].tolist() + future['ds'].tolist()[::-1],
                y=future['yhat_upper'].tolist() + future['yhat_lower'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(255,107,107,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval'
            ))
    
    # Set title based on metric
    metric_titles = {
        'revenue': 'Revenue ($)',
        'profit': 'Profit ($)',
        'transactions': 'Transactions'
    }
    
    fig.update_layout(
        title=f'🔮 {metric.title()} Forecast (Next 30 Days)',
        xaxis_title='Date',
        yaxis_title=metric_titles.get(metric, metric.title()),
        height=400,
        hovermode='x unified',
        template='plotly_dark'
    )
    
    return fig

def create_inventory_chart(inventory_df):
    """Create inventory analysis chart"""
    
    # Products with low stock
    low_stock = inventory_df[inventory_df['current_stock'] <= inventory_df['reorder_point']]
    
    fig = px.bar(
        low_stock,
        x='product',
        y='current_stock',
        title='⚠️ Products Needing Restock',
        labels={'current_stock': 'Current Stock', 'product': 'Product'},
        color='days_of_inventory',
        color_continuous_scale='reds'
    )
    
    fig.update_layout(height=400)
    
    return fig

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">🚀 CEO Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Business Intelligence & AI-Powered Insights")
    
    # Load data
    with st.spinner("Loading business data..."):
        sales_df, inventory_df = load_data()
        kpis = calculate_kpis(sales_df)
    
    # Sidebar filters
    st.sidebar.header("📊 Dashboard Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(sales_df['date'].min().date(), sales_df['date'].max().date()),
        min_value=sales_df['date'].min().date(),
        max_value=sales_df['date'].max().date()
    )
    
    # Category filter
    categories = ['All'] + list(sales_df['category'].unique())
    selected_category = st.sidebar.selectbox("Category", categories)
    
    # Product filter
    if selected_category != 'All':
        products = ['All'] + list(sales_df[sales_df['category'] == selected_category]['product'].unique())
    else:
        products = ['All'] + list(sales_df['product'].unique())
    
    selected_product = st.sidebar.selectbox("Product", products)
    
    # Apply filters
    filtered_sales = sales_df.copy()
    if len(date_range) == 2:
        filtered_sales = filtered_sales[
            (filtered_sales['date'].dt.date >= date_range[0]) &
            (filtered_sales['date'].dt.date <= date_range[1])
        ]
    
    if selected_category != 'All':
        filtered_sales = filtered_sales[filtered_sales['category'] == selected_category]
    
    if selected_product != 'All':
        filtered_sales = filtered_sales[filtered_sales['product'] == selected_product]
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "🔮 Forecasting", 
        "🤖 AI Insights", 
        "📦 Inventory", 
        "💬 Business Chat"
    ])
    
    with tab1:
        st.header("📊 Business Dashboard")
        
        # KPI Cards
        create_kpi_cards(kpis)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            revenue_fig = create_revenue_chart(filtered_sales)
            st.plotly_chart(revenue_fig, use_container_width=True)
            
            product_fig = create_product_performance_chart(filtered_sales)
            st.plotly_chart(product_fig, use_container_width=True)
        
        with col2:
            category_fig = create_category_performance_chart(filtered_sales)
            st.plotly_chart(category_fig, use_container_width=True)
            
            marketing_fig = create_marketing_channel_chart(filtered_sales)
            st.plotly_chart(marketing_fig, use_container_width=True)
        
        # Recent transactions
        st.subheader("🕒 Recent Transactions")
        recent_transactions = filtered_sales.nlargest(10, 'date')[['date', 'product', 'revenue', 'total_profit', 'marketing_channel']]
        st.dataframe(recent_transactions, use_container_width=True)
    
    with tab2:
        st.header("🔮 Business Forecasting")
        
        # Forecasting controls
        col1, col2 = st.columns(2)
        
        with col1:
            forecast_periods = st.selectbox("Forecast Period", [30, 60, 90, 180], index=0)
            forecast_metric = st.selectbox("Forecast Metric", ['revenue', 'profit', 'transactions'], index=0)
        
        with col2:
            if st.button("🔄 Generate Forecast", type="primary"):
                with st.spinner("Training forecasting models..."):
                    forecaster = BusinessForecaster()
                    
                    # Generate comprehensive forecasts for all metrics
                    metrics_data, forecasts_data = forecaster.get_comprehensive_forecast_data(filtered_sales, periods=forecast_periods)
                    
                    # Display forecast for selected metric
                    if forecast_metric in forecasts_data:
                        forecast_fig = create_forecast_charts(forecaster, {forecast_metric: forecasts_data[forecast_metric]})
                        if forecast_fig:
                            st.plotly_chart(forecast_fig, use_container_width=True)
                        
                        # Forecast summary
                        summary = forecasts_data[forecast_metric]['summary']
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Next 30 Days Total", f"${summary['next_30_days_total']:,.0f}")
                        with col2:
                            st.metric("Next 30 Days Avg", f"${summary['next_30_days_avg']:,.0f}")
                        with col3:
                            st.metric("Trend", summary['trend_direction'].title())
                        
                        # Store forecasts for AI analysis
                        st.session_state['forecasts_data'] = forecasts_data
                    else:
                        st.error(f"Could not generate forecast for {forecast_metric}")
        
        # Business trends analysis
        st.subheader("📈 Business Trends Analysis")
        trends = analyze_business_trends(filtered_sales)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Best Month", f"Month {trends['best_month']}")
        with col2:
            st.metric("Worst Month", f"Month {trends['worst_month']}")
        with col3:
            st.metric("Best Day", f"Day {trends['best_day']}")
        with col4:
            st.metric("Revenue Volatility", f"{trends['revenue_volatility']:.1f}%")
    
    with tab3:
        st.header("🤖 AI-Powered Insights")
        
        # AI Model Selection
        st.subheader("🤖 AI Model Configuration")
        
        # Model selection
        model_type = st.selectbox(
            "Choose AI Model:",
            ["openrouter", "openai", "deepseek", "ollama"],
            help="Select your preferred AI model for insights"
        )
        
        # API Key input
        api_key_label = {
            "openrouter": "OpenRouter API Key",
            "openai": "OpenAI API Key", 
            "deepseek": "DeepSeek API Key",
            "ollama": "Ollama Base URL (optional)"
        }
        
        api_key = st.text_input(
            api_key_label[model_type], 
            type="password", 
            help=f"Enter your {model_type.upper()} API key to enable AI insights"
        )
        
        # Base URL for Ollama
        base_url = None
        if model_type == "ollama":
            base_url = st.text_input(
                "Ollama Base URL",
                value="http://localhost:11434",
                help="URL where Ollama is running"
            )
        
        if api_key or model_type == "ollama":
            try:
                recommender = MultiAIRecommender(
                    model_type=model_type,
                    api_key=api_key,
                    base_url=base_url
                )
                
                # Generate insights
                if st.button("🧠 Generate AI Insights", type="primary"):
                    with st.spinner("Generating AI insights..."):
                        insights = recommender.analyze_kpis(kpis)
                        st.subheader("📊 KPI Analysis")
                        st.write(insights)
                        
                        product_insights = recommender.analyze_product_performance(filtered_sales)
                        st.subheader("📦 Product Performance Analysis")
                        st.write(product_insights)
                        
                        marketing_insights = recommender.analyze_marketing_performance(filtered_sales)
                        st.subheader("📢 Marketing Performance Analysis")
                        st.write(marketing_insights)
                        
                        quarterly_report = recommender.generate_quarterly_report(filtered_sales, kpis)
                        st.subheader("📋 Quarterly Business Report")
                        st.write(quarterly_report)
                
                # Comprehensive Forecasting Analysis
                if 'forecasts_data' in st.session_state and st.session_state['forecasts_data']:
                    if st.button("🔮 Generate Comprehensive Forecast Analysis", type="primary"):
                        with st.spinner("Generating comprehensive forecast analysis..."):
                            forecast_analysis = recommender.generate_comprehensive_forecast_analysis(st.session_state['forecasts_data'])
                            st.subheader("🔮 Comprehensive Business Forecasting Analysis")
                            st.write(forecast_analysis)
                else:
                    st.info("💡 Generate forecasts in the Forecasting tab first to enable comprehensive AI analysis.")
                
                # Business question chatbot
                st.subheader("💬 Ask Business Questions")
                question = st.text_input("Ask a question about your business data:")
                
                if question and st.button("🔍 Get Answer"):
                    with st.spinner("Analyzing your question..."):
                        answer = recommender.answer_business_question(question, filtered_sales, kpis)
                        st.write(answer)
            
            except Exception as e:
                st.error(f"Error with AI features: {str(e)}")
                st.info("Please check your OpenAI API key and try again.")
        else:
            st.info("🔑 Enter your OpenAI API key above to enable AI-powered insights and recommendations.")
    
    with tab4:
        st.header("📦 Inventory Management")
        
        # Inventory overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Products", len(inventory_df))
        with col2:
            low_stock_count = len(inventory_df[inventory_df['current_stock'] <= inventory_df['reorder_point']])
            st.metric("Products Needing Restock", low_stock_count)
        with col3:
            avg_days_inventory = inventory_df['days_of_inventory'].mean()
            st.metric("Avg Days of Inventory", f"{avg_days_inventory:.1f}")
        
        # Inventory charts
        col1, col2 = st.columns(2)
        
        with col1:
            inventory_fig = create_inventory_chart(inventory_df)
            st.plotly_chart(inventory_fig, use_container_width=True)
        
        with col2:
            # Days of inventory by category
            category_inventory = inventory_df.groupby('category')['days_of_inventory'].mean().reset_index()
            fig = px.bar(
                category_inventory,
                x='category',
                y='days_of_inventory',
                title='📅 Average Days of Inventory by Category',
                labels={'days_of_inventory': 'Days of Inventory', 'category': 'Category'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Inventory table
        st.subheader("📋 Inventory Details")
        st.dataframe(inventory_df, use_container_width=True)
    
    with tab5:
        st.header("💬 Business Intelligence Chat")
        
        st.info("🤖 This feature allows you to ask natural language questions about your business data.")
        
        # Example questions
        st.subheader("💡 Example Questions")
        example_questions = [
            "How did we perform this quarter?",
            "What are our top 5 products by revenue?",
            "Which marketing channels are most effective?",
            "What's our profit margin trend?",
            "When are our peak sales periods?",
            "How many customers do we have?",
            "What's our average order value?",
            "Which products need restocking?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{question}"):
                st.session_state['chat_question'] = question
        
        # Chat interface
        if 'chat_question' not in st.session_state:
            st.session_state['chat_question'] = ""
        
        user_question = st.text_input("Ask your business question:", value=st.session_state['chat_question'])
        
        if user_question and st.button("🔍 Get Answer"):
            if api_key or model_type == "ollama":
                try:
                    recommender = MultiAIRecommender(
                        model_type=model_type,
                        api_key=api_key,
                        base_url=base_url
                    )
                    with st.spinner("Analyzing your question..."):
                        answer = recommender.answer_business_question(user_question, filtered_sales, kpis)
                        st.write("**Answer:**")
                        st.write(answer)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.error(f"Please enter your {model_type.upper()} API key in the AI Insights tab to use the chat feature.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>🚀 CEO Dashboard - Powered by Alae-Eddine Dahane</p>
        <p>Built with Streamlit, Plotly, Prophet, and DeepSeek R1T2 Chimera</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 