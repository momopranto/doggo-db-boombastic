from flask import current_app as app, render_template, render_template_string, request, redirect, abort, jsonify, \
    json as json_mod, url_for, session, Blueprint, Response

from jinja2.exceptions import TemplateNotFound
from passlib.hash import bcrypt_sha256
from collections import OrderedDict

views = Blueprint('views',__name__)

@views.route("/", defaults={'template' : 'index'})
@views.route("/<template>")
def static_html(template):
	try:
		return render_template(template + '.html')
	except TemplateNotFound:
		abort(404)
