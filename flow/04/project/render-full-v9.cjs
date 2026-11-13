const path=require('path'),fs=require('fs');
const {bundle}=require('@remotion/bundler');const {openBrowser,selectComposition,renderMedia,renderStill}=require('@remotion/renderer');
(async()=>{const mode=process.argv[2],e=path.resolve('../evidence/full-v9');if(!['stills','fixed','full','trial'].includes(mode))throw Error('mode required');
const serveUrl=await bundle({entryPoint:path.resolve('src/v9/Entry.tsx'),outDir:path.join(e,'bundle'),enableCaching:false,webpackOverride:c=>({...c,cache:false})});
const browser=await openBrowser('chrome',{browserExecutable:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',chromiumOptions:{gl:'swangle'}});
try{const composition=await selectComposition({serveUrl,id:'QianwenFullV9',puppeteerInstance:browser});
if(mode==='stills'||mode==='fixed'){for(const t of (mode==='fixed'?[25.3,40.1,43.9,51.5,56.5,65.8,81,98,100.2]:[1.6,6.8,11.8,17.5,21.6,25.3,30.5,35.5,40.1,43.9,47.5,51.5,56.5,59.6,62.8,64.8,65.7,68.1,72.1,75.1,78.4,81,86.5,92.5,95.5,98,100.2])){await renderStill({serveUrl,composition,output:path.join(e,`${mode}-${t}.png`),frame:Math.round(t*60),puppeteerInstance:browser});console.log('STILL',t)}}
else {const outputLocation=path.join(e,mode==='full'?'full-muted.mp4':'trial-23.0to29.0.mp4');if(fs.existsSync(outputLocation))throw Error('Output exists');await renderMedia({serveUrl,composition,outputLocation,frameRange:mode==='full'?[0,6121]:[1380,1740],codec:'h264',crf:18,concurrency:1,imageFormat:'png',muted:true,puppeteerInstance:browser,onProgress:({progress})=>{const n=Math.floor(progress*20);if(n!==global.last){global.last=n;console.log('PROGRESS',n*5)}}});console.log('COMPLETE',outputLocation)}
}finally{await browser.close({silent:true})}})().catch(e=>{console.error(e);process.exit(1)});
