import sys
import sqlite3
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLineEdit, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from langchain_ollama import OllamaLLM  
from langchain.agents import Tool, AgentExecutor, initialize_agent, AgentType

# ---- LLM MODELİ TANIMI ----
llm = OllamaLLM(model="sqlcoder:7b", temperature=0.0)
llm_chatbot = OllamaLLM(model="qwen3:1.7b", temperature=0.1)

# ---- NLTO-SQL AJANI ROL PLANI ----
agent_role_and_schema = """
You are an intelligent SQL assistant. Yu are only generating the perfect sql comands.
**IMPORTANT INSTRUCTIONS:**
- ONLY return the SQL query. Do NOT include any explanations, comments, or additional text.
- The SQL query must be valid and follow standard SQL syntax.
- The database is SQLite. Use only SQLite-compatible SQL syntax and functions (e.g., use strftime for date extraction).
- Do NOT use backticks (`) in the query.
- Never output <think> or <thinking>. Only output the SQL query.
The database contains the following tables:
1.Users (UserID, UserName, UserEmail, UserPassword, UserType)
2.Managers (ManagerID, UserID)
3.CrewMembers (CrewMemberID, UserID)
4.Projects (ProjectID, ProjectName, ProjectDescription, ProjectStatus, StartDate, EndDate)
5.Tasks (TaskID, TaskName, ProjectID, StartDate, EndDate, Status)
6.Activities (ActivityID, ActivityName, ActivityType, ScheduledDate, Duration, ResponsibleManagerID)
7.Customers (CustomerID, CustomerName, CustomerEmail, PhoneNumber)
8.addapro (EntryID, ManagerID, CrewMemberID, TaskID, ExperienceNotes, SubmissionDate)
"""

def generate_sql_from_nl(prompt):
    """ Doğal dili SQL'e çeviren fonksiyon """
    response = llm.invoke(agent_role_and_schema + f"\nUser: {prompt}\nSQL Query:")
    lines = [line for line in response.strip().split("\n") if line.strip()]
    # İlk SELECT, WITH, SHOW, DESCRIBE ile başlayan satırı bul
    for line in lines:
        clean_line = line.strip()
        # <s> veya başka bir token ile başlıyorsa temizle
        clean_line = re.sub(r"^<s>\s*", "", clean_line, flags=re.IGNORECASE)
        if re.match(r"^(select|with|show|describe)\s", clean_line, re.IGNORECASE):
            return clean_line
    # Hiçbiri yoksa ilk satırı temizle ve döndür
    if lines:
        return re.sub(r"^<s>\s*", "", lines[0].strip(), flags=re.IGNORECASE)
    return "Model sql sorgusu üretemedi."

def execute_sql_query(query):
    """ SQL sorgusunu çalıştırıp sonucu döndüren fonksiyon """
    try:
        conn = sqlite3.connect("/home/samur/projects/data/pro_mana.db")
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        print(f"SQL Execution Result: {rows}")
        return rows
    except Exception as e:
        error_message = f"SQL Error: {str(e)}"
        print(error_message)
        return error_message

def convert_sql_result_to_natural_language(user_query, sql_result):
    """ SQL çıktısını doğal dile çeviren fonksiyon """
    if not sql_result:
        return "No results found."
    if len(sql_result[0]) == 1:
        results = [str(row[0]) for row in sql_result]
    else:
        results = [", ".join(str(item) for item in row) for row in sql_result]
    results_text = ", ".join(results)
    return results_text

def process_sql_query(user_query):
    """ Kullanıcı girdisini SQL'e çevirme, sorguyu çalıştırma ve sonucu döndürme """
    sql_query = generate_sql_from_nl(user_query)
    print(f"Generated SQL Query: {sql_query}")

    # Tehlikeli/manipülatif sorguları engelle
    forbidden = r"^\s*(drop|delete|truncate|alter|update|insert|create|rename|attach|detach|pragma)\b"
    if re.match(forbidden, sql_query, re.IGNORECASE):
        return "Error: Manipulative queries (DDL/DML) are not allowed."

    sql_result = execute_sql_query(sql_query)
    if isinstance(sql_result, str) and sql_result.startswith("SQL Error"):
        return sql_result
    final_response = convert_sql_result_to_natural_language(user_query, sql_result)
    return final_response

def process_chatbot(prompt):
    response = llm_chatbot.invoke("\nUser: " + prompt)
    return response.strip()

# ---- PyQt6 ARAYÜZÜ ----
class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLM SQL Chatbot")
        self.setGeometry(100, 100, 600, 420)
        self.setStyleSheet("""
            background-color: #23272e;
            color: #e0e0e0;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 15px;
            border-radius: 14px;
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # ChatBox
        self.chat_box = QTextEdit(self)
        self.chat_box.setReadOnly(True)
        self.chat_box.setStyleSheet("""
            background-color: #22232a;
            color: #e0e0e0;
            border: none;
            border-radius: 10px;
            padding: 18px;
            font-size: 16px;
            min-height: 220px;
        """)
        layout.addWidget(self.chat_box, stretch=1)

        # Kullanıcı Girişi
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Mesajınızı yazın veya SQL için 'db:' ile başlayın...")
        self.user_input.setStyleSheet("""
            background-color: #292b33;
            color: #e0e0e0;
            padding: 12px;
            font-size: 16px;
            border-radius: 8px;
            border: none;
            min-width: 320px;
        """)
        input_layout.addWidget(self.user_input, stretch=1)

        # Gönder Butonu
        self.send_button = QPushButton("→", self)
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_button.setStyleSheet("""
            background-color: #3a3d46;
            color: #50fa7b;
            padding: 10px 0px;
            border-radius: 8px;
            font-size: 20px;
            font-weight: bold;
            min-width: 44px;
            max-width: 44px;
            border: none;
        """)
        self.send_button.clicked.connect(self.handle_user_input)
        input_layout.addWidget(self.send_button)

        # Boşluk
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        input_layout.addItem(spacer)

        layout.addLayout(input_layout)
        self.setLayout(layout)

    def handle_user_input(self):
        prompt = self.user_input.text()
        self.user_input.clear()
        # Demo için örnek cevap
        if prompt.startswith("db:"):
            query = prompt[3:]
            response = process_sql_query(query)
        else:
            response = "Çeviri veya sohbet: " + prompt
        self.chat_box.append(f"<b>You:</b> {prompt}")
        self.chat_box.append(f"<b>Bot:</b> {response}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatbot = ChatbotApp()
    chatbot.show()
    sys.exit(app.exec())