
# class FormaPagamento:
#     def __init__(self, valor):
#         self.valor = valor
#         self.data_hora = datetime.now()
#         self.status = "Pendente"

#     def validar(self):
#         pass

#     def aprovar_pagamento(self):
#         self.status = "Aprovado" if random.random() < 0.8 else "Recusado"
#         return self.status


# class Cartao(FormaPagamento):
#     def __init__(self, numero, nome, validade, cvv, bandeira, valor):
#         super().__init__(valor)
#         self.numero = numero
#         self.nome = nome
#         self.validade = validade
#         self.cvv = cvv
#         self.bandeira = bandeira

#     def validar(self):
#         if not (self.cvv.isdigit() and len(self.cvv) == 3):
#             return False, "CVV inválido."
#         try:
#             validade_data = datetime.strptime(self.validade, "%m/%Y")
#             agora = datetime.now()
#             if (validade_data.year < agora.year) or \
#                (validade_data.year == agora.year and validade_data.month < agora.month):
#                 return False, "Cartão expirado."
#         except:
#             return False, "Data de validade inválida."
#         return True, ""


# class Boleto(FormaPagamento):
#     def __init__(self, cpf, nome, vencimento, descricao, valor):
#         super().__init__(valor)
#         self.cpf = cpf
#         self.nome = nome
#         self.vencimento = vencimento
#         self.descricao = descricao

#     def validar(self):
#         if len(self.cpf) != 14:
#             return False, "CPF inválido."
#         try:
#             if datetime.strptime(self.vencimento, "%d/%m/%Y") < datetime.now():
#                 return False, "Boleto vencido."
#         except:
#             return False, "Data de vencimento inválida."
#         return True, ""


# class Pix(FormaPagamento):
#     def __init__(self, chave, tipo, nome, valor):
#         super().__init__(valor)
#         self.chave = chave
#         self.tipo = tipo
#         self.nome = nome

#     def validar(self):
#         if self.tipo == "Email" and "@" not in self.chave or "." not in self.chave.split("@")[-1]:
#             return False, "E-mail inválido."
#         if self.tipo == "Telefone" and len(self.chave) != 11:
#             return False, "Telefone inválido."
#         return True, ""


# def obter_historico_usuario(usuario_id):
#     conexao_pagamento = conectar_banco()
    
#     historico_cartao = pd.read_sql_query('''
#         SELECT 'Cartão' AS Metodo, 
#                Numero_Cartao AS Info, 
#                Valor, 
#                Data_Hora, 
#                Status 
#         FROM Cartao 
#         WHERE Usuario_ID = ?
#     ''', conexao_pagamento, params=(usuario_id,))
    
#     historico_boleto = pd.read_sql_query('''
#         SELECT 'Boleto' AS Metodo, 
#                CPF AS Info, 
#                Valor, 
#                Data_Hora, 
#                Status 
#         FROM Boleto 
#         WHERE Usuario_ID = ?
#     ''', conexao_pagamento, params=(usuario_id,))
    
#     historico_pix = pd.read_sql_query('''
#         SELECT 'Pix' AS Metodo, 
#                Chave_Pix AS Info, 
#                Valor, 
#                Data_Hora, 
#                Status 
#         FROM Pix 
#         WHERE Usuario_ID = ?
#     ''', conexao_pagamento, params=(usuario_id,))
    
#     conexao_pagamento.close()
    
#     historico = pd.concat([historico_cartao, historico_boleto, historico_pix], ignore_index=True)
#     historico.sort_values(by="Data_Hora", ascending=False, inplace=True)
#     return historico

# # def camuflar_cpf(cpf: str) -> str:
# #     return f"***.{cpf[4:7]}.***-{cpf[-2:]}"

# # def camuflar_telefone(telefone: str) -> str:
# #     return f"{telefone[:2]}*****{telefone[-2:]}"

# # def camuflar_email(email: str) -> str:
# #     partes = email.split("@")
# #     return partes[0][0] + "***@" + partes[1]


from gestor_banco_de_dados import (
    conectar_banco, criar_tabelas, hash_senha, buscar_usuario, buscar_colaborador, 
    buscar_tutor_por_usuario, salvar_ou_atualizar_tutor, obter_tutor_id,
    listar_pets_do_tutor, salvar_ou_atualizar_pet, listar_usuarios_colaboradores_sem_crmv, admin_cadastrar_medico_completo,
    listar_consultas_geral, atualizar_status_e_medico_consulta,
    listar_medicos_disponiveis, listar_medicos_com_turno, listar_horarios_ocupados,
    inserir_consulta)

import time
# import random
# import hashlib
# import sqlite3
import datetime
# import pandas as pd
import streamlit as st

criar_tabelas()

# --- INSERÇÃO DE DADOS TESTE ---

conexao_clinica = conectar_banco()
cursor_clinica = conexao_clinica.cursor() # CRUCIAL: Criando o cursor para o fluxo principal

# 1. EMERSON ROYAL ////////////////////////////////////////////////////////////////////////
senha = hash_senha("emerson123")

# Usamos INSERT OR IGNORE caso o e-mail já exista no banco
cursor_clinica.execute('''
    INSERT OR IGNORE INTO Usuarios (Email, Senha, Tipo) VALUES (?, ?, ?)
''', ("emersonroyal&@gmail.com", senha, "Colaborador"))
conexao_clinica.commit()

usuario = buscar_usuario("emersonroyal&@gmail.com", senha)

if usuario:
    cursor_clinica.execute('''
        INSERT OR IGNORE INTO Colaboradores (Usuario_ID, Nome, Email, Tipo) VALUES (?, ?, ?, ?)
    ''', (usuario[0], "Emerson Royal", usuario[1], "Médico"))
    conexao_clinica.commit()

    colaborador = buscar_colaborador("emersonroyal&@gmail.com")

    if colaborador:
        cursor_clinica.execute('''
            INSERT OR IGNORE INTO Médicos (Colaborador_ID, Nome, CRMV, Email, Turno) VALUES (?, ?, ?, ?, ?)
        ''', (colaborador[0], colaborador[1], "827477", colaborador[2], "Manhã (07h às 12h)"))
        conexao_clinica.commit()


# 2. AYRTON LUCAS ////////////////////////////////////////////////////////////////////////
senha = hash_senha("ayrtonn78")

cursor_clinica.execute('''
    INSERT OR IGNORE INTO Usuarios (Email, Senha, Tipo) VALUES (?, ?, ?)
''', ("ayrtonn78&@gmail.com", senha, "Colaborador"))
conexao_clinica.commit()

usuario = buscar_usuario("ayrtonn78&@gmail.com", senha)

if usuario:
    cursor_clinica.execute('''
        INSERT OR IGNORE INTO Colaboradores (Usuario_ID, Nome, Email, Tipo) VALUES (?, ?, ?, ?)
    ''', (usuario[0], "Ayrton Lucas", usuario[1], "Médico"))
    conexao_clinica.commit()

    colaborador = buscar_colaborador("ayrtonn78&@gmail.com")

    if colaborador:
        cursor_clinica.execute('''
            INSERT OR IGNORE INTO Médicos (Colaborador_ID, Nome, CRMV, Email, Turno) VALUES (?, ?, ?, ?, ?)
        ''', (colaborador[0], colaborador[1], "209891", colaborador[2], "Tarde (12h às 17h)"))
        conexao_clinica.commit()


# 3. ANDREI //////////////////////////////////////////////////////////////////////////////
senha = hash_senha("andrei21")

cursor_clinica.execute('''
    INSERT OR IGNORE INTO Usuarios (Email, Senha, Tipo) VALUES (?, ?, ?)
''', ("andrei@gmail.com", senha, "Colaborador"))
conexao_clinica.commit()

usuario = buscar_usuario("andrei@gmail.com", senha)

if usuario:
    cursor_clinica.execute('''
        INSERT OR IGNORE INTO Colaboradores (Usuario_ID, Nome, Email, Tipo) VALUES (?, ?, ?, ?)
    ''', (usuario[0], "Andrei", usuario[1], "Admin"))
    conexao_clinica.commit()


# 4. DOUGLAS /////////////////////////////////////////////////////////////////////////////
senha = hash_senha("douglas30")

cursor_clinica.execute('''
    INSERT OR IGNORE INTO Usuarios (Email, Senha, Tipo) VALUES (?, ?, ?)
''', ("douglas@gmail.com", senha, "Colaborador"))
conexao_clinica.commit()

usuario = buscar_usuario("douglas@gmail.com", senha)

if usuario:
    cursor_clinica.execute('''
        INSERT OR IGNORE INTO Colaboradores (Usuario_ID, Nome, Email, Tipo) VALUES (?, ?, ?, ?)
    ''', (usuario[0], "Douglas", usuario[1], "Admin"))
    conexao_clinica.commit()

# Finaliza tudo corretamente
cursor_clinica.close()
conexao_clinica.close()

print("Banco carregado e dados inseridos com sucesso!")

def pagina_usuario():
    st.success(f"👋 Olá, {st.session_state.email}")
    st.markdown("---")
    st.text(f"👋 Usuário")

    # Criando as abas na página do usuário

    aba_perfil, aba_pets, aba_agendar, aba_historico = st.tabs([
        "👤 Meu Perfil", 
        "🐾 Meus Pets", 
        "📅 Agendar Consulta", 
        "📋 Minhas Consultas"
        ])
    
    with aba_perfil:
        st.subheader("📋 Seus Dados Pessoais")
        st.write("Mantenha suas informações de contato atualizadas para que a clínica possa falar com você.")

        # Busca no banco se este usuário já preencheu o perfil de Tutor
        dados_tutor = buscar_tutor_por_usuario(st.session_state.usuario_id)

        # Se ele já tiver dados salvos, preenchemos o formulário com o que existe
        if dados_tutor:
            nome_inicial = dados_tutor[0]
            telefone_inicial = dados_tutor[1]
            texto_botao = "Atualizar Meus Dados"
        else:
            nome_inicial = ""
            telefone_inicial = ""
            texto_botao = "Salvar Perfil"

        # Formulário do Streamlit
        with st.form("form_dados_tutor"):
            nome_tutor = st.text_input("Nome Completo", value=nome_inicial)
            telefone_tutor = st.text_input("Telefone de Contato (com DDD)", value=telefone_inicial, placeholder="(00) 99999-9999")
            
            # Botão de envio do formulário
            botao_salvar = st.form_submit_button(texto_botao)

            if botao_salvar:
                if not nome_tutor or not telefone_tutor:
                    st.warning("Por favor, preencha todos os campos antes de salvar.")
                else:
                    # Executa a função para salvar ou atualizar no SQLite
                    salvar_ou_atualizar_tutor(
                        usuario_id=st.session_state.usuario_id,
                        nome=nome_tutor,
                        email=st.session_state.email, # O email vem do session_state do login
                        telefone=telefone_tutor
                    )
                    # st.rerun() # Atualiza a tela para mostrar os dados novos
                    st.success("Dados salvos com sucesso!")
                    time.sleep(3)
                    st.rerun()

    # Coloque o formulário de tutor aqui...
    with aba_pets:
        st.subheader("🐾 Gerenciar Meus Pets")
        
        info_tutor = obter_tutor_id(st.session_state.usuario_id)
        
        if not info_tutor:
            st.error("⚠️ Você precisa preencher seus dados pessoais na aba '👤 Meu Perfil' antes de cadastrar um pet.")
        else:
            tutor_id_banco = info_tutor[0]
            nome_tutor_banco = info_tutor[1]
            # Dados para o selectbox de Raça -> Espécie
            # # Chave: Raça, Valor: Espécie correspondente
            dados_racas = {
                "Vira-lata (SRD)": "Canina/Felina",
                "Golden Retriever": "Canina",
                "Labrador Retriever": "Canina",
                "Dobermann": "Canina",
                "Pastor Alemão": "Canina",
                "Poodle": "Canina",
                "Persa": "Felina",
                "Siamês": "Felina",
                "Sphynx": "Felina",
                "Calopsita": "Ave",
                "Canário": "Ave",
                "Periquito": "Ave",
                "Papagaio": "Ave",
                "Jabuti-piranga": "Répteis",
                "Gecko-leopardo": "Répteis"
                }
            
            # Opções de ação para o usuário
            acao_pet = st.radio("O que deseja fazer?", ["Cadastrar Novo Pet", "Atualizar Pet Existente"], horizontal=True)
            
            # Inicializando variáveis do formulário
            pet_id_selecionado = None
            nome_pet_inicial = ""
            sexo_inicial = "Macho"
            raca_inicial = "Vira-lata (SRD)"
            
            # Se o usuário quiser atualizar, precisamos carregar os pets dele
            if acao_pet == "Atualizar Pet Existente":
                lista_de_pets = listar_pets_do_tutor(tutor_id_banco)
                
                if not lista_de_pets:
                    st.info("Você ainda não tem nenhum pet cadastrado para atualizar.")
                    # Força a voltar para o cadastro se a lista estiver vazia
                    st.stop() 
                else:
                    # Criamos um dicionário para o Selectbox mostrar o nome do pet bonitinho
                    opcoes_pets = {f"{p[1]} ({p[2]} - {p[3]})": p for p in lista_de_pets}
                    pet_escolhido_texto = st.selectbox("Selecione o Pet que deseja editar:", list(opcoes_pets.keys()))
                    
                    # Extrai os dados do pet selecionado
                    pet_dados = opcoes_pets[pet_escolhido_texto]
                    pet_id_selecionado = pet_dados[0]
                    nome_pet_inicial = pet_dados[1]

                    # A raça e sexo salvos no banco (se existirem na nossa lista padrão)
                    raca_inicial = pet_dados[3] if pet_dados[3] in dados_racas else "Vira-lata (SRD)"
                    sexo_inicial = pet_dados[4]
                    
            # 2. FORMULÁRIO DE CADASTRO / EDIÇÃO
            # # Usamos uma chave dinâmica no form para resetar os campos no reload automático do Streamlit
            form_key = f"form_pet_{pet_id_selecionado}" if pet_id_selecionado else "form_novo_pet"
            
            with st.form(key=form_key):
                nome_pet = st.text_input("Nome do Pet", value=nome_pet_inicial)
                
                # Selectbox da Raça
                lista_racas = list(dados_racas.keys())
                index_raca = lista_racas.index(raca_inicial)
                raca_selecionada = st.selectbox("Selecione a Raça", lista_racas, index=index_raca)
                
                # Descobre a Espécie AUTOMATICAMENTE baseado na raça escolhida
                especie_automatica = dados_racas[raca_selecionada]
                
                # Exibe em um campo de texto desabilitado (só para o usuário ver)
                st.text_input("Espécie (Definida pela Raça)", value=especie_automatica, disabled=True)
                
                # Campo de Sexo
                opcoes_sexo = ["Macho", "Fêmea"]
                index_sexo = opcoes_sexo.index(sexo_inicial) if sexo_inicial in opcoes_sexo else 0
                sexo_selecionado = st.selectbox("Sexo", opcoes_sexo, index=index_sexo)
                
                # Botão de envio
                texto_botao_pet = "Salvar Alterações" if pet_id_selecionado else "Cadastrar Pet"
                botao_salvar_pet = st.form_submit_button(texto_botao_pet)
                
                if botao_salvar_pet:
                    if not nome_pet:
                        st.warning("O nome do seu pet não pode ficar em branco.")
                    else:
                        # Envia para a função do banco de dados
                        salvar_ou_atualizar_pet(
                            pet_id=pet_id_selecionado,
                            tutor_id=tutor_id_banco,
                            nome_tutor=nome_tutor_banco,
                            nome_pet=nome_pet,
                            especie=especie_automatica,
                            raca=raca_selecionada,
                            sexo=sexo_selecionado
                            )
                        st.rerun() # Dá o reload na página, limpando os campos ou aplicando a alteração!
                        st.success(f"Pet '{nome_pet}' salvo com sucesso!")
                        time.sleep(3)
                        st.rerun()

    with aba_agendar:
        st.subheader("📅 Agende uma Consulta para o seu Pet")
        st.markdown("---")
    
        # Validação: O usuário precisa ser tutor e ter pets cadastrados
        info_tutor = obter_tutor_id(st.session_state.usuario_id)
    
        if not info_tutor:
            st.warning("⚠️ Cadastre seus dados pessoais na aba '👤 Meu Perfil' primeiro.")
        else:
            tutor_id = info_tutor[0]
            lista_pets = listar_pets_do_tutor(tutor_id)
            lista_medicos = listar_medicos_com_turno()
        
            if not lista_pets:
                st.info("🐾 Você precisa cadastrar pelo menos um Pet na aba 'Meus Pets' antes de agendar.")
            elif not lista_medicos:
                st.info("👨‍⚕️ Não há médicos cadastrados ou disponíveis na clínica no momento.")
            else:
                # Informações fixas da clínica na lateral
                st.sidebar.markdown("### 🏪 Horário da Clínica")
                st.sidebar.caption("Segunda a Sexta: 07h às 17h")
                st.sidebar.caption("Consultas com duração de 1 hora.")

                # --- CAMPOS DINÂMICOS SEM ST.FORM ---

                # 1. Seleção do Pet
                dict_pets = {p[1]: p[0] for p in lista_pets}
                pet_nome_sel = st.selectbox("1. Selecione o Pet para a Consulta:", list(dict_pets.keys()))
                pet_id_sel = dict_pets[pet_nome_sel]
            
                # 2. Seleção do Médico (Gera o "reload" automático de horários ao mudar)
                dict_medicos = {f"Dr(a). {m[1]} — Turno: {m[2]}": (m[0], m[2]) for m in lista_medicos}
                medico_texto_sel = st.selectbox("2. Selecione o Veterinário:", list(dict_medicos.keys()))
                medico_id_sel = dict_medicos[medico_texto_sel][0]
                medico_turno_sel = dict_medicos[medico_texto_sel][1]
            
                # 3. Seleção da Data (Gera o "reload" automático de horários ao mudar o dia)
                data_consulta = st.date_input("3. Selecione a Data:", min_value=datetime.date.today())
                data_texto = data_consulta.strftime("%Y-%m-%d")
            
                # --- PROCESSAMENTO DOS HORÁRIOS (Roda a cada mudança acima) ---
                if "Manhã" in medico_turno_sel:
                    grade_horarios = ["07:00", "08:00", "09:00", "10:00", "11:00"]
                elif "Tarde" in medico_turno_sel:
                    grade_horarios = ["12:00", "13:00", "14:00", "15:00", "16:00"]
                else:
                    grade_horarios = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
            
                # Busca ocupados no banco em tempo real
                horarios_ocupados = listar_horarios_ocupados(medico_id_sel, data_texto)
                horarios_disponiveis = [h for h in grade_horarios if h not in horarios_ocupados]
            
                # 4. Exibe a lista já filtrada de Horários
                if not horarios_disponiveis:
                    st.error("❌ Não há horários livres para este médico nesta data. Escolha outro dia ou profissional.")
                    horario_selecionado = None
                else:
                    horario_selecionado = st.selectbox("4. Selecione o Horário Disponível:", horarios_disponiveis)
            
                # Espaçador visual antes do botão
                st.write("")
            
                # Botão avulso de confirmação
                if st.button("Confirmar Agendamento", type="primary"):
                    if not horario_selecionado:
                        st.error("Não foi possível agendar. Selecione um horário válido.")
                    else:
                        # Grava no banco de dados
                        inserir_consulta(tutor_id, pet_id_sel, medico_id_sel, data_texto, horario_selecionado)
                        st.success(f"🎉 Consulta agendada com sucesso para {pet_nome_sel} no dia {data_consulta.strftime('%d/%m/%Y')} às {horario_selecionado}!")
                        st.balloons()
                     
                        # Um pequeno delay e recarrega para atualizar a tela
                        time.sleep(5)
                        st.rerun()

    # with aba_agendar:
    #     st.subheader("📅 Agende uma Consulta para o seu Pet")
    #     st.markdown("---")
    
    #     # 1. Validação: O usuário precisa ser tutor e ter pets cadastrados
    #     info_tutor = obter_tutor_id(st.session_state.usuario_id)
    
    #     if not info_tutor:
    #         st.warning("⚠️ Cadastre seus dados pessoais na aba '👤 Meu Perfil' primeiro.")
    #     else:
    #         tutor_id = info_tutor[0]
    #         lista_pets = listar_pets_do_tutor(tutor_id)
    #         lista_medicos = listar_medicos_com_turno()
        
    #         if not lista_pets:
    #             st.info("🐾 Você precisa cadastrar pelo menos um Pet na aba 'Meus Pets' antes de agendar.")
    #         elif not lista_medicos:
    #             st.info("👨‍⚕️ Não há médicos cadastrados ou disponíveis na clínica no momento.")
    #         else:
    #             # Informações fixas da clínica na tela para o cliente
    #             st.sidebar.markdown("### 🏪 Horário da Clínica")
    #             st.sidebar.caption("Segunda a Sexta: 07h às 17h")
    #             st.sidebar.caption("Consultas com duração de 1 hora.")

    #             # Formulário estruturado
    #             with st.form("form_agendamento_consulta"):
    #                 # Passos de seleção
    #                 dict_pets = {p[1]: p[0] for p in lista_pets}
    #                 pet_nome_sel = st.selectbox("1. Selecione o Pet para a Consulta:", list(dict_pets.keys()))
    #                 pet_id_sel = dict_pets[pet_nome_sel]
                
    #                 # Seleção do Médico
    #                 # Formata a exibição do médico mostrando o turno dele na lista
    #                 dict_medicos = {f"Dr(a). {m[1]} — Turno: {m[2]}": (m[0], m[2]) for m in lista_medicos}
    #                 medico_texto_sel = st.selectbox("2. Selecione o Veterinário:", list(dict_medicos.keys()))
    #                 medico_id_sel = dict_medicos[medico_texto_sel][0]
    #                 medico_turno_sel = dict_medicos[medico_texto_sel][1]
                
    #                 # Calendário para o Dia (Bloqueia datas passadas para não agendar retroativo)
    #                 data_consulta = st.date_input("3. Selecione a Data:", min_value=datetime.date.today())
    #                 data_texto = data_consulta.strftime("%Y-%m-%d")
                
    #                 # --- LÓGICA DINÂMICA DE HORÁRIOS ---
    #                 # Define a grade completa de horários baseado no Turno do médico escolhido
    #                 if "Manhã" in medico_turno_sel:
    #                     grade_horarios = ["07:00", "08:00", "09:00", "10:00", "11:00"]
    #                 elif "Tarde" in medico_turno_sel:
    #                     grade_horarios = ["12:00", "13:00", "14:00", "15:00", "16:00"]
    #                 else: # Caso seja o turno Integral (07h às 17h)
    #                     grade_horarios = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
                
    #                 # Busca quais horários desse médico já estão ocupados nessa data específica
    #                 horarios_ocupados = listar_horarios_ocupados(medico_id_sel, data_texto)
                
    #                 # Filtra a lista mantendo APENAS os horários que não estão ocupados
    #                 horarios_disponiveis = [h for h in grade_horarios if h not in horarios_ocupados]
                
    #                 # Exibe o selectbox dinâmico de horas
    #                 if not horarios_disponiveis:
    #                     st.error("❌ Não há horários livres para este médico nesta data. Escolha outro dia ou profissional.")
    #                     horario_selecionado = None
    #                 else:
    #                     horario_selecionado = st.selectbox("4. Selecione o Horário Disponível:", horarios_disponiveis)

    #                 st.write("")
                
    #                 # Botão para enviar
    #                 botao_agendar = st.form_submit_button("Confirmar Agendamento")
                
    #                 if botao_agendar:
    #                     if not horario_selecionado:
    #                         st.error("Não foi possível agendar. Selecione um horário válido.")
    #                     else:
    #                         # Salva na tabela Consultas
    #                         inserir_consulta(tutor_id, pet_id_sel, medico_id_sel, data_texto, horario_selecionado)
    #                         st.success(f"🎉 Consulta agendada com sucesso para {pet_nome_sel} no dia {data_consulta.strftime('%d/%m/%Y')} às {horario_selecionado}!")
    #                         st.balloons()

    #                         time.sleep(2)
    #                         st.rerun()

    with aba_historico:
        st.subheader("Consultas salvas")
        st.markdown("---")


def pagina_admin():
    st.success(f"👋 Olá Admin, {st.session_state.email}")
    st.markdown("---")

    st.title("⚙️ Painel do Administrador - Gestão da Clínica")
        
    aba_cadastrar, aba_agenda_medica, aba_gerenciar_consultas = st.tabs([
        "👨‍⚕️ Cadastrar Médico", 
        "⏰ Escalas e Horários", 
        "📋 Gerenciar Consultas"
        ])
    
    # ---------------------------------------------------------
    # # ABA 1: CADASTRAR MÉDICO
    # # ---------------------------------------------------------
    with aba_cadastrar:
        st.subheader("👨‍⚕️ Cadastrar Novo Médico do Zero")
        st.write("Preencha todos os dados abaixo para criar a conta de acesso e o registro profissional do médico.")
        
        with st.form("form_cadastro_medico_do_zero", clear_on_submit=True):
            col_dados1, col_dados2 = st.columns(2)
            
            with col_dados1:
                nome_medico = st.text_input("Nome Completo do Médico")
                email_medico = st.text_input("E-mail de Acesso")
                senha_medico = st.text_input("Senha Inicial", type="password", help="O médico usará este e-mail e senha para logar.")
            
            with col_dados2:
                crmv_medico = st.text_input("Número do CRMV", placeholder="Ex: 12345-SP")
                turno_medico = st.selectbox("Turno de Trabalho", ["Integral (07h às 17h)", "Manhã (07h às 12h)", "Tarde (12h às 17h)"])
        
            # Botão de envio
            botao_cadastrar = st.form_submit_button("Criar e Ativar Médico")

            if botao_cadastrar:
                # Validação simples de campos vazios
                if not nome_medico or not email_medico or not senha_medico or not crmv_medico:
                    st.warning("⚠️ Todos os campos são obrigatórios para efetuar o cadastro.")
                else:
                    # Dispara a função mágica que alimenta as 3 tabelas
                    sucesso, mensagem = admin_cadastrar_medico_completo(
                        nome=nome_medico,
                        email=email_medico,
                        senha_plana=senha_medico,
                        crmv=crmv_medico,
                        turno=turno_medico
                    )
                    if sucesso:
                        st.success(mensagem)
                        time.sleep(3)
                        st.rerun()
                        # O clear_on_submit=True já vai limpar os campos automaticamente após o sucesso!
                    else:
                        st.error(mensagem)
    

    # ---------------------------------------------------------
    # ABA 2: ESCALAS E HORÁRIOS (Para as regras de Negócio da Facul)
    # ---------------------------------------------------------
    with aba_agenda_medica:
        st.subheader("⏰ Configuração de Turnos Disponíveis")
        st.write("Os dois médicos iniciais estão configurados para o horário padrão da clínica:")
            
        # Demonstrando os horários padrões solicitados para a banca ver
        st.info("**Horário de Funcionamento:** Segunda a Sexta — 07:00 às 17:00")
            
        # Uma tabela visual simples estática ou dinâmica das regras
        dados_turnos = {
            "Período": ["Manhã", "Tarde", "Integral"],
            "Horário Inicial": ["07:00", "12:00", "07:00"],
            "Horário Final": ["12:00", "17:00", "17:00"],
            "Intervalo de Consultas": ["1 hora", "1 hora", "1 hora"]
            }
        st.table(dados_turnos)      

    # ---------------------------------------------------------
    # ABA 3: GERENCIAR CONSULTAS (Vincular Médico e Mudar Status)
    # ---------------------------------------------------------
    with aba_gerenciar_consultas:
        st.subheader("📋 Painel Geral de Consultas Solicitadas")
        
        lista_consultas = listar_consultas_geral()
        lista_medicos = listar_medicos_disponiveis()
        
        if not lista_consultas:
            st.info("Nenhuma consulta agendada no momento.")
        else:
            # Mostra todas as consultas em formato amigável
            for consulta in lista_consultas:
                c_id, tutor, pet, medico_nome, data, horario, status = consulta
                 
                # Criando um card visual para cada consulta cadastrada
                with st.expander(f"📌 Consulta #{c_id} - Pet: {pet} ({data} às {horario})"):
                    col_info, col_acao = st.columns(2)
                        
                    with col_info:
                        st.write(f"**Tutor:** {tutor}")
                        st.write(f"**Data/Hora:** {data} às {horario}")
                        st.write(f"**Médico Atual:** {medico_nome if medico_nome else '⚠️ Não Vinculado'}")
                        st.write(f"**Status Atual:** `{status}`")
                        
                    with col_acao:
                        # Selectbox para escolher ou trocar o médico desta consulta
                        dict_medicos = {m[1]: m[0] for m in lista_medicos}
                        # Identifica o index atual do médico se já houver um vinculado
                        lista_nomes_medicos = list(dict_medicos.keys())
                        index_medico = lista_nomes_medicos.index(medico_nome) if medico_nome in lista_nomes_medicos else 0
                        
                        medico_escolhido = st.selectbox(f"Vincular Médico (Consulta #{c_id})", lista_nomes_medicos, index=index_medico)
                        
                        # Selectbox para atualizar o status
                        status_opcoes = ["Agendado", "Em Andamento", "Concluído", "Cancelado"]
                        index_status = status_opcoes.index(status) if status in status_opcoes else 0
                        novo_status = st.selectbox(f"Alterar Status (Consulta #{c_id})", status_opcoes, index=index_status)
                            
                        if st.button(f"Salvar Alterações #{c_id}"):
                            id_medico_banco = dict_medicos[medico_escolhido]
                            atualizar_status_e_medico_consulta(c_id, id_medico_banco, novo_status)
                            st.success("Consulta atualizada!")
                            time.sleep(5)          
                            st.rerun()        


def pagina_medico():
    st.success(f"👋 Olá, {st.session_state.email}")
    st.markdown("---")
    st.text(f"👋 Médico")




def validar_email(email):
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "E-mail inválido"
    return True, ""

st.set_page_config(page_title="Petz", layout="wide")
st.title("🐶 Petz: Cuidando do Seu Animal de Estimação")
st.caption("")
st.markdown("---")

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario_id = None
    st.session_state.email = ""

if not st.session_state.logado:
    st.subheader("🔐 Login ou Cadastro")
    col1, col2 = st.columns(2)

    with col1:
        modo = st.radio("Modo", ["Login", "Cadastro"])
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Confirmar"):
            if not email or not senha:
                st.warning("Preencha todos os campos.")
            else:
                conexao_clinica = conectar_banco()
                cursor_clinica = conexao_clinica.cursor()
                senha_hash = hash_senha(senha)

                email_valido, mensagem_email = validar_email(email)

                if not email_valido:
                    st.error(mensagem_email)
                else:
                    if modo == "Login":
                        cursor_clinica.execute("SELECT ID, Tipo FROM Usuarios WHERE Email = ? AND Senha = ?", (email, senha_hash))
                        usuario = cursor_clinica.fetchone()
                        if usuario:
                            st.session_state.logado = True
                            st.session_state.usuario_id = usuario[0]
                            st.session_state.email = email
                            st.session_state.tipo = usuario[1]
                            st.success("Login realizado com sucesso.")
                            st.rerun()
                        else:
                            st.error("Usuário ou senha inválidos.")
                    else:
                        cursor_clinica.execute("SELECT * FROM Usuarios WHERE Email = ?", (email,))
                        if cursor_clinica.fetchone():
                            st.warning("E-mail já cadastrado.")
                        else:
                            cursor_clinica.execute("INSERT INTO Usuarios (Email, Senha, Tipo) VALUES (?, ?, ?)", (email, senha_hash, "Usuário"))
                            conexao_clinica.commit()
                            st.success("Cadastro realizado! Faça login.")
                            conexao_clinica.close()

else:
    if (st.session_state.tipo == "Usuário"):
        pagina_usuario()
    else:
        conexao_clinica = conectar_banco()
        cursor_clinica = conexao_clinica.cursor()
        cursor_clinica.execute("SELECT Tipo FROM Colaboradores WHERE Email = ?", (st.session_state.email,))
        colaborador = cursor_clinica.fetchone()
        if (colaborador[0] == "Admin"):
            pagina_admin()
        else:
            pagina_medico()

    # st.success(f"👋 Olá, {st.session_state.email}")
    # st.markdown("---")

    # aba_pagamento, aba_historico = st.tabs(["💳 Realizar Pagamento", "📜 Histórico de Transações"])

    # with aba_pagamento:
    #     st.subheader("Escolha o método de pagamento:")
    #     metodo = st.radio("", ["Cartão", "Boleto", "Pix"], horizontal=True)
    #     st.markdown("---")

    #     if metodo == "Cartão":
    #         st.subheader("💳 Pagamento com Cartão")
    #         col1, col2 = st.columns(2)
    #         with col1:
    #             numero = st.text_input("Número do Cartão", max_chars=16)
    #             validade = st.text_input("Validade (MM/AAAA)")
    #             cvv = st.text_input("CVV", max_chars=3, type="password")
    #         with col2:
    #             nome = st.text_input("Nome do Titular")
    #             bandeira = st.selectbox("Bandeira", ["Visa", "Mastercard", "Elo", "Amex"])
    #             valor = st.number_input("Valor", min_value=0.01, step=0.01)

    #         if st.button("💳 Pagar"):
    #             pagamento = Cartao(numero, nome, validade, cvv, bandeira, valor)
    #             valido, msg = pagamento.validar()
    #             if valido:
    #                 status = pagamento.aprovar_pagamento()
    #                 conexao_pagamento = conectar_banco()
    #                 conexao_pagamento.execute('''
    #                     INSERT INTO Cartao (Usuario_ID, Numero_Cartao, Nome_Cartao, Data_Validade, CVV, Bandeira, Valor, Data_Hora, Status)
    #                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    #                 ''', (st.session_state.usuario_id, f"****{numero[-4:]}", nome, validade, "***", bandeira, valor, pagamento.data_hora, status))
    #                 conexao_pagamento.commit()
    #                 conexao_pagamento.close()
    #                 st.success(f"Pagamento {status}")
    #             else:
    #                 st.error(msg)

    #     elif metodo == "Boleto":
    #         st.subheader("🧾 Pagamento com Boleto")
    #         cpf = st.text_input("CPF do Sacado", placeholder="xxx.xxx.xxx-xx")
    #         nome = st.text_input("Nome do Sacado")
    #         vencimento = st.text_input("Data de Vencimento (DD/MM/AAAA)")
    #         descricao = st.text_input("Descrição")
    #         valor = st.number_input("Valor", min_value=0.01, step=0.01)

    #         if st.button("🧾 Gerar Boleto"):
    #             pagamento = Boleto(cpf, nome, vencimento, descricao, valor)
    #             valido, msg = pagamento.validar()
    #             if valido:
    #                 status = pagamento.aprovar_pagamento()
    #                 conexao_pagamento = conectar_banco()
    #                 cpf_camuflado = camuflar_cpf(cpf)
    #                 conexao_pagamento.execute('''
    #                     INSERT INTO Boleto (Usuario_ID, CPF, Nome_Sacado, Data_Vencimento, Descricao, Valor, Data_Hora, Status)
    #                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    #                 ''', (st.session_state.usuario_id, cpf_camuflado, nome, vencimento, descricao, valor, pagamento.data_hora, status))
    #                 conexao_pagamento.commit()
    #                 conexao_pagamento.close()
    #                 st.success(f"Boleto {status}")
    #             else:
    #                 st.error(msg)

    #     elif metodo == "Pix":
    #         st.subheader("📱 Pagamento via Pix")
    #         chave = st.text_input("Chave Pix")
    #         tipo = st.selectbox("Tipo da chave", ["Email", "Telefone", "CPF"])
    #         nome = st.text_input("Nome do destinatário")
    #         valor = st.number_input("Valor", min_value=0.01, step=0.01)

    #         if st.button("📲 Enviar Pix"):
    #             pagamento = Pix(chave, tipo, nome, valor)
    #             valido, msg = pagamento.validar()
    #             if valido:
    #                 status = pagamento.aprovar_pagamento()
    #                 conexao_pagamento = conectar_banco()

    #                 if tipo.lower() == "email":
    #                     chave_camuflada = camuflar_email(chave)
    #                 elif tipo.lower() == "telefone":
    #                     chave_camuflada = camuflar_telefone(chave)
    #                 else:
    #                     chave_camuflada = camuflar_cpf(chave)

    #                 conexao_pagamento.execute('''
    #                     INSERT INTO Pix (Usuario_ID, Chave_Pix, Tipo_Chave, Nome_Destinatario, Valor, Data_Hora, Status)
    #                     VALUES (?, ?, ?, ?, ?, ?, ?)
    #                 ''', (st.session_state.usuario_id, chave_camuflada, tipo, nome, valor, pagamento.data_hora, status))
    #                 conexao_pagamento.commit()
    #                 conexao_pagamento.close()
    #                 st.success(f"Pix {status}")
    #             else:
    #                 st.error(msg)

    # with aba_historico:
    #     st.subheader("📜 Histórico de Transações")
    #     historico = obter_historico_usuario(st.session_state.usuario_id)

    #     if not historico.empty:
    #         historico["Data_Hora"] = pd.to_datetime(historico["Data_Hora"]).dt.strftime("%d/%m/%Y %H:%M")
    #         st.dataframe(historico[["Metodo", "Info", "Valor", "Data_Hora", "Status"]], use_container_width=True)
    #     else:
    #         st.info("Nenhuma transação encontrada.")
