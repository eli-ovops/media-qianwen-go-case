import React from 'react';
const clamp=(x:number)=>Math.max(0,Math.min(1,x));
const P=(t:number,a:number,d:number)=>{const x=clamp((t-a)/d);return x*x*(3-2*x)};
const L=(a:number,b:number,p:number)=>a+(b-a)*p;
const cream='#E9EDE7',lime='#D8F875',orange='#F0A477',ink='#153241';

// A continuous object scene. All motion is derived from the sample frame.
const Appliance=()=> <g>
 <path d="M-175 -405L135 -425 210 -382V170L135 205 -175 185Z" fill="url(#v3side)"/>
 <path d="M-175 -405L135 -382V205L-175 185Z" fill="url(#v3metal)"/>
 <path d="M-175 -405L135 -382 210 -382 135 -425Z" fill="#DCEAEC"/>
 <path d="M-20 -394V-70M-175 -62L135 -41M-175 -53L135 -31" stroke="#315565" strokeWidth="4"/>
 <path d="M-34 -252V-103M-5 -251V-102M-124 15L88 30" stroke="#43697C" strokeWidth="11" strokeLinecap="round"/>
 <path d="M-30 -252V-108M-122 11L89 26" stroke="#E2F1ED" strokeWidth="3"/>
 <path d="M-165 -391L123 -370M-164 -387V-88" stroke="#FFFFFF" strokeWidth="3" opacity=".7"/>
 <path d="M-134 187V215M104 204V222" stroke="#0B1D26" strokeWidth="12"/>
 <path d="M159 -357V168" stroke="#90B2BD" strokeWidth="2" opacity=".4"/>
 <rect x="-127" y="-323" width="222" height="60" rx="5" fill={lime}/>
 <text x="-16" y="-284" fill={ink} textAnchor="middle" fontSize="24" fontWeight="600">收藏夹指定款</text>
</g>;

const Disc=({y=0,fill=cream,rx=310,opacity=1}:any)=><g transform={`translate(0 ${y})`} opacity={opacity}>
 <path d={`M${-rx} 0V35C${-rx} 100 ${rx} 100 ${rx} 35V0Z`} fill={fill}/>
 <path d={`M${-rx} 0V35C${-rx} 100 ${rx} 100 ${rx} 35V0Z`} fill="#062A3C" opacity=".25"/>
 <ellipse rx={rx} ry="65" fill={fill}/><ellipse rx={rx-12} ry="53" fill="none" stroke="#FFFFFF" strokeWidth="2" opacity=".25"/>
 {Array.from({length:15},(_,i)=><path key={i} d={`M${-rx+25+i*(rx*2-50)/14} 45v15`} stroke="#123B4C" strokeWidth="3" opacity=".2"/>)}
</g>;

const Truck=({t}:any)=>{const enter=P(t,10.35,.85),leave=P(t,12.08,.55),x=L(1140,705,enter)-leave*140;
 return <g opacity={enter*(1-leave)} transform={`translate(${x} 1090) scale(.85)`}>
  <ellipse cx="20" cy="178" rx="211" ry="28" fill="#000" opacity=".22"/>
  <path d="M-196 -112H62V137H-196Z" fill={orange}/><path d="M62 -112L100 -86V137H62Z" fill="#BC6F50"/>
  <path d="M100 -40H180L232 47V137H100Z" fill={cream}/><path d="M125 -17H166L201 40H125Z" fill="#275466"/>
  <path d="M-215 118H237V145H-215Z" fill="#5E7780"/>
  {[-140,175].map(x=><g key={x} transform={`translate(${x} 148) rotate(${-enter*240})`}><circle r="43" fill="#0E2431"/><circle r="22" fill="#94AFB3"/><path d="M-15 0H15M0 -15V15" stroke="#D9E4E0" strokeWidth="5"/></g>)}
  <g transform="translate(-72 7) rotate(-35)"><path d="M-10 60V-12C-55 -19 -40 -67 -16 -67V-40H16V-67C40 -62 48 -23 10 -12V60Z" fill={ink}/></g>
  <text x="-68" y="101" textAnchor="middle" fontSize="31" fill={ink}>搬旧 · 安装</text>
 </g>};

export const PhysicalWorldV4=({t}:any)=>{
 const enter=P(t,8,.65),discount=P(t,9.02,1.15),service=P(t,11.05,1.15);
 const merge=P(t,13.30,2.02),handoff=P(t,15.48,1.12),daily=P(t,16.92,.30);
 const stackY=1160+discount*43-service*43;
 const heroScale=L(1.13,.90,handoff),heroY=L(875+discount*77-service*77+merge*90,865,handoff);
 const coinX=L(540,777,handoff),coinY=L(stackY+45,1000,handoff),coinScale=L(1,.48,handoff);
 const face=P(t,16.0,.6),camera=1+Math.sin(P(t,8,1)*Math.PI)*.10;
 const quotePhase=(start:number)=>P(t,start,.55);
 const inspect1=P(t,17.72,.34)*(1-P(t,18.12,.12)),inspect2=P(t,18.75,.34)*(1-P(t,19.19,.12));
 const checks=P(t,19.25,.22),route1=P(t,19.40,.45),route2=P(t,19.92,.38),route3=P(t,20.44,.44);
 const lens=inspect1+inspect2,req=P(t,19.85,.10),budget=P(t,20.30,.10),bell=P(t,20.88,.14);
 return <svg width="1080" height="1585" viewBox="0 0 1080 1585" style={{position:'absolute',inset:0,overflow:'hidden',opacity:enter}}>
 <defs>
  <linearGradient id="v3metal"><stop stopColor="#7D9AA4"/><stop offset=".17" stopColor="#C8D9D9"/><stop offset=".44" stopColor="#F0F2EB"/><stop offset="1" stopColor="#839EA8"/></linearGradient>
  <linearGradient id="v3side"><stop stopColor="#294E60"/><stop offset="1" stopColor="#133447"/></linearGradient>
 </defs>
 <g transform={`translate(540 940) scale(${camera}) translate(-540 -940)`}>
  <ellipse cx="540" cy="1355" rx="445" ry="106" fill="#000B18" opacity={.25*(1-handoff)}/>
  <g transform={`translate(540 ${stackY})`} opacity={1-handoff}>
   {[90,45,0].map((y,i)=><Disc key={i} y={y+merge*(45-y)} fill={cream} rx={310-merge*30}/>)}
   <g transform={`translate(${-discount*430} ${-45-discount*190}) rotate(${-discount*24})`} opacity={1-P(t,10.03,.4)}><Disc fill={lime}/></g>
   <g transform={`translate(${(1-service)*490} ${L(-250,-45,service)+merge*90})`} opacity={P(t,10.92,.2)}><Disc fill={orange} rx={310-merge*30}/></g>
  </g>
  <g transform={`translate(${L(L(1080,530,enter),319,handoff)} ${heroY}) scale(${heroScale})`}><Appliance/></g>
  <g opacity={P(t,8.68,.14)*(1-P(t,9.2,.18))} transform={`translate(${L(320,570,P(t,8.68,.52))} 1120)`}>
   <circle r="72" fill="#D8F87522" stroke={cream} strokeWidth="10"/><path d="M50 50L103 103" stroke={cream} strokeWidth="18" strokeLinecap="round"/>
  </g>
  <g opacity={P(t,8.55,.3)*(1-P(t,9.04,.12))}><text x="540" y="1433" textAnchor="middle" fontSize="49" fill={cream}>从商品报价出发</text></g>
  <g opacity={P(t,9.18,.2)*(1-P(t,10.4,.18))}><text x="540" y="1433" textAnchor="middle" fontSize="49" fill={lime}>扣除适用优惠</text></g>
  <Truck t={t}/>
  <g opacity={P(t,10.65,.3)*(1-P(t,12.45,.3))}><text x="540" y="1433" textAnchor="middle" fontSize="49" fill={orange}>把服务费用计入</text></g>
  <g opacity={P(t,13.30,.25)*(1-handoff)}>
   <ellipse cx="540" cy="1195" rx={L(425,295,merge)} ry={L(170,95,merge)} fill="none" stroke={lime} strokeWidth="4" strokeDasharray="12 12"/>
  </g>
  <g opacity={P(t,14.82,.28)*(1-P(t,16.54,.2))}>
   <text x="540" y="1433" textAnchor="middle" fontSize="63" fill={cream}>总支出估算</text>
   <text x="540" y="1502" textAnchor="middle" fontSize="29" fill="#9CB6BD">金额待核实 · 图形不表示真实金额比例</text>
  </g>
  {/* The same merged disc leaves the base, turns face-on, and remains the check target. */}
  <g opacity={handoff} transform={`translate(${coinX} ${coinY}) scale(${coinScale})`}>
   <ellipse cy="30" rx="280" ry={L(75,263,face)} fill="#9F684E"/>
   <ellipse rx="280" ry={L(65,263,face)} fill={orange}/>
   <ellipse rx="251" ry={L(51,235,face)} fill={cream} opacity={face}/>
   {Array.from({length:20},(_,i)=><path key={i} d="M0 -250V-262" stroke="#835C49" strokeWidth="5" opacity={face*.55} transform={`rotate(${i*18})`}/>)}
   <text y="38" textAnchor="middle" fontSize="150" fontWeight="600" fill={ink} opacity={face}>¥—</text>
  </g>
  <g opacity={P(t,16.4,.2)}><text x="941" y="991" fontSize="36" fill={cream}>估算</text><text x="941" y="1034" fontSize="24" fill="#9CB6BD">待核实</text></g>
  {/* Two incoming quotes are observations; no actual price is asserted. */}
  {[17.18,18.24].map((start,i)=>{const q=quotePhase(start),fade=1-P(t,start+.62,.20);return <g key={i} opacity={P(t,start,.12)*fade} transform={`translate(777 ${L(565,989,q)}) scale(${L(.85,.34,q)}) rotate(${L(8,0,q)})`}>
   <path d="M-98 -124H98V115L80 130 63 115 46 130 29 115 12 130 -5 115 -22 130 -39 115 -56 130 -73 115 -98 130Z" fill={cream}/>
   <path d="M-64 -82H64M-64 -62H31" stroke="#96ADB0" strokeWidth="8"/>
   <text y="24" textAnchor="middle" fill={ink} fontSize="68">¥—</text>
   <path d="M-62 67H62" stroke={orange} strokeWidth="10"/>
  </g>})}
  <g opacity={daily*(1-P(t,19.2,.16))}>
   <text x="777" y="455" textAnchor="middle" fontSize="37" fill={lime}>每日查报价</text>
   <g transform={`translate(590 556)`}><circle r="39" fill="none" stroke="#8FAAB7" strokeWidth="4"/><path d="M0 0V-26M0 0H20" fill="none" stroke={cream} strokeWidth="4" transform={`rotate(${P(t,17.05,2.1)*720})`}/></g>
   <path d="M887 917Q1032 850 1000 687Q978 545 891 553" fill="none" stroke={lime} strokeWidth="5" pathLength="1" strokeDasharray="1" strokeDashoffset={1-P(t,18.02,.25)} opacity={P(t,18.02,.1)}/>
   <path d="M900 537L879 553 901 568" fill="none" stroke={lime} strokeWidth="5" opacity={P(t,18.2,.1)}/>
  </g>
  <g opacity={lens} transform={`translate(${L(700,800,Math.max(inspect1,inspect2))} 980)`}>
   <circle r="85" fill="#D8F87533" stroke={lime} strokeWidth="9"/><path d="M61 61L114 114" stroke={lime} strokeWidth="17" strokeLinecap="round"/>
  </g>
  {/* A causal signal goes from the checked estimate through two conditional gates. */}
  <g opacity={checks}>
   <text x="540" y="386" textAnchor="middle" fontSize="49" fill={lime}>若条件成立</text>
   <path d="M777 1137Q777 1190 528 1210L480 1235M558 1300H674M826 1300Q941 1300 941 1394" fill="none" stroke="#577581" strokeWidth="5"/>
   <path d="M777 1137Q777 1190 528 1210L480 1235" fill="none" stroke={lime} strokeWidth="9" pathLength="1" strokeDasharray="1" strokeDashoffset={1-route1}/>
   <path d="M558 1300H674" fill="none" stroke={lime} strokeWidth="9" pathLength="1" strokeDasharray="1" strokeDashoffset={1-route2}/>
   <path d="M826 1300Q941 1300 941 1394" fill="none" stroke={lime} strokeWidth="9" pathLength="1" strokeDasharray="1" strokeDashoffset={1-route3}/>
   {[[480,req,'需求满足'],[750,budget,'< ¥4,500']].map(([x,p,label]:any)=><g key={x} transform={`translate(${x} 1300)`}>
    <circle r="75" fill={ink} stroke={p>0?lime:'#8CA7B3'} strokeWidth="7"/>
    <path d="M-30 0L-7 23 35 -25" fill="none" stroke={lime} strokeWidth="12" strokeLinecap="round" strokeLinejoin="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p}/>
    <circle r="9" fill="#8CA7B3" opacity={1-p}/>
    <text y="125" textAnchor="middle" fontSize="36" fill={cream}>{label}</text>
   </g>)}
   <g transform={`translate(941 1438) rotate(${Math.sin((t-20.95)*23)*9*bell*(1-P(t,21.4,.25))})`} opacity={bell}>
    <path d="M-39 15V-22A39 39 0 0 1 39 -22V15L51 34H-51Z" fill={lime}/><circle cy="47" r="10" fill={lime}/><path d="M0 -69V-60" stroke={lime} strokeWidth="9" strokeLinecap="round"/>
   </g>
  </g>
  <text x="540" y="1540" textAnchor="middle" fontSize="29" fill="#9CB6BD" opacity={daily}>报价与条件逻辑示意 · 非真实通知</text>
 </g></svg>;
};

