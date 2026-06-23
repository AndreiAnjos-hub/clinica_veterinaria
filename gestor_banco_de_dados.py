import sqlite3
import hashlib

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
            Turno TEXT UNIQUE,
            FOREIGN KEY (Colaborador_ID) REFERENCES Colaboradores(ID),
            FOREIGN KEY (Nome) REFERENCES Colaboradores(Nome),
            FOREIGN KEY (Email) REFERENCES Colaboradores(Email)
        )
    ''')

    cursor_clinica.execute('''
        CREATE TABLE IF NOT EXISTS Consultas (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Tutor_ID INTEGER,
            Pet_ID INTEGER,
            Medico_ID INTEGER,
            Data TEXT,
            Horario TEXT,
            Status TEXT DEFAULT 'Agendado', -- 'Agendado', 'Concluído', 'Cancelado'
            Diagnóstico TEXT,
            FOREIGN KEY (Tutor_ID) REFERENCES Tutores(ID),
            FOREIGN KEY (Pet_ID) REFERENCES Pets(ID),
            FOREIGN KEY (Medico_ID) REFERENCES Médicos(ID)
        )
    ''')

    conexao_clinica.commit()
    conexao_clinica.close()

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

def buscar_tutor_por_usuario(usuario_id):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute("SELECT Nome, Telefone FROM Tutores WHERE Usuario_ID = ?", (usuario_id,))
    tutor = cursor_clinica.fetchone()
    cursor_clinica.close()
    conexao_clinica.close()
    return tutor 

def salvar_ou_atualizar_tutor(usuario_id, nome, email, telefone):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    
    cursor_clinica.execute("SELECT ID FROM Tutores WHERE Usuario_ID = ?", (usuario_id,))
    existe = cursor_clinica.fetchone()
    
    if existe:
        cursor_clinica.execute('''
            UPDATE Tutores 
            SET Nome = ?, Telefone = ? 
            WHERE Usuario_ID = ?
        ''', (nome, telefone, usuario_id))
    else:
        cursor_clinica.execute('''
            INSERT INTO Tutores (Usuario_ID, Nome, Email, Telefone) 
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, nome, email, telefone))
        
    conexao_clinica.commit()
    cursor_clinica.close()
    conexao_clinica.close()

def obter_tutor_id(usuario_id):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute("SELECT ID, Nome FROM Tutores WHERE Usuario_ID = ?", (usuario_id,))
    tutor = cursor_clinica.fetchone()
    cursor_clinica.close()
    conexao_clinica.close()
    return tutor 

def listar_pets_do_tutor(tutor_id):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute("SELECT ID, Pet, Especie, Raca, Sexo FROM Pets WHERE Tutor_ID = ?", (tutor_id,))
    pets = cursor_clinica.fetchall()
    cursor_clinica.close()
    conexao_clinica.close()
    return pets 

def salvar_ou_atualizar_pet(pet_id, tutor_id, nome_tutor, nome_pet, especie, raca, sexo):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    
    if pet_id: 
        cursor_clinica.execute('''
            UPDATE Pets 
            SET Pet = ?, Especie = ?, Raca = ?, Sexo = ? 
            WHERE ID = ?
        ''', (nome_pet, especie, raca, sexo, pet_id))
    else: 
        cursor_clinica.execute('''
            INSERT INTO Pets (Tutor_ID, Tutor, Pet, Especie, Raca, Sexo) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (tutor_id, nome_tutor, nome_pet, especie, raca, sexo))
        
    conexao_clinica.commit()
    cursor_clinica.close()
    conexao_clinica.close()

def listar_usuarios_colaboradores_sem_crmv():
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    
    cursor_clinica.execute('''
        SELECT C.ID, C.Nome, C.Email 
        FROM Colaboradores C
        JOIN Usuarios U ON C.Usuario_ID = U.ID
        WHERE C.Tipo = 'Médico' 
          AND U.Tipo = 'Colaborador'
          AND C.ID NOT IN (SELECT Colaborador_ID FROM Médicos)
    ''')
    
    colaboradores_pendentes = cursor_clinica.fetchall()
    cursor_clinica.close()
    conexao_clinica.close()
    return colaboradores_pendentes 

def admin_cadastrar_medico_completo(nome, email, senha_plana, crmv, turno):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    
    try:
        senha_hash = hashlib.sha256(senha_plana.encode()).hexdigest()
        
        cursor_clinica.execute('''
            INSERT INTO Usuarios (Email, Senha, Tipo)
            VALUES (?, ?, 'Colaborador')
        ''', (email, senha_hash))
        
        usuario_id = cursor_clinica.lastrowid

        cursor_clinica.execute('''
            INSERT INTO Colaboradores (Usuario_ID, Nome, Email, Tipo)
            VALUES (?, ?, ?, 'Médico')
        ''', (usuario_id, nome, email))
        
        colaborador_id = cursor_clinica.lastrowid
        
        cursor_clinica.execute('''
            INSERT INTO Médicos (Colaborador_ID, Nome, CRMV, Email, Turno)
            VALUES (?, ?, ?, ?, ?)
        ''', (colaborador_id, nome, crmv, email, turno))
        
        conexao_clinica.commit()
        return True, "Médico cadastrado com sucesso!"
        
    except sqlite3.IntegrityError:
        return False, "Erro de duplicidade: Verifique se o E-mail ou CRMV já estão cadastrados."
    except Exception as e:
        return False, f"Erro inesperado: {e}"
    finally:
        cursor_clinica.close()
        conexao_clinica.close()

def listar_consultas_geral():
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute('''
        SELECT 
            C.ID, T.Nome, P.Pet, M.Nome, C.Data, C.Horario, C.Status
        FROM Consultas C
        JOIN Tutores T ON C.Tutor_ID = T.ID
        JOIN Pets P ON C.Pet_ID = P.ID
        LEFT JOIN Médicos M ON C.Medico_ID = M.ID
    ''')
    consultas = cursor_clinica.fetchall()
    cursor_clinica.close()
    conexao_clinica.close()
    return consultas

def atualizar_status_e_medico_consulta(consulta_id, medico_id, novo_status):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute('''
        UPDATE Consultas
        SET Medico_ID = ?, Status = ?
        WHERE ID = ?
    ''', (medico_id, novo_status, consulta_id))
    conexao_clinica.commit()
    cursor_clinica.close()
    conexao_clinica.close()

def listar_medicos_disponiveis():
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute("SELECT ID, Nome FROM Médicos")
    medicos = cursor_clinica.fetchall()
    cursor_clinica.close()
    conexao_clinica.close()
    return medicos

def listar_medicos_com_turno():
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    try:
        cursor_clinica.execute("SELECT ID, Nome, Turno FROM Médicos")
        medicos = cursor_clinica.fetchall()
    except sqlite3.OperationalError:
        cursor_clinica.execute("SELECT ID, Nome, 'Integral (07h às 17h)' FROM Médicos")
        medicos = cursor_clinica.fetchall()
        
    cursor_clinica.close()
    conexao_clinica.close()
    return medicos

def listar_horarios_ocupados(medico_id, data_texto):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()

    cursor_clinica.execute('''
        SELECT Horario FROM Consultas 
        WHERE Medico_ID = ? AND Data = ? AND Status != 'Cancelado'
    ''', (medico_id, data_texto))
    
    agendados = cursor_clinica.fetchall()
    cursor_clinica.close()
    conexao_clinica.close()
    return [item[0] for item in agendados]

def inserir_consulta(tutor_id, pet_id, medico_id, data_texto, horario_texto):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute('''
        INSERT INTO Consultas (Tutor_ID, Pet_ID, Medico_ID, Data, Horario, Status)
        VALUES (?, ?, ?, ?, ?, 'Agendado')
    ''', (tutor_id, pet_id, medico_id, data_texto, horario_texto))
    conexao_clinica.commit()
    cursor_clinica.close()
    conexao_clinica.close()

def listar_consultas_do_tutor(tutor_id):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    
    cursor_clinica.execute('''
        SELECT 
            C.ID, 
            P.Pet AS Nome_Pet, 
            IFNULL(M.Nome, 'A definir') AS Nome_Medico, 
            C.Data, 
            C.Horario, 
            C.Status
        FROM Consultas C
        JOIN Pets P ON C.Pet_ID = P.ID
        LEFT JOIN Médicos M ON C.Medico_ID = M.ID
        WHERE C.Tutor_ID = ?
        ORDER BY C.Data DESC, C.Horario DESC
    ''', (tutor_id,))
    
    consultas = cursor_clinica.fetchall()
    cursor_clinica.close()
    conexao_clinica.close()
    return consultas 

def listar_consultas_do_medico(medico_usuario_id):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()

    cursor_clinica.execute('''
        SELECT 
            C.ID, T.Nome AS Tutor, P.Pet AS Pet, P.Especie, P.Raca, C.Data, C.Horario, C.Status, C.Diagnostico
        FROM Consultas C
        JOIN Pets P ON C.Pet_ID = P.ID
        JOIN Tutores T ON C.Tutor_ID = T.ID
        JOIN Médicos M ON C.Medico_ID = M.ID
        JOIN Colaboradores COL ON M.Colaborador_ID = COL.ID
        WHERE COL.Usuario_ID = ? AND C.Status IN ('Agendado', 'Em Andamento', 'Concluído')
        ORDER BY C.Data ASC, C.Horario ASC
    ''', (medico_usuario_id,))
    
    consultas = cursor_clinica.fetchall()
    cursor_clinica.close()
    conexao_clinica.close()
    return consultas

def medico_salvar_atendimento(consulta_id, diagnostico):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute('''
        UPDATE Consultas
        SET Diagnostico = ?, Status = 'Concluído'
        WHERE ID = ?
    ''', (diagnostico, consulta_id))
    conexao_clinica.commit()
    cursor_clinica.close()
    conexao_clinica.close()

def admin_enviar_prontuario(consulta_id):
    conexao_clinica = conectar_banco()
    cursor_clinica = conexao_clinica.cursor()
    cursor_clinica.execute('''
        UPDATE Consultas
        SET Status = 'Finalizado pelo Admin'
        WHERE ID = ?
    ''', (consulta_id,))
    conexao_clinica.commit()
    cursor_clinica.close()
    conexao_clinica.close()





# def listar_consultas_geral():
#     conexao_clinica = conectar_banco()
#     cursor_clinica = conexao_clinica.cursor()
#     # Query que junta os dados das consultas com nomes de tutores, pets e médicos
#     cursor_clinica.execute('''
#         SELECT 
#             C.ID, T.Nome, P.Pet, M.Nome, C.Data, C.Horario, C.Status
#         FROM Consultas C
#         JOIN Tutores T ON C.Tutor_ID = T.ID
#         JOIN Pets P ON C.Pet_ID = P.ID
#         LEFT JOIN Médicos M ON C.Medico_ID = M.ID
#     ''')
#     consultas = cursor_clinica.fetchall()
#     cursor_clinica.close()
#     conexao_clinica.close()
#     return consultas

# def atualizar_status_e_medico_consulta(consulta_id, medico_id, novo_status):
#     conexao_clinica = conectar_banco()
#     cursor_clinica = conexao_clinica.cursor()
#     cursor_clinica.execute('''
#         UPDATE Consultas
#         SET Medico_ID = ?, Status = ?
#         WHERE ID = ?
#     ''', (medico_id, novo_status, consulta_id))
#     conexao_clinica.commit()
#     cursor_clinica.close()
#     conexao_clinica.close()

# def listar_medicos_disponiveis():
#     conexao_clinica = conectar_banco()
#     cursor_clinica = conexao_clinica.cursor()
#     cursor_clinica.execute("SELECT ID, Nome FROM Médicos")
#     medicos = cursor_clinica.fetchall()
#     cursor_clinica.close()
#     conexao_clinica.close()
#     return medicos