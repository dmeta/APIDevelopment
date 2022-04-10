#Docker image 
FROM python:3.9.7 


#Working directory on server
WORKDIR /usr/src/app

# Copy requirements.txt to working directory
COPY requirements_ubuntu.txt ./
RUN pip install --no-cache-dir -r requirements_ubuntu.txt

COPY requirements.txt ./

# Run pip install for all requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy all src files from current directory to server workdir
COPY . .

#excute start up command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

