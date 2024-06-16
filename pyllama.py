import sys
import requests
from PySide6.QtGui import QTextCursor, QAction
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QMessageBox, QFileDialog
)

class ChatApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pyllama')
        self.setGeometry(100, 100, 600, 400)
        self.model = "llama3" #default model

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        main_layout.addWidget(self.text_area)

        input_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)

        self.input_field = QLineEdit()
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        model_label = QLabel("Model:")
        input_layout.addWidget(model_label)

        self.model_field = QLineEdit(self.model)
        input_layout.addWidget(self.model_field)

        export_button = QPushButton('Export Chat')
        export_button.clicked.connect(self.export_chat)
        input_layout.addWidget(export_button)

    def send_message(self):
        message = self.input_field.text().strip()
        model = self.model_field.text().strip()

        if message:
            self.display_message(f"You: {message}", user=True)

            generated_content = self.generate(message, model)

            self.display_message(f"{model}: {generated_content}", user=False)

            self.input_field.clear()

    def display_message(self, message, user=False):
        cursor = self.text_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.text_area.setTextCursor(cursor)

        if user:
            self.text_area.insertPlainText(message + "\n")
        else:
            self.text_area.insertPlainText(message + "\n")

        self.text_area.ensureCursorVisible()

    def generate(self, message, model):
        if model:
            self.model = model

        url = 'http://localhost:11434/api/chat'
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "stream": False
        }
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            generated_content = response.json()["message"]["content"]
        except requests.exceptions.RequestException as e:
            generated_content = f"Error: {e}"
        return generated_content

    def export_chat(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chat", "", "Text Files (*.txt)", options=options)
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.toPlainText())
                QMessageBox.information(self, "Export Successful", "Chat exported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Error exporting chat: {e}")

app = QApplication(sys.argv)
chat_app = ChatApp()
chat_app.show()
sys.exit(app.exec())
