import sqlalchemy as sa

from .base import session
from .models import Test

def get_range():
    return session.query(
        Test.name,
        Test.file,
        sa.func.min(Test.timestamp).label('min_timestamp'),
    ).group_by(
        Test.name,
        Test.file,
    )

def get_histogram(unit='minute'):
    range = get_range().subquery()
    passed = sa.func.count(
        sa.case(
            [(Test.status == '.', 1)],
        ),
    )
    total = sa.func.count(Test.name)
    group_columns = [
        Test.name,
        Test.file,
        sa.extract(unit, Test.timestamp - range.c.min_timestamp).label(unit),
    ]
    return session.query(
        passed.label('passed'),
        total.label('total'),
        (sa.cast(passed, sa.Numeric) / sa.cast(total, sa.Numeric)).label('ratio'),
        *group_columns
    ).join(
        range,
        sa.and_(
            Test.name == range.c.name,
            Test.file == range.c.file,
        ),
    ).group_by(
        *group_columns
    )
