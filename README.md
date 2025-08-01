# 🚀 CEO Dashboard - AI-Powered Business Intelligence

A comprehensive business intelligence dashboard designed for CEOs and business owners, featuring AI-powered insights, advanced forecasting, and interactive analytics.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 📸 Screenshots

### 🏠 Main Dashboard
![Main Dashboard](screenshots/Screen%20Shot%202025-08-01%20at%2018.59.35.png)

### 📊 Business Analytics
![Business Analytics](screenshots/Screen%20Shot%202025-08-01%20at%2018.59.46.png)

### 🤖 AI-Powered Insights
![AI Insights](screenshots/Screen%20Shot%202025-08-01%20at%2019.00.07.png)

## 🌟 Features

### 📊 **Business Analytics**
- **Real-time KPI Dashboard** - Revenue, profit, transactions, and growth metrics
- **Interactive Charts** - Revenue trends, product performance, category analysis
- **Marketing Channel Analytics** - Campaign effectiveness and ROI tracking
- **Inventory Management** - Stock levels, reorder points, and supply chain insights

### 🔮 **Advanced Forecasting**
- **Multi-metric Forecasting** - Revenue, profit, and transaction predictions
- **Prophet Time Series Models** - 90-day projections with confidence intervals
- **Seasonal Trend Analysis** - Peak periods and cyclical patterns
- **Interactive Forecast Charts** - Historical data with future projections

### 🤖 **AI-Powered Intelligence**
- **Multi-AI Model Support** - DeepSeek R1T2 Chimera, OpenAI, Ollama, OpenRouter
- **Strategic Recommendations** - AI-generated business insights and actions
- **Risk Assessment** - Market volatility and threat analysis
- **Growth Opportunities** - Market expansion and optimization strategies
- **Natural Language Queries** - Ask business questions in plain English

### 🎨 **Modern UI/UX**
- **Dark Mode Design** - Professional and easy on the eyes
- **Responsive Layout** - Works on desktop and mobile devices
- **Interactive Filters** - Date ranges, categories, and product selection
- **Real-time Updates** - Live data refresh and dynamic charts

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Plotly, Altair
- **Backend**: Python 3.8+, Pandas, NumPy
- **AI/ML**: Prophet, Scikit-learn, LangChain
- **AI Models**: DeepSeek R1T2 Chimera, OpenAI GPT, Ollama, OpenRouter
- **Data Visualization**: Plotly, Matplotlib, Seaborn
- **Data Generation**: Faker (synthetic business data)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ceo-dashboard.git
   cd ceo-dashboard
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   python run_dashboard.py
   ```

5. **Access the dashboard**
   Open your browser and go to: `http://localhost:8501`

## 🚀 Usage

### Dashboard Tabs

1. **📊 Business Overview**
   - KPI metrics and performance indicators
   - Revenue and profit trends
   - Recent transactions

2. **🔮 Business Forecasting**
   - Generate forecasts for revenue, profit, transactions
   - Interactive forecast charts
   - Business trend analysis

3. **🤖 AI-Powered Insights**
   - Configure AI models (DeepSeek, OpenAI, etc.)
   - Generate strategic recommendations
   - Comprehensive forecast analysis
   - Natural language business queries

4. **📦 Inventory Management**
   - Stock levels and reorder points
   - Product performance analysis
   - Supply chain insights

5. **💬 Business Intelligence Chat**
   - Ask questions about your business data
   - Get AI-powered answers and insights

### AI Model Configuration

The dashboard supports multiple AI models:

- **DeepSeek R1T2 Chimera** (Recommended) - Free, powerful reasoning
- **OpenAI GPT** - Industry standard, reliable
- **Ollama** - Local models, privacy-focused
- **OpenRouter** - Access to multiple models

## 📁 Project Structure

```
ceo-dashboard/
├── 📁 app/                          # Main application files
│   ├── dashboard.py                  # Main Streamlit dashboard
│   └── ai_assistant.py              # AI chatbot assistant
│
├── 📁 utils/                        # Core utility modules
│   ├── data_loader.py               # Data generation and loading
│   ├── forecasting_tools.py         # Prophet forecasting models
│   ├── ai_recommender.py            # Multi-AI model recommender
│   └── gpt_recommender.py          # Legacy GPT integration
│
├── 📁 data/                         # Business data files
│   ├── sales_data.csv               # Sales transaction data
│   └── inventory_data.csv           # Inventory management data
│
├── 📁 notebooks/                    # Jupyter analysis notebooks
│   ├── exploration.ipynb            # Data exploration
│   ├── forecasting.ipynb            # Forecasting analysis
│   └── business_forecasting_analysis.ipynb  # Comprehensive analysis
│
├── requirements.txt                  # Python dependencies
├── setup.py                         # Project setup automation
├── run_dashboard.py                 # Dashboard launcher
└── README.md                        # Project documentation
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

### AI Model Setup

1. **DeepSeek R1T2 Chimera** (Recommended)
   - Free model with excellent reasoning capabilities
   - No API key required for basic usage
   - Supports long-context analysis

2. **OpenAI GPT**
   - Requires OpenAI API key
   - Reliable and well-supported
   - Good for general business analysis

3. **Ollama**
   - Local models for privacy
   - Requires Ollama installation
   - Supports various open-source models

## 📈 Features in Detail

### Business Forecasting
- **Multi-metric Analysis**: Revenue, profit, and transaction forecasting
- **Confidence Intervals**: Statistical uncertainty in predictions
- **Seasonal Patterns**: Identify cyclical business trends
- **Interactive Charts**: Zoom, pan, and explore forecast data

### AI-Powered Insights
- **Strategic Recommendations**: Actionable business advice
- **Risk Assessment**: Market volatility and threat analysis
- **Growth Opportunities**: Market expansion strategies
- **Operational Insights**: Resource allocation and optimization

### Data Analytics
- **Real-time KPIs**: Live business metrics
- **Product Performance**: Top-selling items and trends
- **Marketing ROI**: Campaign effectiveness analysis
- **Inventory Optimization**: Stock level management

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for the amazing web framework
- **Prophet** for time series forecasting
- **DeepSeek AI** for the powerful R1T2 Chimera model
- **OpenAI** for GPT models
- **Plotly** for interactive visualizations

## 📞 Support

If you have any questions or need help:
- Open an issue on GitHub
- Check the documentation in the notebooks
- Review the code comments for implementation details

---

**Built with ❤️ by Alae-Eddine Dahane**

*Empowering business leaders with AI-powered intelligence and data-driven insights.* 