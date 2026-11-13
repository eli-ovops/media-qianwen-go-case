// Adapted: new30-op09/OP09 (objects converge into a continuous main carrier), library-new10-n044/MediaScenesB N044 (same product shrinks into foreground input). Eli content, geometry, audio are independent.
import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {p,q,mix,springAt,clamp} from './theme';
import captions from './captions.json';
const ink='#183A40',teal='#1B746A',mint='#DFF1E2',muted='#6B8082';
const Text=({x=0,y=0,size=40,fill=ink,weight=600,anchor='start',children,...rest}:any)=><text x={x} y={y} fontSize={size} fill={fill} fontWeight={weight} textAnchor={anchor} {...rest}>{children}</text>;
const check=(x:number,y:number,k:number)=><path d={`M${x} ${y}l11 12 24-28`} fill="none" stroke={teal} strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1-k}/>;
export function Fridge({x,y,s=1}:{x:number;y:number;s?:number}){return <g transform={`translate(${x} ${y}) scale(${s})`}>
 <ellipse cx="131" cy="362" rx="126" ry="17" fill="#1A393D" opacity=".12" filter="url(#blur8)"/>
 <rect x="10" y="7" width="238" height="345" rx="32" fill="#8FABA7"/><rect width="236" height="345" rx="30" fill="url(#fridge8)" stroke="#FFFFFF" strokeWidth="2"/>
 <path d="M13 228H228M117 12V227" stroke="#7C9795" strokeWidth="3"/>
 <path d="M94 98v77M141 98v77M64 267h112" stroke="#728E8B" strokeWidth="8" strokeLinecap="round"/><path d="M92 98v75M139 98v75M64 265h112" stroke="#FBFFFC" strokeWidth="2.5" strokeLinecap="round"/>
 <path d="M17 64V39q0-23 23-23h152" stroke="#FFFFFFBB" strokeWidth="4" fill="none" strokeLinecap="round"/>
 <rect x="155" y="39" width="52" height="28" rx="8" fill={ink}/><path d="M169 53h24" stroke="#C5E4CB" strokeWidth="3" strokeLinecap="round"/>
 </g>}
function Coupon({x,y}:{x:number;y:number}){return <g transform={`translate(${x} ${y})`}>
 <path d="M24 0H326Q350 0 350 24V48A18 18 0 0 0 350 84V108Q350 132 326 132H24Q0 132 0 108V84A18 18 0 0 0 0 48V24Q0 0 24 0Z" fill={mint} filter="url(#shadow8)"/>
 <path d="M90 18V114" stroke="#88B9A0" strokeWidth="2" strokeDasharray="5 6"/><Text x={46} y={83} anchor="middle" size={57} fill={teal}>−</Text><Text x={120} y={59} size={35}>优惠</Text><Text x={120} y={99} size={23} weight={500} fill={muted}>从报价中扣除</Text>
 </g>}
function Service({x,y}:{x:number;y:number}){return <g transform={`translate(${x} ${y})`}>
 <rect width="470" height="150" rx="28" fill="#F4E5D6" filter="url(#shadow8)"/>
 <g transform="translate(28 29)" fill="none" stroke="#947258" strokeWidth="4" strokeLinejoin="round" strokeLinecap="round"><path d="M0 78h24V55h24V32h24V9h18"/><path d="M22 38V4h29v34zM36 4v34"/><path d="M81 62V34m-10 12 10-12 10 12"/></g>
 <Text x={150} y={54} size={32}>服务费用</Text><Text x={150} y={95} size={25} weight={500}>回收 · 上楼安装</Text><Text x={150} y={128} size={20} weight={500} fill="#927B69">具体收付以询价为准</Text>
 </g>}
// OP09: the primary carrier persists while secondary items converge; no new page at the seam.
export function CostGather({t}:{t:number}){
 const gather=q(t,5.1,6.35),exit=q(t,8.8,9.65),discount=p(t,.18,.95),service=p(t,1.45,2.25);
 const ledgerY=mix(790,835,gather),carrierY=mix(445,410,exit),carrierH=mix(885,1090,exit);
 return <>
 <rect x="82" y={carrierY} width="916" height={carrierH} rx="42" fill="white" filter="url(#shadow8)"/>
 <g opacity={1-p(t,8.8,9.03)}><Text x={402} y={531} size={25} fill={muted} weight={500}>收藏夹指定款</Text><Text x={400} y={603} size={57}>商品报价</Text><Text x={400} y={659} size={24} weight={500} fill={muted}>把优惠与服务都算进去</Text></g>
 <g opacity={1-gather}><path d={`M154 ${ledgerY-45}H924`} stroke="#DDE7E3" strokeWidth="2"/><Text x={152} y={ledgerY+21} size={36}>报价</Text><Text x={906} y={ledgerY+21} size={35} anchor="end" fill={muted}>按店铺询价</Text></g>
 <g opacity={1-exit}>
  <g transform={`translate(${mix(mix(-390,150,discount),519,gather)} ${mix(910,1059,gather)}) scale(${mix(1,.12,gather)})`} opacity={1-p(t,5.8,6.02)}><Coupon x={0} y={0}/></g>
  <g transform={`translate(${mix(mix(1095,420,service),512,gather)} ${mix(1088,1058,gather)}) scale(${mix(1,.12,gather)})`} opacity={1-p(t,5.8,6.02)}><Service x={0} y={0}/></g>
  <g opacity={discount*(1-gather)}><Text x={879} y={986} size={66} anchor="end" fill={teal}>−</Text><path d="M156 1058H913" stroke="#E6EBE9" strokeWidth="2"/></g>
  <g opacity={service*(1-gather)}><Text x={178} y={1184} size={66} fill="#9C704C">+</Text></g>
  <path d="M145 825V1235H917" fill="none" stroke={teal} strokeWidth="5" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(t,3.05,4.35)} opacity={.52*(1-gather)}/>
  <g opacity={p(t,4.35,4.85)*(1-gather)}>{check(920,1222,p(t,4.4,4.85))}</g>
 </g></>;
}
// N044: attachment and input lift overlap. Keep the product rather than replacing it with an icon at the seam.
export function ProductToReminder({t}:{t:number}){
 const sum=p(t,6.05,6.5),attach=q(t,8.8,9.65),form=p(t,9.18,9.82),enabled=p(t,11.68,12.05),settle=springAt(t,12.04,.62);
 const fx=mix(144,145,attach),fy=mix(355,478,attach),fs=mix(1,.46,attach),totalY=mix(930,588,attach),titleSize=mix(62,39,attach);
 const move=p(t,11.07,11.62),cursorOut=p(t,12.13,12.48),press=p(t,11.61,11.72)*(1-p(t,11.76,11.88));
 return <><Fridge x={fx} y={fy} s={fs}/>
 <g opacity={sum}><Text x={mix(540,642,attach)} y={totalY-65} size={25} weight={500} anchor="middle" fill={muted}>同一款冰箱</Text><Text x={mix(540,642,attach)} y={totalY+13} size={titleSize} weight={900} anchor="middle">预计总支出</Text>
  <g opacity={1-attach}><rect x="145" y="1017" width="790" height="103" rx="32" fill={ink}/><Text x={540} y={1083} size={37} anchor="middle" fill="white" weight={500}>商品报价 <tspan fill="#A5D8AD">− 优惠</tspan> + 服务费用</Text><Text x={540} y={1194} size={27} anchor="middle" weight={500} fill={muted}>按询价结果给出总价估算</Text></g>
 </g>
 <g opacity={form} transform={`translate(0 ${mix(72,0,form)})`}>
  <path d="M145 716H935" stroke="#DDE7E3" strokeWidth="2"/><Text x={149} y={790} size={28} weight={500} fill={muted}>提醒条件</Text><Text x={149} y={886} size={54} weight={900}>总支出 <tspan fill={teal}>&lt; 4500 元</tspan></Text><Text x={149} y={947} size={27} weight={500} fill={muted}>含优惠及相关服务费用</Text>
  <g opacity={p(t,10.1,10.58)}><path d="M145 998H935" stroke="#DDE7E3" strokeWidth="2"/>
   <g transform="translate(149 1043)" stroke={teal} strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round"><rect width="67" height="65" y="10" rx="13"/><path d="M0 31h67M17 0v20M50 0v20M16 47h9M41 47h9M16 61h9"/></g>
   <Text x={252} y={1096} size={41}>每天查价</Text><Text x={252} y={1143} size={24} fill={muted} weight={500}>达到条件时提醒我</Text><rect x="754" y="1051" width="158" height="86" rx="43" fill={enabled>.5?teal:'#DCE4E1'}/><circle cx={797+enabled*73} cy="1094" r="33" fill="white" filter="url(#toggle8)"/>
  </g>
  <g opacity={p(t,12.05,12.35)} transform={`translate(0 ${(1-settle)*12})`}><rect x="149" y="1224" width="764" height="151" rx="28" fill={mint}/>
   <g transform={`translate(194 1280) rotate(${(1-settle)*10} 18 -10)`}><path d="M0 24c9-13 4-33 14-43 10-11 30-8 36 5 5 10 1 26 10 38Z" stroke={teal} strokeWidth="4" fill="none" strokeLinejoin="round"/><path d="M21 33q10 14 19 0" fill="none" stroke={teal} strokeWidth="4" strokeLinecap="round"/></g><Text x={286} y={1285} size={38} fill={teal}>查价提醒已设置</Text><Text x={286} y={1334} size={24} weight={500} fill={muted}>案例流程示意 · 非真实通知</Text>
  </g>
 </g>
 <g opacity={move*(1-cursorOut)} transform={`translate(${mix(1030,848,move)} ${mix(1314,1095,move)}) scale(${1-.12*press})`}><path d="M0 0v62l16-16 15 33 15-7-16-31h27Z" fill={ink} stroke="white" strokeWidth="4" strokeLinejoin="round" filter="url(#toggle8)"/></g>
 {t>11.68&&t<12.15&&<circle cx="850" cy="1094" r={mix(20,74,clamp((t-11.68)/.47))} stroke={teal} strokeWidth="3" fill="none" opacity={1-clamp((t-11.68)/.47)}/>}
 </>;
}
export function CostReminder(){const t=useCurrentFrame()/useVideoConfig().fps;const c=captions.find(x=>t>=x.start&&t<x.end);return <AbsoluteFill style={{background:'#FCFDFC',fontFamily:'Eli MiSans',fontWeight:500,fontSynthesis:'none',color:ink,overflow:'hidden'}}>
 <svg width="1080" height="1560" viewBox="0 0 1080 1560" style={{position:'absolute',inset:0}}><defs><filter id="shadow8" x="-30%" y="-35%" width="165%" height="185%"><feDropShadow dx="0" dy="16" stdDeviation="12.5" floodColor="#163737" floodOpacity=".1333333333"/></filter><filter id="toggle8" x="-80%" y="-80%" width="260%" height="260%"><feDropShadow dx="0" dy="4" stdDeviation="4" floodOpacity=".18"/></filter><filter id="blur8"><feGaussianBlur stdDeviation="10"/></filter><linearGradient id="fridge8" x1="0" y1="0" x2="1" y2=".8"><stop stopColor="#F0F4EF"/><stop offset=".45" stopColor="#C9DAD5"/><stop offset="1" stopColor="#99B7B4"/></linearGradient></defs>
 <Text x={88} y={175} size={26} fill={muted} weight={500}>公开案例 · 原创图解</Text><Text x={88} y={267} size={57} weight={900}>这款冰箱，最后一共花多少？</Text><CostGather t={t}/><ProductToReminder t={t}/></svg>
 <div style={{position:'absolute',left:65,right:65,top:1575,height:195,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',textAlign:'center'}}>{c&&<><div style={{fontSize:42,lineHeight:1.4,fontWeight:600}}>{c.zh}</div><div style={{fontSize:25,lineHeight:1.4,marginTop:12,color:muted}}>{c.en}</div></>}</div><div style={{position:'absolute',top:1815,left:88,right:88,fontSize:23,color:muted,display:'flex',justifyContent:'space-between'}}><span>ELI · AI 实用经验</span><span>图解示意 · 金额非报价</span></div>
 </AbsoluteFill>}
