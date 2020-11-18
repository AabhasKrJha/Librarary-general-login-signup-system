from flask import Flask, render_template, request, session, redirect, flash
from db_access_login import connect_db

from database import create_db_model, add_user, login_reader, add_auth, send_job_applications, find_code, reset_password, check_job_availability, get_applications

from basic_operations import validate_signup, create_libID_file, check_job_application, make_list, check_reset_password_form
import send_mail
import os


app = Flask(__name__)
app.secret_key = 'gt4bvhnwd0voe9i3bnrjwvg387395jyh849u83bgw8q9wh3g485n9oehtbrg7tf'

db_name = 'users'

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
else:
    app.debug = False


@app.route('/', methods=['GET', 'POST'])
def main():

    if 'db-access' in session:
        return redirect('/login')

    else:

        if request.method == "POST":

            form = request.form
            user = form['user']
            password = form['password']

            conn = connect_db(user, password)

            if conn:
                create_db_model(db_name)
                session['db-access'] = True
                return redirect('/login')
            else:
                flash("User ID and Password don't match")

    return render_template('main.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if 'db-access' in session:

        admin_code = os.environ.get('ADMIN_CODE')

        if request.method == 'POST':
            code = request.form['admin-code']
            if code == admin_code:
                applications = get_applications(db_name)
                return render_template('admin.html', applications=applications)
            else:
                flash('Incorrect Code')

        return render_template('admin-enter-code.html')

    else:
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'db-access' in session:

        if 'user' in session:
            return redirect('/main')

        else:

            if request.method == "POST":
                form = request.form

                if 'Reader_login' in form:

                    ID = form['email/library-id']
                    password = form['password']

                    login_data = login_reader(db_name, 'reader', ID, password)

                    if login_data == True:

                        session['user'] = ID
                        return redirect('/main')

                    else:

                        if login_data == 'password':
                            flash('Incorrect Password')
                            return render_template('login.html', ID=ID, form="reader")
                        elif login_data == 'email':
                            flash('Incorrect email')
                            return render_template('login.html', ID=ID, form="reader")
                        elif login_data == 'libID':
                            flash('Incorrect Library ID')
                            return render_template('login.html', ID=ID, form="reader")

                if 'Authority_login' in form:

                    ID = form['email/library-id']
                    password = form['password']

                    login_data = login_reader(
                        db_name, 'authority', ID, password)

                    if login_data == True:

                        session['user'] = ID
                        return redirect('/main')

                    else:

                        if login_data == 'password':
                            flash('Incorrect Password')
                            return render_template('login.html', ID=ID, form="authority")
                        elif login_data == 'email':
                            flash('Incorrect email')
                            return render_template('login.html', ID=ID, form="authority")
                        elif login_data == 'libID':
                            flash('Incorrect Library ID')
                            return render_template('login.html', ID=ID, form="authority")

                if 'Author_login' in form:

                    ID = form['email/library-id']
                    password = form['password']

                    login_data = login_reader(db_name, 'author', ID, password)

                    if login_data == True:

                        session['user'] = ID
                        return redirect('/main')

                    else:

                        if login_data == 'password':
                            flash('Incorrect Password')
                            return render_template('login.html', ID=ID, form="author")
                        elif login_data == 'email':
                            flash('Incorrect email')
                            return render_template('login.html', ID=ID, form="author")
                        elif login_data == 'libID':
                            flash('Incorrect Library ID')
                            return render_template('login.html', ID=ID, form="author")

                if 'Guest_login' in form:

                    ID = form['email/library-id']
                    password = form['password']
                    session['user'] = ID
                    return redirect('/main')

        return render_template('login.html')

    else:
        return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])  # signing up readers not
def signup():

    if 'db-access' in session:

        if 'user' in session:
            return redirect('/main')

        else:

            if request.method == "POST":

                form = request.form
                name = form['name']
                email = form['email']
                phone = form['phone']
                password = form['password']
                designation = form['designation']

                signup = validate_signup(
                    name, email, phone, password)

                if signup == True:

                    try:
                        add_user(db_name, name,
                                 email, phone, designation, password)
                        session['user'] = email
                        return redirect('/main')
                    except:
                        flash('Please Login')

                else:

                    if signup == 'name':
                        flash('Please enter your name')
                        return render_template('signup.html', email=email, phone=phone)
                    elif signup == 'email':
                        flash('Please enter a valid email')
                        return render_template('signup.html', name=name, phone=phone)
                    elif signup == 'phone':
                        flash('Please provide a valid phone number')
                        return render_template('signup.html', name=name, email=email)
                    elif signup == 'password':
                        flash('Please provide a valid password')
                        return render_template('signup.html', name=name, email=email, phone=phone)

        return render_template('signup.html')

    else:
        return redirect('/')


@app.route('/signup-authority', methods=["GET", "POST"])
def auth_signup():

    if 'db-access' in session:

        if request.method == 'POST':

            form = request.form

            if 'signup-code' in form:
                email = form['email']
                code = form['code']
                if find_code(db_name, email, code):
                    return render_template('signup-authority.html', form='show')

            elif 'signup-auth' in form:

                name = form['name']
                email = form['email']
                phone = form['phone']
                password = form['password']

                signup = validate_signup(
                    name, email, phone, password)

                if signup == True:

                    try:
                        add_auth(db_name, name, email, phone, password)
                        session['user'] = email
                        return redirect('/main')
                    except:
                        flash('Please Login')

                else:

                    if signup == 'name':
                        flash('Please enter your name')
                        return render_template('signup.html', email=email, phone=phone)
                    elif signup == 'email':
                        flash('Please enter a valid email')
                        return render_template('signup.html', name=name, phone=phone)
                    elif signup == 'phone':
                        flash('Please provide a valid phone number')
                        return render_template('signup.html', name=name, email=email)
                    elif signup == 'password':
                        flash('Please provide a valid password')
                        return render_template('signup.html', name=name, email=email, phone=phone)

        return render_template('signup-authority.html')

    return redirect('/')


@app.route('/jobs', methods=["GET", "POST"])
def jobs():
    if 'db-access' in session:

        if request.method == "POST":

            if 'headLib' in request.form:

                availibility = check_job_availability(db_name, 'head')

                if availibility:

                    form = request.form
                    name = form['name']
                    email = form['email']
                    phone = form['phone']
                    designation = 'head'

                    if check_job_application(email, phone):
                        try:
                            send_job_applications(
                                db_name, name, email, phone, designation)
                            flash('Application Sent')
                            return redirect('/jobs')
                        except:
                            flash('Application Sent')
                            return redirect('/jobs')

                else:
                    flash('No jobs available')

            elif 'assistLib' in request.form:

                availibility = check_job_availability(db_name, 'assist')

                if availibility:

                    form = request.form
                    name = form['name']
                    email = form['email']
                    phone = form['phone']
                    designation = 'assistant'

                    if check_job_application(email, phone):
                        try:
                            send_job_applications(
                                db_name, name, email, phone, designation)
                            flash('Application Sent')
                            return redirect('/jobs')
                        except:
                            flash('Application Sent')
                            return redirect('/jobs')

                else:
                    flash('No jobs available')

        return render_template('jobs.html')

    else:
        return redirect('/')


@app.route('/job-conf', methods=['POST', 'GET'])
def confirm_job():
    if request.method == 'POST':
        email = request.form['email']
        try:
            send_mail.send(email)
            return email
        except:
            return redirect('/admin')


@app.route('/reset-pass', methods=["GET", "POST"])
def reset_pass():
    if 'db-access' in session:

        if request.method == "POST":
            form = request.form
            email = form['email']
            password = form['passowrd']
            conf_password = form['confirm-password']
            designation = form['designation']

            if check_reset_password_form(email, password, conf_password):
                reset_password(db_name, email, password, designation)

        return render_template('reset-pass.html')
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        return redirect('/login')
    else:
        return redirect('/login')


@app.route('/logout-db')
def logout_db():

    if 'db-access' in session:
        session.pop('db-access')
        return redirect('/')
    else:
        return redirect('/')


@app.route('/main')
def mns():

    if 'user' in session:
        if session['user'] == 'guest':
            return 'Hello Guest'
        else:
            return f'Hello {session["user"]}'
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(port=5000)
