from core.models import BasePage


class HomePage(BasePage):
    """Startpagina van de website."""

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []

    class Meta:
        verbose_name = "Startpagina"
        verbose_name_plural = "Startpagina's"
