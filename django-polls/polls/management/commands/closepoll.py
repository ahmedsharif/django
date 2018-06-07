from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll
from django.utils import translation

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        translation.activate('ru')
        from django.conf import settings
        translation.activate(settings.LANGUAGE_CODE)

        for poll_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            if options['delete']:
                poll.delete()
            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS(
                'Successfully closed poll "%s"' % poll_id))

        translation.deactivate()