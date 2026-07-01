"""
Modèles de l'app accounts.

[Note pédagogique] On garde le modèle User standard de Django (simple et
robuste), et on lui ajoute un Profil 1-pour-1 pour les infos métier qui ne sont
pas dans User — ici `email_verified` (l'utilisateur a-t-il cliqué le lien de
confirmation envoyé par email ?).

Choix d'architecture « email = identifiant » : à l'inscription, on met
username = email (voir SignupSerializer). Le login se fait donc par email, sans
backend d'authentification custom. C'est le compromis le plus simple pour un
kit pédagogique (un vrai produit utiliserait souvent un User personnalisé avec
USERNAME_FIELD = 'email').
"""

from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Informations complémentaires attachées à un utilisateur."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    # Validation "soft" : le compte fonctionne même si l'email n'est pas vérifié,
    # mais un bandeau invite l'utilisateur à cliquer le lien de confirmation.
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Profile<{self.user.email or self.user.username}>"


def get_or_create_profile(user) -> Profile:
    """Récupère (ou crée) le profil d'un utilisateur.

    Pratique pour les comptes créés AVANT l'ajout du modèle Profile (ils n'ont
    pas encore de profil) : on le crée à la volée plutôt que de planter.
    """
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


class DataRequest(models.Model):
    """Audit trail des demandes d'accès aux données (SAR — RGPD art. 15).

    Chaque export ou demande formelle est tracé : demandeur, statut, date de
    réponse et empreinte SHA-256 du fichier transmis (preuve d'intégrité).
    """

    class Status(models.TextChoices):
        RECEIVED = "recue", "Reçue"
        IN_PROGRESS = "en_cours", "En cours"
        RESPONDED = "repondue", "Répondue"

    class RequestType(models.TextChoices):
        ACCESS = "access", "Accès (art. 15)"
        EXPORT = "export", "Export portabilité (art. 20)"
        DELETION = "deletion", "Effacement (art. 17)"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="data_requests",
    )
    request_type = models.CharField(
        max_length=20,
        choices=RequestType.choices,
        default=RequestType.ACCESS,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RECEIVED,
    )
    export_format = models.CharField(
        max_length=10,
        blank=True,
        help_text="Format du fichier exporté (json, csv…).",
    )
    export_file_hash = models.CharField(
        max_length=64,
        blank=True,
        help_text="Empreinte SHA-256 du fichier transmis (hex).",
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-requested_at"]
        verbose_name = "demande d'accès aux données"
        verbose_name_plural = "demandes d'accès aux données"

    def __str__(self) -> str:
        return (
            f"DataRequest<{self.user_id} {self.request_type} "
            f"{self.status} @ {self.requested_at:%Y-%m-%d %H:%M}>"
        )
