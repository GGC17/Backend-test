FROM python:3.11

WORKDIR /repo

COPY requirements.txt ./
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-t 30", "--workers=4", "-b 0.0.0.0:5000", \
     "--log-level=debug", \
     "wsgi:app"]
ENV PYTHONUNBUFFERED=1