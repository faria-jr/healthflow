#!/bin/bash
# Script para configurar o repositório no GitHub

echo "🚀 HealthFlow - Setup do repositório GitHub"
echo ""

# Verificar se gh está instalado
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) não está instalado"
    echo "Instale em: https://cli.github.com/"
    exit 1
fi

# Verificar autenticação
if ! gh auth status &> /dev/null; then
    echo "🔐 Faça login no GitHub:"
    gh auth login
fi

# Criar repositório
echo "📦 Criando repositório..."
gh repo create healthflow \
    --description "Sistema de Clínica Médica - Clean Architecture + DDD" \
    --public \
    --source=. \
    --remote=origin \
    --push

echo ""
echo "✅ Repositório criado com sucesso!"
echo ""
echo "📍 URL: https://github.com/$(gh api user -q '.login')/healthflow"
