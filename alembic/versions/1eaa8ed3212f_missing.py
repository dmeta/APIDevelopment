"""missing

Revision ID: 1eaa8ed3212f
Revises: 5a4db7fb55f6
Create Date: 2022-04-02 16:21:03.826328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1eaa8ed3212f'
down_revision = '5a4db7fb55f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('votes', 'liked',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    op.create_foreign_key("votes_posts_fk2", 'votes', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("votes_posts_fk2", 'votes', type_='foreignkey')
    op.alter_column('votes', 'liked',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    # ### end Alembic commands ###
