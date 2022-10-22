import pandas as pd
from flask import Flask, request, render_template
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

ds = pd.read_csv('data.csv', usecols=[
                 'age', 'income', 'student', 'credit_rating', 'buys_computer'])

# mengambil data tiap atribut
x = ds.iloc[:, :-1].values  # atribut x (age,income,student,credit_rating)
y = ds.iloc[:, -1].values  # atribut y (buys_computer)

# membuat encoder (mengubah string menjadi angka)
encoder = LabelEncoder()

# mengubah value string menjadi angka
x[:, 0] = encoder.fit_transform(x[:, 0])  # age
x[:, 1] = encoder.fit_transform(x[:, 1])  # income
x[:, 2] = encoder.fit_transform(x[:, 2])  # student
x[:, 3] = encoder.fit_transform(x[:, 3])  # credit_rating
y = encoder.fit_transform(y)  # buy_computer

# Membuat Pengklasifikasi menggunakan DecisionTree
model = DecisionTreeClassifier()

# train model
model.fit(x, y)

# tampilan index (halaman awal)

3


@app.route('/')
def index():
    # menampilkan template
    return render_template('index.html', predicted="?", age="?", income="?", student="?", credit_rating="?")

# tampilan setelah button prediksi di klik
# diarahkan ke halaman /prediction
# data dikirimkan menggunakan method post


@app.route('/prediction', methods=['POST'])
def prediction():
    # mengambil data masukan user berdasarkan name form input
    age = int(request.form['age'])
    income = int(request.form['income'])
    student = int(request.form['student'])
    credit_rating = int(request.form['credit_rating'])

    # memprediksi masukan user berdasarkan model
    predicted = model.predict([[age, income, student, credit_rating]])

    # mengubah angka encoder menjadi string
    # age
    if age == 0:
        age = "Middle Age"
    elif age == 1:
        age = "Senior"
    elif age == 2:
        age = "Youth"
    # income
    if income == 0:
        income = "High"
    elif income == 1:
        income = "Low"
    elif income == 2:
        income = "Medium"
    # student
    if student == 0:
        student = "No"
    elif student == 1:
        student = "Yes"
    # credit_rating
    if credit_rating == 0:
        credit_rating = "Excellent"
    elif credit_rating == 1:
        credit_rating = "Fair"
    # credit_rating = "Fair" if credit_rating else "Excellent"

    # menampilkan template yang sama dengan membawa data hasil prediksi
    return render_template('index.html', predicted="Yes" if predicted else "No", age=age, income=income, student=student, credit_rating=credit_rating)


# drive
if __name__ == '__main__':
    app.run(debug=True)
