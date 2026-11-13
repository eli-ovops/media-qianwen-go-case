const path=require('path'),fs=require('fs');
const {bundle}=require('@remotion/bundler');const {openBrowser,selectComposition,renderMedia}=require('@remotion/renderer');
(async()=>{const e=path.resolve('../evidence/full-v9-r3');
const serveUrl=await bundle({entryPoint:path.resolve('src/v9r3/Entry.tsx'),outDir:path.join(e,'bundle'),enableCaching:false,webpackOverride:c=>({...c,cache:false})});
const browser=await openBrowser('chrome',{browserExecutable:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',chromiumOptions:{gl:'swangle'}});
try{const composition=await selectComposition({serveUrl,id:'QianwenFullV9',puppeteerInstance:browser});
for(const [name,a,b] of [['bridge',1407,1713],['opinion',4762,5029],['close',5776,6121]]){
 const outputLocation=path.join(e,`patch-${name}.mp4`);if(fs.existsSync(outputLocation))throw Error('Output exists');let last=-1;
 await renderMedia({serveUrl,composition,outputLocation,frameRange:[a,b],codec:'h264',crf:18,concurrency:1,imageFormat:'png',muted:true,puppeteerInstance:browser,onProgress:({progress})=>{const n=Math.floor(progress*4);if(n!==last){last=n;console.log(name,n*25)}}});console.log('COMPLETE',name);
}
}finally{await browser.close({silent:true})}})().catch(e=>{console.error(e);process.exit(1)});
