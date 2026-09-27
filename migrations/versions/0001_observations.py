"""Create the PostGIS observation store.

Revision ID: 0001_observations
Revises:
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0001_observations"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table(
        "observations",
        sa.Column("observation_id", sa.String(128), primary_key=True),
        sa.Column("species_id", sa.String(255), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", JSONB, nullable=False),
        sa.Column("quality", JSONB, nullable=False),
        sa.Column("provenance", JSONB, nullable=False),
        sa.Column("ecoregion", sa.String(255), nullable=False),
    )
    op.execute("ALTER TABLE observations ADD COLUMN location geometry(Point, 4326) NOT NULL")
    op.create_index(
        "ix_observations_species_observed", "observations", ["species_id", "observed_at"]
    )
    op.execute("CREATE INDEX ix_observations_location ON observations USING GIST (location)")


def downgrade() -> None:
    op.drop_table("observations")
