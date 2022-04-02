"""create post table

Revision ID: ee3e0a4d36f8
Revises: 
Create Date: 2022-04-02 14:02:34.218643

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import UniqueConstraint


# revision identifiers, used by Alembic.
revision = 'ee3e0a4d36f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", 
                    sa.Column("id", sa.Integer(), nullable = False, primary_key = True), 
                    sa.Column("title", sa.String(), nullable = False),
                    sa.Column("title", sa.String(), nullable = False, index = True),
                    sa.Column("content", sa.String(), nullable = False),
                    sa.Column("published", sa.Boolean(), nullable = False, server_default="TRUE"),

                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable = False,
                                                         server_default=sa.text("now()")),
                    sa.Column("owner_id", sa.Integer(), nullable = False)
                    )
    
    
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable = False), 
                    sa.Column("id", sa.Integer(), nullable = False), 
                    sa.Column("email", sa.String(), nullable = False, unique=True), 
                    sa.Column("password", sa.String(), nullable = False), 
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable = False,
                                        server_default=sa.text("now()")),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )

    op.create_table("votes", 
                    sa.Column("user_id", sa.Integer(), nullable = False),
                    sa.Column("post_id", sa.Integer(), nullable = False),
                    sa.Column("liked", sa.Boolean, nullable = False, server_default = "0"),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )

    op.bulk_insert(Table)


def downgrade():
    op.drop_table ("posts")
    op.drop_table ("users")
    op.drop_table ("votes")

