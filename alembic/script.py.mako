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
    pass

def downgrade():
    pass
