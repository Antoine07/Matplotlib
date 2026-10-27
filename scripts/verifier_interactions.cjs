// JSDOM_PATH peut désigner une installation existante de jsdom.
const {JSDOM}=require(process.env.JSDOM_PATH || 'jsdom');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(root,'docs/qcm/01_graphiques_fiables.html'),'utf8');
const dom=new JSDOM(source,{runScripts:'outside-only',pretendToBeVisual:true,url:'https://cours.local/qcm/01_graphiques_fiables.html'});
const win=dom.window,doc=win.document;
function click(selector){const el=doc.querySelector(selector);assert.ok(el,selector);el.click();}
function answer(i,value){click(`input[name="q${i}"][value="${value}"]`);}
(async()=>{
 win.eval(fs.readFileSync(path.join(root,'docs/assets/cours.js'),'utf8'));
 win.eval(fs.readFileSync(path.join(root,'docs/assets/qcm.js'),'utf8'));
 assert.match(doc.querySelector('#recall-counter').textContent,/1 sur 6/);
 assert.equal(doc.querySelector('#recall-prev').disabled,true);
 click('#recall-next');assert.match(doc.querySelector('#recall-counter').textContent,/2 sur 6/);
 for(let i=0;i<5;i++)click('#recall-next');
 assert.match(doc.querySelector('#recall-counter').textContent,/1 sur 6/);
 click('#quiz [type="submit"]');assert.match(doc.querySelector('#quiz-progress').textContent,/choisissez une réponse/);
 const next=()=>doc.querySelector('#quiz .actions button:nth-child(2)').click();
 for(const [i,value] of [1,2,1,3,0,2,3,1].entries()){
  answer(i,value);
  assert.equal(doc.querySelectorAll('#quiz fieldset')[i].querySelector('.quiz-feedback').hidden,false);
  assert.equal(doc.querySelector(`input[name="q${i}"]`).disabled,true);
  next();
 }
 assert.match(doc.querySelector('#quiz-score').textContent,/8 \/ 8 \(100 %\)/);
 click('#quiz [type="reset"]');await new Promise(r=>setTimeout(r,20));
 assert.equal(doc.querySelector('#quiz fieldset').hidden,false);
 assert.equal(doc.querySelector('#quiz input:checked'),null);
 answer(0,0);assert.equal(doc.querySelector('#quiz .quiz-feedback').classList.contains('incorrect'),true);
 next();
 for(const [i,value] of [2,1,3,0,2,3,1].entries()){answer(i+1,value);next();}
 assert.match(doc.querySelector('#quiz-score').textContent,/7 \/ 8/);
 console.log('OK : navigation flashcards et boucle ; QCM sans réponse, 8/8, reset, erreur, 7/8, verrouillage et feedback.');
 win.close();
})().catch(e=>{console.error(e);process.exitCode=1;win.close()});
