FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# OTEL settings
# to be overwritten in k8s
ENV OTEL_SERVICE_NAME=videovault-api
ENV OTEL_RESOURCE_ATTRIBUTES=deployment.environment=dev,service.version=0.3
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_METRICS_EXPORTER=otlp
ENV OTEL_PYTHON_LOG_CORRELATION=true
ENV OTEL_PYTHON_LOG_FORMAT='[%(asctime)s] [%(process)d] [%(levelname)s] trace_id=%(otelTraceID)s span_id=%(otelSpanID)s %(name)s: %(message)s'


RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R app:app /app
COPY --chown=app:app . .

USER app
EXPOSE 8000

CMD ["opentelemetry-instrument", "gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "src:create_app()"]