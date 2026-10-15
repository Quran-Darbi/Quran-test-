#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch-patch script — apply 4 UI improvements to all quiz HTML files.
Skips: alfatiha.html (already done), index.html, progress.html, recitation.html
"""

import os, re

REPO = '/tmp/claude-0/-home-claude/008ada04-2fb2-5a35-a4ee-461817b50eac/scratchpad/repo/Quran-test--main'
SKIP = {'alfatiha.html', 'index.html', 'progress.html', 'recitation.html'}

# ---------- CSS block to inject ----------
CSS_NEW = (
    '\n/* ===== شارات الإحصاء بألوان ===== */\n'
    '.stat-badge.badge-wrong{background:var(--wrong-bg);color:var(--wrong-text);border:1.5px solid var(--wrong-border);}\n'
    '.stat-badge.badge-correct{background:var(--correct-bg);color:var(--correct-text);}\n'
    '.stat-badge.badge-neutral{background:var(--surface2);color:var(--text);border:1.5px solid var(--border);}\n'
    '/* ===== نجوم النتيجة ===== */\n'
    '.result-stars{font-size:30px;margin-bottom:4px;letter-spacing:6px;color:var(--gold);}\n'
    '/* ===== زر الصفحة التالية البارز في النتيجة ===== */\n'
    '#result-page-nav .next-page-btn{background:var(--accent)!important;color:#fff!important;border:none!important;border-radius:14px!important;padding:14px!important;font-size:16px!important;font-weight:700;transition:background .2s;}\n'
    '#result-page-nav .next-page-btn:hover{background:var(--accent-dark)!important;}'
)

# ---------- New updateBadges ----------
NEW_UPDATE_BADGES = (
    "function updateBadges(){\n"
    "  document.getElementById('qnum-badge').innerHTML=`السؤال ${toArabicNum(qIndex+1)} /<br>${toArabicNum(questions.length)}`;\n"
    "  const wb=document.getElementById('wrong-badge');\n"
    "  wb.innerHTML=`${toArabicNum(wrongCount)} ✗<br>خطأ`;\n"
    "  wb.className='stat-badge '+(wrongCount>0?'badge-wrong':'badge-neutral');\n"
    "  const cb=document.getElementById('correct-badge');\n"
    "  cb.innerHTML=`${toArabicNum(correctCount)} ✓<br>صحيح`;\n"
    "  cb.className='stat-badge '+(correctCount>0?'badge-correct':'badge-neutral');\n"
    "}"
)

# ---------- _resetBadges helper ----------
RESET_BADGES_FN = (
    "function _resetBadges(){"
    "const wb=document.getElementById('wrong-badge');"
    "const cb=document.getElementById('correct-badge');"
    "const qb=document.getElementById('qnum-badge');"
    "if(wb){wb.className='stat-badge badge-neutral';}"
    "if(cb){cb.className='stat-badge badge-neutral';}"
    "if(qb){qb.className='stat-badge badge-neutral';}}"
)

patched = []
skipped_list = []
errors = []

html_files = sorted(f for f in os.listdir(REPO) if f.endswith('.html'))

for fname in html_files:
    if fname in SKIP:
        skipped_list.append(fname)
        continue

    fpath = os.path.join(REPO, fname)
    with open(fpath, 'r', encoding='utf-8') as fh:
        content = fh.read()
    orig = content

    # ==================================================================
    # 1. CSS — inject badge/stars/button styles
    # ==================================================================
    if 'badge-wrong' not in content:
        if '.level-return-btn:hover{' in content:
            content = re.sub(
                r'(\.level-return-btn:hover\{[^\n]*)',
                lambda m: m.group(1) + CSS_NEW,
                content, count=1
            )
        elif '.progress-bar-fill{' in content:
            # alghasiya fallback
            content = re.sub(
                r'(\.progress-bar-fill\{[^\n]*)',
                lambda m: m.group(1) + CSS_NEW,
                content, count=1
            )
        else:
            errors.append(f'{fname}: ⚠ CSS anchor not found')

    # ==================================================================
    # 2. HTML — add badge-neutral class to the three stat badges
    # ==================================================================
    for bid in ('qnum-badge', 'wrong-badge', 'correct-badge'):
        content = content.replace(
            f'class="stat-badge" id="{bid}"',
            f'class="stat-badge badge-neutral" id="{bid}"'
        )

    # ==================================================================
    # 3. HTML — add result-stars div before result-icon
    # ==================================================================
    if 'result-stars' not in content:
        content = content.replace(
            '  <div class="result-icon" id="result-icon">',
            '  <div class="result-stars" id="result-stars"></div>\n  <div class="result-icon" id="result-icon">'
        )

    # ==================================================================
    # 4. JS — replace updateBadges with color-aware version
    # ==================================================================
    if "wb.className='stat-badge '" not in content:
        # old version is a single-line function
        content = re.sub(
            r"function updateBadges\(\)\{[^\}]+\}",
            NEW_UPDATE_BADGES,
            content, count=1
        )

    # ==================================================================
    # 5. JS — add stars rating to showResult
    # ==================================================================
    # 5a. add stars to variable declaration
    content = content.replace('let icon,title,msg;', 'let icon,title,msg,stars;', 1)

    # 5b. add stars= to each score branch (they are single-line)
    if 'stars=' not in content:
        content = re.sub(r"(if\(pct===100\)\{(?:[^}])*?msg='[^']*';)", r"\1stars='★★★';", content, count=1)
        content = re.sub(r"(else if\(pct>=80\)\{(?:[^}])*?msg='[^']*';)", r"\1stars='★★☆';", content, count=1)
        content = re.sub(r"(else if\(pct>=60\)\{(?:[^}])*?msg='[^']*';)", r"\1stars='★☆☆';", content, count=1)
        content = re.sub(r"(else\{icon='[^']*';title='[^']*';msg='[^']*';)", r"\1stars='☆☆☆';", content, count=1)

    # 5c. populate result-stars element after setting result-msg
    if 'result-stars' in content and 'stEl' not in content:
        content = content.replace(
            "document.getElementById('result-msg').textContent=msg;",
            "document.getElementById('result-msg').textContent=msg;\n  const stEl=document.getElementById('result-stars');if(stEl)stEl.textContent=stars;"
        )

    # ==================================================================
    # 6. JS — add _resetBadges helper + call in retryQuiz & returnToLevels
    # ==================================================================
    if '_resetBadges' not in content:
        # inject the function just before retryQuiz
        content = content.replace(
            'function retryQuiz(){',
            RESET_BADGES_FN + '\nfunction retryQuiz(){'
        )
        # call at start of retryQuiz  (add after the opening brace)
        content = re.sub(
            r'function retryQuiz\(\)\{',
            'function retryQuiz(){_resetBadges();',
            content, count=1
        )
        # call at start of returnToLevels
        if 'function returnToLevels(){' in content:
            content = re.sub(
                r'function returnToLevels\(\)\{',
                'function returnToLevels(){_resetBadges();',
                content, count=1
            )

    # ==================================================================
    # Write if changed
    # ==================================================================
    if content != orig:
        with open(fpath, 'w', encoding='utf-8') as fh:
            fh.write(content)
        patched.append(fname)
    else:
        errors.append(f'{fname}: لم يتغير شيء (ربما مُعدَّل مسبقاً؟)')

print(f'\n✅  تم التعديل : {len(patched)} ملف')
print(f'⏭️   تم التخطي  : {len(skipped_list)} ملف — {", ".join(skipped_list)}')
if errors:
    print(f'\n⚠️  ملاحظات ({len(errors)}):')
    for e in errors:
        print(f'   • {e}')
