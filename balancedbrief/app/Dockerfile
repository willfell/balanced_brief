# Use an official Python 3 image as a parent image
FROM python:3.9.17-alpine3.17

# Set the working directory in the container
WORKDIR /app

# Copy everything into the container
COPY . .

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/sh", "-c", "/usr/local/bin/python3 /app/article_scraping/scraping.py && /usr/local/bin/python3 /app/newsletter/create_email_template.py"]

