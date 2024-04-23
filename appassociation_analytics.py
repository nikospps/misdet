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
    st.markdown("## Association Rule Mining Analytics")

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
            "Most Frequent Events Analysis",
            ("Event 1", "Event 2"),
            index=None,
            placeholder="Select event..",
        )

        if option == 'Event 1':
            col11, col12 = st.columns(2)
            if 'Rule' in show.columns:
                with col11:
                    aa = show['Rule'].value_counts().reset_index().rename(columns={"index": "value", 0: "count"})
                    st.table(aa)

                with col12:
                    # Visualize pie chart
                    fig = px.pie(aa, names=aa['Rule'], values=aa['count'], hover_name=aa['Rule'])

                    # Hide the legend
                    fig.update_layout(showlegend=False)

                    # Control the size of the chart within Streamlit
                    st.write(fig)
                    # st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Column 'Rule' does not exist in the dataset.")

        elif option == 'Event 2':
            col21, col22 = st.columns(2)
            if 'Rule2' in show.columns:
                with col21:
                    aa = show['Rule2'].value_counts().reset_index().rename(columns={"index": "value", 0: "count"})
                    st.table(aa)

                with col22:
                    # Visualize pie chart
                    fig = px.pie(aa, names=aa['Rule2'], values=aa['count'],
                                 hover_name=aa['Rule2'])

                    # Hide the legend
                    fig.update_layout(showlegend=False)

                    # Control the size of the chart within Streamlit
                    st.write(fig)
                    # st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Column 'Rule' does not exist in the dataset.")
