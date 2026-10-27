"use strict";
const form=document.querySelector('#quiz');
if(form){
  const questions=[...form.querySelectorAll('fieldset')];
  const progress=form.querySelector('#quiz-progress');
  const next=form.querySelector('#quiz-next');
  const scoreBox=form.querySelector('#quiz-score');
  const restart=form.querySelector('#quiz-restart');
  let current=0, correct=0;
  questions.forEach((fieldset,index)=>{
    fieldset.hidden=index!==0;
    fieldset.querySelectorAll('input[type="radio"]').forEach(input=>input.addEventListener('change',()=>{
      if(index!==current||fieldset.dataset.answered)return;
      const answer=fieldset.querySelector('input:checked');
      const expected=fieldset.querySelector(`input[value="${fieldset.dataset.answer}"]`);
      const feedback=fieldset.querySelector('.quiz-feedback');
      const isCorrect=answer.value===fieldset.dataset.answer;
      if(isCorrect)correct++;
      fieldset.dataset.answered='true';
      fieldset.querySelectorAll('input').forEach(option=>option.disabled=true);
      feedback.hidden=false;
      feedback.className=`quiz-feedback ${isCorrect?'correct':'incorrect'}`;
      feedback.textContent=isCorrect
        ?`Bonne réponse : ${expected.nextElementSibling.textContent}. ${fieldset.dataset.why}`
        :`Votre réponse : ${answer.nextElementSibling.textContent}. Réponse attendue : ${expected.nextElementSibling.textContent}. ${fieldset.dataset.why}`;
      next.hidden=false;
      next.textContent=index===questions.length-1?'Voir mon résultat':'Question suivante →';
      progress.textContent=`Question ${index+1} sur ${questions.length} · correction affichée`;
    }));
  });
  next.addEventListener('click',()=>{
    if(!questions[current]||!questions[current].dataset.answered)return;
    questions[current].hidden=true;
    current++;
    next.hidden=true;
    if(current<questions.length){
      questions[current].hidden=false;
      progress.textContent=`Question ${current+1} sur ${questions.length}`;
      questions[current].querySelector('input[type="radio"]').focus();
      return;
    }
    progress.hidden=true;
    scoreBox.hidden=false;
    restart.hidden=false;
    const percent=Math.round(correct/questions.length*100);
    scoreBox.textContent=`Résultat : ${correct} / ${questions.length} (${percent} %). ${percent<70?'Reprenez les exemples du cours avant de poursuivre.':'Vous pouvez revoir les explications en recommençant le QCM.'}`;
  });
  form.addEventListener('reset',()=>setTimeout(()=>{
    current=0;correct=0;
    progress.hidden=false;
    progress.textContent=`Question 1 sur ${questions.length}`;
    scoreBox.hidden=true;scoreBox.textContent='';
    restart.hidden=true;
    next.hidden=true;
    questions.forEach((fieldset,index)=>{
      delete fieldset.dataset.answered;
      fieldset.hidden=index!==0;
      fieldset.querySelectorAll('input').forEach(input=>input.disabled=false);
      const feedback=fieldset.querySelector('.quiz-feedback');
      feedback.hidden=true;feedback.className='quiz-feedback';feedback.textContent='';
    });
  },0));
}
