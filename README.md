# 🐶 Petz: Sistema de Clínica Veterinária

Este é um sistema completo de gerenciamento para uma clínica veterinária, desenvolvido em Python utilizando o **Streamlit** para a interface gráfica e **SQLite3** para o armazenamento de dados. O sistema conta com três níveis de acesso (Tutor, Médico Veterinário e Administrador), permitindo o controle de consultas, pets e relatórios médicos.

---

## 👥 Integrantes do Projeto
* **Andrei**
* **Douglas**

---

## 🛠️ Funcionalidades do Sistema

### 👤 Painel do Tutor (Cliente)
* Cadastrar e atualizar dados do perfil do tutor.
* Cadastrar animais de estimação (Pets).
* Agendar novas consultas escolhendo a data e o horário.
* Visualizar o histórico de consultas anteriores e diagnósticos.

### 🩺 Painel do Médico Veterinário
* Visualizar a agenda de consultas vinculadas ao seu perfil.
* Atualizar o status da consulta (Ex: *"Em Andamento"*, *"Concluído"*).
* Registrar diagnósticos e receitas médicas para o pet atendido.

### ⚙️ Painel do Administrador (Clínica)
* Cadastrar e gerenciar novos colaboradores (Veterinários e Atendentes).
* Aprovar, cancelar ou reagendar consultas.
* Vincular médicos veterinários disponíveis às consultas solicitadas pelos tutores.

---

## 📦 Pré-requisitos e Bibliotecas

O projeto utiliza uma combinação de bibliotecas nativas do próprio ecossistema do Python e dependências externas de terceiros.

### 🔹 Já vêm instaladas com o Python (Nativas):
* `sqlite3` — Armazenamento e gerenciamento do banco de dados relacional.
* `time` — Controle de tempo de execução e transições fluidas de tela.
* `hashlib` — Criptografia segura de senhas via hash para segurança dos usuários.

### 🔸 Precisam ser instaladas (Externas):
Para instalar as dependências externas necessárias de uma só vez, execute o comando abaixo no seu terminal:
```bash
* pip install streamlit pandas


# 🚀 Como Executar o Projeto

Você pode rodar a aplicação tanto direto pelo terminal do seu sistema operacional quanto pelo seu ambiente de desenvolvimento.

## 🖥️ Opção 1: Pelo Prompt de Comando (CMD / PowerShell)

### 1. Abra o seu terminal e navegue até a pasta onde os arquivos do projeto estão salvos:

```bash
cd caminho/para/a/pasta/clinica_veterinaria

### 2. Inicialize a aplicação do Streamlit executando o comando:
```bash
streamlit run clinica_veterinaria.py

### 3. O terminal gerará um endereço local (Ex: http://localhost:8501). Basta clicar no link gerado ou copiá-lo para o seu navegador de internet.

## 💻 Opção 2: Pelo Visual Studio Code (VS Code)

### 1. Abra a pasta do projeto no seu VS Code (File > Open Folder).

### 2. 💡 Recomendação: Vá até a aba de Extensões do VS Code (Ctrl + Shift + X) e instale a extensão oficial do Python (desenvolvida pela Microsoft) para facilitar a execução do código.

### 3. Abra o terminal integrado do VS Code (Ctrl + ' ou pelo menu Terminal > New Terminal).

### 4. Execute o comando de inicialização:
streamlit run clinica_veterinaria.py

### 5. Segure a tecla Ctrl e clique diretamente no endereço exibido no terminal para abrir o sistema automaticamente no seu navegador padrão.

# OBS: Na primeiríssima execução do sistema, o banco de dados SQLite (.db) será estruturado e criado de forma 100% automatizada na raiz do projeto com todas as tabelas necessárias devidamente configuradas.
