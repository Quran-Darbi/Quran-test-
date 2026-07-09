#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re

# ===== كود PWA يُضاف لكل ملف =====
PWA_HEAD = """<link rel="manifest" href="/Quran-test-/manifest.json">
<meta name="theme-color" content="#4a7c4a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="دربي">
<link rel="apple-touch-icon" href="/Quran-test-/icons/icon-192x192.png">"""

PWA_SW = """<script>
if('serviceWorker' in navigator){
  window.addEventListener('load',()=>{
    navigator.serviceWorker.register('/Quran-test-/service-worker.js')
      .then(r=>console.log('SW:',r.scope))
      .catch(e=>console.log('SW err:',e));
  });
}
</script>"""

def ar2en(text):
    """تحويل الأرقام العربية-الهندية إلى غربية"""
    for i, c in enumerate('٠١٢٣٤٥٦٧٨٩'):
        text = text.replace(c, str(i))
    return text

# ====================================================
# ميزة ترتيب الآيات 🔀 (يوليو ٢٠٢٦)
# تُطبَّق فقط على الملفات اللي فيها const AYAT (جزء عم حاليًا).
# صفحات البقرة لسه محتاجة إضافة AYAT كامل قبل ما تستفيد من الميزة دي.
# ====================================================

ORDER_CSS = (
    ".order-item{background:var(--surface2);border:1.5px solid var(--border);border-radius:12px;padding:14px 18px;font-size:18px;font-family:inherit;color:var(--text);cursor:pointer;text-align:right;transition:all .15s;line-height:1.9;width:100%;}"
    ".order-item:hover{background:var(--surface-hover);border-color:var(--accent);}"
    ".order-slot{display:flex;gap:10px;align-items:center;border-radius:10px;padding:12px 14px;margin-bottom:8px;font-size:17px;line-height:1.8;cursor:pointer;}"
    ".order-slot.empty{background:var(--surface2);border:1.5px dashed var(--border);color:var(--text-faint);}"
    ".order-slot.empty.active-slot{border-color:var(--accent);background:var(--hint-bg);color:var(--accent-dark);border-style:solid;}"
    ".order-slot.filled{background:var(--surface3);border:1.5px solid var(--accent);}"
    ".order-slot.correct-slot{background:var(--correct-bg) !important;border-color:var(--accent) !important;color:var(--correct-text) !important;}"
    ".order-slot.wrong-slot{background:var(--wrong-bg) !important;border-color:var(--wrong-border) !important;color:var(--wrong-text) !important;}"
    ".order-badge{background:var(--accent);color:#fff;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;}"
    ".mushaf-block{background:var(--surface3);border:1.5px solid var(--border);border-radius:12px;padding:18px 16px;margin-top:12px;font-size:19px;line-height:2.4;text-align:justify;direction:rtl;color:var(--text);}"
    ".ayah-end{color:var(--gold);font-size:15px;}"
)

ORDER_BTN_HTML = (
    "</button>\n"
    "    <button class=\"level-btn\" onclick=\"selectLevel('order')\" id=\"btn-order\">"
    "<span class=\"level-icon\">🔀</span><span class=\"level-name\">ترتيب</span>"
    "<span class=\"level-desc\">رتّب الآيات</span></button>"
)

ORDER_AREA_HTML = '''<div class="quiz-area" id="order-area">
  <div class="q-number">رتّب الآيات — اضغط على الآية فتُوضَع بالتسلسل. تريد تخطّي خانة؟ اضغط على الخانة التي تريد المتابعة منها</div>
  <div id="order-slots" style="margin-bottom:16px;"></div>
  <div id="order-pool" style="display:flex;flex-direction:column;gap:10px;margin-bottom:14px;"></div>
  <div class="nav-row">
    <button class="nav-btn" id="order-reveal-btn" onclick="revealOrderAnswer()">💡 أظهر الترتيب الصحيح</button>
    <button class="nav-btn primary" id="order-check-btn" onclick="checkOrderAnswer()" style="display:none;">تحقق ✓</button>
  </div>
  <div id="order-reveal" style="display:none;"></div>
  <div class="feedback" id="order-feedback"></div>
  <button class="level-return-btn" onclick="returnToLevels()">🔄 اختر مستوى آخر</button>
</div>
'''

ORDER_JS = '''
/* ===== ترتيب الآيات 🔀 ===== */
let orderPlaced=[],orderCursor=0,orderPoolOrder=[];
function startOrderQuiz(){
  orderPlaced=new Array(AYAT.length).fill(null);
  orderCursor=0;
  orderPoolOrder=AYAT.map((t,idx)=>idx);
  shuffle(orderPoolOrder);
  document.getElementById('level-card').style.display='none';
  document.getElementById('order-area').style.display='block';
  document.getElementById('order-feedback').style.display='none';
  document.getElementById('order-reveal').style.display='none';
  document.getElementById('order-check-btn').style.display='none';
  const rb=document.getElementById('order-reveal-btn');
  rb.disabled=false;rb.style.opacity='1';
  renderOrderQuiz();
}
function mushafHtml(){
  return '<div class="mushaf-block">'+AYAT.map((t,i)=>t+' <span class="ayah-end">﴿'+toArabicNum(i+1)+'﴾</span>').join(' ')+'</div>';
}
function nextEmptyFrom(start){
  for(let i=start;i<orderPlaced.length;i++){if(orderPlaced[i]===null)return i;}
  for(let i=0;i<orderPlaced.length;i++){if(orderPlaced[i]===null)return i;}
  return -1;
}
function renderOrderQuiz(){
  const slotsDiv=document.getElementById('order-slots');
  const poolDiv=document.getElementById('order-pool');
  slotsDiv.innerHTML='';
  poolDiv.innerHTML='';
  orderPlaced.forEach((idx,pos)=>{
    const div=document.createElement('div');
    if(idx===null){
      const active=(pos===orderCursor);
      div.className='order-slot empty'+(active?' active-slot':'');
      div.innerHTML='<span class="order-badge">'+toArabicNum(pos+1)+'</span><span class="order-slot-placeholder">'+(active?'— الخانة النشطة الآن —':'— خانة فاضية، اضغط للمتابعة من هنا —')+'</span>';
      div.onclick=()=>{orderCursor=pos;renderOrderQuiz();};
    }else{
      div.className='order-slot filled';
      div.innerHTML='<span class="order-badge">'+toArabicNum(pos+1)+'</span><span>'+AYAT[idx]+'</span>';
      div.onclick=()=>{orderPlaced[pos]=null;orderCursor=pos;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};
    }
    slotsDiv.appendChild(div);
  });
  orderPoolOrder.forEach(idx=>{
    if(orderPlaced.includes(idx))return;
    const btn=document.createElement('button');
    btn.className='order-item';
    btn.textContent=AYAT[idx];
    btn.onclick=()=>{
      if(orderCursor===-1||orderPlaced[orderCursor]!==null){orderCursor=nextEmptyFrom(0);}
      if(orderCursor===-1)return;
      orderPlaced[orderCursor]=idx;
      orderCursor=nextEmptyFrom(orderCursor+1);
      document.getElementById('order-feedback').style.display='none';
      renderOrderQuiz();
    };
    poolDiv.appendChild(btn);
  });
  const allFilled=!orderPlaced.includes(null);
  document.getElementById('order-check-btn').style.display=allFilled?'block':'none';
}
function checkOrderAnswer(){
  let correct=0;
  document.querySelectorAll('#order-slots .order-slot').forEach((el,pos)=>{
    const ok=(orderPlaced[pos]===pos);
    if(ok)correct++;
    el.classList.remove('correct-slot','wrong-slot');
    el.classList.add(ok?'correct-slot':'wrong-slot');
  });
  const fb=document.getElementById('order-feedback');
  const allCorrect=(correct===AYAT.length);
  fb.className='feedback '+(allCorrect?'correct':'wrong');
  fb.innerHTML='<div style="margin-bottom:8px;">'+toArabicNum(correct)+' / '+toArabicNum(AYAT.length)+' في الترتيب الصحيح'+(allCorrect?' 🌟':'')+'</div>'+(allCorrect?'':'<div style="font-size:14px;margin-bottom:4px;">الترتيب الصحيح للمراجعة:</div>'+mushafHtml());
  fb.style.display='block';
  document.getElementById('order-check-btn').style.display='none';
  if(allCorrect)spawnConfetti();
}
function revealOrderAnswer(){
  document.getElementById('order-reveal').innerHTML=mushafHtml();
  document.getElementById('order-reveal').style.display='block';
  const rb=document.getElementById('order-reveal-btn');
  rb.disabled=true;rb.style.opacity='0.5';
}
/* ===== نهاية ترتيب الآيات ===== */
'''

OLD_SELECT_LEVEL = "function selectLevel(lvl){currentLevel=lvl;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));document.getElementById('btn-'+lvl).classList.add('active');document.getElementById('start-btn').classList.add('ready');document.getElementById('total-q').textContent=toArabicNum((lvl==='easy'?EASY_Q:lvl==='medium'?MEDIUM_Q:HARD_Q).length);}"
NEW_SELECT_LEVEL = "function selectLevel(lvl){currentLevel=lvl;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));document.getElementById('btn-'+lvl).classList.add('active');document.getElementById('start-btn').classList.add('ready');if(lvl==='order'){document.getElementById('total-q').textContent=toArabicNum(AYAT.length);}else{document.getElementById('total-q').textContent=toArabicNum((lvl==='easy'?EASY_Q:lvl==='medium'?MEDIUM_Q:HARD_Q).length);}}"

OLD_START_QUIZ = "function startQuiz(){if(!currentLevel)return;questions=currentLevel==='easy'?[...EASY_Q]:currentLevel==='medium'?[...MEDIUM_Q]:[...HARD_Q];qIndex=correctCount=wrongCount=0;statuses=questions.map(()=>'pending');wrongIndices=[];const rb=document.getElementById('resume-banner');if(rb)rb.style.display='none';document.getElementById('level-card').style.display='none';document.getElementById('quiz-area').style.display='block';showQuestion();}"
NEW_START_QUIZ = "function startQuiz(){if(!currentLevel)return;if(currentLevel==='order'){startOrderQuiz();return;}questions=currentLevel==='easy'?[...EASY_Q]:currentLevel==='medium'?[...MEDIUM_Q]:[...HARD_Q];qIndex=correctCount=wrongCount=0;statuses=questions.map(()=>'pending');wrongIndices=[];const rb=document.getElementById('resume-banner');if(rb)rb.style.display='none';document.getElementById('level-card').style.display='none';document.getElementById('quiz-area').style.display='block';showQuestion();}"

OLD_RETURN_LEVELS = "function returnToLevels(){document.getElementById('quiz-area').style.display='none';document.getElementById('level-card').style.display='block';"
NEW_RETURN_LEVELS = "function returnToLevels(){document.getElementById('quiz-area').style.display='none';document.getElementById('order-area').style.display='none';document.getElementById('level-card').style.display='block';"

BTN_CLOSE_PATTERN = re.compile(r'(</button>)(\s*</div>\s*<button class="start-btn")')

def add_ordering_feature(out):
    """يضيف ميزة ترتيب الآيات 🔀 للملفات اللي فيها AYAT (جزء عم)."""
    if 'order-area' in out:
        return out, False  # مطبّقة بالفعل
    if 'const AYAT=' not in out and 'const AYAT =' not in out:
        return out, False  # مفيش AYAT (صفحات البقرة لسه)

    changed = False

    # 1. CSS
    if '</style>' in out and '.order-slot' not in out:
        out = out.replace('</style>', ORDER_CSS + '\n</style>', 1)
        changed = True

    # 2. زر رابع في منتقي المستوى
    new_out, n = BTN_CLOSE_PATTERN.subn(
        lambda m: ORDER_BTN_HTML + m.group(2), out, count=1
    )
    if n:
        out = new_out
        changed = True

    # توسيع الشبكة عشان تستوعب 4 أزرار على الموبايل
    out = out.replace(
        '.levels-grid{display:flex;gap:10px;justify-content:center;margin-bottom:20px;}',
        '.levels-grid{display:flex;gap:8px;justify-content:center;margin-bottom:20px;flex-wrap:wrap;}'
    )
    out = re.sub(
        r'\.level-btn\{flex:1;max-width:100px;background:var\(--surface2\);border:1\.5px solid var\(--border\);border-radius:14px;padding:16px 8px;',
        '.level-btn{flex:1;min-width:76px;max-width:100px;background:var(--surface2);border:1.5px solid var(--border);border-radius:14px;padding:14px 6px;',
        out
    )

    # 3. قسم order-area كامل — قبل result-area
    if '<div class="result-area" id="result-area">' in out and 'id="order-area"' not in out:
        out = out.replace(
            '<div class="result-area" id="result-area">',
            ORDER_AREA_HTML + '<div class="result-area" id="result-area">',
            1
        )
        changed = True

    # 4. selectLevel
    if OLD_SELECT_LEVEL in out:
        out = out.replace(OLD_SELECT_LEVEL, NEW_SELECT_LEVEL, 1)
        changed = True

    # 5. startQuiz
    if OLD_START_QUIZ in out:
        out = out.replace(OLD_START_QUIZ, NEW_START_QUIZ, 1)
        changed = True

    # 6. returnToLevels
    if OLD_RETURN_LEVELS in out and "order-area').style.display='none'" not in out:
        out = out.replace(OLD_RETURN_LEVELS, NEW_RETURN_LEVELS, 1)
        changed = True

    # 7. دوال JS للترتيب — قبل shareApp
    if 'function shareApp(' in out and 'startOrderQuiz' not in out:
        out = out.replace('function shareApp(', ORDER_JS + '\nfunction shareApp(', 1)
        changed = True

    return out, changed


def fix_file(path):
    with open(path, encoding='utf-8') as f:
        src = f.read()
    out = ar2en(src)

    # ====================================================
    # 0. إصلاح قائمة التشكيل (alburuj/altariq pattern):
    #    - الهمزة على كشيدة بفتحة (ـَٔ) = ألف، غيرها = تتحذف
    #    - ثم المدى الشامل يشمل ۡ وغيره
    #    التشكيل يتحذف أولاً (قبل قواعد ىٰ) عشان ىٰٓ ما تتعرفش غلط
    out = out.replace(
        "replace(/[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞۢ]/g,'')",
        r"replace(/يٓ?ـَٔ/g,'ي').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـ/g,'').replace(/[ًٌٍَؘُؙِؚّْٕٖٜٟۣ۪ۭٓٔٗ٘ٙٚٛٝٞؐؑؒؓؔؕؖؗۖۗۘۙۚۛۜ۟۠ۡۢۤۧۨ۫۬]/g,'')"
    )

    # تصحيح لاحق (يوليو ٢٠٢٦): الملفات اللي اتصلحت قبل كده بالقاعدة القديمة
    # لوحدها (من غير استثناء الياء) بتحسب "خطيئته" غلط — نضيف الاستثناء قبلها
    OLD_KASHIDA_HAMZA = r"replace(/ـَٔ/g,'ا')"
    NEW_KASHIDA_HAMZA = r"replace(/يٓ?ـَٔ/g,'ي').replace(/ـَٔ/g,'ا')"
    if OLD_KASHIDA_HAMZA in out and NEW_KASHIDA_HAMZA not in out:
        out = out.replace(OLD_KASHIDA_HAMZA, NEW_KASHIDA_HAMZA, 1)

    # 1. قواعد الألف الخنجرية والإصلاحات (alburuj/altariq pattern):

    # يٰ = يا (كان ي خطأ)
    if r"يٰ/g,'يا'" not in out:
        out = out.replace(r".replace(/يٰ/g,'ي')", r".replace(/يٰ/g,'يا')")

    # ىٰ: وسط الكلمة = ا، آخرها = ي
    if "[ىی]ٰ(?=" not in out:
        out = re.sub(r"\[ىی\]ٰ/g,'[اي]'\)",
                      r"[ىی]ٰ(?=\\S)/g,'ا').replace(/[ىی]ٰ/g,'ي')",
                      out)

    # وٰ: قبل ة = الواو تتحذف (الصلاة)، غيرها = واو + ا (السماوات، أبواب)
    if r"وٰ(?=ة)" not in out:
        out = out.replace(r".replace(/وٰ/g,'ا')", r".replace(/وٰ(?=ة)/g,'ا').replace(/وٰ/g,'وا')")
        out = out.replace(r".replace(/وٰ/g,'و')", r".replace(/وٰ(?=ة)/g,'ا').replace(/وٰ/g,'وا')")

    # ألف وصل بعد واو (وَٱسۡجُدۡ → وسجد) ما عدا ال التعريف
    # + قبول واسجد/واقترب من المستخدم
    if r"وٱ(?!ل)" not in out:
        out = re.sub(
            r"(\.replace\(/وٰ\(\?=ة\)/g,'ا'\)\.replace\(/وٰ/g,'وا'\))",
            r"\1.replace(/وٱ(?!ل)/g,'و').replace(/^وا(?!ل)/g,'و')",
            out
        )

    # هاؤلاء/هؤلاء قبل حذف ؤ
    if r"ها[ؤو]لاء" not in out:
        out = out.replace(
            r".replace(/[ءئؤ]/g,'')",
            r".replace(/ها[ؤو]لاء|ها[ؤو]لا(?!\S)/g,'هالا').replace(/ه[ؤو]لاء|ه[ؤو]لا(?!\S)/g,'هالا').replace(/[ءئؤ]/g,'')"
        )
        # إزالة الـ rule القديمة الميتة
        out = out.replace(r".replace(/هاؤلاء/g,'هولا').replace(/هؤلاء/g,'هولا')", "")

    # الهمزة على كشيدة (ـَٔ → ا، غيرها تتحذف)
    if r"[ٕٔ]/g,'')" not in out and r"[ٕٔ]/g,'ا')" not in out:
        out = out.replace(
            r".replace(/ـ/g,'')",
            r".replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـ/g,'')"
        )

    # ۦ في وسط الكلمة = ي، في آخرها = صامت اختياري
    if r"ۦ(?=\S)" not in out:
        out = out.replace(
            r".replace(/ه[ۥۦ]/g,'ه').replace(/[ۥۦ]/g,'')",
            r".replace(/ه[ۥۦ]/g,'ه').replace(/ۦ(?=\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'')"
        )
        out = out.replace(
            r".replace(/ه[ۥۦ]/g,'ه').replace(/ۦ/g,'ي').replace(/ۥ/g,'')",
            r".replace(/ه[ۥۦ]/g,'ه').replace(/ۦ(?=\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'')"
        )

    # كلمات خاصة + واو الجماعة + الإقلاب
    if "replace(/يا ايها/g,'يايها')" not in out:
        out = out.replace(
            r".replace(/مولانا/g,'مولنا')",
            r".replace(/مولانا/g,'مولنا').replace(/يا ايها/g,'يايها').replace(/يا ايتها/g,'يايتها').replace(/الاه/g,'اله').replace(/ارايت/g,'اريت').replace(/نب/g,'مب').replace(/وا(?=\s|$)/g,'و').replace(/اولك/g,'اولاك')"
        )

    # ====================================================
    # 1ب. نفس الإصلاحات للصيغة الثانية (alnnas.html pattern):
    if ".replace(/ىٰ(?=" not in out:
        out = re.sub(r"\.replace\(/ىٰ/g,'[اي]'\)",
                      r".replace(/ىٰ(?=\\S)/g,'ا').replace(/ىٰ/g,'ي')",
                      out)

    if r"يٰ/g,'يا'" not in out:
        out = out.replace(r".replace(/يٰ/g,'ي')", r".replace(/يٰ/g,'يا')")

    if r"وٰ(?=ة)" not in out:
        out = out.replace(r".replace(/وٰ/g,'ا')", r".replace(/وٰ(?=ة)/g,'ا').replace(/وٰ/g,'وا')")
        out = out.replace(r".replace(/وٰ/g,'و')", r".replace(/وٰ(?=ة)/g,'ا').replace(/وٰ/g,'وا')")

    if r"وٱ(?!ل)" not in out:
        out = out.replace(
            r".replace(/اٰ/g,'ا')",
            r".replace(/وٱ(?!ل)/g,'و').replace(/^وا(?!ل)/g,'و').replace(/اٰ/g,'ا')"
        )

    if r"ها[ؤو]لاء" not in out:
        out = out.replace(
            r".replace(/هاؤلاء/g,'هولا').replace(/هؤلاء/g,'هولا')",
            r".replace(/ها[ؤو]لاء|ها[ؤو]لا(?!\S)/g,'هالا').replace(/ه[ؤو]لاء|ه[ؤو]لا(?!\S)/g,'هالا')"
        )

    if r"ۦ(?=\S)" not in out:
        out = out.replace(
            r".replace(/هۦ/g,'ه').replace(/[ۥۦ]/g,'')",
            r".replace(/هۦ/g,'ه').replace(/ۦ(?=\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'')"
        )
        out = out.replace(
            r".replace(/هۦ/g,'ه').replace(/ۦ/g,'ي').replace(/ۥ/g,'')",
            r".replace(/هۦ/g,'ه').replace(/ۦ(?=\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'')"
        )

    if "replace(/الاه/g,'اله')" not in out:
        out = out.replace(
            r".replace(/ذالك/g,'ذلك')",
            r".replace(/ذالك/g,'ذلك').replace(/لاكن/g,'لكن').replace(/الاه/g,'اله').replace(/ارايت/g,'اريت').replace(/نب/g,'مب').replace(/وا(?=\s|$)/g,'و').replace(/اولك/g,'اولاك')"
        )

    # تصحيح لباگ "ولكن" اللي كانت بتتحول لـ"ولاكن" بسبب الألف الخنجرية فوق اللام
    # (نفس مشكلة هٰذا/ذٰلك بالظبط) — بلوك مستقل عشان يلحق الملفات القديمة كمان
    if "replace(/لاكن/g,'لكن')" not in out:
        out = out.replace(
            r".replace(/ذالك/g,'ذلك')",
            r".replace(/ذالك/g,'ذلك').replace(/لاكن/g,'لكن')"
        )

    # ====================================================
    # 1جـ. تصحيح باگ قاعدة ^وا اللي كانت بتمسح الهمزة القطعية غلط
    #      (مثال: "وأولئك" مكتوبة "واولئك" كانت بتتحول لـ"ولك" بدل "واولاك")
    #      دلوقتي مقصورة على أفعال الوصل الفعلية بس (اسجد، اقترب...) بدل أي كلمة تبدأ بـ"وا"
    OLD_WA_RULE = r".replace(/^وا(?!ل)/g,'و')"
    NEW_WA_RULE = r".replace(/^وا(?=سجد|قترب|دخل|دعو|ذكر|رحم|ستغفر|ستغن|غفر|عف|نحر|تق|ختلاف|مر[أا])/g,'و')"
    # قائمة أوسع (يوليو ٢٠٢٦): إضافة أفعال وصل شائعة كانت ناقصة وبتسبب
    # رفض إجابات صحيحة زي: واتبعوا، واسمعوا، واستكبر، واستعينوا، واركعوا
    NEWER_WA_RULE = r".replace(/^وا(?=سجد|قترب|دخل|دعو|ذكر|رحم|ستغفر|ستغن|غفر|عف|نحر|تق|ختلاف|مر[أا]|تبع|سمع|ستكبر|ستعين|ركع|صبر|صل|جتنب|هبط|ستبشر|ستقم|ضرب|عتصم|ئتلف|بتغ|حذر)/g,'و')"
    if OLD_WA_RULE in out:
        out = out.replace(OLD_WA_RULE, NEWER_WA_RULE)
    elif NEW_WA_RULE in out:
        out = out.replace(NEW_WA_RULE, NEWER_WA_RULE)
    elif r"وٱ(?!ل)/g,'و')" in out and r"^وا(?=" not in out:
        # ملفات فيها وٱ(?!ل) بس من غير قاعدة ^وا خالص (زي annaba.html) —
        # فضلت ماشية على واتبعوا/واسمعوا غلط لأنها مش من غير القاعدة أصلاً
        out = out.replace(
            r".replace(/وٱ(?!ل)/g,'و')",
            r".replace(/وٱ(?!ل)/g,'و')" + NEWER_WA_RULE,
            1
        )

    # ====================================================
    # 2. الأرقام: استبدل toArabicNum بدالة تعرض أرقام إنجليزي
    if 'function toArabicNum(n){return n;}' not in out and 'toArabicNum' in out:
        out = re.sub(
            r"function toArabicNum\(n\)\{return[^}]+\}",
            "function toArabicNum(n){return n;}",
            out
        )

    # ====================================================
    # 3. زر المشاركة في top-bar (كل صفحات السور)
    SHARE_BTN = '<button onclick="shareApp()" title="شارك الموقع" style="background:none;border:none;font-size:20px;cursor:pointer;padding:4px;margin-right:auto;">🔗</button>'
    SHARE_FN = """function shareApp(){var url='https://quran-darbi.github.io/Quran-test-/';if(navigator.share){navigator.share({title:'دربي لحفظ القرآن',url:url}).catch(function(){});}else{navigator.clipboard.writeText(url).then(function(){var b=document.querySelector('[onclick=\"shareApp()\"]');if(b){b.textContent='✅';setTimeout(function(){b.textContent='🔗';},2000);}}).catch(function(){});}}"""
    if 'shareApp' not in out:
        # أضف الزر في top-bar بعد زر الرجوع مباشرة
        out = out.replace(
            '<a href="index.html" class="back-btn">← الرجوع</a>',
            '<a href="index.html" class="back-btn">← الرجوع</a>\n  ' + SHARE_BTN
        )
        # أضف الدالة قبل applyTheme
        out = out.replace('function applyTheme', SHARE_FN + '\nfunction applyTheme', 1)

    # 3ب. رسالة "استئناف الاختبار": من عامية مؤنثة لصيغة فصحى مذكرة أكثر احترافية
    #     (المستخدم مش بالضرورة أنثى)
    OLD_RESUME_MSG = "📌 عندك اختبار لسه ما خلصتيهوش، عايزة تكملي منين وقفتي؟"
    NEW_RESUME_MSG = "📌 لديك اختبار لم يكتمل. هل ترغب في المتابعة من حيث توقفتَ، أم البدء من جديد؟"
    if OLD_RESUME_MSG in out:
        out = out.replace(OLD_RESUME_MSG, NEW_RESUME_MSG)
    OLD_RESUME_BTN1 = '>كمل من هنا</button>'
    NEW_RESUME_BTN1 = '>المتابعة من هنا</button>'
    if OLD_RESUME_BTN1 in out:
        out = out.replace(OLD_RESUME_BTN1, NEW_RESUME_BTN1)
    OLD_RESUME_BTN2 = '>ابدأ من جديد</button>'
    NEW_RESUME_BTN2 = '>البدء من جديد</button>'
    if OLD_RESUME_BTN2 in out:
        out = out.replace(OLD_RESUME_BTN2, NEW_RESUME_BTN2)

    # 4. أضف زر returnToLevels لو مش موجود
    if 'returnToLevels' not in out:
        # CSS
        if 'level-return-btn' not in out:
            css = '.level-return-btn{display:block;width:100%;margin-top:14px;padding:11px;background:var(--surface2);color:var(--text-soft);border:1.5px solid var(--border);border-radius:12px;font-size:15px;font-family:inherit;cursor:pointer;transition:all .2s;text-align:center;}\n.level-return-btn:hover{background:var(--surface-hover);border-color:var(--accent);color:var(--accent);}'
            out = out.replace('</style>', css + '\n</style>', 1)
        # زر HTML
        btn = '\n  <button class="level-return-btn" onclick="returnToLevels()">&#x1F504; &#x627;&#x62E;&#x62A;&#x631; &#x645;&#x633;&#x62A;&#x648;&#x649; &#x622;&#x62E;&#x631;</button>'
        out = out.replace('<div class="feedback" id="feedback"></div>',
                         '<div class="feedback" id="feedback"></div>' + btn, 1)
        # دالة JS
        fn = """function returnToLevels(){document.getElementById('quiz-area').style.display='none';document.getElementById('level-card').style.display='block';currentLevel=null;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));document.getElementById('start-btn').classList.remove('ready');document.getElementById('total-q').textContent='-';document.getElementById('wrong-badge').innerHTML='&#x6F0; &#x2717;<br>&#x62E;&#x637;&#x623;';document.getElementById('correct-badge').innerHTML='&#x6F0; &#x2713;<br>&#x635;&#x62D;&#x64A;&#x62D;';document.getElementById('qnum-badge').innerHTML='&#x627;&#x644;&#x633;&#x624;&#x627;&#x644; &#x6F1; /<br>-';document.getElementById('progress-fill').style.width='0%';}"""
        out = out.replace('function retryQuiz', fn + '\nfunction retryQuiz', 1)

    # 5. أضف PWA head لو مش موجود
    if 'manifest.json' not in out:
        out = out.replace('</head>', PWA_HEAD + '\n</head>', 1)

    # ====================================================
    # 7. تصحيح شامل يوليو ٢٠٢٦: صفحات القالب القديم (البقرة p2–p13)
    #    اللي normalize() فيها بدائي جداً (بس تشكيل+ألف+تاء مربوطة) وناقصها
    #    كل حاجة: الألف الخنجرية، الهمزات، ألف الوصل، الشدة... إلخ
    #    الباگ ده هو سبب رفض إجابات زي "الصلاة"، "غشاوة"، "خطيئته" وغيرها
    NEW_NORMALIZE_BODY = (
        "function normalize(str){\n"
        "  if(!str)return'';\n"
        "  return str\n"
        "    .replace(/يٓ?ـَٔ/g,'ي')\n"
        "    .replace(/ـَٔ/g,'ا')\n"
        "    .replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'')\n"
        "    .replace(/ـ/g,'')\n"
        "    .replace(/[ًٌٍَؘُؙِؚّْٕٖٜٟۣ۪ۭٓٔٗ٘ٙٚٛٝٞؐؑؒؓؔؕؖؗۖۗۘۙۚۛۜ۟۠ۡۢۤۧۨ۫۬]/g,'')\n"
        "    .replace(/ها[ؤو]لاء|ها[ؤو]لا(?!\\S)/g,'هالا').replace(/ه[ؤو]لاء|ه[ؤو]لا(?!\\S)/g,'هالا')\n"
        "    .replace(/وٱ(?!ل)/g,'و')\n"
        "    " + NEWER_WA_RULE + "\n"
        "    .replace(/وٰ(?=ة)/g,'ا').replace(/وٰ/g,'وا')\n"
        "    .replace(/اٰ/g,'ا').replace(/يٰ/g,'يا')\n"
        "    .replace(/نٰ/g,'نا')\n"
        "    .replace(/ىٰ(?=\\S)/g,'ا').replace(/ىٰ/g,'ي')\n"
        "    .replace(/(.)ٰ/g,'$1ا')\n"
        "    .replace(/هۥ/g,'ه').replace(/هۦ/g,'ه')\n"
        "    .replace(/ۦ(?=\\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'')\n"
        "    .replace(/ه[ۥۦ]/g,'ه')\n"
        "    .replace(/[ئؤ]/g,'ء').replace(/ء/g,'')\n"
        "    .replace(/[آأإٱا]/g,'ا')\n"
        "    .replace(/[ىی]/g,'ي')\n"
        "    .replace(/ة/g,'ه')\n"
        "    .replace(/(.)\\1+/g,'$1')\n"
        "    .replace(/رحمان/g,'رحمن')\n"
        "    .replace(/مولانا/g,'مولنا').replace(/يا ?ايها/g,'يايها').replace(/يا ?ايتها/g,'يايتها')\n"
        "    .replace(/الاه/g,'اله').replace(/ارايت/g,'اريت')\n"
        "    .replace(/هاذا/g,'هذا').replace(/هاذه/g,'هذه').replace(/ذالك/g,'ذلك').replace(/لاكن/g,'لكن')\n"
        "    .replace(/\\s+/g,' ')\n"
        "    .trim();\n"
        "}"
    )
    OLD_MINIMAL_NORMALIZE_RE = re.compile(r"replace\(/\[\\u064B-\\u065F\\u0670\]/g,\s*''\)")
    if OLD_MINIMAL_NORMALIZE_RE.search(out) and 'function normalize(str)' in out:
        m = re.search(r"function normalize\(str\)\s*\{", out)
        if m:
            i = out.index('{', m.start())
            depth = 0
            end = None
            for j in range(i, len(out)):
                if out[j] == '{':
                    depth += 1
                elif out[j] == '}':
                    depth -= 1
                    if depth == 0:
                        end = j + 1
                        break
            if end:
                out = out[:m.start()] + NEW_NORMALIZE_BODY + out[end:]
        # نفس التصحيح لنسخة nm() المكررة جوه wordDiff (لو فيها نفس النمط القديم)
        # (متسامح مع فراغات مختلفة: "s =>" أو "s=>"، إلخ)
        m2 = re.search(
            r"const\s+nm\s*=\s*s\s*=>\s*s\.replace\(/\[\\u064B-\\u065F\\u0670\]/g,\s*''\)[^;]*;",
            out
        )
        if m2:
            out = out[:m2.start()] + "const nm = s => normalize(s||'');" + out[m2.end():]

    # ====================================================
    # 7ب. تصحيح كارثي يوليو ٢٠٢٦: صفحات فيها normalize() بيتم نداؤها
    #      (بتاعت checkText) بس مش متعرّفة خالص — بتخلي زر التحقق
    #      يتعطل تماماً على كل سؤال كتابة/فراغ (medium وhard) لأن
    #      الكود بيرمي استثناء صامت أول ما المستخدم يضغط "تحقق"
    if 'normalize(q.answer)' in out and 'function normalize(' not in out:
        m3 = re.search(r"function wordDiff\(", out)
        if m3:
            out = out[:m3.start()] + NEW_NORMALIZE_BODY + "\n\n" + out[m3.start():]
        # صحّح nm() جوه wordDiff لو موجودة بنفس النمط القديم
        m4 = re.search(r"const\s+nm\s*=\s*s\s*=>\s*s\.replace\(/\[\\u064B-\\u065F\\u0670\]/g,\s*''\)[^;]*;", out)
        if m4:
            out = out[:m4.start()] + "const nm = s => normalize(s||'');" + out[m4.end():]

    # ====================================================
    # 7جـ. تصحيح كارثي يوليو ٢٠٢٦: زر التحقق في وضع التسجيل الصوتي
    #      (المستوى الصعب) بينادي checkTextVal() اللي مش متعرّفة —
    #      بيخلي الزر يتعطل تماماً بلا أي نتيجة ظاهرة للمستخدم
    if 'checkTextVal(q' in out and 'function checkTextVal' not in out:
        CHECK_TEXT_VAL_FN = (
            "function checkTextVal(q, userVal) {\n"
            "  if (!userVal) return;\n"
            "  const fb = document.getElementById('feedback');\n"
            "  const correct = normalize(q.answer);\n"
            "  const user    = normalize(userVal);\n"
            "  if (user === correct) {\n"
            "    correctCount++; statuses[qIndex]='correct';\n"
            "    fb.className = 'feedback correct';\n"
            "    fb.innerHTML = '✓ أحسنت! إجابة صحيحة تماماً 🌟';\n"
            "  } else {\n"
            "    wrongCount++; statuses[qIndex]='wrong'; wrongIndices.push(qIndex);\n"
            "    fb.className = 'feedback wrong';\n"
            "    fb.innerHTML = '✗ الإجابة الصحيحة:<br><span style=\"font-size:18px;line-height:2.2;direction:rtl;display:block;text-align:right;\">'+wordDiff(userVal,q.answer)+'</span>';\n"
            "  }\n"
            "  fb.style.display = 'block';\n"
            "  updateBadges();\n"
            "  renderDotProgress(); saveResumeState(); document.getElementById('next-btn').style.display = 'block'; document.getElementById('skip-btn').style.display = 'none';\n"
            "}\n"
        )
        m5 = re.search(r"function checkText\(", out)
        if m5:
            out = out[:m5.start()] + CHECK_TEXT_VAL_FN + out[m5.start():]

    # ====================================================
    # 9. ميزة ترتيب الآيات 🔀 (جزء عم فقط — الملفات اللي فيها AYAT)
    out, order_changed = add_ordering_feature(out)

    # 8. أضف Service Worker لو مش موجود
    if 'service-worker.js' not in out:
        out = out.replace('</body>', PWA_SW + '\n</body>', 1)

    if out != src:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(out)
        return True
    return False

def fix_index_recitation(path):
    """index.html و recitation.html — PWA + زر مشاركة"""
    with open(path, encoding='utf-8') as f:
        src = f.read()
    out = ar2en(src)

    SHARE_FN = """function shareApp(){var url='https://quran-darbi.github.io/Quran-test-/';if(navigator.share){navigator.share({title:'دربي لحفظ القرآن',url:url}).catch(function(){});}else{navigator.clipboard.writeText(url).then(function(){var b=document.querySelector('[onclick=\"shareApp()\"]');if(b){b.textContent='✅';setTimeout(function(){b.textContent='🔗';},2000);}}).catch(function(){});}}"""
    SHARE_BTN = '<button onclick="shareApp()" title="شارك الموقع" style="background:none;border:none;font-size:20px;cursor:pointer;padding:4px;">🔗</button>'

    if 'shareApp' not in out:
        # أضف الزر في top-bar
        out = out.replace(
            '<a href="index.html" class="back-btn">← الرجوع</a>',
            '<a href="index.html" class="back-btn">← الرجوع</a>\n  ' + SHARE_BTN
        )
        # index.html ممكن ما فيهاش back-btn، نضيف الزر قبل theme-toggle
        if 'shareApp' not in out:
            out = out.replace(
                'id="theme-toggle"',
                'id="share-btn" onclick="shareApp()" title="شارك الموقع" style="background:none;border:none;font-size:20px;cursor:pointer;padding:4px;">🔗</button>\n  <button id="theme-toggle"',
                1
            )
        # أضف الدالة قبل </script> الأخير
        if 'shareApp' in out and SHARE_FN not in out:
            out = out.replace('</script>', SHARE_FN + '\n</script>', 1)

    if 'manifest.json' not in out:
        out = out.replace('</head>', PWA_HEAD + '\n</head>', 1)

    if 'service-worker.js' not in out:
        out = out.replace('</body>', PWA_SW + '\n</body>', 1)

    if out != src:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(out)
        return True
    return False

def main():
    skip = {'index.html', 'recitation.html'}
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fixed = 0

    # index.html و recitation.html — PWA فقط
    for special in ['index.html', 'recitation.html']:
        fp = os.path.join(root, special)
        if os.path.isfile(fp):
            if fix_index_recitation(fp):
                print('FIXED (PWA):', special)
                fixed += 1
            else:
                print('OK:', special)

    # باقي ملفات السور — كل التعديلات + PWA
    for fn in sorted(os.listdir(root)):
        if fn.endswith('.html') and fn not in skip:
            fp = os.path.join(root, fn)
            if os.path.isfile(fp):
                if fix_file(fp):
                    print('FIXED:', fn)
                    fixed += 1
                else:
                    print('OK:', fn)

    print(f'Done: {fixed} fixed')

if __name__ == '__main__':
    main()
