#!/usr/bin/env python3
"""يزامن كتلة بدائل التعرف الصوتي (tools/stt_alts_block.js) داخل الملفين اللذين يستعملانها:
   recitation.html  و  voice-engine.js   (بين علامتي STT_ALTS_BEGIN / STT_ALTS_END).
   idempotent: تشغيله مرتين يعطي نفس الناتج. استعمله بعد أي تعديل في الكتلة:
       python3 tools/sync_stt_alts.py          # يكتب
       python3 tools/sync_stt_alts.py --check  # يتحقق فقط (exit 1 لو الملفات مش متطابقة)
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOCK = (ROOT / 'tools' / 'stt_alts_block.js').read_text(encoding='utf8').rstrip('\n')
PAT = re.compile(r'// ===== STT_ALTS_BEGIN =====.*?// ===== STT_ALTS_END =====', re.S)
check = '--check' in sys.argv
bad = 0
for name in ('recitation.html', 'voice-engine.js'):
    p = ROOT / name
    s = p.read_text(encoding='utf8')
    assert len(PAT.findall(s)) == 1, f'{name}: لازم علامة STT_ALTS واحدة بالظبط'
    new = PAT.sub(lambda m: BLOCK, s)
    if new != s:
        if check:
            print('DIFF', name); bad = 1
        else:
            p.write_text(new, encoding='utf8'); print('updated', name)
    else:
        print('in sync', name)
sys.exit(bad)
