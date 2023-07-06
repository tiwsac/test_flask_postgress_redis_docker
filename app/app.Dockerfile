FROM python:3.9

COPY requirements.txt .

RUN pip install  -r requirements.txt --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org