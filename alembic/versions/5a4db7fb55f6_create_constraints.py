"""create constraints

Revision ID: 5a4db7fb55f6
Revises: ee3e0a4d36f8
Create Date: 2022-04-02 16:04:07.304220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a4db7fb55f6'
down_revision = 'ee3e0a4d36f8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(constraint_name="posts_users_fk", source_table="posts", 
                          referent_table="users",
                          local_cols=["owner_id"], 
                          remote_cols=["id"], ondelete="CASCADE")

    op.create_foreign_key(constraint_name="votes_users_fk", source_table="votes", 
                          referent_table="users",
                          local_cols=["user_id"], 
                          remote_cols=["id"], ondelete="CASCADE")


def downgrade():
    op.drop_constraint(constraint_name="posts_users_fk", table_name="posts")
    op.drop_constraint(constraint_name="votes_users_fk", table_name="votes")
    