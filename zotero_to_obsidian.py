from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import *

from zotero_sqlite_models import Item

path_zotero_sqlite = '/Users/tom/Zotero/zotero.sqlite'


# ref
# https://www.zotero.org/support/dev/client_coding/direct_sqlite_database_access
# https://github.com/zotero/zotero-schema/tree/master
def main():
    assert Path(path_zotero_sqlite).exists()
    engine = create_engine(f"sqlite:///{path_zotero_sqlite}", echo=True)
    session = Session(engine)

    stmt = select(Item)
    for item in session.scalars(stmt):
        print(item)
        break


if __name__ == '__main__':
    main()
