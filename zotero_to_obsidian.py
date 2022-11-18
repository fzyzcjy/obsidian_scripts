import pprint
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import *

from zotero_sqlite_models import Item

path_zotero_sqlite = Path('/Users/tom/Zotero/zotero.sqlite')
dir_obsidian_papers = Path('/Users/tom/Main/notes/Papers')

KEY_ABSTRACT_NOTE = 'abstractNote'
LIBRARY_ID = 1


def parse(obj):
    all_fields = {item.field.fieldName: item.value.value for item in obj.itemData}

    abstract = all_fields.get(KEY_ABSTRACT_NOTE)

    info = {
        'key': obj.key,
        'link': f'zotero://select/items/{LIBRARY_ID}_{obj.key}',
        'dateAdded': obj.dateAdded,
        **{k: v for k, v in all_fields.items() if k != KEY_ABSTRACT_NOTE},
        'creators': [
            f'[[{creator.firstName}, {creator.lastName}]]'
            for creator in obj.creators
        ],
    }

    pprint.pprint(info)
    print(f'abstract={abstract}')

    return info


def calc_filename(info):
    return TODO


def calc_output(info):
    return TODO


# ref
# https://www.zotero.org/support/dev/client_coding/direct_sqlite_database_access
# https://github.com/zotero/zotero-schema/tree/master
def main():
    assert Path(path_zotero_sqlite).exists()
    engine = create_engine(f"sqlite:///{path_zotero_sqlite}", echo=False)
    session = Session(engine)

    stmt = select(Item).where(Item.key.in_(['IAMKX4G9']))

    for obj in session.scalars(stmt):
        info = parse(obj)
        filename = calc_filename(info)
        (dir_obsidian_papers / filename).write_text(calc_output(info))


if __name__ == '__main__':
    main()
