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
    application = Application.objects.get(client_id="l3XcrZnwOS1V8JrItEUSZVpq2pWE3Ir1XaQxBgX2")

    new_uuid = uuid.uuid4()
    expires = timezone.now() + timezone.timedelta(seconds=3600)
    

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
        "access_token": str(access_token),
        "refresh_token": str(refresh_token),
    }

    return tokens
