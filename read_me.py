import pandas as pd
from sqlalchemy import create_engine


def load_excel_to_dataframe(file_path: str, sheet_name=0) -> pd.DataFrame:
    """Reads a specified sheet from an Excel file into a pandas DataFrame."""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=3)
        print(
            f"Successfully loaded '{sheet_name}' with {len(df)} rows and"
            f" {len(df.columns)} columns."
        )
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()


# Execution block:
if __name__ == "__main__":
    file_name = "raw_data/NB1-_New_Domestic_Properties.ods"

    # 1. Load data
    df_dwellings = load_excel_to_dataframe(file_name, sheet_name=0)

    # 2. Filter essential columns
    target_columns = ["Region", "Quarter", "A"]
    df_filtered = df_dwellings[target_columns].copy()

    # 3. Clean and standardize string data
    df_filtered["Region"] = df_filtered["Region"].astype(str).str.strip()

    # 4. Clean numeric data and handle missing values
    df_filtered["A"] = pd.to_numeric(df_filtered["A"], errors="coerce")
    df_filtered = df_filtered.dropna(subset=["Region", "A"])
    df_filtered["A"] = df_filtered["A"].astype(int)

    # Clean up column names for SQL (lowercase avoids needing quotes in Postgres queries)
    df_filtered.columns = ["region", "quarter", "a_rated_count"]

    # 5. Sanity check
    print("\n--- Cleaned DataFrame Preview ---")
    print(df_filtered.head())
    print("\n--- DataFrame Structure ---")
    print(df_filtered.info())

    # ==========================================
    # 6. Load to PostgreSQL (Phase 2)
    # ==========================================
    # Update username, password, host, port, and db_name with your actual PostgreSQL credentials
    DB_URI = "postgresql+psycopg2://postgres:project@localhost:5432/postgres"

    try:
        engine = create_engine(DB_URI)

        # Automatically creates the table if it doesn't exist and appends records
        df_filtered.to_sql(
            name="energy_dwellings",
            con=engine,
            if_exists="append",
            index=False,
        )
        print(
            "\nSuccessfully created table 'energy_dwellings' and inserted"
            " records into PostgreSQL!"
        )

    except Exception as err:
        print(f"\nDatabase insertion failed: {err}")