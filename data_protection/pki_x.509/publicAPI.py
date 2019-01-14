from flask import request, url_for, json
from flask_api import FlaskAPI, status, exceptions
from client import generate_client
from CA import create_cert
from CLR import add_to_revoke_list
import pem
from cryptography import x509
from cryptography.hazmat.backends import default_backend

app = FlaskAPI(__name__)

@app.route("/private/genc", methods=['GET', 'POST'])
def genc():
    generate_client()

@app.route("/private/crec", methods=['GET', 'POST'])
def crec():
    create_cert()

@app.route("/private/revl", methods=['GET', 'POST'])
def revl():
    add_to_revoke_list()

@app.route("/show_certs", methods=['GET', 'POST'])
def load_certificates():
    with open("server/cert.pem", "rb") as f:
        certs = pem.parse(f.read())
    certs = [x509.load_pem_x509_certificate(cert.as_bytes(), default_backend()) for cert in certs]
    out = {cert.serial_number: str([cert.subject, cert.not_valid_after]) for cert in certs}
    return json.jsonify(out)

@app.route("/revocation_list", methods=['GET', 'POST'])
def load_revoked():
    with open("server/revoked_certs.pem", "rb") as f:
        certs = pem.parse(f.read())
    crl = x509.load_pem_x509_crl(certs[0].as_bytes(), default_backend())[0]
    print(crl.serial_number)
    out = {crl.serial_number: str(str(crl.revocation_date)+', --> '+ str([ext for ext in crl.extensions]))}
    return json.jsonify(out)

if __name__ == "__main__":
    app.run(debug=True)