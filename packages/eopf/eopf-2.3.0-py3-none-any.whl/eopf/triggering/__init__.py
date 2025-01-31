"""The eopf.triggering module simplifies the integration of processing units
with the most widespread processing orchestration systems
(Spring Cloud Data Flow, Apache Airflow, Zeebee, Apache Beam ...).
"""

from eopf.triggering.services.kafka_server import EOKafkaServer
from eopf.triggering.services.web_server import EOWebServer
from eopf.triggering.triggers.cli_triggers import EOCLITrigger

__all__ = ["EOCLITrigger", "EOKafkaServer", "EOWebServer"]
