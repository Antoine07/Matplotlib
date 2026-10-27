"use strict";
const anchors = [...document.querySelectorAll('.course-nav a[href^="#"]')];
const sections = anchors.map(a => document.querySelector(a.hash)).filter(Boolean);
let scheduled = false;
function updateNavigation(){let current=sections[0];sections.forEach(s=>{if(s.getBoundingClientRect().top<=180)current=s});if(current)anchors.forEach(a=>{if(a.hash==='#'+current.id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')});scheduled=false;}
window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(updateNavigation)}},{passive:true});updateNavigation();
const cards=[...document.querySelectorAll('.recall-card')];
if(cards.length){let index=0;const counter=document.querySelector('#recall-counter'),prev=document.querySelector('#recall-prev'),next=document.querySelector('#recall-next');document.querySelector('.recall-controls').hidden=false;counter.hidden=false;function show(){cards.forEach((c,i)=>{c.hidden=i!==index;c.querySelector('details').open=false});counter.textContent=`Carte ${index+1} sur ${cards.length}`;prev.disabled=index===0;next.textContent=index===cards.length-1?'Reprendre les cartes ↺':'Suivante →'}prev.addEventListener('click',()=>{index=Math.max(0,index-1);show()});next.addEventListener('click',()=>{index=(index+1)%cards.length;show()});show();}
