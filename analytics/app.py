import altair as alt
import pandas as pd
import streamlit as st
from db import DB

def get_data() -> pd.DataFrame :
    db = DB()
    df = db.get_product_item()
    if len(df) == 0 :
        return None

    prov_uni = df["provider"].unique()
    dict_res = {}
    for p in prov_uni :
        dict_res[p] = df[df['provider'] == p].copy()

    cols = ["name", "price", "brand", "model"]
    merge_df = pd.merge(dict_res[prov_uni[0]][cols], dict_res[prov_uni[1]][cols], how="inner", left_on=["brand", "model"], right_on=["brand", "model"])
    merge_df = merge_df.drop_duplicates(subset=["brand", "model"])
    for c in merge_df.columns :
        if "price" in c :
            merge_df[c] = merge_df[c].astype('str')

    return merge_df


def main() :
    st.title('Compare price 2 website')

    df = get_data()
    if (df is None) or (len(df) == 0) :
        st.markdown("#### Doesn't exist data should to running pipeline for load data to warehouse.")
        return 

    df_c = df[["brand", "model"]]
    df_a = df[["name_x", "price_x"]].rename(columns={
        "name_x": "name",
        "price_x": "price",
    })
    df_b = df[["name_y", "price_y"]].rename(columns={
        "name_y": "name",
        "price_y": "price",
    })

    dict_res = {
        "compare": df_c,
        "website_a": df_a,
        "website_b": df_b,
    }
    avg_price_a = df_a["price"].astype('float').mean()
    avg_price_b = df_b["price"].astype('float').mean()
    st.markdown(f"### Average price")
    st.markdown(f"- website_a: {avg_price_a:.2f}")
    st.markdown(f"- website_b: {avg_price_b:.2f}")
    st.dataframe(
        pd.concat(dict_res.values(), axis=1, keys=dict_res.keys()), 
        hide_index=True
    )

main()