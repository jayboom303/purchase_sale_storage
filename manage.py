#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

from log import init_log
from tools.project_config import ProjectConfig as Config

project_config = Config()
logger = logging.getLogger(__file__)


def main():
    """Run administrative tasks."""
    init_log()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'purchase_sale_storage.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
