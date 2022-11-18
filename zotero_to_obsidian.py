import json
import pprint
from pathlib import Path

import yaml
from sqlalchemy import create_engine, select
from sqlalchemy.orm import *

from zotero_sqlite_models import Item

path_zotero_sqlite = Path('/Users/tom/Zotero/zotero.sqlite')
dir_obsidian_papers = Path('/Users/tom/Main/notes/Papers')

KEY_TITLE = 'title'
KEY_ABSTRACT_NOTE = 'abstractNote'

LIBRARY_ID = 1


def parse(obj):
    all_fields = {item.field.fieldName: item.value.value for item in obj.itemData}

    info = {
        'key': obj.key,
        'zoteroLink': f'zotero://select/items/{LIBRARY_ID}_{obj.key}',
        'dateAdded': obj.dateAdded,
        'creators': [
            f'[[{creator.firstName}, {creator.lastName}]]'
            for creator in obj.creators
        ],
        **all_fields,
    }

    pprint.pprint(info)

    return info


def calc_filename(info):
    sanitized_title = info[KEY_TITLE] \
        .replace('/', '|') \
        .replace('\\', '|') \
        .replace(':', '：')
    return f'{sanitized_title}.md'


def calc_output(info):
    front_matter = json.loads(json.dumps(info))
    del front_matter[KEY_ABSTRACT_NOTE]

    return f'''---
{yaml.dump(front_matter)}
---

## Abstract

{info[KEY_ABSTRACT_NOTE]}

'''


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
        path_output = dir_obsidian_papers / filename
        print(f'Output: {path_output}')
        path_output.write_text(calc_output(info))


if __name__ == '__main__':
    main()
