from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
import pem
import datetime

def create_cert():
    with open("client/csr.pem", "rb") as f:
    certs = pem.parse(f.read())

    cert = certs[0].as_bytes()

    csr = x509.load_pem_x509_csr(cert, default_backend())

    # parsowanie z csr do wejścia do buildera
    countryName = csr.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)
    commonName = csr.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
    organizationName = str(csr.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME))
    extension = csr.extensions[0].value

    one_day = datetime.timedelta(1, 0, 0)
    private_key = rsa.generate_private_key( # klucz CA
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = csr.public_key()
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, organizationName),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, organizationName),
    ]))
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 30))
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(public_key)
    builder = builder.add_extension(
        extension,
        critical=False
    )
    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
    )
    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    print(isinstance(certificate, x509.Certificate))

    with open("server/cert.pem", "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))
