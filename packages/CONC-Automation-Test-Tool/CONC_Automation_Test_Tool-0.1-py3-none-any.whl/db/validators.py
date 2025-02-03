import logging
from sqlalchemy.exc import IntegrityError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_data(session, instance):
    """Validate data before inserting into the database."""
    try:
        session.add(instance)
        session.commit()
        logger.info(f"Data inserted successfully: {instance}")
    except IntegrityError as e:
        session.rollback()
        logger.error(f"IntegrityError: {e}")
    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting data: {e}")