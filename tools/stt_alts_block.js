// ===== STT_ALTS_BEGIN =====
// بدائل التعرف الصوتي (Google STT) — مصدر واحد يُنسخ حرفيًا في recitation.html و voice-engine.js
// بواسطة tools/sync_stt_alts.py (لا تعدّله يدويًا في أحد الملفين، عدّل tools/stt_alts_block.js ثم شغّل السكربت).
// المبدأ: لا تغيير في normalize/wordDiff. أي بديل هنا مشروط بأن تكون الكلمة المرجعية موجودة في نص
// الصفحة/السؤال نفسه وفي نفس موضعها (محاذاة بالترتيب)، فلا تُقبل كلمة غلط مكان كلمة صح.
// كل المفاتيح والبدائل تُمرَّر على دالة التطبيع الخاصة بالملف (norm / normalize) عند البناء.
const STT_WORD_ALTS=[
  // تشابه حروف عند التعرف (ث/س، ص/س، ت/ط، ق/ء ...) أو حرف زائد/ناقص يضيفه التعرف
  {ref:'سوط',heard:['صوت','سوت','صوط']},
  {ref:'دافق',heard:['دافي','دافئ']},
  {ref:'فراتا',heard:['انفراطا','فراطا','انفراتا','فراط','فرات']},
  {ref:'جمالت',heard:['جمالات']},
  {ref:'سيت',heard:['سيه','سيئه']},
  {ref:'ونسرا',heard:['ونسرو','ونسروا','ونسر','نسرو','نسروا']},
  {ref:'رب',heard:['الرب','ربي']},
  {ref:'مؤمنا',heard:['مؤمنه','يامؤمنه']},
  {ref:'تبارا',heard:['تبارك','تبار']},
  {ref:'كثيبا',heard:['كسيبا','كثيرا','كثيب','كسيب']},
  {ref:'وبسر',heard:['وبصر']},
  {ref:'جنات',heard:['جنه','جنتي','جنت']},
  {ref:'ولم',heard:['وبم']},
  {ref:'نك',heard:['نكن','نكون']},
  {ref:'ينبؤا',heard:['ينبا','ينبوا','ينبى']},
  {ref:'فيمت',heard:['فيموت']},
  {ref:'كن',heard:['كنا']},
  {ref:'منا',next:'ولا',heard:['منهم']},
  {ref:'يوف',heard:['وف','وفق','يوفق','يوفي','يوفا','يوفى','يوفوا','يوافق','يوافقه']},
  {ref:'يأب',heard:['يابى','يابي','يابا']},
  {ref:'لبثت',heard:['لبست']},
  {ref:'انى',heard:['ان','اين','انه','اني']},
  {ref:'يتسنه',heard:['يتسنى','يتسني','يتسنا','يتسن','يتسنن','تسنه','يسنه','متسنه']},
  {ref:'ننشزها',heard:['ننشرها','ننشدها','ننشذها','ننشيها','نشرها']},
  {ref:'فاقرءوا',heard:['فقراوا','فاقراوا']}
];
// كلمتان (أو أكثر) في المصحف يسمعها التعرف بعدد كلمات مختلف
const STT_PHRASE_ALTS=[
  {ref:['أنكالا'],heard:[['ان','كانوا'],['ان','كالا'],['انكانوا']]},
  {ref:['وألو','استقاموا'],heard:[['الا','واستقاموا'],['الا','و','استقاموا'],['الا','واستقامو']]},
  {ref:['ونسرا'],heard:[['و','نسرو'],['و','نسروا'],['و','نسر'],['و','نسرا']]},
  {ref:['ألن'],heard:[['الا','ان']]}
];
const _STT_TBL=new Map();
function _sttTable(N){
  let T=_STT_TBL.get(N);
  if(T)return T;
  T={words:new Map(),phrases:[]};
  for(const e of STT_WORD_ALTS){
    const k=N(e.ref);
    const rec={heard:e.heard.map(N).filter(Boolean),next:e.next?N(e.next):null,prev:e.prev?N(e.prev):null};
    if(!T.words.has(k))T.words.set(k,[]);
    T.words.get(k).push(rec);
  }
  for(const e of STT_PHRASE_ALTS){
    T.phrases.push({ref:e.ref.map(N),heard:e.heard.map(h=>h.map(N))});
  }
  _STT_TBL.set(N,T);
  return T;
}
// الصيغ البديلة (مطبَّعة) المسموح بها لكل كلمة مرجعية — تُستعمل في المرحلة الثانية فقط (فجوات المحاذاة)
function sttAltSets(refWords,N){
  const T=_sttTable(N),R=refWords.map(N);
  return refWords.map((w,i)=>{
    const S=new Set(),r=R[i],nx=R[i+1]||'',pv=R[i-1]||'';
    if(!r)return S;
    for(const e of (T.words.get(r)||[])){
      if(e.next&&e.next!==nx)continue;
      if(e.prev&&e.prev!==pv)continue;
      e.heard.forEach(h=>S.add(h));
    }
    // التاء المفتوحة رسمًا في الأسماء المضافة (رَحۡمَتَ، نِعۡمَتَ، جِمَٰلَتࣱ): التعرف يكتبها تاءً مربوطة.
    // مشروطة بحركة أو تنوين على التاء (الأفعال مثل قَالَتۡ بسكون فلا تدخل)
    if(r.length>=3&&r.charAt(r.length-1)==='ت'&&/\u062A[\u064B-\u0650\u08F0-\u08F2]$/.test(w))S.add(r.slice(0,-1)+'ه');
    // ألف التثنية في الفعل (أَرَادَا، بَلَغَا): تسقط من التعرف. بلا ها/نا/يا الضمائر والأسماء
    if(r.length>=4&&/[^هني]َا$/.test(w))S.add(r.slice(0,-1));
    // الإقلاب (تنوين/نون قبل الباء): التعرف يكتب الميم (فَإِمۡسَاكࣱۢ ← فامساكم)
    if(/[ۭۢ]/.test(w))S.add(r.charAt(r.length-1)==='ن'?r.slice(0,-1)+'م':r+'م');
    // ص عليها سين صغيرة (يَبۡصُۜطُ، ٱلۡمُصَۣيۡطِرُونَ) تُنطق سينًا
    if(/ص[ً-ْٰ]*[ۣۜ]/.test(w))
      S.add(N(w.replace(/ص([ً-ْٰ]*)[ۣۜ]/g,'س$1')));
    // مدّ الألف قبل همزة الوصل يسقط نطقًا (مِنَّا ٱلصَّٰلِحُونَ ← من الصالحون)
    if(r.length>=3&&r.charAt(r.length-1)==='ا'&&/َا$/.test(w)&&(refWords[i+1]||'').charAt(0)==='ٱ')S.add(r.slice(0,-1));
    S.delete(r);
    return S;
  });
}
// استبدال تتابعات التعرف (عدد كلمات مختلف عن المصحف) بكلمات المرجع نفسها
function sttPhrasePass(words,refWords,N){
  if(!words||!words.length||!refWords||!refWords.length)return words;
  const T=_sttTable(N),R=refWords.map(N);
  let U=words.map(N);
  let out=words.slice();
  const find=(seq)=>{
    for(let i=0;i+seq.length<=R.length;i++){
      let ok=true;for(let k=0;k<seq.length;k++)if(R[i+k]!==seq[k]){ok=false;break;}
      if(ok)return i;
    }
    return -1;
  };
  const replaceSeq=(heardSeq,refIdx,refLen)=>{
    if(heardSeq.length>1&&find(heardSeq)>=0)return;      // التتابع نفسه موجود في المصحف (إِلَّا أَن) — مانلمسوش
    for(let j=0;j+heardSeq.length<=out.length;j++){
      let ok=true;for(let k=0;k<heardSeq.length;k++)if(U[j+k]!==heardSeq[k]){ok=false;break;}
      if(!ok)continue;
      const rep=refWords.slice(refIdx,refIdx+refLen);
      out.splice(j,heardSeq.length,...rep);U.splice(j,heardSeq.length,...rep.map(N));
      j+=rep.length-1;
    }
  };
  // (أ) جدول العبارات
  for(const p of T.phrases){
    const at=find(p.ref);
    if(at<0)continue;
    for(const h of p.heard)replaceSeq(h,at,p.ref.length);
  }
  // (ب) همزة الوصل بعد ميم الجمع أو غيرها (لَّهُمُ ٱبۡعَثۡ): تسقط الهمزة فيلتصق الحرفان —
  //     «لهمبعث» أو «له مبعث». نبحث عن أزواج المرجع ونقبل الصيغتين الملتصقة والمقسومة
  for(let k=0;k+1<refWords.length;k++){
    if(refWords[k+1].charAt(0)!=='ٱ')continue;
    const r1=R[k],r2=R[k+1];
    if(!r1||r2.length<3||r2.charAt(0)!=='ا')continue;
    const g=r1+r2.slice(1);
    const cuts=[r1.length-1,r1.length];
    replaceSeq([g],k,2);
    for(const c of cuts){
      if(c<1||c>=g.length)continue;
      const a=g.slice(0,c),b=g.slice(c);
      if(a===r1&&b===r2)continue;
      replaceSeq([a,b],k,2);
    }
  }
  // (ج) إدغام النون في الميم (مِن مَّآءࣲ): التعرف يسقط «من» فيسمع «ماء» فقط
  for(let k=0;k+1<refWords.length;k++){
    if((R[k]!=='من'&&R[k]!=='عن')||R[k+1].charAt(0)!=='م')continue;
    const prevRef=k>0?R[k-1]:null;
    for(let j=0;j<out.length;j++){
      if(U[j]!==R[k+1])continue;
      if(j>0&&U[j-1]===R[k])continue;                    // «من» موجودة فعلًا
      if(j===0?prevRef!==null:(prevRef===null||U[j-1]!==prevRef))continue;
      const rep=[refWords[k],refWords[k+1]];
      out.splice(j,1,...rep);U.splice(j,1,...rep.map(N));j+=1;
    }
  }
  return out;
}
// المرحلة الثانية من المحاذاة: داخل الفجوات بين الكلمات المتطابقة فقط، وبشرط القرب من القطر
// matchI[i] = فهرس الكلمة المسموعة المحاذاة للمرجع i أو -1، U = الكلمات المسموعة مطبَّعة
function sttRelaxedMatch(refWords,U,matchI,N){
  const n=refWords.length,m=U.length;
  const pairs=[];
  for(let i=0;i<n;i++)if(matchI[i]>=0)pairs.push([i,matchI[i]]);
  if(!pairs.length)return [];
  const AS=sttAltSets(refWords,N);
  const bounds=[[-1,-1]].concat(pairs,[[n,m]]);
  const found=[];
  for(let b=0;b+1<bounds.length;b++){
    const i0=bounds[b][0],j0=bounds[b][1],i1=bounds[b+1][0],j1=bounds[b+1][1];
    const ri=[],uj=[];
    for(let i=i0+1;i<i1;i++)if(AS[i].size)ri.push(i);
    for(let j=j0+1;j<j1;j++)if(U[j])uj.push(j);
    if(!ri.length||!uj.length)continue;
    const near=(i,j)=>{
      const d=(b>0)?(i-i0)-(j-j0):(i1-i)-(j1-j);
      return Math.abs(d)<=4;
    };
    const M=(a,c)=>AS[ri[a]].has(U[uj[c]])&&near(ri[a],uj[c]);
    const A=ri.length,B=uj.length;
    const dp=Array.from({length:A+1},()=>new Int32Array(B+1));
    for(let a=1;a<=A;a++)for(let c=1;c<=B;c++)
      dp[a][c]=M(a-1,c-1)?dp[a-1][c-1]+1:Math.max(dp[a-1][c],dp[a][c-1]);
    let a=A,c=B;
    while(a>0&&c>0){
      if(M(a-1,c-1)){found.push([ri[a-1],uj[c-1]]);a--;c--;}
      else if(dp[a][c-1]>=dp[a-1][c])c--;
      else a--;
    }
  }
  return found;
}
// ===== STT_ALTS_END =====
