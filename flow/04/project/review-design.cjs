const path=require('path');
const {bundle}=require('@remotion/bundler');
const {openBrowser,selectComposition,renderStill}=require('@remotion/renderer');
(async()=>{
 const url=await bundle({entryPoint:path.resolve('src/index.ts'),webpackOverride:c=>({...c,cache:false}),enableCaching:false});
 const browser=await openBrowser('chrome',{browserExecutable:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',chromiumOptions:{gl:'swangle'}});
 try{
 const comp=await selectComposition({serveUrl:url,id:'QianwenGoV1',puppeteerInstance:browser});
 for(const s of [32,78.5,89]){
 await renderStill({serveUrl:url,composition:comp,output:path.resolve(`../evidence/design-layout2-${s}s.png`),frame:Math.round(s*60),imageFormat:'png',puppeteerInstance:browser});console.log('STILL',s);
 }
 }finally{await browser.close({silent:true})}
})().catch(e=>{console.error(e);process.exit(1)});
