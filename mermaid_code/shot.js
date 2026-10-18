const puppeteer=require('/opt/npm-tools/node_modules/puppeteer-core');
const fs=require('fs');
(async()=>{
 const b=await puppeteer.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox']});
 for(const f of process.argv.slice(2)){
  const svg=fs.readFileSync(f,'utf8');
  const m=svg.match(/viewBox="([^"]+)"/).slice(1)[0].split(/\s+/).map(Number);
  const p=await b.newPage();
  await p.setViewport({width:Math.ceil(m[2]),height:Math.ceil(m[3]),deviceScaleFactor:3});
  await p.setContent('<html><body style="margin:0;background:#fff">'+svg.replace(/<\?xml[^>]*\?>/,'')+'</body></html>');
  await p.screenshot({path:f.replace(/\.svg$/,'.png'),clip:{x:0,y:0,width:Math.ceil(m[2]),height:Math.ceil(m[3])}});
  await p.close();
 }
 await b.close();
})();
