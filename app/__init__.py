# app/__init__.py
import logging
from flask import Flask
from flask_marshmallow import Marshmallow
import os
from app.config import factory  # Importamos solo 'factory' correctamente
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry._logs import set_logger_provider
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter


# Inicializar Marshmallow
ma = Marshmallow()

# Configurar el proveedor de logs y el exportador a Azure
logger_provider = LoggerProvider()
set_logger_provider(logger_provider)
exporter = AzureMonitorLogExporter(connection_string=os.getenv('CONNECTION_STRING'))
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

# Configurar el logger y su nivel
handler = LoggingHandler()
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)

# Función para crear la aplicación Flask
def create_app():
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    
    # Seleccionar la configuración según el contexto de la aplicación
    f = factory(app_context if app_context else 'development')
    app.config.from_object(f)
    
    # Establecer la conexión para el exportador de logs en Azure Monitor
    exporter.from_connection_string(app.config['CONNECTION_STRING'])

    # Configuración del proveedor de trazas para OpenTelemetry
    tracer_provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: app.config['OTEL_SERVICE_NAME']})
    )
    trace.set_tracer_provider(tracer_provider)

    # Instrumentar Flask y Requests con OpenTelemetry
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()

    # Configuración del exportador de trazas a Azure Monitor
    trace_exporter = AzureMonitorTraceExporter(connection_string=app.config['CONNECTION_STRING'])
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(trace_exporter)
    )

    # Inicializar Marshmallow en la aplicación Flask
    ma.init_app(app)

    # Importar y registrar el Blueprint para las rutas de la aplicación
    from app.resources import home_bp
    app.register_blueprint(home_bp, url_prefix='/api/v1')

    # Contexto del shell para interactuar con la aplicación en modo interactivo
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app
