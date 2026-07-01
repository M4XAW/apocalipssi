/**
 * Client axios partage.
 *
 * - Lit l'URL de base depuis VITE_API_BASE_URL.
 * - Envoie le cookie d'auth HttpOnly avec `withCredentials`.
 * - Ajoute le header CSRF sur les requetes qui modifient l'etat.
 */
import axios, { type AxiosInstance } from 'axios';

// Vite remplace import.meta.env.VITE_API_BASE_URL au build ou au demarrage du
// dev-server. En production same-origin, la valeur attendue est souvent "/api".
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api';
const CSRF_COOKIE_NAME = 'csrftoken';

export const api: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 120_000, // 2 min, utile pour generate-quiz qui peut etre long.
  withCredentials: true,
});

function getCookie(name: string): string | null {
  const prefix = `${name}=`;
  return (
    document.cookie
      .split(';')
      .map((cookie) => cookie.trim())
      .find((cookie) => cookie.startsWith(prefix))
      ?.slice(prefix.length) ?? null
  );
}

function isUnsafeMethod(method?: string): boolean {
  return !['get', 'head', 'options', 'trace'].includes((method ?? 'get').toLowerCase());
}

api.interceptors.request.use((config) => {
  if (isUnsafeMethod(config.method)) {
    const csrfToken = getCookie(CSRF_COOKIE_NAME);
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => Promise.reject(error),
);
