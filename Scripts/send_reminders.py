#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
send_reminders.py
-------------------------------------------------------------------
سكربت إرسال تذكير الورد اليومي عبر Firebase Cloud Messaging.
يُشغَّل دوريًا عبر GitHub Action (.github/workflows/daily-reminder.yml)
— لا علاقة له بـ fix_files.py ولا يلمس أي ملف HTML في الموقع.

يقرأ التذكيرات المسجَّلة في Firestore (مجموعة darbi_reminders، كل
وثيقة فيها = جهاز واحد، مفتاحها = رمز الجهاز) ويبعت إشعارًا لكل جهاز
وقته الحالي (UTC) قريب من الوقت المطلوب، بحد أقصى مرة واحدة في اليوم
لكل جهاز.

ملاحظة مهمة: الموقع بلا حسابات ولا سيرفر خاص بنا، فالسكربت مش عارف
هل الزائرة خلّصت وردها اليوم ولا لأ — التذكير مبني على الوقت فقط.
-------------------------------------------------------------------
"""
import os
import sys
import json
import datetime

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, messaging
except ImportError:
    print("firebase-admin غير مثبَّت — نزّليه بـ: pip install firebase-admin", file=sys.stderr)
    sys.exit(1)

COLLECTION = 'darbi_reminders'
WINDOW_MINUTES = 12  # هامش تسامح لجدولة GitHub Action (تعمل كل ١٥ دقيقة تقريبًا)


def main():
    cred_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
    if not cred_json:
        print('السرّ FIREBASE_SERVICE_ACCOUNT_JSON غير موجود في بيئة التشغيل', file=sys.stderr)
        sys.exit(1)

    try:
        cred_data = json.loads(cred_json)
    except json.JSONDecodeError as e:
        print('تعذّر قراءة FIREBASE_SERVICE_ACCOUNT_JSON كـ JSON صالح:', e, file=sys.stderr)
        sys.exit(1)

    cred = credentials.Certificate(cred_data)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    now = datetime.datetime.utcnow()
    today_str = now.strftime('%Y-%m-%d')
    now_minutes = now.hour * 60 + now.minute

    sent, skipped, errors = 0, 0, 0

    for doc in db.collection(COLLECTION).stream():
        data = doc.to_dict() or {}
        token = doc.id
        utc_time = data.get('utcTime')
        if not utc_time:
            continue

        try:
            h, m = map(int, str(utc_time).split(':'))
        except (ValueError, AttributeError):
            continue

        target_minutes = h * 60 + m
        diff = abs(now_minutes - target_minutes)
        diff = min(diff, 1440 - diff)  # التفاف حوالين منتصف الليل
        if diff > WINDOW_MINUTES:
            continue

        if data.get('lastSentDate') == today_str:
            skipped += 1
            continue

        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title='دربي لحفظ القرآن',
                    body='🌙 لم تبدأ وردك اليوم بعد — إنه بانتظارك',
                ),
                token=token,
            )
            messaging.send(message)
            db.collection(COLLECTION).document(token).update({'lastSentDate': today_str})
            sent += 1
        except Exception as e:  # noqa: BLE001 — نلوجّ أي خطأ إرسال ونكمل الباقيين
            msg = str(e)
            # رمز جهاز ملغى/منتهي — نحذفه بدل تكرار محاولة فاشلة كل مرة
            if 'registration-token-not-registered' in msg or 'not found' in msg.lower():
                db.collection(COLLECTION).document(token).delete()
            errors += 1
            print('خطأ في الإرسال إلى', token[:12] + '…', ':', msg, file=sys.stderr)

    print(f'sent={sent} skipped={skipped} errors={errors}')


if __name__ == '__main__':
    main()
