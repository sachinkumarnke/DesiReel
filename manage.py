#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    
    # Add the backend directory to the path
    current_path = os.path.dirname(os.path.abspath(__file__))
    backend_path = os.path.join(current_path, 'backend')
    sys.path.insert(0, backend_path)
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()