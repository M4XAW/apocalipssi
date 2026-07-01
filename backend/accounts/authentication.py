"""Authentification par token DRF depuis un cookie HttpOnly."""

from django.conf import settings
from rest_framework.authentication import CSRFCheck, TokenAuthentication, get_authorization_header
from rest_framework.exceptions import PermissionDenied


class CookieTokenAuthentication(TokenAuthentication):
    """Accepte `Authorization: Token ...` ou le cookie d'auth HttpOnly.

    Le header reste supporte pour les tests, scripts et Swagger. Quand le token
    vient du cookie, les methodes non safe doivent passer le controle CSRF.
    """

    def authenticate(self, request):
        if get_authorization_header(request).split():
            return super().authenticate(request)

        token = request.COOKIES.get(settings.AUTH_TOKEN_COOKIE_NAME)
        if not token:
            return None

        user_auth_tuple = self.authenticate_credentials(token)
        self.enforce_csrf(request)
        return user_auth_tuple

    def enforce_csrf(self, request):
        check = CSRFCheck(lambda req: None)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise PermissionDenied(f"CSRF Failed: {reason}")
