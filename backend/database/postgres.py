from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from config.config import Config
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class PostgreSQLDatabase:
    def __init__(self):
        self.engine = None
        self.Session = None
        self._initialize()
        
    def _initialize(self):
        """Initialize database connection"""
        try:
            self.engine = create_engine(
                Config.DATABASE_URL,
                pool_size=10,
                pool_recycle=3600,
                pool_pre_ping=True
            )
            self.Session = scoped_session(sessionmaker(bind=self.engine))
            logger.info("PostgreSQL connection established")
        except Exception as e:
            logger.error(f"PostgreSQL initialization error: {e}")
            raise
    
    def get_session(self):
        """Get a database session"""
        if not self.Session:
            self._initialize()
        return self.Session()
    
    def create_tables(self):
        """Create all tables"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Tables created successfully")
        except Exception as e:
            logger.error(f"Table creation error: {e}")
            raise
    
    def close_session(self, session):
        """Close a database session"""
        if session:
            session.close()
    
    def execute_query(self, query, params=None):
        """Execute a raw SQL query"""
        session = self.get_session()
        try:
            if params:
                result = session.execute(query, params)
            else:
                result = session.execute(query)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            logger.error(f"Query execution error: {e}")
            raise
        finally:
            self.close_session(session)
    
    def health_check(self):
        """Check database health"""
        try:
            session = self.get_session()
            session.execute("SELECT 1")
            self.close_session(session)
            return {'status': 'healthy', 'message': 'Database connection successful'}
        except Exception as e:
            return {'status': 'unhealthy', 'message': str(e)}