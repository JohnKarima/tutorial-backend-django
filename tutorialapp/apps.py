from django.apps import AppConfig


class TutorialappConfig(AppConfig):
    name = 'tutorialapp'

    def ready(self):
        import tutorialapp.signals
