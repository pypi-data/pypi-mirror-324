from setuptools import setup, find_packages

# Read README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='AutomatedCleaning',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'openpyxl',
        'imblearn',
        'pyspellchecker',
        'thefuzz',  # Updated from fuzzywuzzy
        'missingno',
    ],
    description='Automated Data Cleaning Library',
    long_description=long_description,  # Uses README.md content
    long_description_content_type="text/markdown",  # Ensures Markdown format
    author='Abhishek Kumar Singh',
    author_email='dataspoof007@gmail.com',
    url='https://github.com/DataSpoof/AutomatedCleaning',  # GitHub repo link
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.6",
)
