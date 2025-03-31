FROM python:3.12

RUN pip install requests

WORKDIR /app

COPY ex_smolvlm.py .

COPY existence_check.py .

CMD ["python3","ex_smolvlm.py"]
