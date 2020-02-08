# Base image
FROM python:3.6-stretch

# Meta for Docker Hub
LABEL maintainer='matthewgleich@gmail.com'

# Fixing timezone
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Depencies
RUN pip3 install --upgrade pip
COPY requirements.txt /requirements.txt
COPY dev-requirements.txt /dev-requirements.txt
RUN pip3 install -r requirements.txt

# Copying over files
COPY /vision /vision
WORKDIR /vision

# Running program
CMD ["python3", "main.py"]