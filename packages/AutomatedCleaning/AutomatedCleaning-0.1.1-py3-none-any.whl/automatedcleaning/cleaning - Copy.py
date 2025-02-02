import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
from spellchecker import SpellChecker
import warnings

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


def fix_incorrect_data_types(df):
    """
    Fix incorrect data types in the DataFrame.
    - Handles numeric columns stored as objects with invalid entries like '-'.
    - Converts numeric strings to numbers.
    - Converts invalid entries to NaN.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        
    Returns:
        pd.DataFrame: The DataFrame with corrected data types.
    """
    for col in df.columns:
        # Handle object columns
        if df[col].dtype == 'object':
            # Replace common placeholders for missing values like "-" with NaN
            df[col] = df[col].replace(['-'], np.nan)
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def fix_column_names(df):
    """Fix column names (strip spaces, lowercase, replace spaces with underscores)."""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def fix_spelling_errors_in_columns(df):
    """Fix spelling errors in column names."""
    spell = SpellChecker()
    fixed_columns = [spell.correction(col) for col in df.columns]
    df.columns = fixed_columns
    return df

def fix_spelling_errors_in_categorical(df):
    """Fix spelling errors in categorical columns."""
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: x.lower() if isinstance(x, str) else x)
    return df

def handle_negative_values(df):
    """Handle negative values by replacing them with zero in numeric columns."""
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].apply(lambda x: max(x, 0))
    return df

def handle_missing_values(df):
    """
    Handle missing values using mean imputation for numerical columns 
    and mode imputation for categorical columns.
    """
    # Handle missing values for numerical columns with mean
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        mean_value = df[col].mean()
        df[col].fillna(mean_value, inplace=True)
    
    # Handle missing values for categorical columns with mode
    categorical_cols = df.select_dtypes(include=[object, 'category']).columns
    for col in categorical_cols:
        mode_value = df[col].mode()[0]  # mode()[0] gets the most frequent value
        df[col].fillna(mode_value, inplace=True)
    
    return df


def handle_duplicates(df):
    """Remove duplicate rows."""
    return df.drop_duplicates()

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

def check_multicollinearity(df):
    """Check for multicollinearity using correlation matrix."""
    num_df = df.select_dtypes(include=['int', 'float'])
    correlation_matrix = num_df.corr()
    return correlation_matrix

def remove_multicollinearity(df, threshold=0.7):
    """Remove columns with high correlation."""
    num_df = df.select_dtypes(include=['int', 'float'])
    correlation_matrix = num_df.corr()
    to_drop = [column for column in correlation_matrix.columns if any(abs(correlation_matrix[column]) > threshold)]
    df = df.drop(columns=to_drop)
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
    
    # Calculate and return cardinality of categorical columns
    return df[categorical_cols].nunique()

def save_cleaned_data(df, file_name="cleaned_data.csv"):
    """Save cleaned DataFrame to a CSV file."""
    df.to_csv(file_name, index=False)
    print(f"Cleaned data saved to {file_name}")


def clean_data(df):
    """Main function to clean the data."""
    df = fix_column_names(df)
    df = fix_spelling_errors_in_columns(df)
    df = fix_spelling_errors_in_categorical(df)
    df = handle_negative_values(df)
    df = handle_missing_values(df)
    df = handle_duplicates(df)
    # df = remove_outliers(df)
    df = fix_skewness(df)
    df = remove_multicollinearity(df)
    df=save_cleaned_data(df)
    return df

def visualize_outliers(df):
    """Visualize outliers using boxplots."""
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        sns.boxplot(x=df[col])
        plt.show()

def create_log_file(data_quality_issues):
    """Create a log file of data quality issues."""
    with open("data_quality_log.txt", "w") as file:
        for issue in data_quality_issues:
            file.write(f"{issue}\n")
