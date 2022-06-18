from datetime import datetime

from app.consts import DATETIME_FORMAT


def data_gaps_located_message(gap_info: list[tuple[datetime, datetime]]) -> str:
    singular = True if len(gap_info) == 1 else False
    gap_str: str = 'There {} {} date gap{} that {} already been located on the table :\n'.format(
        'is' if singular else 'are',
        len(gap_info),
        '' if singular else 's',
        'has' if singular else 'have'
    )
    for data_pair in gap_info:
        gap_str += f"From {data_pair[0].strftime(DATETIME_FORMAT)} to {data_pair[1].strftime(DATETIME_FORMAT)}\n"
    return gap_str


def rows_were_affected_message(affected: int) -> str:
    singular: bool = affected == 1
    return '{} row{} {} affected'.format(
        affected,
        '' if singular else 's',
        'was' if singular else 'were'
    )
