// Replace specific promotional components without changing article figures.
const fs=require('node:fs'),path=require('node:path');
const labels=new Map([
 ['150+|Businesses Served',['Define scope','Agree the questions and work to be reviewed']],
 ['92%|Client Retention',['Assign owners','Name the people responsible for implementation']],
 ['92%|Retention Rate',['Assign owners','Name the people responsible for implementation']],
 ['40%|Avg Efficiency Gain',['Set a baseline','Document the operating measures before changes']],
 ['40%|Avg Efficiency Improvement',['Set a baseline','Document the operating measures before changes']],
 ['5x|Avg ROI',['Review outcomes','Compare actual results with the agreed baseline']]
]);
function clean(s){
 return s.replace(/(<div\b[^>]*>\s*<span\b[^>]*class="stat-num"[^>]*>)([^<]+)(<\/span>\s*(?:<br>\s*)?<span\b[^>]*class="stat-label"[^>]*>)([^<]+)(<\/span>\s*<\/div>)/g,(all,start,value,middle,label,end)=>{
  const replacement=labels.get(value+'|'+label);if(!replacement)return all;
  start=start.replace(/style="[^"]*"/g,'').replace('class="stat-num"','class="stat-num" style="font-size:1.3rem"');
  return start+replacement[0]+middle+replacement[1]+end;
 }).replace(/<span class="trust-item"><span>[^<]*<\/span> (?:150\+ businesses served|92% client retention)<\/span>/g,'');
}
function run(root='.',check=false){let changed=[];function walk(dir){for(const entry of fs.readdirSync(dir,{withFileTypes:true})){if(['.git','node_modules'].includes(entry.name))continue;const file=path.join(dir,entry.name);if(entry.isDirectory())walk(file);else if(file.endsWith('.html')){const before=fs.readFileSync(file,'utf8'),after=clean(before);if(after!==before){changed.push(file);if(!check)fs.writeFileSync(file,after);}}}}walk(root);if(check&&changed.length)throw Error('Legacy promotional components remain in '+changed.length+' files');return changed;}
module.exports={clean,run};
if(require.main===module)console.log(JSON.stringify({metricComponentFilesChanged:run('.',process.argv.includes('--check')).length}));
