from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sujal123@",  # Enter your MySQL password
        database="lab_db"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db_connection()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['student_name']
        prn = request.form['student_prn']
        item_id = request.form['item_id']
        date = request.form['borrow_date']

        query = "INSERT INTO Borrow_Records (student_name, student_prn, item_id, borrow_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, prn, item_id, date))
        db.commit()
        cursor.close()
        db.close()
        return "<h3>Component Issued Successfully!</h3><a href='/'>Issue Another</a> | <a href='/admin'>View Lab Records</a>"

    cursor.execute("SELECT * FROM Equipment")
    equipment = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('index.html', equipment=equipment)

@app.route('/admin')
def admin():
    db = get_db_connection()
    cursor = db.cursor()

    # The core DBMS JOIN query linking students to the equipment they borrowed
    sql_join_query = '''
        SELECT 
            Borrow_Records.record_id, 
            Borrow_Records.student_name, 
            Borrow_Records.student_prn, 
            Equipment.item_name, 
            Borrow_Records.borrow_date
        FROM Borrow_Records
        JOIN Equipment ON Borrow_Records.item_id = Equipment.item_id
        ORDER BY Borrow_Records.borrow_date DESC
    '''
    cursor.execute(sql_join_query)
    records = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('admin.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)