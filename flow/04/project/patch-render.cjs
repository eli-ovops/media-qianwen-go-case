const path=require('path'),fs=require('fs');
const {bundle}=require('@remotion/bundler');const {openBrowser,selectComposition,renderMedia}=require('@remotion/renderer');
(async()=>{const url=await bundle({entryPoint:path.resolve('src/index.ts'),webpackOverride:c=>({...c,cache:false}),enableCaching:false});const browser=await openBrowser('chrome',{browserExecutable:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',chromiumOptions:{gl:'swangle'}});
try{const c=await selectComposition({serveUrl:url,id:'QianwenGoV1',puppeteerInstance:browser});const ws=JSON.parse(fs.readFileSync('../evidence/patch-windows.json','utf8'));
for(let i=0;i<ws.length;i++){let w=ws[i];await renderMedia({serveUrl:url,composition:c,outputLocation:path.resolve(`../evidence/patch-${i}.mp4`),codec:'h264',crf:16,muted:true,concurrency:1,frameRange:[w.start_frame,w.end_frame_exclusive-1],puppeteerInstance:browser,chromiumOptions:{gl:'swangle'}});console.log('PATCH',i,w);}}
finally{await browser.close({silent:true})}})().catch(e=>{console.error(e);process.exit(1)});
