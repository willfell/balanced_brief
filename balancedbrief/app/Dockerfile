# Use an official Python 3 image as a parent image
FROM python:3.9.17-alpine3.17

# Set the working directory in the container
WORKDIR /app

# Copy just the requirements.txt first
COPY balancedbrief/app/requirements.txt .

# Install the Python dependencies
RUN pip3 install -r requirements.txt && apk add --no-cache --upgrade bash

# Now, copy everything else
COPY balancedbrief/app .

COPY db /app/db

CMD ["sh", "init.sh"]

