from django.apps import AppConfig
from django.db.backends.signals import connection_created
import logging

class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'



logger = logging.getLogger(__name__)

def on_connection_created(sender, connection, **kwargs):
    connection.connection.set_notice_processor(process_notice)

def process_notice(message):
    logger.warning("PostgreSQL notice: %s" % message)

class YourAppConfig(AppConfig):
    def ready(self):
        connection_created.connect(on_connection_created)
