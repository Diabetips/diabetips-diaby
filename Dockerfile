FROM python:3.8
RUN useradd -m diabetips-diaby
USER diabetips-diaby
WORKDIR /home/diabetips-diaby
RUN pip install --no-cache-dir uwsgi
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY App ./App
