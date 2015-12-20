import sqlalchemy as sa

from .base import Base

class Test(Base):
    __tablename__ = 'test'
    __table_args__ = (
        sa.UniqueConstraint('name', 'file', 'timestamp', 'project_id'),
    )

    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String, index=True)
    file = sa.Column(sa.String, index=True)
    status = sa.Column(sa.String, index=True)
    timestamp = sa.Column(sa.DateTime, index=True)

    project_id = sa.Column(sa.Integer, sa.ForeignKey('project.id'), index=True)

class Project(Base):
    __tablename__ = 'project'

    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String, unique=True, index=True)
