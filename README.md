<div style= "text-align: center;">

# Logistik – Distribution Center Management System
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
</div>
<div align="left">

![Python](https://img.shields.io/badge/Python-3.13.9-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black?logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite&logoColor=white)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen)
</div>

---

## 📦 Sobre o Projeto

**Logistik** é uma aplicação web desenvolvida com **Flask**, **Bootstrap 5** e **SQLAlchemy**, criada para gerenciar o fluxo operacional de um centro de distribuição.  
O sistema conta com **autenticação segura**, **controle de acesso por papéis (Admin e User)** e ferramentas completas para criar, editar e acompanhar entregas.

---

## 🚀 Funcionalidades

### 🔐 Autenticação e Acesso
- Login com gerenciamento de sessão  
- Controle de acesso por cargos (*Admin* e *User*)

### 👨‍💼 Admin
- CRUD completo de entregas  
- Cadastro de usuários  
- Visualização geral das entregas  
- Acesso total ao sistema  

### 👤 User
- Visualiza todas as entregas
- Atualiza status de entregas

### 🚚 Status das Entregas
- **Ongoing** — Preparando para despacho  
- **In Route** — A caminho  
- **Late** — Atrasada  
- **Delivered** — Concluída  

### 🎨 Interface Moderna
- Templates responsivos com **Bootstrap 5**

---

## 📁 Estrutura do Projeto
```bash
Logistik/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── models.py           # Database models (User, Delivery)
├── forms.py            # WTForms forms
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── routes/
│ ├── init.py
│ ├── auth.py           # Authentication routes
│ ├── admin.py          # Admin routes
│ └── user.py           # User routes
└── templates/
├── base.html
├── auth/
│ ├── login.html
│ └── register.html
├── admin/
│ ├── dashboard.html
│ ├── delivery_form.html
│ └── delivery_view.html
└── user/
├── dashboard.html
├── delivery_view.html
└── update_status.html
```

---

## 🛠️ Instalação

### ✔ Pré-requisitos
- Python **3.9+**
- pip instalado

### ✔ Passo a passo

**1. Clone o repositório:**
```bash
git clone https://github.com/PedroBigossi/logistik.git
```
**Crie um ambiente virtual:**

```bash
python -m venv venv
```
**Ative o ambiente:**

>Windows

```
venv\Scripts\activate
```
> Linux/Mac

```
source venv/bin/activate
```
**Instale as dependências:**

```
pip install -r requirements.txt
```
**Inicialize o banco de dados:**

```bash
python init_db.py
```
Usuários padrão criados:

- Admin → admin / admin123

- User → user / user123

**Execute a aplicação:**
```bash
python app.py
```
**Acesse no navegador:**
👉 http://localhost:5000

## 📌 Como Usar
### Admin
1. Gerencia todas as entregas no dashboard
2. Cria novas entregas
3. Edita/exclui entregas
4. Cadastra usuários

### User
1.Visualiza todas as entregas
2. Atualiza status das entregas

## 🗄 Banco de Dados
O projeto utiliza **SQLite** por padrão (logistik.db).
Para alterar para PostgreSQL/MySQL, modifique o SQLALCHEMY_DATABASE_URI em config.py.

## 🧩 Customização
Novos status → atualizar forms.py e templates

Novos campos → alterar modelo em models.py + forms + templates

Novo layout → editar classes Bootstrap no base.html

## 🐛 Problemas Comuns
Problema	Solução
Erros no banco	Deletar logistik.db e rodar init_db.py
Import errors	pip install -r requirements.txt
Porta ocupada	app.run(debug=True, port=5001)

## 📜 License
Projeto liberado para uso educacional e empresarial.

## 💬 Suporte
O código inclui comentários detalhados explicando cada parte da aplicação.

---