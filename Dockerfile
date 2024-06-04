# Use the official Python image from the Docker Hub
FROM python:3.11

# Make port 5001 available to the world outside this container. (PORT OUR FLASK APP WILL RUN IN).
#EXPOSE 5001

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

#RUN pip install -r requirements.txt
RUN pip install -- no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the working directory contents into the container
COPY . .

ENV FLASK_APP=main.py

# Run main.py when the container launches    ( ["--host", "0.0.0.0"] allows an external client to the container to make a request to the flask app that running in the container.)
#CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]
CMD ["gunicorn", "--bind", "0.0.0.0:80", "main:create_app()"]


# how to run the docker locally with gunicorn........   docker run -dp 5001:5000 -w /app -v "$(pwd):/app" flask-docker sh -c 'flask run --host=0.0.0.0'



# Define environment variable
#ENV PYTHONUNBUFFERED=1

# Install any needed packages specified in requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt





#                  NOTE
#  each one of the lines create a LAYER and each layer can be CACHED seprately.
#  so if you change the content of a line, and the layer will re-run the next time you build the image.
#  else it is cached ad does not have to re-run.





#      Command
#          docker build -t flask-docker .     (to build the image)
#          docker run -p 5001:5001 flask-docker       (to run the image)
#          docker run -dp 5001:5000 -w /app -v "$(pwd):/app" flask-docker  (flask app auto refresh because of .flaskenv  [this is ot for deploying, it's just for local evironment]  )