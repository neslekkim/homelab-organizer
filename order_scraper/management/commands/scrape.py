from django.core.management.base import BaseCommand, CommandError, no_translations
from .scrapers.ali import AliScraper
from .scrapers.amazon import AmazonDeScraper
import subprocess

class Command(BaseCommand):
    help = 'Scrapes a webshop for orders using Selenium'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
                'webshop',
                type=str.lower,
                choices=["aliexpress", "amazon.de"],
                help="The online webshop to scrape orders from"
                )

        parser.add_argument(
                '-c',
                '--cache',
                action='store_true',
                help="Use file cache of webshop orders if avaliable (mostly for development)"
                )

        parser.add_argument(
                '-i',
                '--indent',
                action='store_true',
                help="Loop and indent cache files (mostly for development)"
                )

    @no_translations
    def handle(self, *args, **options):
        match options['webshop']:
            case "aliexpress":
                if options['indent']:
                    AliScraper(self, options['cache']).indent()
                else:
                    AliScraper(self, options['cache']).scrape()
            case "amazon.de":
                AmazonDeScraper(self, options['cache'])
            case _:
                raise CommandError("Unknown webshop: {options['webshop']}")