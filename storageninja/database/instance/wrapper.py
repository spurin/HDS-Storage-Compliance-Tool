# ------------------------------------------------------------------------------
# Builtin Imports
# ------------------------------------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# ------------------------------------------------------------------------------
# Internal Imports
# ------------------------------------------------------------------------------
from storageninja.database.schema.shared_base import Base

# ------------------------------------------------------------------------------
# Database Class
# ------------------------------------------------------------------------------
class Database():

    # ------------------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------------------
    def __init__(self, dbname='sqlite:///test.db', Base=Base):

        # ------------------------------------------------------------------------------
        # Initialise the object engine using the dbname
        # ------------------------------------------------------------------------------
        self.engine = create_engine(dbname, echo=False)

        # ------------------------------------------------------------------------------
        # Store the shared base internally
        # ------------------------------------------------------------------------------
        self.base = Base

        # ------------------------------------------------------------------------------
        # Create a scoped session
        # ------------------------------------------------------------------------------
        self.DBSession = scoped_session(sessionmaker())

        # ------------------------------------------------------------------------------
        # Configure session
        # ------------------------------------------------------------------------------
        self.DBSession.configure(bind=self.engine, autoflush=False, expire_on_commit=False)

    # ------------------------------------------------------------------------------
    # Create tables
    # ------------------------------------------------------------------------------
    def create_tables(self):
        self.base.metadata.create_all(self.engine)

    # ------------------------------------------------------------------------------
    # Drop tables
    # ------------------------------------------------------------------------------
    def drop_tables(self):
        self.base.metadata.drop_all(self.engine)

    # ------------------------------------------------------------------------------
    # Insert dictionary
    # ------------------------------------------------------------------------------
    def insert_dict(self, schema, data):
        for dataset in data.keys():

            # ------------------------------------------------------------------------------
            # Capture the corresponding class, i.e. HDS_CS_PATH from a string
            # example taken from http://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
            # ------------------------------------------------------------------------------
            db_class = getattr(schema, dataset.upper())

            try:
                self.engine.execute(
                    db_class.__table__.insert(),
                    data[dataset]
                )
            except Exception as e:
                print("DEBUG error - %s" % e)
                raise SystemExit
            self.DBSession.commit()