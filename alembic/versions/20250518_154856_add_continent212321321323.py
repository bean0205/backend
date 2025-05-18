# This script initializes alembic commands
# You can add custom commands here if needed

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '<revision_id>'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'continent',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(10), nullable=False, unique=True),
    )
    op.create_index('ix_continent_name', 'continent', ['name'])
    op.create_index('ix_continent_code', 'continent', ['code'])


def downgrade():
    op.drop_index('ix_continent_name', table_name='continent')
    op.drop_index('ix_continent_code', table_name='continent')
    op.drop_table('continent')
