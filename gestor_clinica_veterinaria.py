
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


import random
import hashlib
import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime


def conectar_banco():
    return sqlite3.connect("BandoDeDados_ClinicaVeterinaria.db")

def criar_tabelas():
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()

    cursor_clinica.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Email TEXT UNIQUE,
            Senha TEXT,
            Tipo TEXT CHECK(Tipo IN ('Usuário','Colaborador')) NOT NULL
        )
    ''')

    cursor_clinica.execute('''
        CREATE TABLE IF NOT EXISTS Tutores (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Usuario_ID INTEGER,
            Nome TEXT,
            Email TEXT UNIQUE,
            Telefone TEXT,
            FOREIGN KEY (Usuario_ID) REFERENCES Usuarios(ID),
            FOREIGN KEY (Email) REFERENCES Usuarios(Email)
        )
    ''')
    
    cursor_clinica.execute('''
        CREATE TABLE IF NOT EXISTS Pets (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Tutor_ID INTEGER,
            Tutor TEXT,
            Pet TEXT,
            Especie TEXT,
            Raca REAL,
            Sexo TEXT,
            FOREIGN KEY (Tutor_ID) REFERENCES Tutores(ID),
            FOREIGN KEY (Tutor) REFERENCES Tutores(Nome)
        )
    ''')

    cursor_clinica.execute('''
        CREATE TABLE IF NOT EXISTS Colaboradores (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Usuario_ID INTEGER UNIQUE,
            Nome TEXT,
            Email TEXT UNIQUE,
            Tipo TEXT CHECK(Tipo IN ('Admin','Médico')) NOT NULL,
            FOREIGN KEY (Usuario_ID) REFERENCES Usuarios(ID)
        )
    ''')

    cursor_clinica.execute('''
        CREATE TABLE IF NOT EXISTS Médicos (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Colaborador_ID INTEGER UNIQUE,
            Nome TEXT,
            CRMV TEXT UNIQUE,
            Email TEXT UNIQUE,
            FOREIGN KEY (Colaborador_ID) REFERENCES Colaboradores(ID),
            FOREIGN KEY (Nome) REFERENCES Colaboradores(Nome),
            FOREIGN KEY (Email) REFERENCES Colaboradores(Email)
        )
    ''')

    conexao_clinica.commit()
    conexao_clinica.close()

# Garante a criação das tabelas
criar_tabelas()

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def buscar_usuario(email, senha):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute("SELECT ID, Email FROM Usuarios WHERE Email = ? AND Senha = ?", (email, senha))
    usuario = cursor_clinica.fetchone()
    cursor_clinica.close()
    conexao_clinica.close()
    return usuario

def buscar_colaborador(email):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute("SELECT ID, Nome, Email FROM Colaboradores WHERE Email = ?", (email,))
    colaborador = cursor_clinica.fetchone()
    cursor_clinica.close()
    conexao_clinica.close()
    return colaborador


## --- INSERÇÃO DE DADOS TESTE ---

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
            INSERT OR IGNORE INTO Médicos (Colaborador_ID, Nome, CRMV, Email) VALUES (?, ?, ?, ?)
        ''', (colaborador[0], colaborador[1], "827477", colaborador[2]))
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
            INSERT OR IGNORE INTO Médicos (Colaborador_ID, Nome, CRMV, Email) VALUES (?, ?, ?, ?)
        ''', (colaborador[0], colaborador[1], "209891", colaborador[2]))
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
    st.success(f"👋 Olá, {st.session_state.email}")
    st.markdown("---")

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
