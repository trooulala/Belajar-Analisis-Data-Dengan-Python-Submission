import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import datetime as dt

# Function to load and preprocess data (this can be adjusted as per your dataset)
def load_data():
    # Assuming 'all_df' is your dataframe loaded here, e.g., from a CSV file or database
    # Replace this with actual data loading logic
    all_df = pd.read_csv('all_data.csv')  # Example CSV, replace as needed
    all_df['order_approved_at'] = pd.to_datetime(all_df['order_approved_at'])
    return all_df

# Function to calculate the monthly unique orders
def calculate_monthly_orders(all_df):
    group_param = all_df['order_approved_at'].dt.to_period("M")
    monthly_order = all_df.groupby(group_param).order_id.nunique().sort_values(ascending=False)
    return monthly_order

# Function to create the color list based on max orders
def get_bar_colors(monthly_order):
    max_orders = monthly_order.max()
    colors = ['red' if x == max_orders else 'blue' for x in monthly_order]
    return colors

# Function to plot the bar chart
def plot_monthly_orders(monthly_order, colors):
    # Create the figure object
    fig, ax = plt.subplots(figsize=(18, 6))
    
    # Plotting the bar chart on the axes (ax)
    sns.barplot(x=monthly_order.index.astype(str), y=monthly_order.values, palette=colors, ax=ax)
    
    # Remove labels and set title
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_title('Monthly Orders')
    
    # Tighten layout to avoid clipping
    plt.tight_layout()
    
    # Pass the figure to st.pyplot() to display
    st.pyplot(fig)  # Explicitly pass the figure

# Function to calculate customer count by city
def get_customer_by_city(all_df):
    # Group by city and count unique customers
    bycity_df = all_df.groupby(by="customer_city").customer_id.nunique().reset_index()
    bycity_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    return bycity_df

# Function to plot the bar chart
def plot_customer_by_city(bycity_df):
    # Create the figure and axis objects
    fig, ax = plt.subplots(figsize=(10, 5))  # Create figure object
    
    # Define custom colors for the bars
    colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    # Plot the bar chart with seaborn (using the ax object)
    sns.barplot(
        x="customer_count", 
        y="customer_city",
        data=bycity_df.sort_values(by="customer_count", ascending=False).head(),
        palette=colors_,
        ax=ax  # Pass the axes object to seaborn
    )
    
    # Add titles and remove axis labels
    ax.set_title("Most Customers by City", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    
    # Adjust tick labels for better readability
    ax.tick_params(axis='y', labelsize=12)
    
    # Use Streamlit to display the plot, passing the figure explicitly
    st.pyplot(fig)  # Pass the figure object explicitly

def plot_sales_by_payment(all_df):
    """
    Function to plot the sales by payment type as a pie chart.
    
    Parameters:
    - all_df: DataFrame containing the sales data
    """
    # Group data by payment type and calculate total sales
    sales_by_payment = all_df.groupby('payment_type')['price'].sum()

    # Set the figure size
    plt.figure(figsize=(8, 8))

    # Plot pie chart
    sales_by_payment.plot(kind='pie', autopct='%1.1f%%')

    # Add title
    plt.title('Most Used Payment Type', fontsize=16, fontweight='bold')

    # Hide the y-label for better aesthetics
    plt.ylabel('')

    # Adjust layout for better fitting
    plt.tight_layout()

    # Show the plot in Streamlit
    st.pyplot(plt)


# Function to plot the revenue charts (best and worst performing products)
def plot_best_and_worst_products(sum_order_items_df):
    # Create the figure and axes (2 subplots side by side)
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    
    # Define custom colors for the bars
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    # Best performing product (highest revenue)
    sns.barplot(x="price", y="product_category_name_english", 
                data=sum_order_items_df.head(), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Best Performing Product", loc="center", fontsize=15)
    ax[0].tick_params(axis='y', labelsize=12)
    
    # Worst performing product (lowest revenue)
    sns.barplot(x="price", y="product_category_name_english", 
                data=sum_order_items_df.sort_values(by="price", ascending=True).head(), 
                palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()  # Invert x-axis for the worst performing products
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Product", loc="center", fontsize=15)
    ax[1].tick_params(axis='y', labelsize=12)
    
    # Set the main title
    plt.suptitle("Highest and Lowest Revenue", fontsize=20)
    
    # Pass the figure to Streamlit's `st.pyplot()` to display the plot
    st.pyplot(fig)



# Streamlit UI setup
def main():
    st.title("Dashboard by M. Sulthon Sayid")

    # Load and preprocess data
    all_df = load_data()

    # Calculate monthly orders
    monthly_order = calculate_monthly_orders(all_df)

    # Generate color list for bars
    colors = get_bar_colors(monthly_order)

    # Display the plot
    st.write("### Summary of Monthly Orders")
    plot_monthly_orders(monthly_order, colors)

    # Display additional information
    st.write(monthly_order)

    st.write("### Most Used paymePayment Method")
    plot_sales_by_payment(all_df)

    # Calculate customer count by city
    bycity_df = get_customer_by_city(all_df)

    # Display the bar chart
    st.write("### Most Customers Order by City")
    plot_customer_by_city(bycity_df)

    st.write("### Highest and Lowest Revenue")
    sum_order_items_df = all_df.groupby('product_category_name_english').agg(
        price=('price', 'sum')
    ).reset_index()  # Replace 'order_items_price' with the actual column name for price
    
    # Display the bar chart for best and worst performing products
    plot_best_and_worst_products(sum_order_items_df)

# Ensure the app runs only when executed directly
if __name__ == "__main__":
    main()
