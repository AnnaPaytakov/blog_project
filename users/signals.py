from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_delete, post_save


def new_user_created(sender, instance, created, **kwargs):
    if created:
        new_user = instance
        Profile.objects.create(
            user=new_user,
            username=new_user.username,
            firstname = new_user.first_name,
            lastname = new_user.last_name,
            email = new_user.email,
        )
    else:
        try:
            profile=Profile.objects.get(user=instance)
            profile.username=instance.username
            profile.save()
        except:
            pass

post_save.connect(new_user_created, sender=User)

def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_delete.connect(deleteUser, sender=Profile)