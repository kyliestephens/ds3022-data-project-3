import requests
import os
import sys
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='analysis.log')
logger=logging.getLogger(__name__)

def analyze_commits():
    con=duckdb.connect(database='packages.duckdb',read_only=False)
    logger.info("Connected to DuckDB database for analysis.")

    try:
        commit_count=con.execute("""SELECT DISTINCT package as package, COUNT(*) as package_count FROM commits GROUP BY package;""").fetchall()
        commit_counts_df=pd.DataFrame(commit_count, columns=['package', 'package_count'])
        logger.info("Fetched commit counts per package.")

        plt.figure(figsize=(10,6))
        plt.bar(commit_counts_df['package'], commit_counts_df['package_count'], color='skyblue')
        plt.xlabel('Package')
        plt.ylabel('Number of Commits')
        plt.title('Number of Commits per Package')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('commit_counts_per_package.png')
        logger.info("Saved commit counts bar chart as commit_counts_per_package.png.")
        print( commit_counts_df)
    except Exception as e:
        logging.error(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    analyze_commits()