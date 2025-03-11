from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperUser
from django.contrib.auth import get_user_model

UserProfile = get_user_model()

class Command(CreateSuperUser):
    help = "Create a superuser with additional fields"

    def get_input_data(self, field, message, default=None):
        # save user info for further tweaking
        val = super().get_input_data(field, message, default)
        self.options[field.name] = val
        return val

    def handle(self, *args, **options):
        # save options into attribute so when can populate it later
        self.options = options
        # default handling
        super().handle(*args, **options)
        # assign role to user
        username = options.get('username')
        user = UserProfile.objects.get(username=username)
        user.role = UserProfile.ROLE_ADMIN
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Assigned ADMIN role to '{username}'"))
