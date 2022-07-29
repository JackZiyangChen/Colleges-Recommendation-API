from flask import Blueprint, render_template, redirect, request, url_for


adminviews = Blueprint('adminviews',__name__)

@adminviews.route('/')
def test():
    return render_template('rec-system-test-page.html')
