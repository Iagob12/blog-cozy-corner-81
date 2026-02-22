"""
Script para gerar hash de senha admin
"""
import hashlib

def gerar_hash(senha: str) -> str:
    """Gera hash SHA256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔐 GERADOR DE SENHA ADMIN")
    print("="*60)
    
    print("\nSenha atual: admin")
    print("Hash atual: 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918")
    
    print("\n" + "-"*60)
    print("Digite uma nova senha (ou Enter para manter 'admin'):")
    nova_senha = input("> ").strip()
    
    if not nova_senha:
        nova_senha = "admin"
        print("\n✓ Mantendo senha padrão: admin")
    else:
        print(f"\n✓ Nova senha: {nova_senha}")
    
    hash_gerado = gerar_hash(nova_senha)
    
    print("\n" + "="*60)
    print("HASH GERADO:")
    print("="*60)
    print(hash_gerado)
    
    print("\n" + "="*60)
    print("COMO USAR:")
    print("="*60)
    print("\n1. Copie o hash acima")
    print("\n2. Adicione no arquivo .env:")
    print(f"   ADMIN_PASSWORD_HASH={hash_gerado}")
    print("\n3. Reinicie o backend")
    print("\n4. Use a senha no login: " + nova_senha)
    print("\n" + "="*60)
    
    # Salva no .env automaticamente
    print("\nDeseja salvar automaticamente no .env? (s/n)")
    salvar = input("> ").strip().lower()
    
    if salvar == 's':
        try:
            # Lê .env atual
            env_path = ".env"
            try:
                with open(env_path, "r") as f:
                    linhas = f.readlines()
            except FileNotFoundError:
                linhas = []
            
            # Remove linha antiga se existir
            linhas_novas = [l for l in linhas if not l.startswith("ADMIN_PASSWORD_HASH=")]
            
            # Adiciona nova linha
            linhas_novas.append(f"ADMIN_PASSWORD_HASH={hash_gerado}\n")
            
            # Salva
            with open(env_path, "w") as f:
                f.writelines(linhas_novas)
            
            print(f"\n✓ Salvo em {env_path}")
            print("✓ Reinicie o backend para aplicar")
        except Exception as e:
            print(f"\n✗ Erro ao salvar: {e}")
            print("Adicione manualmente no .env")
    
    print("\n" + "="*60)
    print("✓ CONCLUÍDO")
    print("="*60 + "\n")
