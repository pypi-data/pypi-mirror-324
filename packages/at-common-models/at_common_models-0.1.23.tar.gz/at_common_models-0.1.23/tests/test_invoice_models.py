from datetime import datetime
from decimal import Decimal
from at_common_models.user.invoice import UserInvoice, PaymentStatus

def test_user_invoice_model(session):
    # Create test data
    invoice = UserInvoice(
        stripe_invoice_id="in_123",
        stripe_subscription_id="sub_123",
        user_id="user_123",
        amount_due=Decimal("99.990"),
        amount_paid=Decimal("99.990"),
        amount_remaining=Decimal("0.000"),
        currency="usd",
        status=PaymentStatus.SUCCEEDED,
        payment_intent_id="pi_123",
        invoice_date=datetime.now(),
        due_date=datetime.now(),
        paid_at=datetime.now()
    )
    
    session.add(invoice)
    session.commit()
    
    result = session.query(UserInvoice).filter_by(stripe_invoice_id="in_123").first()
    assert result.stripe_invoice_id == "in_123"
    assert result.stripe_subscription_id == "sub_123"
    assert result.user_id == "user_123"
    assert float(result.amount_due) == 99.990
    assert float(result.amount_paid) == 99.990
    assert float(result.amount_remaining) == 0.000
    assert result.currency == "usd"
    assert result.status == PaymentStatus.SUCCEEDED

def test_invoice_status_transitions(session):
    # Test invoice with different payment statuses
    invoice = UserInvoice(
        stripe_invoice_id="in_456",
        stripe_subscription_id="sub_456",
        user_id="user_456",
        amount_due=Decimal("199.990"),
        amount_paid=Decimal("0.000"),
        amount_remaining=Decimal("199.990"),
        currency="usd",
        status=PaymentStatus.PENDING,
        invoice_date=datetime.now(),
        due_date=datetime.now()
    )
    
    session.add(invoice)
    session.commit()
    
    # Update to succeeded status
    invoice.status = PaymentStatus.SUCCEEDED
    invoice.amount_paid = Decimal("199.990")
    invoice.amount_remaining = Decimal("0.000")
    invoice.paid_at = datetime.now()
    session.commit()
    
    result = session.query(UserInvoice).filter_by(stripe_invoice_id="in_456").first()
    assert result.status == PaymentStatus.SUCCEEDED
    assert float(result.amount_paid) == 199.990
    assert float(result.amount_remaining) == 0.000
    assert result.paid_at is not None

def test_invoice_failed_payment(session):
    # Test failed payment scenario
    invoice = UserInvoice(
        stripe_invoice_id="in_789",
        stripe_subscription_id="sub_789",
        user_id="user_789",
        amount_due=Decimal("299.990"),
        amount_paid=Decimal("0.000"),
        amount_remaining=Decimal("299.990"),
        currency="usd",
        status=PaymentStatus.FAILED,
        payment_intent_id="pi_failed_789",
        invoice_date=datetime.now(),
        due_date=datetime.now()
    )
    
    session.add(invoice)
    session.commit()
    
    result = session.query(UserInvoice).filter_by(stripe_invoice_id="in_789").first()
    assert result.status == PaymentStatus.FAILED
    assert float(result.amount_paid) == 0.000
    assert float(result.amount_remaining) == 299.990
    assert result.paid_at is None

def test_invoice_refund(session):
    # Test refund scenario
    invoice = UserInvoice(
        stripe_invoice_id="in_refund",
        stripe_subscription_id="sub_refund",
        user_id="user_refund",
        amount_due=Decimal("399.990"),
        amount_paid=Decimal("399.990"),
        amount_remaining=Decimal("0.000"),
        currency="usd",
        status=PaymentStatus.SUCCEEDED,
        payment_intent_id="pi_refund",
        invoice_date=datetime.now(),
        due_date=datetime.now(),
        paid_at=datetime.now()
    )
    
    session.add(invoice)
    session.commit()
    
    # Process refund
    invoice.status = PaymentStatus.REFUNDED
    invoice.amount_paid = Decimal("0.000")
    invoice.amount_remaining = Decimal("0.000")
    session.commit()
    
    result = session.query(UserInvoice).filter_by(stripe_invoice_id="in_refund").first()
    assert result.status == PaymentStatus.REFUNDED
    assert float(result.amount_paid) == 0.000

def test_invoice_str_repr(session):
    invoice = UserInvoice(
        stripe_invoice_id="in_str_test",
        stripe_subscription_id="sub_str_test",
        user_id="user_str_test",
        amount_due=Decimal("99.990"),
        amount_paid=Decimal("0.000"),
        amount_remaining=Decimal("99.990"),
        currency="usd",
        status=PaymentStatus.PENDING,
        invoice_date=datetime.now()
    )
    
    expected_str = f"<UserInvoice(stripe_invoice_id=in_str_test, amount_due=99.990)>"
    assert str(invoice) == expected_str
    assert repr(invoice) == expected_str 