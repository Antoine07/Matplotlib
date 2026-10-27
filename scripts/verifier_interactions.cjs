// JSDOM_PATH peut désigner une installation existante de jsdom.
const {JSDOM}=require(process.env.JSDOM_PATH || 'jsdom');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const cases=[['01_graphiques_fiables',[0,0,1,2,1,3,2,1]],['02_indicateurs',[1,2,2,1,3,0,1,3]]];
(async()=>{
 for(const [slug,answers] of cases){
  const source=fs.readFileSync(path.join(root,`docs/qcm/${slug}.html`),'utf8');
  const dom=new JSDOM(source,{runScripts:'outside-only',pretendToBeVisual:true,url:`https://cours.local/qcm/${slug}.html`});
  const win=dom.window,doc=win.document;
  try{
   const click=s=>{const e=doc.querySelector(s);assert.ok(e,s);e.click()};
   const next=()=>click('#quiz .actions button:nth-child(2)');
   win.eval(fs.readFileSync(path.join(root,'docs/assets/cours.js'),'utf8'));
   win.eval(fs.readFileSync(path.join(root,'docs/assets/qcm.js'),'utf8'));
   assert.match(doc.querySelector('#recall-counter').textContent,/1 sur 6/);
   assert.equal(doc.querySelector('#recall-prev').disabled,true);
   click('#recall-next');assert.match(doc.querySelector('#recall-counter').textContent,/2 sur 6/);
   click('#recall-prev');assert.match(doc.querySelector('#recall-counter').textContent,/1 sur 6/);
   for(let i=0;i<6;i++)click('#recall-next');
   assert.match(doc.querySelector('#recall-counter').textContent,/1 sur 6/);
   click('#quiz [type="submit"]');assert.match(doc.querySelector('#quiz-progress').textContent,/choisissez une réponse/);
   for(const [i,value] of answers.entries()){
    click(`input[name="q${i}"][value="${value}"]`);
    const field=doc.querySelectorAll('#quiz fieldset')[i],feedback=field.querySelector('.quiz-feedback');
    assert.equal(feedback.hidden,false);assert.match(feedback.textContent,/Bonne réponse/);
    assert.equal(field.querySelector('input').disabled,true);next();
   }
   assert.match(doc.querySelector('#quiz-score').textContent,/8 \/ 8 \(100 %\)/);
   click('#quiz [type="reset"]');await new Promise(r=>setTimeout(r,20));
   assert.equal(doc.querySelector('#quiz input:checked'),null);
   for(const [i,value] of answers.entries()){
    click(`input[name="q${i}"][value="${(value+1)%4}"]`);
    const feedback=doc.querySelectorAll('#quiz fieldset')[i].querySelector('.quiz-feedback');
    assert.equal(feedback.hidden,false);assert.equal(feedback.classList.contains('incorrect'),true);
    assert.ok(feedback.textContent.includes(feedback.dataset.explanation));next();
   }
   assert.match(doc.querySelector('#quiz-score').textContent,/0 \/ 8/);
   console.log(`${slug} : flashcards, réponse obligatoire, feedback correct/incorrect sur 8 questions, reset, scores 8/8 et 0/8 OK.`);
  }finally{win.close()}
 }
})().catch(e=>{console.error(e);process.exitCode=1});
