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

import os
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class MultiAIRecommender:
    """AI-powered business recommendations supporting multiple AI models"""
    
    def __init__(self, model_type: str = "openai", api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize AI recommender with different model options
        
        Args:
            model_type: "openai", "deepseek", "ollama", "openrouter"
            api_key: API key for the chosen service
            base_url: Base URL for API calls (for local/self-hosted models)
        """
        self.model_type = model_type
        self.api_key = api_key
        self.base_url = base_url
        
        # Model configurations
        self.models = {
            "openai": {
                "name": "gpt-3.5-turbo",
                "max_tokens": 800,
                "temperature": 0.7
            },
            "deepseek": {
                "name": "deepseek-r1t2-chimera",
                "max_tokens": 1000,
                "temperature": 0.7
            },
            "ollama": {
                "name": "llama3.1:8b",
                "max_tokens": 800,
                "temperature": 0.7
            },
            "openrouter": {
                "name": "tngtech/deepseek-r1t2-chimera:free",
                "max_tokens": 1000,
                "temperature": 0.7
            }
        }
        
        self.current_model = self.models.get(model_type, self.models["openai"])
        
    def _make_api_call(self, prompt: str, system_prompt: str = None) -> str:
        """Make API call to the selected AI model"""
        
        try:
            if self.model_type == "openai":
                return self._call_openai(prompt, system_prompt)
            elif self.model_type == "deepseek":
                return self._call_deepseek(prompt, system_prompt)
            elif self.model_type == "ollama":
                return self._call_ollama(prompt, system_prompt)
            elif self.model_type == "openrouter":
                return self._call_openrouter(prompt, system_prompt)
            else:
                return self._call_openai(prompt, system_prompt)  # fallback
                
        except Exception as e:
            return f"Error calling AI model: {str(e)}"
    
    def _call_openai(self, prompt: str, system_prompt: str = None) -> str:
        """Call OpenAI API"""
        if not self.api_key:
            return "OpenAI API key is required"
        
        openai.api_key = self.api_key
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model=self.current_model["name"],
            messages=messages,
            max_tokens=self.current_model["max_tokens"],
            temperature=self.current_model["temperature"]
        )
        
        return response.choices[0].message.content
    
    def _call_deepseek(self, prompt: str, system_prompt: str = None) -> str:
        """Call DeepSeek API (OpenRouter compatible)"""
        if not self.api_key:
            return "API key is required for DeepSeek"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "max_tokens": self.current_model["max_tokens"],
            "temperature": self.current_model["temperature"]
        }
        
        response = requests.post(
            "https://api.openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    def _call_ollama(self, prompt: str, system_prompt: str = None) -> str:
        """Call local Ollama API"""
        base_url = self.base_url or "http://localhost:11434"
        
        data = {
            "model": self.current_model["name"],
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.current_model["temperature"],
                "num_predict": self.current_model["max_tokens"]
            }
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        response = requests.post(
            f"{base_url}/api/generate",
            json=data
        )
        
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    def _call_openrouter(self, prompt: str, system_prompt: str = None) -> str:
        """Call OpenRouter API for DeepSeek R1T2 Chimera"""
        if not self.api_key:
            return "OpenRouter API key is required"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ceo-dashboard.com",
            "X-Title": "CEO Dashboard"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.current_model["name"],
            "messages": messages,
            "max_tokens": self.current_model["max_tokens"],
            "temperature": self.current_model["temperature"]
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    
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
        
        system_prompt = "You are an expert business analyst providing insights to CEOs and business owners."
        
        return self._make_api_call(prompt, system_prompt)
    
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
        
        system_prompt = "You are a strategic business advisor helping CEOs understand forecasts and make decisions."
        
        return self._make_api_call(prompt, system_prompt)
    
    def generate_comprehensive_forecast_analysis(self, forecasts_data: Dict[str, Any]) -> str:
        """Generate comprehensive business forecasting analysis"""
        
        # Prepare comprehensive forecast data
        analysis_data = {}
        
        for metric, data in forecasts_data.items():
            if data and 'summary' in data:
                summary = data['summary']
                analysis_data[metric] = {
                    'next_30_days_total': summary.get('next_30_days_total', 0),
                    'next_30_days_avg': summary.get('next_30_days_avg', 0),
                    'trend_direction': summary.get('trend_direction', 'unknown'),
                    'confidence_lower': summary.get('confidence_lower', 0),
                    'confidence_upper': summary.get('confidence_upper', 0)
                }
        
        prompt = f"""
        As a senior business analyst and forecasting expert, provide a comprehensive business forecasting analysis:
        
        FORECAST DATA:
        {json.dumps(analysis_data, indent=2)}
        
        Please provide a detailed analysis including:
        
        1. **Executive Summary**
           - Overall business outlook for the next 30 days
           - Key trends across all metrics
        
        2. **Revenue Forecast Analysis**
           - Revenue projections and growth expectations
           - Seasonal factors and market conditions
           - Revenue optimization strategies
        
        3. **Profit Forecast Analysis**
           - Profit margin trends and projections
           - Cost management implications
           - Profitability improvement opportunities
        
        4. **Transaction Volume Analysis**
           - Customer behavior patterns
           - Sales volume projections
           - Customer acquisition and retention strategies
        
        5. **Strategic Recommendations**
           - Immediate actions (next 7 days)
           - Short-term strategies (next 30 days)
           - Medium-term planning (next 90 days)
        
        6. **Risk Assessment**
           - Potential challenges and threats
           - Market volatility factors
           - Contingency planning suggestions
        
        7. **Growth Opportunities**
           - Market expansion possibilities
           - Product optimization opportunities
           - Marketing and sales strategies
        
        8. **Operational Insights**
           - Resource allocation recommendations
           - Inventory management strategies
           - Team and process optimization
        
        Format this as a professional business report suitable for executive leadership.
        """
        
        system_prompt = "You are a senior business analyst and forecasting expert providing comprehensive business intelligence to CEOs and executive teams."
        
        return self._make_api_call(prompt, system_prompt)
    
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
        
        system_prompt = "You are a product strategy expert helping optimize product mix and performance."
        
        return self._make_api_call(prompt, system_prompt)
    
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
        
        system_prompt = "You are a marketing analytics expert helping optimize channel performance."
        
        return self._make_api_call(prompt, system_prompt)
    
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
        
        system_prompt = "You are a business intelligence expert helping CEOs understand their data and make informed decisions."
        
        return self._make_api_call(prompt, system_prompt)
    
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
        
        system_prompt = "You are a senior business analyst creating executive reports for CEOs and board members."
        
        return self._make_api_call(prompt, system_prompt)

def create_ai_insights_dashboard(sales_df: pd.DataFrame, kpis: Dict[str, Any], 
                                forecast_summary: Dict[str, Any] = None,
                                model_type: str = "openai", 
                                api_key: str = None,
                                base_url: str = None):
    """Create comprehensive AI insights dashboard with multiple model support"""
    
    try:
        recommender = MultiAIRecommender(
            model_type=model_type,
            api_key=api_key,
            base_url=base_url
        )
        
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
            'note': f"Please check your {model_type.upper()} API key configuration."
        }, None

if __name__ == "__main__":
    # Test the AI recommender
    from data_loader import load_or_generate_data, get_kpis
    
    sales_df, _ = load_or_generate_data()
    kpis = get_kpis(sales_df)
    
    # Test with different models
    models_to_test = ["openai", "deepseek", "openrouter"]
    
    for model in models_to_test:
        print(f"\n=== Testing {model.upper()} ===")
        try:
            recommender = MultiAIRecommender(model_type=model)
            insights = recommender.analyze_kpis(kpis)
            print(f"✅ {model} working")
            print(f"Sample insight: {insights[:100]}...")
        except Exception as e:
            print(f"❌ {model} error: {e}") 