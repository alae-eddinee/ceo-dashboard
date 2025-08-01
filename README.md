# 🚀 CEO Dashboard - Business Intelligence Platform

A comprehensive BI dashboard designed for small business owners and CEOs to analyze past performance, forecast future trends, and receive AI-powered recommendations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)

## 🎯 Key Features

### 📊 **Sales & Revenue Analytics**
- Interactive charts and KPIs (daily/monthly/yearly)
- Revenue trends and growth analysis
- Product performance insights

### 📈 **AI-Powered Forecasting**
- Predict sales, traffic, and costs for upcoming periods
- Time series analysis using Prophet
- Seasonal trend identification

### 🤖 **AI Recommendations**
- GPT-3.5 powered business insights
- Actionable recommendations based on data analysis
- Strategic suggestions for business improvement

### 📦 **Inventory & Product Analytics**
- Track bestsellers and underperforming products
- Inventory turnover analysis
- Product category performance

### 📅 **Time-Based Trend Analysis**
- Peak hours, days, and months identification
- Seasonal pattern recognition
- Historical performance comparison

### 💬 **Business Summary Chatbot**
- Natural language queries about business performance
- "How did we do this quarter?" type questions
- Interactive business intelligence

## 🛠️ Tech Stack

- **Python**: Core programming language
- **Streamlit**: Interactive web dashboard
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Prophet**: Time series forecasting
- **OpenAI GPT-3.5**: AI recommendations and insights
- **Faker**: Synthetic business data generation

## 📁 Project Structure

```
ceo-dashboard/
├── data/
│   ├── sales_data.csv
│   └── inventory_data.csv
├── app/
│   ├── dashboard.py
│   └── ai_assistant.py
├── utils/
│   ├── data_loader.py
│   ├── forecasting_tools.py
│   └── gpt_recommender.py
├── notebooks/
│   ├── exploration.ipynb
│   └── forecasting.ipynb
├── README.md
└── requirements.txt
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up OpenAI API Key
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Dashboard
```bash
streamlit run app/dashboard.py
```

### 4. Access the Dashboard
Open your browser and go to: `http://localhost:8501`

## 📊 Dashboard Sections

### **Main Dashboard**
- Key Performance Indicators (KPIs)
- Revenue trends and growth metrics
- Top-performing products
- Recent sales activity

### **Forecasting**
- Sales predictions for next 30/90/365 days
- Revenue forecasting with confidence intervals
- Seasonal trend analysis

### **AI Insights**
- Automated business recommendations
- Performance analysis and suggestions
- Strategic insights based on data patterns

### **Product Analytics**
- Product performance comparison
- Inventory turnover rates
- Category-wise analysis

### **Business Chatbot**
- Ask questions about your business performance
- Get instant insights and recommendations
- Natural language interface for data exploration

## 🎨 Features in Detail

### **Interactive Visualizations**
- Hover effects for detailed information
- Zoom and pan capabilities
- Filterable charts by date range and categories

### **Real-time Data Processing**
- Automatic data updates
- Dynamic KPI calculations
- Responsive design

### **Export Capabilities**
- Download charts as images
- Export data as CSV/Excel
- Generate PDF reports

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for AI features
- `DATA_PATH`: Path to your business data files
- `FORECAST_PERIODS`: Number of periods to forecast

### Customization
- Modify `utils/data_loader.py` to connect to your data sources
- Adjust forecasting parameters in `utils/forecasting_tools.py`
- Customize AI prompts in `utils/gpt_recommender.py`

## 📈 Example Use Cases

1. **Sales Analysis**: "Show me our top 5 products by revenue this quarter"
2. **Forecasting**: "Predict our sales for the next 3 months"
3. **AI Insights**: "What should I focus on to improve profitability?"
4. **Trend Analysis**: "When are our peak sales periods?"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in the notebooks folder
- Review the example data structure

---

**Built with ❤️ for business owners who want data-driven insights** 