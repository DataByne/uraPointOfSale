from flask import render_template, Blueprint

app = Blueprint('errors', __name__)

@app.app_errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
