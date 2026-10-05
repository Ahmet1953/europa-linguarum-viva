import asyncio
from playwright.async_api import async_playwright
SP='/tmp/claude-0/'
html=open('europa-linguarum-viva.html').read()
open('test.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0}[hidden]{display:none!important}</style></head><body>'+html+'</body></html>')
async def run(name,w,h,m):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':h},is_mobile=m,has_touch=m)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///root/viva/test.html?nointro');await pg.wait_for_timeout(2500)
        await pg.click('#enter-at');await pg.wait_for_timeout(1200)
        await pg.evaluate('goState("5")');await pg.wait_for_timeout(1500)
        if m: await pg.click('#sb-cards');await pg.wait_for_timeout(800)
        for cid in ['sbg-atlas','sbg-seid','sbg-border','gau-506','gau-501']:
            i=await pg.evaluate(f'CONTENT.cards.findIndex(c=>c.id==="{cid}")')
            await pg.evaluate(f'goCard({i},false)');await pg.wait_for_timeout(500)
            on=await pg.evaluate('[...document.querySelectorAll("#places .plc.on")].length')
            print(name,cid,'markers on',on)
            await pg.screenshot(path=SP+f'P_{name}_{cid}.png')
        print(name,errs); await b.close()
async def main(): await run('desk',1440,820,False); await run('phone',390,844,True)
asyncio.run(main())
