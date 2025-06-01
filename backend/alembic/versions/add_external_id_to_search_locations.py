"""add external_id to search_locations

Revision ID: add_external_id_to_search_locations
Revises: 04a17d4e0656
Create Date: 2024-03-15 10:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "add_external_id_to_search_locations"
down_revision: Union[str, None] = "04a17d4e0656"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add external_id column to search_locations table."""
    op.add_column(
        "search_locations", sa.Column("external_id", sa.String(), nullable=True)
    )
    op.add_column(
        "search_locations", sa.Column("updated_at", sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    """Remove external_id column from search_locations table."""
    op.drop_column("search_locations", "external_id")
    op.drop_column("search_locations", "updated_at")
