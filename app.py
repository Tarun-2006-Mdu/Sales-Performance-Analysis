from flask import Flask, render_template, request
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


# ---------------------------------------------------------
# FIND COLUMN
# ---------------------------------------------------------

def find_column(df, candidates):

    for column in candidates:
        if column in df.columns:
            return column

    return None


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------------------------------
# ANALYZE DATASET
# ---------------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    # -----------------------------------------------------
    # LOAD CSV
    # -----------------------------------------------------

    try:
        df = pd.read_csv(
            filepath,
            encoding="latin1"
        )
    except Exception:
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            return f"Error reading CSV: {e}"

    # -----------------------------------------------------
    # CLEAN COLUMN NAMES
    # -----------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("/", "_", regex=False)
    )

    df.dropna(
        how="all",
        inplace=True
    )

    print("\nDetected columns:")
    print(df.columns.tolist())

    # -----------------------------------------------------
    # DETECT COLUMNS
    # -----------------------------------------------------

    sales_column = find_column(
        df,
        [
            "sales",
            "sale",
            "sales_amount",
            "total_sales",
            "sales_value",
            "revenue",
            "total_revenue",
            "revenue_amount",
            "amount",
            "total_amount",
            "net_sales"
        ]
    )

    quantity_column = find_column(
        df,
        [
            "quantity",
            "qty",
            "units",
            "units_sold",
            "unit_sold",
            "number_of_units",
            "items_sold"
        ]
    )

    price_column = find_column(
        df,
        [
            "price",
            "unit_price",
            "selling_price",
            "sale_price",
            "item_price",
            "product_price"
        ]
    )

    order_column = find_column(
        df,
        [
            "order_id",
            "orderid",
            "order_number",
            "order_no",
            "transaction_id",
            "transactionid",
            "invoice_id",
            "invoice_no",
            "id"
        ]
    )

    date_column = find_column(
        df,
        [
            "order_date",
            "orderdate",
            "date",
            "sale_date",
            "sales_date",
            "transaction_date",
            "purchase_date",
            "invoice_date",
            "created_at",
            "datetime",
            "timestamp"
        ]
    )

    product_column = find_column(
        df,
        [
            "product_name",
            "product",
            "product_title",
            "productname",
            "item_name",
            "item",
            "iphone_model",
            "model"
        ]
    )

    category_column = find_column(
        df,
        [
            "category",
            "product_category",
            "category_name",
            "product_type",
            "subcategory"
        ]
    )

    country_column = find_column(
        df,
        [
            "country",
            "country_name",
            "location_country"
        ]
    )

    state_column = find_column(
        df,
        [
            "state",
            "state_name",
            "region",
            "province"
        ]
    )

    customer_column = find_column(
        df,
        [
            "customer_name",
            "customer",
            "customer_id",
            "client_name",
            "buyer_name"
        ]
    )

    profit_column = find_column(
        df,
        [
            "profit",
            "profit_amount",
            "net_profit",
            "gross_profit"
        ]
    )

    payment_column = find_column(
        df,
        [
            "payment_method",
            "payment_type",
            "payment",
            "method"
        ]
    )

    # -----------------------------------------------------
    # CALCULATE SALES
    # -----------------------------------------------------

    calculated_sales = False

    # Case 1: Dataset already contains Sales / Revenue
    if sales_column:

        df["analysis_sales"] = (
            df[sales_column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace("€", "", regex=False)
            .str.strip()
        )

        df["analysis_sales"] = pd.to_numeric(
            df["analysis_sales"],
            errors="coerce"
        )

    # Case 2: Calculate Sales = Quantity × Price
    elif quantity_column and price_column:

        df[quantity_column] = pd.to_numeric(
            df[quantity_column],
            errors="coerce"
        )

        df[price_column] = (
            df[price_column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace("€", "", regex=False)
            .str.strip()
        )

        df[price_column] = pd.to_numeric(
            df[price_column],
            errors="coerce"
        )

        df["analysis_sales"] = (
            df[quantity_column]
            * df[price_column]
        )

        calculated_sales = True

    else:

        # No sales information available.
        # Use row count as a basic activity metric.
        df["analysis_sales"] = 0

    # Remove invalid sales rows
    df["analysis_sales"] = pd.to_numeric(
        df["analysis_sales"],
        errors="coerce"
    ).fillna(0)

    # -----------------------------------------------------
    # KPIs
    # -----------------------------------------------------

    total_sales = df["analysis_sales"].sum()

    # Quantity
    if quantity_column:

        df[quantity_column] = pd.to_numeric(
            df[quantity_column],
            errors="coerce"
        ).fillna(0)

        total_quantity = df[
            quantity_column
        ].sum()

    else:

        total_quantity = 0

    # Orders
    if order_column:

        total_orders = df[
            order_column
        ].nunique()

    else:

        total_orders = len(df)

    # Customers
    if customer_column:

        unique_customers = df[
            customer_column
        ].nunique()

    else:

        unique_customers = 0

    # Products
    if product_column:

        unique_products = df[
            product_column
        ].nunique()

    else:

        unique_products = 0

    # Countries
    if country_column:

        unique_countries = df[
            country_column
        ].nunique()

    else:

        unique_countries = 0

    # Average Order Value
    if total_orders > 0:

        average_order_value = (
            total_sales / total_orders
        )

    else:

        average_order_value = 0

    # -----------------------------------------------------
    # PROFIT
    # -----------------------------------------------------

    if profit_column:

        df[profit_column] = (
            df[profit_column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace("€", "", regex=False)
            .str.strip()
        )

        df[profit_column] = pd.to_numeric(
            df[profit_column],
            errors="coerce"
        ).fillna(0)

        total_profit = df[
            profit_column
        ].sum()

        profit_available = True

    else:

        total_profit = 0

        profit_available = False

    # -----------------------------------------------------
    # DATE CONVERSION
    # -----------------------------------------------------

    date_available = False

    if date_column:

        df[date_column] = pd.to_datetime(
            df[date_column],
            errors="coerce"
        )

        valid_dates = df[
            date_column
        ].dropna()

        if len(valid_dates) > 0:

            date_available = True

    # -----------------------------------------------------
    # MONTHLY SALES CHART
    # -----------------------------------------------------

    monthly_chart = False

    if date_available:

        date_df = df.dropna(
            subset=[date_column]
        ).copy()

        date_df["Month"] = (
            date_df[date_column]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_sales = (
            date_df
            .groupby("Month")["analysis_sales"]
            .sum()
            .reset_index()
        )

        if not monthly_sales.empty:

            plt.figure(
                figsize=(10, 5)
            )

            sns.lineplot(
                data=monthly_sales,
                x="Month",
                y="analysis_sales",
                marker="o"
            )

            plt.title(
                "Monthly Sales Trend"
            )

            plt.xlabel("Month")

            plt.ylabel("Sales")

            plt.xticks(
                rotation=45
            )

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    STATIC_FOLDER,
                    "monthly_sales.png"
                ),
                dpi=120
            )

            plt.close()

            monthly_chart = True

    # -----------------------------------------------------
    # PRODUCT SALES CHART
    # -----------------------------------------------------

    product_chart = False

    if product_column:

        product_data = (
            df.groupby(product_column)
            ["analysis_sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        if not product_data.empty:

            plt.figure(
                figsize=(10, 5)
            )

            sns.barplot(
                data=product_data,
                x=product_column,
                y="analysis_sales",
                hue=product_column,
                legend=False
            )

            plt.title(
                "Top 10 Products by Sales"
            )

            plt.xlabel("Product")

            plt.ylabel("Sales")

            plt.xticks(
                rotation=45
            )

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    STATIC_FOLDER,
                    "product_sales.png"
                ),
                dpi=120
            )

            plt.close()

            product_chart = True

    # -----------------------------------------------------
    # CATEGORY SALES CHART
    # -----------------------------------------------------

    category_chart = False

    if category_column:

        category_data = (
            df.groupby(category_column)
            ["analysis_sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        if not category_data.empty:

            plt.figure(
                figsize=(9, 5)
            )

            sns.barplot(
                data=category_data,
                x=category_column,
                y="analysis_sales",
                hue=category_column,
                legend=False
            )

            plt.title(
                "Sales by Category"
            )

            plt.xlabel("Category")

            plt.ylabel("Sales")

            plt.xticks(
                rotation=45
            )

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    STATIC_FOLDER,
                    "category_sales.png"
                ),
                dpi=120
            )

            plt.close()

            category_chart = True

    # -----------------------------------------------------
    # COUNTRY SALES CHART
    # -----------------------------------------------------

    country_chart = False

    if country_column:

        country_data = (
            df.groupby(country_column)
            ["analysis_sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        if not country_data.empty:

            plt.figure(
                figsize=(10, 5)
            )

            sns.barplot(
                data=country_data,
                x=country_column,
                y="analysis_sales",
                hue=country_column,
                legend=False
            )

            plt.title(
                "Top 10 Countries by Sales"
            )

            plt.xlabel("Country")

            plt.ylabel("Sales")

            plt.xticks(
                rotation=45
            )

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    STATIC_FOLDER,
                    "country_sales.png"
                ),
                dpi=120
            )

            plt.close()

            country_chart = True

    # -----------------------------------------------------
    # STATE / REGION SALES CHART
    # -----------------------------------------------------

    state_chart = False

    if state_column:

        state_data = (
            df.groupby(state_column)
            ["analysis_sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        if not state_data.empty:

            plt.figure(
                figsize=(10, 5)
            )

            sns.barplot(
                data=state_data,
                x=state_column,
                y="analysis_sales",
                hue=state_column,
                legend=False
            )

            plt.title(
                "Top 10 Regions by Sales"
            )

            plt.xlabel(
                "Region"
            )

            plt.ylabel(
                "Sales"
            )

            plt.xticks(
                rotation=45
            )

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    STATIC_FOLDER,
                    "state_sales.png"
                ),
                dpi=120
            )

            plt.close()

            state_chart = True

    # -----------------------------------------------------
    # PAYMENT METHOD CHART
    # -----------------------------------------------------

    payment_chart = False

    if payment_column:

        payment_data = (
            df.groupby(payment_column)
            ["analysis_sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .reset_index()
        )

        if not payment_data.empty:

            plt.figure(
                figsize=(8, 5)
            )

            sns.barplot(
                data=payment_data,
                x=payment_column,
                y="analysis_sales",
                hue=payment_column,
                legend=False
            )

            plt.title(
                "Sales by Payment Method"
            )

            plt.xlabel(
                "Payment Method"
            )

            plt.ylabel(
                "Sales"
            )

            plt.xticks(
                rotation=30
            )

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    STATIC_FOLDER,
                    "payment_sales.png"
                ),
                dpi=120
            )

            plt.close()

            payment_chart = True

    # -----------------------------------------------------
    # TOP PRODUCTS
    # -----------------------------------------------------

    top_products = []

    if product_column:

        top_product_data = (
            df.groupby(product_column)
            ["analysis_sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(5)
            .reset_index()
        )

        top_products = (
            top_product_data
            .values
            .tolist()
        )

    # -----------------------------------------------------
    # TOP COUNTRIES
    # -----------------------------------------------------

    top_countries = []

    if country_column:

        top_country_data = (
            df.groupby(country_column)
            ["analysis_sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(5)
            .reset_index()
        )

        top_countries = (
            top_country_data
            .values
            .tolist()
        )

    # -----------------------------------------------------
    # TOP CATEGORIES
    # -----------------------------------------------------

    top_categories = []

    if category_column:

        top_category_data = (
            df.groupby(category_column)
            ["analysis_sales"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(5)
            .reset_index()
        )

        top_categories = (
            top_category_data
            .values
            .tolist()
        )

    # -----------------------------------------------------
    # RENDER DASHBOARD
    # -----------------------------------------------------

    return render_template(
        "dashboard.html",

        total_sales=total_sales,

        total_profit=total_profit,

        profit_available=profit_available,

        total_quantity=total_quantity,

        total_orders=total_orders,

        average_order_value=average_order_value,

        unique_customers=unique_customers,

        unique_products=unique_products,

        unique_countries=unique_countries,

        calculated_sales=calculated_sales,

        monthly_chart=monthly_chart,

        product_chart=product_chart,

        category_chart=category_chart,

        country_chart=country_chart,

        state_chart=state_chart,

        payment_chart=payment_chart,

        top_products=top_products,

        top_countries=top_countries,

        top_categories=top_categories,

        sales_column=sales_column,

        quantity_column=quantity_column,

        price_column=price_column,

        date_column=date_column,

        product_column=product_column,

        category_column=category_column
    )


if __name__ == "__main__":
    app.run(debug=True)