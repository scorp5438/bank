FROM python:3.12
WORKDIR /app/bank
COPY requirements.txt bank/
RUN pip install --no-cache-dir -r bank/requirements.txt
COPY . .
CMD ["sh", "-c", "gunicorn bank.wsgi:application --bind 0.0.0.0:8000 --workers $((4 * $(nproc)))"]