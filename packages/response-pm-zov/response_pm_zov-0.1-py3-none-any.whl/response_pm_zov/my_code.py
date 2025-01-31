def response_api():
    return """
    from flask import Flask, request, jsonify
import json

app = Flask(__name__)

with open('users.json', 'r') as f:
    users = json.load(f)

with open('data.json', 'r') as f:
    data = json.load(f)

@app.route('/save', methods=['POST'])
def save():
    new_data = request.json
    id = new_data['id']
    code = new_data['code']

    user_exists = any(user['id'] == int(id) and user['code'] == code for user in users)
    if not user_exists:
        return jsonify({"error": "User not found"}), 404

    user_data_exists = False
    for index, item in enumerate(data):
        if item['id'] == id and item['code'] == code:
            data[index] = new_data
            user_data_exists = True
            break

    if not user_data_exists:
        data.append(new_data)

    with open('data.json', 'w') as f:
        json.dump(data, f)

    return jsonify({"message": "Data saved successfully"}), 200

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/delete', methods=['POST'])
def delete():
    delete_data = request.json
    id = delete_data['id']
    code = delete_data['code']

    global data
    data = [item for item in data if not (item['id'] == id and item['code'] == code)]

    with open('data.json', 'w') as f:
        json.dump(data, f)

    return jsonify({"message": "Data deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)

    """
def response_pyqt():
    return """
    import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My App')

        layout = QVBoxLayout()

        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText('Enter ID')
        layout.addWidget(self.id_input)

        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText('Enter Code')
        layout.addWidget(self.code_input)

        self.info1_input = QLineEdit(self)
        self.info1_input.setPlaceholderText('Enter Info 1')
        layout.addWidget(self.info1_input)

        self.info2_input = QLineEdit(self)
        self.info2_input.setPlaceholderText('Enter Info 2')
        layout.addWidget(self.info2_input)

        self.save_button = QPushButton('Save Data', self)
        self.save_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_button)

        self.delete_button = QPushButton('Delete Data', self)
        self.delete_button.clicked.connect(self.delete_data)
        layout.addWidget(self.delete_button)

        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        self.show_data()

    def save_data(self):
        id = self.id_input.text()
        code = self.code_input.text()
        info1 = self.info1_input.text()
        info2 = self.info2_input.text()

        data = {
            "id": id,
            "code": code,
            "info1": info1,
            "info2": info2
        }

        response = requests.post('http://127.0.0.1:5000/save', json=data)
        if response.status_code == 200:
            print("Data saved successfully")
            self.show_data()
        else:
            print("Failed to save data")

    def delete_data(self):
        id = self.id_input.text()
        code = self.code_input.text()

        if not id or not code:
            QMessageBox.warning(self, "Error", "Please enter ID and Code to delete data.")
            return

        delete_data = {
            "id": id,
            "code": code
        }

        response = requests.post('http://127.0.0.1:5000/delete', json=delete_data)
        if response.status_code == 200:
            print("Data deleted successfully")
            self.show_data()
        else:
            print("Failed to delete data")

    def show_data(self):
        response = requests.get('http://127.0.0.1:5000/data')
        if response.status_code == 200:
            data = response.json()
            self.list_widget.clear()
            for item in data:
                self.list_widget.addItem(f"ID: {item['id']}, Code: {item['code']}, Info1: {item['info1']}, Info2: {item['info2']}")
        else:
            print("Failed to load data")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())

    """
