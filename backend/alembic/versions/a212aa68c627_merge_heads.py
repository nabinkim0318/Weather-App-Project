"""merge heads

Revision ID: a212aa68c627
Revises: add_external_id_to_search_locations, f29e46885ef2
Create Date: 2025-06-01 10:16:04.538440

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a212aa68c627"
down_revision: Union[str, None] = (
    "add_external_id_to_search_locations",
    "f29e46885ef2",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
