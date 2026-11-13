const fs=require('fs'),path=require('path');
const PDFDocument=require('pdfkit'),SVGtoPDF=require('svg-to-pdfkit');
const [dir,out]=process.argv.slice(2);
const F=(pkg,v,n)=>path.join(__dirname,'node_modules/@expo-google-fonts',pkg,v,n);
const fonts={
 'A':F('arimo','400Regular','Arimo_400Regular.ttf'),'A-B':F('arimo','700Bold','Arimo_700Bold.ttf'),
 'A-I':F('arimo','400Regular_Italic','Arimo_400Regular_Italic.ttf'),'A-BI':F('arimo','700Bold_Italic','Arimo_700Bold_Italic.ttf'),
 'G':F('gelasio','400Regular','Gelasio_400Regular.ttf'),'G-B':F('gelasio','700Bold','Gelasio_700Bold.ttf'),
 'G-I':F('gelasio','400Regular_Italic','Gelasio_400Regular_Italic.ttf'),'G-BI':F('gelasio','700Bold_Italic','Gelasio_700Bold_Italic.ttf')};
const doc=new PDFDocument({size:'A4',margin:0,autoFirstPage:false,info:{Title:'Optics & Wave Nature of Light - Physics Investigatory Project'}});
for(const k in fonts) doc.registerFont(k,fonts[k]);
doc.pipe(fs.createWriteStream(out));
const files=fs.readdirSync(dir).filter(f=>f.endsWith('.svg')).sort();
for(const f of files){
  let svg=fs.readFileSync(path.join(dir,f),'utf8').replace(/<metadata[\s\S]*?<\/metadata>/g,'');
  doc.addPage({size:'A4',margin:0});
  SVGtoPDF(doc,svg,0,0,{width:595.28,height:841.89,preserveAspectRatio:'xMidYMid meet',
    warningCallback:w=>console.log('WARN',f,w),
    fontCallback:(family,bold,italic)=>{const b=/georgia|serif/i.test(family||'')&&!/sans/i.test(family||'')?'G':'A';return b+(bold||italic?'-':'')+(bold?'B':'')+(italic?'I':'');}});
}
doc.end(); console.log('pages',files.length);
