"""Django app configuration for agents API."""

from django.apps import AppConfig


class AgentsApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.agents_api'
    verbose_name = 'Agents API'
