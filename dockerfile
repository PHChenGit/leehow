# Use the official Python 3.10-alpine image as the base image
FROM python:3.10-alpine

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install mysqlclient 

# Copy the rest of the application files to the working directory
COPY . .

# Start MariaDB and keep the container running
# CMD ["sh", "-c", "service mariadb start && tail -f /dev/null"]



