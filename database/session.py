from sqlmodel import create_engine, Session, SQLModel

# Base de datos SQLite local para desarrollo
sqlite_file_name = "jaguar.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Configuramos el motor de base de datos
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Crea las tablas en la base de datos si no existen."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Generador de sesiones para inyección de dependencias o contexto."""
    with Session(engine) as session:
        yield session
