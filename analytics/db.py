from sqlalchemy import create_engine
import pandas as pd
import os

class DB:

    def __init__(self) -> None:
        
        self._engine = self.get_engine()
        pass
    
    def get_engine(self) :
        user = os.environ.get("PG_USER", None)
        password = os.environ.get("PG_PW", None)
        host = os.environ.get("PG_HOST", None)
        db_name = os.environ.get("PG_DB_NAME", None)

        if not (user and password and host and db_name) :
            raise ValueError(f"Doesn't exist PG_USER, PG_PW, PG_HOST, PG_DB_NAME")

        cnt_string = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
        return create_engine(cnt_string)

    def get_product_item(self) -> pd.DataFrame :
        query = f"SELECT * FROM product_item;"
        try :
            df = pd.read_sql(
                query,
                self._engine
            )
        except Exception as e :
            return pd.DataFrame()
        return df