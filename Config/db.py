
# Lock permet de synchroniser l'accès à une partie du code
# lorsqu'il est exécuté par plusieurs threads.
from threading import Lock

# create_engine crée le moteur SQLAlchemy qui gère
# le pool de connexions vers la base de données.
from sqlalchemy import create_engine

# URL.create construit proprement l'URL de connexion
# sans devoir concaténer manuellement les paramètres.
from sqlalchemy.engine import URL

# sessionmaker est une fabrique qui crée des sessions SQLAlchemy.
from sqlalchemy.orm import sessionmaker

# declarative_base crée la classe de base de nos modèles ORM.
from sqlalchemy.orm import declarative_base

# On importe les paramètres chargés depuis le fichier .env.
# Exemple : settings.db_host, settings.db_name, etc.
from config import settings


class Database:
    """
    Classe responsable de la gestion de la connexion à MySQL.

    Elle applique le design pattern Singleton :
    plusieurs appels à Database() renvoient la même instance.
    """

    # Attribut de classe partagé par toutes les instances.
    # Il contiendra l'unique instance de Database.
    _instance = None

    # Verrou utilisé pour éviter que plusieurs threads
    # créent simultanément l'instance du Singleton.
    _lock = Lock()

    def __new__(cls):
        """
        Contrôle la création de l'objet.

        __new__ est appelé avant __init__.
        C'est ici que nous garantissons une instance partagée.
        """

        # Un seul thread à la fois peut entrer dans cette section.
        with cls._lock:

            # Si aucune instance n'existe encore...
            if cls._instance is None:

                # ...on crée l'objet pour la première fois.
                cls._instance = super().__new__(cls)

        # On retourne toujours la même instance.
        return cls._instance

    def __init__(self):
        """
        Initialise les attributs de l'instance.

        Attention : __init__ peut être appelé plusieurs fois,
        même si __new__ retourne toujours le même objet.
        """

        # Si l'objet a déjà été initialisé, on ne recommence pas.
        if getattr(self, "_initialized", False):
            return

        # Le moteur n'est pas encore créé.
        self.engine = None

        # La fabrique de sessions n'est pas encore créée.
        self.SessionLocal = None

        # On mémorise que l'initialisation est terminée.
        self._initialized = True

    def connect(self):
        """
        Crée le moteur SQLAlchemy et la fabrique de sessions.

        Le moteur est créé uniquement s'il n'existe pas déjà.
        """

        if self.engine is None:

            # Construction de l'URL de connexion à MySQL.
            # Les valeurs proviennent du fichier .env via settings.
            database_url = URL.create(
                drivername="mysql+pymysql",
                username=settings.db_username,
                password=settings.db_password,
                host=settings.db_host,
                port=settings.db_port,
                database=settings.db_name,
            )

            # Création du moteur SQLAlchemy.
            self.engine = create_engine(
                database_url,

                # Vérifie qu'une connexion du pool est encore valide
                # avant de l'utiliser.
                pool_pre_ping=True,

                # Renouvelle les connexions après 1800 secondes
                # pour limiter les problèmes liés aux connexions
                # anciennes ou expirées.
                pool_recycle=1800,
            )

            # Création d'une fabrique de sessions.
            # Chaque appel à SessionLocal() crée une nouvelle session.
            self.SessionLocal = sessionmaker(
                bind=self.engine,

                # Les modifications ne sont pas synchronisées
                # automatiquement à chaque opération.
                autoflush=False,

                # Les transactions doivent être validées
                # explicitement avec db.commit().
                autocommit=False,
            )

        # Retourne le moteur, qu'il vienne d'être créé
        # ou qu'il existe déjà.
        return self.engine

    def get_session(self):
        """
        Fournit une nouvelle session SQLAlchemy.
        """

        # Si la fabrique n'existe pas encore, on initialise
        # le moteur et la fabrique de sessions.
        if self.SessionLocal is None:
            self.connect()

        # Création et retour d'une session indépendante.
        return self.SessionLocal()

    def close(self):
        """
        Libère les ressources du moteur SQLAlchemy.
        """

        if self.engine is not None:

            # Libère les connexions du pool du moteur.
            self.engine.dispose()

            # Indique que le moteur n'est plus disponible.
            self.engine = None

            # La fabrique doit être recréée au prochain accès.
            self.SessionLocal = None


# Création de la classe de base utilisée par les modèles ORM.
# Les classes UserSchema et Avis peuvent hériter de Base.
Base = declarative_base()


# Création de l'instance partagée du Singleton.
# Tous les modules qui importent cette variable
# utilisent cette même instance dans ce processus Python.
database = Database()


def get_db():
    """
    Dépendance FastAPI qui fournit une session SQLAlchemy.

    Le mot-clé yield transmet la session à la route.
    Le bloc finally garantit sa fermeture après la requête,
    même si une exception survient.
    """

    # Création d'une session pour la requête courante.
    db = database.get_session()

    try:
        # Transmet la session au contrôleur ou à la route.
        yield db

    finally:
        # Ferme la session après le traitement de la requête.
        # Cela libère les ressources utilisées par la session.
        db.close()

