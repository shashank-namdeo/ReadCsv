from flask import Flask, flash, request, redirect, render_template

import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Something went wrong!!!!!"
        file = request.files['file']
        df = pd.read_csv(file)

        col_type = (df.dtypes).to_dict()
        columns_names = [c for c in df.columns if "unnamed" not in c.lower()]

        conn = sqlite3.connect('APTUDE_TEST.db')
        c = conn.cursor()

        table_str = ''
        for col in columns_names:
            table_str = table_str +" "+col
            if col_type[col] == 'float64':
                table_str = table_str +" real,"
            elif col_type[col] == 'int64':
                table_str = table_str +" real,"
            elif col_type[col] == 'object':
                table_str = table_str +" text,"
        table_str = table_str.rstrip(',')

        # Create table
        c.execute('CREATE TABLE if not exists stocks ('+table_str+')')

        for i ,r in df.iterrows():
            insert_str='('
            for col in columns_names:
                insert_str=insert_str+"'"+str(r[col])+"',"
            insert_str = insert_str.rstrip(',')
            if insert_str !='':    
               try:
                   c.execute("INSERT INTO stocks VALUES "+insert_str+")")
               except Exception as e:
                   print(e)
                   pass
        conn.commit()

    return "Scuccessfully Done !!!!!"

@app.route('/show', methods=['POST','GET'])
def show_form():
    # Create your connection.
    cnn = sqlite3.connect('APTUDE_TEST.db')

    df = pd.read_sql_query("SELECT * FROM stocks", cnn)

    return render_template("show.html",  data=df.to_html())


if __name__ == "__main__":
    app.run()