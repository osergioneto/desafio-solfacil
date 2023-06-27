# Use the official Python base image
FROM python:3.10.6

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY ./requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the application app
COPY ./app /app/app
COPY ./assets /app/assets

RUN chmod 755 /app/assets

# Expose the port that the FastAPI application listens on
EXPOSE 8000

# Start the FastAPI application with Uvicorn when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]