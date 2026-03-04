#!/bin/bash
# Script pour nettoyer le repository Git et ajouter uniquement les fichiers nécessaires

echo "Nettoyage du repository Git..."

# Retirer tous les fichiers de l'index
git rm -r --cached .

echo "Ajout uniquement des fichiers nécessaires..."

# Ajouter les fichiers selon .gitignore
git add .

echo ""
echo "✓ Repository nettoyé !"
echo ""
echo "Fichiers à commiter :"
git status --short | head -20
echo ""
echo "Pour commiter : git commit -m 'votre message'"
