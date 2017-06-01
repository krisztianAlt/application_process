from flask import Flask, render_template, request, redirect, url_for
import data_manager


app = Flask(__name__)


# Menu
@app.route('/', methods=['POST', 'GET'])
def menu():
    return render_template("menu.html")


# Mentors and schools page
@app.route('/mentors', methods=['POST', 'GET'])
def mentors():
    table = data_manager.mentors_and_schools()
    column_names = ['Mentor\'s First Name', 'Mentor\'s Last Name', 'School\'s Name', 'School\'s Country']
    return render_template("table.html", table=table, column_names=column_names)


# All school page
@app.route('/all-school', methods=['POST', 'GET'])
def all_school():
    table = data_manager.all_school()
    column_names = ['Mentor\'s First Name', 'Mentor\'s Last Name', 'School\'s Name', 'School\'s Country']
    return render_template("table.html", table=table, column_names=column_names)


# Mentors per country
@app.route('/mentors-by-country', methods=['POST', 'GET'])
def mentors_by_country():
    table = data_manager.mentors_by_country()
    column_names = ['Country', 'Count']
    return render_template("table.html", table=table, column_names=column_names)


# Contacts page
@app.route('/contacts', methods=['POST', 'GET'])
def contacts():
    table = data_manager.contacts()
    column_names = ['School\'s Name', 'Mentor\'s First Name', 'Mentor\'s Last Name']
    return render_template("table.html", table=table, column_names=column_names)



if __name__ == '__main__':
    app.run(debug=True)
