import uuid
from datetime import datetime

from db import db
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.mutable import MutableList



class OrderModel(db.Model):
    """
    RDS Postgres table for orders
    """

    __tablename__ = "orders"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = db.Column(db.Text(), nullable=False, index=True)
    items = db.Column(MutableList.as_mutable(db.PickleType), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="Created")
    createdAt = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    
    # # Constraints of status field
    __table_args__ = (CheckConstraint(status.in_(["Created",
                                                  "Shipped",
                                                  "Delivered",
                                                  "Cancelled"])),)

    def json(self):
        return {
            "id": str(self.id),
            "userId": self.userId,
            "items": self.items,  # array of {productId, quantity}
            "status": self.status,
            "createdAt": self.createdAt.isoformat(),
        }
        
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    