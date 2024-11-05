# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class config:
    OTEL_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "flask-api")
    
    CONNECTION_STRING = os.getenv("CONNECTION_STRING", "InstrumentationKey=fd877389-3f5d-47d6-9b5c-c66929a1e6dc;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/;ApplicationId=1ed0b7cf-1583-412d-ab51-11d87cd86644")

class DevelopmentConfig(config):
    DEBUG = True

class ProductionConfig(config):
    DEBUG = True

def factory(context):
    if context == 'production':
        return ProductionConfig
    return DevelopmentConfig
