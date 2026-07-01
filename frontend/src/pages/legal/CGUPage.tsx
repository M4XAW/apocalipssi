/** Conditions Générales d'Utilisation. */
import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: 'Objet',
    hint: 'ce que régissent ces CGU et le service concerné (EduTutor IA).',
    content: (
      <p>
        Les présentes Conditions Générales d'Utilisation encadrent l'accès et l'utilisation
        d'EduTutor IA, un service pédagogique permettant de générer des quiz de révision à partir de
        contenus fournis par l'utilisateur.
      </p>
    ),
  },
  {
    title: 'Acceptation des conditions',
    hint: "comment l'utilisateur accepte les CGU (inscription, usage…).",
    content: (
      <p>
        L'utilisation du service, la création d'un compte ou la connexion à un compte existant vaut
        acceptation des présentes CGU. Si l'utilisateur n'accepte pas ces conditions, il doit cesser
        d'utiliser le service.
      </p>
    ),
  },
  {
    title: 'Accès au service',
    hint: "conditions d'accès, disponibilité, prérequis techniques.",
    content: (
      <p>
        Le service est accessible depuis un navigateur web récent et une connexion Internet.
        L'équipe projet s'efforce de maintenir l'application disponible, mais ne garantit pas un
        accès permanent, notamment en cas de maintenance, d'incident technique ou de contraintes
        liées au cadre pédagogique du projet.
      </p>
    ),
  },
  {
    title: 'Compte utilisateur',
    hint: 'création, responsabilité du mot de passe, exactitude des informations.',
    content: (
      <>
        <p>
          L'utilisateur peut être amené à créer un compte à l'aide d'une adresse email et d'un mot
          de passe. Il est responsable de la confidentialité de ses identifiants et des actions
          réalisées depuis son compte.
        </p>
        <p>
          Les informations fournies doivent être exactes et ne pas usurper l'identité d'un tiers.
          L'utilisateur peut modifier son profil ou demander la suppression de son compte depuis les
          fonctionnalités prévues à cet effet.
        </p>
      </>
    ),
  },
  {
    title: 'Comportements interdits',
    hint: 'usages abusifs, contenus illicites, atteinte à la sécurité.',
    content: (
      <p>
        Il est interdit d'utiliser le service pour déposer des contenus illicites, porter atteinte
        aux droits de tiers, contourner les mécanismes de sécurité, perturber le fonctionnement de
        l'application, extraire massivement des données ou tenter d'accéder à des comptes, données
        ou espaces non autorisés.
      </p>
    ),
  },
  {
    title: 'Contenu généré par IA',
    hint: "limites des quiz générés (peuvent contenir des erreurs), responsabilité de l'utilisateur.",
    content: (
      <>
        <p>
          Les quiz et corrections sont générés automatiquement par un système d'intelligence
          artificielle. Ils peuvent contenir des erreurs, imprécisions, omissions ou formulations
          ambiguës.
        </p>
        <p>
          Ces contenus sont fournis comme aide à la révision. Ils ne remplacent pas un cours, une
          correction officielle, un avis pédagogique ou l'appréciation d'un enseignant.
          L'utilisateur conserve un esprit critique sur les réponses proposées.
        </p>
      </>
    ),
  },
  {
    title: 'Responsabilité',
    hint: "limites de responsabilité de l'éditeur.",
    content: (
      <p>
        EduTutor IA est fourni dans un cadre pédagogique et expérimental. L'équipe projet ne peut
        pas être tenue responsable d'une indisponibilité temporaire, d'une perte de données non
        imputable à une faute directe, d'une mauvaise utilisation du service ou des conséquences
        liées à l'exploitation des contenus générés.
      </p>
    ),
  },
  {
    title: 'Propriété intellectuelle',
    hint: "droits sur le service et sur les contenus déposés par l'utilisateur.",
    content: (
      <>
        <p>
          Le code, l'interface, les textes, la structure et les éléments graphiques du service sont
          protégés par le droit de la propriété intellectuelle, sauf mention contraire.
        </p>
        <p>
          L'utilisateur reste responsable des contenus qu'il dépose dans l'application. Il garantit
          disposer des droits nécessaires pour utiliser les documents, extraits de cours ou textes
          transmis au service.
        </p>
      </>
    ),
  },
  {
    title: 'Modification des CGU',
    hint: 'comment et quand les CGU peuvent évoluer.',
    content: (
      <p>
        Les présentes CGU peuvent être modifiées afin de tenir compte de l'évolution du service, du
        cadre pédagogique, de la réglementation ou des choix techniques du projet. La version
        applicable est celle publiée sur le site au moment de l'utilisation.
      </p>
    ),
  },
  {
    title: 'Droit applicable et litiges',
    hint: 'droit applicable et juridiction compétente.',
    content: (
      <p>
        Les présentes CGU sont soumises au droit français. En cas de difficulté, l'utilisateur est
        invité à contacter l'équipe projet afin de rechercher une solution amiable avant toute autre
        démarche.
      </p>
    ),
  },
];

export default function CGUPage() {
  return (
    <LegalScaffold
      title="Conditions Générales d'Utilisation"
      intro="Les règles d'utilisation du service EduTutor IA, acceptées par chaque utilisateur."
      sections={SECTIONS}
    />
  );
}
