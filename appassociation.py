import pandas as pd
import streamlit as st
# from apyori import apriori
import appassociation_helpfunc
import plotly.express as px
# import matplotlib.pyplot as plt
# import base64

def app():
    st.markdown("## Association Rule Mining")

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:

        # Add three buttons for different processes in the same row
        col1, col2, col3= st.columns(3)

        if col1.button("Uploaded Dataset"):
            # Execute process 1
            # st.write("Dataset ...")
            show = pd.read_csv(uploaded_file, encoding='unicode_escape')
            st.write(show)
            # st.write('-----------------')

        if col2.button("Mining"):
            # Execute process 2
            st.write("Association Rule Mining...")
            # Reset the buffer to avoid issues
            uploaded_file.seek(0)
            # Display association results
            st.write(appassociation_helpfunc.association_results(appassociation_helpfunc.preprocess(uploaded_file)))

        if col3.button("Analysis"):
            st.write("Association Rule Mining Analysis...")
            # Reset the buffer to avoid issues
            uploaded_file.seek(0)
            df=appassociation_helpfunc.association_results2(appassociation_helpfunc.preprocess(uploaded_file))
            # Display association results
            st.write(df)

            # Plot unstacked multiple columns using Plotly Express
            fig = px.bar(df, x="Rule", y=["Support", "Confidence", "Lift"],
                         labels={"value": "Values", "variable": "Metrics"}, barmode="group")

            # Display plot in Streamlit
            st.plotly_chart(fig, use_container_width=True)

        # if col3.button("Download CSV"):
        #     # Execute process 3 and download CSV
        #     processed_data = appassociation_helpfunc.association_results(
        #         appassociation_helpfunc.preprocess(uploaded_file))
        #     csv_data = processed_data.to_csv(index=True).encode('utf-8')
        #
        #     # Create a custom-styled download link with an icon using HTML and CSS
        #     icon = "📥"  # You can replace this with the desired icon
        #
        #     download_link = f'<a href="data:file/csv;base64,{base64.b64encode(csv_data).decode()}" download="processed_data.csv" style="text-decoration: none; padding: 10px; background-color: grey; color: white; border-radius: 5px; display: inline-block;">{icon}</a>'
        #
        #     st.markdown(download_link, unsafe_allow_html=True)
