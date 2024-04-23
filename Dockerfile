# Use an official Python base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Install required packages
RUN pip install streamlit \
                streamlit_authenticator \
                transformers \
                torch \
                plotly.express \
                pandas \
                newspaper3k \
                pysentimiento \
                matplotlib \
                lxml_html_clean

# Copy the entire content of the local source directory
COPY . .

# Command to run the Streamlit app
CMD ["streamlit", "run", "main.py"]
