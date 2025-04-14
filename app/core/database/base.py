# app/core/database/base.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Note: Removed the model imports here to prevent circular imports
# Models will be imported separately during initialization