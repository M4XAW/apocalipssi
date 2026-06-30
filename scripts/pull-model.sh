#!/usr/bin/env bash
# ============================================================================
# pull-model.sh — Télécharge le modèle Llama 3.2 3B dans Ollama
# ----------------------------------------------------------------------------
# À exécuter UNE fois après le premier `docker compose up`.
# Modèle retenu après benchmark/ADR pour réduire la latence CPU et la charge
# disque par rapport au 8B.
# ============================================================================

set -euo pipefail

MODEL="${OLLAMA_MODEL:-llama3.2:3b}"
CONTAINER="${OLLAMA_CONTAINER:-apocalipssi-2026-ollama}"

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "❌ Conteneur Ollama '${CONTAINER}' non démarré."
    echo "   Lancez d'abord : docker compose up -d"
    exit 1
fi

echo "⏳ Téléchargement du modèle ${MODEL} dans ${CONTAINER}..."
echo "   Cela prend généralement 3 à 10 minutes selon votre connexion."
echo ""

docker exec "${CONTAINER}" ollama pull "${MODEL}"

echo ""
echo "✅ Modèle ${MODEL} téléchargé avec succès."
echo ""
echo "🧪 Test rapide :"
docker exec "${CONTAINER}" ollama list
