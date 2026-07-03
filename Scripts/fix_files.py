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
        r"replace(/ي\u0653?ـ\u064E\u0654/g,'ي').replace(/ـ\u064E\u0654/g,'ا').replace(/ـ[\u064B-\u065F]*[\u0654\u0655]/g,'').replace(/ـ/g,'').replace(/[\u064B-\u065F\u0610-\u061A\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]/g,'')"
    )

    # تصحيح لاحق (يوليو ٢٠٢٦): الملفات اللي اتصلحت قبل كده بالقاعدة القديمة
    # لوحدها (من غير استثناء الياء) بتحسب "خطيئته" غلط — نضيف الاستثناء قبلها
    OLD_KASHIDA_HAMZA = r"replace(/ـ\u064E\u0654/g,'ا')"
    NEW_KASHIDA_HAMZA = r"replace(/ي\u0653?ـ\u064E\u0654/g,'ي').replace(/ـ\u064E\u0654/g,'ا')"
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
    if r"[\u0654\u0655]/g,'')" not in out and r"[\u0654\u0655]/g,'ا')" not in out:
        out = out.replace(
            r".replace(/ـ/g,'')",
            r".replace(/ـ\u064E\u0654/g,'ا').replace(/ـ[\u064B-\u065F]*[\u0654\u0655]/g,'').replace(/ـ/g,'')"
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
        "    .replace(/ي\\u0653?ـ\\u064E\\u0654/g,'ي')\n"
        "    .replace(/ـ\\u064E\\u0654/g,'ا')\n"
        "    .replace(/ـ[\\u064B-\\u065F]*[\\u0654\\u0655]/g,'')\n"
        "    .replace(/ـ/g,'')\n"
        "    .replace(/[\\u064B-\\u065F\\u0610-\\u061A\\u06D6-\\u06DC\\u06DF-\\u06E4\\u06E7\\u06E8\\u06EA-\\u06ED]/g,'')\n"
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
    OLD_MINIMAL_NORMALIZE_MARKER = "replace(/[\\u064B-\\u065F\\u0670]/g, '')"
    if OLD_MINIMAL_NORMALIZE_MARKER in out and 'function normalize(str)' in out:
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
        m2 = re.search(r"const nm\s*=\s*s\s*=>\s*s\.replace\(/\[\\u064B-\\u065F\\u0670\]/g,''\)[^;]*;", out)
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
        m4 = re.search(r"const nm\s*=\s*s\s*=>\s*s\.replace\(/\[\\u064B-\\u065F\\u0670\]/g,''\)[^;]*;", out)
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
