from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Load dataset
    df = pd.read_csv(filepath, encoding='latin1')

    # Clean and prepare data
    df.dropna(inplace=True)
    df.columns = df.columns.str.strip()

    # KPIs
    total_sales = df['Sales'].sum()
    total_orders = df['Order_ID'].nunique()

    # Handle Profit column or simulate if missing
    if 'Profit' in df.columns:
        df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
        total_profit = df['Profit'].sum()
    else:
    # Simulate profit as 15% of sales
        df['Profit'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0) * 0.15
        total_profit = df['Profit'].sum()


    # Monthly Sales Trend
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Order_Date'])
    df['Month'] = df['Order_Date'].dt.to_period('M')
    monthly_sales = df.groupby('Month')['Sales'].sum().reset_index()
    monthly_sales['Month'] = monthly_sales['Month'].astype(str)

    plt.figure(figsize=(10,5))
    sns.lineplot(data=monthly_sales, x='Month', y='Sales', marker='o')
    plt.title('Monthly Sales Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()
    sales_path = os.path.join(STATIC_FOLDER, 'monthly_sales.png')
    plt.savefig(sales_path)
    plt.close()

    # Sales by Category
    category_sales = df.groupby('Category')['Sales'].sum().reset_index()
    plt.figure(figsize=(8,5))
    sns.barplot(data=category_sales, x='Category', y='Sales', palette='viridis')
    plt.title('Sales by Category')
    plt.tight_layout()
    cat_path = os.path.join(STATIC_FOLDER, 'category_sales.png')
    plt.savefig(cat_path)
    plt.close()

    #  Summary Insights
    top_states = df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(3).reset_index()
    top_products = df.groupby('Product_Name')['Sales'].sum().sort_values(ascending=False).head(3).reset_index()
    avg_order_value = total_sales / total_orders if total_orders != 0 else 0

    return render_template('dashboard.html',
                           total_sales=total_sales,
                           total_profit=total_profit,
                           total_orders=total_orders,
                           sales_img='static/monthly_sales.png',
                           cat_img='static/category_sales.png',
                           top_states=top_states.values.tolist(),
                           top_products=top_products.values.tolist(),
                           avg_order_value=avg_order_value)

if __name__ == '__main__':
    app.run(debug=True)
