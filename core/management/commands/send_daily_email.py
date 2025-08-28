from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.conf import settings
from core.dailyEmail import buildEmailContext

def safeSend(msg, stdout):
    try:
        msg.send()
        return True
    except Exception as e:
        stdout.write(f"Email send failed: {e}\nFalling back to console EmailBackend…")
        consoleConn = get_connection("django.core.mail.backends.console.EmailBackend")
        consoleConn.send_messages([msg])
        return False

class Command(BaseCommand):
    help = "Send the daily Kind Code email"

 
    def handle(self, *args, **options):
        from django.conf import settings
        self.stdout.write(f"backend: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"postmark token present: {bool(settings.POSTMARK_API_TOKEN)}")

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
        sentOk = safeSend(msg, self.stdout)
        if sentOk:
            self.stdout.write(self.style.SUCCESS(f"Daily email sent to: {', '.join(toList)}"))
        else:
            self.stdout.write(self.style.WARNING("Delivered to console (fallback)."))

        self.stdout.write(self.style.SUCCESS(f"Daily email sent to: {', '.join(toList)}"))
