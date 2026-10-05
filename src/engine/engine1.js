

function saveDarbiProgress(level,correct,total){try{var pk='darbi_progress';var all=JSON.parse(localStorage.getItem(pk)||'{}');var key=RESUME_KEY.replace('quranResume_','');var pct=total>0?Math.round((correct/total)*100):0;if(!all[key])all[key]={};var prev=(all[key][level]&&all[key][level].score)||0;all[key][level]={done:pct>=70,score:Math.max(pct,prev),at:new Date().toISOString()};all[key].lastVisited=new Date().toISOString();localStorage.setItem(pk,JSON.stringify(all));}catch(e){}}






let currentLevel=null,statuses=[],wrongIndices=[],questions=[],qIndex=0,correctCount=0,wrongCount=0;let wCorrect=0,wTotal=0;
;







function wordDiff(userVal,correctAnswer,q){const nm=s=>{if(!s)return'';return s.replace(/ـ([ٕٔ])([ً-ٟ])/g,'ـ$2$1').replace(/ـِ[ٕٔ]/g,'ي').replace(/يٓ?ـَٔ/g,'ي').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـ/g,'').replace(/[\u064B-\u065F\u0610-\u061A\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED\u08F0-\u08F2]/g,'').replace(/[ىی]ٰ(?=\S)/g,'ا').replace(/[ىی]ٰ/g,'ي').replace(/وٱ(?!ل)/g,'و').replace(/(?<=^|\s)وا(?=سجد|قترب|دخل|دعو|ذكر|رحم|ستغفر|ستغن|غفر|عف|نحر|تق|ختلاف|مر[أا]|تبع|سمع|ستكبر|ستعين|ركع|صبر|صل|جتنب|هبط|ستبشر|ستقم|ضرب|عتصم|ئتلف|بتغ|حذر|شرب|صفح|تخذ|علم|رزق|جعل|خش|شكر|نظر|بعث|قتل|نصر|ستشهد|علم|رزق|جعل|خش|شكر|نظر|بعث|قتل|نصر|ستشهد|جتب|متاز)/g,'و').replace(/اٰ/g,'ا').replace(/نٰ/g,'نا').replace(/ٰ/g,'ا').replace(/[آأإٱا]/g,'ا').replace(/ها[ؤو]لاء|ها[ؤو]لا(?!\S)/g,'هالا').replace(/ه[ؤو]لاء|ه[ؤو]لا(?!\S)/g,'هالا').replace(/^اولايك$/,'اوليك').replace(/^هاولا$/,'هالا').replace(/^يوتيني$/,'يوتين').replace(/ئ(?=و)/g,'').replace(/ئ/g,'ي').replace(/ؤ/g,'و').replace(/ء/g,'').replace(/ة/g,'ه').replace(/[ىی]/g,'ي').replace(/ه[ۥۦ]/g,'ه').replace(/ۦ(?=\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'').replace(/واه(?=\s|$)/g,'اه').replace(/رحمان/g,'رحمن').replace(/مولانا/g,'مولنا').replace(/يا ايها/g,'يايها').replace(/يا ايتها/g,'يايتها').replace(/الاه/g,'اله').replace(/ارايت/g,'اريت').replace(/هاذا/g,'هذا').replace(/ذالك/g,'ذلك').replace(/لاكن/g,'لكن').replace(/اولك/g,'اولاك').replace(/اولااك/g,'اولاك').replace(/ياايها/g,'يايها').replace(/ياايتها/g,'يايتها').replace(/نب/g,'مب').replace(/لل/g,'ل').replace(/(.)\1+/g,'$1').replace(/\s+/g,' ').replace(/(?<=^|\s)وا(?=سجد|قترب|دخل|دعو|ذكر|رحم|ستغفر|ستغن|غفر|عف|نحر|تق|ختلاف|مر[أا]|تبع|سمع|ستكبر|ستعين|ركع|صبر|صل|جتنب|هبط|ستبشر|ستقم|ضرب|عتصم|ئتلف|بتغ|حذر|شرب|صفح|تخذ|علم|رزق|جعل|خش|شكر|نظر|بعث|قتل|نصر|ستشهد|علم|رزق|جعل|خش|شكر|نظر|بعث|قتل|نصر|ستشهد|جتب|متاز)/g,'و').trim();};const uWords=collapseMuqattaat(userVal.trim().split(/\s+/),correctAnswer),cWords=correctAnswer.split(/\s+/).filter(w=>nm(w)!==''),n=cWords.length,m=uWords.length;const dp=Array.from({length:n+1},()=>new Array(m+1).fill(0));for(let i=1;i<=n;i++)for(let j=1;j<=m;j++){if(nm(cWords[i-1])===nm(uWords[j-1]))dp[i][j]=dp[i-1][j-1]+1;else dp[i][j]=Math.max(dp[i-1][j],dp[i][j-1]);}const aligned=[];let i=n,j=m;while(i>0||j>0){if(i>0&&j>0&&nm(cWords[i-1])===nm(uWords[j-1])){aligned.push({ref:cWords[i-1],ok:true});i--;j--;}else if(j>0&&(i===0||dp[i][j-1]>=dp[i-1][j])){aligned.push({ref:uWords[j-1],user:uWords[j-1],extra:true});j--;}else{aligned.push({ref:cWords[i-1],ok:false});i--;}}aligned.reverse();const correct=aligned.filter(x=>x.ok).length;const extra=aligned.filter(x=>x.extra).length;window._lastDiff={matched:correct,total:n,extra:extra};let __refI=-1;const html=aligned.map(x=>{const __seg=x.extra?`<span style="color:#7a4a00;background:#ffe0a3;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;text-decoration:line-through;" translate="no" class="notranslate">${x.ref}</span>`:x.ok?`<span style="color:#155724;background:#c3e6cb;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;font-weight:bold;" translate="no" class="notranslate">${x.ref}</span>`:`<span style="color:#fff;background:#c0392b;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;" translate="no" class="notranslate">${x.ref}</span>`;if(!x.extra)__refI++;return __seg+((!x.extra&&q&&q.ayah!=null&&__refI===n-1)?' <span class="ayah-end" translate="no">﴿'+toArabicNum(q.ayah)+'﴾</span>':'');}).join(' ');return `<div style="margin-bottom:6px;font-size:13px;color:var(--text-soft);">${darbiT('feedback.words_correct_count',{correct:correct,total:n})}${extra?darbiT('feedback.words_extra',{extra:extra}):''}</div><div style="font-size:18px;line-height:2.5;direction:rtl;text-align:right;">${html}</div>`;}
function toArabicNum(n){return n;}
function updateBadges(){
  document.getElementById('qnum-badge').innerHTML=`${darbiT('quiz.q_number_short',{cur:toArabicNum(qIndex+1)})}<br>${toArabicNum(questions.length)}`;
  const wb=document.getElementById('wrong-badge');
  wb.innerHTML=`${toArabicNum(wrongCount)} ✗<br>${darbiT('quiz.stat_wrong')}`;
  wb.className='stat-badge '+(wrongCount>0?'badge-wrong':'badge-neutral');
  const cb=document.getElementById('correct-badge');
  cb.innerHTML=`${toArabicNum(correctCount)} ✓<br>${darbiT('quiz.stat_correct')}`;
  cb.className='stat-badge '+(correctCount>0?'badge-correct':'badge-neutral');
}
function selectLevel(lvl){if(lvl==='order'){currentLevel=lvl;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));var __ob=document.getElementById('btn-order');if(__ob)__ob.classList.add('active');document.getElementById('start-btn').classList.add('ready');document.getElementById('total-q').textContent=toArabicNum(AYAT.length);return;}currentLevel=lvl;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));document.getElementById('btn-'+lvl).classList.add('active');document.getElementById('start-btn').classList.add('ready');if(lvl==='order'){document.getElementById('total-q').textContent=toArabicNum(AYAT.length);}else{document.getElementById('total-q').textContent=toArabicNum((lvl==='easy'?EASY_Q:lvl==='medium'?MEDIUM_Q:HARD_Q).length);}}
function startQuiz(){if(currentLevel==='order'){startOrderQuiz();return;}if(!currentLevel)return;questions=currentLevel==='easy'?[...EASY_Q]:currentLevel==='medium'?[...MEDIUM_Q]:[...HARD_Q];qIndex=correctCount=wrongCount=0;wCorrect=wTotal=0;statuses=questions.map(()=>'pending');wrongIndices=[];document.getElementById('resume-banner').style.display='none';document.getElementById('level-card').style.display='none';document.getElementById('quiz-area').style.display='block';showQuestion();}
function shuffle(arr){for(let i=arr.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]];}return arr;}
function renderDotProgress(){const wrap=document.getElementById('dot-progress');if(!wrap)return;wrap.innerHTML='';statuses.forEach((st,i)=>{const dot=document.createElement('span');dot.className='q-dot'+(i===qIndex?' current':st!=='pending'?' '+st:'');wrap.appendChild(dot);});}
function saveResumeState(){try{localStorage.setItem(RESUME_KEY,JSON.stringify({level:currentLevel,qIndex,correctCount,wrongCount,statuses,wrongIndices,date:Date.now()}));}catch(e){}}
function dismissResume(){try{localStorage.removeItem(RESUME_KEY);}catch(e){}document.getElementById('resume-banner').style.display='none';}
function resumeQuiz(){let saved=null;try{saved=JSON.parse(localStorage.getItem(RESUME_KEY));}catch(e){}if(!saved)return;currentLevel=saved.level;questions=currentLevel==='easy'?[...EASY_Q]:currentLevel==='medium'?[...MEDIUM_Q]:[...HARD_Q];qIndex=saved.qIndex;correctCount=saved.correctCount;wrongCount=saved.wrongCount;statuses=saved.statuses||questions.map(()=>'pending');wrongIndices=saved.wrongIndices||[];document.getElementById('resume-banner').style.display='none';document.getElementById('level-card').style.display='none';document.getElementById('quiz-area').style.display='block';showQuestion();}
function showQuestion(){const q=questions[qIndex];updateBadges();document.getElementById('progress-fill').style.width=(qIndex/questions.length)*100+'%';document.getElementById('q-number').textContent=darbiT('quiz.q_number',{cur:toArabicNum(qIndex+1),total:toArabicNum(questions.length)});var __qt=document.getElementById('q-text');__qt.textContent=q.q;if(currentLevel==='hard'){__qt.classList.remove('notranslate');__qt.removeAttribute('translate');}else{__qt.classList.add('notranslate');__qt.setAttribute('translate','no');}const fb=document.getElementById('feedback');fb.style.display='none';fb.className='feedback';const prevBtn=document.getElementById('prev-btn');prevBtn.disabled=(qIndex===0);prevBtn.style.opacity=(qIndex===0)?'0.4':'1';document.getElementById('skip-btn').style.display='';document.getElementById('next-btn').style.display='none';renderDotProgress();const qpn=document.getElementById('quiz-page-nav');if(qpn)qpn.style.display=(qIndex===questions.length-1)?'flex':'none';const zone=document.getElementById('answer-zone');zone.innerHTML='';if(currentLevel==='easy')renderEasy(q,zone);else if(currentLevel==='medium')renderMedium(q,zone);else renderHard(q,zone);}
function renderEasy(q,zone){const div=document.createElement('div');div.className='choices';shuffle(q.choices.map((c,i)=>({text:c,idx:i}))).forEach(opt=>{const btn=document.createElement('button');btn.className='choice-btn';btn.textContent=opt.text;btn.classList.add('notranslate');btn.setAttribute('translate','no');btn.onclick=()=>checkMCQ(opt.idx,q.answer,btn);div.appendChild(btn);});zone.appendChild(div);}
function renderMedium(q,zone){const ta=document.createElement('textarea');ta.className='answer-input';ta.placeholder=darbiT('quiz.medium_placeholder');ta.id='user-input';zone.appendChild(ta);const sub=document.createElement('button');sub.className='submit-btn';sub.textContent=darbiT('quiz.submit_check');sub.onclick=()=>checkText(q);zone.appendChild(sub);setTimeout(()=>{const el=document.getElementById('user-input');if(el)el.focus();},100);}
function renderHard(q,zone){
  const ayahNum=document.createElement('div');ayahNum.style.cssText='text-align:center;font-size:13px;color:var(--text-soft);margin-bottom:8px;';ayahNum.textContent=((typeof PAGE_OPTIONS!=='undefined'&&PAGE_OPTIONS.hardLabel==='text')||q.ayah==null)?(function(){const mm=String(q.q||'').match(/^اكتب\s+(\S+\s+\d+(?:[–-]\d+)?)/);return mm?mm[1]:'';})():darbiT('quiz.ayah_label',{n:toArabicNum(q.ayah)});zone.appendChild(ayahNum);
  const modeRow=document.createElement('div');modeRow.style.cssText='display:flex;gap:10px;margin-bottom:12px;';
  const bVoice=document.createElement('button');bVoice.textContent=darbiT('voice.record_btn');bVoice.style.cssText='flex:1;padding:11px;border-radius:11px;font-size:15px;font-family:inherit;cursor:pointer;background:var(--accent);color:#fff;border:1.5px solid var(--accent);';
  const bText=document.createElement('button');bText.textContent=darbiT('voice.text_btn');bText.style.cssText='flex:1;padding:11px;border-radius:11px;font-size:15px;font-family:inherit;cursor:pointer;background:var(--surface2);color:var(--text);border:1.5px solid var(--border);';
  modeRow.appendChild(bVoice);modeRow.appendChild(bText);zone.appendChild(modeRow);
  const vZone=document.createElement('div');zone.appendChild(vZone);
  const tZone=document.createElement('div');tZone.style.display='none';zone.appendChild(tZone);
  let _rec=null,_recog=false,_words=[],_cur='',_sel=null;
  const _SpeechAPI=window.SpeechRecognition||window.webkitSpeechRecognition;
  const _secure=location.protocol==='https:'||location.hostname==='localhost';
  const recBtn=document.createElement('button');recBtn.style.cssText='width:100%;padding:14px;border-radius:12px;font-size:16px;font-family:inherit;cursor:pointer;border:2px solid var(--border);background:var(--surface2);color:var(--text);margin-bottom:8px;';recBtn.textContent=darbiT('voice.press_to_record');
  const txBox=document.createElement('div');txBox.className='rec-transcript';
  const clrBtn=document.createElement('button');clrBtn.style.cssText='width:100%;padding:9px;border-radius:10px;font-size:14px;font-family:inherit;cursor:pointer;border:1.5px solid var(--wrong-border);background:var(--wrong-bg);color:var(--wrong-text);margin-bottom:8px;display:none;';clrBtn.textContent=darbiT('voice.clear_btn');
  const vSub=document.createElement('button');vSub.className='submit-btn';vSub.textContent=darbiT('quiz.submit_check');vSub.style.display='none';
  vZone.appendChild(recBtn);vZone.appendChild(txBox);vZone.appendChild(clrBtn);vZone.appendChild(vSub);
  ;
function _fixWords(words){return _fixWordsCore(words,(typeof q!=='undefined'&&q&&q.answer)||'');}
        function _addWords(nw){
    if(!nw||!nw.length)return;
    nw=_fixWords(nw);
    if(_sel!==null&&_sel<_words.length){_words.splice(_sel,1);_words.splice(_sel,0,...nw);_sel=null;}
    else{_words=_fixWords([].concat(_words,nw));}
  }

      function renderWords(){if(!_words.length&&!_cur){txBox.style.display='none';clrBtn.style.display='none';vSub.style.display='none';return;}txBox.style.display='block';txBox.innerHTML='';
    if(_sel!==null&&_sel>=_words.length)_sel=null;
    if(_sel!==null){
      const bar=document.createElement('div');
      bar.style.cssText='width:100%;box-sizing:border-box;background:var(--hint-btn-bg);border:1px solid var(--gold);border-radius:8px;padding:6px 10px;margin-bottom:8px;font-size:14px;display:flex;align-items:center;gap:8px;justify-content:space-between;';
      const t=document.createElement('span');
      t.appendChild(document.createTextNode(darbiT('order.selected_label')));
      const b=document.createElement('b');b.className='notranslate';b.setAttribute('translate','no');
      b.textContent=_words[_sel];t.appendChild(b);
      t.appendChild(document.createTextNode(darbiT('order.selected_suffix')));
      const x=document.createElement('button');x.type='button';x.textContent=darbiT('order.delete_btn');
      x.style.cssText='background:var(--wrong-border);color:#fff;border:0;border-radius:6px;padding:3px 10px;font-size:13px;cursor:pointer;font-family:inherit;flex:0 0 auto;';
      x.onclick=()=>{_words.splice(_sel,1);_sel=null;renderWords();};
      bar.appendChild(t);bar.appendChild(x);txBox.appendChild(bar);
    }
_words.forEach((w,i)=>{const span=document.createElement('span');span.className='rec-word';span.style.cssText='background:var(--surface-hover);border-radius:4px;padding:2px 5px;margin:2px;cursor:pointer;';span.textContent=w;
      if(i===_sel){span.style.outline='2px solid var(--gold)';span.style.background='var(--hint-btn-bg)';span.style.fontWeight='700';span.title=darbiT('order.deselect_title');}
      else{span.title=darbiT('order.select_title');}
      span.onclick=()=>{_sel=(_sel===i)?null:i;renderWords();};txBox.appendChild(span);});if(_cur){const cur=document.createElement('span');cur.style.cssText='color:var(--text-soft);font-style:italic;';cur.textContent=' '+_cur;txBox.appendChild(cur);}clrBtn.style.display='block';vSub.style.display=_words.length?'block':'none';}
  function _setB(s){recBtn.disabled=false;if(s==='rec'){recBtn.textContent=darbiT('voice.recording');recBtn.style.background='#e74c3c';recBtn.style.color='#fff';recBtn.style.borderColor='#e74c3c';}else if(s==='pause'){recBtn.textContent=darbiT('voice.paused');recBtn.style.background='#e67e22';recBtn.style.color='#fff';recBtn.style.borderColor='#e67e22';}else{recBtn.textContent=darbiT('voice.press_to_record');recBtn.style.background='var(--surface2)';recBtn.style.color='var(--text)';recBtn.style.borderColor='var(--border)';}}
  function _mkRec(){const r=new _SpeechAPI();r.lang='ar-SA';r.continuous=true;r.interimResults=false;r.onstart=()=>{_recog=true;_cur='';_setB('rec');renderWords();};r.onresult=e=>{for(let i=e.resultIndex;i<e.results.length;i++){if(e.results[i].isFinal){_addWords(e.results[i][0].transcript.trim().split(/\s+/));_cur='';}}renderWords();};r.onerror=e=>{if(e.error!=='no-speech'&&e.error!=='aborted'){_recog=false;_setB(_words.length?'pause':'idle');}};r.onend=()=>{_recog=false;if(_cur){_addWords(_cur.trim().split(/\s+/));_cur='';}renderWords();_setB(_words.length?'pause':'idle');};return r;}
  clrBtn.onclick=()=>{if(_recog){try{_rec.stop();}catch(e){}_recog=false;}_rec=null;_words=[];_cur='';_sel=null;txBox.innerHTML='';txBox.style.display='none';clrBtn.style.display='none';vSub.style.display='none';_setB('idle');recBtn.disabled=false;};
  vSub.onclick=()=>{const t=_words.join(' ').trim();if(!t)return;vSub.disabled=true;checkTextVal(q,t);setTimeout(()=>{recBtn.disabled=false;vSub.disabled=false;},300);};
  if(_SpeechAPI&&_secure){recBtn.onclick=()=>{if(_recog){_recog=false;try{_rec.stop();}catch(e){}_setB('pause');return;}_rec=_mkRec();try{_rec.start();}catch(e){_setB(_words.length?'pause':'idle');}};}else{recBtn.textContent=_secure?darbiT('voice.not_supported'):darbiT('voice.https_only');recBtn.disabled=true;recBtn.style.opacity='0.65';}
  function activateVoice(){vZone.style.display='';tZone.style.display='none';bVoice.style.background='var(--accent)';bVoice.style.color='#fff';bText.style.background='var(--surface2)';bText.style.color='var(--text)';if(_SpeechAPI&&_secure&&!_recog){_rec=_mkRec();try{_rec.start();}catch(e){_setB('idle');}}}
  function activateText(){vZone.style.display='none';tZone.style.display='';bText.style.background='var(--accent)';bText.style.color='#fff';bVoice.style.background='var(--surface2)';bVoice.style.color='var(--text)';if(_recog){try{_rec.stop();}catch(e){}_recog=false;}setTimeout(()=>{const el=document.getElementById('user-input');if(el)el.focus();},100);}
  bVoice.onclick=activateVoice;bText.onclick=activateText;
  const ta2=document.createElement('textarea');ta2.className='answer-input';ta2.placeholder=darbiT('quiz.hard_placeholder');ta2.id='user-input';tZone.appendChild(ta2);
  const tSub=document.createElement('button');tSub.className='submit-btn';tSub.textContent=darbiT('quiz.submit_check');tSub.onclick=()=>checkText(q);tZone.appendChild(tSub);
  const hBox=document.createElement('div');hBox.className='hint-box';zone.appendChild(hBox);
  const hBtn=document.createElement('button');hBtn.className='hint-btn';hBtn.textContent=darbiT('hint.btn');hBtn.onclick=()=>{hBox.textContent=q.answer.split(' ').filter(w=>normalize(w)!=='').slice(0,3).join(' ')+' ...';hBox.classList.add('notranslate');hBox.setAttribute('translate','no');hBox.style.display='block';hBtn.disabled=true;hBtn.style.opacity='0.5';};zone.appendChild(hBtn);
}
function _pctNow(){const st=window._lastDiff||{};let a='';if(st.total){const wp=Math.round(st.matched*100/st.total);a=`<div style="margin-top:6px;font-size:14px;opacity:.9;">${darbiT('feedback.accuracy_line',{pct:wp,matched:st.matched,total:st.total})}</div>`;}// السطر التاني يظهر بس لو فيه أسئلة سابقة — من غير كده الرقمين واحد
if(!wTotal||wTotal===st.total)return a;const p=Math.round(wCorrect*100/wTotal);return a+`<div style="margin-top:2px;font-size:13px;opacity:.75;">${darbiT('feedback.accuracy_total_line',{pct:p,correct:wCorrect,total:wTotal})}</div>`;}

function checkTextVal(q,userVal){
  const fb=document.getElementById('feedback');
  const _sk=document.getElementById('skip-btn');if(_sk)_sk.style.display='none';
  const _nx=document.getElementById('next-btn');if(_nx)_nx.style.display='block';
  // بعض الصفحات بتلفّ التطبيع بدالة زيادة (الحروف المقطعة)
  const _pre=(typeof normalizeHurufMuqattaa==='function')?normalizeHurufMuqattaa:(x=>x);
  const userNorm=normalize(_pre(userVal));
  const ansNorm=normalize(_pre(q.answer));
  const _dh=wordDiff(userVal,q.answer,q);
  const _st=window._lastDiff||{};
  if(_st.total){wCorrect+=_st.matched;wTotal+=_st.total;}
  // الحكم من نفس مصدر العرض: تطابق كامل أو كل الكلمات مطابقة ومفيش زيادة
  const _ok=(userNorm===ansNorm)||(_st.total>0&&_st.matched===_st.total&&!_st.extra);
  if(_ok){
    correctCount++;statuses[qIndex]='correct';
    fb.className='feedback correct';
    fb.innerHTML=darbiT('feedback.correct_full');
    if(currentLevel==='hard'){const __qi=qIndex;setTimeout(()=>{if(qIndex===__qi)nextQuestion();},3500);}
  }else{
    wrongCount++;statuses[qIndex]='wrong';wrongIndices.push(qIndex);if(window.DarbiExtra)DarbiExtra.recordMiss(currentLevel,qIndex,questions[qIndex]);
    fb.className='feedback wrong';
    fb.innerHTML=darbiT('feedback.wrong_full_prefix')+'<br><span style="font-size:18px;line-height:2.2;direction:rtl;display:block;text-align:right;">'+_dh+'</span>';
  }
  fb.style.display='block';
  if(typeof updateBadges==='function')updateBadges();
  if(typeof renderDotProgress==='function')renderDotProgress();
  if(typeof saveResumeState==='function')saveResumeState();
}
/* ===== حارس الإملاء (الكتابة فقط) =====
   «ٱلَّذِينَ» بلام واحدة هي الرسم الوحيد في المصحف، لكن تقليص
   الحروف المكرّرة جوّه normalize بيخلّي «اللذين» تعدّي كإجابة صحيحة.
   القاعدة دي لازم تفضل زي ما هي عشان التلاوة الصوتية (بتصلّح
   «إنن» → «إنَّ»)، فبدل ما نلمسها بنعلّم الكلمة المكتوبة غلط بفاصل
   صفري العرض U+200B قبل المقارنة: بيمنع التطابق من غير ما يغيّر
   شكل الكلمة قدام المستخدم. الصوت مابيمرّش من هنا فبيفضل متساهل. */

function markBadSpelling(t){
  return String(t||'').trim().split(/\s+/).map(function(w){
    const bare=w.replace(/[\u064B-\u065F\u0610-\u061A\u06D6-\u06ED\u08F0-\u08F2\u0640\u200B-\u200F]/g,'').replace(/[آأإٱ]/g,'ا').replace(/[ىی]/g,'ي');
    return BAD_SPELL.test(bare)?w+'\u200B':w;
  }).join(' ');
}
function checkText(q){const input=document.getElementById('user-input');const userVal=input?input.value.trim():'';if(!userVal)return;if(input)input.disabled=true;document.querySelectorAll('.submit-btn').forEach(s=>s.disabled=true);checkTextVal(q,(typeof markBadSpelling==='function')?markBadSpelling(userVal):userVal);}
function checkMCQ(chosen,correct,btn){wTotal++;if(chosen===correct)wCorrect++;document.querySelectorAll('.choice-btn').forEach(b=>b.disabled=true);const fb=document.getElementById('feedback');const _ans=questions[qIndex].choices[correct];if(chosen===correct){if(btn)btn.classList.add('correct');correctCount++;statuses[qIndex]='correct';fb.className='feedback correct';fb.innerHTML=darbiT('feedback.correct_mcq');const __qi=qIndex;setTimeout(()=>{if(qIndex===__qi)nextQuestion();},2200);}else{if(btn)btn.classList.add('wrong');wrongCount++;statuses[qIndex]='wrong';wrongIndices.push(qIndex);if(window.DarbiExtra)DarbiExtra.recordMiss(currentLevel,qIndex,questions[qIndex]);document.querySelectorAll('.choice-btn').forEach(b=>{if(b.textContent===_ans)b.classList.add('correct');});fb.className='feedback wrong';fb.innerHTML=darbiT('feedback.wrong_mcq_prefix')+'<span class="notranslate" translate="no">'+_ans+'</span>';}fb.style.display='block';document.getElementById('skip-btn').style.display='none';document.getElementById('next-btn').style.display='block';if(typeof updateBadges==='function')updateBadges();if(typeof renderDotProgress==='function')renderDotProgress();if(typeof saveResumeState==='function')saveResumeState();}
function skipQuestion(){const q=questions[qIndex];const fb=document.getElementById('feedback');wTotal+=(currentLevel==='easy'?1:String(q.answer||'').trim().split(/\s+/).filter(Boolean).length||1);if(currentLevel==='easy'){document.querySelectorAll('.choice-btn').forEach(b=>{b.disabled=true;if(b.textContent===q.choices[q.answer])b.classList.add('correct');});fb.className='feedback wrong';fb.innerHTML=darbiT('feedback.skip_prefix')+' <span class="notranslate" translate="no">'+q.choices[q.answer]+'</span>';}else{const inp=document.getElementById('user-input');if(inp)inp.disabled=true;document.querySelectorAll('.submit-btn').forEach(s=>s.disabled=true);fb.className='feedback wrong';fb.innerHTML=darbiT('feedback.skip_prefix')+'<br><span style="font-size:18px;line-height:2.2;direction:rtl;display:block;text-align:right;" class="notranslate" translate="no">'+q.answer+'</span>';}wrongCount++;statuses[qIndex]='wrong';wrongIndices.push(qIndex);if(window.DarbiExtra)DarbiExtra.recordMiss(currentLevel,qIndex,questions[qIndex]);fb.style.display='block';document.getElementById('skip-btn').style.display='none';document.getElementById('next-btn').style.display='block';if(typeof updateBadges==='function')updateBadges();if(typeof renderDotProgress==='function')renderDotProgress();if(typeof saveResumeState==='function')saveResumeState();}
function prevQuestion(){if(qIndex===0)return;qIndex--;showQuestion();}
function nextQuestion(){qIndex++;if(qIndex>=questions.length)showResult();else showQuestion();}
function showResult(){document.getElementById('quiz-area').style.display='none';const _cf=(correctCount===questions.length)?45:((correctCount/questions.length)>=0.8?22:0);if(_cf&&typeof spawnConfetti==='function')setTimeout(()=>spawnConfetti(_cf),260);document.getElementById('result-area').style.display='block';const pct=wTotal?Math.round(wCorrect*100/wTotal):0;document.getElementById('result-score').textContent=darbiT('result.score_line',{wc:toArabicNum(wCorrect),wt:toArabicNum(wTotal),pct:toArabicNum(pct),cc:toArabicNum(correctCount),qt:toArabicNum(questions.length)});let icon,title,msg,stars;if(pct===100){icon='🌟';title=darbiT('result.perfect_title');msg=darbiT('result.perfect_msg');stars='★★★';}else if(pct>=80){icon='✨';title=darbiT('result.great_title');msg=darbiT('result.great_msg');stars='★★☆';}else if(pct>=60){icon='📖';title=darbiT('result.good_title');msg=darbiT('result.good_msg');stars='★☆☆';}else{icon='🌱';title=darbiT('result.weak_title');msg=darbiT('result.weak_msg');stars='☆☆☆';}document.getElementById('result-icon').textContent=icon;document.getElementById('result-title').textContent=title;document.getElementById('result-msg').textContent=msg;
  const stEl=document.getElementById('result-stars');if(stEl)stEl.textContent=stars;document.getElementById('progress-fill').style.width='100%';updateBadges();saveDarbiProgress(currentLevel,correctCount,questions.length);try{localStorage.removeItem(RESUME_KEY);}catch(e){}const rb=document.getElementById('review-mistakes-btn');if(rb)rb.style.display=(wrongIndices.length>0?'inline-block':'none');if(pct===100)spawnConfetti();}
function returnToLevels(){_resetBadges();document.getElementById('quiz-area').style.display='none';document.getElementById('order-area').style.display='none';document.getElementById('level-card').style.display='block';currentLevel=null;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));document.getElementById('start-btn').classList.remove('ready');document.getElementById('total-q').textContent='-';document.getElementById('wrong-badge').innerHTML='0 ✗<br>'+darbiT('quiz.stat_wrong');document.getElementById('correct-badge').innerHTML='0 ✓<br>'+darbiT('quiz.stat_correct');document.getElementById('qnum-badge').innerHTML=darbiT('quiz.q_number_short',{cur:1})+'<br>-';document.getElementById('progress-fill').style.width='0%';}
function _resetBadges(){const wb=document.getElementById('wrong-badge');const cb=document.getElementById('correct-badge');const qb=document.getElementById('qnum-badge');if(wb){wb.className='stat-badge badge-neutral';}if(cb){cb.className='stat-badge badge-neutral';}if(qb){qb.className='stat-badge badge-neutral';}}
function retryQuiz(){_resetBadges();document.getElementById('result-area').style.display='none';document.getElementById('level-card').style.display='block';currentLevel=null;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));document.getElementById('start-btn').classList.remove('ready');document.getElementById('total-q').textContent='-';document.getElementById('wrong-badge').innerHTML='0 ✗<br>'+darbiT('quiz.stat_wrong');document.getElementById('correct-badge').innerHTML='0 ✓<br>'+darbiT('quiz.stat_correct');document.getElementById('qnum-badge').innerHTML=darbiT('quiz.q_number_short',{cur:1})+'<br>-';document.getElementById('progress-fill').style.width='0%';}
let orderPlaced=[],orderCursor=0,orderPoolOrder=[],orderSelected=-1;

/*OHJS v5*/
/* ===== لوحة شرح الترتيب — عرض متحرك (يظهر تلقائيًا أول مرة فقط) ===== */
/* توقيت العرض بالملّي ثانية — كل الإيقاع من السطر ده:
   read = وقفة القراية قبل أي حركة | move = حركة المؤشّر | press = الضغطة
   hold = وقفة بعد التغيير عشان العين تشوف النتيجة
   link = وقفة أقصر بين ضغطتين في نفس الخطوة (الشرح واحد فمش محتاج قراية تاني) */
const OH_MS={read:4400,move:1100,press:600,hold:3400,link:1800};
const ORDER_HELP_KEY='darbi_order_help_seen';
function OH_SEG_AT(i){return [darbiT('oh.seg1'),darbiT('oh.seg2'),darbiT('oh.seg3')][i];}
function ohAr(n){return typeof toArabicNum==='function'?toArabicNum(n):String(n);}
function ohNum(i){return '﴿'+ohAr(i+1)+'﴾';}
function ohEmpty(p,f){for(let i=f;i<p.length;i++)if(p[i]===null)return i;for(let i=0;i<p.length;i++)if(p[i]===null)return i;return -1;}
function ohS0(){return {placed:[null,null,null],cursor:0,selected:-1,pool:[1,0,2]};}
let ohSt=ohS0(),ohStep=0,ohTap=0,ohTimer=null,ohPlaying=false,ohFlash=null;
/* كل خطوة = شرح واحد + ضغطة أو أكتر (taps). الخطوة اللي فيها ضغطتين
   بتاخد وقفة قراية واحدة بس في أولها، والوقفة اللي بين الضغطتين أقصر. */
const OH_STEPS=[
 {get act(){return darbiT('oh.step1_act');},
  get why(){return darbiT('oh.step1_why');},
  taps:[
   {at:function(){return document.querySelector('#oh-pool [data-p="1"]');},
    run:function(s){s.placed[s.cursor]=1;ohFlash='s'+s.cursor;s.cursor=ohEmpty(s.placed,s.cursor+1);}}
  ]},
 {get act(){return darbiT('oh.step2_act');},
  get why(){return darbiT('oh.step2_why');},
  taps:[
   {at:function(){return document.querySelector('#oh-slots [data-d="2"]');},
    run:function(s){s.cursor=2;ohFlash='d2';}},
   {at:function(){return document.querySelector('#oh-pool [data-p="0"]');},
    run:function(s){s.placed[2]=0;ohFlash='s2';s.cursor=ohEmpty(s.placed,0);}}
  ]},
 {get act(){return darbiT('oh.step3_act');},
  get why(){return darbiT('oh.step3_why');},
  taps:[
   {at:function(){return document.querySelector('#oh-slots [data-s="0"] .order-badge');},
    run:function(s){s.selected=0;ohFlash='s0';}}
  ]},
 {get act(){return darbiT('oh.step4_act');},
  get why(){return darbiT('oh.step4_why');},
  taps:[
   {at:function(){return document.querySelector('#oh-slots [data-s="2"] .order-badge');},
    run:function(s){const t=s.placed[0];s.placed[0]=s.placed[2];s.placed[2]=t;s.selected=-1;ohFlash='s0';}}
  ]},
 {get act(){return darbiT('oh.step5_act');},
  get why(){return darbiT('oh.step5_why');},
  taps:[
   {at:function(){return document.querySelector('#oh-slots [data-s="0"]');},
    run:function(s){ohFlash='p'+s.placed[0];s.placed[0]=null;s.cursor=0;}}
  ]}
];
function ohDraw(){
 const sl=document.getElementById('oh-slots'),po=document.getElementById('oh-pool');
 if(!sl||!po)return;
 sl.innerHTML='';po.innerHTML='';
 const g=document.createElement('div');g.className='order-filled-grid';
 const st=document.createElement('div');st.className='order-empty-strip';
 ohSt.placed.forEach(function(idx,pos){
  if(idx===null){
   const d=document.createElement('span');
   d.className='order-dot'+(pos===ohSt.cursor?' active':'')+(ohFlash==='d'+pos?' oh-flash':'');
   d.setAttribute('data-d',pos);d.textContent=ohNum(pos);st.appendChild(d);
  }else{
   const c=document.createElement('div');
   c.className='order-slot filled'+(pos===ohSt.selected?' oh-swap':'')+(ohFlash==='s'+pos?' oh-flash':'');
   c.setAttribute('data-s',pos);
   const b=document.createElement('span');b.className='order-badge';b.textContent=ohNum(pos);
   const t=document.createElement('span');t.textContent=OH_SEG_AT(idx);
   c.appendChild(b);c.appendChild(t);g.appendChild(c);
  }
 });
 if(g.children.length)sl.appendChild(g);
 if(st.children.length)sl.appendChild(st);
 ohSt.pool.forEach(function(idx){
  if(ohSt.placed.indexOf(idx)>-1)return;
  const b=document.createElement('div');
  b.className='order-item'+(ohFlash==='p'+idx?' oh-flash':'');
  b.setAttribute('data-p',idx);b.textContent=OH_SEG_AT(idx);po.appendChild(b);
 });
 ohFlash=null;
}
function ohBuildDots(){
 const d=document.getElementById('oh-dots');if(!d)return;
 if(d.children.length===OH_STEPS.length)return;
 d.innerHTML='';
 for(let i=0;i<OH_STEPS.length;i++)d.appendChild(document.createElement('i'));
}
function ohPaintDots(){
 const d=document.getElementById('oh-dots');
 if(d){for(let i=0;i<d.children.length;i++)d.children[i].className=(i===ohStep?'on':(i<ohStep?'done':''));}
 const c=document.getElementById('oh-count');
 if(c)c.textContent=ohAr(ohStep+1)+' / '+ohAr(OH_STEPS.length);
}
function ohSay(a,w){
 const c=document.getElementById('oh-cap');if(!c)return;
 c.innerHTML='<div class="act">'+a+'</div><div class="why">'+w+'</div>';
 c.classList.remove('in');void c.offsetWidth;c.classList.add('in');
}
function ohStateAt(n){const s=ohS0();
 for(let i=0;i<n;i++)OH_STEPS[i].taps.forEach(function(t){t.run(s);});
 ohFlash=null;return s;}
function ohShow(n){
 ohStep=((n%OH_STEPS.length)+OH_STEPS.length)%OH_STEPS.length;ohTap=0;
 ohSt=ohStateAt(ohStep);ohDraw();ohBuildDots();ohPaintDots();
 ohSay(OH_STEPS[ohStep].act,OH_STEPS[ohStep].why);
 const t=document.getElementById('oh-tap');if(t)t.className='oh-tap';
}
function ohVisible(){const p=document.getElementById('order-help');return !!p&&p.style.display!=='none'&&p.offsetParent!==null;}
function ohStop(){clearTimeout(ohTimer);ohTimer=null;const t=document.getElementById('oh-tap');if(t)t.className='oh-tap';}
function ohSetPlay(v){
 ohPlaying=v;const b=document.getElementById('oh-play');
 if(b)b.innerHTML=v?darbiT('order.help_stop'):darbiT('order.help_play');
}
function ohRun(){
 if(!ohPlaying||!ohVisible()){ohStop();return;}
 const s=OH_STEPS[ohStep],tap=s.taps[ohTap];
 if(!tap)return;
 const el=tap.at(),bd=document.getElementById('oh-board'),tp=document.getElementById('oh-tap');
 if(!el||!bd||!tp)return;
 const last=(ohTap>=s.taps.length-1);
 /* وقفة القراية في أول ضغطة بس — الضغطة التانية في نفس الخطوة بتيجي أسرع */
 ohTimer=setTimeout(function(){
  if(!ohPlaying||!ohVisible()){ohStop();return;}
  const br=bd.getBoundingClientRect(),er=el.getBoundingClientRect();
  tp.style.left=(er.left-br.left+er.width/2)+'px';
  tp.style.top=(er.top-br.top+er.height/2)+'px';
  tp.classList.add('on');
  ohTimer=setTimeout(function(){
   tp.classList.remove('press');void tp.offsetWidth;tp.classList.add('press');
   ohTimer=setTimeout(function(){
    tap.run(ohSt);ohDraw();tp.classList.remove('on');
    ohTimer=setTimeout(function(){
     if(!last){ohTap++;ohRun();return;}
     if(ohStep>=OH_STEPS.length-1){
      ohSay(darbiT('order.final_step_caption'),darbiT('order.final_step_why'));
      ohSetPlay(false);ohStop();return;
     }
     ohStep++;ohTap=0;ohPaintDots();
     ohSay(OH_STEPS[ohStep].act,OH_STEPS[ohStep].why);ohRun();
    },last?OH_MS.hold:OH_MS.link);
   },OH_MS.press);
  },OH_MS.move);
 },ohTap===0?OH_MS.read:OH_MS.link);
}
function ohToggle(){
 if(ohPlaying){ohSetPlay(false);ohStop();return;}
 if(ohStep>=OH_STEPS.length-1)ohShow(0);
 ohSetPlay(true);ohRun();
}
function ohNext(){ohStop();ohSetPlay(false);ohShow(ohStep+1);}
function ohPrev(){ohStop();ohSetPlay(false);ohShow(ohStep-1);}
function ohStart(){
 ohShow(0);
 const rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 if(rm){ohSetPlay(false);}else{ohSetPlay(true);ohTimer=setTimeout(ohRun,600);}
}
function _orderHelpSeen(){try{return localStorage.getItem(ORDER_HELP_KEY)==='1';}catch(e){return false;}}
function _orderHelpMark(){try{localStorage.setItem(ORDER_HELP_KEY,'1');}catch(e){}}
function _orderHelpSet(open){
 const p=document.getElementById('order-help');if(p)p.style.display=open?'block':'none';
 const b=document.getElementById('order-help-btn');if(b)b.setAttribute('aria-expanded',open?'true':'false');
 if(open){ohStart();}else{ohSetPlay(false);ohStop();}
}
function toggleOrderHelp(){const p=document.getElementById('order-help');if(!p)return;_orderHelpSet(p.style.display==='none');_orderHelpMark();}
function closeOrderHelp(){_orderHelpSet(false);_orderHelpMark();}
function maybeShowOrderHelp(){_orderHelpSet(false);}
/* ===== نهاية لوحة شرح الترتيب ===== */
/*OHJS-END*/
function startOrderQuiz(){orderPlaced=new Array(AYAT.length).fill(null);orderCursor=0;orderSelected=-1;orderPoolOrder=AYAT.map((t,idx)=>idx);shuffle(orderPoolOrder);document.getElementById('level-card').style.display='none';document.getElementById('order-area').style.display='block';document.getElementById('order-feedback').style.display='none';document.getElementById('order-reveal').style.display='none';document.getElementById('order-check-btn').style.display='none';const rb=document.getElementById('order-reveal-btn');rb.disabled=false;rb.style.opacity='1';maybeShowOrderHelp();renderOrderQuiz();}
function ayahNumAt(i){return (typeof AYAT_NUMS!=='undefined'&&AYAT_NUMS&&AYAT_NUMS.length===AYAT.length&&AYAT_NUMS[i]!=null)?AYAT_NUMS[i]:(i+1);}
function _orderNum(pos){return (typeof AYAT_NUMS!=='undefined'&&AYAT_NUMS&&AYAT_NUMS.length===AYAT.length&&AYAT_NUMS.every(function(x){return x>0;}))?AYAT_NUMS[pos]:(pos+1);}
/* صفحات المقاطع (مثل آية الدَّين) أرقامها 0 لغير الأخير: تُعرض أرقام ترتيب عادية لا أقواس آيات */
function _orderLbl(pos){return (typeof AYAT_NUMS!=='undefined'&&AYAT_NUMS&&AYAT_NUMS.length===AYAT.length&&AYAT_NUMS.every(function(x){return x>0;}))?'﴿'+toArabicNum(_orderNum(pos))+'﴾':String(pos+1);}
function mushafHtml(){return '<div class="mushaf-block notranslate" translate="no">'+AYAT.map((t,i)=>t+(ayahNumAt(i)>0?' <span class="ayah-end">﴿'+toArabicNum(ayahNumAt(i))+'﴾</span>':'')).join(' ')+'</div>';}
function nextEmptyFrom(start){for(let i=start;i<orderPlaced.length;i++){if(orderPlaced[i]===null)return i;}for(let i=0;i<orderPlaced.length;i++){if(orderPlaced[i]===null)return i;}return -1;}
function renderOrderQuiz(){const slotsDiv=document.getElementById('order-slots');const poolDiv=document.getElementById('order-pool');slotsDiv.innerHTML='';poolDiv.innerHTML='';const filledGrid=document.createElement('div');filledGrid.className='order-filled-grid';const emptyStrip=document.createElement('div');emptyStrip.className='order-empty-strip';orderPlaced.forEach((idx,pos)=>{if(idx===null){const active=(pos===orderCursor);const dot=document.createElement('span');dot.className='order-dot'+(active?' active':'');dot.textContent=_orderLbl(pos);dot.title=active?darbiT('order.dot_active_title'):darbiT('order.dot_jump_title');dot.onclick=()=>{orderCursor=pos;renderOrderQuiz();};emptyStrip.appendChild(dot);}else{const card=document.createElement('div');card.className='order-slot filled'+(pos===orderSelected?' order-slot-selected':'');card.setAttribute('translate','no');card.innerHTML='<span class="order-badge">﴿'+toArabicNum(_orderNum(pos))+'﴾</span><span class="notranslate">'+AYAT[idx]+'</span>';card.onclick=(e)=>{if(e.target.closest('.order-badge')){if(orderSelected===pos){orderSelected=-1;renderOrderQuiz();return;}if(orderSelected===-1){orderSelected=pos;renderOrderQuiz();return;}const tmp=orderPlaced[orderSelected];orderPlaced[orderSelected]=orderPlaced[pos];orderPlaced[pos]=tmp;orderSelected=-1;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();return;}orderPlaced[pos]=null;orderCursor=pos;orderSelected=-1;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};filledGrid.appendChild(card);}});if(filledGrid.children.length)slotsDiv.appendChild(filledGrid);if(emptyStrip.children.length)slotsDiv.appendChild(emptyStrip);orderPoolOrder.forEach(idx=>{if(orderPlaced.includes(idx))return;const btn=document.createElement('button');btn.className='order-item notranslate';btn.setAttribute('translate','no');btn.textContent=AYAT[idx];btn.onclick=()=>{if(orderCursor===-1||orderPlaced[orderCursor]!==null){orderCursor=nextEmptyFrom(0);}if(orderCursor===-1)return;orderPlaced[orderCursor]=idx;orderCursor=nextEmptyFrom(orderCursor+1);document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};poolDiv.appendChild(btn);});const allFilled=!orderPlaced.includes(null);document.getElementById('order-check-btn').style.display=allFilled?'block':'none';}
function checkOrderAnswer(){let correct=0;document.querySelectorAll('#order-slots .order-slot').forEach((el,pos)=>{const ok=(orderPlaced[pos]!==null&&AYAT[orderPlaced[pos]]===AYAT[pos]);if(ok)correct++;el.classList.remove('correct-slot','wrong-slot');el.classList.add(ok?'correct-slot':'wrong-slot');});const fb=document.getElementById('order-feedback');const allCorrect=(correct===AYAT.length);fb.className='feedback '+(allCorrect?'correct':'wrong');fb.innerHTML='<div style="margin-bottom:8px;">'+darbiT('order.result_line',{correct:toArabicNum(correct),total:toArabicNum(AYAT.length)})+(allCorrect?' 🌟':'')+'</div>'+(allCorrect?'':'<div style="font-size:14px;margin-bottom:4px;">'+darbiT('order.result_review_label')+'</div>'+mushafHtml());fb.style.display='block';document.getElementById('order-check-btn').style.display='none';saveDarbiProgress('order',correct,AYAT.length);if(allCorrect)spawnConfetti();}
function revealOrderAnswer(){document.getElementById('order-reveal').innerHTML=mushafHtml();document.getElementById('order-reveal').style.display='block';const rb=document.getElementById('order-reveal-btn');rb.disabled=true;rb.style.opacity='0.5';}
function shareApp(){var url=location.href;var t=document.title||darbiT('home.title');if(navigator.share){navigator.share({title:t,url:url}).catch(function(){});}else if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){var b=document.getElementById('tools-fab-btn');if(b){var old=b.textContent;b.textContent='✅';setTimeout(function(){b.textContent=old;},1800);}}).catch(function(){});}}
function applyTheme(mode){document.documentElement.setAttribute('data-theme',mode);document.getElementById('theme-toggle').textContent=mode==='dark'?'☀️':'🌙';}
function toggleTheme(){const cur=document.documentElement.getAttribute('data-theme');const next=cur==='dark'?'light':'dark';applyTheme(next);try{localStorage.setItem('quranTheme',next);}catch(e){}}
(function initTheme(){let saved=null;try{saved=localStorage.getItem('quranTheme');}catch(e){}if(!saved)saved=(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';applyTheme(saved);})();
let reviewQuestions=[],reviewIdx=0;
function startReview(){reviewQuestions=wrongIndices.map(i=>questions[i]);reviewIdx=0;if(!reviewQuestions.length)return;document.getElementById('result-area').style.display='none';document.getElementById('review-area').style.display='block';renderReviewQ();}
function renderReviewQ(){const q=reviewQuestions[reviewIdx];document.getElementById('review-number').textContent=darbiT('review.number_label',{cur:toArabicNum(reviewIdx+1),total:toArabicNum(reviewQuestions.length)});var __rqt=document.getElementById('review-q-text');__rqt.textContent=q.q;if(currentLevel==='hard'){__rqt.classList.remove('notranslate');__rqt.removeAttribute('translate');}else{__rqt.classList.add('notranslate');__rqt.setAttribute('translate','no');}document.getElementById('review-answer').textContent='✓ '+((currentLevel==='easy')?q.choices[q.answer]:q.answer);}
function reviewNav(dir){reviewIdx=Math.max(0,Math.min(reviewQuestions.length-1,reviewIdx+dir));renderReviewQ();}
function endReview(){document.getElementById('review-area').style.display='none';document.getElementById('result-area').style.display='block';}
function spawnConfetti(count){const colors=['#4a7c4a','#c4a84a','#9db89d','#e0edd8','#7a9a7a'];const container=document.getElementById('confetti-container');if(!container)return;container.innerHTML='';container.style.display='block';for(let i=0;i<(count||45);i++){const piece=document.createElement('div');piece.className='confetti-piece';piece.style.left=Math.random()*100+'vw';piece.style.background=colors[Math.floor(Math.random()*colors.length)];piece.style.animationDuration=(2+Math.random()*1.5)+'s';piece.style.animationDelay=(Math.random()*0.4)+'s';container.appendChild(piece);}setTimeout(()=>{container.style.display='none';container.innerHTML='';},4000);}
(function enableSwipe(){const area=document.getElementById('quiz-area');if(!area)return;let startX=0,startY=0;area.addEventListener('touchstart',e=>{startX=e.touches[0].clientX;startY=e.touches[0].clientY;},{passive:true});area.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-startX;const dy=e.changedTouches[0].clientY-startY;if(Math.abs(dx)<60||Math.abs(dx)<Math.abs(dy))return;const nextBtn=document.getElementById('next-btn');if(dx<0&&nextBtn&&nextBtn.style.display!=='none'){nextQuestion();}else if(dx>0){prevQuestion();}},{passive:true});})();
(function checkResumeOnLoad(){let saved=null;try{saved=JSON.parse(localStorage.getItem(RESUME_KEY));}catch(e){}if(saved&&saved.qIndex>0){document.getElementById('resume-banner').style.display='block';}})();
