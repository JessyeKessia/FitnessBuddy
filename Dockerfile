FROM python:3.10
EXPOSE 5000
WORKDIR /FitnessBuddy
COPY ./FitnessBuddy/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./FitnessBuddy .
CMD [ "flask", "run", "--host", "0.0.0.0" ]