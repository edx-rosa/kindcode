from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from core.dailyEmail import buildEmailContext

class Command(BaseCommand):
    help = "Send the daily Kind Code email"

    def handle(self, *args, **options):
        ctx = buildEmailContext()
        subject = f"Kind Code — {ctx['prettyDate']}"
        htmlBody = render_to_string("emails/daily.html", ctx)
        textBody = f"""Good morning

{ctx['prettyDate']}

Your mission:
- {ctx['mission']}

Quote:
- "{ctx['quote']['text']}" — {ctx['quote']['author']}

Today:
""" + "\n".join([f"- {a['time']} — {a['title']}" for a in ctx["appointments"]])

        toList = [e.strip() for e in settings.DAILY_EMAIL_TO.split(",") if e.strip()]
        if not toList:
            self.stdout.write(self.style.WARNING("No DAILY_EMAIL_TO configured; printing to console instead."))
            print(textBody)
            return

        msg = EmailMultiAlternatives(
            subject=subject,
            body=textBody,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=toList,
        )
        msg.attach_alternative(htmlBody, "text/html")
        msg.send()
        self.stdout.write(self.style.SUCCESS(f"Daily email sent to: {', '.join(toList)}"))
