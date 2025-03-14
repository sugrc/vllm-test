FROM python:3.12

RUN pip install requests

COPY ex_smolvlm.py .

CMD ["python3","ex_smolvlm.py"]
