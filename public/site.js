(function(){
  var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
  var esc=function(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})};
  $$('.yr').forEach(function(e){var y=new Date().getFullYear();if(y>2026)e.textContent=y});
  // centre the current building in the scrolling building bar
  var cur=$('.bn a[aria-current]');if(cur){var p=cur.parentNode;if(p.scrollWidth>p.clientWidth)p.scrollLeft=cur.offsetLeft-p.clientWidth/2+cur.clientWidth/2}
  // home slideshow
  var hs=$$('.hero-show img');
  if(hs.length>1&&!matchMedia('(prefers-reduced-motion: reduce)').matches){var k=0;setInterval(function(){
    var nx=(k+1)%hs.length,go=function(){hs[k].classList.remove('on');hs[nx].classList.add('on');k=nx};
    if(hs[nx].complete&&hs[nx].naturalWidth)go();else{hs[nx].loading='eager';hs[nx].onload=go}},5500)}
  // lightbox
  function lightbox(list,i){
    var bx=document.createElement('div');bx.className='lbx';bx.setAttribute('role','dialog');bx.setAttribute('aria-modal','true');
    bx.innerHTML='<img alt=""><button class="x" type="button" aria-label="閉じる">×</button>'+(list.length>1?'<button class="p" type="button" aria-label="前">‹</button><button class="n" type="button" aria-label="次">›</button>':'');
    var im=$('img',bx),x0=null;function show(j){i=(j+list.length)%list.length;im.src=list[i].src;im.alt=list[i].alt||''}
    function close(){bx.remove();removeEventListener('keydown',kd)}
    function kd(e){if(e.key==='Escape')close();if(e.key==='ArrowRight')show(i+1);if(e.key==='ArrowLeft')show(i-1)}
    bx.addEventListener('click',function(e){var c=e.target.classList;if(e.target===bx||c.contains('x'))close();else if(c.contains('p'))show(i-1);else if(c.contains('n'))show(i+1)});
    bx.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
    bx.addEventListener('touchend',function(e){if(x0===null)return;var d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>40)show(i+(d<0?1:-1));x0=null});
    addEventListener('keydown',kd);document.body.appendChild(bx);show(i);$('.x',bx).focus();
  }
  // gallery
  $$('.gallery').forEach(function(g){
    var sl=$$('.stage img',g),th=$$('.th',g),cn=$('.cur',g),c=0;
    function go(i){c=(i+sl.length)%sl.length;sl.forEach(function(s,n){s.classList.toggle('on',n===c);if(Math.abs(n-c)<=1)s.loading='eager'});
      th.forEach(function(t,n){t.classList.toggle('on',n===c)});if(cn)cn.textContent=c+1;
      var t=th[c],tb=$('.thumbs',g);if(t&&tb)tb.scrollLeft=t.offsetLeft-tb.clientWidth/2+t.clientWidth/2}
    $('.prev',g).onclick=function(){go(c-1)};$('.next',g).onclick=function(){go(c+1)};
    th.forEach(function(t,n){t.onclick=function(){go(n)}});
    var st=$('.stage',g),x0=null;
    st.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
    st.addEventListener('touchend',function(e){if(x0===null)return;var d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>40)go(c+(d<0?1:-1));x0=null});
    sl.forEach(function(s,n){s.onclick=function(){lightbox(sl.map(function(x){return {src:x.src,alt:x.alt}}),n)}});
    if(sl.length<2)$$('.nav,.count',g).forEach(function(b){b.hidden=true});
  });
  var lbs=$$('a.lb');lbs.forEach(function(a,n){a.onclick=function(e){e.preventDefault();lightbox(lbs.map(function(x){return {src:x.href,alt:$('img',x).alt}}),n)}});
  // vacancies: everything is rendered from /vacancies.json so updates need only that file
  var vb=$('#vblocks'),vr=$('#vrows');
  if((vb||vr)&&window.fetch){fetch('/vacancies.json',{cache:'no-cache'}).then(function(r){return r.ok?r.json():null}).then(function(v){if(!v)return;
    $$('.js-asof').forEach(function(e){e.textContent=v.updated});
    if(vr){var rows=[];v.buildings.forEach(function(b){b.units.forEach(function(u){rows.push('<li><a href="'+esc(u.pdf)+'" target="_blank" rel="noopener" aria-label="'+esc(b.name+' '+u.room)+' 物件資料（PDF）"><span class="vr-b">'+esc(b.name)+'</span><span class="vr-r">'+esc(u.room)+'</span><span class="vr-a">'+esc(u.area)+'</span><span class="vr-p">'+esc(u.rent)+'</span><span class="vr-n">'+esc(u.badge)+'</span><span class="arr" aria-hidden="true">↗</span></a></li>')})});
      vr.innerHTML=rows.length?rows.join(''):'<li class="none">ただいま募集中の住戸はございません。</li>'}
    if(vb){vb.innerHTML=v.buildings.map(function(b){
      var us=b.units.length?b.units.map(function(u){return '<a class="unit" href="'+esc(u.pdf)+'" target="_blank" rel="noopener"><img src="'+esc(u.flyer)+'" alt="'+esc(b.name+' '+u.room)+' 物件資料" loading="lazy"><span class="u-t"><span class="u-room">'+esc(u.room)+'</span><span class="u-badge">'+esc(u.badge)+'</span><span class="u-row"><span class="u-k">専有面積</span>'+esc(u.area)+'</span><span class="u-row"><span class="u-k">賃料（税込）</span>'+esc(u.rent)+'</span><span class="u-pdf">物件資料 PDF <span aria-hidden="true">↗</span></span></span></a>'}).join(''):'<p class="full">ただいま満室となっております</p>';
      return '<section class="row" id="'+esc(b.slug)+'"><div class="lab vb-h"><a href="/'+esc(b.slug)+'"><span class="vb-jp">'+esc(b.name)+'</span><span>'+esc(b.en)+'</span></a></div><div class="row-c"><p class="tag">'+b.tagline.map(esc).join('<br>')+'</p><div class="units">'+us+'</div><iframe class="map" title="'+esc(b.name)+' 地図" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q='+encodeURIComponent(b.address)+'&z=16&output=embed"></iframe></div></section>'}).join('');
      if(location.hash){var t=document.getElementById(location.hash.slice(1));if(t)t.scrollIntoView()}}
  }).catch(function(){})}
})();
