/** Politique de confidentialité. */
import LegalScaffold, { type LegalSection } from './LegalScaffold';

const SECTIONS: LegalSection[] = [
  {
    title: 'Responsable du traitement',
    hint: 'qui décide pourquoi et comment les données sont traitées.',
    content: (
      <p>
        Le traitement des données est réalisé par l'équipe projet EduTutor IA, dans le cadre
        pédagogique APOCAL'IPSSI 2026. L'équipe détermine les finalités et les moyens du traitement
        pour permettre l'accès au service, la génération de quiz et le suivi des résultats.
      </p>
    ),
  },
  {
    title: 'Données personnelles collectées',
    hint: 'email, nom, prénom, documents envoyés, historique de quiz…',
    content: (
      <>
        <p>
          Le service peut collecter les données de compte nécessaires à l'authentification :
          adresse email, mot de passe chiffré, statut de validation de l'email, date de création du
          profil et informations techniques liées à la session.
        </p>
        <p>
          Pour générer les quiz, l'application conserve le titre du quiz, le texte source transmis
          par l'utilisateur ou extrait d'un PDF, les questions générées, les options de réponse, les
          réponses sélectionnées, le score obtenu et l'historique associé au compte.
        </p>
      </>
    ),
  },
  {
    title: 'Finalités du traitement',
    hint: 'pourquoi vous collectez ces données (créer un compte, générer des quiz…).',
    content: (
      <p>
        Les données sont utilisées pour créer et sécuriser les comptes, vérifier les adresses email,
        permettre la réinitialisation du mot de passe, générer des quiz personnalisés, corriger les
        réponses, afficher l'historique, proposer la révision des erreurs et administrer le service.
      </p>
    ),
  },
  {
    title: 'Base légale',
    hint: 'consentement, contrat, intérêt légitime… (RGPD art. 6).',
    content: (
      <p>
        Les traitements nécessaires au fonctionnement du service reposent sur l'exécution du service
        demandé par l'utilisateur. Les traitements de sécurité, d'administration et de prévention des
        abus reposent sur l'intérêt légitime de l'équipe projet. Lorsque l'utilisateur dépose un
        document ou un texte afin de générer un quiz, il consent à son utilisation pour cette
        finalité.
      </p>
    ),
  },
  {
    title: 'Durée de conservation',
    hint: 'combien de temps les données sont gardées, puis supprimées/anonymisées.',
    content: (
      <p>
        Les données de compte sont conservées tant que le compte utilisateur existe. Les quiz,
        textes sources, questions, réponses et scores sont conservés afin de permettre l'historique
        et la révision, jusqu'à suppression par l'utilisateur, suppression du compte ou fin du projet
        pédagogique. Une politique de rétention dédiée peut préciser les durées par catégorie de
        données.
      </p>
    ),
  },
  {
    title: 'Destinataires des données',
    hint: 'qui y a accès (équipe, sous-traitants, fournisseurs LLM…).',
    content: (
      <p>
        Les données sont accessibles aux utilisateurs concernés et, lorsque nécessaire, aux membres
        autorisés de l'équipe projet disposant d'un accès d'administration. Certaines données
        peuvent être transmises à des prestataires techniques utilisés par le service, notamment
        l'hébergeur, le fournisseur d'envoi d'emails et le fournisseur LLM sélectionné pour générer
        les quiz.
      </p>
    ),
  },
  {
    title: 'Transferts hors UE',
    hint: 'si un fournisseur cloud héberge les données hors Union européenne.',
    content: (
      <p>
        Selon la configuration retenue, la génération de quiz peut être réalisée localement ou via un
        fournisseur LLM externe. Si un fournisseur situé hors de l'Union européenne est utilisé, les
        textes transmis pour générer les quiz peuvent faire l'objet d'un transfert hors UE. L'équipe
        projet doit privilégier, lorsque possible, des fournisseurs offrant des garanties adaptées au
        RGPD.
      </p>
    ),
  },
  {
    title: 'Vos droits',
    hint: 'accès, rectification, suppression, portabilité, opposition, et comment les exercer.',
    content: (
      <p>
        Conformément au RGPD, l'utilisateur peut demander l'accès à ses données, leur rectification,
        leur effacement, la limitation du traitement, leur portabilité ou s'opposer à certains
        traitements. Il peut également supprimer son compte depuis son profil lorsque la
        fonctionnalité est disponible. Toute demande peut être adressée à l'équipe projet via le
        canal de contact indiqué par l'IPSSI.
      </p>
    ),
  },
  {
    title: 'Cookies',
    hint: 'renvoi vers la politique de cookies du site.',
    content: (
      <p>
        Le service utilise principalement des mécanismes techniques nécessaires à l'authentification
        et au fonctionnement de l'application, notamment le stockage local du token de connexion dans
        le navigateur. Pour plus d'informations, consultez la politique de gestion des cookies et du
        stockage local du site.
      </p>
    ),
  },
  {
    title: 'Contact & réclamation',
    hint: 'email du référent données + droit de réclamation auprès de la CNIL.',
    content: (
      <p>
        Pour toute question ou demande relative aux données personnelles, l'utilisateur peut
        contacter l'équipe projet via le canal pédagogique communiqué par l'IPSSI. Il peut également
        introduire une réclamation auprès de la CNIL si la réponse apportée ne lui paraît pas
        satisfaisante.
      </p>
    ),
  },
];

export default function ConfidentialitePage() {
  return (
    <LegalScaffold
      title="Politique de confidentialité"
      intro="Comment les données personnelles des utilisateurs sont collectées, utilisées et protégées (RGPD)."
      sections={SECTIONS}
    />
  );
}
