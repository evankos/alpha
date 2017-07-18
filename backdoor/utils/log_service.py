from backdoor.models import Exception
from django.utils import timezone
import traceback

def log(message, user, db=True):
    print(traceback.print_exc(),message)#TODO redirect to log output
    if db:
        exc = Exception(user=user,message=message,occurence_date=timezone.now())
        exc.save()
