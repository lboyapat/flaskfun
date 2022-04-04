#Create a ubuntu base image with python 3 installed.
FROM public.ecr.aws/docker/library/python:latest

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


#Set the working directory
WORKDIR /usr/src/app

#copy all the files
COPY . .

#Install the dependencies
RUN apt-get -y update && apt-get install -y python3 python3-pip

RUN pip3 install flask Flask-SQLAlchemy
RUN pip3 install sqlalchemy
RUN pip install -r requirements.txt

#Expose the required port
EXPOSE 80

#Run the command
CMD python ./app.py

