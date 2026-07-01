/** Mentions légales (modèle vierge à compléter). */
import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: 'Éditeur du site',
    hint: "nom de l'organisation/équipe, statut, adresse, email de contact.",
    content: (
      <>
        <p>
          Le site EduTutor IA est édité dans le cadre du projet pédagogique APOCAL'IPSSI 2026 par
          l'équipe 29.
        </p>
        <p>
          Ce service est un projet étudiant de formation et n'est pas exploité comme service
          commercial. Pour toute demande relative au site, contactez l'équipe projet via l'adresse
          communiquée par l'IPSSI ou par l'encadrement pédagogique.
        </p>
      </>
    ),
  },
  {
    title: 'Directeur de la publication',
    hint: 'nom de la personne responsable du contenu publié.',
    content: (
      <p>
        Le directeur de la publication est le responsable désigné de l'équipe projet EduTutor IA,
        sous supervision pédagogique APOCAL'IPSSI 2026. À compléter avant mise en ligne : [nom du
        responsable de publication].
      </p>
    ),
  },
  {
    title: 'Hébergeur',
    hint: "nom, adresse et téléphone de l'hébergeur du site.",
    content: (
      <>
        <p>
          En production, l'application est prévue pour être hébergée sur un VPS OVHcloud, avec un
          reverse proxy HTTPS et des conteneurs applicatifs Docker.
        </p>
        <p>OVH SAS, 2 rue Kellermann, 59100 Roubaix, France. Téléphone : 1007 depuis la France.</p>
      </>
    ),
  },
  {
    title: 'Propriété intellectuelle',
    hint: 'à qui appartiennent les textes, logos, code, contenus.',
    content: (
      <>
        <p>
          Le code source du kit de démarrage est fourni à des fins pédagogiques sous licence CC
          BY-NC-SA 4.0, sauf mention contraire dans les fichiers du projet.
        </p>
        <p>
          Les contenus déposés par les utilisateurs afin de générer des quiz restent sous leur
          responsabilité. Ils doivent disposer des droits nécessaires sur les documents, textes ou
          supports transmis au service.
        </p>
      </>
    ),
  },
  {
    title: 'Contact',
    hint: 'comment vous joindre pour toute question juridique.',
    content: (
      <p>
        Pour toute question concernant les présentes mentions légales, l'utilisation du service ou
        une demande liée aux données personnelles, contactez l'équipe projet via le canal
        pédagogique indiqué par l'IPSSI.
      </p>
    ),
  },
];

export default function MentionsLegalesPage() {
  return (
    <LegalScaffold
      title="Mentions légales"
      intro="Informations légales obligatoires identifiant l'éditeur et l'hébergeur du site."
      sections={SECTIONS}
    />
  );
}
