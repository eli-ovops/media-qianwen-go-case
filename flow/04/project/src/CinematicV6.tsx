import React from 'react';
const C={ink:'#123041',lime:'#DAF87D',blue:'#AFCBD2',orange:'#F6AC75',white:'#EBEFE8'};
const clamp=(v:number)=>Math.max(0,Math.min(1,v));const P=(t:number,a:number,d=.6)=>{let x=clamp((t-a)/d);return x*x*(3-2*x)};
const L=(a:number,b:number,v:number)=>a+(b-a)*v;
const K=(t:number,ps:number[][])=>{if(t<ps[0][0])return ps[0][1];for(let i=1;i<ps.length;i++)if(t<ps[i][0])return L(ps[i-1][1],ps[i][1],P(t,ps[i-1][0],ps[i][0]-ps[i-1][0]));return ps[ps.length-1][1]};
const T=({x=0,y=0,s=36,c=C.white,children,...props}:any)=><text x={x} y={y} textAnchor="middle" fontSize={s} fill={c} {...props}>{children}</text>;
const Block=({x=0,y=0,c=C.blue,w=100,h=235,icon}:any)=><g transform={`translate(${x} ${y})`}><path d={`M0 0l45 -38h${w}l-45 38z`} fill={c}/><path d={`M${w} 0l45 -38v${h}l-45 38z`} fill={c} style={{filter:'brightness(.57)'}}/><rect width={w} height={h} rx="2" fill={c} style={{filter:'brightness(.83)'}}/><path d={`M4 5h${w-8}`} stroke="#FFFFFF88" strokeWidth="3"/>{icon&&<T x={w/2} y={h/2+12} s={48} c={C.ink}>{icon}</T>}</g>;
const Coin=({x,y,o=1,turn=0}:any)=><g opacity={o} transform={`translate(${x} ${y}) rotate(${turn})`}><ellipse cy="17" rx="103" ry="87" fill="#778F91"/><ellipse rx="103" ry="87" fill={C.white} stroke="#D7EEEC" strokeWidth="4"/><T y="14" s={58} c={C.ink}>¥—</T></g>;
const Bell=({x,y,t}:any)=><g transform={`translate(${x} ${y}) rotate(${P(t,20.65,.3)*Math.sin((t-20.65)*14)*8})`}><ellipse cy="175" rx="140" ry="24" fill="#02172066"/><path d="M-100 82q25 -20 25 -110q0 -95 75 -100q75 5 75 100q0 90 25 110z" fill="url(#brass6)" stroke="#F8EBAF" strokeWidth="3"/><ellipse cy="90" rx="107" ry="22" fill="#98744A"/><circle cy="111" r="21" fill={C.lime}/><circle cy="-138" r="13" fill="#F0D58F"/><path d="M-43 -79q-21 33 -21 84" fill="none" stroke="#FFF8C899" strokeWidth="10" strokeLinecap="round"/>{t>20.65&&<g fill="none" stroke={C.lime} strokeWidth="5" opacity={.4+.5*Math.abs(Math.sin(t*9))}><path d="M-142 -83q-55 77 -3 155M142 -83q55 77 3 155"/></g>}</g>;
export const CinematicV6=({t}:{t:number})=>{
 const remove=P(t,8.7,1.0),add=P(t,10.3,1.8),join=P(t,13.3,1.25),daily=P(t,16.6,.65),pass=P(t,20.05,.72);
 const bx=K(t,[[8,175],[10.1,230],[12.5,120],[14.8,145],[16.6,260],[17.3,325],[19.7,325],[20.9,170]]);
 const by=K(t,[[8,680],[10.1,770],[12.6,780],[15,710],[16.6,735],[17.3,1030],[19.7,1030],[21,975]]);
 const scale=K(t,[[8,1.43],[10,1.43],[12.8,1.24],[15.1,1.28],[16.6,1.02],[17.3,.74],[19.7,.74],[21,.70]]);
 const spread=L(143,108,join);const camRot=K(t,[[8,-15],[10.5,-15],[13,9],[15.5,-6],[17.3,0],[21.8,0]]);
 const q1=P(t,17.08,.5),q1out=P(t,18.35,.5),q2=P(t,18.7,.5),scan1=P(t,17.7,.4)*(1-P(t,18.14,.2)),scan2=P(t,19.25,.4)*(1-P(t,19.7,.2));
 return <svg width="1080" height="1620" viewBox="0 0 1080 1620" style={{position:'absolute',top:0,left:0}}><defs><radialGradient id="halo6"><stop stopColor="#83B2B2" stopOpacity=".23"/><stop offset="1" stopColor="#83B2B2" stopOpacity="0"/></radialGradient><linearGradient id="brass6"><stop stopColor="#8F885B"/><stop offset=".28" stopColor="#F4E6A2"/><stop offset=".64" stopColor="#C7BA75"/><stop offset="1" stopColor="#777750"/></linearGradient></defs>
 <ellipse cx="550" cy="1030" rx="660" ry="400" fill="url(#halo6)"/>
 {/* Time is a visible day/night cycle, two independent quote arrivals. */}
 <g opacity={daily}>
 <g transform={`translate(540 500)`}><path d="M-215 0a215 215 0 1 1 430 0" fill="none" stroke="#B8D6DC33" strokeWidth="4" strokeDasharray="5 14"/>
 <g transform={`rotate(${P(t,18.02,.8)*180})`}><circle cx="-215" cy="0" r="37" fill={C.lime}/>{Array.from({length:8},(_,i)=><path key={i} transform={`translate(-215 0) rotate(${i*45})`} d="M0 -49v-14" stroke={C.lime} strokeWidth="4"/>)}<path opacity={Math.pow(Math.abs(Math.cos(P(t,18.02,.8)*Math.PI)),4)} d="M185 -30a35 35 0 1 0 33 53a34 34 0 0 1 -33 -53" fill="#BBD3DD"/></g>
 <T y="-26" s={81}>{t<18.48?'第 1 天':'次日'}</T><T y="38" s={27} c="#A7C5CE">时间推进示意</T>
 </g>
 <Coin x={L(1030,610,q1)-q1out*930} y={L(655,825,q1)-Math.sin(q1out*Math.PI)*80} o={q1*(1-q1out)} turn={-12+q1*12-q1out*50}/>
 <Coin x={L(1030,610,q2)} y={L(655,825,q2)} o={q2*(1-P(t,20,.3))} turn={12-q2*12}/>
 <g opacity={(scan1+scan2)*.8} transform={`translate(${L(310,810,t<18.5?P(t,17.7,.5):P(t,19.25,.5))} 980)`}><ellipse rx="74" ry="37" stroke={C.lime} strokeWidth="8" fill="#DAF87D13"/><path d="M55 26l54 42" stroke={C.lime} strokeWidth="16" strokeLinecap="round"/></g>
 <T x="540" y="645" s={30} c={C.lime} opacity={1-pass}>每天重新查价</T>
 </g>
 {/* The same pieces are removed, joined and carried through to the estimate. */}
 <g transform={`translate(${bx} ${by}) scale(${scale}) rotate(${camRot} 270 100)`}>
 <ellipse cx="267" cy="278" rx="345" ry="60" fill="#041A2766"/>
 {[0,1,2].map(i=><Block key={i} x={i*spread} y={i===1?-18*(1-join):0} c={C.blue} icon={i===1?'¥':null}/>)}
 <g opacity={1-P(t,9.65,.35)} transform={`translate(${3*143+remove*210} ${-remove*390}) rotate(${remove*25})`}><Block c={C.lime} h={235} icon="−"/><T x="50" y="-70" s={32} c={C.lime}>优惠</T></g>
 {[0,1].map(i=>{const a=P(t,10.3+i*.48,1.0);return <g key={i} opacity={P(t,10.3+i*.48,.15)} transform={`translate(${L(-290-i*100,(3+i)*spread,a)} ${L(465+i*30,0,a)})`}><Block c={C.orange} icon={i===0?'+':null}/></g>})}
 <g opacity={join}><path d="M-17 -47h595v305h-595z" fill="none" stroke="#E8F1E575" strokeWidth="4" strokeDasharray={`${2400*join} 2400`}/><path d="M224 -40v291M242 -40v291" stroke={C.lime} strokeWidth="7"/></g>
 </g>
 <g opacity={1-P(t,16.6,.28)}>
 
 <T x={540} y={470} s={34} c={C.orange} opacity={P(t,10,.35)*(1-P(t,13.3,.4))}>加入服务费用</T>
 <T x={540} y={580} s={40} opacity={P(t,13.3,.4)}>支出估算</T>
 <T x="540" y="310" s={26} c="#A9C6CE">构成示意 · 部件大小不代表金额比例</T>
 <g opacity={P(t,14.7,.4)}><T x="540" y="1175" s={92} c={C.lime}>¥—</T><T x="540" y="1232" s={29}>金额待核实</T></g>
 </g>
 <g opacity={daily}>
 <T opacity={P(t,17.04,.2)} x={L(550,365,pass)} y={L(1320,1240,pass)} s={37}>支出估算</T>
 <T opacity={P(t,17.04,.2)} x={L(550,365,pass)} y={L(1370,1290,pass)} s={27} c="#AAC5CB">构成示意 · 金额待核实</T>
 {/* Two compact jaws open only in the explicitly hypothetical branch. */}
 <g opacity={P(t,19.5,.35)}><g opacity={1-P(t,20.48,.3)} transform={`translate(215 935) rotate(${pass*78})`}><path d="M0 0v260h40" fill="none" stroke={C.lime} strokeWidth="13" strokeLinecap="round"/></g><g opacity={1-P(t,20.48,.3)} transform={`translate(870 935) rotate(${-pass*78})`}><path d="M0 0v260h-40" fill="none" stroke={C.lime} strokeWidth="13" strokeLinecap="round"/></g>
 <T x="340" y="1510" s={30} c={C.lime}>同款需求</T><T x="745" y="1510" s={30} c={C.lime}>总支出 &lt; ¥4,500</T>
 <T x="540" y="1445" s={31}>条件成立时，才提醒</T>
 </g>
 <g opacity={pass} transform={`translate(${(1-pass)*230} ${-(1-pass)*120})`}><Bell x={830} y={830} t={t}/></g>
 </g>
 </svg>
};
