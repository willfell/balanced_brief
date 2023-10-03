# Use an official Python 3 image as a parent image
FROM python:3.9.17-alpine3.17

# Set the working directory in the container
WORKDIR /app

# Copy just the requirements.txt first
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Now, copy everything else
COPY . .

# For Backend Testing
# ENTRYPOINT ["/bin/sh", "-c", "/usr/local/bin/python3 /app/article_scraping/scraping.py"]

# For Email Testing
# ENTRYPOINT ["/bin/sh", "-c", "/usr/local/bin/python3 /app/newsletter/create_email_template.py"]

# Complete Process
ENTRYPOINT ["/bin/sh", "-c", "/usr/local/bin/python3 /app/article_scraping/scraping.py && /usr/local/bin/python3 /app/newsletter/create_email_template.py"]

