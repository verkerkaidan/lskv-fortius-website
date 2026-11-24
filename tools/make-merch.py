#!/usr/bin/env python3
"""Merch page + reusable merch patterns. Writes src/patterns/merch-*.html, dist/patterns/merch-*.json, src/content/merch-page.html"""
import os, json, re, base64
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
svg=re.search(r"svg='''(.*?)'''",open(os.path.join(ROOT,'tools','make-textphoto.py')).read(),re.S).group(1).replace('width="1200" height="800" viewBox="0 0 1200 800"','width="800" height="800" viewBox="0 0 800 800"').replace('M0 0L1200 800M1200 0L0 800','M0 0L800 800M800 0L0 800').replace('<rect width="1200" height="800"','<rect width="800" height="800"').replace('x="330" y="360"','x="130" y="360"').replace('x="600" y="415"','x="400" y="415"')
URI='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
def p(t,cls=None):
    a=' {"className":"%s"}'%cls if cls else ''
    c=' class="%s"'%cls if cls else ''
    return '<!-- wp:paragraph%s -->\n<p%s>%s</p>\n<!-- /wp:paragraph -->'%(a,c,t)
def photo_block(pid,url,alt,cap=None):
    return '<!-- wp:image {"id":%d,"sizeSlug":"large","linkDestination":"none","className":"fortius-merch-image"} -->\n<figure class="wp-block-image size-large fortius-merch-image"><img src="%s" alt="%s" class="wp-image-%d"/>%s</figure>\n<!-- /wp:image -->'%(pid,url,alt,pid,'<figcaption class="wp-element-caption">%s</figcaption>'%cap if cap else '')
def img_block(alt,caption=None):
    cap='<figcaption class="wp-element-caption">%s</figcaption>'%caption if caption else ''
    return '<!-- wp:image {"sizeSlug":"large","linkDestination":"none","className":"fortius-merch-image"} -->\n<figure class="wp-block-image size-large fortius-merch-image"><img src="%s" alt="%s"/>%s</figure>\n<!-- /wp:image -->'%(URI,alt,cap)
def card(name='[Placeholder Productnaam]',sizes=True,images=2,price=None,desc=None,colors=None,fits=None,sizetxt=None,extra=None,photo=None,photos=None):
    if photos: imgs=[photo_block(*x) for x in photos]
    elif photo: imgs=[photo_block(*photo)]
    elif colors: imgs=[img_block('[Placeholder Image] %s – %s'%(name,c),c) for c in colors] if len(colors)>1 else [img_block(name)]
    else: imgs=[img_block('[Placeholder Image]','[Placeholder: kleur %d]'%(i+1)) for i in range(images)] if images>1 else [img_block('[Placeholder Image]')]
    gallery='<!-- wp:group {"className":"fortius-merch-gallery","layout":{"type":"default"}} -->\n<div class="wp-block-group fortius-merch-gallery">'+'\n\n'.join(imgs)+'</div>\n<!-- /wp:group -->'
    body=['<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">%s</h3>\n<!-- /wp:heading -->'%name, p(price or '€ [prijs]','fortius-merch-price'), p(desc or '[Placeholder: korte omschrijving]')]
    if photo and colors: body.append(p('<strong>Kleuren</strong> '+', '.join(colors),'fortius-merch-meta'))
    if fits: body.append(p('<strong>Pasvorm</strong> '+fits,'fortius-merch-meta'))
    if sizes: body.append(p('<strong>Maten</strong> '+(sizetxt or '[Placeholder: bijv. XS – XXL]'),'fortius-merch-meta'))
    if extra: body.append(p(extra,'fortius-merch-meta'))
    inner='\n\n'.join(body)
    return ('<!-- wp:group {"className":"fortius-merch-card","layout":{"type":"default"}} -->\n<div class="wp-block-group fortius-merch-card">'+gallery+'\n\n'
      '<!-- wp:group {"className":"fortius-merch-body","layout":{"type":"default"}} -->\n<div class="wp-block-group fortius-merch-body">'+inner+'</div>\n<!-- /wp:group --></div>\n<!-- /wp:group -->')
def section(name,style,inner_blocks,inner_cls='fortius-section-inner',gap=None):
    return ('<!-- wp:group {"metadata":{"name":"%s","categories":["lskvfortius"]},"align":"full","className":"is-style-section-%d","style":{"spacing":{"padding":{"top":"80px","bottom":"80px"},"blockGap":"0","margin":{"top":"0","bottom":"0"}}}} -->\n'
      '<div class="wp-block-group alignfull is-style-section-%d" style="margin-top:0;margin-bottom:0;padding-top:80px;padding-bottom:80px"><!-- wp:group {"className":"%s"%s} -->\n<div class="wp-block-group %s">%s</div>\n<!-- /wp:group --></div>\n<!-- /wp:group -->')%(name,style,style,inner_cls,(',"style":{"spacing":{"blockGap":"%s"}}'%gap) if gap else '',inner_cls,inner_blocks)
hero=('<!-- wp:group {"metadata":{"name":"Hero (No Buttons)","categories":["lskvfortius"]},"align":"full","className":"fortius-page-hero is-style-section-1","style":{"spacing":{"padding":{"top":"48px","bottom":"48px"},"blockGap":"0","margin":{"top":"0","bottom":"0"}}}} -->\n'
 '<div class="wp-block-group alignfull fortius-page-hero is-style-section-1" style="margin-top:0;margin-bottom:0;padding-top:48px;padding-bottom:48px"><!-- wp:group {"className":"fortius-section-inner","style":{"spacing":{"blockGap":"0px"}}} -->\n<div class="wp-block-group fortius-section-inner">'
 +p('merch','is-style-text-annotation')+'\n\n<!-- wp:heading {"style":{"typography":{"textAlign":"center"}}} -->\n<h2 class="wp-block-heading has-text-align-center">fortius merch</h2>\n<!-- /wp:heading -->\n\n'
 +p('Loop tijdens én buiten je trainingen helemaal in Fortius-style rond.','fortius-hero-sub')+'</div>\n<!-- /wp:group --></div>\n<!-- /wp:group -->')
JS=("(function(){var el=document.getElementById('fortius-countdown');if(!el)return;var t=new Date(el.getAttribute('data-date')).getTime();"
 "var f=new Intl.DateTimeFormat('nl-NL',{day:'numeric',month:'long',year:'numeric'});var d0=document.getElementById('fortius-countdown-date');if(d0&&!isNaN(t))d0.textContent=f.format(new Date(t));"
 "function u(n,l){return '<div class=\"fortius-countdown__unit\"><span class=\"fortius-countdown__num\">'+n+'</span><span class=\"fortius-countdown__label\">'+l+'</span></div>';}"
 "function tick(){var n=t-Date.now();if(isNaN(t))return;if(n<=0){el.innerHTML='<p class=\"fortius-countdown__done\">'+el.getAttribute('data-done')+'</p>';clearInterval(i);return;}"
 "var d=Math.floor(n/864e5),h=Math.floor(n%864e5/36e5),m=Math.floor(n%36e5/6e4),s=Math.floor(n%6e4/1e3);"
 "el.innerHTML=u(d,'dagen')+u(h,'uur')+u(m,'min')+u(s,'sec');}"
 "var i=setInterval(tick,1000);tick();})();")
countdown=('<!-- wp:group {"metadata":{"name":"Volgende merch-ronde","categories":["lskvfortius"]},"align":"full","className":"is-style-section-2 fortius-merch-countdown","style":{"spacing":{"padding":{"top":"28px","bottom":"28px"},"blockGap":"0","margin":{"top":"0","bottom":"0"}}}} -->\n'
 '<div class="wp-block-group alignfull is-style-section-2 fortius-merch-countdown" style="margin-top:0;margin-bottom:0;padding-top:28px;padding-bottom:28px"><!-- wp:group {"className":"fortius-section-inner"} -->\n<div class="wp-block-group fortius-section-inner">'
 +p('special drop: bestellen kan nog t/m','is-style-text-annotation')+'\n\n'
 '<!-- wp:html -->\n<p class="fortius-countdown__date wp-block-paragraph"><time id="fortius-countdown-date" datetime="2026-11-22">22 november 2026</time></p>\n'
 '<div id="fortius-countdown" class="fortius-countdown" data-date="2026-11-22T23:59:59+01:00" data-done="De bestelronde is gesloten. Houd onze socials in de gaten voor de volgende merch-ronde."></div>\n'
 '<script>'+JS+'</script>\n<!-- /wp:html --></div>\n<!-- /wp:group --></div>\n<!-- /wp:group -->')
countdown_live=countdown
intro=(p('special drop','is-style-text-annotation')+'\n\n<!-- wp:heading -->\n<h2 class="wp-block-heading">wat zat er in de drop?</h2>\n<!-- /wp:heading -->\n\n'
 +p('Dit was een special drop: sommige items, zoals het T-shirt, werden maar één keer aangeboden. Van de andere items weten we niet of ze terugkomen. Bij de waterfles en de shaker kon je gratis je eigen naam laten zetten.')+'\n\n')
def grid(cards):
    return ('<!-- wp:group {"className":"fortius-merch-grid","layout":{"type":"grid","minimumColumnWidth":"18rem"}} -->\n<div class="wp-block-group fortius-merch-grid">'+'\n\n'.join(cards)+'</div>\n<!-- /wp:group -->')
NAME='Eigen naam erop is mogelijk, zonder extra kosten.'
SZ='XS – XXL'
items=[card('Limited edition T-shirt',photo=(1045,'https://lskvfortius.nl/wp-content/uploads/2026/11/merch-drop-limited-edition-tshirt.webp','Limited edition T-shirt met Fortius-ontwerp, voor- en achterkant'),price='€ 24,99',desc='T-shirt met een limited edition design. Wordt maar één keer aangeboden.',fits='Oversized',sizetxt=SZ),
 card('Fortius sportsokken',photo=(1046,'https://lskvfortius.nl/wp-content/uploads/2026/11/merch-drop-sportsokken.webp','Fortius sportsokken'),price='€ 4,99 per paar',desc='Witte sportsokken met Fortius-logo.',sizetxt='35–38, 39–42 of 43–46',extra='Je kunt 1 tot 5 paar per bestelling kiezen.'),
 card('Wide leg joggingbroek',photo=(1047,'https://lskvfortius.nl/wp-content/uploads/2026/11/merch-drop-wide-leg-joggingbroek.webp','Wide leg joggingbroek in zwart met Fortius-logo'),price='€ 29,99',desc='Joggingbroek met wijde pijpen en Fortius-logo.',sizetxt=SZ,extra='Pijpen recht laten vallen? Bestel je gebruikelijke maat. Liever wijd? Bestel een maat groter.'),
 card('Cuffed joggingbroek',colors=['Zwart','Donkergrijs'],photos=[(1052,'https://lskvfortius.nl/wp-content/uploads/2026/11/merch-drop-cuffed-joggingbroek-zwart.webp','Cuffed joggingbroek in zwart met Fortius-logo','Zwart'),(1053,'https://lskvfortius.nl/wp-content/uploads/2026/11/merch-drop-cuffed-joggingbroek-donkergrijs.webp','Cuffed joggingbroek in donkergrijs met Fortius-logo','Donkergrijs')],price='€ 24,99',desc='Joggingbroek met boorden om de enkels en Fortius-logo.',sizetxt=SZ),
 card('Waterfles 750 ml',photo=(1049,'https://lskvfortius.nl/wp-content/uploads/2026/11/merch-drop-waterfles.webp','Gegraveerde RVS waterfles van 750 ml met Fortius-logo'),price='€ 21,99',desc='Gegraveerde RVS thermosfles: blijft tot 24 uur koud of tot 12 uur warm.',sizes=False,images=1,extra=NAME),
 card('Fortius shaker 600 ml',photo=(1050,'https://lskvfortius.nl/wp-content/uploads/2026/11/merch-drop-shaker.webp','Fortius shaker van 600 ml met Fortius-logo'),price='€ 25,99',desc='RVS thermosshaker: blijft tot 8 uur koud of tot 6 uur warm.',sizes=False,images=1,extra=NAME),
 card('Chalk 100 ml',photo=(1051,'https://lskvfortius.nl/wp-content/uploads/2026/11/merch-drop-chalk.webp','Navulbaar flesje chalk van 100 ml met Fortius-logo'),price='€ 4,99',desc='Navulbaar flesje met chalk. Gratis bijvullen kan bij het Fortius-bord.',sizes=False,images=1)]
PICK=("(function(){var C={zwart:'#121212',wit:'#ffffff',rood:'#c81e2c',donkerrood:'#8f1520',blauw:'#1f4fa3',navy:'#14213d',marine:'#14213d',grijs:'#8a8a86',donkergrijs:'#3a3a38',lichtgrijs:'#c9c9ce',groen:'#2e7d32',geel:'#f2c230',oranje:'#e8832a',roze:'#e58fb1',paars:'#6b3fa0',bruin:'#6b4a32',beige:'#d8c8a8',creme:'#f1ead7'};"
 "function dot(n){var k=n.toLowerCase().replace(/[^a-z]/g,'');return C[k]||'';}"
 "document.querySelectorAll('.fortius-merch-card').forEach(function(card){var figs=[].slice.call(card.querySelectorAll('.fortius-merch-gallery figure'));if(!(figs.length>1))return;card.classList.add('is-enhanced');"
 "var bar=document.createElement('div');bar.className='fortius-merch-colors';bar.setAttribute('role','group');bar.setAttribute('aria-label','Kleur');var btns=[];"
 "function pick(i){figs.forEach(function(f,j){f.classList.toggle('is-active',j===i);});btns.forEach(function(b,j){b.setAttribute('aria-pressed',j===i?'true':'false');});}"
 "figs.forEach(function(f,i){var im=f.querySelector('img');var cap=f.querySelector('figcaption');var name=(cap?cap.textContent.trim():'')||(im?im.alt:'')||('Variant '+(i+1));var b=document.createElement('button');b.type='button';b.className='fortius-merch-color';var d=dot(name);if(d){var s=document.createElement('span');s.className='fortius-merch-dot';s.style.background=d;b.appendChild(s);}b.appendChild(document.createTextNode(name));b.addEventListener('click',function(){pick(i);});bar.appendChild(b);btns.push(b);});"
 "var after=card.querySelector('.fortius-merch-price');(after||card.querySelector('.fortius-merch-body')).insertAdjacentElement('afterend',bar);pick(0);});})();")
picker='<!-- wp:html -->\n<script>'+PICK+'</script>\n<!-- /wp:html -->'
products=section('Merch-items',3,intro+grid(items)+'\n\n'+picker)
order=section('Bestellen',5,
 p('bestellen','is-style-text-annotation')+'\n\n<!-- wp:heading -->\n<h2 class="wp-block-heading">bestel je merch</h2>\n<!-- /wp:heading -->\n\n'
 +p('Bestellen kan tijdens een merch-ronde via het formulier hieronder.')+'\n\n'
 +p('<strong>Deadline:</strong> bestellen kan t/m zondag 22 november. Daarna kunnen er geen bestellingen of wijzigingen meer worden gedaan. Vragen, of wil je je bestelling nog wijzigen? Mail de MerchCo via <a href="mailto:merchcommissie.lskvfortius@gmail.com">merchcommissie.lskvfortius@gmail.com</a>.')+'\n\n'
 +p('<strong>Betalen:</strong> na de deadline stuurt de MerchCo je een Tikkie voor je bestelling. Betaal die vóór de betaaldeadline, anders wordt je bestelling niet geplaatst.')+'\n\n'
 +p('Liever een apart venster? <a href="https://docs.google.com/forms/d/e/1FAIpQLScam6dXJBfA69J1MM-gAAFjhSj5vuL8k2ED41650j_HHBPzLQ/viewform" target="_blank" rel="noreferrer noopener">Open het formulier in een nieuw tabblad</a>.')+'\n\n'
 +p('Is het formulier hieronder leeg of gesloten? Dan loopt er op dit moment geen bestelronde.','fortius-merch-meta')+'\n\n'
 +'<!-- wp:html -->\n<div class="fortius-form-embed fortius-merch-form">\n<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScam6dXJBfA69J1MM-gAAFjhSj5vuL8k2ED41650j_HHBPzLQ/viewform?embedded=true" width="100%" height="1500" frameborder="0" marginheight="0" marginwidth="0" title="Merch bestellen" loading="lazy">Formulier laden…</iframe>\n</div>\n<!-- /wp:html -->')
order_form=order
countdown_closed=('<!-- wp:group {"metadata":{"name":"Merch-ronde gesloten","categories":["lskvfortius"]},"align":"full","className":"is-style-section-2 fortius-merch-countdown","style":{"spacing":{"padding":{"top":"28px","bottom":"28px"},"blockGap":"0","margin":{"top":"0","bottom":"0"}}}} -->\n'
 '<div class="wp-block-group alignfull is-style-section-2 fortius-merch-countdown" style="margin-top:0;margin-bottom:0;padding-top:28px;padding-bottom:28px"><!-- wp:group {"className":"fortius-section-inner"} -->\n<div class="wp-block-group fortius-section-inner">'
 +p('special drop','is-style-text-annotation')+'\n\n'+p('bestelronde gesloten','fortius-countdown__date')+'</div>\n<!-- /wp:group --></div>\n<!-- /wp:group -->')
IG='https://www.instagram.com/lskvfortius/'
MAIL='<a href="mailto:merchcommissie.lskvfortius@gmail.com">merchcommissie.lskvfortius@gmail.com</a>'
order_closed=section('Bestellen',5,
 p('bestellen','is-style-text-annotation')+'\n\n<!-- wp:heading -->\n<h2 class="wp-block-heading">de bestelronde is gesloten</h2>\n<!-- /wp:heading -->\n\n'
 +p('Bedankt voor je bestelling! De bestelronde van de special drop is afgesloten, dus er kunnen geen bestellingen of wijzigingen meer worden gedaan.')+'\n\n'
 +p('<strong>Betalen:</strong> heb je besteld? De MerchCo stuurt je een Tikkie voor je bestelling. Betaal die vóór de betaaldeadline, anders wordt je bestelling niet geplaatst.')+'\n\n'
 +p('Vragen over je bestelling? Mail de MerchCo via '+MAIL+'.')+'\n\n'
 +p('Houd onze <a href="'+IG+'" target="_blank" rel="noreferrer noopener">Instagram</a> in de gaten voor de volgende merch-ronde.'))
card_pat_plain=card('[Placeholder: Productnaam]')
card_pat_nosize=card('[Placeholder: Productnaam]',sizes=False)
card_pat_simple=card('[Placeholder: Productnaam]',sizes=False,images=1)

def qa(q,a):
    return '<!-- wp:details -->\n<details class="wp-block-details"><summary>%s</summary><!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph --></details>\n<!-- /wp:details -->'%(q,a)
FAQ=[('Wanneer kan ik merch bestellen?','Tijdens een bestelronde, via het formulier op deze pagina. De huidige special drop loopt t/m zondag 22 november.'),
 ('Tot wanneer kan ik bestellen of mijn bestelling wijzigen?','Tot de deadline van de ronde. Die is hard: daarna plaatst de MerchCo de bestelling bij de leverancier en zijn er geen bestellingen of wijzigingen meer mogelijk. Wil je vóór de deadline iets wijzigen? Mail de MerchCo via <a href="mailto:merchcommissie.lskvfortius@gmail.com">merchcommissie.lskvfortius@gmail.com</a>.'),
 ('Hoe betaal ik?','Na de deadline krijg je van de MerchCo een Tikkie voor je bestelling. Betaal die vóór de betaaldeadline. Betaal je niet op tijd, dan wordt je bestelling niet geplaatst.'),
 ('Kan ik mijn eigen naam laten zetten?','Ja, op de waterfles (gegraveerd) en de shaker (bedrukt) kun je een (bij)naam laten zetten. Dat kost niets extra. Het Fortius-logo zit er altijd op, ook als je geen naam kiest. Laat het veld in het formulier leeg als je geen naam wilt.'),
 ('Welke maat moet ik kiezen?','Het T-shirt en de joggingbroeken zijn er in XS t/m XXL. De sokken zijn er in maat 35–38, 39–42 en 43–46, en je kunt 1 tot 5 paar bestellen. Let op: het T-shirt heeft een oversized pasvorm. Wil je de pijpen van de wide leg joggingbroek recht laten vallen? Bestel dan je gebruikelijke maat. Wil je ze wijd? Bestel een maat groter. Twijfel je? Mail de MerchCo via <a href="mailto:merchcommissie.lskvfortius@gmail.com">merchcommissie.lskvfortius@gmail.com</a>.'),
 ('Wanneer krijg ik mijn bestelling?','[Placeholder: verwachte levertijd en waar je de bestelling ophaalt]')]
faq=section('Veelgestelde vragen',3,p('twijfels?','is-style-text-annotation')+'\n\n<!-- wp:heading -->\n<h2 class="wp-block-heading">veelgestelde vragen</h2>\n<!-- /wp:heading -->\n\n'
 +'<!-- wp:group {"className":"fortius-faq","style":{"spacing":{"blockGap":"24px"}}} -->\n<div class="wp-block-group fortius-faq">'+'\n\n'.join(qa(q,a) for q,a in FAQ)+'</div>\n<!-- /wp:group -->',gap='40px')
page=hero+'\n\n'+countdown_closed+'\n\n'+products+'\n\n'+order_closed+'\n'
patterns={'merch-countdown':('Merch – countdown naar volgende ronde',countdown_live),
 'merch-product':('Merch – product (kleuren + maten)',card_pat_plain),
 'merch-product-zonder-maten':('Merch – product (alleen kleuren)',card_pat_nosize),
 'merch-product-simpel':('Merch – product (geen varianten)',card_pat_simple),
 'merch-bestelformulier':('Merch – bestelformulier',order_form),
 'merch-faq':('Merch – veelgestelde vragen (niet op de pagina)',faq),
 'merch-kleurkiezer':('Merch – kleurkiezer (script, 1x per pagina)',picker)}
os.makedirs(os.path.join(ROOT,'src','patterns'),exist_ok=True);os.makedirs(os.path.join(ROOT,'dist','patterns'),exist_ok=True)
for slug,(title,c) in patterns.items():
    open(os.path.join(ROOT,'src','patterns',slug+'.html'),'w').write(c+'\n')
    json.dump({'__file':'wp_block','title':title,'content':c+'\n','syncStatus':'unsynced'},open(os.path.join(ROOT,'dist','patterns',slug+'.json'),'w'),ensure_ascii=False,indent=1)
open(os.path.join(ROOT,'src','content','merch-page.html'),'w').write(page)
print(len(page),{k:len(v[1]) for k,v in patterns.items()})
