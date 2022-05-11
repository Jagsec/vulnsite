#This file has the common routes for a site, a home page and routes in case a user tries to access a page
#which does not exist or is not logged in to view certain parts of the site
from flask import render_template, redirect, url_for, flash
from interface import app

@app.route("/")
def homePage():
    return render_template("home.html")

def notFoundPage(error):
    flash('Page not found', category='info')
    return redirect(url_for('homePage'))

def notAuthenticatedPage(error):
    flash("You must be logged in to view this page")
    return redirect(url_for("loginPage"))