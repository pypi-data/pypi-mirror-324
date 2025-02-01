import json
import os
from pathlib import Path
from loguru import logger
from openai import OpenAI
import instructor
import polib

client = instructor.from_openai(OpenAI())
default_locale = "en"

default_catalog_path = str(Path(__file__).parent / default_locale / "LC_MESSAGES" / "messages.po")
default_catalog = polib.pofile(default_catalog_path)

for entry in default_catalog:
    if not entry.msgstr:
        messages = [
            {
                "role": "system",
                "content": f"You are a helpful translator helping me fill a string placeholder.",
            },
            {
                "role": "user",
                "content": f"Fill the following string:\n\n{entry.msgid}:",
            },
        ]
        tl = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_model=str,
            max_retries=3,
            temperature=0,
            top_p=0,
            seed=1234,
        )
        entry.msgstr = tl
        logger.warning(f"Translated {entry.msgid} to {entry.msgstr}")
default_catalog.save(default_catalog_path)

for other_locale in Path(__file__).parent.iterdir():
    if other_locale.name == default_locale or not other_locale.is_dir() or not "LC_MESSAGES" in os.listdir(other_locale):
        continue

    logger.info(f"Checking {other_locale.name} ({other_locale})")
    other_local_path = other_locale / "LC_MESSAGES" / "messages.po"
    if not other_local_path.exists():
        po = polib.POFile()
        po.metadata = default_catalog.metadata
        po.save(other_local_path)
    other_catalog = polib.pofile(other_locale / "LC_MESSAGES" / "messages.po")
    for entry in default_catalog:
        other_entry = other_catalog.find(entry.msgid)
        if not other_entry or not other_entry.msgstr:
            logger.info(f"Translating {entry.msgid} from {default_locale} to {other_locale}")
            messages = [
                {
                    "role": "system",
                    "content": f"You are a helpful translator helping me translate my website from {default_locale} to {other_locale}.",
                },
                {
                    "role": "user",
                    "content": f"Translate the following string:\n\n{entry.msgid}\n\n{entry.msgstr}",
                },
            ]
            tl = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                response_model=str,
                max_retries=3,
                temperature=0,
                top_p=0,
                seed=1234,
            )
            other_entry = polib.POEntry(
                msgid=entry.msgid,
                msgstr=tl,
            )
            other_catalog.append(other_entry)
    other_catalog.save(other_local_path)