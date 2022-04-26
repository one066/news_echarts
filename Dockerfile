FROM python:3.9
WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app" \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
COPY src/ /app

CMD gunicorn --preload -k eventlet -w 1 -b 0.0.0.0:8008 manage:app --timeout 7200
