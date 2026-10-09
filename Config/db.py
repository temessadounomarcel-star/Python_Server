from threading import Lock

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base



from config import settings


class Database:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        # Créer une seule instance, même si plusieurs
        # appels arrivent simultanément.
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        # Ne pas réinitialiser la connexion à chaque appel.
        if getattr(self, "_initialized", False):
            return

        self.engine = None
        self.SessionLocal = None
        self._initialized = True

    def connect(self):
        # Créer le moteur une seule fois.
        if self.engine is None:
            database_url = URL.create(
                drivername="mysql+pymysql",
                username=settings.db_username,
                password=settings.db_password,
                host=settings.db_host,
                port=settings.db_port,
                database=settings.db_name,
            )

            self.engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=1800,
            )

            self.SessionLocal = sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
            )

        return self.engine

    def get_session(self):
        if self.SessionLocal is None:
            self.connect()

        return self.SessionLocal()

    def close(self):
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
            self.SessionLocal = None

def get_db():
    db = database.get_session()
    try:
        yield db
    finally:
        db.close()

#l'utilisation de declarative_base() pour créer une classe de base pour les modèles SQLAlchemy
Base = declarative_base()

# Instance partagée dans l'application
database = Database()