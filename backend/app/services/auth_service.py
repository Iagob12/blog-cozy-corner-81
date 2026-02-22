"""
Serviço de Autenticação Admin
Sistema simples e seguro para admin
"""
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict
import hashlib
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """
    Autenticação simples para admin
    
    Features:
    - Login com senha
    - Token de sessão
    - Expiração automática
    """
    
    def __init__(self):
        # Senha admin (hash SHA256)
        # Senha padrão: "alpha2026" (você pode mudar no .env)
        self.admin_password_hash = os.getenv(
            "ADMIN_PASSWORD_HASH",
            "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"  # "admin"
        )
        
        # Tokens ativos (em memória)
        self.active_tokens: Dict[str, datetime] = {}
        
        # Duração do token: 24 horas
        self.token_duration = timedelta(hours=24)
        
        logger.info("✓ Auth Service inicializado")
    
    def _hash_password(self, password: str) -> str:
        """Gera hash SHA256 da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, password: str) -> Optional[Dict]:
        """
        Faz login do admin
        
        Args:
            password: Senha do admin
        
        Returns:
            Dict com token e expiração ou None se senha incorreta
        """
        # Verifica senha
        password_hash = self._hash_password(password)
        
        if password_hash != self.admin_password_hash:
            logger.warning("❌ Tentativa de login com senha incorreta")
            return None
        
        # Gera token
        token = secrets.token_urlsafe(32)
        expira_em = datetime.now() + self.token_duration
        
        # Salva token
        self.active_tokens[token] = expira_em
        
        logger.info("✓ Admin logado com sucesso")
        
        return {
            "token": token,
            "expira_em": expira_em.isoformat(),
            "tipo": "Bearer"
        }
    
    def validar_token(self, token: str) -> bool:
        """
        Valida se token é válido
        
        Args:
            token: Token de autenticação
        
        Returns:
            True se válido, False caso contrário
        """
        if token not in self.active_tokens:
            return False
        
        # Verifica expiração
        expira_em = self.active_tokens[token]
        
        if datetime.now() > expira_em:
            # Token expirado, remove
            del self.active_tokens[token]
            return False
        
        return True
    
    def logout(self, token: str):
        """Remove token (logout)"""
        if token in self.active_tokens:
            del self.active_tokens[token]
            logger.info("✓ Admin deslogado")
    
    def limpar_tokens_expirados(self):
        """Remove tokens expirados"""
        agora = datetime.now()
        tokens_expirados = [
            token for token, expira_em in self.active_tokens.items()
            if agora > expira_em
        ]
        
        for token in tokens_expirados:
            del self.active_tokens[token]
        
        if tokens_expirados:
            logger.debug(f"Removidos {len(tokens_expirados)} tokens expirados")
    
    def gerar_hash_senha(self, senha: str) -> str:
        """
        Utilitário para gerar hash de uma nova senha
        Use isso para criar o hash da sua senha personalizada
        """
        return self._hash_password(senha)


# Singleton
_auth_service: Optional[AuthService] = None


def get_auth_service() -> AuthService:
    """Retorna instância singleton"""
    global _auth_service
    
    if _auth_service is None:
        _auth_service = AuthService()
    
    return _auth_service
