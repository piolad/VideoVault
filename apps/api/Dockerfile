FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt
RUN chown -R app:app /app

COPY --chown=app:app . .

USER app

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "src:create_app()"]