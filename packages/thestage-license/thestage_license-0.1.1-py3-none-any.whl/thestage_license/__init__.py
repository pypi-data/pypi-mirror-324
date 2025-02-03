import json
import os
import socket
import requests

from hashlib import sha256
from OpenSSL import SSL
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

TRUSTED_ROOT_HASHES = {
    "fbe3018031f9586bcbf41727e417b7d1c45c2f47f93be372a17b96b50757d5a2",
    "7f4296fc5b6a4e3b35d3c369623e364ab1af381d8fa7121533c9d6c633ea2461",
    "36abc32656acfc645c61b71613c4bf21c787f5cabbee48348d58597803d7abc9",
    "f7ecded5c66047d28ed6466b543c40e0743abe81d109254dcf845d4c2c7853c5",
    "2b071c59a0a0ae76b0eadb2bad23bad4580b69c3601b630c2eaf0613afa83f92",
}

def validate_root_ca() -> bool:
    try:
        host = "backend.thestage.ai"
        port = 443
        context = SSL.Context(SSL.TLS_CLIENT_METHOD)
        context.set_verify(SSL.VERIFY_NONE, lambda conn, cert, errnum, depth, ok: ok)

        sock = socket.create_connection((host, port))
        ssl_sock = SSL.Connection(context, sock)
        ssl_sock.set_connect_state()
        ssl_sock.set_tlsext_host_name(host.encode())

        ssl_sock.do_handshake()
        cert_chain = ssl_sock.get_peer_cert_chain()

        if not cert_chain:
            return False

        chain = [x509.load_der_x509_certificate(cert.to_cryptography().public_bytes(Encoding.DER)) for cert in cert_chain]

        for cert in chain:
            spki_hash = sha256(
                cert.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
            ).hexdigest()

            if spki_hash in TRUSTED_ROOT_HASHES:
                return True

        return False

    except Exception:
        return False


def validate_token() -> bool:
    config_path = os.path.expanduser("~/.thestage/config.json")
    api_url = "https://backend.thestage.ai"
    api_token = None

    if os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                main_cfg = json.load(f).get("main", {})
                api_token = main_cfg.get("thestage_auth_token")
        except (OSError, json.JSONDecodeError):
            pass

    if not api_token:
        api_token = os.getenv("THESTAGE_AUTH_TOKEN") or os.getenv("THESTAGE_DAEMON_TOKEN")

    if not api_token:
        return False

    is_daemon_token = api_token == os.getenv("THESTAGE_DAEMON_TOKEN")

    if is_daemon_token:
        endpoint = f"{api_url}/daemon-api/v1/validate-token"
        payload = {"daemonApiToken": api_token}
    else:
        endpoint = f"{api_url}/user-api/v1/validate-token"
        payload = {"userApiToken": api_token}

    try:
        resp = requests.post(endpoint, json=payload, timeout=10)
        resp.raise_for_status()
        return bool(resp.json().get("isSuccess", False))
    except (requests.RequestException, ValueError):
        return False



def init_check():
    if not validate_root_ca():
        raise ImportError("Pinned Amazon Root CA not present in chain.")

    if not validate_token():
        raise ImportError("Invalid or missing API token!")