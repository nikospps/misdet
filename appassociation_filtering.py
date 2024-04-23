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

        # Add three buttons for different processes in the same row
        # col1, col2, col3= st.columns(3)
        show = pd.read_csv(uploaded_file, index_col=0)

        if st.button("Uploaded Dataset"):
            # Execute process 1
            # st.write("Dataset ...")
            # show = pd.read_csv(uploaded_file, index_col=0)  # Assuming 'Rule' and 'Rule2' are column names in your CSV file
            st.write(show)

        option = st.selectbox(
            "Events Filtering",
            ("Event 1", "Event 2"),
            index=None,
            placeholder="Select event..",
        )

        if option == 'Event 1':
            option1 = st.selectbox(
                "Most Frequent Events",
                show['Rule'].unique().tolist(),
                index=None,
                placeholder="Select an event..",
            )
            lift = st.slider('Select the lift', 0, 60, 1)

            filter1 = show[(show['Rule']==option1) & (show['Lift']>=lift)]
            st.table(filter1)
            # st.write(option1)
            # st.write(lift)

        elif option == 'Event 2':
            option2 = st.selectbox(
                "Most Frequent Events",
                show['Rule2'].unique().tolist(),
                index=None,
                placeholder="Select an event..",
            )
            lift2 = st.slider('Select the lift', 0, 60, 1)

            filter2 = show[(show['Rule2'] == option2) & (show['Lift'] >= lift2)]
            st.table(filter2)
            # st.write(option1)
            # st.write(lift)