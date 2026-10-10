(function(root){
 'use strict';
 function calculate(v){
  const values=[v.months,v.fee,v.implementation,v.monthlyCost,v.monthlyRevenue,v.margin,v.monthlySavings];
  if(values.some(x=>!Number.isFinite(x)||x<0)||v.months<1||!Number.isInteger(v.months)||v.months>120||v.margin>100)throw new Error('Use nonnegative numbers, a margin from 0 to 100, and a whole period from 1 to 120 months.');
  const cost=v.fee+v.implementation+v.monthlyCost*v.months;
  const contribution=v.monthlyRevenue*v.margin/100;
  const benefit=(contribution+v.monthlySavings)*v.months;
  const net=benefit-cost,monthlyNet=contribution+v.monthlySavings-v.monthlyCost;
  if (![cost,benefit,net,monthlyNet].every(Number.isFinite)) throw new Error('These values are too large. Use smaller scenario amounts.');
  return {cost,benefit,net,roi:cost>0?net/cost*100:null,payback:monthlyNet>0?(v.fee+v.implementation)/monthlyNet:null};
 }
 if(typeof module==='object'&&module.exports)module.exports={calculate};
 if(!root.document)return;
 const form=root.document.getElementById('consulting-roi');if(!form)return;
 const result=root.document.getElementById('roi-result');
 const cash=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0});
 const names=['months','fee','implementation','monthlyCost','monthlyRevenue','margin','monthlySavings'];
 function update(){
  try{
   if(names.some(n=>form.elements[n].value.trim()===''))throw new Error('Complete each field; enter zero where appropriate.');
   const v=Object.fromEntries(names.map(n=>[n,Number(form.elements[n].value)]));const r=calculate(v);
   result.textContent='Over '+v.months+' months: modeled contribution and cash savings '+cash.format(r.benefit)+'; total cost '+cash.format(r.cost)+'; net modeled benefit '+cash.format(r.net)+'; ROI '+(r.roi===null?'undefined because cost is zero':r.roi.toFixed(1)+'%')+'. Simple payback: '+(r.payback===null?'not reached under these steady monthly assumptions':r.payback.toFixed(1)+' months from benefit commencement')+'. Scenario only, not a forecast or verified client result.';return true;
  }catch(e){result.textContent=e.message;return false;}
 }
 form.addEventListener('input',update);form.addEventListener('submit',e=>{e.preventDefault();update()});
 root.document.getElementById('roi-print').addEventListener('click',()=>root.print());
 root.document.getElementById('roi-export').addEventListener('click',()=>{
  if(!update())return;const lines=['Consulting ROI scenario',...names.map(n=>n+': '+form.elements[n].value),result.textContent,'Assumes steady benefits from month one; excludes tax, discounting, delays and sale value. Verify each assumption.'];
  const url=URL.createObjectURL(new Blob([lines.join('\n')],{type:'text/plain;charset=utf-8'}));
  const a=root.document.createElement('a');a.href=url;a.download='consulting-roi-scenario.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 });
 update();
})(typeof window==='undefined'?globalThis:window);
