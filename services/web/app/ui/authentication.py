from urllib.parse import urlencode
from django.conf import settings
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class MyOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = super(MyOIDCAuthenticationBackend, self).create_user(claims)
        user.username = claims.get('preferred_username', )
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        print(claims)
        user.save()

        return user

    def update_user(self, user, claims):
        user.username = claims.get('preferred_username', )
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()

        return user


def provider_logout(request):
    """ Create the user's OIDC logout URL."""
    # User must confirm logout request with the default logout URL
    # and is not redirected.
    logout_url = settings.OIDC_OP_LOGOUT_ENDPOINT

    # If we have the oidc_id_token, we can automatically redirect
    # the user back to the application.
    oidc_id_token = request.session.get('oidc_id_token')
    if oidc_id_token:
        keycloak_data = {
            "id_token_hint": oidc_id_token,
            "post_logout_redirect_uri": request.build_absolute_uri(location=settings.LOGOUT_REDIRECT_URL)
        }
        logout_url = (
                settings.OIDC_OP_LOGOUT_ENDPOINT
                + "?"
                + urlencode(keycloak_data)
        )
    print(logout_url)
    return logout_url
