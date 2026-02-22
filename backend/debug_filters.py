import pandas as pd
from app.services.perfis_operacionais import PerfisOperacionais

df = pd.read_csv('data/stocks.csv')
print(f'Total inicial: {len(df)}')

# Aplica eliminação
df_filtrado, motivos = PerfisOperacionais.aplicar_eliminacao_imediata(df)
print(f'Após eliminação: {len(df_filtrado)}')
print('Motivos:', motivos)

# Testa Perfil A
print('\n--- TESTANDO PERFIL A ---')
print(f'ROE min: {PerfisOperacionais.PERFIL_A.roe_min}')
print(f'ROE max no df: {df_filtrado["roe"].max()}')
print(f'Empresas com ROE > 0.1:', len(df_filtrado[df_filtrado['roe'] > 0.1]))
print(f'Empresas com ROE > 10:', len(df_filtrado[df_filtrado['roe'] > 10]))

# Normaliza colunas
if 'Margem EBITDA' in df_filtrado.columns:
    df_filtrado['margem_ebitda'] = df_filtrado['Margem EBITDA']
if 'Dívida Líq. / EBITDA' in df_filtrado.columns:
    df_filtrado['divida_ebitda'] = df_filtrado['Dívida Líq. / EBITDA']
if 'ROIC' in df_filtrado.columns:
    df_filtrado['roic'] = df_filtrado['ROIC']

# Testa cada critério
print(f'\nCritérios Perfil A:')
print(f'ROE > 0.1: {len(df_filtrado[df_filtrado["roe"] > 0.1])} empresas')
print(f'P/L > 0 e < 20: {len(df_filtrado[(df_filtrado["pl"] > 0) & (df_filtrado["pl"] < 20)])} empresas')
print(f'ROIC > 0.08: {len(df_filtrado[df_filtrado["roic"] > 0.08])} empresas')
print(f'Dívida/EBITDA < 3.5: {len(df_filtrado[df_filtrado["divida_ebitda"] < 3.5])} empresas')
print(f'Margem EBITDA > 0.08: {len(df_filtrado[df_filtrado["margem_ebitda"] > 0.08])} empresas')

# Testa filtro completo
df_a = PerfisOperacionais.filtrar_por_perfil(df_filtrado, 'A')
print(f'\nPerfil A final: {len(df_a)} empresas')

# Mostra algumas empresas que passaram
if len(df_a) > 0:
    print('\nEmpresas que passaram:')
    print(df_a[['ticker', 'roe', 'pl', 'roic', 'divida_ebitda', 'margem_ebitda']].head(10))
