import uuid
from django.utils import timezone
from oauth2_provider.models import Application, AccessToken, RefreshToken, IDToken
import random
import string



class AuthUtils:
    @staticmethod
    def generate_unique_string(length):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    

def get_access_token(user):
    application = Application.objects.get(client_id="4pa0xsXkY5gBjitJto3iUgYO2srLSKMLca748ngq")

    new_uuid = uuid.uuid4()
    expires = timezone.now() + timezone.timedelta(seconds=300)
    

    id_token = IDToken.objects.create(jti=new_uuid, expires=expires)

    access_token = AccessToken(
        user=user,
        scope='read write groups',
        expires=expires,
        token=AuthUtils.generate_unique_string(126),
        application=application,
        id_token=id_token
    )
    access_token.save()

    refresh_token = RefreshToken(
        user=user,
        token=AuthUtils.generate_unique_string(126),
        application=application,
        access_token=access_token
    )
    refresh_token.save()

    AccessToken.objects.filter(token=access_token.token).update(source_refresh_token=refresh_token)

    tokens = {
        "access_token": str(access_token) ,
        "refresh_token": str(refresh_token),
    }

    return tokens


def generate_access_token_from_refresh_token(refresh_token,access_token_obj):
    try:
        refresh_token_obj = RefreshToken.objects.get(token=refresh_token)
        application = refresh_token_obj.application

        
        new_access_token_expires = timezone.now() + timezone.timedelta(seconds=5)

        new_access_token = AuthUtils.generate_unique_string(126)

        access_token_obj.token = new_access_token
        access_token_obj.expires = new_access_token_expires
        access_token_obj.save()

        return new_access_token

    except RefreshToken.DoesNotExist:
        return None
