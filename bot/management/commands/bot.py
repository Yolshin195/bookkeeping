from django.core.management.base import BaseCommand, CommandError


class RunBotCommand(BaseCommand):
    help = "Running telegram bot"

    def handle(self, *args, **options):
        print("running bot!")
