from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import *

from zotero_sqlite_models import Item

path_zotero_sqlite = Path('/Users/tom/Zotero/zotero.sqlite')
dir_obsidian_papers = Path('/Users/tom/Main/notes/Papers')

KEY_TITLE = 'title'
KEY_ABSTRACT_NOTE = 'abstractNote'
KEY_DATE = 'date'

META_BLACKLIST_KEYS = [
    KEY_ABSTRACT_NOTE
]

MANUALLY_SORTED_KEYS = [
    KEY_TITLE,
    'zoteroLink',
    'date',
    'creators',
]

LIBRARY_ID = 1

BLOCK_START = '%% AUTO GENERATED BY zotero_to_obsidian.py START %%'
BLOCK_END = '%% AUTO GENERATED BY zotero_to_obsidian.py END %%'

DEFAULT_TEXT = f'''**rating**:: ⭐

**summary**:: 

---

{BLOCK_START}
/* nothing */
{BLOCK_END}
'''


def parse(obj):
    all_fields = {item.field.fieldName: item.value.value for item in obj.itemData}

    if KEY_TITLE not in all_fields:
        return None

    interpolated_date, partial_date = \
        all_fields[KEY_DATE].split(' ') if KEY_DATE in all_fields else ('', '')

    zotero_link = f'zotero://select/items/{LIBRARY_ID}_{obj.key}'

    info = {
        'key': obj.key,
        'zoteroLink': f'[{zotero_link}]({zotero_link})',
        'dateAdded': obj.dateAdded,
        'creators': ' ; '.join(
            f'[[{creator.firstName}, {creator.lastName}]]'
            for creator in obj.creators
        ),
        **all_fields,
        'date': interpolated_date,
    }
    print(info)

    return info


def calc_filename(info):
    sanitized_title = info[KEY_TITLE] \
        .replace('/', '|') \
        .replace('\\', '|') \
        .replace(':', '：')
    return f'{sanitized_title}.md'


def format_meta(info):
    def format_one_key(k):
        return f'**{k}**:: {info[k]}'

    lines = []

    for key in MANUALLY_SORTED_KEYS:
        if key in info:
            lines.append(format_one_key(key))
    for key in info.keys():
        if key not in MANUALLY_SORTED_KEYS and key not in META_BLACKLIST_KEYS:
            lines.append(format_one_key(key))

    return '\n'.join(lines)


def calc_block_output(info):
    return f'''
## Metadata

{format_meta(info)}

## Abstract

{info.get(KEY_ABSTRACT_NOTE) or 'N/A'}
'''


def calc_output(block_output, old_text):
    old_text = old_text or DEFAULT_TEXT
    old_lines = old_text.split('\n')

    idx_start = old_lines.index(BLOCK_START)
    idx_end = old_lines.index(BLOCK_END)

    return '\n'.join([
        *old_lines[:idx_start + 1],
        *block_output.split('\n'),
        *old_lines[idx_end:],
    ])


# ref
# https://www.zotero.org/support/dev/client_coding/direct_sqlite_database_access
# https://github.com/zotero/zotero-schema/tree/master
def main():
    assert Path(path_zotero_sqlite).exists()
    engine = create_engine(f"sqlite:///{path_zotero_sqlite}", echo=False)
    session = Session(engine)

    stmt = select(Item)

    for obj in session.scalars(stmt):
        info = parse(obj)
        if info is None:
            continue

        filename = calc_filename(info)
        path_output = dir_obsidian_papers / filename
        old_text = path_output.read_text() if path_output.exists() else None
        block_output = calc_block_output(info)

        print(f'Output: {path_output}')
        path_output.write_text(calc_output(block_output, old_text))


if __name__ == '__main__':
    main()
