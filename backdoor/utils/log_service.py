from backdoor.models import Exception
from django.utils import timezone

def log(message, user, db=True):
    print(message)#TODO redirect to log output
    if db:
        exc = Exception(user=user,message=message,occurence_date=timezone.now())
        exc.save()
