FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8888
ENV NAME World
CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]

# FROM python:3
# ENV PYTHONUNBUFFERED 1

# WORKDIR /code

# COPY requirements.txt /code/

# RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


# FROM python:3
# ENV PYTHONUNBUFFERED 1
# RUN mkdir /app
# WORKDIR /app
# COPY requirements.txt /app/
# RUN pip install -r requirements.txt
# COPY . /app/