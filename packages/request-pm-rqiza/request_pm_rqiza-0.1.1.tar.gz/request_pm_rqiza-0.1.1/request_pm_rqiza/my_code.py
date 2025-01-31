def api_rqiza():
    return """
    from flask import Flask, request, jsonify
import json

app = Flask(__name__)


with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('item.json', 'r', encoding='utf-8') as file:
    items = json.load(file)


@app.route('/check_user', methods=['POST'])
def check_user():
    user_data = request.get_json()
    if not user_data or 'code' not in user_data or 'id' not in user_data:
        return jsonify({"error": "Invalid request"}), 400

    code = user_data['code']
    user_id = user_data['id']


    for user in data:
        if user['code'] == code and str(user['id']) == str(user_id):
            print("User found!")


            for item in items:
                if str(item['id']) == str(user_id):
                    return jsonify({
                        "fio": user['fio'],
                        "info1": item['info1'],
                        "info2": item['info2']
                    }), 200


            return jsonify({
                "fio": user['fio'],
                "info1": None,
                "info2": None
            }), 200


    return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
    """
def pyqt_rqiza():
    return """
    import sys
import json

import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DataApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("qwe")
        self.setGeometry(100,100,400,300)

        self.label_id = QLabel("ID")
        self.input_id = QLineEdit()
        self.input_id.setValidator(QIntValidator())

        self.label_code = QLabel("CODE")
        self.input_code = QLineEdit()

        self.label_info1 = QLabel("info1")
        self.input_info1 = QLineEdit()

        self.label_info2 = QLabel("info2")
        self.input_info2 = QLineEdit()

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)

        self.btn_submit = QPushButton("Добавить данные")
        self.btn_submit.clicked.connect(self.check_end_add_data)

        layout = QVBoxLayout()
        layout.addWidget(self.label_id)
        layout.addWidget(self.input_id)

        layout.addWidget(self.label_code)
        layout.addWidget(self.input_code)

        layout.addWidget(self.label_info1)
        layout.addWidget(self.input_info1)

        layout.addWidget(self.label_info2)
        layout.addWidget(self.input_info2)

        layout.addWidget(self.text_output)
        layout.addWidget(self.btn_submit)


        self.load_data()
        self.setLayout(layout)

    def load_data(self):
        with open('item.json','r',encoding='utf-8')as file:
            items = json.load(file)
            self.text_output.clear()
            for item in items:
                self.text_output.append(f"ID: {item['id']}, info1: {item['info1']},info2: {item['info2']}")

    def check_end_add_data(self):
        print("penis")
        user_id = self.input_id.text()
        code = self.input_code.text()
        if not user_id or not code:
            QMessageBox.critical(self,"error","error1")
            return
        response = requests.post(url='http://127.0.0.1:5000/check_user',json={"id":user_id,"code":code})
        if response.status_code == 200:
            info1 =self.input_info1.text()
            info2 =self.input_info2.text()
            if not info1 or not info2:
                QMessageBox.critical(self, "error", "error2")
                return
            found = False
            print("found")
            with open('item.json', 'r', encoding='utf-8') as file:
                items = json.load(file)
            for item in items:
                if str(item['id']) == user_id and str(item['code']) == code:
                    item['info1'] = info1
                    item['info2'] = info2
                    found = True
                    break
            if not found:
                new_item = {
                    "id": user_id,
                    "code": code,
                    "info1" :info1,
                    "info2": info2
                }
                items.append(new_item)
            with open('item.json','w',encoding='utf-8') as file:
                json.dump(items,file,indent=4,ensure_ascii=True)
            self.load_data()
            QMessageBox.information(self,"True","dannie dobavleni")
        else:
            QMessageBox.information(self, "Eror", f"{response.status_code}")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataApp()
    window.show()
    sys.exit(app.exec_())

    """
def android_rqiza():
    return """
    package com.example.kotlin_test

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.example.kotlin_test.R
import org.json.JSONObject

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val codeInput = findViewById<EditText>(R.id.codeInput)
        val idInput = findViewById<EditText>(R.id.idInput)
        val submitButton = findViewById<Button>(R.id.submitButton)
        val resultText = findViewById<TextView>(R.id.resultText)

        submitButton.setOnClickListener {
            val code = codeInput.text.toString()
            val id = idInput.text.toString().toIntOrNull()
            if (code.isNotEmpty() && id != null) sendRequest(code, id, resultText)
            else resultText.text = "Заполните все поля"
        }
    }

    private fun sendRequest(code: String, id: Int, resultText: TextView) {
        val url = "http://10.0.2.2:5000/check_user" // Замените на IP сервера
        val queue = Volley.newRequestQueue(this)
        val jsonBody = JSONObject().apply {
            put("code", code)
            put("id", id)
        }

        val request = JsonObjectRequest(
            Request.Method.POST, url, jsonBody,
            { response ->
                val fio = response.optString("fio", "Ошибка")
                val info1 = response.optString("info1", "Нет информации")
                val info2 = response.optString("info2", "Нет информации")
                resultText.text = "Фамилия: $fio\nInfo1: $info1\nInfo2: $info2"
            },
            { error ->
                error.printStackTrace()
                resultText.text = "Ошибка: ${error.message}"
            })
        queue.add(request)
    }
}



--------

<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <EditText
        android:id="@+id/codeInput"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Введите код" />

    <EditText
        android:id="@+id/idInput"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Введите ID"
        android:inputType="number" />

    <Button
        android:id="@+id/submitButton"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Отправить" />

    <TextView
        android:id="@+id/resultText"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Результат"
        android:textSize="18sp"
        android:gravity="center"
        android:padding="16dp" />
</LinearLayout>

    """