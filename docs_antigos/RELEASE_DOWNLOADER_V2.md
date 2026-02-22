# 🚀 Release Downloader V2 - Busca Melhorada

## O Que Foi Implementado

Criei uma versão completamente nova do Release Downloader com foco em encontrar releases de **Q3 2025** (mais recentes disponíveis).

### Arquivo Criado:
`blog-cozy-corner-81/backend/app/services/release_downloader_v2.py`

---

## 🎯 Melhorias Principais

### 1. Busca Q3 2025 Primeiro
```python
# Ordem de busca:
Q3 2025 → Q2 2025 → Q1 2025 → Q4 2024 → Q3 2024
```

**Antes:** Buscava Q4 2024 primeiro
**Agora:** Busca Q3 2025 primeiro (mais recente)

### 2. Mais Variações de URLs
```python
urls_tentar = [
    f"{base_url}/resultados",
    f"{base_url}/central-de-resultados",
    f"{base_url}/releases",
    f"{base_url}/comunicados",
    f"{base_url}/resultados-trimestrais",  # NOVO
    f"{base_url}/relatorios",  # NOVO
    f"{base_url}/relatorios-financeiros",  # NOVO
    f"{base_url}/investidores/resultados",  # NOVO
    f"{base_url}/pt/resultados",  # NOVO
    f"{base_url}/pt-br/resultados",  # NOVO
    base_url,  # Página principal também
]
```

**Antes:** 4 URLs
**Agora:** 11 URLs

### 3. Busca Mais Flexível

**Variações de Trimestre:**
```python
# Para Q3 2025, busca:
- "q3", "3t", "3º", "3°"
- "2025", "25"
- "q32025", "q3 2025", "3t2025", "3t 2025", "3t25"
- "terceiro", "terceiro trimestre", "terceiro trimestre 2025"
```

**Antes:** Buscava apenas "Q3 2025" exato
**Agora:** Busca 15+ variações

### 4. Procura em Mais Lugares

```python
# Procura em:
- href (link)
- data-href (atributo)
- data-url (atributo)
- text (texto do link)
- title (título do link)
```

**Antes:** Apenas href e text
**Agora:** 5 lugares diferentes

### 5. Keywords Mais Abrangentes

```python
keywords = [
    'resultado', 
    'release', 
    'earnings', 
    'trimestre', 
    'trimestral', 
    'iti',  # NOVO - Informações Trimestrais
    'itr'   # NOVO - Informações Trimestrais
]
```

---

## 📊 Como Funciona

### Fluxo de Busca:

```
1. Verifica cache (90 dias)
   ↓
2. Para cada trimestre (Q3 2025 → Q4 2024):
   ↓
3. Gera variações (q3, 3t, terceiro, etc)
   ↓
4. Para cada URL do site de RI:
   ↓
5. Baixa HTML
   ↓
6. Procura links de PDF
   ↓
7. Verifica se contém variação do trimestre
   ↓
8. Verifica se é release/resultado
   ↓
9. Encontrou? Retorna informações
   ↓
10. Não encontrou? Tenta próximo trimestre
```

---

## 🔧 Integração

### Alpha System V3 Atualizado:

```python
# ANTES:
from app.services.release_downloader import ReleaseDownloader
self.release_downloader = ReleaseDownloader()

# AGORA:
from app.services.release_downloader_v2 import get_release_downloader_v2
self.release_downloader = get_release_downloader_v2()
```

### Uso:

```python
release_info = await self.release_downloader.buscar_release_mais_recente("PRIO3")

# Retorna:
{
    "ticker": "PRIO3",
    "trimestre": "Q3",
    "ano": 2025,
    "url": "https://ri.prioenergia.com.br/...",
    "fonte": "https://ri.prioenergia.com.br/resultados",
    "tipo": "release",
    "data_relatorio": datetime(2025, 9, 1),
    "resumo": "Release Q3 2025 encontrado em ..."
}
```

---

## 🎯 Próximos Passos

### Para Melhorar Ainda Mais:

1. **Adicionar mais URLs de RI**
   - Atualmente: ~30 empresas configuradas
   - Objetivo: 100+ empresas

2. **Usar IA para encontrar links**
   - Quando scraping falha, usar Groq para analisar HTML
   - IA identifica qual link é o release correto

3. **Cache inteligente**
   - Salvar PDFs baixados
   - Extrair texto com OCR
   - Indexar para busca rápida

4. **API de busca**
   - Google Custom Search API
   - Busca "PRIO3 release Q3 2025 filetype:pdf"

5. **Validação de conteúdo**
   - Verificar se PDF realmente é do trimestre correto
   - Extrair data de publicação do PDF

---

## 📝 Exemplo de Logs

### Sucesso:
```
🔍 PRIO3: Buscando Release (Q3 2025 → Q4 2024)...
  ✓ PRIO3: Encontrado Q3 2025 em https://ri.prioenergia.com.br/resultados
```

### Fallback:
```
🔍 VALE3: Buscando Release (Q3 2025 → Q4 2024)...
  ⚠ VALE3: Q3 2025 não encontrado, tentando Q2 2025...
  ✓ VALE3: Encontrado Q2 2025 em https://ri.vale.com/releases
```

### Não Encontrado:
```
🔍 ABEV3: Buscando Release (Q3 2025 → Q4 2024)...
  ⚠ ABEV3: Nenhum release encontrado
```

---

## ✅ Status

- ✅ Código implementado
- ✅ Integrado no Alpha System V3
- ✅ Busca Q3 2025 primeiro
- ✅ 11 URLs por empresa
- ✅ 15+ variações por trimestre
- ⏳ Aguardando teste em produção
- ⏳ Precisa adicionar mais URLs de RI

---

## 🚀 Resultado Esperado

Com essas melhorias, a taxa de sucesso de encontrar releases deve aumentar significativamente:

**Antes:**
- 0/30 releases encontrados (0%)
- Todas empresas caem em pesquisa web

**Agora (esperado):**
- 10-15/30 releases encontrados (33-50%)
- Menos dependência de pesquisa web
- Dados mais confiáveis (releases oficiais)

**Objetivo:**
- 20-25/30 releases encontrados (66-83%)
- Adicionar mais URLs de RI
- Implementar busca com IA como fallback
