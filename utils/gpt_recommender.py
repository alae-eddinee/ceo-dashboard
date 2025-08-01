import os
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import openai
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class BusinessAIRecommender:
    """AI-powered business recommendations using GPT"""
    
    def __init__(self, api_key=None):
        """Initialize the AI recommender"""
        
        # Set up OpenAI API key
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Initialize LangChain
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=self.api_key
        )
    
    def analyze_kpis(self, kpis: Dict[str, Any]) -> str:
        """Analyze KPIs and provide insights"""
        
        prompt = f"""
        As a business analyst, analyze these Key Performance Indicators and provide actionable insights:
        
        Revenue (30 days): ${kpis.get('total_revenue_30d', 0):,.2f}
        Profit (30 days): ${kpis.get('total_profit_30d', 0):,.2f}
        Transactions (30 days): {kpis.get('total_transactions_30d', 0):,}
        Average Order Value: ${kpis.get('avg_order_value_30d', 0):,.2f}
        Profit Margin: {kpis.get('profit_margin_30d', 0):.1f}%
        Revenue Growth: {kpis.get('revenue_growth', 0):.1f}%
        Profit Growth: {kpis.get('profit_growth', 0):.1f}%
        Top Product: {kpis.get('top_product', 'N/A')}
        Top Category: {kpis.get('top_category', 'N/A')}
        Best Marketing Channel: {kpis.get('best_channel', 'N/A')}
        
        Provide:
        1. A brief analysis of current performance
        2. 3-5 specific, actionable recommendations
        3. Areas of concern or opportunity
        4. Next steps for the business owner
        
        Format your response in a clear, professional manner suitable for a CEO dashboard.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert business analyst providing insights to CEOs and business owners."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def generate_forecast_insights(self, forecast_summary: Dict[str, Any], metric: str = 'revenue') -> str:
        """Generate insights from forecasting results"""
        
        prompt = f"""
        As a business analyst, analyze this {metric} forecast and provide strategic insights:
        
        Next 30 Days Total: ${forecast_summary.get('next_30_days_total', 0):,.2f}
        Next 30 Days Average: ${forecast_summary.get('next_30_days_avg', 0):,.2f}
        Trend Direction: {forecast_summary.get('trend_direction', 'unknown')}
        Confidence Range: ${forecast_summary.get('confidence_lower', 0):,.2f} - ${forecast_summary.get('confidence_upper', 0):,.2f}
        
        Provide:
        1. What this forecast means for the business
        2. Strategic implications of the trend
        3. Recommended actions based on the forecast
        4. Risk factors to consider
        5. Opportunities to capitalize on
        
        Keep the response concise and actionable for business decision-making.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a strategic business advisor helping CEOs understand forecasts and make decisions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating forecast insights: {str(e)}"
    
    def analyze_product_performance(self, sales_df: pd.DataFrame) -> str:
        """Analyze product performance and provide recommendations"""
        
        # Calculate product metrics
        product_analysis = sales_df.groupby('product').agg({
            'revenue': 'sum',
            'total_profit': 'sum',
            'quantity': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        
        product_analysis['profit_margin'] = (product_analysis['total_profit'] / product_analysis['revenue'] * 100)
        product_analysis['avg_price'] = product_analysis['revenue'] / product_analysis['quantity']
        
        # Get top and bottom performers
        top_products = product_analysis.nlargest(5, 'revenue')
        bottom_products = product_analysis.nsmallest(5, 'revenue')
        high_margin_products = product_analysis.nlargest(5, 'profit_margin')
        
        # Prepare data for AI analysis
        top_products_data = top_products.to_dict('records')
        bottom_products_data = bottom_products.to_dict('records')
        high_margin_data = high_margin_products.to_dict('records')
        
        prompt = f"""
        Analyze this product performance data and provide strategic recommendations:
        
        TOP 5 PRODUCTS BY REVENUE:
        {json.dumps(top_products_data, indent=2)}
        
        BOTTOM 5 PRODUCTS BY REVENUE:
        {json.dumps(bottom_products_data, indent=2)}
        
        TOP 5 PRODUCTS BY PROFIT MARGIN:
        {json.dumps(high_margin_data, indent=2)}
        
        Provide:
        1. Key insights about product performance
        2. Recommendations for underperforming products
        3. Opportunities to optimize high-margin products
        4. Inventory and pricing strategies
        5. Marketing focus recommendations
        
        Focus on actionable business strategies.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a product strategy expert helping optimize product mix and performance."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error analyzing product performance: {str(e)}"
    
    def analyze_marketing_performance(self, sales_df: pd.DataFrame) -> str:
        """Analyze marketing channel performance"""
        
        # Calculate marketing metrics
        marketing_analysis = sales_df.groupby('marketing_channel').agg({
            'revenue': 'sum',
            'total_profit': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()
        
        marketing_analysis['avg_order_value'] = marketing_analysis['revenue'] / marketing_analysis['transaction_id']
        marketing_analysis['profit_margin'] = (marketing_analysis['total_profit'] / marketing_analysis['revenue'] * 100)
        marketing_analysis['customer_acquisition_cost'] = marketing_analysis['revenue'] / marketing_analysis['customer_id']
        
        marketing_data = marketing_analysis.to_dict('records')
        
        prompt = f"""
        Analyze this marketing channel performance data:
        
        {json.dumps(marketing_data, indent=2)}
        
        Provide:
        1. Which channels are performing best and why
        2. Marketing budget allocation recommendations
        3. Channel-specific optimization strategies
        4. Customer acquisition insights
        5. ROI improvement opportunities
        
        Focus on data-driven marketing decisions.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a marketing analytics expert helping optimize channel performance."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error analyzing marketing performance: {str(e)}"
    
    def answer_business_question(self, question: str, sales_df: pd.DataFrame, kpis: Dict[str, Any] = None) -> str:
        """Answer specific business questions using natural language"""
        
        # Prepare context data
        context = f"""
        Business Data Context:
        - Total sales records: {len(sales_df):,}
        - Date range: {sales_df['date'].min()} to {sales_df['date'].max()}
        - Total revenue: ${sales_df['revenue'].sum():,.2f}
        - Total profit: ${sales_df['total_profit'].sum():,.2f}
        - Number of products: {sales_df['product'].nunique()}
        - Number of customers: {sales_df['customer_id'].nunique()}
        """
        
        if kpis:
            context += f"""
            Recent KPIs (30 days):
            - Revenue: ${kpis.get('total_revenue_30d', 0):,.2f}
            - Profit: ${kpis.get('total_profit_30d', 0):,.2f}
            - Growth: {kpis.get('revenue_growth', 0):.1f}%
            """
        
        prompt = f"""
        {context}
        
        Business Question: {question}
        
        Based on the available business data, provide a comprehensive answer to the question. 
        Include relevant metrics, insights, and actionable recommendations where appropriate.
        If the question cannot be answered with the available data, explain what additional data would be needed.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a business intelligence expert helping CEOs understand their data and make informed decisions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error answering question: {str(e)}"
    
    def generate_quarterly_report(self, sales_df: pd.DataFrame, kpis: Dict[str, Any]) -> str:
        """Generate a comprehensive quarterly business report"""
        
        # Calculate quarterly metrics
        sales_df['quarter'] = sales_df['date'].dt.quarter
        sales_df['year'] = sales_df['date'].dt.year
        
        quarterly_data = sales_df.groupby(['year', 'quarter']).agg({
            'revenue': 'sum',
            'total_profit': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()
        
        quarterly_data['profit_margin'] = (quarterly_data['total_profit'] / quarterly_data['revenue'] * 100)
        quarterly_data['avg_order_value'] = quarterly_data['revenue'] / quarterly_data['transaction_id']
        
        # Get latest quarter
        latest_quarter = quarterly_data.iloc[-1]
        
        prompt = f"""
        Generate a comprehensive quarterly business report based on this data:
        
        QUARTERLY PERFORMANCE:
        {quarterly_data.to_string()}
        
        LATEST QUARTER (Q{latest_quarter['quarter']} {latest_quarter['year']}):
        - Revenue: ${latest_quarter['revenue']:,.2f}
        - Profit: ${latest_quarter['total_profit']:,.2f}
        - Transactions: {latest_quarter['transaction_id']:,}
        - Customers: {latest_quarter['customer_id']:,}
        - Profit Margin: {latest_quarter['profit_margin']:.1f}%
        - Average Order Value: ${latest_quarter['avg_order_value']:.2f}
        
        RECENT KPIs:
        - 30-day Revenue: ${kpis.get('total_revenue_30d', 0):,.2f}
        - 30-day Growth: {kpis.get('revenue_growth', 0):.1f}%
        - Top Product: {kpis.get('top_product', 'N/A')}
        - Best Channel: {kpis.get('best_channel', 'N/A')}
        
        Structure the report with:
        1. Executive Summary
        2. Financial Performance
        3. Operational Highlights
        4. Key Insights
        5. Strategic Recommendations
        6. Next Quarter Outlook
        
        Make it professional and actionable for business leadership.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a senior business analyst creating executive reports for CEOs and board members."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating quarterly report: {str(e)}"

def create_ai_insights_dashboard(sales_df: pd.DataFrame, kpis: Dict[str, Any], forecast_summary: Dict[str, Any] = None):
    """Create comprehensive AI insights dashboard"""
    
    try:
        recommender = BusinessAIRecommender()
        
        insights = {
            'kpi_analysis': recommender.analyze_kpis(kpis),
            'product_analysis': recommender.analyze_product_performance(sales_df),
            'marketing_analysis': recommender.analyze_marketing_performance(sales_df),
            'quarterly_report': recommender.generate_quarterly_report(sales_df, kpis)
        }
        
        if forecast_summary:
            insights['forecast_insights'] = recommender.generate_forecast_insights(forecast_summary)
        
        return insights, recommender
        
    except Exception as e:
        return {
            'error': f"Failed to create AI insights: {str(e)}",
            'note': "Please check your OpenAI API key configuration."
        }, None

if __name__ == "__main__":
    # Test the AI recommender
    from data_loader import load_or_generate_data, get_kpis
    
    sales_df, _ = load_or_generate_data()
    kpis = get_kpis(sales_df)
    
    # Test with mock API key (replace with real key for testing)
    try:
        recommender = BusinessAIRecommender()
        insights = recommender.analyze_kpis(kpis)
        print("KPI Analysis:")
        print(insights)
    except Exception as e:
        print(f"Error: {e}")
        print("Please set OPENAI_API_KEY environment variable to test AI features.") 