const puppeteer=require('/Users/USER/.npm/_npx/110f701c48e68d66/node_modules/puppeteer-core');
const fs=require('fs'),path=require('path');
(async()=>{
const root=path.resolve('..');
const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--mute-audio','--allow-file-access-from-files'],userDataDir:path.join(root,'evidence/sample-player-profile')});
fs.writeFileSync(path.join(root,'evidence/sample-player-process.json'),JSON.stringify({pid:browser.process().pid,profile:path.join(root,'evidence/sample-player-profile')},null,2));
try{
 const page=await browser.newPage();await page.setViewport({width:900,height:1100,deviceScaleFactor:1});
 await page.goto('file://'+path.join(root,'preview.html'));
 await page.waitForFunction(()=>{const v=document.querySelector('video');return v.readyState>=2},{timeout:30000});
 const initial=await page.$eval('video',v=>({paused:v.paused,muted:v.muted,duration:v.duration,width:v.videoWidth,height:v.videoHeight}));
 await page.$eval('video',v=>{v.muted=true;v.currentTime=20.5});
 await page.waitForFunction(()=>Math.abs(document.querySelector('video').currentTime-20.5)<.1&&!document.querySelector('video').seeking);
 await page.screenshot({path:path.join(root,'evidence/sample-player-20.5.png')});
 const before=await page.$eval('video',v=>v.currentTime);await page.$eval('video',v=>v.play());
 await page.waitForFunction(t=>document.querySelector('video').currentTime>t+.4,{},before);
 const played=await page.$eval('video',v=>({time:v.currentTime,muted:v.muted,error:v.error?.message||null}));await page.$eval('video',v=>v.pause());
 const paused=await page.$eval('video',v=>v.paused);
 fs.writeFileSync(path.join(root,'evidence/sample-player-check.json'),JSON.stringify({initial,seek:20.5,played,paused,scope:'muted programmatic playback and screenshot; no human audio audition'},null,2));
}finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
