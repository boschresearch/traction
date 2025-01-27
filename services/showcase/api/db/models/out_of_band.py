import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, Relationship

from api.db.models.base import BaseModel, BaseTable


class OutOfBandBase(BaseModel):
    msg_type: str = Field(nullable=False)
    msg: dict = Field(default={}, sa_column=Column(JSON))
    sender_id: Optional[uuid.UUID] = Field(default=None, foreign_key="tenant.id")
    recipient_id: Optional[uuid.UUID] = Field(default=None, foreign_key="tenant.id")
    sandbox_id: Optional[uuid.UUID] = Field(default=None, foreign_key="sandbox.id")


class OutOfBand(OutOfBandBase, BaseTable, table=True):
    sender: Optional["Tenant"] = Relationship(  # noqa: F821
        sa_relationship_kwargs={
            "primaryjoin": "OutOfBand.sender_id==Tenant.id",
            "lazy": "joined",
        }
    )
    recipient: Optional["Tenant"] = Relationship(  # noqa: F821
        sa_relationship_kwargs={
            "primaryjoin": "OutOfBand.recipient_id==Tenant.id",
            "lazy": "joined",
        }
    )

    class Config:
        arbitrary_types_allowed = True


class OutOfBandCreate(OutOfBandBase):
    pass


class OutOfBandRead(OutOfBandBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class OutOfBandUpdate(OutOfBandBase):
    name: Optional[str] = None
