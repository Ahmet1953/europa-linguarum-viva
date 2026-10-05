# Wraps the assembled page into a standalone document for the public site (index.html at the repository root).
# Run from src/:  node build.mjs && python3 content_src.py && python3 assemble.py && python3 build_site.py
import pathlib
page = pathlib.Path('europa-linguarum-viva.html').read_text()
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="description" content="A living atlas of Europe\'s languages and regional voices. Austria pilot, source-checked, CEFR-linked.">\n'
        # not yet announced: keep search engines out until Impressum and privacy pages are online
        '<meta name="robots" content="noindex">\n'
        '<style>html,body{margin:0;background:#06101f}[hidden]{display:none!important}</style>\n')
pathlib.Path('../index.html').write_text(head + page + '\n</html>\n')
print('index.html written')
