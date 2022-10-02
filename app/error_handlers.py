from app import app, db

from flask import render_template,request

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f'Server error {e}, route {request.url}')
    db.session.rollback()
    return render_template('500.html', title='Server error')

@app.errorhandler(404)
def server_error(e):

    return render_template('404.html', title='Page not found')