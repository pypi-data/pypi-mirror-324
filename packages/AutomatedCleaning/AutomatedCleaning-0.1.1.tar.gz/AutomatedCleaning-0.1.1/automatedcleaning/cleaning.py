import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
from spellchecker import SpellChecker
import warnings
import math
import os
import missingno as msno


import difflib



# Suppress all warnings
warnings.filterwarnings('ignore')


def load_data(file_path):
    """Load data from different formats."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.tsv'):
        return pd.read_csv(file_path, sep='\t')
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    elif file_path.endswith('.parquet'):
        return pd.read_parquet(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

def check_data_types(df):
    """Check the data types of columns."""
    return df.dtypes


def replace_dash_and_symbols_with_nan(df):
    # Replace '-' with NaN
    df.replace('-', np.nan, inplace=True)
    
    # Replace '$' and '₹' with nothing (remove them)
    df.replace({'\$': '', '₹': ''}, regex=True, inplace=True)
    
    return df

def fix_incorrect_data_types(df):
    for col in df.columns:
        try:
            # Attempt to convert column to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')
        except Exception as e:
            # Log any errors for debugging purposes
            print(f"Could not convert column {col} due to: {e}")
    return df

def fix_column_names(df):
    """Fix column names (strip spaces, lowercase, replace spaces with underscores)."""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df


def fix_spelling_errors_in_columns(df):
    """Fix spelling errors in column names by interacting with the user."""
    corrected_columns = {}

    for col in df.columns:
        print(f"Processing column name: {col}")
        suggestion = difflib.get_close_matches(col, df.columns, n=1, cutoff=0.8)

        if suggestion and suggestion[0] != col:
            print(f"Did you mean: {suggestion[0]}?")

        user_input = input(f"Enter the correct spelling for column '{col}' (or press Enter to skip): ").strip()

        if user_input:
            corrected_columns[col] = user_input
        else:
            corrected_columns[col] = col

    # Rename columns
    df.rename(columns=corrected_columns, inplace=True)

    return df

def fix_spelling_errors_in_categorical(df):
    """Fix spelling errors in categorical columns by interacting with the user."""
    for col in df.select_dtypes(include=['object']).columns:
        print(f"Processing column: {col}")
        unique_values = df[col].dropna().unique()
        corrected_values = {}

        for value in unique_values:
            if not value.isalpha():
                # Skip if the value is numeric or contains special characters
                continue

            print(f"Potential spelling error detected: {value}")
            suggestion = difflib.get_close_matches(value, unique_values, n=1, cutoff=0.8)

            if suggestion:
                print(f"Did you mean: {suggestion[0]}?")

            user_input = input(f"Enter the correct spelling for '{value}' (or press Enter to skip): ").strip()

            if user_input:
                corrected_values[value] = user_input
            else:
                corrected_values[value] = value

        # Apply corrections to the column
        df[col] = df[col].map(corrected_values).fillna(df[col])

    return df


import numpy as np

def handle_negative_values(df):
    """Handle negative values by printing column names with negatives and replacing them with absolute values."""
    
    # Iterate over each numerical column
    for col in df.select_dtypes(include=[np.number]).columns:
        # Check the minimum value of the column
        min_val = df[col].min()
        
        # If the minimum value is negative, print the column name
        if min_val < 0:
            print(f"Column '{col}' contains negative values.")
            
            # Apply absolute function to the column
            df[col] = df[col].abs()
    
    return df

def handle_missing_values(df):
    """
    Handle missing values using user-selected imputation method:
    - Simple Imputation (Mean for numerical, Mode for categorical)
    - KNN-based Imputation (Only for numerical columns)
    """

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate and save missing values plot
    plt.figure(figsize=(10, 6))
    msno.bar(df)
    plot_path = os.path.join(output_dir, "missing_values_plot.png")
    plt.savefig(plot_path)
    print(f"Missing values plot saved as '{plot_path}'")

    
    choice = input("Choose imputation method: (1) Simple (mean/mode) or (2) KNN: ")
    
    if choice == '1':
        # Simple Imputation
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                mean_value = df[col].mean()
                print(f"Column '{col}' contains {missing_count} missing values. Imputing with mean: {mean_value}")
                df[col].fillna(mean_value, inplace=True)
        
        categorical_cols = df.select_dtypes(include=[object, 'category']).columns
        for col in categorical_cols:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                mode_value = df[col].mode()[0]  # mode()[0] gets the most frequent value
                print(f"Column '{col}' contains {missing_count} missing values. Imputing with mode: {mode_value}")
                df[col].fillna(mode_value, inplace=True)
        
    elif choice == '2':
        # KNN Imputation (Only for numerical columns)
        num_df = df.select_dtypes(include=[np.number])
        imputer = KNNImputer(n_neighbors=5)
        df[num_df.columns] = imputer.fit_transform(num_df)
        print("KNN imputation applied to numerical columns.")
        
        # Mode imputation for categorical columns
        categorical_cols = df.select_dtypes(include=[object, 'category']).columns
        for col in categorical_cols:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                mode_value = df[col].mode()[0]
                print(f"Column '{col}' contains {missing_count} missing values. Imputing with mode: {mode_value}")
                df[col].fillna(mode_value, inplace=True)
    
    else:
        print("Invalid choice. Please enter 1 or 2.")
    
    return df

def handle_duplicates(df):
    """Check for duplicate rows, print them, and then remove them."""
    # Check for duplicate rows
    duplicates = df[df.duplicated()]
    
    # If there are any duplicate rows, print them
    if not duplicates.empty:
        print("Duplicate rows found: So we are dropping the duplicate rows")
        print(duplicates)
    
    # Remove duplicate rows
    df_cleaned = df.drop_duplicates()
    
    return df_cleaned

def check_outliers(df):
    """Check for outliers using IQR method."""
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    outliers = {}
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers[col] = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    return outliers

def remove_outliers(df):
    """Remove outliers using IQR method."""
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

def check_data_imbalance(df, target_col):
    """Check for class imbalance in the target column."""
    return df[target_col].value_counts()

def handle_imbalance(df, target_col):
    """Handle data imbalance by oversampling or undersampling."""
    from imblearn.over_sampling import SMOTE
    from imblearn.under_sampling import RandomUnderSampler
    
    smote = SMOTE()
    X = df.drop(columns=[target_col])
    y = df[target_col]
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    return pd.concat([X_resampled, y_resampled], axis=1)

def check_skewness(df):
    """Check skewness in numerical columns."""
    return df.skew()

def fix_skewness(df):
    """Fix skewness in numerical columns using log transformation."""
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        if df[col].skew() > 1:
            df[col] = np.log1p(df[col])
    return df

def check_multicollinearity(df, threshold=0.7):
    """Check for multicollinearity using correlation matrix and remove highly correlated features."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    num_df = df.select_dtypes(include=['int', 'float'])
    correlation_matrix = num_df.corr()
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Matrix")
    
    plot_path = os.path.join(output_dir, "correlation_matrix.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Correlation matrix plot saved as '{plot_path}'")
    
    # Identify highly correlated features and remove them
    to_drop = set()
    for i in range(len(correlation_matrix.columns)):
        for j in range(i):  # Avoid duplicate pairs
            if abs(correlation_matrix.iloc[i, j]) > threshold:
                col_to_drop = correlation_matrix.columns[i]
                to_drop.add(col_to_drop)
    
    if to_drop:
        print(f"Dropping highly correlated columns: {', '.join(to_drop)}")
        df.drop(columns=to_drop, inplace=True)
    else:
        print("No highly correlated feature pairs found above the threshold.")
    
    return df



def check_cardinality(df):
    """
    Check the cardinality (number of unique values) of categorical columns.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        
    Returns:
        pd.Series: A series with column names as index and their cardinality as values.
    """
    # Select only categorical columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    print(f"Categorical columns found: {list(categorical_cols)}")
    
    # Calculate cardinality
    cardinality = df[categorical_cols].nunique()
    print(f"Cardinality of categorical columns:\n{cardinality}")
    
    return cardinality


def save_cleaned_data(df, file_name="cleaned_data.csv"):
    """Save cleaned DataFrame to a CSV file."""
    df.to_csv(file_name, index=False)
    print(f"Cleaned data saved to {file_name}")


def save_boxplots(df, output_filename="output/boxplots.png"):
    """
    Create boxplots for numerical columns in a DataFrame and save the plot as a PNG file.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        output_filename (str): The filename for saving the boxplots image.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    # Select numerical columns
    numerical_cols = df.select_dtypes(include=['number']).columns
    print(f"Numerical columns found: {list(numerical_cols)}")
    
    if numerical_cols.empty:
        print("No numerical columns found in the DataFrame.")
        return
    
    # Determine the number of rows and columns for subplots
    num_cols = len(numerical_cols)
    cols_per_row = 3
    num_rows = math.ceil(num_cols / cols_per_row)
    
    # Create subplots
    fig, axes = plt.subplots(num_rows, min(num_cols, cols_per_row), figsize=(15, 5 * num_rows))
    axes = axes.flatten() if num_cols > 1 else [axes]
    
    # Plot boxplots
    for i, col in enumerate(numerical_cols):
        df.boxplot(column=col, ax=axes[i])
        axes[i].set_title(f"Boxplot of {col}")
    
    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(output_filename)
    print(f"Boxplots saved as '{output_filename}'")
    plt.close()



def clean_data(df):
    """Main function to clean the data."""
    df = replace_dash_and_symbols_with_nan(df)
    df = fix_spelling_errors_in_columns(df)
    df = fix_spelling_errors_in_categorical(df)
    df = handle_negative_values(df)
    df = handle_missing_values(df)
    df = handle_duplicates(df)
    check_cardinality(df)
    save_boxplots(df)
    
    # df = remove_outliers(df)
    df = fix_skewness(df)
    df=check_multicollinearity(df)
    df=save_cleaned_data(df)
    return df


def create_log_file(data_quality_issues):
    """Create a log file of data quality issues."""
    with open("data_quality_log.txt", "w") as file:
        for issue in data_quality_issues:
            file.write(f"{issue}\n")
