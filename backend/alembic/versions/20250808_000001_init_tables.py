from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250808_000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('vk_user_id', sa.String(length=64), nullable=False, unique=True),
        sa.Column('username', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'matches',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('mode', sa.String(length=16), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('ended_at', sa.DateTime(), nullable=True),
        sa.Column('winner_user_id', sa.Integer(), nullable=True),
    )

    op.create_table(
        'match_participants',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('match_id', sa.Integer(), sa.ForeignKey('matches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('kills', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('deaths', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('damage_done', sa.Integer(), nullable=False, server_default='0'),
    )

    op.create_table(
        'player_state_snapshots',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('match_id', sa.Integer(), sa.ForeignKey('matches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('t', sa.Integer(), nullable=False),
        sa.Column('payload_json', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('player_state_snapshots')
    op.drop_table('match_participants')
    op.drop_table('matches')
    op.drop_table('users')