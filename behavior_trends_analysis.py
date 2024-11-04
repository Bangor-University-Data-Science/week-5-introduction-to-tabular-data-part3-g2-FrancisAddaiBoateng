import pandas as pd

def import_data(file_path: str = "Customer_Behavior.xlsx") -> pd.DataFrame:
    """
    Load data from an Excel or CSV file into a pandas DataFrame.
    
    Args:
    file_path (str): Path to the data file. Defaults to "Customer_Behavior.xlsx".
    
    Returns:
    pd.DataFrame: DataFrame containing the imported data.
    
    Raises:
    ValueError: If the file extension is neither .xlsx nor .csv.
    """
    file_extension = file_path.split('.')[-1].lower()
    
    if file_extension == 'xlsx':
        return pd.read_excel(file_path)
    elif file_extension == 'csv':
        return pd.read_csv(file_path)
    else:
        raise ValueError("File format not supported. Use .xlsx or .csv files.")

# Usage example:
# customer_data = import_data()







def filter_data(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset by removing incomplete or invalid entries.

    Args:
    dataset (pd.DataFrame): The original DataFrame to be cleaned.

    Returns:
    pd.DataFrame: A cleaned DataFrame with valid entries only.

    This function removes rows with missing CustomerID and
    eliminates entries where Quantity or UnitPrice are negative.
    """
    # Eliminate rows with null CustomerID
    valid_data = dataset.dropna(subset=['CustomerID'])
    
    # Keep only rows with non-negative Quantity and UnitPrice
    mask = (valid_data['Quantity'] >= 0) & (valid_data['UnitPrice'] >= 0)
    cleaned_data = valid_data[mask]
    
    return cleaned_data

# Example implementation:
# Assuming we have a file named 'Customer_Behavior.xlsx'

# Import the dataset
raw_data = pd.read_excel("Customer_Behavior.xlsx")

# Apply the cleaning function
clean_data = filter_data(raw_data)

# Show the first few rows of the cleaned data
print(clean_data.head())






def loyalty_customers(df: pd.DataFrame, min_purchases: int) -> pd.DataFrame:
    """
    Identify loyal customers based on a minimum purchase threshold.

    Parameters:
    df (pd.DataFrame): The cleaned DataFrame.
    min_purchases (int): Minimum number of purchases required to qualify as a loyal customer.

    Returns:
    pd.DataFrame: A DataFrame listing customers who have made at least min_purchases transactions,
                  including the count of their purchases.
    """
    # Count the number of unique transactions for each customer
    customer_purchases = df.groupby('CustomerID')['InvoiceNo'].nunique().reset_index()
    customer_purchases.columns = ['CustomerID', 'PurchaseCount']

    # Filter customers who meet the minimum purchase threshold
    loyal_customers = customer_purchases[customer_purchases['PurchaseCount'] >= min_purchases]

    # Sort by purchase count in descending order
    loyal_customers = loyal_customers.sort_values('PurchaseCount', ascending=False)

    return loyal_customers

# Example usage:
# Assuming `df_filtered` is your cleaned DataFrame with relevant purchase data

# Define minimum purchases threshold
min_purchases = 5

# Identify loyal customers
loyal_customers_df = loyalty_customers(df_filtered, min_purchases)

# Display the resulting DataFrame of loyal customers
print(loyal_customers_df)





def quarterly_revenue(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Computes the aggregate revenue for each quarter.
    
    Args:
    transactions (pd.DataFrame): A DataFrame containing cleaned transaction records.
    
    Returns:
    pd.DataFrame: A DataFrame summarizing quarterly revenue with columns 'period' and 'revenue'.
    """
    # Convert InvoiceDate to datetime if not already
    transactions['InvoiceDate'] = pd.to_datetime(transactions['InvoiceDate'])

    # Calculate revenue per transaction
    transactions['TransactionRevenue'] = transactions['UnitPrice'] * transactions['Quantity']

    # Aggregate revenue by quarter
    quarterly_summary = (
        transactions.groupby(pd.Grouper(key='InvoiceDate', freq='Q'))
        ['TransactionRevenue'].sum()
        .reset_index()
    )

    # Rename columns for clarity
    quarterly_summary.columns = ['period', 'revenue']

    return quarterly_summary

# Example implementation:
# Assuming 'clean_data' is your preprocessed DataFrame

# Generate quarterly revenue report
revenue_report = quarterly_revenue(clean_data)

# Display the quarterly revenue summary
print(revenue_report)







def high_demand_products(sales_data: pd.DataFrame, limit: int) -> pd.DataFrame:
    """
    Determines the most popular products based on total quantity sold.
    
    Args:
    sales_data (pd.DataFrame): Cleaned sales transaction data.
    limit (int): Number of top-selling products to return.
    
    Returns:
    pd.DataFrame: A DataFrame containing the 'limit' most sold products, 
                  sorted by total quantity in descending order.
    """
    # Aggregate sales by product
    product_sales = sales_data.groupby('Description')['Quantity'].sum().reset_index()
    
    # Rename columns for better readability
    product_sales.columns = ['ProductName', 'TotalSold']
    
    # Sort products by total quantity sold and select top sellers
    bestsellers = (
        product_sales.sort_values('TotalSold', ascending=False)
        .head(limit)
        .reset_index(drop=True)
    )
    
    return bestsellers

# Example implementation:
# Assuming 'clean_data' is your preprocessed DataFrame

# Set the number of top products to retrieve
n_top_products = 10

# Get the list of best-selling products
top_products = high_demand_products(clean_data, n_top_products)

# Display the best-selling products
print(top_products)







def purchase_patterns(sales_data: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a product-wise summary of average purchase quantity and price.
    
    Args:
    sales_data (pd.DataFrame): Cleaned sales transaction data.
    
    Returns:
    pd.DataFrame: A summary DataFrame with columns 'item', 'mean_quantity', and 'mean_price'.
    """
    # Compute average quantity and price for each product
    product_analysis = sales_data.groupby('Description').agg({
        'Quantity': 'mean',
        'UnitPrice': 'mean'
    }).reset_index()
    
    # Rename columns for clarity
    product_analysis.columns = ['item', 'mean_quantity', 'mean_price']
    
    return product_analysis

# Example implementation:
# Assuming 'clean_data' is your preprocessed DataFrame

# Generate purchase pattern summary
product_summary = purchase_patterns(clean_data)

# Display the product purchase summary
print(product_summary)





def answer_conceptual_questions() -> dict:
    """
    Implement a function named answer_conceptual_questions that returns a dictionary with your answers
    to the multiple-choice questions.
    
    Returns:
    dict: A dictionary where each key is a question number (e.g., "Q1") and each value is a set of answer choices.
    """
    answers = {
        "Q1": {"A"},  # A) Negative or missing values could represent data entry errors, which affect calculations.
        "Q2": {"B"},  # B) Quarterly aggregation helps reveal seasonal trends.
        "Q3": {"C"},  # C) Loyal customers are easier to retain and less likely to churn.
        "Q4": {"A", "B"},  # A) To optimize pricing strategies based on demand. B) To predict future stock needs for each product.
        "Q5": {"A"}   # A) Counting the total quantity sold of each product.
    }
    return answers

# Example usage:
answers_dict = answer_conceptual_questions()
print(answers_dict)
