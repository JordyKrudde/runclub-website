#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techture_media.settings.dev")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django kon niet worden geïmporteerd. Controleer of Django is geïnstalleerd "
            "en beschikbaar is in je virtuele omgeving."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
