from sqlalchemy import create_engine
import pandas as pd
import requests
import psycopg2

def main() :

    create_table()

    website_a = "http://0.0.0.0:8001/api/items"
    website_b = "http://0.0.0.0:8002/api/items"

    pipeline(website_a, "website_a")
    pipeline(website_b, "website_b")

def pipeline(api: str, src: str) :
    ##### ingest data
    print(f"Ingest data from {src}")
    df = ingest_data(api)
    transform_df = transfrom_data(df, src)
    load_to_warehouse(transform_df)
    print("-------------------------")

def get_connection_string() -> str :
    host = "0.0.0.0"
    port = "5432"
    user = "postgres"
    password = "admin1234"
    db_name = "postgres"
    cnt_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    
    return cnt_string

def get_engine() :
    cnt_string = get_connection_string()
    return create_engine(cnt_string)

def ingest_data(api: str) -> pd.DataFrame :
    """
    Extract data from outside source

    Args:
        api (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    data = requests.get(api)
    df = pd.DataFrame(data.json())
    return df

def transfrom_data(df: pd.DataFrame, source_data: str) -> pd.DataFrame :

    df["provider"] = source_data
    df["created_by"] = "data_engineer"

    return df

def load_to_warehouse(df: pd.DataFrame) :
    engine = get_engine()

    tb_name = "product_item"
    with engine.begin() as connection:
        df.to_sql(
            name=tb_name,
            con=connection,
            if_exists='append',
            index=False,
        )
    
    print(f"Load data: {len(df)} to {tb_name} success.")

def create_table() :
    query = f"""
        CREATE TABLE IF NOT EXISTS product_item (
        id SERIAL PRIMARY KEY,
        name CHARACTER VARYING,
        price DOUBLE PRECISION,
        brand CHARACTER VARYING,
        model CHARACTER VARYING,
        category CHARACTER VARYING,
        provider CHARACTER VARYING,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by CHARACTER VARYING
        ) ;
    """
    cnt_string = get_connection_string()
    conn = psycopg2.connect(cnt_string)
    cur = conn.cursor()

    cur.execute(query=query)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__" :
    main()