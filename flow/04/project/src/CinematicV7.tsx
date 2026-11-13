import React from 'react';
import {Easing} from 'remotion';
const C={ink:'#12313A',paper:'#EAF0E8',mint:'#D5EDA1',blue:'#B6CFCD',amber:'#E7B38B',muted:'#A4BCC0'};
const clamp=(x:number)=>Math.max(0,Math.min(1,x));
const out=Easing.bezier(.18,1,.32,1),inout=Easing.bezier(.65,0,.35,1);
const p=(t:number,a:number,d=.6,e=inout)=>e(clamp((t-a)/d));
const l=(a:number,b:number,x:number)=>a+(b-a)*x;
const k=(t:number,ps:number[][])=>{if(t<=ps[0][0])return ps[0][1];for(let i=1;i<ps.length;i++)if(t<ps[i][0])return l(ps[i-1][1],ps[i][1],p(t,ps[i-1][0],ps[i][0]-ps[i-1][0]));return ps[ps.length-1][1]};
// A causal impact, finite envelope; unrelated objects do not share a perpetual spring.
const impact=(t:number,a:number,amp=1)=>{const u=t-a;return u<0||u>1.35?0:amp*Math.sin(u*12)*Math.exp(-u*4.8)*(1-p(u,1, .35))};
const T=({x=540,y=0,size=36,c=C.paper,children,...props}:any)=><text x={x} y={y} fill={c} fontSize={size} textAnchor="middle" {...props}>{children}</text>;
const Shadow=({x=0,y=0,rx=100,ry=18,o=.4}:any)=><ellipse cx={x} cy={y} rx={rx} ry={ry} fill="#031A24" opacity={o} filter="url(#soft7)"/>;
const Tile=({x=0,y=0,w=120,h=218,tone='blue',icon='',angle=0,sy=1}:any)=><g transform={`translate(${x} ${y}) rotate(${angle} ${w/2} ${h}) translate(0 ${h*(1-sy)}) scale(1 ${sy})`}>
 <rect x="9" y="8" width={w} height={h} rx="25" fill={`url(#${tone}Edge7)`}/>
 <rect width={w} height={h} rx="25" fill={`url(#${tone}7)`} stroke="#F0FFF52A" strokeWidth="1.5"/>
 <path d={`M12 51v-21q0 -18 19 -18h${w-65}`} fill="none" stroke="#FFFFFF85" strokeWidth="3" strokeLinecap="round"/>
 <path d={`M${w-9} 95v${h-130}q0 25 -22 25`} fill="none" stroke="#12333B22" strokeWidth="3" strokeLinecap="round"/>
 {icon&&<T x={w/2} y={h/2+16} size={44} c={C.ink}>{icon}</T>}
 </g>;
const Quote=({x=0,y=0,o=1,rot=0}:any)=><g opacity={o} transform={`translate(${x} ${y}) rotate(${rot})`}><Shadow x={7} y={106} rx={123} ry={16} o={.22}/><rect x="-125" y="-70" width="250" height="150" rx="48" fill="url(#blueEdge7)"/><rect x="-129" y="-82" width="250" height="150" rx="48" fill="url(#paper7)" stroke="#F4FFF866" strokeWidth="2"/><path d="M-109 -34q0 -29 32 -29h110" stroke="#FFFFFF99" strokeWidth="3" strokeLinecap="round" fill="none"/><T x="0" y="17" size={62} c={C.ink}>¥—</T></g>;
const Bell=({t}:any)=>{const a=impact(t,20.38,14);return <g transform={`rotate(${a} 0 -108)`}><Shadow y={163} rx={103} ry={17} o={.4}/><circle cy="-117" r="16" fill="url(#amber7)"/><path d="M-91 73C-66 40 -76 -44 -49 -76C-25 -108 29 -110 53 -75C75 -42 62 43 91 73Q104 89 81 99Q0 126 -81 99Q-104 89 -91 73Z" fill="url(#bell7)" stroke="#FFF6D533" strokeWidth="2"/><ellipse cy="94" rx="86" ry="21" fill="#9D7751"/><ellipse cy="89" rx="86" ry="16" fill="#F4D8A0"/><g transform={`rotate(${-a*.7} 0 85)`}><circle cy="114" r="19" fill="url(#amber7)"/></g><path d="M-35 -65q-26 29 -23 93" stroke="#FFF7DC99" strokeWidth="8" strokeLinecap="round" fill="none"/>{[-1,1].map(s=><path key={s} d={`M${s*125} -46q${s*24} 54 0 98`} fill="none" stroke={C.mint} strokeWidth="4" strokeLinecap="round" opacity={Math.abs(a)/14}/>)}</g>};
const Fridge=({t}:any)=>{const zoom=k(t,[[0,.84],[1.2,.88],[2.35,1.03],[3,1.03],[4.1,.9]]),leave=p(t,3.15,.95);return <g opacity={1-leave} transform={`translate(${540-leave*650} ${870+leave*25}) scale(${zoom}) rotate(${-leave*5})`}>
 <Shadow x={25} y={587} rx={280} ry={29}/><rect x="-232" y="-502" width="492" height="1050" rx="70" fill="url(#blueEdge7)"/><rect x="-256" y="-526" width="488" height="1048" rx="63" fill="url(#metal7)" stroke="#D9EBE84D" strokeWidth="2"/>
 <path d="M-230 -425v-42q0 -36 40 -36h296" stroke="#FFFFFFB3" strokeWidth="5" fill="none" strokeLinecap="round"/>
 <path d="M-246 143H225M-246 160H225M-7 -508V143" stroke="#3C646B" strokeWidth="5"/>
 <path d="M-33 -233v240M16 -233V7M-168 230h296" stroke="#456B73" strokeWidth="14" strokeLinecap="round"/><path d="M-36 -234v237M13 -234V3M-168 225h296" stroke="#E9F4EB" strokeWidth="4" strokeLinecap="round"/>
 <g opacity={1-p(t,2.35,.3)}><rect x="-136" y="-343" width="256" height="94" rx="25" fill="#183E49"/><T x="-8" y="-284" size={28}>型号 / MODEL</T><rect x="-148" y="-355" width="280" height="118" rx="34" fill="none" stroke={C.mint} strokeWidth="3" opacity={p(t,1.75,.35)}/></g>
 </g>};
const First=({t}:any)=>{const exit=p(t,7.55,.7);return <g opacity={1-exit}>
 <Fridge t={t}/>
 <g opacity={p(t,2.5,.4)*(1-p(t,6.25,.35))} transform={`translate(540 ${k(t,[[2.5,522],[3.7,422]])})`}><Shadow y={72} rx={244} ry={12} o={.25}/><rect x="-284" y="-55" width="568" height="110" rx="35" fill="url(#mint7)"/><T x="0" y="14" size={38} c={C.ink}>收藏夹指定款</T></g>
 {[0,1,2].map(i=>{const a=p(t,3.8+i*.13,.8,out),f=p(t,6.25,.7);const x=l(210+i*330,i===1?450:i===0?-350:1430,f),y=l(850,775,f)+(1-a)*160;const z=l(.93,i===1?1.75:.9,f),rot=l((i-1)*5,0,f)+impact(t,4.6+i*.13,(i-1)*2);return <g key={i} opacity={a} transform={`translate(${x} ${y}) rotate(${rot}) scale(${z})`}><Shadow y={434} rx={136} ry={19}/><rect x="-136" y="-245" width="278" height="626" rx="26" fill="#5D7B7E"/><rect x="-143" y="-256" width="278" height="625" rx="26" fill="url(#paper7)"/>
 <g opacity={1-p(t,7.45,.25)} fill={C.ink}><T x="-4" y="-201" size={24} c={C.ink}>{i===1&&f>.7?'当前核对项':'店铺报价单'}</T><T x="-4" y="-112" size={65} c={C.ink}>{String.fromCharCode(65+i)}</T><path d="M-112 -70h215" stroke="#8FA8A7" strokeWidth="2" strokeDasharray="4 6"/><g opacity={1-f}><T x="-4" y="8" size={29} c={C.ink}>同一款型号</T><T x="-4" y="62" size={26} c="#617C7E">报价待核实</T><path d="M-98 114H90M-98 139H45" stroke="#8EA7A4" strokeWidth="5" strokeLinecap="round"/><T x="-4" y="211" size={25} c={C.ink}>优惠与服务</T><path d="M-85 260H80" stroke="#56767A" strokeWidth="12" strokeDasharray="2 4 3 5"/></g></g></g>})}
 <g opacity={p(t,6.65,.28)} transform={`translate(${l(650,602,p(t,6.65,.65,out))} ${l(1200,1115,p(t,6.65,.65,out))}) rotate(${impact(t,7.05,1.3)})`}><Shadow y={146} rx={325} ry={24} o={.22}/><rect x="-330" y="-128" width="660" height="268" rx="48" fill="url(#mint7)"/><T x="0" y="-63" size={26} c="#5B7658">询问客服</T><T x="0" y="8" size={48} c={C.ink}>优惠和服务</T><T x="0" y="77" size={48} c={C.ink}>都算进去了吗？</T></g>
 </g>};
export const CinematicV7=({t}:{t:number})=>{
 const enter=p(t,7.75,.65),remove=p(t,8.75,1.15),join=p(t,13.25,1.05),day=p(t,16.5,.8),pass=p(t,20,.65);
 const bx=k(t,[[7.75,214],[9.95,214],[12.3,132],[14.65,175],[16.5,175],[17.35,300],[19.75,300],[20.85,125]]);
 const by=k(t,[[7.75,835],[10.15,835],[12.3,835],[14.65,835],[16.5,835],[17.35,1040],[19.75,1040],[20.85,1020]]);
 const scale=k(t,[[7.75,1.14],[10.15,1.14],[12.3,1.02],[14.65,1.04],[16.5,1.04],[17.35,.70],[19.75,.70],[20.85,.65]]);
 const recoil=impact(t,11.08,2.5)+impact(t,11.75,2.1);const groupAngle=k(t,[[7.75,-5],[10.15,-5],[12.6,0],[16.5,0],[17.35,0]])+recoil-impact(t,17.13,1.5);
 const spacing=l(156,132,join),first=p(t,17.2,.57,out),out1=p(t,18.4,.55),second=p(t,18.78,.58,out);
 return <svg width="1080" height="1620" viewBox="0 0 1080 1620" style={{position:'absolute',inset:0}}><defs>
 <filter id="soft7" x="-60%" y="-200%" width="220%" height="500%"><feGaussianBlur stdDeviation="15"/></filter>
 {Object.entries({blue:['#DFE9E0','#B6CECA','#84A6A8'],mint:['#EEF6CF','#D4E99C','#ABC576'],amber:['#F6DEBA','#E6B18A','#BD8667'],paper:['#FCFCF0','#E9ECDD','#D1DACA'],metal:['#F0F3E8','#B9CFCB','#71979B']}).map(([id,colors])=><linearGradient key={id} id={`${id}7`} x1="0" y1="0" x2=".9" y2="1"><stop stopColor={colors[0]}/><stop offset=".43" stopColor={colors[1]}/><stop offset="1" stopColor={colors[2]}/></linearGradient>)}
 {Object.entries({blue:['#7E9FA0','#385F6B'],mint:['#A8BF76','#698B56'],amber:['#CB9874','#8C6555']}).map(([id,colors])=><linearGradient key={id} id={`${id}Edge7`} x1="0" y1="0" x2="1" y2="1"><stop stopColor={colors[0]}/><stop offset="1" stopColor={colors[1]}/></linearGradient>)}
 <linearGradient id="bell7"><stop stopColor="#AF8B61"/><stop offset=".28" stopColor="#F7DEAD"/><stop offset=".6" stopColor="#E4BB80"/><stop offset="1" stopColor="#AE865B"/></linearGradient>
 <radialGradient id="halo7"><stop stopColor="#A2D0C8" stopOpacity=".16"/><stop offset="1" stopColor="#A2D0C8" stopOpacity="0"/></radialGradient>
 </defs>
 <ellipse cx="550" cy="870" rx="630" ry="730" fill="url(#halo7)"/>
 {t<8.3&&<First t={t}/>}
 <g opacity={enter}>
 <g opacity={day} transform={`translate(0 ${(1-day)*-55})`}>
 <path d="M338 490a202 202 0 0 1 404 0" fill="none" stroke="#B6CEC626" strokeWidth="3" strokeDasharray="3 14"/>
 <g transform={`translate(540 490) rotate(${p(t,18.03,.85)*180})`}><circle cx="-202" r="29" fill="url(#mint7)"/><circle cx="-202" r="43" fill="none" stroke="#DBEDAD22" strokeWidth="8"/><path d="M181 -27a31 31 0 1 0 31 49a31 31 0 0 1 -31 -49" fill={C.blue}/></g>
 <T y="473" size={70}>{t<18.47?'第 1 天':'次日'}</T><T y="538" size={27} c={C.muted}>时间推进示意</T><T y="625" size={31} c={C.mint} opacity={1-pass}>每天重新查价</T>
 <Quote x={l(915,565,first)-out1*580} y={l(716,820,first)-Math.sin(out1*Math.PI)*85+impact(t,17.73,10)} rot={l(-13,0,first)-out1*16+impact(t,17.73,2)} o={first*(1-out1)}/>
 <Quote x={l(915,565,second)} y={l(716,820,second)+impact(t,19.31,10)} rot={l(-13,0,second)+impact(t,19.31,2)} o={second*(1-p(t,20,.3))}/>
 {[17.83,19.41].map((a,i)=>{const v=p(t,a,.48),o=p(t,a,.12)*(1-p(t,a+.36,.22));return <g key={i} opacity={o} transform={`translate(${l(365,760,v)} ${984-Math.sin(v*Math.PI)*27}) rotate(${l(-14,10,v)})`}><circle r="42" fill="#D7F0B713" stroke={C.mint} strokeWidth="6"/><path d="M30 32l34 34" stroke={C.mint} strokeWidth="13" strokeLinecap="round"/></g>})}
 </g>
 <g transform={`translate(${bx} ${by+(1-enter)*90}) scale(${scale}) rotate(${groupAngle} 345 235)`}>
 <Shadow x={340} y={282} rx={l(280,340,join)} ry={22} o={.35}/>
 <g opacity={join}><rect x="-27" y="-24" width="712" height="284" rx="49" fill="#BAD9D414" stroke="#D0E3D049" strokeWidth="2"/><path d="M-11 28q0 -36 37 -36h587" fill="none" stroke="#DDECD977" strokeWidth="3" strokeLinecap="round"/></g>
 {[0,1,2].map(i=><g key={i}><Shadow x={i*spacing+65} y="231" rx="56" ry="8" o={.28}/><Tile x={i*spacing} y={-12*(1-join)*(i===1?1:0)+impact(t,11.08+i*.035,4)+impact(t,11.75+i*.035,3)} angle={impact(t,11.12+i*.04,-1.4)} icon={i===1?'¥':''}/></g>)}
 <g opacity={1-p(t,9.65,.38)} transform={`translate(${468+remove*85} ${k(t,[[8.3,0],[8.65,8],[8.8,8],[9.9,-345]])}) rotate(${remove*14} 60 150)`}><Tile tone="mint" icon="−"/><T x="60" y="-35" size={30} c={C.mint}>优惠</T></g>
 {[0,1].map(i=>{const a=10.35+i*.67,travel=p(t,a,.73,out),hit=a+.73;const tx=(3+i)*spacing;const y=-320*(1-travel)-Math.sin(travel*Math.PI)*38+impact(t,hit,9);return <g key={i} opacity={p(t,a,.2)}><Shadow x={tx+62} y="233" rx={l(86,57,travel)} ry={l(20,8,travel)} o={l(.03,.3,travel)}/><Tile x={tx+105*(1-travel)} y={y} tone="amber" angle={-10*(1-travel)+impact(t,hit,2.5)} sy={1-impact(t,hit,.024)} icon={i===0?'+':''}/></g>})}
 </g>
 <g opacity={1-p(t,16.5,.4)}><T y="308" size={26} c={C.muted}>构成示意 · 部件大小不代表金额比例</T><T y="482" size={34} c={C.amber} opacity={p(t,10.1,.3)*(1-p(t,13.25,.4))}>加入服务费用</T><T y="580" size={39} opacity={p(t,13.35,.4)}>支出估算</T><g opacity={p(t,14.5,.45)} transform={`translate(0 ${(1-p(t,14.5,.6,out))*18})`}><T y="1240" size={88} c={C.mint}>¥—</T><T y="1295" size={28} c={C.muted}>金额待核实</T></g></g>
 <g opacity={day}><T x={l(540,354,pass)} y="1285" size={35}>支出估算</T><T x={l(540,354,pass)} y="1333" size={26} c={C.muted}>构成示意 · 金额待核实</T>
 <g opacity={p(t,19.62,.3)}><g opacity={1-p(t,20.32,.42)}><path d={`M${260-pass*200} 1010v164q0 28 28 28h15`} fill="none" stroke={C.mint} strokeWidth="9" strokeLinecap="round"/><path d={`M${824+pass*85} 1010v164q0 28 -28 28h-15`} fill="none" stroke={C.mint} strokeWidth="9" strokeLinecap="round"/></g><T y="1462" size={31}>条件成立时，才提醒</T><T x="323" y="1520" size={29} c={C.mint}>同款需求</T><T x="741" y="1520" size={29} c={C.mint}>总支出 &lt; ¥4,500</T></g>
 <g opacity={pass} transform={`translate(${l(915,817,pass)} ${l(885,925,pass)}) scale(${l(.83,1,pass)})`}><Bell t={t}/></g>
 </g>
 </g></svg>;
};
