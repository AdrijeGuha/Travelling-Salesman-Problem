from flask import Flask, render_template, flash, request, redirect, url_for
import RouteOptimizer
from datetime import datetime as dt

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute/', methods =["POST","GET"])
def execute():
    location = ''
    if request.method == "POST":
        location = request.form.get('city')
    location.strip().rstrip()
    with open('storage/Location_for_Show_Map.txt','w') as file:
        file.write(location)
    # RouteOptimizer.main()
    with open('storage/shortest_path_sequence.txt','r') as file:
        text = file.read()

    return render_template('execute.html', text=text) 

@app.route('/House_Route_On_Map')
def House_Route_On_Map():
    return render_template('House_Route_On_Map.html')

@app.route('/query/', methods =["POST","GET"])
def query():
    if request.method == "POST":
        now = dt.now()
        name = request.form.get('name')
        mail = request.form.get('email')
        query_text = request.form.get('query_text')
        with open('storage/query.csv', 'a') as file:
            file.write(f'\n{now.strftime("%d/%m/%y")},{now.strftime("%H:%M:%S")},{name},{mail},{query_text}')
    flash('Query has been noted! Thank you for using our service! 🙏')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)