/**
 * Appels API liés à l'authentification (Lot 3 : identifiant = EMAIL).
 *
 * [Note pédagogique] L'inscription et la connexion se font désormais par EMAIL
 * (et non plus par un "nom d'utilisateur"). Le backend stocke username = email
 * en interne, mais le front n'a plus à connaître cette astuce : il manipule
 * uniquement l'email.
 */
import { api } from './client';
import axios from 'axios';

export type User = {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  /** L'utilisateur a-t-il confirmé son adresse email (lien reçu par mail) ? */
  email_verified?: boolean;
  /** Compte administrateur (accès à la page /admin) ? */
  is_staff?: boolean;
};

type LoginResponse = { user: User };

/** Connexion par email + mot de passe. Le backend pose le cookie HttpOnly. */
export async function login(email: string, password: string): Promise<User> {
  const { data } = await api.post<LoginResponse>('/accounts/login/', { email, password });
  return data.user;
}

/** Inscription par email. Connecte automatiquement l'utilisateur ensuite. */
export async function signup(input: {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}): Promise<User> {
  const { data } = await api.post<User>('/accounts/signup/', input);
  // Auto-login après signup (réutilise email + mot de passe).
  await login(input.email, input.password);
  return data;
}

export async function logout(): Promise<void> {
  try {
    await api.post('/accounts/logout/');
  } catch (error) {
    if (!axios.isAxiosError(error) || ![401, 403].includes(error.response?.status ?? 0)) {
      throw error;
    }
  }
}

export async function me(): Promise<User> {
  const { data } = await api.get<User>('/accounts/me/');
  return data;
}

function getFilenameFromContentDisposition(header: string | undefined): string | null {
  if (!header) return null;
  const utf8Match = header.match(/filename\*=UTF-8''([^;]+)/i);
  if (utf8Match?.[1]) return decodeURIComponent(utf8Match[1]);
  const plainMatch = header.match(/filename="?([^"]+)"?/i);
  return plainMatch?.[1] ?? null;
}

export type ExportFormat = 'json' | 'csv';

/** Télécharge l'export RGPD des données de l'utilisateur connecté. */
export async function exportMyData(format: ExportFormat = 'json'): Promise<void> {
  const { data, headers } = await api.get<Blob>('/accounts/me/export/', {
    params: format === 'csv' ? { format } : undefined,
    responseType: 'blob',
  });

  const fallbackFilename = `edututor-export.${format}`;
  const filename =
    getFilenameFromContentDisposition(headers['content-disposition']) ?? fallbackFilename;
  const url = URL.createObjectURL(data);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

// ---------------------------------------------------------------------------
// Validation d'email
// ---------------------------------------------------------------------------

/** Confirme l'adresse email à partir du token reçu par email. */
export async function verifyEmail(token: string): Promise<string> {
  const { data } = await api.post<{ detail: string }>('/accounts/verify-email/', { token });
  return data.detail;
}

/** Renvoie l'email de validation à l'utilisateur connecté. */
export async function resendVerification(): Promise<string> {
  const { data } = await api.post<{ detail: string }>('/accounts/resend-verification/');
  return data.detail;
}

// ---------------------------------------------------------------------------
// Mot de passe oublié
// ---------------------------------------------------------------------------

/** Demande un lien de réinitialisation (réponse identique que le compte existe ou non). */
export async function requestPasswordReset(email: string): Promise<string> {
  const { data } = await api.post<{ detail: string }>('/accounts/password-reset/', { email });
  return data.detail;
}

/** Définit le nouveau mot de passe à partir du lien (uid + token). */
export async function confirmPasswordReset(
  uid: string,
  token: string,
  new_password: string,
): Promise<string> {
  const { data } = await api.post<{ detail: string }>('/accounts/password-reset/confirm/', {
    uid,
    token,
    new_password,
  });
  return data.detail;
}

// ---------------------------------------------------------------------------
// Profil (Lot 4) : modifier ses infos, son mot de passe, supprimer son compte
// ---------------------------------------------------------------------------

/** Modifie le profil (prénom / nom / email). Renvoie l'utilisateur à jour. */
export async function updateProfile(input: {
  first_name?: string;
  last_name?: string;
  email?: string;
}): Promise<User> {
  const { data } = await api.patch<User>('/accounts/profile/', input);
  return data;
}

/** Change le mot de passe (ancien requis). Le backend renouvelle le cookie d'auth. */
export async function changePassword(old_password: string, new_password: string): Promise<string> {
  const { data } = await api.post<{ detail: string }>('/accounts/change-password/', {
    old_password,
    new_password,
  });
  return data.detail;
}

/** Supprime définitivement le compte (confirmé par le mot de passe). */
export async function deleteAccount(password: string): Promise<void> {
  // axios : le corps d'une requête DELETE se passe via la clé `data`.
  await api.delete('/accounts/profile/', { data: { password } });
}
