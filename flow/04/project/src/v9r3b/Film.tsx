// C005 connected goals/tools; EP102Selected07 sequential category lift/grouping; OP09 task gathering; N044 media-to-condition handoff.
import React from 'react';
import {AbsoluteFill,OffthreadVideo,Sequence,staticFile,useCurrentFrame} from 'remotion';
import {p,q,mix} from '../v8/theme';
import {Fridge} from '../v8/CostReminder';
import {CostScene,ServiceTools} from './CostScene';
import captions from './captions.json';
export const C={bg:'#090D11',fg:'#EDF5F2',muted:'#9DAFB4',lime:'#C0F279',cyan:'#79E0E2',amber:'#F0B875',panel:'#1D282E',line:'#42565A'};
const T=({x=100,y=250,size=48,fill=C.fg,weight=600,anchor='start',children,...rest}:any)=><text x={x} y={y} fontSize={size} fontWeight={weight} fill={fill} textAnchor={anchor} {...rest}>{children}</text>;
function Icon({kind,x=0,y=0,s=1,color=C.lime}:any){const paths:any={bag:<><path d="M18 34h64l7 55H11zM34 34V22a16 16 0 0 1 32 0v12"/></>,ticket:<><path d="M8 22h84v20a10 10 0 0 0 0 20v19H8V62a10 10 0 0 0 0-20zM65 23v57"/></>,pin:<><path d="M50 94S14 61 14 38a36 36 0 1 1 72 0c0 23-36 56-36 56Z"/><circle cx="50" cy="37" r="12"/></>,chat:<><path d="M8 13h84v58H42L19 91V71H8zM26 34h48M26 50h32"/></>,search:<><circle cx="42" cy="42" r="27"/><path d="m62 62 28 28"/></>,check:<path d="m16 51 22 23 48-51"/>,list:<><path d="M31 23h58M31 50h58M31 77h58M10 23h1M10 50h1M10 77h1"/></>,arrow:<path d="M8 50h82M66 26l24 24-24 24"/>,bell:<><path d="M22 62V40a28 28 0 0 1 56 0v22l12 13H10zM39 87h22"/></>,star:<path d="m50 6 14 29 32 5-23 23 5 32-28-15-28 15 5-32L4 40l32-5z"/>};return <g transform={`translate(${x} ${y}) scale(${s})`} fill="none" stroke={color} strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">{paths[kind]||paths.list}</g>}
const Head=({title,sub}:any)=><><T y={238} size={66} weight={900}>{title}</T>{sub&&<T y={316} size={29} fill={C.muted} weight={500}>{sub}</T>}</>;
const Panel=({x,y,w,h,fill=C.panel,children}:any)=><g><rect x={x} y={y} width={w} height={h} rx="34" fill={fill} stroke={C.line} strokeWidth="2" filter="url(#soft9)"/>{children}</g>;
export function Defs(){return <defs><filter id="soft9" x="-30%" y="-40%" width="180%" height="200%"><feDropShadow dx="0" dy="18" stdDeviation="20" floodColor="#000" floodOpacity=".4"/></filter><filter id="blur8"><feGaussianBlur stdDeviation="10"/></filter><linearGradient id="fridge8" x1="0" y1="0" x2="1" y2=".8"><stop stopColor="#F0F4EF"/><stop offset=".45" stopColor="#C9DAD5"/><stop offset="1" stopColor="#99B7B4"/></linearGradient></defs>}
export function Portrait({name,start,duration,x=270,y=480,width=540,t}:any){const enter=p(t,start,start+.25),exit=1-p(t,start+duration-.25,start+duration);return <Sequence from={Math.round(start*60)} durationInFrames={Math.round(duration*60)} layout="none"><div style={{position:'absolute',left:x,top:y,width,height:width*(name==='intro'?740:960)/540,opacity:enter*exit,transform:`translateY(${26*(1-enter)}px)`,overflow:'hidden',borderRadius:38}}><OffthreadVideo src={staticFile(`${name==='intro'?'v9':'v9r3-final'}/${name}.mp4`)} muted style={{width:'100%',height:'100%',objectFit:'contain'}}/></div></Sequence>}
export function GoalsToTools({t}:{t:number}){
 const s=t-4.9,collapse=q(t,18.85,20.0),run=q(t,14.55,15.85),titleOpacity=1-p(t,18.85,19.15);
 const goalY=mix(540,630,collapse),scale=mix(1,.83,collapse);
 return <><g opacity={titleOpacity}><Head title="个人 AI 助理" sub="Personal Agent"/></g><g opacity={p(t,18.85,19.35)}><Head title={t<21.05?"从目标到行动":"千问 Go"} sub="从一个具体的目标说起"/></g>
  <g transform={`translate(${80*collapse} ${-20*collapse}) scale(${scale})`}>
   <Panel x={140} y={goalY} w={800} h={180} fill="#263B32"><Icon kind="chat" x={182} y={goalY+40} s={.85}/><T x={302} y={goalY+104} size={52} fill={C.lime}>说清楚你的目标</T></Panel>
   {[['bag','买东西',10.01],['ticket','订票',10.85],['pin','安排出行',11.7]].map(([icon,label,at],i)=>{const a=p(t,Number(at),Number(at)+.6),x=110+i*300;return <g key={i} opacity={a} transform={`translate(0 ${80*(1-a)})`}><path d={`M540 ${goalY+180}V850H${x+130}V965`} stroke={C.line} strokeWidth="4" fill="none"/><rect x={x} y="962" width="260" height="230" rx="36" fill={C.panel} stroke={C.line} strokeWidth="2"/><Icon kind={icon} x={x+91} y={994} s={.78} color={i===1?C.amber:C.cyan}/><T x={x+130} y={1155} size={38} anchor="middle">{label}</T><path d={`M540 ${goalY+180}V850H${x+130}V960`} stroke={C.lime} strokeWidth="5" pathLength="1" strokeDasharray="1" strokeDashoffset={1-run} fill="none"/></g>})}
   <g opacity={p(t,16.61,17.2)}><path d="M240 1220V1315H840V1220M540 1315v80" fill="none" stroke={C.cyan} strokeWidth="4"/><T x={540} y={1455} size={44} anchor="middle" fill={C.cyan}>调用工具，推进事情</T></g>
  </g><g opacity={p(s,.1,.7)*(1-p(t,10.01,10.45))}><g opacity={p(t,6.3,6.85)} transform={`translate(0 ${-75*(1-q(t,6.3,6.85))})`}><Icon kind="arrow" x={473} y={850} s={1.4}/></g><g opacity={p(t,8.08,8.63)} transform={`translate(0 ${65*(1-q(t,8.08,8.63))})`}><T x={540} y={1155} size={49} anchor="middle" fill={C.lime}>让目标变成下一步</T></g></g>
 </>;
}
// EP102Selected07: each new category enters after the existing group makes room; all established requirements remain.
export function RequirementBuild({t}:{t:number}){
 const spread=q(t,34.51,35.25),collapse=q(t,55.51,56.2);
 const fridgeX=mix(380,115,spread),fridgeY=mix(620,470,spread),fridgeS=mix(1.35,.86,spread);
 const rows=[['star','收藏夹里的这款',36.39],['pin','送到杭州',39.55],['arrow','旧冰箱搬走',40.83],['list','优惠 · 回收 · 安装',42.91],['bell','总支出 < 4500 元',48.59]];
 return <><Head title={t<34.51?'双十一，想买台冰箱':'把需求一次说完整'} sub={t<34.51?'从收藏夹里的那一款开始':undefined}/><g opacity={p(t,28.57,29.17)} transform={`translate(${100*(1-q(t,28.57,29.17))} 0)`}><Fridge x={fridgeX} y={fridgeY} s={fridgeS}/></g>
 <g opacity={1-spread}><g opacity={p(t,29.95,30.5)} transform={`translate(0 ${45*(1-q(t,29.95,30.5))})`}><T x={540} y={1260} size={65} anchor="middle" fill={C.amber}>11.11</T></g><g opacity={p(t,32.55,33.2)}><path d="M320 1390h440" stroke={C.lime} strokeWidth="4"/><T x={540} y={1460} size={38} anchor="middle">一款冰箱，一个完整需求</T></g></g>
 {rows.map(([icon,label,cue],i)=>{const a=p(t,Number(cue),Number(cue)+.7),n=q(t,Number(cue),Number(cue)+1.0),y=600+i*183-40*[39.55,40.83,42.91,48.59].reduce((v,c)=>v+q(t,c,c+.6),0);return <g key={i} opacity={a} transform={`translate(${120*(1-n)} ${-32*collapse})`}><rect x="420" y={y} width="560" height="142" rx="29" fill={i===4?'#CCEFA1':C.panel} stroke={i===4||t>52.07+i*.4?C.lime:C.line} strokeWidth={2+3*p(t,52.07+i*.4,52.37+i*.4)}/><Icon kind={icon} x={446} y={y+37} s={.64} color={i===4?'#244128':C.cyan}/><T x={540} y={y+88} size={i===3?33:36} fill={i===4?'#17351F':C.fg}>{label}</T></g>})}
 <g opacity={p(t,45.39,46.1)} transform="translate(138 940)"><ServiceTools x={0} y={0} progress={q(t,45.39,46.5)}/></g>
 <g opacity={p(t,52.07,52.8)}><path d="M420 1395h550" stroke={C.lime} strokeWidth="3"/><T x={690} y={1470} size={39} anchor="middle" fill={C.lime}>全部满足，再提醒</T></g>
 </>;
}
// C005: a single verified input branches into queries and rejoins one quote node; same appliance remains throughout.
export function ModelToQuote({t}:{t:number}){
 const confirm=p(t,60.0,60.55),branch=q(t,61.91,62.65),service=p(t,64.11,64.8),gather=q(t,65.15,65.7667);
 return <><Head title={t<61.91?'先确认同一款型号':t<64.11?'把店铺报价放到一起':'把服务条件问清楚'}/>
 <Fridge x={mix(138,147,gather)} y={mix(680,444,gather)} s={mix(.9,.46,gather)}/>
 <g opacity={1-branch}><Panel x={465} y={600} w={485} h={460}><Icon kind="search" x={520} y={655} s={.85}/><T x={515} y={855} size={41}>收藏夹指定型号</T><T x={515} y={970} size={35} fill={C.lime} opacity={confirm}>✓ 型号已对齐</T></Panel><path d="M370 850h85" stroke={C.cyan} strokeWidth="4"/><g opacity={p(t,58.0,58.6)}><rect x="130" y="655" width="270" height="440" rx="30" stroke={C.lime} strokeWidth="5" fill="none" pathLength="1" strokeDasharray="1" strokeDashoffset={1-q(t,58,58.6)}/></g><g opacity={confirm} transform={`translate(0 ${40*(1-confirm)})`}><Icon kind="check" x={195} y={1140} s={1.1}/><T x={260} y={1320} size={36} anchor="middle" fill={C.lime}>型号一致</T></g></g>
 <g opacity={branch*(1-gather)}>{[0,1,2].map(i=>{const y=540+i*250;return <g key={i} transform={`translate(${80*(1-branch)} 0)`}><path d={`M370 820H420V${y+90}H470`} stroke={C.cyan} strokeWidth="3" fill="none"/><Panel x={470} y={y} w={475} h={195}><Icon kind={service>.5?'chat':'bag'} x={495} y={y+44} s={.72}/><T x={592} y={y+78} size={37}>店铺 {String.fromCharCode(65+i)}</T><T x={502} y={y+154} size={29} fill={C.muted}>{service>.5?'优惠 / 回收 / 安装':'商品报价 + 服务条件'}</T></Panel></g>})}</g>
 <g opacity={gather}><rect x="100" y="446" width="880" height="225" rx="40" fill={C.panel}/><Fridge x={147} y={444} s={.46}/><T x={305} y={529} size={26} fill={C.muted}>收藏夹里的同一款冰箱</T><T x={305} y={593} size={50} weight={900}>商品报价</T><T x={878} y={591} size={27} anchor="end" fill={C.muted}>按店铺询价</T></g>
 </>;
}
// OP09: existing tasks move into one recipient; the final human choice is separate from AI's preparation work.
export function TasksToChoice({t}:{t:number}){
 const take=q(t,94.55,96.27),final=p(t,99.03,99.65);
 return <><Head title={t<94.55?'来回查、问、理清楚':t<99.03?'把这些麻烦交给 AI':'把精力留给最后的选择'}/>
 {[['search','来回查',83.83],['chat','来回问',89.07],['list','理清楚',90.87]].map(([icon,label,cue],i)=>{const a=p(t,Number(cue),Number(cue)+.6),emphasis=p(t,[86.27,89.77,92.0][i],[86.82,90.32,92.55][i])*(i<2?1-p(t,[89.77,92.0][i],[90.32,92.55][i]):1),x=mix(125,366,take),y=mix(520+i*265,710+i*10,take),sc=mix(1,.48,take);return <g key={i} opacity={a*(1-p(t,95.85,96.27))} transform={`translate(${x} ${y}) scale(${sc})`}><rect width="830" height="190" rx="34" fill={C.panel} stroke={C.line} strokeWidth="2"/><rect width="830" height="190" rx="34" fill="#355744" opacity={emphasis}/><Icon kind={icon} x={42} y={42} s={.93}/><T x={202} y={116} size={50}>{label}</T><path d="M640 97h120m-28-25 28 25-28 25" fill="none" stroke={C.cyan} strokeWidth="4"/></g>})}
 <g opacity={p(t,94.55,95.2)*(1-p(t,96.27,96.6))}><rect x="325" y="660" width="430" height="260" rx="50" fill="#CCEFA1"/><T x={540} y={824} size={88} anchor="middle" fill="#17351F" weight={900}>AI</T></g>
 <g opacity={final}><T x={540} y={1488} size={44} anchor="middle" fill={C.lime}>最后的决定，留给自己。</T></g></>;
}
export function FullFilm(){const t=useCurrentFrame()/60,c=captions.find(v=>t>=v.start&&t<v.end);return <AbsoluteFill style={{background:C.bg,color:C.fg,fontFamily:'Eli MiSans',fontWeight:500,fontSynthesis:'none',overflow:'hidden'}}>
 <svg width="1080" height="1560"><Defs/>
 {t<4.9&&<><Head title="AI 的下一步" sub="帮普通人，把日常的事办好"/><path d="M100 396h880" stroke={C.line} strokeWidth="2"/><path d="M100 396h880" stroke={C.lime} strokeWidth="4" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p(t,0,2.2)}/></>}
 {t>=4.9&&t<23.45&&<GoalsToTools t={t}/>}
 {t>=23.45&&t<28.57&&<><Head title="一个买冰箱的案例"/><g opacity={p(t,24,25)}><Fridge x={760} y={740} s={.85}/><path d="M680 950h60" stroke={C.cyan} strokeWidth="4"/><T x={540} y={1460} size={39} fill={C.lime} anchor="middle">看看一个需求怎样串起这些事</T></g></>}
 {t>=28.57&&t<57.47&&<RequirementBuild t={t}/>}
 {t>=57.47&&t<(3946/60)&&<ModelToQuote t={t}/>}
 {t>=79.37&&t<83.83&&<Head title="我想要的 AI" sub="其实没有那么复杂"/>}
 {t>=83.83&&<TasksToChoice t={t}/>}
 </svg>
 {t>=(3946/60)&&t<79.37&&<CostScene time={t-(3946/60)}/>}
 <Portrait name="intro" x={220} width={640} y={555} start={0} duration={4.9} t={t}/>
 <Portrait name="bridge-safe" start={23.45} duration={5.12} x={105} width={500} t={t}/>
 <Portrait name="opinion-safe" start={79.37} duration={4.46} t={t}/>
 <Portrait name="close-safe" start={96.27} duration={5.75} y={460} t={t}/>
 <div style={{position:'absolute',left:65,right:65,top:1575,height:205,display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center',textAlign:'center'}}>{c&&<><div style={{fontSize:c.zh.length>20?39:42,lineHeight:1.45,fontWeight:600}}>{c.zh}</div><div style={{fontSize:25,lineHeight:1.4,marginTop:12,color:C.muted}}>{c.en}</div></>}</div>
 </AbsoluteFill>}
