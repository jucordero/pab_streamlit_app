import streamlit as st
import pandas as pd
import numpy as np
from store_names import store_names

url_base = "https://cdn.rebrickable.com/media/parts/elements/"
elm_per_row = 15

elements = pd.read_csv("Data/elements.csv")
colors = pd.read_csv("Data/colors.csv")

df = pd.read_excel(st.secrets["doc_url"], sheet_name=None, dtype='string')

# GUI
st.set_page_config(layout='wide')
st.write("""Select a store from the dropdown list below. The app will display
         what pieces are in stock according to the public spreadsheet""")

selected_store = st.selectbox("Store", store_names)
try:
    for coli, (id, color, name) in enumerate(zip(df[selected_store]["Part ID"],
                                                df[selected_store]["Color"],
                                                df[selected_store]["Part name"])):
        if coli%elm_per_row == 0:
            cols = st.columns(elm_per_row)
        
        color_id = colors[colors["name"] == color]["id"].values[0]
        element = elements[np.logical_and(elements["part_num"] == id, elements["color_id"]==int(color_id))]["element_id"].values[0]
        cols[coli%elm_per_row].image(url_base + str(element) + ".jpg", width=100)
        cols[coli%elm_per_row].write(color)
        cols[coli%elm_per_row].write(name)

        if coli%elm_per_row == 0:
            st.divider()

except KeyError:
    st.write("Data for this store hasn't been added yet.")