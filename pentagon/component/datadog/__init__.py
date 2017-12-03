
from pentagon.component import ComponentBase
import os


class Datadog(ComponentBase):
    _environment = [{'aws_region': 'AWS_DEFAULT_REGION'}, 'infrastructure_bucket']
