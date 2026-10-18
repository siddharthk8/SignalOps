from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, String, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.core import Base


class EmailSuppressionReason(StrEnum):
    HARD_BOUNCE = "hard_bounce"
    COMPLAINT = "complaint"


# Used to suppress bounced/complaint emails from AWS SES.
class EmailSuppression(Base):
    __tablename__ = "email_suppressions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    reason: Mapped[EmailSuppressionReason] = mapped_column(
        SAEnum(
            EmailSuppressionReason,
            name="email_suppression_reason",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
    )

    # datetime
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
