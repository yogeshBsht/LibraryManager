"""empty message

Revision ID: 04bef6086eb8
Revises: 
Create Date: 2022-05-14 19:05:41.339345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04bef6086eb8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bookname', sa.String(length=64), nullable=True),
    sa.Column('author', sa.String(length=64), nullable=True),
    sa.Column('inventory', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_book_bookname'), 'book', ['bookname'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_timestamp'), 'review', ['timestamp'], unique=False)
    op.create_table('user_book',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_book')
    op.drop_index(op.f('ix_review_timestamp'), table_name='review')
    op.drop_table('review')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_book_bookname'), table_name='book')
    op.drop_table('book')
    # ### end Alembic commands ###
