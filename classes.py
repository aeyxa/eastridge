import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Invoice(Base):

    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, unique=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    invoice_items = relationship('InvoiceItem',backref='invoice',lazy='dynamic')

    def create():

        engine = create_engine('mysql://root@localhost/test')
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        invoice = Invoice()
        session.add(invoice)
        session.commit()

        return invoice.id

    def find(id):

        engine = create_engine('mysql://root@localhost/test')
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        invoice = session.query(Invoice).get(id)

        return invoice

class InvoiceItem(Base):

    __tablename__ = 'invoice_items'

    id = Column(Integer, primary_key=True, unique=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    units = Column(Integer)
    description = Column(String(64))
    amount = Column(Numeric)

    def create(invoice_id, units, description, amount):

        engine = create_engine('mysql://root@localhost/test')
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        invoice_item = InvoiceItem(
            invoice_id=invoice_id,
            units=units,
            description=description,
            amount=amount
        )

        session.add(invoice_item)
        session.commit()

        return invoice_item.id

    def find(id):

        engine = create_engine('mysql://root@localhost/test')
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        invoice_items = session.query(InvoiceItem).filter(
            InvoiceItem.invoice_id==id
        ).all()

        return invoice_items
