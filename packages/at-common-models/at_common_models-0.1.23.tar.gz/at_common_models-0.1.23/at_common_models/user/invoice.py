from sqlalchemy import Index, Column, String, DateTime, Numeric, Enum as SQLEnum
from at_common_models.base import BaseModel
from sqlalchemy.sql import func
from enum import Enum

class PaymentStatus(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    PENDING = "pending"
    REFUNDED = "refunded"

class UserInvoice(BaseModel):
    __tablename__ = "user_invoices"

    stripe_invoice_id = Column(String(255), primary_key=True, default='')
    stripe_subscription_id = Column(String(255), nullable=False)
    user_id = Column(String(36), nullable=False)

    # Amount details
    amount_due = Column(Numeric(10, 3), nullable=False)
    amount_paid = Column(Numeric(10, 3), nullable=False)
    amount_remaining = Column(Numeric(10, 3), nullable=False)
    currency = Column(String(3), nullable=False, default='usd')

    # Status
    status = Column(SQLEnum(PaymentStatus), nullable=False)
    payment_intent_id = Column(String(255), nullable=True)

    # Dates
    invoice_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Metadata and timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_invoice_user_date', user_id, invoice_date),
        Index('idx_invoice_user_status', user_id, status),
    )

    def __repr__(self):
        return f"<UserInvoice(stripe_invoice_id={self.stripe_invoice_id}, amount_due={self.amount_due})>"
    
    def __str__(self) -> str:
        return f"<UserInvoice(stripe_invoice_id={self.stripe_invoice_id}, amount_due={self.amount_due})>"