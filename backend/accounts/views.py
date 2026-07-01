"""
Endpoints d'authentification (Lot 3 : email-identifiant + validation + reset).

    POST /api/accounts/signup/                  — créer un compte (par email)
    POST /api/accounts/login/                   — se connecter (par email) -> token
    POST /api/accounts/logout/                  — se déconnecter
    GET  /api/accounts/me/                       — utilisateur courant (+ email_verified)
    POST /api/accounts/verify-email/             — confirmer l'email (token du lien)
    POST /api/accounts/resend-verification/      — renvoyer l'email de validation
    POST /api/accounts/password-reset/           — demander un reset (envoie un email)
    POST /api/accounts/password-reset/confirm/   — définir le nouveau mot de passe
"""

import csv
import json
import logging
from io import StringIO

from django.conf import settings
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils import timezone
=======
from django.middleware.csrf import get_token
>>>>>>> auth-cookie-migration
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails import EmailError, send_password_reset_email, send_verification_email
from .models import get_or_create_profile
from .serializers import (
    ChangePasswordSerializer,
    DeleteAccountSerializer,
    EmailVerifySerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ProfileUpdateSerializer,
    SignupSerializer,
    UserSerializer,
)
from .tokens import read_email_verify_token, read_password_reset_tokens

logger = logging.getLogger(__name__)

class CSVExportRenderer(BaseRenderer):
    """Renderer minimal pour autoriser `?format=csv` sur l'export RGPD."""

    media_type = "text/csv"
    format = "csv"
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

def _set_auth_cookie(response: Response, token: Token) -> None:
    response.set_cookie(
        settings.AUTH_TOKEN_COOKIE_NAME,
        token.key,
        max_age=settings.AUTH_TOKEN_COOKIE_MAX_AGE,
        httponly=True,
        secure=settings.AUTH_TOKEN_COOKIE_SECURE,
        samesite=settings.AUTH_TOKEN_COOKIE_SAMESITE,
    )


def _clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(
        settings.AUTH_TOKEN_COOKIE_NAME,
        samesite=settings.AUTH_TOKEN_COOKIE_SAMESITE,
    )

class SignupView(APIView):
    """Inscription par email. Envoie l'email de validation (best-effort)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(request=SignupSerializer, responses={201: UserSerializer})
    def post(self, request):
        # Lot 8 : l'admin peut fermer les inscriptions depuis l'interface.
        from administration.models import SiteConfig

        if not SiteConfig.load().allow_signups:
            return Response(
                {"detail": "Les inscriptions sont actuellement fermées."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Validation SOFT : on tente d'envoyer l'email de confirmation, mais on
        # NE bloque PAS l'inscription si l'envoi échoue (clé Brevo expirée, etc.).
        try:
            send_verification_email(user)
        except EmailError as exc:
            logger.warning("Email de validation non envoyé pour %s : %s", user.email, exc)

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Connexion par email + mot de passe. Pose un cookie HttpOnly + crée la session."""

    permission_classes = [AllowAny]
    # Endpoint PUBLIC (pré-auth) : on désactive l'authentification de requête.
    # Sinon DRF SessionAuthentication, dès qu'un cookie `sessionid` résiduel est
    # présent (posé par django_login au login précédent), impose un contrôle CSRF
    # et rejette l'appel : « CSRF Failed: CSRF token missing ». Le frontend
    # s'authentifie par token, pas par session — il n'envoie pas de jeton CSRF.
    authentication_classes = []

    @extend_schema(
        request=LoginSerializer, responses={200: OpenApiResponse(description="{ user }")}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        token, _ = Token.objects.get_or_create(user=user)
        django_login(request, user)  # session utile pour la Swagger UI
        get_token(request)  # force l'émission du cookie CSRF pour les futures écritures
        response = Response({"user": UserSerializer(user).data})
        _set_auth_cookie(response, token)
        return response


class LogoutView(APIView):
    """Déconnexion : invalide le token + détruit la session."""

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(responses={204: OpenApiResponse(description="Déconnexion réussie")})
    def post(self, request):
        auth = get_authorization_header(request).split()
        token_key = None

        if len(auth) == 2 and auth[0].lower() == b"token":
            token_key = auth[1].decode()
        else:
            token_key = request.COOKIES.get(settings.AUTH_TOKEN_COOKIE_NAME)

        if token_key:
            Token.objects.filter(key=token_key).delete()

        django_logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        _clear_auth_cookie(response)
        return response


class MeView(APIView):
    """Renvoie l'utilisateur connecté (avec email_verified pour le bandeau front)."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class MeExportView(APIView):
    """Export RGPD des données de l'utilisateur connecté.

    GET /api/accounts/me/export/             — JSON complet
    GET /api/accounts/me/export/?format=csv  — CSV machine-readable
    """

    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, CSVExportRenderer]

    def _build_payload(self, user):
        from quizzes.models import Quiz

        profile = get_or_create_profile(user)
        quizzes = Quiz.objects.filter(user=user).prefetch_related("questions").order_by("id")

        return {
            "exported_at": timezone.now(),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": user.date_joined,
                "last_login": user.last_login,
                "is_active": user.is_active,
            },
            "profile": {
                "email_verified": profile.email_verified,
                "created_at": profile.created_at,
            },
            "quizzes": [
                {
                    "id": quiz.id,
                    "title": quiz.title,
                    "source_text": quiz.source_text,
                    "score": quiz.score,
                    "created_at": quiz.created_at,
                    "updated_at": quiz.updated_at,
                    "questions": [
                        {
                            "id": question.id,
                            "index": question.index,
                            "prompt": question.prompt,
                            "options": question.options,
                            "correct_index": question.correct_index,
                            "selected_index": question.selected_index,
                        }
                        for question in quiz.questions.all()
                    ],
                }
                for quiz in quizzes
            ],
            # Aucun modèle de signalement n'existe dans ce codebase pour l'instant.
            "reports": [],
        }

    def _filename(self, user, extension: str) -> str:
        timestamp = timezone.now().strftime("%Y%m%d-%H%M%S")
        return f"edututor-export-user-{user.id}-{timestamp}.{extension}"

    def _json_response(self, request, payload):
        response = HttpResponse(
            json.dumps(payload, cls=DjangoJSONEncoder, ensure_ascii=False, indent=2),
            content_type="application/json",
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{self._filename(request.user, "json")}"'
        )
        return response

    def _csv_response(self, request, payload):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["entity", "entity_id", "parent_entity", "parent_id", "field", "value"])

        for field, value in payload["user"].items():
            writer.writerow(["user", payload["user"]["id"], "", "", field, value])

        for field, value in payload["profile"].items():
            writer.writerow(
                ["profile", payload["user"]["id"], "user", payload["user"]["id"], field, value]
            )

        for quiz in payload["quizzes"]:
            questions = quiz["questions"]
            for field, value in quiz.items():
                if field != "questions":
                    writer.writerow(
                        ["quiz", quiz["id"], "user", payload["user"]["id"], field, value]
                    )

            for question in questions:
                for field, value in question.items():
                    writer.writerow(
                        [
                            "question",
                            question["id"],
                            "quiz",
                            quiz["id"],
                            field,
                            json.dumps(value, ensure_ascii=False),
                        ]
                    )

        response = HttpResponse(output.getvalue(), content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = (
            f'attachment; filename="{self._filename(request.user, "csv")}"'
        )
        return response

    @extend_schema(responses={200: OpenApiResponse(description="Export RGPD JSON ou CSV")})
    def get(self, request):
        payload = self._build_payload(request.user)
        if request.query_params.get("format") == "csv":
            return self._csv_response(request, payload)
        return self._json_response(request, payload)


class VerifyEmailView(APIView):
    """Confirme l'adresse email à partir du token reçu par email."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(
        request=EmailVerifySerializer,
        responses={200: OpenApiResponse(description="Email confirmé")},
    )
    def post(self, request):
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = read_email_verify_token(serializer.validated_data["token"])
        if uid is None:
            return Response(
                {"detail": "Lien de validation invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response(
                {"detail": "Utilisateur introuvable."}, status=status.HTTP_400_BAD_REQUEST
            )

        profile = get_or_create_profile(user)
        profile.email_verified = True
        profile.save(update_fields=["email_verified"])
        return Response({"detail": "Adresse email confirmée avec succès."})


class ResendVerificationView(APIView):
    """Renvoie l'email de validation à l'utilisateur connecté."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: OpenApiResponse(description="Email renvoyé")})
    def post(self, request):
        if get_or_create_profile(request.user).email_verified:
            return Response({"detail": "Votre email est déjà confirmé."})
        try:
            send_verification_email(request.user)
        except EmailError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({"detail": "Email de validation renvoyé."})


class PasswordResetRequestView(APIView):
    """Demande de réinitialisation : envoie un email avec un lien (si le compte existe)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={200: OpenApiResponse(description="Email envoyé si le compte existe")},
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip().lower()

        user = User.objects.filter(email__iexact=email).first()
        if user is not None:
            try:
                send_password_reset_email(user)
            except EmailError as exc:
                logger.warning("Email de reset non envoyé pour %s : %s", email, exc)

        # Anti-énumération : réponse IDENTIQUE que le compte existe ou non
        # (on ne révèle pas quels emails sont enregistrés).
        return Response(
            {
                "detail": "Si un compte existe pour cet email, un lien "
                "de réinitialisation vient d'être envoyé."
            }
        )


class PasswordResetConfirmView(APIView):
    """Définit le nouveau mot de passe à partir du lien (uid + token)."""

    permission_classes = [AllowAny]
    authentication_classes = []  # endpoint public : pas de CSRF via session (cf. LoginView)

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={200: OpenApiResponse(description="Mot de passe réinitialisé")},
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = read_password_reset_tokens(
            serializer.validated_data["uid"], serializer.validated_data["token"]
        )
        if user is None:
            return Response(
                {"detail": "Lien de réinitialisation invalide ou expiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response({"detail": "Mot de passe réinitialisé. Vous pouvez vous connecter."})


# ---------------------------------------------------------------------------
# Gestion du profil (Lot 4)
# ---------------------------------------------------------------------------


class ProfileView(APIView):
    """Profil de l'utilisateur connecté : consulter, modifier, supprimer.

    GET    /api/accounts/profile/  — lire son profil
    PATCH  /api/accounts/profile/  — modifier prénom / nom / email
    DELETE /api/accounts/profile/  — supprimer définitivement son compte
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    @extend_schema(request=ProfileUpdateSerializer, responses={200: UserSerializer})
    def patch(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Si l'email a changé, on (re)envoie un email de validation (best-effort,
        # validation SOFT : on ne bloque pas si l'envoi échoue).
        if getattr(user, "_email_changed", False):
            try:
                send_verification_email(user)
            except EmailError as exc:
                logger.warning("Email de validation non renvoyé pour %s : %s", user.email, exc)

        return Response(UserSerializer(user).data)

    @extend_schema(
        request=DeleteAccountSerializer,
        responses={204: OpenApiResponse(description="Compte supprimé")},
    )
    def delete(self, request):
        # Suppression DURE (hard delete) : confirmée par le mot de passe.
        # [TODO J3-bis RGPD] Avant de supprimer, proposer un export des données
        #   personnelles (droit à la portabilité). Voir Lot futur "export RGPD".
        serializer = DeleteAccountSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        Token.objects.filter(user=user).delete()  # invalide le token courant
        django_logout(request)
        user.delete()  # supprime aussi le Profile (on_delete=CASCADE)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        _clear_auth_cookie(response)
        return response


class ChangePasswordView(APIView):
    """Changement de mot de passe (en étant connecté, avec l'ancien mot de passe)."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: OpenApiResponse(description="Mot de passe modifié")},
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        # Changer le mot de passe invalide les tokens DRF existants : on en
        # régénère un pour que l'utilisateur reste connecté sans avoir à se
        # reconnecter manuellement.
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        get_token(request)
        response = Response({"detail": "Mot de passe modifié."})
        _set_auth_cookie(response, token)
        return response
