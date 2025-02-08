from sqlmodel import Session, SQLModel, create_engine

class DB:    
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)
    session: Session = None

    @staticmethod
    def create_db_and_tables():
        # This logic can be replaced with your migration handler
        SQLModel.metadata.create_all(DB.engine)

    @staticmethod
    def get_session():
        # Returns the existing DB session or create a new one.

        if DB.session:
            return DB.session
        
        with Session(DB.engine) as session:
            return session

    @staticmethod 
    def init():
        DB.create_db_and_tables()
        DB.session = DB.get_session()
