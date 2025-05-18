import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# Load CSV into DataFrame
csv_path = "Amazon-Sale-Report.csv"
df = pd.read_csv(csv_path)

# Data Cleaning
df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%y', errors='coerce')

# Filter valid rows: Qty > 0 and Status not Cancelled, drop NaN Amount
df = df[(df['Qty'] > 0) & (~df['Status'].str.contains("Cancelled", na=False))]
df = df.dropna(subset=['Amount'])

# Rename columns for consistency (optional)
df.rename(columns={'Order ID': 'OrderID', 'ship-city': 'ShipCity'}, inplace=True)

# ---------- Analysis and Plotting ----------

# Helper function for INR formatting in bar charts
def plot_bar(data, x_col, y_col, title, xlabel, ylabel):
    plt.figure(figsize=(10,6))
    sns.barplot(x=data[x_col], y=data[y_col])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.gca().xaxis.set_major_formatter(mtick.StrMethodFormatter('₹{x:,.0f}'))
    plt.tight_layout()
    plt.show()

# 1. Top 10 Categories by Sales
top_categories = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).head(10).reset_index()
plot_bar(top_categories, 'Amount', 'Category', 'Top 10 Categories by Sales', 'Total Sales (INR)', 'Category')

# 2. Sales Trend Over Time
sales_over_time = df.groupby('Date')['Amount'].sum().reset_index()
plt.figure(figsize=(12,6))
plt.plot(sales_over_time['Date'], sales_over_time['Amount'])
plt.title('Sales Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales (INR)')
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('₹{x:,.0f}'))
plt.tight_layout()
plt.show()

# 3. Top 10 Cities by Sales
top_cities = df.groupby('ShipCity')['Amount'].sum().sort_values(ascending=False).head(10).reset_index()
plot_bar(top_cities, 'Amount', 'ShipCity', 'Top 10 Cities by Sales', 'Total Sales (INR)', 'City')

# 4. Top 10 SKUs by Quantity Sold
top_products = df.groupby('SKU')['Qty'].sum().sort_values(ascending=False).head(10).reset_index()
plt.figure(figsize=(10,6))
sns.barplot(x=top_products['Qty'], y=top_products['SKU'])
plt.title('Top 10 SKUs by Quantity Sold')
plt.xlabel('Quantity Sold')
plt.ylabel('SKU')
plt.tight_layout()
plt.show()

# 5. Total Cancelled Orders
cancelled_df = pd.read_csv("Amazon-Sale-Report.csv")
cancelled_orders = cancelled_df[cancelled_df['Status'].str.contains("Cancelled")]
print("Total Cancelled Orders:", len(cancelled_orders))

