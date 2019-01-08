from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_client():
    # generowanie własnego klucza
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # zapisanie klucza na dysku
    with open("client/key.pem", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
        ))

    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes

    # generowanie CSR(Certificate Signing Request)

    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"PL"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"WP"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Poznan"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"ebookisomfajne"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"stronka.pl"),
    ])).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(u"ebookisomfajne.pl"),
            x509.DNSName(u"www.ebookisomfajne.pl"),
            x509.DNSName(u"ebookisomfajne"),
        ]),
        critical=False,
    # podpisanie CSR swoim prywatnym kluczem
    ).sign(key, hashes.SHA256(), default_backend())
    # zapisanie CSR na dysk
    with open("client/csr.pem", "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))
    # po tym CSR przekazywany jest do weryfikacji


