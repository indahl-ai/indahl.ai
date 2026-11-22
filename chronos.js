// CHRONOS (indahl.ai/chronos). Source: indahl-ai/chronos.js; build_site.py copies it to the worker's public/chronos.js. External, not inline: the page CSP is default-src 'self'.
(function(){
'use strict';
var CALS=[
 {id:'gregory',name:'Gregorian',loc:''},
 {id:'buddhist',name:'Buddhist Era',loc:'th-TH'},
 {id:'islamic-umalqura',name:'Islamic, Umm al-Qura',loc:'ar-SA'},
 {id:'islamic-civil',name:'Islamic, civil',loc:'ar-EG'},
 {id:'hebrew',name:'Hebrew',loc:'he-IL'},
 {id:'persian',name:'Persian',loc:'fa-IR'},
 {id:'chinese',name:'Chinese',loc:'zh-CN'},
 {id:'dangi',name:'Korean',loc:'ko-KR'},
 {id:'indian',name:'Indian national',loc:'hi-IN'},
 {id:'ethiopic',name:'Ethiopian',loc:'am-ET'},
 {id:'coptic',name:'Coptic',loc:'ar-EG'},
 {id:'japanese',name:'Japanese',loc:'ja-JP'},
 {id:'roc',name:'Republic of China',loc:'zh-TW'}
];
var PALS=[
 {id:'ymd',ex:'YYYYMMDD',where:'ISO 8601 and much of East Asia',f:function(y,m,d){return y4(y)+p2(m)+p2(d);},show:function(y,m,d){return y4(y)+'-'+p2(m)+'-'+p2(d);}},
 {id:'mdy',ex:'MMDDYYYY',where:'United States',f:function(y,m,d){return p2(m)+p2(d)+y4(y);},show:function(y,m,d){return p2(m)+'/'+p2(d)+'/'+y4(y);}},
 {id:'dmy',ex:'DDMMYYYY',where:'Most of the world',f:function(y,m,d){return p2(d)+p2(m)+y4(y);},show:function(y,m,d){return p2(d)+'.'+p2(m)+'.'+y4(y);}},
 {id:'ymd2',ex:'YYMMDD',where:'Short year first',f:function(y,m,d){return p2(y%100)+p2(m)+p2(d);},show:function(y,m,d){return p2(y%100)+'-'+p2(m)+'-'+p2(d);}},
 {id:'mdy2',ex:'MMDDYY',where:'Short United States',f:function(y,m,d){return p2(m)+p2(d)+p2(y%100);},show:function(y,m,d){return p2(m)+'/'+p2(d)+'/'+p2(y%100);}},
 {id:'dmy2',ex:'DDMMYY',where:'Short day first',f:function(y,m,d){return p2(d)+p2(m)+p2(y%100);},show:function(y,m,d){return p2(d)+'.'+p2(m)+'.'+p2(y%100);}}
];
var TZN=['Imix','Ik’','Ak’b’al','K’an','Chikchan','Kimi','Manik’','Lamat','Muluk','Ok','Chuwen','Eb’','B’en','Ix','Men','K’ib’','Kab’an','Etz’nab’','Kawak','Ajaw'];
var HBN=['Pop','Wo’','Sip','Sotz’','Sek','Xul','Yaxk’in','Mol','Ch’en','Yax','Sak’','Keh','Mak','K’ank’in','Muwan','Pax','K’ayab','Kumk’u','Wayeb’'];
var GMT=584283;
function md(a,b){return ((a%b)+b)%b;}
function jdn(d){return Math.round(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())/864e5)+2440588;}
function maya(d){var n=jdn(d)-GMT,h=md(n+348,365);return {n:n,lc:[Math.floor(n/144000),Math.floor(md(n,144000)/7200),Math.floor(md(n,7200)/360),Math.floor(md(n,360)/20),md(n,20)].join('.'),tz:(md(n+3,13)+1)+' '+TZN[md(n+19,20)],hb:(h%20)+' '+HBN[Math.floor(h/20)],h:h,cr:md(n,18980)};}
function fromN(n){var u=new Date((n+GMT-2440588)*864e5);return day(u.getUTCFullYear(),u.getUTCMonth(),u.getUTCDate());}
function p2(n){return (n<10?'0':'')+n;}
function y4(n){return ('000'+n).slice(-4);}
function $(id){return document.getElementById(id);}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
var cache={};
function F(loc,cal,o){var k=loc+'|'+cal+'|'+JSON.stringify(o);if(!cache[k]){var x={};for(var i in o)x[i]=o[i];x.calendar=cal;cache[k]=new Intl.DateTimeFormat(loc,x);}return cache[k];}
function ok(cal){try{return new Intl.DateTimeFormat('en-US',{calendar:cal}).resolvedOptions().calendar===cal;}catch(e){return false;}}
function day(y,m,d){return new Date(y,m,d,12);}
function add(b,n){return day(b.getFullYear(),b.getMonth(),b.getDate()+n);}
function diff(a,b){return Math.round((Date.UTC(b.getFullYear(),b.getMonth(),b.getDate())-Date.UTC(a.getFullYear(),a.getMonth(),a.getDate()))/864e5);}
function midnight(d){return new Date(d.getFullYear(),d.getMonth(),d.getDate(),0,0,0);}
function rawParts(cal,d){var o={};F('en-US',cal,{year:'numeric',month:'long',day:'numeric',era:'short'}).formatToParts(d).forEach(function(p){o[p.type]=p.value;});o.order=F('en-US',cal,{month:'long',day:'numeric'}).formatToParts(d).filter(function(p){return p.type==='month'||p.type==='day';}).map(function(p){return p.value;}).join(' ');return o;}
function ykey(cal,d){var p=rawParts(cal,d);return (p.relatedYear||p.year||'')+'|'+(p.era||'');}
var LUNI={chinese:8,dangi:9};
function nmJDE(k){var T=k/1236.85,R=Math.PI/180,T2=T*T,T3=T2*T,T4=T3*T;
 var J=2451550.09766+29.530588861*k+0.00015437*T2-0.00000015*T3+0.00000000073*T4,E=1-0.002516*T-0.0000074*T2;
 var M=(2.5534+29.1053567*k-0.0000014*T2-0.00000011*T3)*R,Mp=(201.5643+385.81693528*k+0.0107582*T2+0.00001238*T3-0.000000058*T4)*R,F=(160.7108+390.67050284*k-0.0016118*T2-0.00000227*T3+0.000000011*T4)*R,O=(124.7746-1.56375588*k+0.0020672*T2+0.00000215*T3)*R,sn=Math.sin;
 J+=-0.4072*sn(Mp)+0.17241*E*sn(M)+0.01608*sn(2*Mp)+0.01039*sn(2*F)+0.00739*E*sn(Mp-M)-0.00514*E*sn(Mp+M)+0.00208*E*E*sn(2*M)-0.00111*sn(Mp-2*F)-0.00057*sn(Mp+2*F)+0.00056*E*sn(2*Mp+M)-0.00042*sn(3*Mp)+0.00042*E*sn(M+2*F)+0.00038*E*sn(M-2*F)-0.00024*E*sn(2*Mp-M)-0.00017*sn(O)-0.00007*sn(Mp+2*M)+0.00004*sn(2*Mp-2*F)+0.00004*sn(3*M)+0.00003*sn(Mp+M-2*F)+0.00003*sn(2*Mp+2*F)-0.00003*sn(Mp+M+2*F)+0.00003*sn(Mp-M+2*F)-0.00002*sn(Mp-M-2*F)-0.00002*sn(3*Mp+M)+0.00002*sn(4*Mp);
 var A=[[299.77,0.107408,0.000325],[251.88,0.016321,0.000165],[251.83,26.651886,0.000164],[349.42,36.412478,0.000126],[84.66,18.206239,0.00011],[141.74,53.303771,0.000062],[207.14,2.453732,0.00006],[154.84,7.30686,0.000056],[34.52,27.261239,0.000047],[207.19,0.121824,0.000042],[291.34,1.844379,0.00004],[161.72,24.198154,0.000037],[239.56,25.513099,0.000035],[331.55,3.592518,0.000023]];
 for(var i=0;i<A.length;i++)J+=A[i][2]*sn((A[i][0]+A[i][1]*k-(i===0?0.009173*T2:0))*R);
 return J;}
function fromJDN(j){var u=new Date((j-2440588)*864e5);return day(u.getUTCFullYear(),u.getUTCMonth(),u.getUTCDate());}
function nmDay(k,tz){return fromJDN(Math.floor(nmJDE(k)-69/86400+tz/24+0.5));}
function trueStart(s,tz){var k=Math.round((jdn(s)-2451550.09766)/29.530588861),best=null;for(var i=-1;i<=1;i++){var t=nmDay(k+i,tz);if(!best||Math.abs(diff(t,s))<Math.abs(diff(best,s)))best=t;}return best;}
function icuStart(cal,d){for(var i=0;i<32;i++){var x=add(d,-i);if(rawParts(cal,x).day==='1')return x;}return d;}
function icuNext(cal,s){for(var i=27;i<33;i++){var x=add(s,i);if(rawParts(cal,x).day==='1')return x;}return add(s,30);}
function luniParts(cal,d){var tz=LUNI[cal],s=icuStart(cal,d),t=trueStart(s,tz),base=s;
 if(diff(t,d)<0){base=icuStart(cal,add(s,-1));t=trueStart(base,tz);}
 else{var n=icuNext(cal,s),tn=trueStart(n,tz);if(diff(tn,d)>=0){base=n;t=tn;}}
 var r=rawParts(cal,add(base,14)),dd=diff(t,d)+1;r.day=String(dd);r.order=r.month+' '+dd;
 var eq=add(base,dd-1),ep=rawParts(cal,eq);r.eq=(ep.month===r.month&&ep.day===String(dd))?eq:null;return r;}
function parts(cal,d){return LUNI[cal]?luniParts(cal,d):rawParts(cal,d);}
function icuNextNY(cal,b){var k=ykey(cal,b);for(var i=1;i<=420;i++){var d=add(b,i);if(ykey(cal,d)!==k)return d;}return null;}
function icuLastNY(cal,b){var k=ykey(cal,b);for(var i=1;i<=420;i++){var d=add(b,-i);if(ykey(cal,d)!==k)return add(d,1);}return null;}
function nextNY(cal,b){if(!LUNI[cal])return icuNextNY(cal,b);var r=icuNextNY(cal,b),t=r&&trueStart(r,LUNI[cal]);if(t&&diff(b,t)<=0){r=icuNextNY(cal,r);t=r&&trueStart(r,LUNI[cal]);}return t;}
function lastNY(cal,b){if(!LUNI[cal])return icuLastNY(cal,b);var r=icuLastNY(cal,b),t=r&&trueStart(r,LUNI[cal]);if(t&&diff(t,b)<0){r=icuLastNY(cal,add(r,-1));t=r&&trueStart(r,LUNI[cal]);}return t;}
function yearLine(p){if(p.yearName)return 'Year '+p.yearName+' ('+p.relatedYear+')';return 'Year '+p.year+(p.era?' '+p.era:'');}
var greg=function(d,o){return F('en-US','gregory',o||{weekday:'short',year:'numeric',month:'short',day:'numeric'}).format(d);};
var today=day(new Date().getFullYear(),new Date().getMonth(),new Date().getDate());
var sel=today;
var nyRows=[];

function renderCards(){
 var h='';
 CALS.forEach(function(c){
  h+='<article class="chr-card'+(c.id==='gregory'?' is-hl':'')+'"><p class="label"><a href="#'+c.id+'">'+esc(c.name)+'</a></p>';
  if(!ok(c.id)){h+='<p class="chr-na">This browser has no data for this calendar.</p></article>';return;}
  var p=parts(c.id,sel),a=lastNY(c.id,sel),b=nextNY(c.id,sel);
  h+='<p class="chr-date">'+esc(p.order)+'</p><p class="chr-year">'+esc(yearLine(p))+'</p>';
  var nat='';if(c.loc)try{var nd=LUNI[c.id]?p.eq:sel;if(nd)nat=F(c.loc,c.id,{dateStyle:'long'}).format(nd);}catch(e){}
  if(nat)h+='<p class="chr-native" lang="'+c.loc+'" dir="auto">'+esc(nat)+'</p>';
  if(a&&b){var n=diff(a,sel)+1,len=diff(a,b);h+='<div class="chr-meter"><div class="chr-bar"><i data-w="'+(100*n/len).toFixed(1)+'"></i></div><p>Day '+n+' of '+len+'</p></div>';}
  h+='</article>';
 });
 var M=maya(sel);
 h+='<article class="chr-card"><p class="label"><a href="#maya">Maya</a></p><p class="chr-date">'+M.lc+'</p><p class="chr-year">'+esc(M.tz+' '+M.hb)+'</p><div class="chr-meter"><div class="chr-bar"><i data-w="'+(100*(M.h+1)/365).toFixed(1)+'"></i></div><p>Haab\u2019 day '+(M.h+1)+' of 365</p></div></article>';
 $('chr-grid').innerHTML=h;
 var bars=document.querySelectorAll('#chr-grid [data-w]');for(var bi=0;bi<bars.length;bi++)bars[bi].style.width=bars[bi].getAttribute('data-w')+'%';
 renderMaya();
 var s=sel.getTime()===today.getTime();
 $('chr-dek').textContent=(s?'Today, ':'')+greg(sel,{weekday:'long',year:'numeric',month:'long',day:'numeric'})+'. Each card gives the date, the year count and how far the day sits into that calendar’s year.';
}

function renderMaya(){
 var M=maya(sel);$('maya-lc').textContent=M.lc;$('maya-tz').textContent=M.tz;$('maya-hb').textContent=M.hb;$('maya-cr').textContent='Day '+(M.cr+1).toLocaleString('en-US');
 var T=maya(today),k=(Math.floor(T.n/7200)+1)*7200,b=(Math.floor(T.n/144000)+1)*144000,rows=[['Next k\u2019atun',k],['Next b\u2019ak\u2019tun',b],['Next Calendar Round',T.n-T.cr+18980]];
 $('maya-next').innerHTML=rows.map(function(r){var d=fromN(r[1]),m=maya(d);return '<tr><td>'+r[0]+'</td><td>'+m.lc+', '+esc(m.tz+' '+m.hb)+'<small>'+esc(greg(d))+'</small></td><td class="chr-cd" role="timer" data-t="'+midnight(d).getTime()+'"></td></tr>';}).join('');
}
function buildNY(){
 var now=new Date(),base=day(now.getFullYear(),now.getMonth(),now.getDate());
 nyRows=CALS.filter(function(c){return ok(c.id);}).map(function(c){var d=nextNY(c.id,base);return d?{c:c,d:d,t:midnight(d).getTime()}:null;}).filter(Boolean);
 var hd=add(base,365-maya(base).h);nyRows.push({c:{id:'maya',name:'Maya Haab\u2019'},d:hd,t:midnight(hd).getTime(),maya:1});
 nyRows.sort(function(x,y){return x.t-y.t;});
 $('chr-ny').innerHTML=nyRows.map(function(r,i){var p=r.maya?null:parts(r.c.id,r.d);return '<tr><td><a href="#'+r.c.id+'">'+esc(r.c.name)+'</a></td><td>'+(r.maya?'0 Pop':esc(p.order)+', '+esc(yearLine(p).replace(/^Year /,'')))+'<small>'+esc(greg(r.d))+'</small></td><td class="chr-cd" role="timer" id="ny'+i+'"></td></tr>';}).join('');
}
function cd(ms){if(ms<0)ms=0;var s=Math.floor(ms/1000),d=Math.floor(s/86400);s-=d*86400;var h=Math.floor(s/3600);s-=h*3600;var m=Math.floor(s/60);s-=m*60;return '<b>'+d+'</b> d <b>'+p2(h)+'</b> h <b>'+p2(m)+'</b> m <b>'+p2(s)+'</b> s';}

function isoWeek(d){var t=new Date(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate()));var wd=t.getUTCDay()||7;t.setUTCDate(t.getUTCDate()+4-wd);var y=t.getUTCFullYear();var w=Math.ceil(((t-Date.UTC(y,0,1))/864e5+1)/7);return y+'-W'+p2(w)+'-'+wd;}

function palOf(s){return s===s.split('').reverse().join('');}
function search(f,b,step){var d=add(b,step);for(var i=0;i<4000000;i++){var y=d.getFullYear();if(y>9999||y<1)return null;if(palOf(f(y,d.getMonth()+1,d.getDate())))return d;d=add(d,step);}return null;}
function renderPal(){
 var y=sel.getFullYear(),m=sel.getMonth()+1,d=sel.getDate(),isT=sel.getTime()===today.getTime();
 var rows='',tape='',hits=[],soon=null;
 PALS.forEach(function(P,i){
  var s=P.f(y,m,d),yes=palOf(s),nx=search(P.f,sel,1),lt=search(P.f,sel,-1);
  if(yes)hits.push(P.ex);
  if(nx&&(!soon||nx<soon.d))soon={d:nx,f:[P.ex]};else if(nx&&soon&&nx.getTime()===soon.d.getTime())soon.f.push(P.ex);
  tape+='<span'+(yes?' class="yes"':'')+'>'+s+'<em>'+P.ex+'</em></span>';
  var dd=function(x){return x?greg(x,{year:'numeric',month:'short',day:'numeric'}):'None found';};
  var ago=lt?'<small>'+diff(lt,sel)+' days before</small>':'';
  var nxt=nx?(isT?'<small class="chr-cd" role="timer" data-t="'+midnight(nx).getTime()+'"></small>':'<small>'+diff(sel,nx)+' days after</small>'):'';
  rows+='<tr><td>'+P.ex+'<small>'+esc(P.where)+'</small></td><td><code>'+P.show(y,m,d)+'</code></td><td class="'+(yes?'chr-yes':'chr-no')+'">'+(yes?'Palindrome':'Not a palindrome')+'</td><td>'+dd(lt)+ago+'</td><td>'+dd(nx)+nxt+'</td></tr>';
 });
 $('chr-pal').innerHTML=rows;$('chr-tape').innerHTML=tape;
 var who=isT?'Today':'This day';
 var v=hits.length?who+' reads the same backward as '+hits.join(' and ')+'.':who+' is not a palindrome in any of these formats.';
 if(soon)v+=' The next palindrome date is '+greg(soon.d,{weekday:'long',year:'numeric',month:'long',day:'numeric'})+', as '+soon.f.join(' and ')+'.';
 $('chr-verdict').textContent=v;
}

function tick(){
 var now=new Date();
 if(now.getDate()!==today.getDate()||now.getMonth()!==today.getMonth()){var was=sel.getTime()===today.getTime();today=day(now.getFullYear(),now.getMonth(),now.getDate());if(was){sel=today;setInput();renderCards();renderPal();}buildNY();upDay();renderMaya();}
 for(var i=0;i<nyRows.length;i++){var el=$('ny'+i);if(el)el.innerHTML=cd(nyRows[i].t-now.getTime());}
 var ts=document.querySelectorAll('[data-t]');for(var j=0;j<ts.length;j++)ts[j].innerHTML=cd(+ts[j].getAttribute('data-t')-now.getTime());
 $('up-unix').textContent=Math.floor(now.getTime()/1000).toLocaleString('en-US');
 $('up-jd').textContent=(now.getTime()/864e5+2440587.5).toFixed(5);
}
function upDay(){
 var n=diff(day(today.getFullYear(),0,1),today)+1,len=diff(day(today.getFullYear(),0,1),day(today.getFullYear()+1,0,1));
 $('up-doy').textContent=n;$('up-doy-s').textContent='Of '+len+' days in '+today.getFullYear()+', Gregorian, local time';
 $('up-iso').textContent=isoWeek(today);
}
function setInput(){$('chr-day').value=sel.getFullYear()+'-'+p2(sel.getMonth()+1)+'-'+p2(sel.getDate());}

$('chr-tz').textContent='Time zone: '+(Intl.DateTimeFormat().resolvedOptions().timeZone||'this device');
setInput();
$('chr-day').addEventListener('change',function(){var v=this.value.split('-');if(v.length!==3)return;var y=+v[0];if(!(y>=1900&&y<=2100))return;sel=day(y,+v[1]-1,+v[2]);renderCards();renderPal();tick();});
$('chr-today').addEventListener('click',function(){sel=today;setInput();renderCards();renderPal();tick();});
renderCards();buildNY();renderPal();upDay();tick();
setInterval(tick,1000);
})();
