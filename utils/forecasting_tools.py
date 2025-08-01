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

import pandas as pd
import numpy as np
from prophet import Prophet
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class BusinessForecaster:
    """Forecasting tools for business metrics using Prophet"""
    
    def __init__(self):
        self.models = {}
        self.forecasts = {}
        
    def prepare_data(self, sales_df, metric='revenue', period='D'):
        """Prepare data for Prophet forecasting"""
        
        # Group by date and aggregate
        if period == 'D':
            ts_data = sales_df.groupby(pd.Grouper(key='date', freq='D')).agg({
                'revenue': 'sum',
                'total_profit': 'sum',
                'transaction_id': 'count'
            }).reset_index()
        elif period == 'W':
            ts_data = sales_df.groupby(pd.Grouper(key='date', freq='W')).agg({
                'revenue': 'sum',
                'total_profit': 'sum',
                'transaction_id': 'count'
            }).reset_index()
        elif period == 'M':
            ts_data = sales_df.groupby(pd.Grouper(key='date', freq='ME')).agg({
                'revenue': 'sum',
                'total_profit': 'sum',
                'transaction_id': 'count'
            }).reset_index()
        
        # Rename columns for Prophet
        ts_data.columns = ['ds', 'revenue', 'profit', 'transactions']
        
        # Remove any NaN values
        ts_data = ts_data.dropna()
        
        # Select the metric to forecast
        if metric == 'revenue':
            forecast_data = ts_data[['ds', 'revenue']].copy()
            forecast_data.columns = ['ds', 'y']
        elif metric == 'profit':
            forecast_data = ts_data[['ds', 'profit']].copy()
            forecast_data.columns = ['ds', 'y']
        elif metric == 'transactions':
            forecast_data = ts_data[['ds', 'transactions']].copy()
            forecast_data.columns = ['ds', 'y']
        else:
            raise ValueError(f"Unknown metric: {metric}")
        
        return forecast_data, ts_data
    
    def train_model(self, data, metric='revenue', periods=30, seasonality_mode='multiplicative'):
        """Train Prophet model for forecasting"""
        
        # Configure Prophet model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode=seasonality_mode,
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10.0
        )
        
        # Add custom seasonality for business cycles
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        model.add_seasonality(name='quarterly', period=91.25, fourier_order=8)
        
        # Fit the model
        model.fit(data)
        
        # Make future predictions
        future = model.make_future_dataframe(periods=periods, freq='D')
        forecast = model.predict(future)
        
        # Store model and forecast
        self.models[metric] = model
        self.forecasts[metric] = forecast
        
        return model, forecast
    
    def get_forecast_summary(self, metric='revenue'):
        """Get summary statistics from forecast"""
        
        if metric not in self.forecasts:
            raise ValueError(f"No forecast available for {metric}")
        
        forecast = self.forecasts[metric]
        
        # Get the forecasted values (last periods)
        future_forecast = forecast.tail(30)  # Last 30 days
        
        summary = {
            'next_30_days_total': future_forecast['yhat'].sum(),
            'next_30_days_avg': future_forecast['yhat'].mean(),
            'next_30_days_min': future_forecast['yhat'].min(),
            'next_30_days_max': future_forecast['yhat'].max(),
            'trend_direction': 'increasing' if future_forecast['trend'].iloc[-1] > future_forecast['trend'].iloc[0] else 'decreasing',
            'confidence_lower': future_forecast['yhat_lower'].sum(),
            'confidence_upper': future_forecast['yhat_upper'].sum()
        }
        
        return summary
    
    def get_comprehensive_forecast_data(self, sales_df, periods=90):
        """Generate comprehensive forecasting data for AI training"""
        
        # Prepare data for multiple metrics
        metrics_data = {}
        forecasts_data = {}
        
        for metric in ['revenue', 'profit', 'transactions']:
            try:
                # Prepare data
                data, _ = self.prepare_data(sales_df, metric=metric, period='D')
                
                # Train model
                model, forecast = self.train_model(data, metric=metric, periods=periods)
                
                # Store data
                metrics_data[metric] = data
                forecasts_data[metric] = {
                    'model': model,
                    'forecast': forecast,
                    'summary': self.get_forecast_summary(metric)
                }
                
            except Exception as e:
                print(f"Error forecasting {metric}: {str(e)}")
                continue
        
        return metrics_data, forecasts_data
    
    def plot_forecast(self, metric='revenue', periods=30):
        """Create interactive forecast plot"""
        
        if metric not in self.models or metric not in self.forecasts:
            raise ValueError(f"No forecast available for {metric}")
        
        model = self.models[metric]
        forecast = self.forecasts[metric]
        
        # Create the plot
        fig = model.plot_components(forecast)
        
        # Convert to Plotly
        plotly_fig = go.Figure()
        
        # Historical data
        plotly_fig.add_trace(go.Scatter(
            x=forecast['ds'],
            y=forecast['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='blue')
        ))
        
        # Confidence intervals
        plotly_fig.add_trace(go.Scatter(
            x=forecast['ds'].tolist() + forecast['ds'].tolist()[::-1],
            y=forecast['yhat_upper'].tolist() + forecast['yhat_lower'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Interval'
        ))
        
        # Actual data (if available)
        if 'y' in forecast.columns:
            actual_data = forecast[forecast['y'].notna()]
            plotly_fig.add_trace(go.Scatter(
                x=actual_data['ds'],
                y=actual_data['y'],
                mode='markers',
                name='Actual',
                marker=dict(color='red', size=4)
            ))
        
        plotly_fig.update_layout(
            title=f'{metric.title()} Forecast - Next {periods} Days',
            xaxis_title='Date',
            yaxis_title=metric.title(),
            hovermode='x unified'
        )
        
        return plotly_fig
    
    def get_seasonal_patterns(self, metric='revenue'):
        """Analyze seasonal patterns in the data"""
        
        if metric not in self.models:
            raise ValueError(f"No model available for {metric}")
        
        model = self.models[metric]
        forecast = self.forecasts[metric]
        
        # Extract seasonal components
        seasonal_data = forecast[['ds', 'yearly', 'weekly', 'monthly']].copy()
        
        # Calculate peak periods
        yearly_peaks = seasonal_data.nlargest(5, 'yearly')
        weekly_peaks = seasonal_data.nlargest(5, 'weekly')
        
        patterns = {
            'yearly_peaks': yearly_peaks[['ds', 'yearly']].to_dict('records'),
            'weekly_peaks': weekly_peaks[['ds', 'weekly']].to_dict('records'),
            'avg_yearly_effect': seasonal_data['yearly'].mean(),
            'avg_weekly_effect': seasonal_data['weekly'].mean()
        }
        
        return patterns
    
    def forecast_multiple_metrics(self, sales_df, metrics=['revenue', 'profit', 'transactions'], periods=30):
        """Forecast multiple business metrics"""
        
        results = {}
        
        for metric in metrics:
            try:
                # Prepare data
                data, _ = self.prepare_data(sales_df, metric=metric)
                
                # Train model
                model, forecast = self.train_model(data, metric=metric, periods=periods)
                
                # Get summary
                summary = self.get_forecast_summary(metric)
                
                results[metric] = {
                    'model': model,
                    'forecast': forecast,
                    'summary': summary
                }
                
            except Exception as e:
                print(f"Error forecasting {metric}: {str(e)}")
                results[metric] = None
        
        return results

def create_forecast_dashboard(sales_df, periods=30):
    """Create a comprehensive forecast dashboard"""
    
    forecaster = BusinessForecaster()
    
    # Forecast multiple metrics
    forecasts = forecaster.forecast_multiple_metrics(sales_df, periods=periods)
    
    # Create summary dashboard
    summary_data = []
    for metric, result in forecasts.items():
        if result is not None:
            summary = result['summary']
            summary_data.append({
                'Metric': metric.title(),
                'Next 30 Days Total': f"${summary['next_30_days_total']:,.0f}",
                'Next 30 Days Avg': f"${summary['next_30_days_avg']:,.0f}",
                'Trend': summary['trend_direction'].title(),
                'Confidence Range': f"${summary['confidence_lower']:,.0f} - ${summary['confidence_upper']:,.0f}"
            })
    
    summary_df = pd.DataFrame(summary_data)
    
    return forecaster, forecasts, summary_df

def analyze_business_trends(sales_df):
    """Analyze business trends and patterns"""
    
    # Monthly trends
    monthly_data = sales_df.groupby(pd.Grouper(key='date', freq='ME')).agg({
        'revenue': 'sum',
        'total_profit': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    
    # Calculate month-over-month growth
    monthly_data['revenue_growth'] = monthly_data['revenue'].pct_change() * 100
    monthly_data['profit_growth'] = monthly_data['total_profit'].pct_change() * 100
    
    # Seasonal analysis
    sales_df['month'] = sales_df['date'].dt.month
    sales_df['day_of_week'] = sales_df['date'].dt.dayofweek
    
    monthly_avg = sales_df.groupby('month')['revenue'].mean()
    weekly_avg = sales_df.groupby('day_of_week')['revenue'].mean()
    
    # Best and worst periods
    best_month = monthly_avg.idxmax()
    worst_month = monthly_avg.idxmin()
    best_day = weekly_avg.idxmax()
    worst_day = weekly_avg.idxmin()
    
    trends = {
        'monthly_data': monthly_data,
        'best_month': best_month,
        'worst_month': worst_month,
        'best_day': best_day,
        'worst_day': worst_day,
        'avg_monthly_revenue': monthly_data['revenue'].mean(),
        'avg_monthly_profit': monthly_data['total_profit'].mean(),
        'revenue_volatility': monthly_data['revenue'].std() / monthly_data['revenue'].mean() * 100
    }
    
    return trends

if __name__ == "__main__":
    # Test forecasting
    from data_loader import load_or_generate_data
    
    sales_df, _ = load_or_generate_data()
    
    forecaster = BusinessForecaster()
    data, _ = forecaster.prepare_data(sales_df, metric='revenue')
    
    model, forecast = forecaster.train_model(data, periods=30)
    summary = forecaster.get_forecast_summary('revenue')
    
    print("Forecast Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}") 