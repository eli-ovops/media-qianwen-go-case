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

export const PhysicalWorldV3=({t}:any)=>{
 const enter=P(t,8,.65),discount=P(t,9.02,1.15),service=P(t,11.05,1.15),merge=P(t,13.12,1.42),daily=P(t,17.15,.65);
 const heroScale=L(1.13,.90,daily),heroY=L(875+discount*77-service*77+merge*90,930,daily);
 const stackY=1160+discount*43-service*43;
 const camera=1+Math.sin(P(t,8.0,1)*Math.PI)*.10;
 const dayAngle=L(-130,440,P(t,18.02,3.1));
 const phase=t<18.02?0:((t-18.02)/1.2)%1;
 const scanY=L(-435,218,phase);
 return <svg width="1080" height="1585" viewBox="0 0 1080 1585" style={{position:'absolute',inset:0,overflow:'hidden',opacity:enter}}>
 <defs>
  <linearGradient id="v3metal"><stop stopColor="#7D9AA4"/><stop offset=".17" stopColor="#C8D9D9"/><stop offset=".44" stopColor="#F0F2EB"/><stop offset="1" stopColor="#839EA8"/></linearGradient>
  <linearGradient id="v3side"><stop stopColor="#294E60"/><stop offset="1" stopColor="#133447"/></linearGradient>
  <linearGradient id="v3beam" x1="0" y1="0" x2="0" y2="1"><stop stopColor={lime} stopOpacity="0"/><stop offset="1" stopColor={lime} stopOpacity=".8"/></linearGradient>
  <clipPath id="v3clip"><path d="M-175 -405L135 -425 210 -382V170L135 205 -175 185Z"/></clipPath>
 </defs>
 <g transform={`translate(540 940) scale(${camera}) translate(-540 -940)`}>
  <ellipse cx="540" cy="1355" rx="445" ry="106" fill="#000B18" opacity=".25"/>
  <g transform={`translate(540 ${stackY})`} opacity={1-daily}>
   {[90,45,0].map((y,i)=><Disc key={i} y={y+merge*(45-y)} fill={cream} rx={310-merge*30}/>)}
   <g transform={`translate(${-discount*430} ${-45-discount*190}) rotate(${-discount*24})`} opacity={1-P(t,10.03,.4)}><Disc fill={lime}/></g>
   <g transform={`translate(${(1-service)*490} ${L(-250,-45,service)+merge*90})`} opacity={P(t,10.92,.2)}><Disc fill={orange} rx={310-merge*30}/></g>
  </g>
  <g opacity={daily}>
   <ellipse cx="540" cy="1277" rx="384" ry="108" fill="none" stroke="#618895" strokeWidth="3"/>
   <ellipse cx="540" cy="1277" rx="384" ry="108" fill="none" stroke={lime} strokeWidth="9" strokeDasharray="115 65" strokeDashoffset={-P(t,17.3,4)*430}/>
  </g>
  <g transform={`translate(${L(1080,530,enter)} ${heroY}) scale(${heroScale})`}>
   <Appliance/>
   <g clipPath="url(#v3clip)" opacity={daily*P(t,18,.2)}><rect x="-200" y={scanY-60} width="460" height="65" fill="url(#v3beam)"/><path d={`M-200 ${scanY}H260`} stroke={lime} strokeWidth="4"/></g>
  </g>
  <g opacity={P(t,8.68,.14)*(1-P(t,9.2,.18))} transform={`translate(${L(320,570,P(t,8.68,.52))} 1120)`}>
   <circle r="72" fill="#D8F87522" stroke={cream} strokeWidth="10"/>
   <path d="M50 50L103 103" stroke={cream} strokeWidth="18" strokeLinecap="round"/>
  </g>
  <g opacity={P(t,8.55,.3)*(1-P(t,9.04,.12))}><text x="540" y="1433" textAnchor="middle" fontSize="49" fill={cream}>从商品报价出发</text></g>
  <g opacity={P(t,9.18,.2)*(1-P(t,10.4,.18))}><text x="540" y="1433" textAnchor="middle" fontSize="49" fill={lime}>扣除适用优惠</text></g>
  <Truck t={t}/>
  <g opacity={P(t,10.65,.3)*(1-P(t,12.45,.3))}><text x="540" y="1433" textAnchor="middle" fontSize="49" fill={orange}>把服务费用计入</text></g>
  <g opacity={P(t,13.15,.35)*(1-P(t,17.1,.17))}>
   <ellipse cx="540" cy="1195" rx={L(425,350,merge)} ry={L(150,100,merge)} fill="none" stroke={lime} strokeWidth="4" strokeDasharray="12 12"/>
   <text x="540" y="1433" textAnchor="middle" fontSize="63" fill={cream}>总支出估算</text>
   <text x="540" y="1502" textAnchor="middle" fontSize="29" fill="#9CB6BD">金额待核实 · 图形不表示真实金额比例</text>
  </g>
  <g opacity={daily}>
   <circle cx="540" cy="872" r="402" fill="none" stroke="#708F9C" strokeWidth="3" strokeDasharray="3 18" opacity={1-P(t,20.15,.4)*.75}/>
   <g opacity={1-P(t,20.15,.4)*.8} transform={`translate(540 872) rotate(${dayAngle}) translate(0 -402) rotate(${-dayAngle})`}>
    <circle r="46" fill={lime}/>{Array.from({length:8},(_,i)=><path key={i} d="M0 -57V-73" transform={`rotate(${i*45})`} stroke={lime} strokeWidth="5" strokeLinecap="round"/>)}
   </g>
   <g opacity={1-P(t,20.15,.4)*.8} transform={`translate(540 872) rotate(${dayAngle+180}) translate(0 -402) rotate(${-dayAngle-180})`}>
    <path d="M25 -43A48 48 0 1 0 25 43A40 40 0 0 1 25 -43Z" fill="#A9C3D2"/>
   </g>
   <text x="540" y="378" textAnchor="middle" fontSize="59" fill={lime}>每天，再查一次</text>
   <text x="540" y="1440" textAnchor="middle" fontSize="42" fill={cream} opacity={P(t,17.35,.25)}>满足需求且总支出 &lt; ¥4,500，再提醒</text>
   <text x="540" y="1502" textAnchor="middle" fontSize="29" fill="#9CB6BD" opacity={P(t,17.35,.25)}>条件逻辑演示 · 非真实通知</text>
   <g opacity={P(t,20.05,.25)}>
    <path d="M729 1060Q875 1050 875 1180" fill="none" stroke={lime} strokeWidth="7" pathLength="1" strokeDasharray="1" strokeDashoffset={1-P(t,20.12,.5)}/>
    <text x="880" y="1018" textAnchor="middle" fontSize="29" fill={lime}>若条件成立</text>
    <g transform={`translate(875 1240) rotate(${Math.sin((t-20.65)*22)*9*P(t,20.65,.08)*(1-P(t,21.15,.35))})`} opacity={P(t,20.55,.2)}>
     <path d="M-47 19V-23A47 47 0 0 1 47 -23V19L61 40H-61Z" fill={lime}/><circle cy="55" r="12" fill={lime}/><path d="M0 -81V-70" stroke={lime} strokeWidth="10" strokeLinecap="round"/>
    </g>
   </g>
  </g>
 </g>
 </svg>;
};
