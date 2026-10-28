# 📊 Sales Performance Analysis

A **Flask-based Sales Performance Analysis Dashboard** that transforms raw sales data into meaningful business insights through data processing, KPI calculations, and interactive visualizations.

Built using Python, Flask, Pandas, Matplotlib, and Seaborn, this application allows users to upload CSV datasets and analyze sales performance across products, categories, time periods, geographic regions, and payment methods.

The project demonstrates the practical application of **Data Analytics, Data Visualization, and Web Development** to support data-driven business decisions.

---

## 🚀 Features

* 📁 **CSV Dataset Upload:** Upload sales datasets through a web interface.
* 🧹 **Data Preprocessing:** Normalize column names, remove completely empty rows, and process numeric sales values.
* 💰 **Total Sales Analysis:** Calculate total sales revenue from the uploaded dataset.
* 📈 **Sales Performance KPIs:** Analyze total sales, quantity sold, orders, average order value, customers, products, and countries.
* 🗓️ **Monthly Sales Trends:** Visualize sales performance over time using a line chart.
* 🛍️ **Product Performance:** Identify the top-selling products based on recorded sales.
* 🗂️ **Category Analysis:** Compare sales across product categories.
* 🌍 **Geographic Sales Analysis:** Analyze sales by country and state or region.
* 💳 **Payment Method Analysis:** Compare sales across different payment methods.
* 💹 **Profit Analysis:** Calculate total profit when profit data is available.
* 🔍 **Automatic Column Detection:** Recognize common column names used in sales datasets.
* 🧮 **Automatic Sales Calculation:** Calculate sales using quantity × price when a sales or revenue column is unavailable.
* 📊 **Automated Visualizations:** Generate charts based on the columns available in the uploaded dataset.
* 🏆 **Top Performer Summaries:** Display leading products, countries, and categories by sales.

---

## 🛠️ Technologies Used

| Technology | Purpose                                                   |
| ---------- | --------------------------------------------------------- |
| Python     | Core application logic                                    |
| Flask      | Web application framework                                 |
| Pandas     | Data loading, cleaning, and analysis                      |
| Matplotlib | Chart generation                                          |
| Seaborn    | Statistical data visualization                            |
| HTML5      | Web page structure                                        |
| CSS3       | Dashboard styling                                         |
| JavaScript | Client-side interactions, if implemented in the templates |
| CSV        | Input dataset format                                      |

---

## 📊 Dashboard Insights

The application generates several sales performance metrics and visualizations.

### 1. Key Performance Indicators (KPIs)

The dashboard calculates:

* **Total Sales:** Sum of the processed sales values.
* **Total Profit:** Sum of profit values, when a supported profit column exists.
* **Total Quantity Sold:** Sum of the available quantity values.
* **Total Orders:** Number of unique order identifiers, when available.
* **Average Order Value:** Total sales divided by the calculated order count.
* **Unique Customers:** Number of distinct customer identifiers, when available.
* **Unique Products:** Number of distinct products, when available.
* **Unique Countries:** Number of distinct countries, when available.

### 2. Monthly Sales Analysis

Visualizes sales totals grouped by month using the detected date column.

**Visualization:** Line chart.

**Purpose:** Identify changes in sales performance across different months.

### 3. Product Performance Analysis

Ranks products by their total recorded sales and displays the top 10 products in a bar chart.

**Purpose:** Identify products contributing the most to overall sales.

### 4. Category-wise Sales Analysis

Groups sales by product category and visualizes the leading categories.

**Purpose:** Understand which product categories contribute the most revenue.

### 5. Geographic Sales Analysis

Analyzes sales across countries and states or regions.

**Purpose:** Identify geographic markets with higher recorded sales.

### 6. Payment Method Analysis

Groups sales by payment method and compares their total values.

**Purpose:** Understand the distribution of recorded sales across payment methods.

### 7. Top Performer Summaries

Provides summary tables for the top five products, countries, and categories by sales.

---

## ⚙️ How It Works

The application follows a structured data analytics workflow:

1. **Upload Dataset:** The user uploads a sales CSV file through the web interface.
2. **Load Data:** Pandas reads the uploaded dataset and attempts to handle different CSV encodings.
3. **Clean Data:** Column names are normalized, and completely empty rows are removed.
4. **Detect Columns:** The application identifies sales, quantity, price, order, date, product, category, country, region, customer, profit, and payment fields.
5. **Calculate Sales:** Existing sales values are used when available; otherwise, sales are calculated from quantity and price when both fields exist.
6. **Calculate KPIs:** The application computes key sales metrics.
7. **Analyze Trends:** Data is grouped by time, product, category, geography, and payment method when the required columns are available.
8. **Generate Charts:** Matplotlib and Seaborn produce the relevant visualizations.
9. **Display Dashboard:** Flask passes the calculated metrics and chart availability indicators to the dashboard template.

---

## 📂 Project Structure

```text
Sales-Performance-Analysis/
│
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
│
├── templates/
│   ├── index.html             # Dataset upload page
│   └── dashboard.html         # Sales analytics dashboard
│
├── static/
│   ├── monthly_sales.png
│   ├── product_sales.png
│   ├── category_sales.png
│   ├── country_sales.png
│   ├── state_sales.png
│   └── payment_sales.png
│
└── uploads/                   # Uploaded CSV datasets
```

*Note: The `static/` and `uploads/` directories are created automatically when the application starts. Chart images are generated when the relevant data is available. The HTML templates and dependency file must be present in the project.*

---

## 📄 Dataset Requirements

The application accepts CSV datasets containing sales transaction data.

It recognizes several alternative column names, allowing it to work with differently structured datasets.

| Data Field     | Example Supported Column Names                                               |
| -------------- | ---------------------------------------------------------------------------- |
| Sales          | `sales`, `sales_amount`, `total_sales`, `revenue`, `total_revenue`, `amount` |
| Quantity       | `quantity`, `qty`, `units`, `units_sold`, `items_sold`                       |
| Price          | `price`, `unit_price`, `selling_price`, `product_price`                      |
| Order          | `order_id`, `order_number`, `transaction_id`, `invoice_id`                   |
| Date           | `order_date`, `date`, `sales_date`, `purchase_date`, `timestamp`             |
| Product        | `product_name`, `product`, `item_name`, `model`                              |
| Category       | `category`, `product_category`, `product_type`, `subcategory`                |
| Country        | `country`, `country_name`, `location_country`                                |
| State/Region   | `state`, `state_name`, `region`, `province`                                  |
| Customer       | `customer_name`, `customer`, `customer_id`, `client_name`                    |
| Profit         | `profit`, `profit_amount`, `net_profit`, `gross_profit`                      |
| Payment Method | `payment_method`, `payment_type`, `payment`, `method`                        |

### Example Dataset

```csv
order_id,order_date,product_name,category,quantity,price,country,state,customer_id,payment_method
ORD001,2026-01-05,Laptop,Electronics,2,50000,India,Tamil Nadu,C001,UPI
ORD002,2026-01-10,Headphones,Accessories,3,2000,India,Karnataka,C002,Credit Card
ORD003,2026-02-15,Keyboard,Accessories,5,1500,India,Tamil Nadu,C003,UPI
ORD004,2026-02-20,Monitor,Electronics,2,12000,India,Kerala,C001,Debit Card
ORD005,2026-03-12,Mouse,Accessories,4,800,India,Telangana,C004,Cash
```

This sample is illustrative. The application can process other CSV datasets with supported column names.

**Important:** If a sales or revenue column exists, its values are used for the sales calculations. Otherwise, the application calculates sales from quantity multiplied by price when both columns are available.

If neither sales values nor both quantity and price columns exist, the application assigns zero to its calculated sales field. Meaningful sales analysis therefore requires valid sales data or both quantity and price fields.

---

## 💻 Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

Install the following:

* Python 3.9 or later
* pip
* Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/Tarun-2006-Mdu/Sales-Performance-Analysis.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Sales-Performance-Analysis
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### Step 5: Install Dependencies

If a `requirements.txt` file exists:

```bash
pip install -r requirements.txt
```

Otherwise, install the required packages:

```bash
pip install Flask pandas matplotlib seaborn
```

### Step 6: Run the Application

```bash
python app.py
```

### Step 7: Open the Dashboard

Open your browser and navigate to:

```text
http://127.0.0.1:5000/
```

Upload a sales CSV dataset to generate the dashboard.

---

## 🎯 Use Cases

This project can support:

* Sales performance monitoring.
* Product and category performance analysis.
* Monthly revenue trend analysis.
* Geographic sales comparisons.
* Payment method analysis.
* Identification of top-performing products and markets.
* Exploratory Data Analysis (EDA).
* Business reporting and decision support.

---

## 🔮 Future Enhancements

Potential improvements include:

* Interactive visualizations using Plotly.
* Monthly, quarterly, and yearly performance comparisons.
* Sales growth and percentage change calculations.
* Profit margin analysis.
* Customer purchase trend analysis.
* Sales forecasting using Machine Learning.
* Date-range and category filters.
* Downloadable reports in CSV or PDF format.
* Database integration for historical sales records.
* Improved validation for missing and inconsistent data.
* Cloud deployment for online access.

---

## 👨‍💻 Author

**Tarunraj M.**

* GitHub: [Tarun-2006-Mdu](https://github.com/Tarun-2006-Mdu)
* Project Repository: [Sales-Performance-Analysis](https://github.com/Tarun-2006-Mdu/Sales-Performance-Analysis)

---

## 📜 License

This project can be distributed under the MIT License if an appropriate `LICENSE` file is added to the repository. Until then, no specific open-source license is declared.

---

## ⭐ Support

If you find this project useful for learning Python, Flask, Data Analytics, or Data Visualization, consider giving the repository a star!

**Built with Python, Flask, Pandas, Matplotlib, and Seaborn.**
