import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Maak een superuser aan als er nog geen bestaat.

    Gebruik via omgevingsvariabelen:
        DJANGO_SUPERUSER_USERNAME  (standaard: admin)
        DJANGO_SUPERUSER_EMAIL     (standaard: leeg)
        DJANGO_SUPERUSER_PASSWORD  (verplicht)

    Als DJANGO_SUPERUSER_PASSWORD niet gezet is, doet het commando niets
    zodat de startup niet faalt op een omgeving zonder deze variabele.
    """

    help = "Maak een superuser aan als er nog geen bestaat (idempotent)."

    def handle(self, *args, **kwargs):
        User = get_user_model()

        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_PASSWORD niet ingesteld — superuser overgeslagen."
                )
            )
            return

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS("Superuser bestaat al — niets gedaan.")
            )
            return

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(
            self.style.SUCCESS(f'Superuser "{username}" succesvol aangemaakt.')
        )
