FROM python:3.9-buster
# By default, listen on port 5000
EXPOSE 80/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY *.py .
COPY shape_68.dat .
COPY requirements.txt .
COPY uwsgi.ini .
COPY start.sh .

# Install any dependencies
RUN apt-get update && apt-get install -y build-essential cmake nginx
RUN pip install -r requirements.txt


# Specify the command to run on container start
COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]