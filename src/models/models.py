from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Index
from src.config.database import Base, engine
from sqlalchemy.orm import relationship


class ScanResultModel(Base):
    __tablename__ = "scan_results"

    id = Column(String, primary_key=True, index=True)
    scan_type = Column(String, index=True)
    website = Column(String, index=True)
    status = Column(String, index=True)
    target = Column(Text)
    created_at = Column(DateTime, index=True)
    completed_at = Column(DateTime, index=True)
    error = Column(Text, nullable=True)

    subdomains = relationship("SubdomainModel", back_populates="scan_result", cascade="all, delete-orphan", lazy='joined')
    ips = relationship("IPModel", back_populates="scan_result", cascade="all, delete-orphan", lazy='joined')
    emails = relationship("EmailModel", back_populates="scan_result", cascade="all, delete-orphan", lazy='joined')


class SubdomainModel(Base):
    __tablename__ = "subdomains"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scan_results.id", ondelete="CASCADE"), index=True)
    subdomain = Column(String, index=True)

    scan_result = relationship("ScanResultModel", back_populates="subdomains")

    __table_args__ = (Index('ix_subdomain_scan_id', 'scan_id', 'subdomain'),)


class IPModel(Base):
    __tablename__ = "ips"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scan_results.id", ondelete="CASCADE"), index=True)
    ip = Column(String, index=True)

    scan_result = relationship("ScanResultModel", back_populates="ips")

    __table_args__ = (Index('ix_ip_scan_id', 'scan_id', 'ip'),)


class EmailModel(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scan_results.id", ondelete="CASCADE"), index=True)
    email = Column(String, index=True)

    scan_result = relationship("ScanResultModel", back_populates="emails")

    __table_args__ = (Index('ix_email_scan_id', 'scan_id', 'email'),)


Base.metadata.create_all(bind=engine)
