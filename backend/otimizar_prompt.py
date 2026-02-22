import re

# Lê o arquivo
with open('app/services/analise_com_release_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Novo prompt otimizado (reduzido de ~2000 para ~600 tokens)
new_prompt_code = '''prompt = f"""Analista: identifique ações 5%/mês.

{ticker}|{setor}|R${preco_atual:.2f} ROE:{roe_brapi*100:.1f}% P/L:{pl:.1f} Margem:{margem_liquida*100:.1f}% Div:{debt_to_equity:.1f}%

RELEASE:{texto_release[:2500]}

CATALISADORES(40pts)-Sem concretos máx 6.0:
✅Concreto:contrato(cliente,valor),expansão física,produto(nome,data),mercado(país,quando)
❌Vago:"expansão","melhoria","novos produtos"

MOMENTUM(25pts):Setor aquecido?Gatilho iminente?Preço entrada?
SAÚDE(20pts):Margens↑?Caixa ok?Dívida ok?
GESTÃO(10pts)|PREÇO(5pts)

NOTAS:
9-10:3+concretos+timing perfeito(50%+)
7.5-8.9:2+concretos+bom(30-50%)
6-7.4:1-2concretos(20-30%)
4-5.9:vagos(10-20%)
0-3.9:sem

JSON:{{"nota":8.5,"recomendacao":"COMPRA FORTE","preco_teto":65.0,"upside":18.0,"catalisadores":["Específico 1(o quê,quando,quanto)","2","3"],"riscos":["Concreto 1","2","3"],"resumo":"2 linhas"}}"""'''

# Encontra o início do método _montar_prompt_analise
start_marker = 'def _montar_prompt_analise'
end_marker = 'return prompt'

# Encontra as posições
start_pos = content.find(start_marker)
if start_pos == -1:
    print("Método não encontrado!")
    exit(1)

# Encontra o primeiro return prompt após o início do método
temp_content = content[start_pos:]
end_pos = temp_content.find(end_marker)
if end_pos == -1:
    print("return prompt não encontrado!")
    exit(1)

# Calcula posição absoluta
end_pos = start_pos + end_pos + len(end_marker)

# Encontra onde começa o prompt = f"""
prompt_start = content.find('prompt = f"""', start_pos)
if prompt_start == -1:
    print("Início do prompt não encontrado!")
    exit(1)

# Substitui apenas a parte do prompt
before = content[:prompt_start]
after = content[end_pos:]

new_content = before + new_prompt_code + '\n        ' + after

# Remove return duplicado se existir
new_content = re.sub(r'(return prompt)\s+(return prompt)', r'\1', new_content)

# Salva
with open('app/services/analise_com_release_service.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Prompt otimizado! Reduzido de ~2000 para ~600 tokens")
print("   - Mantém foco em catalisadores concretos")
print("   - Mantém critérios de nota rigorosos")
print("   - Consome 70% menos tokens do Groq")
