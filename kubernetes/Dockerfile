# Read from Ubuntu Base Image
FROM python:2.7
RUN mkdir -p /service
# Copy over all the files of interest
ADD mysite /service/mysite
ADD data /service/data
ADD kmeans.py /service/kmeans.py
ADD manage.py /service/manage.py
ADD db.sqlite3 /service/db.sqlite3
ADD project_template /service/project_template
ADD winecluster.py /service/winecluster.py
ADD requirements.txt /service/requirements.txt
WORKDIR /service/
RUN pip install -r requirements.txt
CMD python manage.py runserver 0.0.0.0:8000
