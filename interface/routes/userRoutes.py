#This file has the routes related to the user, like log in, register and profile
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from interface import app, db
from interface.models.userModel import Users
from interface.models.challengeModel import Challenges, User_cleared_challenges
from interface.forms.userForms import LoginForm, RegisterForm, EditForm
from interface.controllers.fileController import editUpload, removeFile

#This route renders the log in form and logs in the user if the correct credentials are provided
@app.route("/login", methods=["GET", "POST"])
def loginPage():
    login_form = LoginForm()
    #The user existence in the database is checked and then if the password provided matches
    if login_form.validate_on_submit():
        attempted_user = Users.query.filter_by(username=login_form.username.data).first()
        if attempted_user: 
            if attempted_user.check_password(attempted_password=login_form.password.data):
                login_user(attempted_user)
                flash("Log in succesful", category="success")
                return redirect(url_for("challengePage"))
            else:
                flash("Incorrect password", category="danger")
        else:
            flash("User not found", category="danger")
    return render_template("user/login.html", form=login_form)

#This route logs out the user
@app.route("/logout")
def logoutPage():
    logout_user()
    flash('Logged out', category='info')
    return redirect(url_for('homePage'))

#This route renders the register form and logs the user in after creating the account
@app.route("/register", methods=["GET", "POST"])
def registerPage():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        #We check the password provided matches with the confirmation field, then create the user
        if register_form.password.data == register_form.password_confirm.data:
            #We create the user based on the model and insert it to the database
            userToCreate = Users(username = register_form.username.data,
                                unhashed_password = register_form.password.data,
                                profile_desc='Insert your description here',
                                score=0)
            db.session.add(userToCreate)
            db.session.commit()
            login_user(userToCreate)
            flash('Account created', category='success')
            return redirect(url_for('homePage'))
        else:
            flash("The passwords do not match", category="danger")
    if register_form.errors != {}:
        for errorMsg in register_form.errors.values():
            flash(f'An error ocurred while registering the user {errorMsg}', category='danger')
    return render_template("user/register.html", form=register_form)

#This route renders the user profile, showing a profile picture, description, cleared challenges
# and ranking on the site
@app.route("/user/<username>")
@login_required
def profilePage(username):
    #We look for the user in the database
    user_profile = Users.query.filter_by(username=username).first()
    #If the user exist we look for the challenges cleared to render them in the page as well as all the
    #scores to show the top 5 as well as the user's position among the ranking
    if user_profile:
        challenge_info = []
        cleared_challenges = User_cleared_challenges.query.filter_by(user_id=user_profile.id).all()
        for challenge in cleared_challenges:
            challenge_info.append(Challenges.query.filter_by(id=challenge.challenge_id).first())
        user_scores = Users.query.order_by(Users.score.desc()).all()
        return render_template("user/profile.html", user=user_profile, 
                                challenges= challenge_info, user_scores=user_scores)
    else:
        flash('This user does not exist', category='danger')
        return redirect(url_for('challengePage'))

#This route renders the form for editing the user info, like the profile picture and description
@app.route("/user/<username>/edit", methods=['GET', 'POST'])
@login_required
def editProfilePage(username):
    #We query the user entry and check if the current user corresponds to the user page being viewed
    #if so the user can edit the user info, otherwise it is not allowed
    user_profile = Users.query.filter_by(username=username).first()
    if user_profile:
        if current_user.id == user_profile.id:
            edit_form = EditForm()
            if edit_form.validate_on_submit():
                #We check for a change in the profile picture since it's optional, if there is we
                #erase the current one and add the new one
                if edit_form.profile_pic.data:
                    file_path = 'images/profile/'
                    user_profile.profile_pic = editUpload(edit_form.profile_pic, 
                                                        user_profile.profile_pic, 
                                                        file_path)
                #The current picture can be deleted and a default one will be shown instead
                if edit_form.delete_pic.data:
                    user_profile.profile_pic = removeFile(user_profile.profile_pic)
                user_profile.profile_desc = edit_form.profile_desc.data
                db.session.commit()
                flash('Profile edited', category='success')
                return redirect(url_for('profilePage', username=username))
            if edit_form.errors != {}:
                    for errorMsg in edit_form.errors.values():
                        flash(f'An error ocurred while editing this profile {errorMsg}', category='danger')
            edit_form.profile_desc.data = user_profile.profile_desc
            return render_template("user/editProfile.html", form=edit_form)
        else:
            flash('This user cannot edit this profile', category='danger')
            return redirect(url_for('profilePage', username=username))
    else:
        flash('This user does not exist', category='danger')
        return redirect(url_for('profilePage', username=username))