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
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_or_generate_data, get_kpis
from utils.ai_recommender import MultiAIRecommender

def main():
    """AI Assistant for Business Intelligence"""
    
    st.set_page_config(
        page_title="AI Business Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    # Dark mode CSS
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
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>
        🤖 AI Business Assistant
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("### Your AI-powered business intelligence companion")
    
    # Load data
    with st.spinner("Loading business data..."):
        sales_df, inventory_df = load_data()
        kpis = calculate_kpis(sales_df)
    
    # Sidebar for API key
    st.sidebar.header("🔑 Configuration")
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key to enable AI features"
    )
    
    if not api_key:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar to use the AI assistant.")
        st.info("""
        **How to get an OpenAI API key:**
        1. Go to [OpenAI Platform](https://platform.openai.com/)
        2. Sign up or log in
        3. Navigate to API Keys section
        4. Create a new API key
        5. Copy and paste it here
        """)
        return
    
    try:
        recommender = MultiAIRecommender(model_type="openai", api_key=api_key)
    except Exception as e:
        st.error(f"❌ Error initializing AI assistant: {str(e)}")
        return
    
    # Main interface
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Insights", "📋 Reports"])
    
    with tab1:
        st.header("💬 Business Intelligence Chat")
        
        # Chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            with st.expander(f"Q: {question[:50]}...", expanded=False):
                st.write(f"**Question:** {question}")
                st.write(f"**Answer:** {answer}")
        
        # Input area
        st.subheader("Ask a Business Question")
        
        # Quick questions
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📈 How are our sales performing?"):
                question = "How are our sales performing this quarter compared to last quarter?"
                st.session_state.current_question = question
        
        with col2:
            if st.button("💰 What's our profit margin trend?"):
                question = "What's our profit margin trend and how can we improve it?"
                st.session_state.current_question = question
        
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("🏆 What are our best products?"):
                question = "What are our top 5 products by revenue and why are they successful?"
                st.session_state.current_question = question
        
        with col4:
            if st.button("📢 Which marketing channels work best?"):
                question = "Which marketing channels are most effective and how should we allocate our budget?"
                st.session_state.current_question = question
        
        # Custom question input
        if 'current_question' not in st.session_state:
            st.session_state.current_question = ""
        
        user_question = st.text_area(
            "Ask your business question:",
            value=st.session_state.current_question,
            height=100,
            placeholder="e.g., How can we increase our revenue by 20% in the next quarter?"
        )
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("🔍 Ask", type="primary"):
                if user_question.strip():
                    with st.spinner("🤖 Analyzing your question..."):
                        try:
                            answer = recommender.answer_business_question(user_question, sales_df, kpis)
                            
                            # Add to chat history
                            st.session_state.chat_history.append((user_question, answer))
                            
                            # Display answer
                            st.success("✅ Analysis complete!")
                            st.write("**Answer:**")
                            st.write(answer)
                            
                            # Clear current question
                            st.session_state.current_question = ""
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("Please enter a question.")
        
        with col2:
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.session_state.current_question = ""
                st.success("Chat history cleared!")
    
    with tab2:
        st.header("📊 AI-Powered Insights")
        
        # Insight categories
        insight_type = st.selectbox(
            "Choose insight type:",
            ["KPI Analysis", "Product Performance", "Marketing Analysis", "Strategic Recommendations"]
        )
        
        if st.button("🧠 Generate Insights", type="primary"):
            with st.spinner("Generating insights..."):
                try:
                    if insight_type == "KPI Analysis":
                        insights = recommender.analyze_kpis(kpis)
                        st.subheader("📊 KPI Analysis")
                        st.write(insights)
                    
                    elif insight_type == "Product Performance":
                        insights = recommender.analyze_product_performance(sales_df)
                        st.subheader("📦 Product Performance Analysis")
                        st.write(insights)
                    
                    elif insight_type == "Marketing Analysis":
                        insights = recommender.analyze_marketing_performance(sales_df)
                        st.subheader("📢 Marketing Performance Analysis")
                        st.write(insights)
                    
                    elif insight_type == "Strategic Recommendations":
                        # Combine multiple insights
                        kpi_insights = recommender.analyze_kpis(kpis)
                        product_insights = recommender.analyze_product_performance(sales_df)
                        marketing_insights = recommender.analyze_marketing_performance(sales_df)
                        
                        st.subheader("🎯 Strategic Recommendations")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**KPI Insights:**")
                            st.write(kpi_insights)
                        
                        with col2:
                            st.write("**Product Strategy:**")
                            st.write(product_insights)
                        
                        st.write("**Marketing Strategy:**")
                        st.write(marketing_insights)
                
                except Exception as e:
                    st.error(f"❌ Error generating insights: {str(e)}")
    
    with tab3:
        st.header("📋 Business Reports")
        
        # Report options
        report_type = st.selectbox(
            "Choose report type:",
            ["Quarterly Business Report", "Performance Summary", "Strategic Analysis"]
        )
        
        if st.button("📄 Generate Report", type="primary"):
            with st.spinner("Generating report..."):
                try:
                    if report_type == "Quarterly Business Report":
                        report = recommender.generate_quarterly_report(sales_df, kpis)
                        st.subheader("📋 Quarterly Business Report")
                        st.write(report)
                    
                    elif report_type == "Performance Summary":
                        # Create a comprehensive performance summary
                        summary_prompt = f"""
                        Create a comprehensive performance summary for our business based on:
                        - Revenue: ${kpis['total_revenue_30d']:,.2f} (30 days)
                        - Profit: ${kpis['total_profit_30d']:,.2f} (30 days)
                        - Growth: {kpis['revenue_growth']:.1f}%
                        - Top Product: {kpis['top_product']}
                        - Best Channel: {kpis['best_channel']}
                        
                        Include key highlights, trends, and actionable insights.
                        """
                        
                        report = recommender.answer_business_question(summary_prompt, sales_df, kpis)
                        st.subheader("📊 Performance Summary")
                        st.write(report)
                    
                    elif report_type == "Strategic Analysis":
                        # Strategic analysis combining multiple perspectives
                        strategic_prompt = """
                        Provide a strategic analysis of our business including:
                        1. Current market position
                        2. Competitive advantages
                        3. Growth opportunities
                        4. Risk factors
                        5. Strategic recommendations for the next 6 months
                        """
                        
                        report = recommender.answer_business_question(strategic_prompt, sales_df, kpis)
                        st.subheader("🎯 Strategic Analysis")
                        st.write(report)
                
                except Exception as e:
                    st.error(f"❌ Error generating report: {str(e)}")
        
        # Export options
        st.subheader("📤 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export KPIs"):
                kpi_df = pd.DataFrame([kpis])
                st.download_button(
                    label="Download KPIs as CSV",
                    data=kpi_df.to_csv(index=False),
                    file_name="business_kpis.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Export Sales Data"):
                st.download_button(
                    label="Download Sales Data as CSV",
                    data=sales_df.to_csv(index=False),
                    file_name="sales_data.csv",
                    mime="text/csv"
                )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>🤖 AI Business Assistant - Powered by Alae-Eddine Dahane</p>
        <p>Ask intelligent questions, get data-driven insights</p>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache business data"""
    return load_or_generate_data()

@st.cache_data
def calculate_kpis(sales_df):
    """Calculate and cache KPIs"""
    return get_kpis(sales_df)

if __name__ == "__main__":
    main() 