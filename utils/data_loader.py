import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os
import random

fake = Faker()

class BusinessDataGenerator:
    """Generate realistic business data for the CEO dashboard"""
    
    def __init__(self):
        self.products = [
            "Laptop Pro", "Smartphone X", "Wireless Headphones", "Tablet Air",
            "Gaming Console", "Smart Watch", "Bluetooth Speaker", "Camera DSLR",
            "Fitness Tracker", "Wireless Mouse", "Mechanical Keyboard", "Monitor 4K",
            "USB Drive", "Power Bank", "Webcam HD", "Microphone Pro", "Gaming Chair",
            "Desk Lamp", "Coffee Maker", "Blender"
        ]
        
        self.categories = {
            "Laptop Pro": "Electronics",
            "Smartphone X": "Electronics", 
            "Wireless Headphones": "Audio",
            "Tablet Air": "Electronics",
            "Gaming Console": "Gaming",
            "Smart Watch": "Wearables",
            "Bluetooth Speaker": "Audio",
            "Camera DSLR": "Photography",
            "Fitness Tracker": "Wearables",
            "Wireless Mouse": "Accessories",
            "Mechanical Keyboard": "Accessories",
            "Monitor 4K": "Electronics",
            "USB Drive": "Accessories",
            "Power Bank": "Accessories",
            "Webcam HD": "Accessories",
            "Microphone Pro": "Audio",
            "Gaming Chair": "Furniture",
            "Desk Lamp": "Furniture",
            "Coffee Maker": "Appliances",
            "Blender": "Appliances"
        }
        
        self.marketing_channels = ["Organic Search", "Paid Ads", "Social Media", "Email", "Direct", "Referral"]
        
    def generate_sales_data(self, days=365, base_sales=1000):
        """Generate realistic sales data with seasonality and trends"""
        
        # Create date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        sales_data = []
        
        for date in dates:
            # Base sales with some randomness
            daily_sales = base_sales + np.random.normal(0, 200)
            
            # Add seasonality (higher sales in December, lower in January)
            if date.month == 12:  # December
                daily_sales *= 1.8
            elif date.month == 1:  # January
                daily_sales *= 0.7
            elif date.month == 11:  # November (Black Friday)
                daily_sales *= 1.5
            elif date.month == 7:  # July (summer sales)
                daily_sales *= 1.2
                
            # Weekend effect
            if date.weekday() >= 5:  # Weekend
                daily_sales *= 1.1
                
            # Add some growth trend
            days_from_start = (date - start_date).days
            growth_factor = 1 + (days_from_start * 0.0005)  # 0.05% daily growth
            
            daily_sales *= growth_factor
            
            # Generate individual sales records
            num_transactions = max(1, int(daily_sales / 50))  # Average $50 per transaction
            
            for _ in range(num_transactions):
                product = random.choice(self.products)
                quantity = random.randint(1, 3)
                
                # Product-specific pricing
                base_price = self._get_product_price(product)
                price = base_price + np.random.normal(0, base_price * 0.1)  # 10% variance
                
                # Calculate costs and profit
                cost = price * random.uniform(0.4, 0.7)  # 30-60% margin
                profit = price - cost
                
                # Marketing channel
                channel = random.choices(
                    self.marketing_channels,
                    weights=[0.3, 0.2, 0.15, 0.1, 0.15, 0.1]  # Organic search is most common
                )[0]
                
                # Customer info
                customer_id = fake.uuid4()
                customer_name = fake.name()
                customer_email = fake.email()
                
                sales_data.append({
                    'date': date,
                    'product': product,
                    'category': self.categories[product],
                    'quantity': quantity,
                    'price': round(price, 2),
                    'cost': round(cost, 2),
                    'profit': round(profit, 2),
                    'revenue': round(price * quantity, 2),
                    'total_cost': round(cost * quantity, 2),
                    'total_profit': round(profit * quantity, 2),
                    'marketing_channel': channel,
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'customer_email': customer_email,
                    'transaction_id': fake.uuid4()
                })
        
        return pd.DataFrame(sales_data)
    
    def generate_inventory_data(self):
        """Generate current inventory data"""
        
        inventory_data = []
        
        for product in self.products:
            base_price = self._get_product_price(product)
            
            # Generate realistic inventory levels
            current_stock = random.randint(10, 200)
            reorder_point = max(5, int(current_stock * 0.2))
            max_stock = current_stock + random.randint(50, 100)
            
            # Calculate days of inventory
            avg_daily_sales = random.randint(2, 8)
            days_of_inventory = current_stock / avg_daily_sales if avg_daily_sales > 0 else 999
            
            inventory_data.append({
                'product': product,
                'category': self.categories[product],
                'current_stock': current_stock,
                'reorder_point': reorder_point,
                'max_stock': max_stock,
                'avg_daily_sales': avg_daily_sales,
                'days_of_inventory': round(days_of_inventory, 1),
                'unit_cost': round(base_price * random.uniform(0.4, 0.7), 2),
                'unit_price': round(base_price, 2),
                'last_restocked': fake.date_between(start_date='-30d', end_date='today'),
                'supplier': fake.company()
            })
        
        return pd.DataFrame(inventory_data)
    
    def _get_product_price(self, product):
        """Get base price for a product"""
        price_ranges = {
            "Laptop Pro": (800, 1500),
            "Smartphone X": (600, 1000),
            "Wireless Headphones": (50, 200),
            "Tablet Air": (400, 800),
            "Gaming Console": (300, 500),
            "Smart Watch": (200, 400),
            "Bluetooth Speaker": (30, 100),
            "Camera DSLR": (500, 1200),
            "Fitness Tracker": (50, 150),
            "Wireless Mouse": (20, 60),
            "Mechanical Keyboard": (80, 200),
            "Monitor 4K": (300, 600),
            "USB Drive": (10, 50),
            "Power Bank": (20, 80),
            "Webcam HD": (40, 120),
            "Microphone Pro": (60, 150),
            "Gaming Chair": (150, 300),
            "Desk Lamp": (30, 80),
            "Coffee Maker": (80, 200),
            "Blender": (40, 120)
        }
        
        min_price, max_price = price_ranges.get(product, (50, 100))
        return random.uniform(min_price, max_price)

def load_or_generate_data():
    """Load existing data or generate new data if it doesn't exist"""
    
    data_dir = "data"
    sales_file = os.path.join(data_dir, "sales_data.csv")
    inventory_file = os.path.join(data_dir, "inventory_data.csv")
    
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate sales data if it doesn't exist
    if not os.path.exists(sales_file):
        print("Generating sales data...")
        generator = BusinessDataGenerator()
        sales_df = generator.generate_sales_data()
        sales_df.to_csv(sales_file, index=False)
        print(f"Sales data saved to {sales_file}")
    else:
        print("Loading existing sales data...")
        sales_df = pd.read_csv(sales_file)
        sales_df['date'] = pd.to_datetime(sales_df['date'])
    
    # Generate inventory data if it doesn't exist
    if not os.path.exists(inventory_file):
        print("Generating inventory data...")
        generator = BusinessDataGenerator()
        inventory_df = generator.generate_inventory_data()
        inventory_df.to_csv(inventory_file, index=False)
        print(f"Inventory data saved to {inventory_file}")
    else:
        print("Loading existing inventory data...")
        inventory_df = pd.read_csv(inventory_file)
        inventory_df['last_restocked'] = pd.to_datetime(inventory_df['last_restocked'])
    
    return sales_df, inventory_df

def get_kpis(sales_df):
    """Calculate key performance indicators"""
    
    # Date range
    latest_date = sales_df['date'].max()
    start_date = latest_date - timedelta(days=30)
    
    # Filter for last 30 days
    recent_sales = sales_df[sales_df['date'] >= start_date]
    
    # Previous 30 days for comparison
    prev_start = start_date - timedelta(days=30)
    prev_sales = sales_df[(sales_df['date'] >= prev_start) & (sales_df['date'] < start_date)]
    
    kpis = {
        'total_revenue_30d': recent_sales['revenue'].sum(),
        'total_profit_30d': recent_sales['total_profit'].sum(),
        'total_transactions_30d': len(recent_sales),
        'avg_order_value_30d': recent_sales['revenue'].sum() / len(recent_sales) if len(recent_sales) > 0 else 0,
        'profit_margin_30d': (recent_sales['total_profit'].sum() / recent_sales['revenue'].sum() * 100) if recent_sales['revenue'].sum() > 0 else 0,
        
        # Growth metrics
        'revenue_growth': ((recent_sales['revenue'].sum() - prev_sales['revenue'].sum()) / prev_sales['revenue'].sum() * 100) if prev_sales['revenue'].sum() > 0 else 0,
        'profit_growth': ((recent_sales['total_profit'].sum() - prev_sales['total_profit'].sum()) / prev_sales['total_profit'].sum() * 100) if prev_sales['total_profit'].sum() > 0 else 0,
        
        # Top products
        'top_product': recent_sales.groupby('product')['revenue'].sum().idxmax() if len(recent_sales) > 0 else "N/A",
        'top_category': recent_sales.groupby('category')['revenue'].sum().idxmax() if len(recent_sales) > 0 else "N/A",
        
        # Marketing performance
        'best_channel': recent_sales.groupby('marketing_channel')['revenue'].sum().idxmax() if len(recent_sales) > 0 else "N/A"
    }
    
    return kpis

def get_time_series_data(sales_df, period='D'):
    """Get time series data for forecasting"""
    
    # Group by date and period
    ts_data = sales_df.groupby(pd.Grouper(key='date', freq=period)).agg({
        'revenue': 'sum',
        'total_profit': 'sum',
        'transaction_id': 'count'
    }).reset_index()
    
    ts_data.columns = ['ds', 'y', 'profit', 'transactions']
    
    # Remove any NaN values
    ts_data = ts_data.dropna()
    
    return ts_data

if __name__ == "__main__":
    # Test data generation
    sales_df, inventory_df = load_or_generate_data()
    print(f"Generated {len(sales_df)} sales records")
    print(f"Generated {len(inventory_df)} inventory items")
    
    kpis = get_kpis(sales_df)
    print("\nKey Performance Indicators:")
    for key, value in kpis.items():
        print(f"{key}: {value}") 