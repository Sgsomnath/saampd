# app/core/database/base.py

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# সব models নিচে import করুন, যাতে circular import এড়ানো যায়
from app.core.models import (
    admin,
    distributor,
    investor,
    commission,
)
