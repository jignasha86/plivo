from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from plivoapis.models import Account

class PlivoAuthentication(authentication.BasicAuthentication):

      def authenticate_credentials(self, userid, password):
          try:
              user = Account.objects.get(username=userid, auth_id=password)
          except Account.DoesNotExist:
                 raise exceptions.AuthenticationFailed('Invalid username/password')
          except Account.MultipleObjectsReturned:
                 raise exceptions.AuthenticationFailed('Conflicts in records')

          return (user, None)
