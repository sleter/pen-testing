from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
import datetime
import pem

def add_to_revoke_list():
    # wczytanie requestu usunięcia
    with open("server/cert.pem", "rb") as f:
        certs = pem.parse(f.read())

    cert = certs[0].as_bytes()
    cert = x509.load_pem_x509_certificate(cert, default_backend())

    #niezbędne parametry
    organizationName = str(cert.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME))
    serialNum = int(cert.serial_number)

    one_day = datetime.timedelta(1, 0, 0)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    #CRL - Certificate Revocation List
    builder = x509.CertificateRevocationListBuilder()
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, organizationName),
    ]))
    builder = builder.last_update(datetime.datetime.today())
    builder = builder.next_update(datetime.datetime.today() + one_day)
    revoked_cert = x509.RevokedCertificateBuilder().serial_number(
        serialNum
    ).revocation_date(
        datetime.datetime.today()
    ).build(default_backend())

    builder = builder.add_revoked_certificate(revoked_cert)

    crl = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )
    len(crl)

    with open("server/revoked_certs.pem", "wb") as f:
        f.write(crl.public_bytes(serialization.Encoding.PEM))

add_to_revoke_list()