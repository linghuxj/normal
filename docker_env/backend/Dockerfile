FROM python:3.10

COPY ./backend/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

WORKDIR /app

CMD [ "python", "main.py", "run"]