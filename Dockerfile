# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port for Gunicorn
EXPOSE 8000

# Run Gunicorn server
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
