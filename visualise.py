import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 1. Connect to your local PostgreSQL database
DB_URI = "postgresql+psycopg2://postgres:project@localhost:5432/postgres"
engine = create_engine(DB_URI)

# 2. Write and execute the SQL query directly into a pandas DataFrame
query = """
SELECT 
    region, 
    SUM(a_rated_count) AS total_a_rated_properties
FROM 
    energy_dwellings
GROUP BY 
    region
ORDER BY 
    total_a_rated_properties DESC;
"""

df_results = pd.read_sql(query, engine)
print("--- Query Results Loaded into Python ---")
print(df_results)

# 3. Plot the results as a bar chart
plt.figure(figsize=(12, 6))
plt.bar(df_results['region'], df_results['total_a_rated_properties'], color='#2b5c8f')

# Add labels and styling
plt.xlabel('Region', fontsize=12, fontweight='bold')
plt.ylabel('Total A-Rated New Dwellings', fontsize=12, fontweight='bold')
plt.title('Regional Distribution of A-Rated New Dwellings', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the chart so you can include it in your GitHub README!
plt.savefig('energy_dwellings_chart.png')
print("\nChart saved successfully as 'energy_dwellings_chart.png'!")

# Display the chart on screen
plt.show()