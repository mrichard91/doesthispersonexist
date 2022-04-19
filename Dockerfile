FROM python:3.9-buster

EXPOSE 80/tcp

# Set the working directory in the container
WORKDIR /app

# Install any dependencies
RUN apt-get update && apt-get install -y build-essential cmake

COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy the dependencies file to the working directory
COPY shape_68.dat .
COPY *.py /app/


# Specify the command to run on container start
CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
