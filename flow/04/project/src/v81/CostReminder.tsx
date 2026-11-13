// OP09 adapts into persistent operand docking, with NO operand removal at the sum.
// N044 adapts into the same receipt scaling into a reminder condition. Original v8 is preserved.
import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {p,q,mix} from '../v8/theme';
import {Fridge} from '../v8/CostReminder';
import captions from '../v8/captions.json';
const ink='#EDF5F2',teal='#C0F279',muted='#9DAFB4',green='#1E3B31',peach='#3E2E24';
const T=({x=0,y=0,size=40,fill=ink,weight=600,anchor='start',children,...rest}:any)=><text x={x} y={y} fontSize={size} fill={fill} fontWeight={weight} textAnchor={anchor} {...rest}>{children}</text>;

// New semantic component: an old appliance inside a recycling loop, and a box ascending stairs.
export function ServiceTools({x,y,progress}:{x:number;y:number;progress:number}){return <g transform={`translate(${x} ${y})`}>
 <g><rect x="-10" y="-12" width="92" height="113" rx="24" fill="#604527" stroke="#A47B45" strokeWidth="2"/><rect x="22" y="10" width="31" height="47" rx="6" fill="#EDC28B"/><path d="M25 38h25M46 18v12" stroke="#604527" strokeWidth="3"/>
 <path d="M14 43C-5 68 43 92 63 62M62 62l-1 17M62 62l-18 4" fill="none" stroke="#FFD997" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"/></g>
 <g transform="translate(113 0)"><rect x="-10" y="-12" width="97" height="113" rx="24" fill="#604527" stroke="#A47B45" strokeWidth="2"/><path d="M0 80h23V59h23V38h23V17h12" stroke="#FFD997" strokeWidth="4" fill="none" strokeLinejoin="round"/><g transform={`translate(${progress*22} ${-progress*19})`}><rect x="4" y="19" width="30" height="32" rx="4" fill="#EDC28B"/><path d="M19 19v32" stroke="#604527" strokeWidth="3"/></g></g>
 </g>}

// C005: connected input branches resolve into one output flow. Paths follow actual operand positions.
export function CalculationRails({t,discountY,serviceY}:{t:number;discountY:number;serviceY:number}){
 const a=p(t,3.02,3.83),b=p(t,3.95,4.9),c=p(t,5.08,6.18);
 return <g fill="none" strokeLinecap="round" strokeLinejoin="round">
  <path d={`M928 558H981V${discountY}H940`} stroke="#92C76C" strokeWidth="4" pathLength="1" strokeDasharray="1" strokeDashoffset={1-a}/>
  <path d={`M940 ${discountY}H981V${serviceY}H940`} stroke="#F0B875" strokeWidth="4" pathLength="1" strokeDasharray="1" strokeDashoffset={1-b}/>
  <path d={`M940 ${serviceY}H981V1238H948`} stroke="#79E0E2" strokeWidth="5" pathLength="1" strokeDasharray="1" strokeDashoffset={1-c}/>
  {[{y:558,p:a,color:'#92C76C'},{y:discountY,p:a,color:'#92C76C'},{y:serviceY,p:b,color:'#F0B875'},{y:1238,p:c,color:'#79E0E2'}].map((v,i)=><circle key={i} cx={i===0?928:i===3?947:940} cy={v.y} r={5+v.p*3} fill={v.color} stroke="#091116" strokeWidth="2" opacity={v.p}/>)}
 </g>;
}

export function CostGather({t}:{t:number}){
 const minus=q(t,3.0,3.82),plus=q(t,3.9,4.88),sum=q(t,5.0633,6.4);
 const intro=p(t,.12,.65),svc=p(t,1.42,2.05);
 const paperY=mix(446,420,minus);
 const dx=mix(mix(-440,92,intro),145,minus),dy=mix(790,693,minus)-25*sum,dw=mix(465,790,minus),dh=mix(188,164,minus);
 const sx=mix(mix(1120,530,svc),145,plus),sy=mix(1068,900,plus)-31*sum,sw=mix(460,790,plus),sh=mix(212,206,plus);
 const headerY=mix(555,528,minus),fridgeScale=mix(.46,.41,minus);
 return <>
  {/* Persistent quote module; live input modules dock into a connected computation, without a full-page board. */}
  <rect x="100" y={paperY} width="880" height="225" rx="40" fill="url(#quoteMetal81)" stroke="#435058" strokeWidth="2" filter="url(#shadow81)"/>
  <Fridge x={147} y={mix(444,443,minus)} s={fridgeScale}/>
  <T x={305} y={headerY-26} size={26} weight={500} fill={muted}>收藏夹里的同一款冰箱</T>
  <T x={305} y={headerY+38} size={50} weight={900}>商品报价</T>
  <T x={878} y={headerY+36} size={27} anchor="end" fill={muted} weight={500}>按店铺询价</T>
  {/* Coupon remains the same g/rect/text nodes from loose ticket to subtraction operand. */}
  <g transform={`translate(${dx} ${dy})`}>
   <path d={`M27 0H${dw-27}Q${dw} 0 ${dw} 27V${dh*.37}A17 17 0 0 0 ${dw} ${dh*.63}V${dh-27}Q${dw} ${dh} ${dw-27} ${dh}H27Q0 ${dh} 0 ${dh-27}V${dh*.63}A17 17 0 0 0 0 ${dh*.37}V27Q0 0 27 0Z`} fill={green} stroke="#598D66" strokeWidth="2" filter="url(#smallShadow81)"/>
   <path d={`M98 23V${dh-23}`} stroke="#557862" strokeWidth="2" strokeDasharray="5 6"/>
   <T x={49} y={dh/2+22} size={68} anchor="middle" fill={teal}>−</T>
   <T x={131} y={mix(73,69,minus)} size={42} weight={900}>优惠</T>
   <T x={131} y={mix(128,122,minus)} size={27} fill={muted} weight={500}>从报价中扣除</T>
   <path d={`M${dw-75} ${dh/2-14}l-12 14 12 14M${dw-87} ${dh/2}h35`} stroke={teal} strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" fill="none" opacity={minus}/>
  </g>
  {/* Service is the same node while docking below discount; plus is a live arithmetic operator. */}
  <g transform={`translate(${sx} ${sy})`}>
   <rect width={sw} height={sh} rx="28" fill={peach} stroke="#9C734C" strokeWidth="2" filter="url(#smallShadow81)"/>
   <T x={49} y={sh/2+21} size={64} anchor="middle" fill="#FFD18A">+</T>
   <path d={`M98 25V${sh-25}`} stroke="#85613F" strokeWidth="2"/>
   <T x={131} y={64} size={39} weight={900}>服务费用</T>
   <T x={131} y={116} size={29} weight={500}>回收 · 上楼安装</T>
   <T x={131} y={163} size={24} fill="#D8B78F" weight={500}>具体收付以询价为准</T>
   <ServiceTools x={mix(275,sw-240,plus)} y={mix(-116,50,plus)} progress={plus}/>
  </g>
  {/* The sum is added BELOW the intact operands. No old-to-empty-to-new text switch. */}
  <CalculationRails t={t} discountY={dy+dh/2} serviceY={sy+sh/2}/>
  <clipPath id="resultReveal81"><rect x="133" y="1142" width="817" height={218*sum}/></clipPath>
  <g clipPath="url(#resultReveal81)">
   <rect x="145" y="1162" width="790" height="179" rx="29" fill="#CCEFA1" stroke="#DBFFB3" strokeWidth="2"/>
   <T x={174} y={1231} size={54} fill="#234327">=</T>
   <T x={240} y={1231} size={44} weight={900} fill="#17351F">预计总支出</T>
   <T x={240} y={1294} size={26} weight={500} fill="#46644C" opacity={1-p(t,8.8,9.03)}>以上三项，合在一起算</T>
   <clipPath id="budgetReveal81"><rect x="536" y="1168" width={380*p(t,9.12,9.7)} height="180"/></clipPath>
   <g clipPath="url(#budgetReveal81)"><T x={590} y={1231} size={48} fill="#234327" weight={900}>&lt; 4500 元</T></g>
   <T x={240} y={1294} size={26} fill="#46644C" weight={500} opacity={p(t,9.08,9.42)}>低于预算时提醒我</T>
  </g>
 </>;
}

export function ProductToReminder({t,children}:{t:number;children:React.ReactNode}){
 const handoff=q(t,8.8,9.72),scale=mix(1,.79,handoff),tx=mix(0,114,handoff),ty=mix(0,21,handoff);
 const panel=p(t,9.88,10.48),on=p(t,11.55,11.94),cursor=p(t,10.97,11.48),out=p(t,12.02,12.35),feedback=p(t,12,12.3);
 return <>
  <g transform={`translate(${tx} ${ty}) scale(${scale})`}>{children}</g>
  <g opacity={p(t,9.3,9.72)}><path d="M536 1095V1160" stroke="#9FBEB5" strokeWidth="3" strokeDasharray="5 7"/><T x={164} y={305} size={27} fill={muted} weight={500}>把这份总支出，作为提醒条件</T></g>
  <g clipPath="url(#settingsReveal81)">
   <rect x="166" y="1158" width="748" height="169" rx="36" fill="#1D282E" stroke="#3F535A" strokeWidth="2" filter="url(#smallShadow81)"/>
   <g transform="translate(201 1205)" stroke={teal} strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round"><rect width="63" height="61" y="8" rx="12"/><path d="M0 27h63M16 0v17M48 0v17M15 43h8M39 43h8M15 57h8"/></g>
   <T x={299} y={1229} size={42} weight={900}>每天查价</T><T x={299} y={1282} size={25} fill={muted} weight={500}>按这个条件检查</T>
   <rect x="723" y="1196" width="148" height="80" rx="40" fill={on>.5?teal:'#49545A'}/><circle cx={762+on*69} cy="1236" r="31" fill="#F7FFF5" filter="url(#smallShadow81)"/>
  </g>
  <clipPath id="settingsReveal81"><rect x="140" y="1132" width="800" height={235*panel}/></clipPath>
  <g opacity={cursor*(1-out)} transform={`translate(${mix(990,812,cursor)} ${mix(1430,1240,cursor)}) scale(${1-.1*Math.sin(on*Math.PI)})`}><path d="M0 0v58l16-15 14 30 13-6-15-29h24Z" fill={ink} stroke="white" strokeWidth="4" strokeLinejoin="round"/></g>
  <g clipPath="url(#feedbackReveal81)"><rect x="166" y="1366" width="748" height="118" rx="30" fill={green}/><T x={211} y={1418} size={34} fill={teal} weight={900}>✓ 查价提醒已设置</T><T x={211} y={1460} size={22} fill={muted} weight={500}>案例流程示意 · 非真实通知</T></g>
  <clipPath id="feedbackReveal81"><rect x="150" y="1352" width="785" height={153*feedback}/></clipPath>
 </>;
}

export function CostReminder(){
 const t=useCurrentFrame()/useVideoConfig().fps,c=captions.find(x=>t>=x.start&&t<x.end),focus=q(t,2.7,3.2),change=q(t,9.02,9.45);
 return <AbsoluteFill style={{background:'#090D11',fontFamily:'Eli MiSans',fontWeight:500,fontSynthesis:'none',color:ink,overflow:'hidden'}}>
  <svg width="1080" height="1560" viewBox="0 0 1080 1560"><defs>
   <filter id="shadow81" x="-25%" y="-25%" width="150%" height="165%"><feDropShadow dx="0" dy="18" stdDeviation="21" floodColor="#000000" floodOpacity=".55"/></filter>
   <filter id="smallShadow81" x="-30%" y="-40%" width="170%" height="190%"><feDropShadow dx="0" dy="7" stdDeviation="9" floodColor="#000000" floodOpacity=".6"/></filter>
   <linearGradient id="quoteMetal81" x1="0" y1="0" x2="1" y2="1"><stop stopColor="#34424A"/><stop offset="1" stopColor="#182026"/></linearGradient><filter id="blur8"><feGaussianBlur stdDeviation="10"/></filter><linearGradient id="fridge8" x1="0" y1="0" x2="1" y2=".8"><stop stopColor="#F0F4EF"/><stop offset=".45" stopColor="#C9DAD5"/><stop offset="1" stopColor="#99B7B4"/></linearGradient>
  </defs>
  <T x={100} y={129} size={25} fill={muted} weight={500}>公开案例 · 原创图解</T>
  <g opacity={1-p(t,8.8,9.0)} transform={`translate(0 ${-45*q(t,8.8,9.1)})`}><T x={100} y={mix(279,247,focus)} size={mix(65,48,focus)} weight={900}>把每一笔，都算清楚</T><T x={103} y={mix(347,307,focus)} size={29} weight={500} fill={muted}>报价 − 优惠 + 服务费用</T></g>
  <g opacity={change} transform={`translate(0 ${80*(1-change)})`}><T x={100} y={244} size={58} weight={900}>低于预算，就提醒我</T></g>
  <ProductToReminder t={t}><CostGather t={t}/></ProductToReminder>
  
  </svg>
  <div style={{position:'absolute',left:65,right:65,top:1575,height:195,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',textAlign:'center'}}>{c&&<><div style={{fontSize:42,lineHeight:1.4,fontWeight:600}}>{c.zh}</div><div style={{fontSize:25,lineHeight:1.4,marginTop:12,color:muted}}>{c.en}</div></>}</div>
  <div style={{position:'absolute',top:1815,left:88,right:88,fontSize:23,color:muted,display:'flex',justifyContent:'space-between'}}><span>ELI · AI 实用经验</span><span>图解示意 · 金额非报价</span></div>
 </AbsoluteFill>;
}
