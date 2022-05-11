#This file has all the routes related to the challenges
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from interface import app, db
from interface.models.userModel import Users
from interface.models.challengeModel import Challenges, User_cleared_challenges
from interface.forms.challengeForms import FilterForm, FlagForm, ChallengeForm, EditForm
from interface.controllers.fileController import editUpload, fileUpload, removeFile

#This route shows all the challenges available
@app.route("/challenges", methods=['GET', 'POST'])
@login_required
def challengePage():
    #The filter form is used to filter the challenges by category
    filter_form = FilterForm()
    challenges = Challenges.query.order_by(Challenges.score).all()
    if filter_form.validate_on_submit():
        if filter_form.category.data != "all":
            challenges = Challenges.query.filter_by(category=filter_form.category.data).order_by(Challenges.score).all()    
    #This query and for loop are used to determine which challenges have been cleared by the user
    #we pass this on to the template to add a class which colors cleared challenges with green
    user_cleared_challenges = User_cleared_challenges.query.all()
    cleared_challenges = []
    for cleared_challenge in user_cleared_challenges:
        if current_user.id == cleared_challenge.user_id:
            cleared_challenges.append(cleared_challenge.challenge_id)
    return render_template("challenges/index.html", challenges=challenges, 
                            cleared_challenges=cleared_challenges, form=filter_form)

#This route renders the form for creating a new challenge and when receiving a post request, creates it
@app.route("/challenges/new", methods=['GET', 'POST'])
@login_required
def newChallengePage():
    #To protect this route we check is the current user has admin privileges
    if current_user.is_admin:
        challenge_form = ChallengeForm()
        if challenge_form.validate_on_submit():
            #Since the file field is optional we check if it has any data, if so, we call the fileUpload function
            if challenge_form.file.data:
                file_path = 'files/'
                db_dir = fileUpload(challenge_form.file, file_path)
            else: 
            #If it's empty we set the value to None
                db_dir = None
            challengeToCreate = Challenges(name=challenge_form.name.data,
                                            category=challenge_form.category.data,
                                            description=challenge_form.description.data,
                                            score=challenge_form.score.data,
                                            author=current_user.username,
                                            flag=challenge_form.flag.data,
                                            file_url=db_dir)
            db.session.add(challengeToCreate)
            db.session.commit()
            flash("Challenge created", category='success')
            return redirect(url_for('challengePage'))
        if challenge_form.errors != {}:
            for errorMsg in challenge_form.errors.values():
                flash(f'An error occured while creating the challenge {errorMsg}', category='danger')
        return render_template("challenges/new.html", form=challenge_form)
    flash('This user does not have admin privileges', category='danger')
    return redirect(url_for('challengePage'))

#This route shows the details for each challenge and allows the user to submit the flag
@app.route("/challenges/<id>", methods=['GET', 'POST'])
@login_required
def detailPage(id):
    flag_form = FlagForm()
    challenge = Challenges.query.filter_by(id=id).first()
    if flag_form.validate_on_submit():
        #We check if the submitted flag is equal to the one stored in the database, if so, we add a new entry
        #to the users cleared challenges table and add the score to the current user score
        if challenge.flag == flag_form.flag.data:
            cleared_challenge = User_cleared_challenges(user_id=current_user.id,
                                                        challenge_id=challenge.id)
            current_user.score += challenge.score
            db.session.add(cleared_challenge)
            db.session.commit()
            flash("Correct flag!", category='success')
            return redirect(url_for("challengePage"))
        else:
            flash("Incorrect flag", category='danger')
            return render_template("challenges/detail.html", challenge=challenge, form=flag_form)
    #We check is the challenge id is in the database, if not we flash a message saying this route doesn't
    #exist, otherwise, we check if the user has already cleared the challenge to display the flag form or not
    if challenge != None:
        isCleared = False
        cleared_challenges = User_cleared_challenges.query.filter_by(user_id=current_user.id).all()
        for cleared_challenge in cleared_challenges:
            if challenge.id == cleared_challenge.challenge_id:
                isCleared = True
        return render_template("challenges/detail.html", challenge=challenge, 
                                isCleared=isCleared, form=flag_form)
    else: 
        flash(f"The site /challenges/{id} does not exist", category="info")
        return redirect(url_for("challengePage"))

#This route renders the form for editing an existing challenges and edit the database entry
@app.route("/challenges/<id>/edit", methods=['GET', 'POST'])
@login_required
def editPage(id):
    #We only want admin users to be able to edit challenges, so we check that first
    if current_user.is_admin:
        challenge = Challenges.query.filter_by(id=id).first()
        edit_form = EditForm()
        if edit_form.validate_on_submit():
            #We change the current challenge data to the one submitted in the form and commit it to the database
            if edit_form.file.data:
                file_path = 'files/'
                challenge.file_url = editUpload(edit_form.file, challenge.file_url, file_path)
            else:
                if edit_form.delete_file.data:
                    challenge.file_url = removeFile(challenge.file_url) 

            challenge.name = edit_form.name.data
            challenge.category = edit_form.category.data
            challenge.description = edit_form.description.data
            challenge.score = edit_form.score.data
            challenge.flag = edit_form.flag.data
            db.session.commit()
            flash('Challenge edited', category='success')
            return redirect(url_for('detailPage', id=challenge.id))

        if edit_form.errors != {}:
            for errorMsg in edit_form.errors.values():
                flash(f'An error ocurred while editing the challenge {errorMsg}', category='danger')
        #The current challenge id is checked to determine if the form is rendered or not
        if challenge != None:
            #The form fields are populated with the current data for the challenge
            edit_form.name.data = challenge.name
            edit_form.category.data = challenge.category
            edit_form.description.data = challenge.description
            edit_form.score.data = challenge.score
            edit_form.flag.data = challenge.flag
            return render_template("challenges/edit.html", challenge=challenge, form=edit_form)
        else:
            flash('This challenge does not exist', category='info')
            return redirect(url_for('challengePage'))
    flash('This user does not have admin privileges', category='danger')
    return redirect(url_for('detailPage', id=id))

#This route is used to delete existing challenges with it's attached file if it exists, it only
# accepts post requests since it doesn't render any template 
@app.route("/challenges/<id>/delete", methods=['POST'])
@login_required
def deletePage(id):
    #We protect this route so only admin users can delete the challenges
    if current_user.is_admin:
        challengeToDelete = Challenges.query.filter_by(id=id).first()
        if challengeToDelete:
            #The attached file is deleted in case it exists
            if challengeToDelete.file_url:
                challengeToDelete.file_url = removeFile(challengeToDelete.file_url)
            #We get the cleared challenges entry and delete them, also reduce the points from the users
            #who had cleared them
            cleared_entries = User_cleared_challenges.query.filter_by(challenge_id=id).all()
            for entry in cleared_entries:
                user = Users.query.filter_by(id=entry.user_id).first()
                user.score -= challengeToDelete.score
                db.session.delete(entry)
                
            db.session.delete(challengeToDelete)
            db.session.commit()
            flash("Challenge deleted", category='success')
            return redirect(url_for('challengePage'))
    flash('This user does not have admin privileges', category='danger')
    return redirect(url_for('challengePage'))