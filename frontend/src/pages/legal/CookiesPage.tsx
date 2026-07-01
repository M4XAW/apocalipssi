/** Politique de gestion des cookies. */
import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: "Qu'est-ce qu'un cookie ?",
    hint: 'définition simple à destination des utilisateurs.',
    content: (
      <p>
        Un cookie est un petit fichier enregistré par le navigateur lors de la consultation d'un
        site. Par extension, cette politique couvre aussi les technologies de stockage local du
        navigateur, comme le localStorage, utilisées pour mémoriser certaines informations
        techniques.
      </p>
    ),
  },
  {
    title: 'Cookies et stockage utilisés',
    hint: "lister ce que le site dépose (ex. token d'authentification en localStorage).",
    content: (
      <>
        <p>
          EduTutor IA utilise le stockage local du navigateur pour conserver le token
          d'authentification sous la clé{' '}
          <code className="bg-slate-200 px-1 rounded">apocal_token</code>. Ce token permet de
          maintenir la session de l'utilisateur entre deux pages ou deux visites.
        </p>
        <p>
          Le site mémorise également la préférence d'affichage clair/sombre sous la clé{' '}
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
          Le token d'authentification sert uniquement à identifier l'utilisateur connecté auprès de
          l'API et à sécuriser l'accès aux pages réservées, comme l'historique, le profil ou les
          quiz.
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
        Les stockages utilisés par EduTutor IA sont strictement techniques. Ils ne nécessitent pas
        de consentement préalable au sens des règles applicables aux cookies non essentiels, car ils
        ne servent ni à la publicité, ni à la mesure d'audience, ni au suivi intersite.
      </p>
    ),
  },
  {
    title: 'Durée de conservation',
    hint: 'combien de temps chaque cookie est conservé.',
    content: (
      <p>
        Le token de connexion reste stocké jusqu'à la déconnexion, la suppression du compte, une
        expiration technique côté serveur ou une suppression manuelle par l'utilisateur dans son
        navigateur. La préférence de thème reste stockée jusqu'à modification du choix ou
        suppression des données locales du navigateur.
      </p>
    ),
  },
  {
    title: 'Gérer ou refuser les cookies',
    hint: 'comment paramétrer ou supprimer les cookies (navigateur, bannière).',
    content: (
      <p>
        L'utilisateur peut supprimer les données stockées par EduTutor IA depuis les paramètres de
        son navigateur, généralement dans la rubrique confidentialité, cookies ou données de site.
        La suppression du token entraîne la déconnexion. Le refus ou la suppression de ces stockages
        peut donc limiter l'accès aux fonctionnalités nécessitant un compte connecté.
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
