from gestor_banco_de_dados import (
    conectar_banco, criar_tabelas, hash_senha, buscar_usuario, buscar_colaborador, 
    buscar_tutor_por_usuario, salvar_ou_atualizar_tutor, obter_tutor_id,
    listar_pets_do_tutor, salvar_ou_atualizar_pet, admin_cadastrar_medico_completo,
    listar_consultas_geral, atualizar_status_e_medico_consulta,
    listar_medicos_disponiveis, listar_medicos_com_turno, listar_horarios_ocupados,
    inserir_consulta, listar_consultas_do_tutor, listar_consultas_do_medico,
    medico_salvar_atendimento)

import time
import datetime
import pandas as pd
import streamlit as st

criar_tabelas()

# --- INSERÇÃO DE DADOS TESTE ---

conexao_clinica = conectar_banco()
cursor_clinica = conexao_clinica.cursor()

# 1. EMERSON ROYAL /////////////////////

senha = hash_senha("emerson123")

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

# 2. AYRTON LUCAS ////////////////////////////

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


# 3. ANDREI ////////////////////////////////

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


# 4. DOUGLAS ////////////////////////////////

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

cursor_clinica.close()
conexao_clinica.close()



print("Banco carregado e dados inseridos com sucesso!")


def pagina_usuario():
    st.success(f"👋 Olá, {st.session_state.email}")
    st.markdown("---")

    aba_perfil, aba_pets, aba_agendar, aba_historico = st.tabs([
        "👤 Meu Perfil", 
        "🐾 Meus Pets", 
        "📅 Agendar Consulta", 
        "📋 Minhas Consultas"
        ])
    
    with aba_perfil:
        st.subheader("📋 Seus Dados Pessoais")
        st.write("Mantenha suas informações de contato atualizadas para que a clínica possa falar com você.")

        dados_tutor = buscar_tutor_por_usuario(st.session_state.usuario_id)

        if dados_tutor:
            nome_inicial = dados_tutor[0]
            telefone_inicial = dados_tutor[1]
            texto_botao = "Atualizar Meus Dados"
        else:
            nome_inicial = ""
            telefone_inicial = ""
            texto_botao = "Salvar Perfil"

        with st.form("form_dados_tutor"):
            nome_tutor = st.text_input("Nome Completo", value=nome_inicial)
            telefone_tutor = st.text_input("Telefone de Contato (com DDD)", value=telefone_inicial, placeholder="(00) 99999-9999")
            
            st.write("")
            botao_salvar = st.form_submit_button(texto_botao)

            if botao_salvar:
                if not nome_tutor or not telefone_tutor:
                    st.warning("Por favor, preencha todos os campos antes de salvar.")
                else:
                    salvar_ou_atualizar_tutor(
                        usuario_id=st.session_state.usuario_id,
                        nome=nome_tutor,
                        email=st.session_state.email,
                        telefone=telefone_tutor
                    )
                    st.success("Dados salvos com sucesso!")
                    time.sleep(3)
                    st.rerun()

    with aba_pets:
        st.subheader("🐾 Gerenciar Meus Pets")
        
        info_tutor = obter_tutor_id(st.session_state.usuario_id)
        
        if not info_tutor:
            st.error("⚠️ Você precisa preencher seus dados pessoais na aba '👤 Meu Perfil' antes de cadastrar um pet.")
        else:
            tutor_id_banco = info_tutor[0]
            nome_tutor_banco = info_tutor[1]

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
            
            acao_pet = st.radio("O que deseja fazer?", ["Cadastrar Novo Pet", "Atualizar Pet Existente"], horizontal=True)
            
            pet_id_selecionado = None
            nome_pet_inicial = ""
            sexo_inicial = "Macho"
            raca_inicial = "Vira-lata (SRD)"
            
            if acao_pet == "Atualizar Pet Existente":
                lista_de_pets = listar_pets_do_tutor(tutor_id_banco)
                
                if not lista_de_pets:
                    st.info("Você ainda não tem nenhum pet cadastrado para atualizar.")
                    st.stop() 
                else:
                    opcoes_pets = {f"{p[1]} ({p[2]} - {p[3]})": p for p in lista_de_pets}
                    pet_escolhido_texto = st.selectbox("Selecione o Pet que deseja editar:", list(opcoes_pets.keys()))
                    
                    pet_dados = opcoes_pets[pet_escolhido_texto]
                    pet_id_selecionado = pet_dados[0]
                    nome_pet_inicial = pet_dados[1]

                    raca_inicial = pet_dados[3] if pet_dados[3] in dados_racas else "Vira-lata (SRD)"
                    sexo_inicial = pet_dados[4]
                    
            form_key = f"form_pet_{pet_id_selecionado}" if pet_id_selecionado else "form_novo_pet"
            
            with st.form(key=form_key):
                nome_pet = st.text_input("Nome do Pet", value=nome_pet_inicial)
                
                lista_racas = list(dados_racas.keys())
                index_raca = lista_racas.index(raca_inicial)
                raca_selecionada = st.selectbox("Selecione a Raça", lista_racas, index=index_raca)
                
                especie_automatica = dados_racas[raca_selecionada]
                
                st.text_input("Espécie (Definida pela Raça)", value=especie_automatica, disabled=True)
                
                opcoes_sexo = ["Macho", "Fêmea"]
                index_sexo = opcoes_sexo.index(sexo_inicial) if sexo_inicial in opcoes_sexo else 0
                sexo_selecionado = st.selectbox("Sexo", opcoes_sexo, index=index_sexo)
                
                texto_botao_pet = "Salvar Alterações" if pet_id_selecionado else "Cadastrar Pet"

                st.write("")
                botao_salvar_pet = st.form_submit_button(texto_botao_pet)
                
                if botao_salvar_pet:
                    if not nome_pet:
                        st.warning("O nome do seu pet não pode ficar em branco.")
                    else:
                        salvar_ou_atualizar_pet(
                            pet_id=pet_id_selecionado,
                            tutor_id=tutor_id_banco,
                            nome_tutor=nome_tutor_banco,
                            nome_pet=nome_pet,
                            especie=especie_automatica,
                            raca=raca_selecionada,
                            sexo=sexo_selecionado
                            )
                        st.rerun() 
                        st.success(f"Pet '{nome_pet}' salvo com sucesso!")
                        time.sleep(3)
                        st.rerun()

    with aba_agendar:
        st.subheader("📅 Agende uma Consulta para o seu Pet")
        st.markdown("---")
    
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
                st.sidebar.markdown("### 🏪 Horário da Clínica")
                st.sidebar.caption("Segunda a Sexta: 07h às 17h")
                st.sidebar.caption("Consultas com duração de 1 hora.")

                dict_pets = {p[1]: p[0] for p in lista_pets}
                pet_nome_sel = st.selectbox("1. Selecione o Pet para a Consulta:", list(dict_pets.keys()))
                pet_id_sel = dict_pets[pet_nome_sel]
            
                dict_medicos = {f"Dr(a). {m[1]} — Turno: {m[2]}": (m[0], m[2]) for m in lista_medicos}
                medico_texto_sel = st.selectbox("2. Selecione o Veterinário:", list(dict_medicos.keys()))
                medico_id_sel = dict_medicos[medico_texto_sel][0]
                medico_turno_sel = dict_medicos[medico_texto_sel][1]
            
                data_consulta = st.date_input("3. Selecione a Data:", min_value=datetime.date.today())
                data_texto = data_consulta.strftime("%Y-%m-%d")

                if "Manhã" in medico_turno_sel:
                    grade_horarios = ["07:00", "08:00", "09:00", "10:00", "11:00"]
                elif "Tarde" in medico_turno_sel:
                    grade_horarios = ["12:00", "13:00", "14:00", "15:00", "16:00"]
                else:
                    grade_horarios = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
            
                horarios_ocupados = listar_horarios_ocupados(medico_id_sel, data_texto)
                horarios_disponiveis = [h for h in grade_horarios if h not in horarios_ocupados]
            
                if not horarios_disponiveis:
                    st.error("❌ Não há horários livres para este médico nesta data. Escolha outro dia ou profissional.")
                    horario_selecionado = None
                else:
                    horario_selecionado = st.selectbox("4. Selecione o Horário Disponível:", horarios_disponiveis)

                st.write("")
                st.markdown("""
                    <style>
                    div.stButton > button:first-child {
                        background-color: #28a745; /* Cor de fundo Verde */
                        color: white; /* Cor do texto */
                        border-radius: 8px; /* Cantos arredondados */
                    }
                    div.stButton > button:first-child:hover {
                        background-color: #218838; /* Verde mais escuro quando passa o mouse */
                        color: white;
                        }
                    </style>
                """, unsafe_allow_html=True)
            
                if st.button("Confirmar Agendamento"):
                    if not horario_selecionado:
                        st.error("Não foi possível agendar. Selecione um horário válido.")
                    else:
                        inserir_consulta(tutor_id, pet_id_sel, medico_id_sel, data_texto, horario_selecionado)
                        st.success(f"🎉 Consulta agendada com sucesso para {pet_nome_sel} no dia {data_consulta.strftime('%d/%m/%Y')} às {horario_selecionado}!")
                        st.balloons()
                     
                        time.sleep(5)
                        st.rerun()

    with aba_historico:
        st.subheader("📋 Suas Consultas e Histórico")
        st.markdown("---")
    
        info_tutor = obter_tutor_id(st.session_state.usuario_id)
    
        if not info_tutor:
            st.info("Você ainda não possui dados cadastrados em seu perfil.")
        else:
            tutor_id = info_tutor[0]
            dados_consultas = listar_consultas_do_tutor(tutor_id)
        
            if not dados_consultas:
                st.info("🐾 Você ainda não realizou ou agendou nenhuma consulta.")
            else:
                df = pd.DataFrame(dados_consultas, columns=["ID", "Pet", "Veterinário", "Data", "Horário", "Status"])
            
                df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%Y")
            
                consultas_ativas = df[df["Status"].isin(["Agendado", "Em Andamento"])]
                historico_consultas = df[df["Status"].isin(["Concluído", "Cancelado", "Finalizado pelo Admin"])]
            
                st.markdown("### 🗓️ Próximas Consultas")
                if consultas_ativas.empty:
                    st.caption("Você não tem nenhuma consulta agendada para os próximos dias.")
                else:
                    st.dataframe(
                        consultas_ativas[["Pet", "Veterinário", "Data", "Horário", "Status"]], 
                        use_container_width=True,
                        hide_index=True
                    )
            
                    st.markdown("<br>", unsafe_allow_html=True)

                    st.markdown("### ⏳ Consultas Anteriores")

                    if historico_consultas.empty:
                        st.caption("Nenhum histórico de consultas anteriores encontrado.")
                    else:
                        st.dataframe(
                            historico_consultas[["Pet", "Veterinário", "Data", "Horário", "Status", "Diagnostico"]], 
                            use_container_width=True,
                            hide_index=True
                        )


def pagina_admin():
    st.success(f"👋 Olá Admin, {st.session_state.email}")
    st.markdown("---")

    st.title("⚙️ Painel do Administrador - Gestão da Clínica")
        
    aba_cadastrar, aba_agenda_medica, aba_gerenciar_consultas = st.tabs([
        "👨‍⚕️ Cadastrar Médico", 
        "⏰ Escalas e Horários", 
        "📋 Gerenciar Consultas"
        ])

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
            st.write("")
            botao_cadastrar = st.form_submit_button("Criar e Ativar Médico", type="primary")

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

    # Adapte para a sua lógica de papel médico
    st.title("🩺 Painel do Médico Veterinário")
    
    consultas_medico = listar_consultas_do_medico(st.session_state.usuario_id)
    
    if not consultas_medico:
        st.info("Nenhuma consulta agendada ou pendente para você no momento.")
    else:
        st.subheader("📋 Suas Consultas Cadastradas")
        
        for con in consultas_medico:
            c_id, tutor, pet, especie, raca, data, horario, status, diagnostico_atual = con
            
            # Formata um badge visual para o status
            cor_status = "🔴" if status == "Agendado" else "🟢" if status == "Concluído" else "🟡"
            
            with st.expander(f"{cor_status} Atendimento #{c_id} - {pet} ({tutor}) às {horario}"):
                st.write(f"**Paciente:** {pet} ({especie} - {raca})")
                st.write(f"**Data/Hora:** {data} às {horario}")
                st.write(f"**Status Atual:** `{status}`")
                
                diagnostico_input = st.text_area(
                    "Prontuário / Diagnóstico / Recomendações Médicas:", 
                    value=diagnostico_atual if diagnostico_atual else "",
                    key=f"diag_{c_id}"
                )
                
                st.markdown("""<style>div.stButton > button { border-radius: 5px; }</style>""", unsafe_allow_html=True)
                
                if st.button("💾 Finalizar Consulta e Salvar Laudo", key=f"btn_med_{c_id}"):
                    if not diagnostico_input.strip():
                        st.warning("⚠️ Por favor, insira o diagnóstico antes de concluir o atendimento.")
                    else:
                        medico_salvar_atendimento(c_id, diagnostico_input)
                        st.success(f"Consulta #{c_id} concluída com sucesso! Enviada para revisão do Admin.")
                        import time
                        time.sleep(1.5)
                        st.rerun()


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
        st.write("")
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
