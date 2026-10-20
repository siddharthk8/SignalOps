"""modify check constraint

Revision ID: 2d46a7f609c3
Revises: 2b0a06b2290d
Create Date: 2026-10-20 15:22:41.034491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d46a7f609c3'
down_revision: Union[str, Sequence[str], None] = '2b0a06b2290d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_check_constraint(
        "ck_source_apps_tokens_both_present_or_absent",
        "source_apps",
        """
        (access_key IS NULL AND secret_access_key_hash IS NULL)
        OR
        (access_key IS NOT NULL AND secret_access_key_hash IS NOT NULL)
        """,
    )


def downgrade():
    op.drop_constraint(
        "ck_source_apps_tokens_both_present_or_absent",
        "source_apps",
        type_="check",
    )
