/** Politique de gestion des cookies. */
import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: "Qu'est-ce qu'un cookie ?",
    hint: 'définition simple à destination des utilisateurs.',
    content: (
      <p>
        Un cookie est un petit fichier déposé par le navigateur lors de la consultation d'un site,
        qui permet notamment de reconnaître l'utilisateur d'une page à l'autre. Par extension, cette
        politique couvre aussi les technologies de stockage local du navigateur, comme le
        localStorage, utilisées pour mémoriser certaines informations techniques.
      </p>
    ),
  },
  {
    title: 'Cookies et stockage utilisés',
    hint: "lister ce que le site dépose (cookie HttpOnly d'authentification, localStorage du thème…).",
    content: (
      <>
        <p>
          EduTutor IA dépose un cookie d'authentification en <strong>HTTP only</strong> et{' '}
          <strong>Secure</strong> pour maintenir la session de l'utilisateur connecté. Ce cookie
          n'est pas accessible en JavaScript et n'est transmis que via des connexions chiffrées
          (HTTPS), ce qui réduit les risques de vol de session par des scripts malveillants.
        </p>
        <p>
          Le site mémorise également la préférence d'affichage clair/sombre dans le stockage local
          du navigateur, sous la clé{' '}
          <code className="bg-slate-200 px-1 rounded">edututor-theme</code>. Aucun cookie de mesure
          d'audience, de publicité ou de suivi marketing n'est utilisé par défaut.
        </p>
      </>
    ),
  },
  {
    title: 'Finalité de chaque cookie',
    hint: "à quoi sert chaque cookie/stockage (technique, mesure d'audience…).",
    content: (
      <>
        <p>
          Le cookie d'authentification sert uniquement à identifier l'utilisateur connecté auprès de
          l'API et à sécuriser l'accès aux pages réservées, comme l'historique, le profil ou les
          quiz. Son caractère HTTP only empêche tout script exécuté sur la page d'y accéder ou de le
          lire, et son caractère Secure garantit qu'il n'est jamais envoyé en clair.
        </p>
        <p>
          La préférence de thème sert uniquement à conserver le choix d'affichage de l'utilisateur.
          Ces stockages sont techniques et nécessaires au bon fonctionnement ou au confort
          d'utilisation du service.
        </p>
      </>
    ),
  },
  {
    title: 'Consentement',
    hint: 'cookies nécessitant un consentement préalable et comment il est recueilli.',
    content: (
      <p>
        Les cookies et stockages utilisés par EduTutor IA sont strictement techniques et nécessaires
        au fonctionnement du service (authentification, préférence d'affichage). Ils ne nécessitent
        pas de consentement préalable au sens des règles applicables aux cookies non essentiels, car
        ils ne servent ni à la publicité, ni à la mesure d'audience, ni au suivi intersite.
      </p>
    ),
  },
  {
    title: 'Durée de conservation',
    hint: 'combien de temps chaque cookie est conservé.',
    content: (
      <p>
        Le cookie d'authentification est conservé jusqu'à la déconnexion, son expiration technique
        définie côté serveur, ou sa suppression manuelle par l'utilisateur dans son navigateur. La
        préférence de thème reste stockée jusqu'à modification du choix ou suppression des données
        locales du navigateur.
      </p>
    ),
  },
  {
    title: 'Gérer ou refuser les cookies',
    hint: 'comment paramétrer ou supprimer les cookies (navigateur, bannière).',
    content: (
      <p>
        L'utilisateur peut supprimer le cookie d'authentification et les données stockées par
        EduTutor IA depuis les paramètres de son navigateur, généralement dans la rubrique
        confidentialité, cookies ou données de site. Le cookie étant HTTP only, il ne peut pas être
        lu ou supprimé par du code JavaScript exécuté sur la page : la déconnexion depuis le site
        déclenche sa suppression côté serveur. Le refus ou la suppression de ce cookie entraîne la
        déconnexion et peut donc limiter l'accès aux fonctionnalités nécessitant un compte connecté.
      </p>
    ),
  },
];

export default function CookiesPage() {
  return (
    <LegalScaffold
      title="Politique de gestion des cookies"
      intro="Les cookies et technologies de stockage utilisés par le site, et comment les gérer."
      sections={SECTIONS}
    />
  );
}
