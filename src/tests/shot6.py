import asyncio
from playwright.async_api import async_playwright
SP='/tmp/claude-0/-home-claude/37c37c24-e61e-5f96-a9b1-f0bd18559ae8/scratchpad/'
async def run(name,w,h,mobile):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':h},is_mobile=mobile,has_touch=mobile)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///root/viva/test.html');await pg.wait_for_timeout(2500)
        await pg.click('#enter-at');await pg.wait_for_timeout(1500)
        await pg.evaluate('goState("5")');await pg.wait_for_timeout(1500)
        if mobile: await pg.click('#sb-cards');await pg.wait_for_timeout(900)
        await pg.evaluate('goCard(4,false)');await pg.wait_for_timeout(700)
        print(name,'places on',await pg.evaluate('document.querySelectorAll("#places .plc.on").length'))
        await pg.screenshot(path=SP+f'p_{name}_seid.png')
        await pg.evaluate('goCard(13,false)');await pg.wait_for_timeout(700)
        print(name,'lungau on',await pg.evaluate('[...document.querySelectorAll("#places .plc.on")].map(n=>n.textContent)'))
        await pg.evaluate('closeDrawer()');await pg.wait_for_timeout(300)
        print(name,'after close',await pg.evaluate('document.querySelectorAll("#places .plc.on").length'),errs)
        await b.close()
async def main(): await run('desk',1440,820,False); await run('phone',390,844,True)
asyncio.run(main())
