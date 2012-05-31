from django.core.management.base import NoArgsCommand
from django.core.management.commands import cleanup
from django.utils import timezone

class Command(cleanup.Command):
    help = "Can be run as a cronjob or directly to clean out old data from the database (only expired sessions and sso_tokens at the moment)."

    def handle_noargs(self, **options):
        super(Command, self).handle_noargs(self, **options)
        from django.db import transaction
        from token_sso.models import Token
        Token.objects.filter(used_expired=True).delete()
        transaction.commit_unless_managed()