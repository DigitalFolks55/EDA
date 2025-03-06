# Base image
FROM python:3.12

# Working directory
WORKDIR /eda

# Copy files
COPY . /eda

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8501

# Execute the app
CMD ["streamlit", "run", "eda_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
