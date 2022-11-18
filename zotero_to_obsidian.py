import pprint
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import *

from zotero_sqlite_models import Item

path_zotero_sqlite = '/Users/tom/Zotero/zotero.sqlite'

KEY_ABSTRACT_NOTE = 'abstractNote'


# ref
# https://www.zotero.org/support/dev/client_coding/direct_sqlite_database_access
# https://github.com/zotero/zotero-schema/tree/master
def main():
    assert Path(path_zotero_sqlite).exists()
    engine = create_engine(f"sqlite:///{path_zotero_sqlite}", echo=False)
    session = Session(engine)

    stmt = select(Item).where(Item.key.in_(['IAMKX4G9']))
    for obj in session.scalars(stmt):
        all_fields = {item.field.fieldName: item.value.value for item in obj.itemData}

        abstract = all_fields.get(KEY_ABSTRACT_NOTE)

        info = {
            'key': obj.key,
            'dateAdded': obj.dateAdded,
            **{k: v for k, v in all_fields.items() if k != KEY_ABSTRACT_NOTE},
            'creators': [
                f'[[{creator.firstName}, {creator.lastName}]]'
                for creator in obj.creators
            ],
        }

        pprint.pprint(info)
        print(f'abstract={abstract}')


if __name__ == '__main__':
    main()
