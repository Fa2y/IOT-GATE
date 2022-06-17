FROM python:3.9

WORKDIR /opt/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./backend/requirements.txt /opt/backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /opt/backend/requirements.txt

COPY ./backend /opt/backend/

# --proxy-headers because running behind a Nginx proxy  
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]