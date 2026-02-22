"""
Corrige TODOS os encodings de uma vez
"""
import os
import re

def fix_file(filepath):
    """Corrige encoding em um arquivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substitui encoding='utf-8' por encoding='utf-8-sig' em opens
        original = content
        content = re.sub(
            r"open\(([^)]*),\s*'r',\s*encoding='utf-8'\)",
            r"open(\1, 'r', encoding='utf-8-sig')",
            content
        )
        content = re.sub(
            r'open\(([^)]*),\s*"r",\s*encoding="utf-8"\)',
            r'open(\1, "r", encoding="utf-8-sig")',
            content
        )
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Erro em {filepath}: {e}")
        return False

# Processa todos os arquivos Python
count = 0
for root, dirs, files in os.walk('app'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            if fix_file(filepath):
                print(f"✓ {filepath}")
                count += 1

print(f"\n✅ {count} arquivos corrigidos!")
