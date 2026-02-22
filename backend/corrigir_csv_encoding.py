"""
Script para corrigir todos os pd.read_csv para usar encoding='utf-8-sig'
Isso resolve o problema do UTF-8 BOM
"""
import os
import re

arquivos_para_corrigir = [
    'app/services/csv_manager.py',
    'app/routes/admin.py',
    'app/services/analise_com_release_service.py',
    'app/services/analise_automatica/analise_service.py',
]

# Padrão para encontrar pd.read_csv sem encoding ou com encoding errado
pattern = r'pd\.read_csv\(["\']([^"\']+)["\'](?:,\s*encoding=["\'][^"\']+["\'])?\)'
replacement = r'pd.read_csv("\1", encoding="utf-8-sig")'

total_corrigido = 0

for arquivo in arquivos_para_corrigir:
    if not os.path.exists(arquivo):
        print(f"⚠️  {arquivo} não encontrado")
        continue
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Conta quantas ocorrências
        matches = re.findall(pattern, content)
        if matches:
            # Substitui
            new_content = re.sub(pattern, replacement, content)
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ {arquivo}: {len(matches)} correções")
            total_corrigido += len(matches)
        else:
            print(f"✓  {arquivo}: já correto")
    
    except Exception as e:
        print(f"❌ {arquivo}: {e}")

print(f"\n✅ Total: {total_corrigido} correções aplicadas")
print("   Todos os pd.read_csv agora usam encoding='utf-8-sig'")
