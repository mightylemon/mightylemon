
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    requires_model_validation = False
    
    def handle(self, *args, **options):
        print "hello world"
