import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

def load_data(file_path):
    """
    Load dataset from a CSV file.
    """
    return pd.read_csv(file_path)

def plot_histogram(df, column, save_path):
    """
    Plot a histogram for a given column in the DataFrame and save the plot.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column], kde=True)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.savefig(save_path)
    plt.close()

def plot_scatter(df, x_col, y_col, save_path):
    """
    Plot a scatter plot for two columns in the DataFrame and save the plot.
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_col, y=y_col)
    plt.title(f'Scatter Plot of {x_col} vs {y_col}')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.savefig(save_path)
    plt.close()

def plot_pairplot(df, save_path):
    """
    Plot pairplot for the DataFrame and save the plot.
    """
    g = sns.pairplot(df)
    g.savefig(save_path)
    plt.close()

def plot_correlation_heatmap(df, save_path):
    """
    Plot a heatmap of correlations between numerical columns and save the plot.
    """
    corr = df.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.savefig(save_path)
    plt.close()

def plot_pie_chart(df, column, save_path):
    """
    Plot a pie chart for a categorical column and save the plot.
    """
    plt.figure(figsize=(10, 6))
    plt.pie(df[column].value_counts(), labels=df[column].unique(), autopct='%1.1f%%')
    plt.title(f'Pie Chart of {column}')
    plt.savefig(save_path)
    plt.close()

def auto_generate_plots(df):
    """
    Automatically generate plots based on the dataset content and save them as files.
    """
    numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    
    plot_paths = []

    if numerical_cols:
        for col in numerical_cols:
            plot_path = f'histogram_{col}.png'
            plot_histogram(df, col, plot_path)
            plot_paths.append(plot_path)
    
    if len(numerical_cols) > 1:
        for i in range(len(numerical_cols)):
            for j in range(i + 1, len(numerical_cols)):
                plot_path = f'scatter_{numerical_cols[i]}vs{numerical_cols[j]}.png'
                plot_scatter(df, numerical_cols[i], numerical_cols[j], plot_path)
                plot_paths.append(plot_path)
    
    if numerical_cols:
        plot_path = 'correlation_heatmap.png'
        plot_correlation_heatmap(df, plot_path)
        plot_paths.append(plot_path)
    
    if numerical_cols:
        plot_path = 'pairplot.png'
        plot_pairplot(df, plot_path)
        plot_paths.append(plot_path)
    
    if categorical_cols:
        for col in categorical_cols:
            plot_path = f'pie_chart_{col}.png'
            plot_pie_chart(df, col, plot_path)
            plot_paths.append(plot_path)
    
    return plot_paths

def generate_pdf_report(plot_paths, output_filename):
    """
    Generate a PDF report with the plots.
    """
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, height - 100, "Data Visualization Report")

    y_position = height - 150

    for plot_path in plot_paths:
        c.drawImage(plot_path, 100, y_position, width=400, height=300)
        y_position -= 350
        
        if y_position < 100:  # Check if we need to start a new page
            c.showPage()
            c.setFont("Helvetica-Bold", 18)
            c.drawString(100, height - 100, "Data Visualization Report")
            y_position = height - 150
    
    c.save()

def main():
    # Load dataset
    file_path = input("Enter the path to the dataset (CSV file): ")
    df = load_data(file_path)
    
    # Display column names
    print("Columns available in the dataset:")
    print(df.columns)

    # Choose visualization option
    print("\nChoose an option:")
    print("1. Auto-generate all plots")
    print("2. Generate specific plots")
    print("3. Generate PDF report")
    print("4. Generate inferences")


    choice = input("Enter the number of your choice: ")

    if choice == '1':
        auto_generate_plots(df)
    elif choice == '2':
        print("\nChoose specific plots to generate:")
        print("1. Histogram")
        print("2. Scatter Plot")
        print("3. Pairplot")
        print("4. Correlation Heatmap")
        print("5. Pie Chart")
        
        specific_choice = input("Enter the number of your choice: ")
        
        if specific_choice == '1':
            column = input("Enter the column name for the histogram: ")
            if column in df.columns:
                plot_histogram(df, column, f'histogram_{column}.png')
            else:
                print("Column not found.")
        
        elif specific_choice == '2':
            x_col = input("Enter the column name for the x-axis: ")
            y_col = input("Enter the column name for the y-axis: ")
            if x_col in df.columns and y_col in df.columns:
                plot_scatter(df, x_col, y_col, f'scatter_{x_col}vs{y_col}.png')
            else:
                print("One or both columns not found.")
        
        elif specific_choice == '3':
            plot_pairplot(df, 'pairplot.png')
        
        elif specific_choice == '4':
            plot_correlation_heatmap(df, 'correlation_heatmap.png')
        
        elif specific_choice == '5':
            column = input("Enter the column name for the pie chart: ")
            if column in df.columns:
                plot_pie_chart(df, column, f'pie_chart_{column}.png')
            else:
                print("Column not found.")
        
        else:
            print("Invalid choice.")
    
    elif choice == '3':
        plot_paths = auto_generate_plots(df)
        generate_pdf_report(plot_paths, 'data_visualization_report.pdf')
        print("PDF report generated: data_visualization_report.pdf")
        
        # Optionally, remove the image files after generating the report
        for plot_path in plot_paths:
            os.remove(plot_path)

    else:
        print("Invalid choice.")

if _name_ == "_main_":
    main()