"""Presentation-only navigation; no engine or policy changes."""
from pathlib import Path
ASSETS=Path(__file__).with_name('navigation_web')


def respond(handler):
    if handler.path=='/navigation/info':
        handler.reply(200,dict(menu_url=getattr(handler.server,'menu_url',None)));return True
    files={'/navigation.js':('navigation.js','text/javascript'),'/menu.js':('menu.js','text/javascript'),
           '/navigation.css':('navigation.css','text/css')}
    if handler.path not in files:return False
    name,kind=files[handler.path]
    handler.reply(200,(ASSETS/name).read_bytes(),kind+'; charset=utf-8');return True


def viewer_page(page,controller):
    page=page.replace('</head>','<link rel="stylesheet" href="/navigation.css"></head>')
    return page.replace(f'<script src="/{controller}">',f'<script src="/navigation.js"></script><script src="/{controller}">')


def menu_page(page,live=False):
    page=page.replace('</head>','<link rel="stylesheet" href="/navigation.css"></head>')
    return page.replace('</body>',f'<script src="/menu.js" data-live="{str(live).lower()}"></script></body>')
