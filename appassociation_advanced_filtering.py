import pandas as pd
import streamlit as st
# from apyori import apriori
# import appassociation_helpfunc
# import base64
import plotly.express as px

# st.set_page_config(
#     page_title = 'Data Quality Assessment',
#     page_icon = '✅',
#     layout = 'wide'
# )

def app():
    st.markdown("## Association Rule Mining Filtering")

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        show = pd.read_csv(uploaded_file, index_col=0)

        if st.button("Uploaded Dataset"):
            st.write(show)

        option1 = st.selectbox(
            "Most Frequent Events",
            show['Rule'].unique().tolist(),
            index=None,
            placeholder="Select an event..",
        )

        option2 = st.selectbox(
            "Most Frequent Events",
            show['Rule2'].unique().tolist(),
            index=None,
            placeholder="Select an event..",
        )

        lift = st.slider('Select the lift', 0, 60, 1)

        filter = show[(show['Rule']==option1) & (show['Rule2']==option2) & (show['Lift']>=lift)]
        st.table(filter)