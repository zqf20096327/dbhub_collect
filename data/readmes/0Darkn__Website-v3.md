**Qt (Desktop)**, **Flask (Web)**, **SQLite (Banco de Dados)** duas matrizes de 100 \times 100 campos de texto é um excelente projeto para entender como integrar diferentes tecnologias.
Como criar uma matriz de 100 \times 100 (10.000 caixas de texto) diretamente no HTML ou no Qt de forma estática travaria a aplicação, a melhor prática é focar na **estrutura do sistema** e usar loops dinâmicos para renderizar a interface.
Aqui está o desenvolvimento completo do ecossistema, dividido entre o **Backend (Flask + SQLite)**, o **Frontend Web (HTML/CSS/JS)** e o **App Desktop (Python + PyQt/PySide)**.
## 1. O Banco de Dados e o Servidor Web (Flask + SQLite)
O Flask vai servir tanto como a API para gerenciar os usuários quanto como o servidor que entrega a página web.
Crie um arquivo chamado app.py:
```python
import sqlite3
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)


# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def init_db():
    """Cria a tabela de usuários se ela não existir."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """
    )
    conn.commit()
    conn.close()


# --- ROTAS DA API REST (Para o CRUD de Usuários) ---


@app.route("/api/users", methods=["GET"])
def get_users():
    """Retorna todos os usuários cadastrados."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = [
        {"id": row[0], "name": row[1], "email": row[2]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(users)


@app.route("/api/users", methods=["POST"])
def add_user():
    """Adiciona un novo usuário."""
    data = request.json
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (data["name"], data["email"]),
        )
        conn.commit()
        return (
            jsonify(
                {"message": "Usuário adicionado!", "id": cursor.lastrowid}
            ),
            201,
        )
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email já cadastrado!"}), 400
    finally:
        conn.close()


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Atualiza os dados de um usuário existente."""
    data = request.json
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (data["name"], data["email"], user_id),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Usuário atualizado!"})


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Remove um usuário do banco."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Usuário removido!"})


# --- ROTA DO WEBSITE HTML ---
# Código HTML/CSS/JS injetado diretamente para simplificar o exemplo em um único arquivo
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Gerenciador e Matrizes</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f4f4f9; }
        .container { max-width: 1200px; margin: auto; }
        .section { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        input, button { padding: 8px; margin: 5px 0; display: inline-block; }
        button { background: #007BFF; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .matrix-container { display: flex; gap: 20px; overflow-x: auto; }
        .matrix-wrapper { flex: 1; }
        /* Grid dinâmico para a matriz 100x100 */
        .matrix { 
            display: grid; 
            grid-template-columns: repeat(100, 40px); 
            gap: 2px; 
            max-height: 400px; 
            overflow: auto; 
            border: 1px solid #ccc;
            padding: 5px;
        }
        .matrix input { width: 100%; box-sizing: border-box; padding: 2px; text-align: center; font-size: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Painel de Controle Web</h2>
        
        <div class="section">
            <h3>Gerenciar Usuários</h3>
            <input type="hidden" id="userId">
            <input type="text" id="userName" placeholder="Nome">
            <input type="email" id="userEmail" placeholder="Email">
            <button onclick="saveUser()">Salvar Usuário</button>
            <ul id="userList"></ul>
        </div>

        <div class="section">
            <h3>Matrizes Dinâmicas (100 x 100)</h3>
            <div class="matrix-container">
                <div class="matrix-wrapper">
                    <h4>Matriz A</h4>
                    <div id="matrixA" class="matrix"></div>
                </div>
                <div class="matrix-wrapper">
                    <h4>Matriz B</h4>
                    <div id="matrixB" class="matrix"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_URL = '/api/users';

        // Carrega usuários ao iniciar
        document.addEventListener('DOMContentLoaded', () => {
            loadUsers();
            createMatrix('matrixA');
            createMatrix('matrixB');
        });

        // Gera a matriz 100x100 de inputs de forma performática
        function createMatrix(matrixId) {
            const container = document.getElementById(matrixId);
            const fragment = document.createDocumentFragment();
            for (let i = 0; i < 100 * 100; i++) {
                const input = document.createElement('input');
                input.type = 'text';
                input.maxLength = 3; // Limita caracteres para não quebrar o layout
                fragment.appendChild(input);
            }
            container.appendChild(fragment);
        }

        // Busca usuários no backend
        async function loadUsers() {
            const res = await fetch(API_URL);
            const users = await res.json();
            const list = document.getElementById('userList');
            list.innerHTML = '';
            users.forEach(u => {
                list.innerHTML += `<li>${u.name} (${u.email}) 
                    <button onclick="editUser(${u.id}, '${u.name}', '${u.email}')">Editar</button>
                    <button style="background:red;" onclick="deleteUser(${u.id})">Excluir</button>
                </li>`;
            });
        }

        // Salva (Adiciona ou Atualiza) usuário
        async function saveUser() {
            const id = document.getElementById('userId').value;
            const name = document.getElementById('userName').value;
            const email = document.getElementById('userEmail').value;
            
            const method = id ? 'PUT' : 'POST';
            const url = id ? `${API_URL}/${id}` : API_URL;

            await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email })
            });

            // Limpa formulário
            document.getElementById('userId').value = '';
            document.getElementById('userName').value = '';
            document.getElementById('userEmail').value = '';
            loadUsers();
        }

        function editUser(id, name, email) {
            document.getElementById('userId').value = id;
            document.getElementById('userName').value = name;
            document.getElementById('userEmail').value = email;
        }

        async function deleteUser(id) {
            if(confirm('Deseja mesmo excluir?')) {
                await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
                loadUsers();
            }
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


if __name__ == "__main__":
    init_db()
    # Executa o servidor Flask na porta 5000
    app.run(debug=True, port=5000)

```
## 2. A Aplicação Desktop (Python + PyQt6)
Para a interface desktop, usamos o **PyQt6**. Ele vai se comunicar diretamente com o banco de dados SQLite para o CRUD e renderizar as duas matrizes usando componentes de tabela (QTableWidget), que lidam com 100 \times 100 campos de entrada de forma muito mais leve do que criar 20.000 widgets individuais.
Instale o PyQt6 antes de rodar: pip install PyQt6
Crie um arquivo chamado desktop_app.py:
```python
import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QMessageBox,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador Desktop e Matrizes")
        self.setGeometry(100, 100, 1000, 700)

        # Widget Principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # --- PAINEL ESQUERDO: CRUD ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.label_info = QLabel("Gerenciar Usuários:")
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nome")
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")

        self.btn_add = QPushButton("Adicionar Usuário")
        self.btn_update = QPushButton("Atualizar Selecionado")
        self.btn_delete = QPushButton("Remover Selecionado")

        self.user_list = QListWidget()

        # Adiciona os elementos ao layout esquerdo
        left_layout.addWidget(self.label_info)
        left_layout.addWidget(self.input_name)
        left_layout.addWidget(self.input_email)
        left_layout.addWidget(self.btn_add)
        left_layout.addWidget(self.btn_update)
        left_layout.addWidget(self.btn_delete)
        left_layout.addWidget(self.user_list)

        # --- PAINEL DIREITO: MATRIZES ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Matriz A (100x100) usando QTableWidget para performance
        right_layout.addWidget(QLabel("Matriz A (100 x 100)"))
        self.matrix_a = QTableWidget(100, 100)
        right_layout.addWidget(self.matrix_a)

        # Matriz B (100x100)
        right_layout.addWidget(QLabel("Matriz B (100 x 100)"))
        self.matrix_b = QTableWidget(100, 100)
        right_layout.addWidget(self.matrix_b)

        # Junta os dois painéis na tela principal
        main_layout.addWidget(left_panel, 1)  # Proporção 1
        main_layout.addWidget(right_panel, 2)  # Proporção 2 (mais largo)

        # Eventos dos Botões e Cliques
        self.btn_add.clicked.connect(self.add_user)
        self.btn_update.clicked.connect(self.update_user)
        self.btn_delete.clicked.connect(self.delete_user)
        self.user_list.itemClicked.connect(self.load_user_fields)

        # Inicializações
        self.selected_user_id = None
        self.load_users_from_db()

    # --- FUNÇÕES DE BANCO DE DADOS (CRUD) ---

    def load_users_from_db(self):
        """Busca os usuários do SQLite e joga na lista da interface."""
        self.user_list.clear()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            # Armazena o ID escondido dentro do item da lista
            item_text = f"{row[0]} - {row[1]} ({row[2]})"
            self.user_list.addItem(item_text)
        conn.close()

    def load_user_fields(self, item):
        """Preenche os inputs de texto quando clica em um usuário da lista."""
        parts = item.text().split(" - ")
        self.selected_user_id = parts[0]
        name_email = parts[1].split(" (")
        self.input_name.setText(name_email[0])
        self.input_email.setText(name_email[1].replace(")", ""))

    def add_user(self):
        name = self.input_name.text()
        email = self.input_email.text()
        if name and email:
            try:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    (name, email),
                )
                conn.commit()
                conn.close()
                self.load_users_from_db()
                self.clear_inputs()
            except sqlite3.IntegrityError:
                QMessageBox.warning(
                    self, "Erro", "Este e-mail já existe no sistema."
                )
        else:
            QMessageBox.warning(
                self, "Erro", "Preencha todos os campos vazios!"
            )

    def update_user(self):
        if not self.selected_user_id:
            return
        name = self.input_name.text()
        email = self.input_email.text()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name, email, self.selected_user_id),
        )
        conn.commit()
        conn.close()
        self.load_users_from_db()
        self.clear_inputs()

    def delete_user(self):
        if not self.selected_user_id:
            return
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (self.selected_user_id,))
        conn.commit()
        conn.close()
        self.load_users_from_db()
        self.clear_inputs()

    def clear_inputs(self):
        self.input_name.clear()
        self.input_email.clear()
        self.selected_user_id = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

```
## 💡 Como Tudo Funciona (Explicação Passo a Passo)
### O Banco de Dados Centralizado (database.db)
Tanto o script web (Flask) quanto o aplicativo desktop (PyQt6) apontam para o arquivo database.db. Se você adicionar um usuário pelo aplicativo desktop, ele aparecerá na página Web assim que você atualizá-la (e vice-versa).
### Desafio de Performance: As Matrizes 100 \times 100
Criar 10.000 caixas de texto estruturais de forma literal (uma por uma no código) destruiria a legibilidade do script e travaria o computador por falta de memória. A resolução foi:
 1. **No Website:** Usamos propriedades modernas de CSS (display: grid) e o JavaScript gerou os elementos em lote usando um loop de fragmentos (DocumentFragment), o que impede o navegador de renderizar a página 10.000 vezes, fazendo o processo em milissegundos.
 2. **No Qt (Desktop):** Usamos o componente nativo QTableWidget. Ele cria uma planilha otimizada de 100 linhas por 100 colunas onde cada célula já atua nativamente como uma caixa de texto ao dar duplo clique, economizando o processamento do sistema operacional.
### Como rodar o ecossistema:
 1. Em um terminal, execute o backend: python app.py
 2. Abra o navegador e acesse: http://127.0.0.1:5000/
 3. Em outro terminal, execute o app desktop: python desktop_app.py
 4. 
