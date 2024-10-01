from flask import Blueprint, render_template, flash,redirect
from .forms import SignUpForm, LogInForm
from .models import Customer,Admin
from . import db
from flask_login import login_user, login_required, logout_user,current_user

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sing_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            # take an instane of mt database Customer
            new_user = Customer()
            new_user.email = email
            new_user.username = username
            new_user.password = password1
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Account Created Successfully, You can now Login')
                return redirect('/login')
            except Exception as e:
                print(f"problems to create an accont{e}")
                flash('Account Not Created!!, Email already exists')

        else:
            flash("passowrd1 Not Equal to password2" , category='success')

    return render_template('sign-up.html', form=form,type='Buy',user='login')



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form =LogInForm()
    email = form.email.data
    password = form.password.data
    user_check = Customer.query.filter_by(email=email).first()
    if user_check:
        # check the password
        if user_check.verify_password(password):
            login_user(user_check)
            print(f'user_id{current_user.id}')
            flash("You loged in Successfully")
            return redirect('/')


    return render_template('login.html', form=LogInForm(),user='sign-up')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')




@auth.route('/sign-up-admin',methods=['GET', 'POST'])
def sign_up_admin():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            # take an instane of mt database Customer
            new_user = Admin()
            new_user.email = email
            new_user.username = username
            new_user.password = password1
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Account Created Successfully, You can now Login')
                return redirect('/login-admin')
            except Exception as e:
                print(f"problems to create an accont{e}")
                flash('Account Not Created!!, Email already exists')

        else:
            flash("passowrd1 Not Equal to password2" , category='success')

    return render_template('sign-up.html',form=form,type="Sell",user='login-admin')




@auth.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    form =LogInForm()
    email = form.email.data
    password = form.password.data
    user_check = Admin.query.filter_by(email=email).first()
    if user_check:
        # check the password
        if user_check.verify_password(password):
            login_user(user_check)
            flash("You loged in Successfully")
            return redirect('/add-items')


    return render_template('login.html', form=LogInForm(),user='sign-up-admin')
