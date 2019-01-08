from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from client import generate_client
from CA import create_cert
from CLR import add_to_revoke_list

app = FlaskAPI(__name__)

@app.route("/genc", methods=['GET', 'POST'])
def genc():
    generate_client()

@app.route("/crec", methods=['GET', 'POST'])
def crec():
    create_cert()

@app.route("/revl", methods=['GET', 'POST'])
def revl():
    add_to_revoke_list()

if __name__ == "__main__":
    app.run(debug=True)