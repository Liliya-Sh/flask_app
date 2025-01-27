import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID

from ..extensions import db


class Wallet(db.Model):
    """Свойства кошелька"""
    __tablename__ = 'wallets'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = db.Column(db.Integer,  nullable=False)
    added = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f"Wallet(balance:{self.balance!r})"
