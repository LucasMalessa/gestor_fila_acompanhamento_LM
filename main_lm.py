# %% [markdown]
# ### Importando bibliotecas

# %%
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import datetime, time, timedelta
from datetime import timedelta, time
import os

# %% [markdown]
# ### Criando arquivo contador de atualizações

# %%
# Nome do arquivo auxiliar
filename = 'arquivos_auxiliares/contador_atualizacoes.txt'


# Função para ler o dia e o contador do arquivo
def ler_dados():
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            linha = file.readline().strip()
            if linha:
                dia, contador = linha.split(',')
                return dia, int(contador)
    return None, 0

# Função para escrever o dia e o contador no arquivo
def escrever_dados(dia, contador):
    with open(filename, 'w') as file:
        file.write(f"{dia},{contador}")

# Função para atualizar o contador
def atualizar_contador():
    dia_atual = datetime.now().strftime('%Y-%m-%d')
    dia_armazenado, contador = ler_dados()

    # Verifica se o dia atual é diferente do dia armazenado
    if dia_armazenado != dia_atual:
        contador = 0  # Zera o contador se for um novo dia

    contador += 1  # Incrementa o contador
    escrever_dados(dia_atual, contador)  # Atualiza o arquivo

    return contador  # Retorna o contador atualizado

# Função para obter o contador atual
def obter_contagem_atualizacoes_dia():
    _, contador = ler_dados()  # Lê o contador do arquivo
    return contador  # Retorna o contador

# Exemplo de uso
if __name__ == "__main__":
    # Atualiza o contador e imprime o número de atualizações
    contagem_atualizacoes_dia = atualizar_contador()
    print(f"Atualizações hoje: {contagem_atualizacoes_dia}")

    # Você pode chamar obter_contagem_atualizacoes_dia em qualquer parte do seu código
    contador_atual = obter_contagem_atualizacoes_dia()
    print(f"Contagem atual de atualizações: {contador_atual}")

# %%
contagem_atualizacoes_dia

# %% [markdown]
# ### Importando arquivos

# %% [markdown]
# #### Importando arquivo relatorioAcompanhamento

# %%
# Função para buscar relatorioAcompanhamento.csv automaticamente no OneDrive
def buscar_relatorio_acompanhamento():
    user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
    onedrive_dir = os.path.join(user_profile, 'OneDrive - EDENRED')
    
    if not os.path.isdir(onedrive_dir):
        raise FileNotFoundError(f"Pasta OneDrive não encontrada: {onedrive_dir}")
    
    # Busca o arquivo em todas as subpastas do OneDrive (1 nível)
    for pasta in os.listdir(onedrive_dir):
        caminho = os.path.join(onedrive_dir, pasta, 'relatorioAcompanhamento.csv')
        if os.path.isfile(caminho):
            print(f"Arquivo encontrado em: {caminho}")
            return caminho
    
    raise FileNotFoundError(
        f"relatorioAcompanhamento.csv não encontrado em nenhuma subpasta de: {onedrive_dir}\n"
        f"Verifique se a pasta do OneDrive/SharePoint com os dados de acompanhamento está sincronizada."
    )

caminho_acompanhamento = buscar_relatorio_acompanhamento()
df_acompanhamento = pd.read_csv(caminho_acompanhamento, encoding='ISO-8859-1', sep=';')

df_acompanhamento.info()

# %% [markdown]
# #### Importando arquivo clientes

# %%
df_clientes = pd.read_excel('arquivos_gestao/bases_acompanhamento.xlsx',sheet_name='informacao_adicional')

df_clientes.info()

# %% [markdown]
# #### Importando arquivo agentes

# %%
df_agentes = pd.read_excel('arquivos_gestao/agentes_acompanhamento.xlsx',sheet_name='lista_colaboradores')

df_agentes.info()

# %% [markdown]
# #### Importando arquivo placas

# %%
df_placas = pd.read_csv('arquivos_gestao/placas.csv', sep=',')

df_placas.info()

# %% [markdown]
# ### Definindo variáveis

# %%
# Assuming feriados_brasil is a list of holidays
feriados_brasil = pd.to_datetime([
    # 2024
    '2024-01-01',  # Confraternização Universal
    '2024-03-29',  # Sexta-feira Santa
    '2024-04-21',  # Tiradentes
    '2024-05-01',  # Dia do Trabalho
    '2024-06-15',  # Corpus Christi
    '2024-09-07',  # Independência do Brasil
    '2024-10-12',  # Nossa Senhora Aparecida
    '2024-11-02',  # Finados
    '2024-11-20',  # Consciência Negra
    '2024-11-15',  # Proclamação da República
    '2024-12-25',  # Natal
    # 2025
    '2025-01-01',  # Confraternização Universal
    '2025-04-18',  # Sexta-feira Santa
    '2025-04-21',  # Tiradentes
    '2025-05-01',  # Dia do Trabalho
    '2025-06-19',  # Corpus Christi
    '2025-09-07',  # Independência do Brasil
    '2025-10-12',  # Nossa Senhora Aparecida
    '2025-11-02',  # Finados
    '2025-11-20',  # Consciência Negra
    '2025-11-15',  # Proclamação da República
    '2025-12-25',  # Natal
])
feriados_brasil = pd.to_datetime(feriados_brasil).date



# Definindo hora atual
hora_atual = pd.Timestamp.now()




# Função para determinar o turno
def determinar_turno(hora):
    if hora.hour < 12 or (hora.hour == 12 and hora.minute == 0):
        return "Turno 1"
    else:
        return "Turno 2"

turno_atual = determinar_turno(hora_atual)

print("Turno atual:", turno_atual)
print("Hora atual:", hora_atual)


# %% [markdown]
# ### Transformação de dados

# %% [markdown]
# #### Filtrando dados

# %%
# Filtrando colunas importantes
lista_colunas_acompanhamento = [
    'Protocolo (BD)','Número OS','Informação Adicional 2','Placa','Código Cliente','Nome do Cliente','Situação de Disponibilidade Protocolo','Dias Indisponível','Código Estabelecimento','Nome Estabelecimento','Cidade','UF','Tipo de Manutenção','Data Agendada','Data da Parada','Data Primeiro Envio da OS','Data Aprovação da OS','Status do Protocolo','Próximo Acompanhamento','Valor OS','Acompanhamentos','Status OS','Observação','Tipo de Frota'
    ]
df = df_acompanhamento[lista_colunas_acompanhamento]


# Filtrando código LM 
df = df[df['Código Cliente'] == 223309]

# # Removendo Oficina Interna 
# df = df[df['Nome Estabelecimento'] != 'OFICINA INTERNA PLATAFORMA ECOFROTAS3']

# Filtrando Status do Protocolo diferente de 'Orçamento em Aprovação' 
df = df[df['Status do Protocolo'] != 'Orçamento em Aprovação']


# df


# %% [markdown]
# #### Trazendo informações

# %%
# Trazendo informação do fator multiplicador e Fila
df = df.merge(df_clientes[['Fila','IA 2']], left_on='Informação Adicional 2', right_on='IA 2', how='left')
df = df.drop(columns=['IA 2'])

# Trazendo informação de familia veículo
df = df.merge(df_placas[['LicensePlate', 'MaintenanceModelFamily']], left_on='Placa', right_on='LicensePlate', how='left')
df = df.drop(columns=['LicensePlate'])
df = df.rename(columns={'MaintenanceModelFamily': 'MaintenanceModelFamily'})

# df


# %% [markdown]
# #### Criando coluna Sublocado

# %%
# Criando coluna Sublocado
df['Sublocado'] = df['Observação'].apply(lambda x: 'SIM' if x == 'SIM' else None)

# Remover as coluna Observação
df = df.drop(columns=['Observação'])

# df

# %% [markdown]
# #### Corrigindo filas

# %%
# # Criando Fila BRF Sublocados
# # Sublocados
# df.loc[(df['Informação Adicional 2'] == 'BRF') & (df['Sublocado'] == 'SIM' ), 'Fila'] = 'BRF - Sublocados'



# Criando Fila ICOMON Sinistro Veículos Prioritários
# Sinistro 
df.loc[(df['Informação Adicional 2'] == 'ICOMON') & (df['Tipo de Manutenção'] == 'Sinistro' ), 'Fila'] = 'ICOMON - Sinistro'
df.loc[(df['Informação Adicional 2'] == 'ICOMON') & (df['Tipo de Manutenção'] == 'Sinistro LM' ), 'Fila'] = 'ICOMON - Sinistro'
df.loc[(df['Informação Adicional 2'] == 'CSR') & (df['Tipo de Manutenção'] == 'Sinistro' ), 'Fila'] = 'ICOMON - Sinistro'
df.loc[(df['Informação Adicional 2'] == 'CSR') & (df['Tipo de Manutenção'] == 'Sinistro LM' ), 'Fila'] = 'ICOMON - Sinistro'
df.loc[(df['Informação Adicional 2'] == 'CSR ENGENHARIA LTDA') & (df['Tipo de Manutenção'] == 'Sinistro' ), 'Fila'] = 'ICOMON - Sinistro'
df.loc[(df['Informação Adicional 2'] == 'CSR ENGENHARIA LTDA') & (df['Tipo de Manutenção'] == 'Sinistro LM' ), 'Fila'] = 'ICOMON - Sinistro'


# # Veículos Prioritários
# df.loc[(df['Informação Adicional 2'] == 'ICOMON') & (df['Tipo de Frota'] == 'PRIORITARIA' ), 'Fila'] = 'ICOMON - Prioritários'


# Criando Fila RECALL
df['Fila'] = df.apply(lambda row: 'RECALL' if row['Código Estabelecimento'] == 8725675 else row['Fila'], axis=1)
df['Fila'] = df.apply(lambda row: 'RECALL' if row['Nome Estabelecimento'] == 'OFICINA INTERNA PLATAFORMA ECOFROTAS3' else row['Fila'], axis=1)

# Filtrando protocolos que a IA2 está numa Fila
df = df[df['Fila'].notna()]

df1 = df
# df1


# %% [markdown]
# #### Convertendo colunas

# %%
# Converter as colunas para datetime, tratando erros
# Convertendo colunas para datas
colunas_a_converter = [
       'Data Agendada',
       'Data da Parada',
       'Data Primeiro Envio da OS',
       'Data Aprovação da OS',
       'Próximo Acompanhamento',
        ]

# Converter as colunas para datetime
for coluna in colunas_a_converter:
        df[coluna] = pd.to_datetime(df[coluna], format='%d/%m/%Y %H:%M:%S')#,errors='coerce')


# Convertendo colunas para object
df['Protocolo (BD)'] = df['Protocolo (BD)'].astype(object)
df['Código Cliente'] = df['Código Cliente'].astype(object)
df['Código Estabelecimento'] = df['Código Estabelecimento'].astype(object)


# Remover 'R$' e substituir a vírgula por ponto
df['Valor OS'] = df['Valor OS'].str.split(' ', n=1).str[1]
# Transformando a coluna em float
df['Valor OS'] = df['Valor OS'].str.replace('.', '', regex=False)  # Remove os pontos
df['Valor OS'] = df['Valor OS'].str.replace(',', '.', regex=False)  # Substitui a vírgula por ponto
df['Valor OS'] = df['Valor OS'].astype(float)  # Converte para float

# df

# %% [markdown]
# ### Criando colunas

# %% [markdown]
# #### Coluna família veículo

# %%
# Criando coluna familia veiculo
df['familia_veiculo'] = np.where(df['MaintenanceModelFamily'].str.contains('Caminhao Pesado'), 'Caminhao Pesado'
    ,np.where(df['MaintenanceModelFamily'].str.contains('Caminhao'), 'Caminhao'
        ,np.where(df['MaintenanceModelFamily'].str.contains('Pickup Pesada'), 'Pickup Pesada'
            ,np.where(df['MaintenanceModelFamily'].str.contains('Pickup Media'), 'Pickup Media'
                ,np.where(df['MaintenanceModelFamily'].str.contains('Pickup Media'), 'Pickup Media'
                    ,np.where(df['MaintenanceModelFamily'].str.contains('Pickup Leve'), 'Pickup Leve'
                        ,np.where(df['MaintenanceModelFamily'].str.contains('Van'), 'Van'
                            ,np.where(df['MaintenanceModelFamily'].str.contains('Moto'), 'Moto'
                                ,np.where(df['MaintenanceModelFamily'].str.contains('Leve'), 'Leve'
                                    ,np.where(df['MaintenanceModelFamily'].str.contains('Equipamento'), 'Equipamento'
                                        ,np.where(df['MaintenanceModelFamily'].str.contains('Implemento'), 'Caminhao'
                                            ,np.where(df['MaintenanceModelFamily'].str.contains('Onibus'), 'Caminhao'
                                                ,np.where(df['MaintenanceModelFamily'].str.contains('Reboque'), 'Caminhao'
                                                    ,np.where(df['MaintenanceModelFamily'].str.contains('Suv'), 'Pickup Pesada'
                                                        ,np.where(df['MaintenanceModelFamily'].str.contains('Micro Onibus'), 'Caminhao'
                                                            ,np.where(df['MaintenanceModelFamily'].str.contains('Quadriciclo'), 'Moto'
                                                                ,np.where(df['MaintenanceModelFamily'].str.contains('Utilitario'), 'Van'    
                              
             
, 'Leve')))))))))))))))))

# df

# %%
df = df[(df['Data da Parada'] > '2000-01-01') | (df['Data Agendada'] > '2000-01-01')]

# df

# %% [markdown]
# #### Coluna Etapa atual
# 

# %%
# Função para definir a Etapa Atual
def definir_etapa(row):
    if pd.isna(row['Data da Parada']):
        return 'No Show'
    elif pd.isna(row['Data Primeiro Envio da OS']):
        return 'Diagnóstico'
    elif pd.isna(row['Data Aprovação da OS']):
        return 'Aprovação'
    else:
        return 'Execução do serviço'

# Aplicar a função para criar a nova coluna 'ETAPA ATUAL'
df['Etapa Atual'] = df.apply(definir_etapa, axis=1)

# df

# %% [markdown]
# #### SLA No Show

# %%
# Criando coluna SLA No Show

def calcular_sla_no_show(row):
    if row['Etapa Atual'] == 'No Show':
        # Calcular a diferença em horas entre hora_atual e Data Agendada
        return (hora_atual - row['Data Agendada']).total_seconds() / 3600  # Convertendo para horas
    else:
        return None

# Aplicar a função para criar a nova coluna 'SLA No Show'
df['SLA No Show'] = df.apply(calcular_sla_no_show, axis=1)

# Formatando a coluna 'SLA No Show' para 1 casa decimal
df['SLA No Show'] = df['SLA No Show'].round(1)

# df

# %% [markdown]
# #### SLA Diagnóstico

# %%
# Criando coluna SLA Diagnóstico

def calcular_sla_no_show(row):
    if row['Etapa Atual'] == 'Diagnóstico':
        # Calcular a diferença em horas entre hora_atual e Data Agendada
        return (hora_atual - row['Data da Parada']).total_seconds() / 3600  # Convertendo para horas
    else:
        return None

# Aplicar a função para criar a nova coluna 'SLA Diagnóstico'
df['SLA Diagnóstico'] = df.apply(calcular_sla_no_show, axis=1)

# Formatando a coluna 'SLA Diagnóstico' para 1 casa decimal
df['SLA Diagnóstico'] = df['SLA Diagnóstico'].round(1)

# df

# %% [markdown]
# #### SLA Execução

# %%
# Criando coluna SLA Execução

def calcular_sla_no_show(row):
    if row['Etapa Atual'] == 'Execução do serviço':
        # Calcular a diferença em horas entre hora_atual e Data Agendada
        return (hora_atual - row['Data Aprovação da OS']).total_seconds() / 3600  # Convertendo para horas
    else:
        return None

# Aplicar a função para criar a nova coluna 'SLA Execução'
df['SLA Execução'] = df.apply(calcular_sla_no_show, axis=1)

# Formatando a coluna 'SLA Execução' para 1 casa decimal
df['SLA Execução'] = df['SLA Execução'].round(1)

# df

# %% [markdown]
# #### Coluna Tipo de Solicitação

# %%
# Criando tabela tipo_solicitacao
def tipo_manutencao(row):
    if row['Tipo de Manutenção'] =='Manutenção Preventiva':
        return 'Preventiva'
    else:
        return 'Corretiva'
df['tipo_solicitacao'] = df.apply(tipo_manutencao, axis=1)

# df

# %% [markdown]
# #### Coluna monta

# %%
def classificar_monta(row):
    if pd.isnull(row['Valor OS']):
        return None
    elif row['tipo_solicitacao'] == 'Preventiva':
        return 'Preventiva'
    elif (row['familia_veiculo'] == 'Caminhao Pesado' and row['Valor OS'] > 35000 ) or \
         (row['familia_veiculo'] == 'Caminhao' and row['Valor OS'] > 15000) or \
         (row['familia_veiculo'] == 'Pickup Pesada' and row['Valor OS'] > 15000) or \
         (row['familia_veiculo'] == 'Equipamento' and row['Valor OS'] > 15000) or \
         (row['familia_veiculo'] == 'Pickup Media' and row['Valor OS'] > 10000) or \
         (row['familia_veiculo'] == 'Pickup Leve' and row['Valor OS'] > 7000) or \
         (row['familia_veiculo'] == 'Van' and row['Valor OS'] > 15000) or \
         (row['familia_veiculo'] == 'Leve' and row['Valor OS'] > 6000) or \
         (row['familia_veiculo'] == 'Moto' and row['Valor OS'] > 2000):
        return 'alta monta'
    elif (row['familia_veiculo'] == 'Caminhao Pesado' and row['Valor OS'] <= 35000 and row['Valor OS'] > 15000) or \
         (row['familia_veiculo'] == 'Caminhao' and row['Valor OS'] <= 15000 and row['Valor OS'] > 5000) or \
         (row['familia_veiculo'] == 'Pickup Pesada' and row['Valor OS'] <= 15000 and row['Valor OS'] > 5000) or \
         (row['familia_veiculo'] == 'Equipamento' and row['Valor OS'] <= 15000 and row['Valor OS'] > 5000) or \
         (row['familia_veiculo'] == 'Pickup Media' and row['Valor OS'] <= 10000 and row['Valor OS'] > 3000) or \
         (row['familia_veiculo'] == 'Pickup Leve' and row['Valor OS'] <= 7000 and row['Valor OS'] > 2000) or \
         (row['familia_veiculo'] == 'Van' and row['Valor OS'] <= 15000 and row['Valor OS'] > 5000) or \
         (row['familia_veiculo'] == 'Leve' and row['Valor OS'] <= 6000 and row['Valor OS'] > 1500) or \
         (row['familia_veiculo'] == 'Moto' and row['Valor OS'] <= 2000 and row['Valor OS'] > 600):
        return 'media monta'
    elif pd.notna(row['familia_veiculo']):
        return 'baixa monta'
    else:
        return None  # Retorna None para deixar vazio
    

# Aplicando a função ao DataFrame
df['classificacao_monta'] = df.apply(classificar_monta, axis=1)

# df

# %% [markdown]
# #### Prazo No Show

# %%
########################### Regras para o prazo de No Show #############################
# BRF ou ICOMON = 2h
# PROSEGUR ou ENEL = 12h
# Outros = 4h
########################################################################################

# Função para definir o Prazo No Show
def definir_prazo_no_show(base):
    if base in ['BRF', 'ICOMON']:                         
        return 2
    if base in ['PROSEGUR','PROSEGUR I','PROSEGUR II','ENEL']:
        return 12
    else:
        return 4

# Aplicar a função para criar a nova coluna 'Prazo No Show'
df['Prazo No Show'] = df['Informação Adicional 2'].apply(definir_prazo_no_show)

# df

# %% [markdown]
# #### Prazo Diagnóstico

# %%
########################### Regras para o prazo de Diagnóstico #############################
# PREVENTIVAS
# BRF = 1h
# COPASA ou PROSEGUR = 2h
# Outros = 2h

# CORRETIVAS
# BRF, COPASA  ou PROSEGUR = 2h
# Outros = 4h
############################################################################################



# Função para definir o Prazo Diagnóstico Preventiva
def definir_prazo_diagnostico(row):
    if row['tipo_solicitacao'] == 'Preventiva' and row['Informação Adicional 2'] == 'BRF':
        return 1
    elif row['tipo_solicitacao'] == 'Preventiva' and row['Informação Adicional 2'] in ['COPASA', 'PROSEGUR']:
        return 2
    elif row['tipo_solicitacao'] == 'Preventiva':
        return 2
    elif row['tipo_solicitacao'] == 'Corretiva' and row['Informação Adicional 2'] in ['BRF', 'COPASA', 'PROSEGUR']:
        return 2
    else:
        return 4  # Retorna None para deixar vazio

# Aplicar a função para criar a nova coluna 'Prazo Diagnóstico'
df['Prazo Diagnóstico'] = df.apply(definir_prazo_diagnostico, axis=1)


# df

# %% [markdown]
# #### Prazo Execução

# %% [markdown]
# ##### Tempo padrão execução - Célula Técnina

# %%
# Função para definir o Tempo padrão de execução definido pela Célula Técnica
def definir_prazo_execucao_tempo_padrao(row):
    ############################################################### Caminhao
    if (
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Caminhao') & 
        (row['classificacao_monta'] == 'alta monta') 
    ):
        return 40
        
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Caminhao') & 
        (row['classificacao_monta'] == 'media monta') 
    ):
        return 24
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Caminhao') & 
        (row['classificacao_monta'] == 'baixa monta') 
    ):
        return 8
    ############################################################### Caminhao Pesado
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Caminhao Pesado') & 
        (row['classificacao_monta'] == 'alta monta') 
    ):
        return 56
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Caminhao Pesado') & 
        (row['classificacao_monta'] == 'media monta') 
    ):
        return 32
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Caminhao Pesado') & 
        (row['classificacao_monta'] == 'baixa monta') 
    ):
        return 12
    ############################################################### Leve
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Leve') & 
        (row['classificacao_monta'] == 'alta monta') 
    ):
        return 30
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Leve') & 
        (row['classificacao_monta'] == 'media monta') 
    ):
        return 17
    
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Leve') & 
        (row['classificacao_monta'] == 'baixa monta') 
    ):
        return 4
    ############################################################### Moto
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Moto') & 
        (row['classificacao_monta'] == 'alta monta') 
    ):
        return 15
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Moto') & 
        (row['classificacao_monta'] == 'media monta') 
    ):
        return 9
    
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Moto') & 
        (row['classificacao_monta'] == 'baixa monta') 
    ):
        return 3
    ############################################################### Pickup Leve
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Pickup Leve') & 
        (row['classificacao_monta'] == 'alta monta') 
    ):
        return 30
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Pickup Leve') & 
        (row['classificacao_monta'] == 'media monta') 
    ):
        return 20
    
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Pickup Leve') & 
        (row['classificacao_monta'] == 'baixa monta') 
    ):
        return 4
    ############################################################### Pickup Media
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Pickup Media') & 
        (row['classificacao_monta'] == 'alta monta') 
    ):
        return 35
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Pickup Media') & 
        (row['classificacao_monta'] == 'media monta') 
    ):
        return 22
    
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Pickup Media') & 
        (row['classificacao_monta'] == 'baixa monta') 
    ):
        return 6
    ############################################################### Pickup Pesada ou Equipamento
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        ((row['familia_veiculo'] == 'Pickup Pesada') | (row['familia_veiculo'] == 'Equipamento')) & 
        (row['classificacao_monta'] == 'alta monta') 
    ):
        return 38
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        ((row['familia_veiculo'] == 'Pickup Pesada') | (row['familia_veiculo'] == 'Equipamento')) & 
        (row['classificacao_monta'] == 'media monta') 
    ):
        return 23
    
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        ((row['familia_veiculo'] == 'Pickup Pesada') | (row['familia_veiculo'] == 'Equipamento')) & 
        (row['classificacao_monta'] == 'baixa monta') 
    ):
        return 8
    ############################################################### Van
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Van') & 
        (row['classificacao_monta'] == 'alta monta') 
    ):
        return 38
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Van') & 
        (row['classificacao_monta'] == 'media monta') 
    ):
        return 22
    
    elif(
        (row['tipo_solicitacao'] == 'Corretiva') & 
        (row['familia_veiculo'] == 'Van') & 
        (row['classificacao_monta'] == 'baixa monta') 
    ):
        return 8
    ############################################################### Preventivas
    elif(
        (row['tipo_solicitacao'] == 'Preventiva') & 
        (row['familia_veiculo'] == 'Caminhao') 
    ):
        return 10
    elif(
        (row['tipo_solicitacao'] == 'Preventiva') & 
        (row['familia_veiculo'] == 'Caminhao Pesado') 
    ):
        return 11
    elif(
        (row['tipo_solicitacao'] == 'Preventiva') & 
        (row['familia_veiculo'] == 'Leve') 
    ):
        return 2.2
    elif(
        (row['tipo_solicitacao'] == 'Preventiva') & 
        (row['familia_veiculo'] == 'Moto') 
    ):
        return 1.5
    elif(
        (row['tipo_solicitacao'] == 'Preventiva') & 
        (row['familia_veiculo'] == 'Pickup Leve') 
    ):
        return 2.4
    elif(
        (row['tipo_solicitacao'] == 'Preventiva') & 
        (row['familia_veiculo'] == 'Pickup Media') 
    ):
        return 2.8
    elif(
        (row['tipo_solicitacao'] == 'Preventiva') & 
        ((row['familia_veiculo'] == 'Pickup Pesada') | (row['familia_veiculo'] == 'Equipamento')) 
    ):
        return 2.9
    elif(
        (row['tipo_solicitacao'] == 'Preventiva') & 
        (row['familia_veiculo'] == 'Van') 
    ):
        return 3.7
    else:
        return None  # Retorna None para deixar vazio

# Aplicar a função para criar a nova coluna 'Prazo Execução Tempo Padrão Célula Técnica'
df['Prazo Execução Tempo Padrão Célula Técnica'] = df.apply(definir_prazo_execucao_tempo_padrao, axis=1)

# df

# %% [markdown]
# ##### Prazo Real Execução

# %%
########################### Regras para o prazo de Execução #############################
# PREVENTIVAS
# BRF, COPASA ou PROSEGUR = 2h OK
# Outros = Gold (1x tempo célula técnica) OK

# CORRETIVAS
# BRF (Baixa Monta), COPASA, PROSEGUR = 2h OK
# BRF (Media ou Alta Monta) = 4h OK
# ICOMON (Media ou Alta Monta), GEQ (Media ou Alta Monta), WURTH (Media ou Alta Monta) = Diamond (1x tempo célula técnica) OK
# Outros = Gold (1x tempo célula técnica)
############################################################################################




# Função para definir o Prazo Real Execução
def definir_prazo_real_execuca(row):
    ### Preventivas
    if row['tipo_solicitacao'] == 'Preventiva' and row['Informação Adicional 2'] in ['BRF', 'COPASA', 'PROSEGUR'] and row['classificacao_monta'] is not None:
        return 2
    elif row['tipo_solicitacao'] == 'Preventiva' and row['classificacao_monta'] is not None:
        return row['Prazo Execução Tempo Padrão Célula Técnica']

    ### Corretivas
    elif row['tipo_solicitacao'] == 'Corretiva' and row['classificacao_monta'] == 'baixa monta' and row['Informação Adicional 2'] == 'BRF':
        return 2
    elif row['tipo_solicitacao'] == 'Corretiva' and row['Informação Adicional 2'] in ['COPASA', 'PROSEGUR'] and row['classificacao_monta'] is not None:
        return 2
    elif row['tipo_solicitacao'] == 'Corretiva' and row['classificacao_monta']  in ['media monta','alta monta'] and row['Informação Adicional 2'] == 'BRF':
        return 4
    elif row['tipo_solicitacao'] == 'Corretiva' and row['classificacao_monta'] in ['media monta','alta monta'] and row['Informação Adicional 2'] in ['ICOMON', 'GEQ', 'WURTH']:
        return (row['Prazo Execução Tempo Padrão Célula Técnica'] * 0.5) 
    elif row['classificacao_monta'] is not None:
        return row['Prazo Execução Tempo Padrão Célula Técnica']
    else:
        return None  # Retorna None para deixar vazio

# Aplicar a função para criar a nova coluna 'Prazo Diagnóstico'
df['Prazo Real Execução'] = df.apply(definir_prazo_real_execuca, axis=1)

# df

# %% [markdown]
# #### Coluna com Total de Acompanhamentos no Protocolo

# %%
# Contando o total de Acompanhamentos no Protocolo com base na repetição do texto "[ Data Cadastro:"
df['Total de Acompanhamentos'] = df['Acompanhamentos'].str.count(r'\[ Data Cadastro:')

# df


# %% [markdown]
# #### Status Próximo Acompanhamento

# %%
# Função para gerar o status do próximo acompanhamento
def gerar_status(data_acompanhamento):
    if pd.isna(data_acompanhamento):
        return "Sem Acompanhamento"
    
    if data_acompanhamento.date() < hora_atual.date():
        return "Atraso >= 1 dia"
    
    if data_acompanhamento.date() == hora_atual.date():
        if data_acompanhamento < hora_atual:
            return "Atrasado"
        elif determinar_turno(data_acompanhamento) == turno_atual:
            return "Acompanhar no turno"
        else:
            return "Acompanhar no próximo turno"
    
    return None
# Aplicar a função
df['Status Próximo Acompanhamento'] = df['Próximo Acompanhamento'].apply(gerar_status)

# df

# %% [markdown]
# ### Filtrando protocolos a serem acompanhados

# %% [markdown]
# #### Filtro pela etapa ou Fila Recall

# %%
# Filtrar protocolos onde o SLA passou o prazo da etapa ou a Fila é RECALL
df = df[
    # Gatilho na etapa No Show
    ((df['Etapa Atual'] == 'No Show') & (df['SLA No Show'] >= df['Prazo No Show'])) |

    # Gatilho na etapa Diagnóstico
    ((df['Etapa Atual'] == 'Diagnóstico') & (df['SLA Diagnóstico'] >= df['Prazo Diagnóstico'])) |

    # Gatilho na etapa Execução
    ((df['Etapa Atual'] == 'Execução do serviço') & (df['SLA Execução'] >= df['Prazo Real Execução'])) |

    # Fila RECALL
    (df['Fila'] == 'RECALL') |

    #Filtro de BRF, Preventiva e Imobilizado há 4 horas ou mais
    ((df['Informação Adicional 2'] == 'BRF') & (df['tipo_solicitacao'] == 'Preventiva') & ((df['SLA Diagnóstico'] + df['SLA Execução']) > 4))
]

# df_teste = df
# df_teste

# %% [markdown]
# #### Filtro acompanhamento amanhã ou depois

# %%
# Removendo casos onde o próximo acompanhamento é depois do dia atual

# Definindo 'amanha' como 00:00 do dia seguinte
amanha = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
# Filtrando os casos onde o próximo acompanhamento é maior ou igual a 'amanha'
acomp_amanha = df[df['Próximo Acompanhamento'] >= amanha]
# Removendo os protocolos que estão em 'acomp_amanha'
df = df[~df['Protocolo (BD)'].isin(acomp_amanha['Protocolo (BD)'])]

df

# %% [markdown]
# ### Resultados

# %% [markdown]
# #### Por Status

# %%
df_por_status = df.groupby('Status do Protocolo')['Protocolo (BD)'].nunique().reset_index()
df_por_status = df_por_status.sort_values(by='Protocolo (BD)', ascending=False)

df_por_status

# %% [markdown]
# #### Por Informação Adicional

# %%
df_ia2 = df.groupby('Informação Adicional 2')['Protocolo (BD)'].nunique().reset_index()
df_ia2 = df_ia2.sort_values(by='Protocolo (BD)', ascending=False)

df_ia2

# %% [markdown]
# #### Por Fila

# %%
df_fila = df.groupby('Fila')['Protocolo (BD)'].nunique().reset_index()
df_fila = df_fila.sort_values(by='Protocolo (BD)', ascending=False)

df_fila

# %% [markdown]
# ### Distribuição de protocolos

# %% [markdown]
# #### Função 1

# %%
df2 = df

# %%
def atualizar_dataframe(df2, df_agentes):
    # Passo 1: Contar quantos estabelecimentos distintos existem por Fila
    estabelecimentos_por_fila = df2.groupby(['Código Estabelecimento', 'Fila']).size().reset_index(name='Contagem')

    # Passo 2: Obter lista de agentes disponíveis por Fila
    agentes_por_fila = df_agentes.groupby('Fila')['Nome'].apply(list).to_dict()

    # Passo 3: Distribuir os agentes de forma equitativa para cada Código Estabelecimento dentro de cada Fila
    atribuicao = {}
    for fila, estabelecimentos in estabelecimentos_por_fila.groupby('Fila'):
        agentes = agentes_por_fila.get(fila, [])  # Lista de agentes disponíveis para essa fila
        num_agentes = len(agentes)
        estabelecimentos_lista = estabelecimentos['Código Estabelecimento'].tolist()
        
        # Atribuir um agente a cada estabelecimento de forma circular
        for i, estabelecimento in enumerate(estabelecimentos_lista):
            if num_agentes > 0:
                atribuicao[(estabelecimento, fila)] = agentes[i % num_agentes]
            else:
                atribuicao[(estabelecimento, fila)] = None  # Caso não haja agentes

    # Passo 4: Atualizar o df2 com a nova coluna "Nome"
    df2_atualizado = df2.copy()  # Criar uma cópia do DataFrame original
    df2_atualizado['Nome'] = df2_atualizado.apply(lambda row: atribuicao.get((row['Código Estabelecimento'], row['Fila']), None), axis=1)

    # Resultado final: Agrupar e contar os protocolos únicos
    contagem_distinta = df2_atualizado.groupby(['Fila', 'Nome Estabelecimento', 'Nome'])['Protocolo (BD)'].nunique().reset_index(name='Contagem')

    # Manter apenas o nome com a maior contagem por Fila e Nome Estabelecimento
    resultado = contagem_distinta.loc[contagem_distinta.groupby(['Fila', 'Nome Estabelecimento'])['Contagem'].idxmax()]

    # Ordenar o resultado, se necessário
    resultado = resultado.sort_values(by='Nome', ascending=False)

    # Atualizar df2_atualizado com o resultado final
    df2_atualizado = df2_atualizado.merge(resultado[['Nome Estabelecimento', 'Fila', 'Nome']], on=['Nome Estabelecimento', 'Fila'], how='left')

    # Removendo coluna Nome_x
    df2_atualizado.drop('Nome_x', axis=1, inplace=True)

    # Atualizar Nome df2
    df2_atualizado.rename(columns={'Nome_y': 'Nome'}, inplace=True)

    # Criar relação entre Fila, Nome e Código Estabelecimento
    relacao_fila_ec_agente = df2_atualizado.groupby(['Fila', 'Nome', 'Código Estabelecimento'])['Protocolo (BD)'].nunique().reset_index()
    relacao_fila_ec_agente = relacao_fila_ec_agente.drop(columns=['Protocolo (BD)'])
    
    # Exportar para CSV
    df2_atualizado.to_csv('arquivos_painel/protocolos_agente.csv', sep=';', index=False, encoding='utf-8')

    # Exportar para CSV
    relacao_fila_ec_agente.to_csv('arquivos_auxiliares/relacao_fila_ec_agente.csv', sep=';', index=False, encoding='utf-8')

    # Retornar o DataFrame atualizado e a relação criada
    return df2_atualizado, relacao_fila_ec_agente

# %% [markdown]
# #### Função 2

# %%
# Importando arquivo gerado na Função 1
relacao_fila_ec_agente = pd.read_csv('arquivos_auxiliares/relacao_fila_ec_agente.csv', encoding='utf-8',sep=';')

# Criando df3 sem coluna Nome
df3 = df

# Trazendo a infromação de Nome
df3 = df3.merge(relacao_fila_ec_agente[['Fila', 'Código Estabelecimento', 'Nome']], on=['Fila', 'Código Estabelecimento'], how='left')

# Filtrando protocolos sem nome
df4 = df3[df3['Nome'].isnull()]

# %%
# df4.head()

# %%
# Verificando quantidade de protocolos atrelado para cada agente
protocolos_por_agente = df3.groupby(['Fila','Nome'])['Protocolo (BD)'].nunique().reset_index()
protocolos_por_agente = protocolos_por_agente.sort_values(by='Protocolo (BD)', ascending=False)

# %%
# protocolos_por_agente.head()

# %%
def primeira_parte():
    # Importando arquivo gerado na Função 1
    relacao_fila_ec_agente = pd.read_csv('arquivos_auxiliares/relacao_fila_ec_agente.csv', encoding='utf-8',sep=';')

    # Criando df3 sem coluna Nome
    df3 = df2

    # Trazendo a infromação de Nome
    df3 = df3.merge(relacao_fila_ec_agente[['Fila', 'Código Estabelecimento', 'Nome']], on=['Fila', 'Código Estabelecimento'], how='left')

    # Filtrando protocolos sem nome
    df4 = df3[df3['Nome'].isnull()]

    # Verificando quantidade de protocolos atrelado para cada agente
    protocolos_por_agente = df3.groupby(['Fila','Nome'])['Protocolo (BD)'].nunique().reset_index()
    protocolos_por_agente = protocolos_por_agente.sort_values(by='Protocolo (BD)', ascending=False)

# %%
# Função para distribuir os protocolos
def distribuir_protocolos(df4, protocolos_por_agente):
    for fila in df4['Fila'].unique():
        # Filtra os protocolos da fila atual
        protocolos_fila = df4[df4['Fila'] == fila]
        
        # Filtra os agentes da fila atual e ordena pelo total de protocolos
        agentes_fila = protocolos_por_agente[protocolos_por_agente['Fila'] == fila].sort_values(by='Protocolo (BD)')
        
        # Dicionário para rastrear os estabelecimentos já atendidos
        estabelecimentos_atendidos = {}
        
        for index, protocolo in protocolos_fila.iterrows():
            estabelecimento = protocolo['Código Estabelecimento']
            
            # Verifica se o estabelecimento já foi atendido
            if estabelecimento not in estabelecimentos_atendidos:
                # Seleciona o agente com menor total de protocolos
                agente_selecionado = agentes_fila.iloc[0]
                
                # Atualiza o nome no df4
                df4.at[index, 'Nome'] = agente_selecionado['Nome']
                
                # Atualiza o total de protocolos do agente
                protocolos_por_agente.loc[protocolos_por_agente['Nome'] == agente_selecionado['Nome'], 'Protocolo (BD)'] += 1
                
                # Marca o estabelecimento como atendido
                estabelecimentos_atendidos[estabelecimento] = agente_selecionado['Nome']
                
                # Reordena os agentes após a atualização
                agentes_fila = protocolos_por_agente[protocolos_por_agente['Fila'] == fila].sort_values(by='Protocolo (BD)')

    return df4

# %%
def parte_tres():
    # Juntando os protocolos antigos com os novos
    df5 = df3[df3['Nome'].notnull()]
    df5 = pd.concat([df5, df4], ignore_index=True)

    # Exportar df para CSV
    df5.to_csv('arquivos_painel/protocolos_agente.csv', sep=';', index=False, encoding='utf-8')


    # Criar relação entre Fila, Nome e Código Estabelecimento
    relacao_fila_ec_agente = df5.groupby(['Fila', 'Nome', 'Código Estabelecimento'])['Protocolo (BD)'].nunique().reset_index()
    relacao_fila_ec_agente = relacao_fila_ec_agente.drop(columns=['Protocolo (BD)'])

    # Exportar relação para CSV
    relacao_fila_ec_agente.to_csv('arquivos_auxiliares/relacao_fila_ec_agente.csv', sep=';', index=False, encoding='utf-8')

# %%
# Criador Função 2
def funcao2():
    primeira_parte()
    distribuir_protocolos(df4, protocolos_por_agente)
    parte_tres()

# %%
# Validador de função
if contador_atual == 1:
    atualizar_dataframe(df2, df_agentes)
else:
    funcao2()


