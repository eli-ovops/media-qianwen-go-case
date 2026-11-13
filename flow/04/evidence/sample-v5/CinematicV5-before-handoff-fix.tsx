import React from 'react';
const C=(v:number)=>Math.max(0,Math.min(1,v));
const P=(t:number,a:number,d:number)=>{let v=C((t-a)/d);return v*v*(3-2*v)};
const L=(a:number,b:number,p:number)=>a+(b-a)*p;
const K=(t:number,keys:number[][])=>{if(t<=keys[0][0])return keys[0][1];for(let i=1;i<keys.length;i++)if(t<keys[i][0])return L(keys[i-1][1],keys[i][1],P(t,keys[i-1][0],keys[i][0]-keys[i-1][0]));return keys[keys.length-1][1]};
const paper='#F1EDDE',ink='#193743',lime='#D8F875',orange='#ED9567';

const Sheet=({estimate=false,service=0,discount=0}:any)=><g>
 <path d={`M-270 -380H270V${380-discount*85}L245 ${365-discount*85} 220 ${380-discount*85} 195 ${365-discount*85} 170 ${380-discount*85} 145 ${365-discount*85} 120 ${380-discount*85} 95 ${365-discount*85} 70 ${380-discount*85} 45 ${365-discount*85} 20 ${380-discount*85} -5 ${365-discount*85} -30 ${380-discount*85} -55 ${365-discount*85} -80 ${380-discount*85} -105 ${365-discount*85} -130 ${380-discount*85} -155 ${365-discount*85} -180 ${380-discount*85} -205 ${365-discount*85} -230 ${380-discount*85} -255 ${365-discount*85} -270 ${380-discount*85}Z`} fill={paper}/>
 <path d="M-267 -377H264M-264 -369H263" stroke="white" opacity=".6" strokeWidth="4"/>
 <path d="M-220 -207H220" stroke="#91A19D" strokeWidth="3" strokeDasharray="10 7"/>
 <text y="-274" textAnchor="middle" fontSize={estimate?58:47} fill={ink} fontWeight="600">{estimate?'支出估算':'商品报价'}</text>
 <text y="-45" textAnchor="middle" fontSize="123" fill={ink}>¥—</text>
 {estimate?<><text y="50" textAnchor="middle" fontSize="35" fill="#60767A">金额待核实</text><path d="M-180 120H180M-180 143H100" stroke="#9CAAA5" strokeWidth="6"/><path d="M-185 210H185" stroke={orange} strokeWidth="22"/></>:<><path d="M-190 34H145M-190 67H100" stroke="#9CAAA5" strokeWidth="8"/><g opacity={service}><rect x="-240" y="115" width="480" height="100" rx="2" fill={orange}/><text y="180" textAnchor="middle" fontSize="39" fill={ink}>＋ 搬旧 · 安装</text></g></>}
 <g opacity=".55">{Array.from({length:32},(_,i)=><path key={i} d={`M${-165+i*10} ${estimate?281:288-discount*50}v32`} stroke={ink} strokeWidth={i%4===0?5:2}/>)}</g>
</g>;

const Coupon=()=> <g><path d="M-242 -77H242V-30Q210 0 242 30V77H-242V30Q-210 0 -242 -30Z" fill={lime}/><path d="M-130 -60V60" stroke={ink} strokeWidth="3" strokeDasharray="7 7" opacity=".35"/><text x="-184" y="25" textAnchor="middle" fontSize="73" fill={ink}>−</text><text x="38" y="19" textAnchor="middle" fontSize="43" fill={ink}>适用优惠</text></g>;
const Cart=({wheel=0}:any)=><g>
 <ellipse cx="0" cy="188" rx="300" ry="45" fill="#061D26" opacity=".35"/>
 <path d="M-275 -152H45V112H-275Z" fill={orange}/><path d="M45 -152L95 -116V112H45Z" fill="#BC6445"/><path d="M-275 -152L-215 -188H95L45 -152Z" fill="#FFC294"/>
 <path d="M95 -56H204L271 40V112H95Z" fill={paper}/><path d="M130 -29H187L226 29H130Z" fill="#3C6471"/><path d="M-288 108H284V144H-288Z" fill="#91ACAC"/>
 {[-208,209].map(x=><g key={x} transform={`translate(${x} 151) rotate(${wheel})`}><circle r="47" fill="#112A34"/><circle r="26" fill="#ADC5C2"/><path d="M-19 0H19M0 -19V19" stroke={paper} strokeWidth="5"/></g>)}
 <g transform="translate(-109 -34) rotate(-35)"><path d="M-13 81V-21C-57 -39 -37 -85 -13 -83V-50H15V-83C48 -77 54 -35 13 -21V81Z" fill={ink}/></g><text x="-110" y="89" fontSize="36" fill={ink} textAnchor="middle">搬旧 · 安装</text>
</g>;
const Estimate=({x=0,y=0,s=1,r=0}:any)=><g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}><path d="M-270 -380H270V380H-270Z" transform="translate(18 24)" fill="#061D26" opacity=".23"/><Sheet estimate/></g>;

const Cost=({t}:any)=>{
 const cut=P(t,8.85,1.0),load=P(t,11.25,1.08);
 const x=K(t,[[8,595],[8.6,535],[10.25,390],[11.2,315],[12.4,450],[13.25,540]]),y=K(t,[[8,890],[10.2,800],[11.3,765],[13.25,850]]),z=K(t,[[8,1.65],[8.6,1.37],[10.35,1.10],[11.3,.90],[13.25,1.14]]),rot=K(t,[[8,-17],[10.35,-11],[11.4,7],[13.25,4]]);
 return <g>
  <path d="M-250 1440L1330 1090V1590H-250Z" fill="#0D2934" opacity=".72"/><path d="M-250 1425L1330 1075" stroke="#6D919A" opacity=".23" strokeWidth="4"/>
  <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${z})`}>
   <path d="M-270 -380H270V380H-270Z" fill="#001C27" transform="translate(25 35)" opacity=".35"/><Sheet discount={cut} service={load}/>
   <g transform={`translate(${-cut*1000} ${118-cut*240}) rotate(${-cut*40}) scale(${1+cut*.8})`} opacity={1-P(t,9.72,.30)}><Coupon/></g>
  </g>
  <g transform={`translate(${L(1500,760,P(t,10.15,1.1))-P(t,12.20,.75)*1400} ${1120-P(t,12.2,.75)*100}) scale(.86)`} opacity={P(t,10.15,.15)*(1-P(t,12.7,.25))}><Cart wheel={-P(t,10.15,1.1)*380-P(t,12.2,.75)*650}/></g>
  <g opacity={P(t,11.2,.14)*(1-P(t,12.2,.15))} transform={`translate(${L(640,420,load)} ${L(1060,928,load)-Math.sin(load*Math.PI)*150}) rotate(${L(-12,7,load)}) scale(${L(.82,.90,load)})`}><rect x="-235" y="-62" width="470" height="124" fill={orange}/><text textAnchor="middle" y="18" fontSize="40" fill={ink}>＋ 搬旧 · 安装</text></g>
 </g>;
};

const Total=({t}:any)=>{
 const press=P(t,13.3,1.35),issued=P(t,14.8,.55),fly=P(t,16.25,.93);
 const sx=K(t,[[13.2,540],[14.7,530],[15.6,538],[17.2,595]]),sy=K(t,[[13.2,850],[14.7,830],[15.6,870],[17.2,740]]),s=K(t,[[13.2,1.14],[14.0,1.3],[15.5,1.25],[16.1,1.23],[17.2,.68]]),angle=K(t,[[13.2,4],[14.5,0],[15.4,-6],[16.25,-12],[17.2,6]]);
 return <g>
  <g transform={`translate(${sx} ${sy}) rotate(${angle}) scale(${s})`}>
   <path d="M-330 -430H330V445H-330Z" fill="#092531" opacity={(1-fly)*.7}/>
   <g opacity={1-issued}><Sheet discount={1} service={1}/></g>
   <g opacity={issued}><Sheet estimate/></g>
   <g transform={`translate(0 ${L(-540,500,press)})`} opacity={P(t,13.23,.2)*(1-P(t,14.6,.2))}>
    <ellipse cy="42" rx="344" ry="58" fill="#08212A" opacity=".34"/><path d="M-325 -55H325V50H-325Z" fill="url(#roller5)"/><ellipse cx="-325" cy="-2" rx="29" ry="55" fill="#88A8A9"/><ellipse cx="325" cy="-2" rx="29" ry="55" fill="#2A4A58"/><path d="M-319 -34H319" stroke="#E7F3E8" opacity=".6" strokeWidth="4"/>
   </g>
  </g>
  <path d={`M-200 ${1430-P(t,14.8,1.45)*70}L1300 ${1250-P(t,14.8,1.45)*70}`} stroke="#B7CEC8" strokeWidth="25" opacity={(1-fly)*.14}/>
 </g>;
};

const Calendar=({t}:any)=>{
 const flip=P(t,17.48,.42),next=P(t,18.03,.42);
 return <g><path d="M-286 278L-235 -305H237L307 278Z" fill="#153A48"/><path d="M-247 -291H247V269H-247Z" fill={paper}/><rect x="-247" y="-291" width="494" height="118" fill={orange}/><text y="-213" textAnchor="middle" fontSize="42" fill={ink}>每日查价</text><text y="32" textAnchor="middle" fontSize="134" fill={ink}>¥—</text><path d="M-165 98H160M-165 129H84" stroke="#8CA09D" strokeWidth="9"/>
  {[-160,160].map(x=><g key={x}><path d={`M${x} -322V-266`} stroke="#0A232E" strokeWidth="24" strokeLinecap="round"/><path d={`M${x-4} -319V-270`} stroke="#B5CAC8" strokeWidth="8" strokeLinecap="round"/></g>)}
  {[flip,next].map((p,i)=><g key={i} transform={`translate(${p*490} ${-p*390}) rotate(${p*68}) scale(1 ${Math.cos(p*Math.PI/2)})`} opacity={1-P(p,.85,.15)}><path d="M-240 -164H240V266H-240Z" fill={i? '#E5E7D9':'#F6F2E7'}/><text y="35" textAnchor="middle" fontSize="134" fill={ink}>¥—</text><path d="M-165 98H160M-165 129H84" stroke="#8CA09D" strokeWidth="9"/></g>)}
 </g>;
};
const Quote=()=> <g><path d="M-190 -260H190V243L163 260 136 243 109 260 82 243 55 260 28 243 1 260 -26 243 -53 260 -80 243 -107 260 -134 243 -161 260 -190 243Z" fill={paper}/><rect x="-190" y="-260" width="380" height="70" fill={orange}/><text y="-210" textAnchor="middle" fontSize="31" fill={ink}>更新报价</text><text y="-40" textAnchor="middle" fontSize="99" fill={ink}>¥—</text><path d="M-131 29H130M-131 58H70" stroke="#8EA19F" strokeWidth="8"/><path d="M-132 128H131" stroke={lime} strokeWidth="30"/></g>;

const Daily=({t}:any)=>{
 const dive=P(t,18.35,.70),slide=P(t,19.05,.62),open=P(t,19.72,.45),follow=P(t,20.12,.65),strike=P(t,20.78,.26);
 const camX=K(t,[[17.1,540],[18.35,540],[19.05,555],[19.7,555],[20.7,1220],[21.8,1240]]),camY=K(t,[[17.1,820],[18.35,820],[19.05,1000],[20.1,1000],[20.7,950],[21.8,950]]),zoom=K(t,[[17.1,1],[18.35,1],[19.05,1.25],[20.1,1.25],[20.7,1.7],[21.8,1.62]]);
 return <g>
  <path d="M-100 900L1300 520V1600H-100Z" fill="#35525A"/><path d="M-200 860L1250 495V1540L-200 1720Z" fill="url(#desk5)"/>
  <g opacity={(1-dive)*.20} transform={`translate(${P(t,17.3,1.1)*600} 0)`}>{[0,1,2,3].map(i=><path key={i} d={`M${-240+i*330} 270L${100+i*330} 270 ${550+i*330} 1500 ${230+i*330} 1500Z`} fill="#F5D4A1"/>)}</g>
  <g transform={`translate(540 840) scale(${zoom}) translate(${-camX} ${-camY})`}>
   <g opacity={1-dive} transform={`translate(550 ${515-dive*600}) rotate(6)`}><ellipse cy="301" rx="325" ry="80" fill="#071F28" opacity=".35"/><Calendar t={t}/></g>
   <Estimate x={K(t,[[17,595],[18.1,350],[19.05,570]])+follow*590+strike*85} y={K(t,[[17,740],[18.1,1070],[19.05,1060]])-follow*205} s={K(t,[[17,.68],[18.1,.62],[19.05,.48],[20.75,.56]])} r={K(t,[[17,6],[18.1,-13],[19.67,-8]])+follow*8}/>
   {/* Each calendar turn yields a new quote; the earlier observation slides into a tray. */}
   <g opacity={P(t,17.52,.12)*(1-P(t,18.46,.18))} transform={`translate(${L(550,1060,P(t,17.83,.64))} ${L(660,1110,P(t,17.53,.8))}) rotate(${P(t,17.7,.6)*30}) scale(.56)`}><Quote/></g>
   <g transform={`translate(${L(548,570,P(t,18.12,.9))+follow*590+strike*85} ${L(660,1040,P(t,18.12,.9))-follow*45}) rotate(${L(6,-8,slide)+follow*8}) scale(${L(.56,.82,dive)})`} opacity={P(t,18.12,.13)*(1-dive)}><Quote/></g>
   {/* A physical condition stencil opens only in the explicitly hypothetical branch. */}
   <g transform="translate(560 1070)" opacity={dive*(1-follow)}>
    <path d="M-310 -335H310V330H-310Z M-223 -187V188H222V-187Z" fill="#173642" fillRule="evenodd" stroke="#93ACA9" strokeWidth="4"/>
    <path d="M-304 -329H304V-247H-304Z" fill={lime}/><text y="-273" textAnchor="middle" fontSize="39" fill={ink}>需求符合 · 总支出 &lt; ¥4,500</text>
    <path d="M-309 201H309V329H-309Z" fill="#224652"/><text y="279" textAnchor="middle" fontSize="42" fill={paper}>条件核对</text>
    <g transform={`translate(0 -190) scale(1 ${1-open})`}><rect x="-222" y="0" width="444" height="376" fill="#ABC0B6" opacity=".72"/><path d="M-186 49H168M-186 93H85" stroke="#5D7D7F" strokeWidth="9"/><path d="M-185 167H186" stroke={lime} strokeWidth="30"/></g>
    {[-275,275].map(x=><g key={x}><circle cx={x} cy="-212" r="12" fill="#B7CDCB"/><path d={`M${x-6} -218l12 12`} stroke={ink} strokeWidth="3"/></g>)}
   </g>
   <g transform="translate(1355 947)">
    <ellipse cy="243" rx="235" ry="66" fill="#071D26" opacity=".42"/>
    <path d="M-210 152H210L246 207H-246Z" fill="#0B2530"/><ellipse cy="149" rx="210" ry="52" fill="#42666E"/>
    <g transform={`translate(0 ${strike*18}) rotate(${Math.sin((t-21.03)*27)*3.5*strike*(1-P(t,21.45,.3))} 0 120)`}>
     <path d="M-174 128C-173 -86 -105 -144 0 -145C105 -144 173 -86 174 128Z" fill="url(#bell5)"/><ellipse cy="129" rx="174" ry="35" fill="#D7AA62"/><path d="M-95 -84C-48 -124 5 -133 56 -103" stroke="#FFF0BB" strokeWidth="13" fill="none" opacity=".58"/><path d="M0 -145V-186" stroke="#C5A061" strokeWidth="17"/><ellipse cy="-190" rx="54" ry="19" fill="#F5D393"/>
    </g>
    <path d={`M-267 ${135-strike*14}H-194`} stroke={orange} strokeWidth="20" strokeLinecap="round"/>
   </g>
  </g>
 </g>;
};

export const CinematicV5=({t}:any)=>{
 const daily=P(t,17.00,.22);
 return <svg width="1080" height="1620" viewBox="0 0 1080 1620" style={{position:'absolute',inset:0,overflow:'hidden'}}>
  <defs><linearGradient id="roller5" x2="0" y2="1"><stop stopColor="#688B90"/><stop offset=".27" stopColor="#D5E2D9"/><stop offset=".52" stopColor="#709393"/><stop offset="1" stopColor="#264551"/></linearGradient><linearGradient id="desk5" x2="1" y2="1"><stop stopColor="#527374"/><stop offset="1" stopColor="#193F4C"/></linearGradient><linearGradient id="bell5"><stop stopColor="#997749"/><stop offset=".2" stopColor="#EFC889"/><stop offset=".5" stopColor="#FFF0B9"/><stop offset=".76" stopColor="#DBB579"/><stop offset="1" stopColor="#9B773F"/></linearGradient><radialGradient id="vignette5"><stop offset=".55" stopColor="#071C2A" stopOpacity="0"/><stop offset="1" stopColor="#071C2A" stopOpacity=".75"/></radialGradient></defs>
  <g opacity={1-daily}>{t<13.2?<Cost t={t}/>:<Total t={t}/>}</g>
  <g opacity={daily}><Daily t={t}/></g>
  <rect width="1080" height="1620" fill="url(#vignette5)" pointerEvents="none"/>
  <text x="540" y="1490" textAnchor="middle" fontSize="43" fill={paper} opacity={P(t,19.15,.2)}>条件成立时，才提醒</text>
  <rect x="0" y="1570" width="1080" height="50" fill="#102A3B" opacity=".5"/>
 </svg>;
};
