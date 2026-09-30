from flask import Flask, render_template, request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import hashlib
import secrets
import string
import base64


# ============================================================
# APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# CONFIGURATION
# ============================================================

app.config["SECRET_KEY"] = "cle-novasec-a-changer-plus-tard"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///novasec.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# ============================================================
# INITIALISATION
# ============================================================

db = SQLAlchemy(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


# ============================================================
# MODELE UTILISATEUR
# ============================================================

class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


# ============================================================
# FLASK-LOGIN
# ============================================================

@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


# ============================================================
# PAGE D'ACCUEIL
# ============================================================

@app.route("/")
def accueil():

    return render_template(
        "index.html"
    )


# ============================================================
# INSCRIPTION
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        first_name = request.form.get(
            "first_name",
            ""
        ).strip()

        last_name = request.form.get(
            "last_name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # Vérification des champs

        if (
            not first_name
            or not last_name
            or not email
            or not password
        ):

            flash(
                "Tous les champs sont obligatoires."
            )

            return redirect(
                url_for("register")
            )

        # Vérification du mot de passe

        if len(password) < 8:

            flash(
                "Le mot de passe doit contenir au moins 8 caractères."
            )

            return redirect(
                url_for("register")
            )

        # Confirmation du mot de passe

        if password != confirm_password:

            flash(
                "Les deux mots de passe ne correspondent pas."
            )

            return redirect(
                url_for("register")
            )

        # Vérification email déjà utilisé

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Cette adresse email existe déjà."
            )

            return redirect(
                url_for("register")
            )

        # Hash du mot de passe

        password_hash = generate_password_hash(
            password
        )

        # Création utilisateur

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash
        )

        db.session.add(new_user)

        db.session.commit()

        flash(
            "Compte créé avec succès ! Vous pouvez maintenant vous connecter."
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# ============================================================
# CONNEXION
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password_hash,
            password
        ):

            login_user(user)

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Email ou mot de passe incorrect."
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "login.html"
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


# ============================================================
# SHA-256
# ============================================================

@app.route("/hash", methods=["GET", "POST"])
@login_required
def hash_tool():

    result = None

    original_text = ""

    if request.method == "POST":

        original_text = request.form.get(
            "text",
            ""
        )

        result = hashlib.sha256(
            original_text.encode("utf-8")
        ).hexdigest()

    return render_template(
        "hash.html",
        result=result,
        original_text=original_text
    )


# ============================================================
# GENERATEUR DE MOTS DE PASSE
# ============================================================

@app.route("/password-generator", methods=["GET", "POST"])
@login_required
def password_generator():

    password = None

    length = 16

    error = None

    if request.method == "POST":

        try:

            length = int(
                request.form.get(
                    "length",
                    16
                )
            )

        except ValueError:

            length = 16

        # Limite : 8 à 64 caractères

        length = max(
            8,
            min(length, 64)
        )

        use_uppercase = (
            request.form.get("uppercase") == "on"
        )

        use_lowercase = (
            request.form.get("lowercase") == "on"
        )

        use_numbers = (
            request.form.get("numbers") == "on"
        )

        use_symbols = (
            request.form.get("symbols") == "on"
        )

        characters = ""

        if use_lowercase:

            characters += string.ascii_lowercase

        if use_uppercase:

            characters += string.ascii_uppercase

        if use_numbers:

            characters += string.digits

        if use_symbols:

            characters += "!@#$%^&*()-_=+[]{}?"

        # Vérification des catégories

        if not characters:

            error = (
                "Veuillez sélectionner au moins "
                "une catégorie de caractères."
            )

        else:

            password = "".join(
                secrets.choice(characters)
                for _ in range(length)
            )

    return render_template(
        "password_generator.html",
        password=password,
        length=length,
        error=error
    )


# ============================================================
# FONCTIONS AES
# ============================================================

def derive_key(password, salt):
    """
    Transforme le mot de passe utilisateur
    en clé AES-256 grâce à PBKDF2-HMAC-SHA256.
    """

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000
    )

    return kdf.derive(
        password.encode("utf-8")
    )


def encrypt_aes(text, password):
    """
    Chiffre un texte avec AES-256-GCM.
    """

    # Sel aléatoire
    salt = secrets.token_bytes(16)

    # Nonce de 96 bits
    nonce = secrets.token_bytes(12)

    # Création de la clé AES-256
    key = derive_key(
        password,
        salt
    )

    # AES-GCM
    aes = AESGCM(key)

    # Chiffrement
    encrypted = aes.encrypt(
        nonce,
        text.encode("utf-8"),
        None
    )

    # salt + nonce + ciphertext + tag
    data = (
        salt
        + nonce
        + encrypted
    )

    # Base64
    return base64.urlsafe_b64encode(
        data
    ).decode("utf-8")


def decrypt_aes(encrypted_text, password):
    """
    Déchiffre un texte AES-256-GCM.
    """

    # Décodage Base64
    data = base64.urlsafe_b64decode(
        encrypted_text.encode("utf-8")
    )

    # Vérification minimale de la taille
    if len(data) < 28:
        raise ValueError(
            "Données AES invalides."
        )

    # Extraction du salt
    salt = data[:16]

    # Extraction du nonce
    nonce = data[16:28]

    # Extraction du ciphertext + tag
    encrypted = data[28:]

    # Reconstruction de la clé
    key = derive_key(
        password,
        salt
    )

    # AES-GCM
    aes = AESGCM(key)

    # Déchiffrement
    decrypted = aes.decrypt(
        nonce,
        encrypted,
        None
    )

    return decrypted.decode("utf-8")


# ============================================================
# CHIFFREMENT AES
# ============================================================

@app.route("/aes", methods=["GET", "POST"])
@login_required
def aes_tool():

    result = None

    error = None

    operation = None

    text = ""

    if request.method == "POST":

        operation = request.form.get(
            "operation"
        )

        text = request.form.get(
            "text",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )

        # Vérification des champs

        if not text or not password:

            error = (
                "Le texte et le mot de passe sont obligatoires."
            )

        else:

            try:

                if operation == "encrypt":

                    result = encrypt_aes(
                        text,
                        password
                    )

                elif operation == "decrypt":

                    result = decrypt_aes(
                        text,
                        password
                    )

                else:

                    error = (
                        "Opération invalide."
                    )

            except Exception:

                error = (
                    "Impossible de traiter les données. "
                    "Vérifiez le texte chiffré et le mot de passe."
                )

    return render_template(
        "aes.html",
        result=result,
        error=error,
        operation=operation,
        text=text
    )


# ============================================================
# FONCTIONS RSA
# ============================================================

def generate_rsa_keys():
    """
    Génère une paire de clés RSA 2048 bits :
    - clé publique
    - clé privée
    """

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    # Export de la clé privée au format PEM

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Export de la clé publique au format PEM

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return (
        public_pem.decode("utf-8"),
        private_pem.decode("utf-8")
    )


def load_public_key(public_key_text):
    """
    Charge une clé publique RSA depuis son format PEM.
    """

    return serialization.load_pem_public_key(
        public_key_text.encode("utf-8")
    )


def load_private_key(private_key_text):
    """
    Charge une clé privée RSA depuis son format PEM.
    """

    return serialization.load_pem_private_key(
        private_key_text.encode("utf-8"),
        password=None
    )


def encrypt_rsa(text, public_key_text):
    """
    Chiffre un texte avec une clé publique RSA.
    """

    public_key = load_public_key(
        public_key_text
    )

    encrypted = public_key.encrypt(
        text.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(
        encrypted
    ).decode("utf-8")


def decrypt_rsa(encrypted_text, private_key_text):
    """
    Déchiffre un texte avec une clé privée RSA.
    """

    private_key = load_private_key(
        private_key_text
    )

    encrypted = base64.b64decode(
        encrypted_text.encode("utf-8")
    )

    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted.decode("utf-8")


# ============================================================
# RSA
# ============================================================

@app.route("/rsa", methods=["GET", "POST"])
@login_required
def rsa_tool():

    public_key = None

    private_key = None

    result = None

    error = None

    operation = None

    text = ""

    key = ""

    if request.method == "POST":

        operation = request.form.get(
            "operation"
        )

        text = request.form.get(
            "text",
            ""
        )

        key = request.form.get(
            "key",
            ""
        )

        try:

            # ================================================
            # GENERATION DES CLES
            # ================================================

            if operation == "generate":

                public_key, private_key = (
                    generate_rsa_keys()
                )

            # ================================================
            # CHIFFREMENT
            # ================================================

            elif operation == "encrypt":

                if not text or not key:

                    error = (
                        "Le texte et la clé publique "
                        "sont obligatoires."
                    )

                else:

                    result = encrypt_rsa(
                        text,
                        key
                    )

            # ================================================
            # DECHIFFREMENT
            # ================================================

            elif operation == "decrypt":

                if not text or not key:

                    error = (
                        "Le texte chiffré et la clé privée "
                        "sont obligatoires."
                    )

                else:

                    result = decrypt_rsa(
                        text,
                        key
                    )

            else:

                error = (
                    "Opération RSA invalide."
                )

        except Exception:

            error = (
                "Impossible de traiter les données RSA. "
                "Vérifiez la clé et le contenu fourni."
            )

    return render_template(
        "rsa.html",
        public_key=public_key,
        private_key=private_key,
        result=result,
        error=error,
        operation=operation,
        text=text,
        key=key
    )


# ============================================================
# DECONNEXION
# ============================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


# ============================================================
# CREATION BASE DE DONNEES
# ============================================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(
        debug=True
    )