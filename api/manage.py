#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Set the default settings module for the Django project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinearc.settings')
    try:
        # Import the Django function to execute command-line tasks
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise an error if Django is not installed or not properly configured
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute the command-line arguments passed to the script
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Entry point of the script
    main()
