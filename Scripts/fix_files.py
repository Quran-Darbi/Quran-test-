#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, json, hashlib, sys, time

# ====================================================
# بيانات AYAT للسور اللي كانت ناقصة (يوليو ٢٠٢٦)
# مستخرجة من صور المصحف مباشرة، مقسّمة آية بآية.
# بتتحقن تلقائيًا في الملف المناسب لو الملف من غير AYAT أصلاً.
# ====================================================
AYAT_DATA = {
"alfatiha": [
  "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
  "ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ",
  "ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
  "مَٰلِكِ يَوْمِ ٱلدِّينِ",
  "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
  "ٱهْدِنَا ٱلصِّرَٰطَ ٱلْمُسْتَقِيمَ",
  "صِرَٰطَ ٱلَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ ٱلْمَغْضُوبِ عَلَيْهِمْ وَلَا ٱلضَّآلِّينَ"
],
"atteen": [
  "وَٱلتِّينِ وَٱلزَّيْتُونِ",
  "وَطُورِ سِينِينَ",
  "وَهَٰذَا ٱلْبَلَدِ ٱلْأَمِينِ",
  "لَقَدْ خَلَقْنَا ٱلْإِنسَٰنَ فِىٓ أَحْسَنِ تَقْوِيمٍ",
  "ثُمَّ رَدَدْنَٰهُ أَسْفَلَ سَٰفِلِينَ",
  "إِلَّا ٱلَّذِينَ ءَامَنُوا وَعَمِلُوا ٱلصَّٰلِحَٰتِ فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ",
  "فَمَا يُكَذِّبُكَ بَعْدُ بِٱلدِّينِ",
  "أَلَيْسَ ٱللَّهُ بِأَحْكَمِ ٱلْحَٰكِمِينَ"
],
"alalaq": [
  "ٱقْرَأْ بِٱسْمِ رَبِّكَ ٱلَّذِى خَلَقَ",
  "خَلَقَ ٱلْإِنسَٰنَ مِنْ عَلَقٍ",
  "ٱقْرَأْ وَرَبُّكَ ٱلْأَكْرَمُ",
  "ٱلَّذِى عَلَّمَ بِٱلْقَلَمِ",
  "عَلَّمَ ٱلْإِنسَٰنَ مَا لَمْ يَعْلَمْ",
  "كَلَّآ إِنَّ ٱلْإِنسَٰنَ لَيَطْغَىٰٓ",
  "أَن رَّءَاهُ ٱسْتَغْنَىٰٓ",
  "إِنَّ إِلَىٰ رَبِّكَ ٱلرُّجْعَىٰٓ",
  "أَرَءَيْتَ ٱلَّذِى يَنْهَىٰ",
  "عَبْدًا إِذَا صَلَّىٰٓ",
  "أَرَءَيْتَ إِن كَانَ عَلَى ٱلْهُدَىٰٓ",
  "أَوْ أَمَرَ بِٱلتَّقْوَىٰٓ",
  "أَرَءَيْتَ إِن كَذَّبَ وَتَوَلَّىٰٓ",
  "أَلَمْ يَعْلَم بِأَنَّ ٱللَّهَ يَرَىٰ",
  "كَلَّا لَئِن لَّمْ يَنتَهِ لَنَسْفَعًۢا بِٱلنَّاصِيَةِ",
  "نَاصِيَةٍ كَٰذِبَةٍ خَاطِئَةٍ",
  "فَلْيَدْعُ نَادِيَهُۥ",
  "سَنَدْعُ ٱلزَّبَانِيَةَ",
  "كَلَّا لَا تُطِعْهُ وَٱسْجُدْ وَٱقْتَرِب"
],
"alqadr": [
  "إِنَّآ أَنزَلْنَٰهُ فِى لَيْلَةِ ٱلْقَدْرِ",
  "وَمَآ أَدْرَىٰكَ مَا لَيْلَةُ ٱلْقَدْرِ",
  "لَيْلَةُ ٱلْقَدْرِ خَيْرٌ مِّنْ أَلْفِ شَهْرٍ",
  "تَنَزَّلُ ٱلْمَلَٰٓئِكَةُ وَٱلرُّوحُ فِيهَا بِإِذْنِ رَبِّهِم مِّن كُلِّ أَمْرٍ",
  "سَلَٰمٌ هِىَ حَتَّىٰ مَطْلَعِ ٱلْفَجْرِ"
],
"albayyina": [
  "لَمْ يَكُنِ ٱلَّذِينَ كَفَرُوا مِنْ أَهْلِ ٱلْكِتَٰبِ وَٱلْمُشْرِكِينَ مُنفَكِّينَ حَتَّىٰ تَأْتِيَهُمُ ٱلْبَيِّنَةُ",
  "رَسُولٌ مِّنَ ٱللَّهِ يَتْلُوا۟ صُحُفًا مُّطَهَّرَةً",
  "فِيهَا كُتُبٌ قَيِّمَةٌ",
  "وَمَا تَفَرَّقَ ٱلَّذِينَ أُوتُوا۟ ٱلْكِتَٰبَ إِلَّا مِنۢ بَعْدِ مَا جَآءَتْهُمُ ٱلْبَيِّنَةُ",
  "وَمَآ أُمِرُوٓا۟ إِلَّا لِيَعْبُدُوا۟ ٱللَّهَ مُخْلِصِينَ لَهُ ٱلدِّينَ حُنَفَآءَ وَيُقِيمُوا۟ ٱلصَّلَوٰةَ وَيُؤْتُوا۟ ٱلزَّكَوٰةَ وَذَٰلِكَ دِينُ ٱلْقَيِّمَةِ",
  "إِنَّ ٱلَّذِينَ كَفَرُوا۟ مِنْ أَهْلِ ٱلْكِتَٰبِ وَٱلْمُشْرِكِينَ فِى نَارِ جَهَنَّمَ خَٰلِدِينَ فِيهَآ أُو۟لَٰٓئِكَ هُمْ شَرُّ ٱلْبَرِيَّةِ",
  "إِنَّ ٱلَّذِينَ ءَامَنُوا۟ وَعَمِلُوا۟ ٱلصَّٰلِحَٰتِ أُو۟لَٰٓئِكَ هُمْ خَيْرُ ٱلْبَرِيَّةِ",
  "جَزَآؤُهُمْ عِندَ رَبِّهِمْ جَنَّٰتُ عَدْنٍ تَجْرِى مِن تَحْتِهَا ٱلْأَنْهَٰرُ خَٰلِدِينَ فِيهَآ أَبَدًا رَّضِىَ ٱللَّهُ عَنْهُمْ وَرَضُوا۟ عَنْهُ ذَٰلِكَ لِمَنْ خَشِىَ رَبَّهُۥ"
],
"alzalzala": [
  "إِذَا زُلْزِلَتِ ٱلْأَرْضُ زِلْزَالَهَا",
  "وَأَخْرَجَتِ ٱلْأَرْضُ أَثْقَالَهَا",
  "وَقَالَ ٱلْإِنسَٰنُ مَا لَهَا",
  "يَوْمَئِذٍ تُحَدِّثُ أَخْبَارَهَا",
  "بِأَنَّ رَبَّكَ أَوْحَىٰ لَهَا",
  "يَوْمَئِذٍ يَصْدُرُ ٱلنَّاسُ أَشْتَاتًا لِّيُرَوْا۟ أَعْمَٰلَهُمْ",
  "فَمَن يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُۥ",
  "وَمَن يَعْمَلْ مِثْقَالَ ذَرَّةٍ شَرًّا يَرَهُۥ"
],
"alaadiyat": [
  "وَٱلْعَٰدِيَٰتِ ضَبْحًا",
  "فَٱلْمُورِيَٰتِ قَدْحًا",
  "فَٱلْمُغِيرَٰتِ صُبْحًا",
  "فَأَثَرْنَ بِهِۦ نَقْعًا",
  "فَوَسَطْنَ بِهِۦ جَمْعًا",
  "إِنَّ ٱلْإِنسَٰنَ لِرَبِّهِۦ لَكَنُودٌ",
  "وَإِنَّهُۥ عَلَىٰ ذَٰلِكَ لَشَهِيدٌ",
  "وَإِنَّهُۥ لِحُبِّ ٱلْخَيْرِ لَشَدِيدٌ",
  "أَفَلَا يَعْلَمُ إِذَا بُعْثِرَ مَا فِى ٱلْقُبُورِ",
  "وَحُصِّلَ مَا فِى ٱلصُّدُورِ",
  "إِنَّ رَبَّهُم بِهِمْ يَوْمَئِذٍ لَّخَبِيرٌ"
],
"alqaria": [
  "ٱلْقَارِعَةُ",
  "مَا ٱلْقَارِعَةُ",
  "وَمَآ أَدْرَىٰكَ مَا ٱلْقَارِعَةُ",
  "يَوْمَ يَكُونُ ٱلنَّاسُ كَٱلْفَرَاشِ ٱلْمَبْثُوثِ",
  "وَتَكُونُ ٱلْجِبَالُ كَٱلْعِهْنِ ٱلْمَنفُوشِ",
  "فَأَمَّا مَن ثَقُلَتْ مَوَٰزِينُهُۥ",
  "فَهُوَ فِى عِيشَةٍ رَّاضِيَةٍ",
  "وَأَمَّا مَنْ خَفَّتْ مَوَٰزِينُهُۥ",
  "فَأُمُّهُۥ هَاوِيَةٌ",
  "وَمَآ أَدْرَىٰكَ مَا هِيَهْ",
  "نَارٌ حَامِيَةٌ"
],
"altakathur": [
  "أَلْهَىٰكُمُ ٱلتَّكَاثُرُ",
  "حَتَّىٰ زُرْتُمُ ٱلْمَقَابِرَ",
  "كَلَّا سَوْفَ تَعْلَمُونَ",
  "ثُمَّ كَلَّا سَوْفَ تَعْلَمُونَ",
  "كَلَّا لَوْ تَعْلَمُونَ عِلْمَ ٱلْيَقِينِ",
  "لَتَرَوُنَّ ٱلْجَحِيمَ",
  "ثُمَّ لَتَرَوُنَّهَا عَيْنَ ٱلْيَقِينِ",
  "ثُمَّ لَتُسْـَٔلُنَّ يَوْمَئِذٍ عَنِ ٱلنَّعِيمِ"
],
"alasr": [
  "وَٱلْعَصْرِ",
  "إِنَّ ٱلْإِنسَٰنَ لَفِى خُسْرٍ",
  "إِلَّا ٱلَّذِينَ ءَامَنُوا وَعَمِلُوا ٱلصَّٰلِحَٰتِ وَتَوَاصَوْا۟ بِٱلْحَقِّ وَتَوَاصَوْا۟ بِٱلصَّبْرِ"
],
"alhumaza": [
  "وَيْلٌ لِّكُلِّ هُمَزَةٍ لُّمَزَةٍ",
  "ٱلَّذِى جَمَعَ مَالًا وَعَدَّدَهُۥ",
  "يَحْسَبُ أَنَّ مَالَهُۥٓ أَخْلَدَهُۥ",
  "كَلَّا لَيُنۢبَذَنَّ فِى ٱلْحُطَمَةِ",
  "وَمَآ أَدْرَىٰكَ مَا ٱلْحُطَمَةُ",
  "نَارُ ٱللَّهِ ٱلْمُوقَدَةُ",
  "ٱلَّتِى تَطَّلِعُ عَلَى ٱلْأَفْـِٔدَةِ",
  "إِنَّهَا عَلَيْهِم مُّؤْصَدَةٌ",
  "فِى عَمَدٍ مُّمَدَّدَةٍۭ"
],
"alfiyl": [
  "أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ بِأَصْحَٰبِ ٱلْفِيلِ",
  "أَلَمْ يَجْعَلْ كَيْدَهُمْ فِى تَضْلِيلٍ",
  "وَأَرْسَلَ عَلَيْهِمْ طَيْرًا أَبَابِيلَ",
  "تَرْمِيهِم بِحِجَارَةٍ مِّن سِجِّيلٍ",
  "فَجَعَلَهُمْ كَعَصْفٍ مَّأْكُولٍ"
],
"aquraysh": [
  "لِإِيلَٰفِ قُرَيْشٍ",
  "إِۦلَٰفِهِمْ رِحْلَةَ ٱلشِّتَآءِ وَٱلصَّيْفِ",
  "فَلْيَعْبُدُوا۟ رَبَّ هَٰذَا ٱلْبَيْتِ",
  "ٱلَّذِىٓ أَطْعَمَهُم مِّن جُوعٍ وَءَامَنَهُم مِّنْ خَوْفٍ"
],
"almaoon": [
  "أَرَءَيْتَ ٱلَّذِى يُكَذِّبُ بِٱلدِّينِ",
  "فَذَٰلِكَ ٱلَّذِى يَدُعُّ ٱلْيَتِيمَ",
  "وَلَا يَحُضُّ عَلَىٰ طَعَامِ ٱلْمِسْكِينِ",
  "فَوَيْلٌ لِّلْمُصَلِّينَ",
  "ٱلَّذِينَ هُمْ عَن صَلَاتِهِمْ سَاهُونَ",
  "ٱلَّذِينَ هُمْ يُرَآءُونَ",
  "وَيَمْنَعُونَ ٱلْمَاعُونَ"
],
"alkawthur": [
  "إِنَّآ أَعْطَيْنَٰكَ ٱلْكَوْثَرَ",
  "فَصَلِّ لِرَبِّكَ وَٱنْحَرْ",
  "إِنَّ شَانِئَكَ هُوَ ٱلْأَبْتَرُ"
],
"alkafirun": [
  "قُلْ يَٰٓأَيُّهَا ٱلْكَٰفِرُونَ",
  "لَآ أَعْبُدُ مَا تَعْبُدُونَ",
  "وَلَآ أَنتُمْ عَٰبِدُونَ مَآ أَعْبُدُ",
  "وَلَآ أَنَا۠ عَابِدٌ مَّا عَبَدتُّمْ",
  "وَلَآ أَنتُمْ عَٰبِدُونَ مَآ أَعْبُدُ",
  "لَكُمْ دِينُكُمْ وَلِىَ دِينِ"
],
"alnnasr": [
  "إِذَا جَآءَ نَصْرُ ٱللَّهِ وَٱلْفَتْحُ",
  "وَرَأَيْتَ ٱلنَّاسَ يَدْخُلُونَ فِى دِينِ ٱللَّهِ أَفْوَاجًا",
  "فَسَبِّحْ بِحَمْدِ رَبِّكَ وَٱسْتَغْفِرْهُ إِنَّهُۥ كَانَ تَوَّابًۢا"
],
"almasad": [
  "تَبَّتْ يَدَآ أَبِى لَهَبٍ وَتَبَّ",
  "مَآ أَغْنَىٰ عَنْهُ مَالُهُۥ وَمَا كَسَبَ",
  "سَيَصْلَىٰ نَارًا ذَاتَ لَهَبٍ",
  "وَٱمْرَأَتُهُۥ حَمَّالَةَ ٱلْحَطَبِ",
  "فِى جِيدِهَا حَبْلٌ مِّن مَّسَدٍ"
],
"alikhlas": [
  "قُلْ هُوَ ٱللَّهُ أَحَدٌ",
  "ٱللَّهُ ٱلصَّمَدُ",
  "لَمْ يَلِدْ وَلَمْ يُولَدْ",
  "وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌۢ"
],
"alfalaq": [
  "قُلْ أَعُوذُ بِرَبِّ ٱلْفَلَقِ",
  "مِن شَرِّ مَا خَلَقَ",
  "وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ",
  "وَمِن شَرِّ ٱلنَّفَّٰثَٰتِ فِى ٱلْعُقَدِ",
  "وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ"
],
"alnnas": [
  "قُلْ أَعُوذُ بِرَبِّ ٱلنَّاسِ",
  "مَلِكِ ٱلنَّاسِ",
  "إِلَٰهِ ٱلنَّاسِ",
  "مِن شَرِّ ٱلْوَسْوَاسِ ٱلْخَنَّاسِ",
  "ٱلَّذِى يُوَسْوِسُ فِى صُدُورِ ٱلنَّاسِ",
  "مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ"
],
}

OLD_RENDER_ORDER_QUIZ = (
    "function renderOrderQuiz(){\n"
    "  const slotsDiv=document.getElementById('order-slots');\n"
    "  const poolDiv=document.getElementById('order-pool');\n"
    "  slotsDiv.innerHTML='';\n"
    "  poolDiv.innerHTML='';\n"
    "  orderPlaced.forEach((idx,pos)=>{\n"
    "    const div=document.createElement('div');\n"
    "    if(idx===null){\n"
    "      const active=(pos===orderCursor);\n"
    "      div.className='order-slot empty'+(active?' active-slot':'');\n"
    "      div.innerHTML='<span class=\"order-badge\">'+toArabicNum(pos+1)+'</span><span class=\"order-slot-placeholder\">'+(active?'— الخانة النشطة الآن —':'— خانة فاضية، اضغط للمتابعة من هنا —')+'</span>';\n"
    "      div.onclick=()=>{orderCursor=pos;renderOrderQuiz();};\n"
    "    }else{\n"
    "      div.className='order-slot filled';\n"
    "      div.innerHTML='<span class=\"order-badge\">'+toArabicNum(pos+1)+'</span><span>'+AYAT[idx]+'</span>';\n"
    "      div.onclick=()=>{orderPlaced[pos]=null;orderCursor=pos;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};\n"
    "    }\n"
    "    slotsDiv.appendChild(div);\n"
    "  });\n"
    "  orderPoolOrder.forEach(idx=>{\n"
    "    if(orderPlaced.includes(idx))return;\n"
    "    const btn=document.createElement('button');\n"
    "    btn.className='order-item';\n"
    "    btn.textContent=AYAT[idx];\n"
    "    btn.onclick=()=>{\n"
    "      if(orderCursor===-1||orderPlaced[orderCursor]!==null){orderCursor=nextEmptyFrom(0);}\n"
    "      if(orderCursor===-1)return;\n"
    "      orderPlaced[orderCursor]=idx;\n"
    "      orderCursor=nextEmptyFrom(orderCursor+1);\n"
    "      document.getElementById('order-feedback').style.display='none';\n"
    "      renderOrderQuiz();\n"
    "    };\n"
    "    poolDiv.appendChild(btn);\n"
    "  });\n"
    "  const allFilled=!orderPlaced.includes(null);\n"
    "  document.getElementById('order-check-btn').style.display=allFilled?'block':'none';\n"
    "}\n"
)

NEW_RENDER_ORDER_QUIZ = (
    "function renderOrderQuiz(){\n"
    "  const slotsDiv=document.getElementById('order-slots');\n"
    "  const poolDiv=document.getElementById('order-pool');\n"
    "  slotsDiv.innerHTML='';\n"
    "  poolDiv.innerHTML='';\n"
    "  const filledGrid=document.createElement('div');\n"
    "  filledGrid.className='order-filled-grid';\n"
    "  const emptyStrip=document.createElement('div');\n"
    "  emptyStrip.className='order-empty-strip';\n"
    "  orderPlaced.forEach((idx,pos)=>{\n"
    "    if(idx===null){\n"
    "      const active=(pos===orderCursor);\n"
    "      const dot=document.createElement('span');\n"
    "      dot.className='order-dot'+(active?' active':'');\n"
    "      dot.textContent='﴿'+toArabicNum(pos+1)+'﴾';\n"
    "      dot.title=active?'الخانة النشطة الآن':'اضغط للمتابعة من هنا';\n"
    "      dot.onclick=()=>{orderCursor=pos;renderOrderQuiz();};\n"
    "      emptyStrip.appendChild(dot);\n"
    "    }else{\n"
    "      const card=document.createElement('div');\n"
    "      card.className='order-slot filled'+(pos===orderSelected?' order-slot-selected':'');\n"
    "      card.innerHTML='<span class=\"order-badge\">﴿'+toArabicNum(pos+1)+'﴾</span><span>'+AYAT[idx]+'</span>';\n"
    "      card.onclick=(e)=>{if(e.target.closest('.order-badge')){if(orderSelected===pos){orderSelected=-1;renderOrderQuiz();return;}if(orderSelected===-1){orderSelected=pos;renderOrderQuiz();return;}const tmp=orderPlaced[orderSelected];orderPlaced[orderSelected]=orderPlaced[pos];orderPlaced[pos]=tmp;orderSelected=-1;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();return;}orderPlaced[pos]=null;orderCursor=pos;orderSelected=-1;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};\n"
    "      filledGrid.appendChild(card);\n"
    "    }\n"
    "  });\n"
    "  if(filledGrid.children.length)slotsDiv.appendChild(filledGrid);\n"
    "  if(emptyStrip.children.length)slotsDiv.appendChild(emptyStrip);\n"
    "  orderPoolOrder.forEach(idx=>{\n"
    "    if(orderPlaced.includes(idx))return;\n"
    "    const btn=document.createElement('button');\n"
    "    btn.className='order-item';\n"
    "    btn.textContent=AYAT[idx];\n"
    "    btn.onclick=()=>{\n"
    "      if(orderCursor===-1||orderPlaced[orderCursor]!==null){orderCursor=nextEmptyFrom(0);}\n"
    "      if(orderCursor===-1)return;\n"
    "      orderPlaced[orderCursor]=idx;\n"
    "      orderCursor=nextEmptyFrom(orderCursor+1);\n"
    "      document.getElementById('order-feedback').style.display='none';\n"
    "      renderOrderQuiz();\n"
    "    };\n"
    "    poolDiv.appendChild(btn);\n"
    "  });\n"
    "  const allFilled=!orderPlaced.includes(null);\n"
    "  document.getElementById('order-check-btn').style.display=allFilled?'block':'none';\n"
    "}\n"
)


def inject_ayat_from_data(path, out):
    """يحقن AYAT تلقائيًا في الملف لو اسمه موجود في AYAT_DATA ومفيهوش AYAT أصلاً."""
    fn = os.path.splitext(os.path.basename(path))[0]
    if fn not in AYAT_DATA:
        return out, False
    if 'const AYAT=' in out or 'const AYAT =' in out:
        return out, False
    m = re.search(r"const RESUME_KEY=[^;]+;", out)
    if not m:
        return out, False
    ayat_js = "const AYAT=[\n" + ",\n".join(
        '  "' + a.replace('"', '\\"') + '"' for a in AYAT_DATA[fn]
    ) + "\n];\n"
    insert_pos = m.end()
    out = out[:insert_pos] + "\n" + ayat_js + out[insert_pos:]
    return out, True

# ===== كود PWA يُضاف لكل ملف =====
PWA_HEAD = """<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#4a7c4a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="دربي">
<link rel="apple-touch-icon" href="icons/icon-192x192.png">"""

PWA_SW = """<script>
if('serviceWorker' in navigator){
  window.addEventListener('load',()=>{
    navigator.serviceWorker.register('service-worker.js')
      .then(r=>console.log('SW:',r.scope))
      .catch(e=>console.log('SW err:',e));
  });
}
</script>"""

# ===== وضع المطوّر (يوليو ٢٠٢٦) =====
# يخفي مستوى "صعب" وزر التلاوة الصوتية عن أي زائر ما عندوش فلاج
# darbi_dev محفوظ في localStorage. تفعيل الفلاج: فتح أي صفحة بالرابط
# ?dev=1 مرة واحدة على المتصفح — وبعدها كل حاجة تفضل ظاهرة تلقائيًا.
DEV_MODE_LOCK = """<script>
(function(){
  try{
    var p=new URLSearchParams(location.search);
    if(p.get('dev')==='1'){localStorage.setItem('darbi_dev','1');}
    if(localStorage.getItem('darbi_dev')!=='1'){
      document.documentElement.classList.add('darbi-locked');
    }
  }catch(e){}
})();
</script>
<style>html.darbi-locked #btn-hard,html.darbi-locked a[href*="recitation.html"]{display:none !important;}</style>"""

# نسخة خاصة بـ recitation.html: بدل ما تخفي جزء من الصفحة، بترجّع
# أي زائر من غير الفلاج لصفحة index.html مباشرة (الصفحة كلها ميزة واحدة).
DEV_MODE_REDIRECT = """<script>
(function(){
  try{
    var p=new URLSearchParams(location.search);
    if(p.get('dev')==='1'){localStorage.setItem('darbi_dev','1');}
    if(localStorage.getItem('darbi_dev')!=='1'){
      location.replace('index.html');
    }
  }catch(e){}
})();
</script>"""

def add_dev_mode(out):
    """يحقن كود إخفاء المستوى الصعب/زر التلاوة (صفحات السور وindex.html)"""
    if 'darbi_dev' in out or '<head>' not in out:
        return out, False
    out = out.replace('<head>', '<head>\n' + DEV_MODE_LOCK, 1)
    return out, True

# ===== ودجت "💬 شاركنا رأيك" (يوليو ٢٠٢٦) =====
# زر عائم في كل صفحة يفتح نافذة صغيرة (نوع الملاحظة + تفاصيل) وعند
# الإرسال يفتح واتساب برسالة جاهزة تتضمن اسم الصفحة تلقائيًا. الرقم
# مكتوب داخل كود الصفحة (مش ظاهر كنص على الشاشة) بناءً على طلب هند —
# ملحوظة: ده مش إخفاء كامل 100%، أي حد يفتح "عرض المصدر" هيقدر يشوفه.
FEEDBACK_WIDGET = """<style>
.fdbk-fab{position:fixed;bottom:20px;left:20px;background:#2E6B3E;color:#fff;border:none;border-radius:50px;width:52px;height:52px;font-size:22px;box-shadow:0 4px 14px rgba(0,0,0,0.25);cursor:pointer;z-index:9999;display:flex;align-items:center;justify-content:center;}
.fdbk-fab:hover{filter:brightness(1.1);}
html[data-theme="dark"] .fdbk-fab{background:#4A9E40;}
.fdbk-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:10000;align-items:center;justify-content:center;padding:16px;}
.fdbk-overlay.open{display:flex;}
.fdbk-modal{background:#fff;border-radius:14px;max-width:380px;width:100%;padding:20px;border-top:4px solid #C4A84A;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;direction:rtl;text-align:right;}
html[data-theme="dark"] .fdbk-modal{background:#182018;color:#DCF0D8;}
.fdbk-modal h3{margin:0 0 12px;color:#2E6B3E;font-size:1.15rem;}
html[data-theme="dark"] .fdbk-modal h3{color:#6BBF5A;}
.fdbk-modal label{display:block;font-size:14px;margin:12px 0 6px;}
.fdbk-modal select,.fdbk-modal textarea{width:100%;padding:9px;border-radius:8px;border:1px solid #d8e0d8;background:#f7faf7;color:#222;font-family:inherit;font-size:14px;box-sizing:border-box;}
html[data-theme="dark"] .fdbk-modal select,html[data-theme="dark"] .fdbk-modal textarea{background:#101810;color:#DCF0D8;border-color:#2A4028;}
.fdbk-modal textarea{min-height:80px;resize:vertical;}
.fdbk-actions{display:flex;gap:8px;margin-top:16px;}
.fdbk-actions button{flex:1;padding:10px;border-radius:8px;border:none;font-size:14px;cursor:pointer;font-family:inherit;}
.fdbk-send{background:#2E6B3E;color:#fff;}
html[data-theme="dark"] .fdbk-send{background:#4A9E40;}
.fdbk-cancel{background:none;border:1px solid #d8e0d8;color:inherit;}
</style>
<button class="fdbk-fab" id="fdbk-fab-btn" onclick="fdbkOpen()" title="شاركنا رأيك">💬</button>
<div class="fdbk-overlay" id="fdbk-overlay">
  <div class="fdbk-modal">
    <h3>💬 شاركنا رأيك</h3>
    <label>نوع الملاحظة</label>
    <select id="fdbk-type">
      <option>خطأ في النص القرآني</option>
      <option>خطأ في السؤال أو الإجابة</option>
      <option>مشكلة في التسجيل الصوتي</option>
      <option>مشكلة تصميم أو عرض</option>
      <option>اقتراح تحسين</option>
      <option>أخرى</option>
    </select>
    <label>تفاصيل الملاحظة (اختياري)</label>
    <textarea id="fdbk-note" placeholder="اكتب ملاحظتك هنا..."></textarea>
    <div class="fdbk-actions">
      <button class="fdbk-send" onclick="fdbkSend()">إرسال عبر واتساب</button>
      <button class="fdbk-cancel" onclick="fdbkClose()">إلغاء</button>
    </div>
  </div>
</div>
<script>
function fdbkOpen(){document.getElementById('fdbk-overlay').classList.add('open');}
function fdbkClose(){document.getElementById('fdbk-overlay').classList.remove('open');}
function fdbkSend(){
  var type=document.getElementById('fdbk-type').value;
  var note=document.getElementById('fdbk-note').value.trim();
  var page=document.title||location.pathname.split('/').pop();
  var msg='ملاحظة من دربي لحفظ القرآن\\nالصفحة: '+page+'\\nالنوع: '+type+(note?'\\nالتفاصيل: '+note:'');
  window.open('https://wa.me/201034365326?text='+encodeURIComponent(msg),'_blank');
  fdbkClose();
}
</script>"""

# ===== ودجت اختيار اللغة (يوليو ٢٠٢٦) =====
# زر عائم أسفل يمين الشاشة (مقابل زر شاركنا رأيك أسفل اليسار — بدون
# تعارض). يعرض علم + اسم اللغة الحالية + سهم ▼. يترجم واجهة الموقع
# فقط عبر Google Translate (تعليمات/أزرار/رسائل)، مع حماية أي عنصر
# عليه class="notranslate" (نص الآيات وأسماء السور) من الترجمة نهائيًا.
LANG_WIDGET = """<style>
.lang-switch{position:fixed;bottom:20px;right:20px;z-index:9998;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;}
.lang-btn{display:flex;align-items:center;gap:6px;background:var(--card,#fff);color:var(--green,var(--accent,#2E6B3E));border:1.5px solid var(--border,#E4EAE4);border-radius:24px;padding:10px 14px;font-size:0.85rem;box-shadow:0 4px 14px var(--shadow,rgba(45,90,39,0.12));cursor:pointer;font-family:inherit;}
.lang-btn:hover{border-color:var(--green,var(--accent,#2E6B3E));}
.lang-btn .lang-arrow{font-size:0.6rem;color:var(--gold,#B8963A);transition:transform .2s;margin-inline-start:2px;}
.lang-switch.open .lang-arrow{transform:rotate(180deg);}
.lang-menu{display:none;position:absolute;bottom:52px;right:0;background:var(--card,#fff);border:1.5px solid var(--border,#E4EAE4);border-radius:14px;box-shadow:0 6px 20px var(--shadow,rgba(45,90,39,0.18));overflow:hidden;min-width:150px;border-top:3px solid var(--gold,#B8963A);}
.lang-switch.open .lang-menu{display:block;}
.lang-menu button{display:flex;align-items:center;gap:8px;width:100%;background:none;border:none;padding:11px 14px;font-size:0.85rem;color:var(--text,#1A1A1A);cursor:pointer;text-align:right;font-family:inherit;}
.lang-menu button:hover{background:var(--green3,var(--surface2,#F0F7F2));}
.lang-menu button.lang-active{color:var(--green,var(--accent,#2E6B3E));font-weight:700;}
#google_translate_element{display:none !important;}
.goog-te-banner-frame.skiptranslate{display:none !important;}
.goog-te-gadget{height:0;overflow:hidden;}
body{top:0 !important;}
</style>
<div class="lang-switch" id="lang-switch">
  <button class="lang-btn" id="lang-btn" onclick="langToggle(event)">
    <span id="lang-flag">🇸🇦</span><span id="lang-label">العربية</span><span class="lang-arrow">▼</span>
  </button>
  <div class="lang-menu" id="lang-menu">
    <button onclick="langSelect('ar','🇸🇦','العربية')" data-code="ar">🇸🇦 العربية</button>
    <button onclick="langSelect('en','🇬🇧','English')" data-code="en">🇬🇧 English</button>
    <button onclick="langSelect('fr','🇫🇷','Français')" data-code="fr">🇫🇷 Français</button>
    <button onclick="langSelect('tr','🇹🇷','Türkçe')" data-code="tr">🇹🇷 Türkçe</button>
    <button onclick="langSelect('fa','🇮🇷','فارسی')" data-code="fa">🇮🇷 فارسی</button>
    <button onclick="langSelect('de','🇩🇪','Deutsch')" data-code="de">🇩🇪 Deutsch</button>
    <button onclick="langSelect('es','🇪🇸','Español')" data-code="es">🇪🇸 Español</button>
  </div>
</div>
<div id="google_translate_element"></div>
<script>
function googleTranslateElementInit(){
  new google.translate.TranslateElement({pageLanguage:'ar',includedLanguages:'en,fr,tr,fa,de,es',autoDisplay:false},'google_translate_element');
}
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit" async></script>
<script>
function langCookie(){var m=document.cookie.match(/googtrans=([^;]+)/);return m?decodeURIComponent(m[1]):'';}
function langApplyLabel(){
  var map={ar:['🇸🇦','العربية'],en:['🇬🇧','English'],fr:['🇫🇷','Français'],tr:['🇹🇷','Türkçe'],fa:['🇮🇷','فارسی'],de:['🇩🇪','Deutsch'],es:['🇪🇸','Español']};
  var c=langCookie();var code='ar';
  if(c){var parts=c.split('/');if(parts[2])code=parts[2];}
  var d=map[code]||map.ar;
  document.getElementById('lang-flag').textContent=d[0];
  document.getElementById('lang-label').textContent=d[1];
  document.querySelectorAll('#lang-menu button').forEach(function(b){b.classList.toggle('lang-active',b.dataset.code===code);});
}
function langToggle(e){
  if(e)e.stopPropagation();
  document.getElementById('lang-switch').classList.toggle('open');
}
function langSelect(code){
  document.getElementById('lang-switch').classList.remove('open');
  if(code==='ar'){
    document.cookie='googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie='googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.'+location.hostname+';';
  }else{
    document.cookie='googtrans=/ar/'+code+'; path=/;';
  }
  location.reload();
}
document.addEventListener('click',function(e){
  var sw=document.getElementById('lang-switch');
  if(sw && !sw.contains(e.target))sw.classList.remove('open');
});
langApplyLabel();
</script>"""

# ===== قائمة "☰ الأدوات" الموحّدة (يوليو ٢٠٢٦) =====
# بعد ما عدد الأزرار العائمة زاد (شاركنا رأيك + اللغة + مشاركة + QR في
# الرئيسية)، دمجناهم كلهم في زر عائم واحد بيفتح قائمة، ماعدا 🌙 الوضع
# الليلي اللي فضل مكانه في الشريط العلوي زي ما هو (استخدام متكرر جدًا
# يستاهل نقرة واحدة مباشرة). القائمة نفس المنطق والدوال بالظبط
# (fdbkOpen/fdbkSend/langSelect/shareApp) — بس نقطة الدخول اتغيرت.
TOOLS_MENU_STYLE = """<style>
.tools-fab{position:fixed;top:14px;left:14px;z-index:9990;display:inline-flex;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;}
.tools-fab-btn{display:flex;align-items:center;justify-content:center;background:var(--green3,var(--surface2,#EAF2EA));color:var(--green,var(--accent,#2E6B3E));border:1px solid var(--border,#E4EAE4);border-radius:50%;width:34px;height:34px;font-size:1rem;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.15);}
.tools-fab-btn:hover{filter:brightness(1.05);}
.tools-menu{display:none;position:absolute;top:calc(100% + 8px);left:0;max-width:min(240px,calc(100vw - 24px));background:var(--card,#fff);border:1.5px solid var(--border,#E4EAE4);border-radius:14px;box-shadow:0 6px 20px rgba(0,0,0,0.18);overflow:hidden;min-width:195px;border-top:3px solid #C4A84A;z-index:9998;}
.tools-fab.open .tools-menu{display:block;}
.tools-item{display:flex;align-items:center;gap:8px;width:100%;background:none;border:none;padding:12px 14px;font-size:0.88rem;color:var(--text,#1A1A1A);cursor:pointer;text-align:right;font-family:inherit;}
.tools-item:hover{background:var(--green3,var(--surface2,#F0F7F2));}
.tools-item .tools-lang-inline{margin-inline-start:auto;display:flex;align-items:center;gap:4px;}
.tools-item .tools-lang-inline span:first-child{font-size:1em;color:inherit;}
.tools-item .tools-arrow{font-size:0.75em;color:#B8963A;transition:transform .2s;}
.tools-item svg{flex-shrink:0;}
.tools-lang-list{display:none;border-top:1px solid var(--border,#E4EAE4);background:var(--bg,#F7FAF7);}
.tools-lang-list.open{display:block;}
.tools-lang-list button{display:flex;align-items:center;gap:8px;width:100%;background:none;border:none;padding:10px 14px 10px 22px;font-size:0.82rem;color:var(--text,#1A1A1A);cursor:pointer;text-align:right;font-family:inherit;}
.tools-lang-list button:hover{background:var(--green3,var(--surface2,#F0F7F2));}
.tools-lang-list button.lang-active{font-weight:700;}
.tools-lang-list button .lang-check{margin-inline-start:auto;color:var(--green,#2E6B3E);font-weight:700;visibility:hidden;}
.tools-lang-list button.lang-active .lang-check{visibility:visible;}
#google_translate_element{display:none !important;}
.goog-te-banner-frame.skiptranslate{display:none !important;}
.goog-te-gadget{height:0;overflow:hidden;}
body{top:0 !important;}
.fdbk-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:10000;align-items:center;justify-content:center;padding:16px;}
.fdbk-overlay.open{display:flex;}
.fdbk-modal{background:#fff;border-radius:14px;max-width:380px;width:100%;padding:20px;border-top:4px solid #C4A84A;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;direction:rtl;text-align:right;}
html[data-theme="dark"] .fdbk-modal{background:#182018;color:#DCF0D8;}
.fdbk-modal h3{margin:0 0 12px;color:#2E6B3E;font-size:1.15rem;}
html[data-theme="dark"] .fdbk-modal h3{color:#6BBF5A;}
.fdbk-modal label{display:block;font-size:14px;margin:12px 0 6px;}
.fdbk-modal select,.fdbk-modal textarea{width:100%;padding:9px;border-radius:8px;border:1px solid #d8e0d8;background:#f7faf7;color:#222;font-family:inherit;font-size:14px;box-sizing:border-box;}
html[data-theme="dark"] .fdbk-modal select,html[data-theme="dark"] .fdbk-modal textarea{background:#101810;color:#DCF0D8;border-color:#2A4028;}
.fdbk-modal textarea{min-height:80px;resize:vertical;}
.fdbk-actions{display:flex;gap:8px;margin-top:16px;}
.fdbk-actions button{flex:1;padding:10px;border-radius:8px;border:none;font-size:14px;cursor:pointer;font-family:inherit;}
.fdbk-send{background:#2E6B3E;color:#fff;}
html[data-theme="dark"] .fdbk-send{background:#4A9E40;}
.fdbk-cancel{background:none;border:1px solid #d8e0d8;color:inherit;}
.qr-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.55);z-index:10001;align-items:center;justify-content:center;padding:16px;}
.qr-overlay.open{display:flex;}
.qr-modal{background:var(--card,#fff);border:1px solid var(--border,#E4EAE4);border-radius:18px;padding:22px;max-width:320px;width:100%;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,0.2);border-top:4px solid #C4A84A;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;}
.qr-title{font-size:1.05rem;color:#2E6B3E;font-weight:700;margin-bottom:14px;}
html[data-theme="dark"] .qr-title{color:#6BBF5A;}
.qr-img{border-radius:12px;border:1px solid var(--border,#E4EAE4);background:#fff;padding:8px;}
.qr-caption{font-size:0.8rem;color:var(--text,#1A1A1A);margin-top:12px;line-height:1.6;}
.qr-caption .qr-caption-en{direction:ltr;display:inline-block;font-size:0.72em;color:var(--soft,#888);margin-top:2px;}
.qr-url{font-size:0.72rem;color:var(--soft,#888);margin-top:8px;direction:ltr;word-break:break-all;}
.qr-actions{display:flex;gap:8px;margin-top:16px;}
.qr-actions button{flex:1;padding:10px;border-radius:10px;font-size:0.85rem;font-family:inherit;cursor:pointer;}
.qr-copy-btn{background:#2E6B3E;color:#fff;border:none;}
html[data-theme="dark"] .qr-copy-btn{background:#4A9E40;}
.qr-close-btn{background:none;border:1px solid var(--border,#E4EAE4);color:var(--text,#1A1A1A);}
</style>"""

# جزء الزر + القائمة نفسها — بيتحط جوه الـnav جنب زر 🌙 مباشرة (مش عائم)
NAV_TOOLS_BTN = """<div class="tools-fab" id="tools-fab">
  <button class="tools-fab-btn" id="tools-fab-btn" onclick="toolsToggle(event)" title="الأدوات">☰</button>
  <div class="tools-menu" id="tools-menu">
    <button class="tools-item" onclick="toolsLangToggle(event)">🌍 اللغة <span class="tools-lang-inline"><span id="tools-lang-cur">العربية</span><span class="tools-arrow" id="tools-lang-arrow">▾</span></span></button>
    <div class="tools-lang-list" id="tools-lang-list">
      <button onclick="langSelect('ar')" data-code="ar">العربية<span class="lang-check">✓</span></button>
      <button onclick="langSelect('en')" data-code="en">🇬🇧 English<span class="lang-check">✓</span></button>
      <button onclick="langSelect('es')" data-code="es">🇪🇸 Español<span class="lang-check">✓</span></button>
      <button onclick="langSelect('fr')" data-code="fr">🇫🇷 Français<span class="lang-check">✓</span></button>
      <button onclick="langSelect('de')" data-code="de">🇩🇪 Deutsch<span class="lang-check">✓</span></button>
      <button onclick="langSelect('tr')" data-code="tr">🇹🇷 Türkçe<span class="lang-check">✓</span></button>
      <button onclick="langSelect('fa')" data-code="fa">🇮🇷 فارسی<span class="lang-check">✓</span></button>
    </div>
    <button class="tools-item" onclick="toolsClose();fdbkOpen();">💬 الاقتراحات</button>
    <button class="tools-item" onclick="toolsClose();shareApp();"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.6" y1="10.5" x2="15.4" y2="6.5"/><line x1="8.6" y1="13.5" x2="15.4" y2="17.5"/></svg> مشاركة الصفحة</button>
    <button class="tools-item" onclick="toolsClose();showQR();"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><rect x="8" y="8" width="8" height="8" rx="1"/></svg> كود QR</button>
  </div>
</div>"""

# باقي الودجت (المودالز + الاسكريبتات) — بتفضل تتحقن قبل </body> زي الأول
TOOLS_MODALS_TEMPLATE = """<div class="fdbk-overlay" id="fdbk-overlay">
  <div class="fdbk-modal">
    <h3>💬 شاركنا رأيك</h3>
    <label>نوع الملاحظة</label>
    <select id="fdbk-type">
      <option>خطأ في النص القرآني</option>
      <option>خطأ في السؤال أو الإجابة</option>
      <option>مشكلة في التسجيل الصوتي</option>
      <option>مشكلة تصميم أو عرض</option>
      <option>اقتراح تحسين</option>
      <option>أخرى</option>
    </select>
    <label>تفاصيل الملاحظة (اختياري)</label>
    <textarea id="fdbk-note" placeholder="اكتب ملاحظتك هنا..."></textarea>
    <div class="fdbk-actions">
      <button class="fdbk-send" onclick="fdbkSend()">إرسال عبر واتساب</button>
      <button class="fdbk-cancel" onclick="fdbkClose()">إلغاء</button>
    </div>
  </div>
</div>
<div class="qr-overlay" id="qr-overlay" onclick="if(event.target===this)closeQR()">
  <div class="qr-modal">
    <div class="qr-title">🔲 امسح الكود لفتح الصفحة</div>
    <img class="qr-img" id="qr-img" src="" alt="QR كود لفتح هذه الصفحة على الموبايل" width="260" height="260" loading="lazy">
    <div class="qr-caption">امسح الكود لفتح الموقع على موبايلك<br><span class="qr-caption-en">Scan to open Quran Darbi</span></div>
    <div class="qr-url notranslate" translate="no" id="qr-url-text"></div>
    <div class="qr-actions">
      <button class="qr-copy-btn" onclick="copyQRLink()" id="qr-copy-btn">📋 نسخ الرابط</button>
      <button class="qr-close-btn" onclick="closeQR()">إغلاق</button>
    </div>
  </div>
</div>
<div id="google_translate_element"></div>
<script>
function googleTranslateElementInit(){
  new google.translate.TranslateElement({pageLanguage:'ar',includedLanguages:'en,fr,tr,fa,de,es',autoDisplay:false},'google_translate_element');
}
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit" async></script>
<script>
function toolsToggle(e){if(e)e.stopPropagation();document.getElementById('tools-fab').classList.toggle('open');}
function toolsClose(){document.getElementById('tools-fab').classList.remove('open');var l=document.getElementById('tools-lang-list');if(l)l.classList.remove('open');}
function toolsLangToggle(e){if(e)e.stopPropagation();var l=document.getElementById('tools-lang-list');var a=document.getElementById('tools-lang-arrow');l.classList.toggle('open');a.style.transform=l.classList.contains('open')?'rotate(180deg)':'rotate(0)';}
document.addEventListener('click',function(e){var w=document.getElementById('tools-fab');if(w&&!w.contains(e.target))toolsClose();});

function fdbkOpen(){toolsClose();document.getElementById('fdbk-overlay').classList.add('open');}
function fdbkClose(){document.getElementById('fdbk-overlay').classList.remove('open');}
function fdbkSend(){
  var type=document.getElementById('fdbk-type').value;
  var note=document.getElementById('fdbk-note').value.trim();
  var page=document.title||location.pathname.split('/').pop();
  var msg='ملاحظة من دربي لحفظ القرآن\\nالصفحة: '+page+'\\nالنوع: '+type+(note?'\\nالتفاصيل: '+note:'');
  window.open('https://wa.me/201034365326?text='+encodeURIComponent(msg),'_blank');
  fdbkClose();
}

function showQR(){
  var url=location.href;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&margin=10&data='+encodeURIComponent(url);
  document.getElementById('qr-url-text').textContent=url.replace(/^https?:\\/\\//,'');
  document.getElementById('qr-overlay').classList.add('open');
}
function closeQR(){document.getElementById('qr-overlay').classList.remove('open');}
function copyQRLink(){
  var url=location.href;
  var b=document.getElementById('qr-copy-btn');
  navigator.clipboard.writeText(url).then(function(){b.textContent='✅ تم النسخ';setTimeout(function(){b.textContent='📋 نسخ الرابط';},2000);}).catch(function(){b.textContent='تعذر النسخ';setTimeout(function(){b.textContent='📋 نسخ الرابط';},2000);});
}

function langCookie(){var m=document.cookie.match(/googtrans=([^;]+)/);return m?decodeURIComponent(m[1]):'';}
function langApplyLabel(){
  var map={ar:'العربية',en:'English',fr:'Français',tr:'Türkçe',fa:'فارسی',de:'Deutsch',es:'Español'};
  var c=langCookie();var code='ar';
  if(c){var parts=c.split('/');if(parts[2])code=parts[2];}
  var cur=document.getElementById('tools-lang-cur');
  if(cur)cur.textContent=map[code]||map.ar;
  document.querySelectorAll('#tools-lang-list button').forEach(function(b){b.classList.toggle('lang-active',b.dataset.code===code);});
}
function langSelect(code){
  if(code==='ar'){
    document.cookie='googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie='googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.'+location.hostname+';';
  }else{
    document.cookie='googtrans=/ar/'+code+'; path=/;';
  }
  location.reload();
}
langApplyLabel();
</script>"""

SHARE_BTN_ANY_RE = re.compile(r'\s*<button[^>]*onclick="shareApp\(\)"[^>]*>🔗</button>')
QR_NAV_BTN_RE = re.compile(r'\s*<button onclick="showQR\(\)"[^>]*>.*?</button>', re.S)


def strip_div_block(html, start_marker):
    """يشيل عنصر <div ...>...</div> بالكامل بداية من start_marker، مع
    عدّ الأعماق الصحيح (مش regex ساذج) عشان ديف متداخلة جوه بعض متتقطعش
    غلط. بيرجع (html_بعد_الحذف, تم_الحذف)."""
    i = html.find(start_marker)
    if i == -1:
        return html, False
    depth = 0
    j = i
    open_re = re.compile(r'<div\b')
    close_tag = '</div>'
    while j < len(html):
        nxt_open = html.find('<div', j)
        nxt_close = html.find(close_tag, j)
        if nxt_close == -1:
            return html, False  # مش متوازن — منعمل حاجة أسلم
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            j = nxt_open + 4
        else:
            depth -= 1
            j = nxt_close + len(close_tag)
            if depth == 0:
                end = j
                # ناكل أي سطر فاضي بعد الحذف
                while end < len(html) and html[end] == '\n':
                    end += 1
                return html[:i] + html[end:], True
    return html, False


# الكود القديم اللي كان متكتوب يدويًا جوه index.html نفسها (قبل ما
# ميزة الـQR تتحول لودجت مشتركة قابلة للتعميم على كل الملفات)
OLD_INDEX_QR_CSS = (
    ".qr-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.55);z-index:9997;align-items:center;justify-content:center;padding:16px;}\n"
    ".qr-overlay.open{display:flex;}\n"
    ".qr-modal{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:22px;max-width:320px;width:100%;text-align:center;box-shadow:0 8px 30px var(--shadow);border-top:4px solid var(--gold);}\n"
    ".qr-title{font-family:'Scheherazade New',serif;font-size:1.05rem;color:var(--green);font-weight:700;margin-bottom:14px;}\n"
    ".qr-img{border-radius:12px;border:1px solid var(--border);background:#fff;padding:8px;}\n"
    ".qr-url{font-size:0.78rem;color:var(--soft);margin-top:10px;direction:ltr;word-break:break-all;}\n"
    ".qr-actions{display:flex;gap:8px;margin-top:16px;}\n"
    ".qr-actions button{flex:1;padding:10px;border-radius:10px;font-size:0.85rem;font-family:'Amiri',serif;cursor:pointer;}\n"
    ".qr-copy-btn{background:var(--green);color:#fff;border:none;}\n"
    ".qr-close-btn{background:none;border:1px solid var(--border);color:var(--text);}"
)
OLD_INDEX_QR_JS = (
    "function showQR(){document.getElementById('qr-overlay').classList.add('open');}\n"
    "function closeQR(){document.getElementById('qr-overlay').classList.remove('open');}\n"
    "function copyQRLink(){var url='https://quran-darbi.github.io/Quran-test-/';var b=document.getElementById('qr-copy-btn');navigator.clipboard.writeText(url).then(function(){b.textContent='✅ تم النسخ';setTimeout(function(){b.textContent='📋 نسخ الرابط';},2000);}).catch(function(){b.textContent='تعذر النسخ';setTimeout(function(){b.textContent='📋 نسخ الرابط';},2000);});}"
)


THEME_BTN_RE = re.compile(r'<button[^>]*id="theme-(?:btn|toggle)"[^>]*>[^<]*</button>')


OLD_TOOLS_FAB_POSITION = ".tools-fab{position:relative;display:inline-flex;z-index:60;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;}"
NEW_TOOLS_FAB_POSITION = ".tools-fab{position:fixed;top:14px;left:14px;z-index:9990;display:inline-flex;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;}"
OLD_TOOLS_FAB_BTN_STYLE = ".tools-fab-btn{display:flex;align-items:center;justify-content:center;background:var(--green3,var(--surface2,#EAF2EA));color:var(--green,var(--accent,#2E6B3E));border:1px solid var(--border,#E4EAE4);border-radius:50%;width:34px;height:34px;font-size:1rem;cursor:pointer;}"
NEW_TOOLS_FAB_BTN_STYLE = ".tools-fab-btn{display:flex;align-items:center;justify-content:center;background:var(--green3,var(--surface2,#EAF2EA));color:var(--green,var(--accent,#2E6B3E));border:1px solid var(--border,#E4EAE4);border-radius:50%;width:34px;height:34px;font-size:1rem;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.15);}"


def upgrade_tools_fab_fixed_position(out):
    """يثبّت زر ☰ الأدوات في مكان عائم ثابت (أعلى الشاشة يسار) بدل ما
    يكون جوه صف الهيدر — لأن صف الهيدر بيختلف شكله شوية بين قوالب
    الصفحات المختلفة (البقرة/جزء عم/الفهرس)، فكان مكان الزر بيتزحلق
    من صفحة لصفحة. بقى position:fixed فهيفضل في نفس البكسل بالظبط
    في كل صفحات الموقع (يوليو ٢٠٢٦)."""
    changed = False
    if OLD_TOOLS_FAB_POSITION in out:
        out = out.replace(OLD_TOOLS_FAB_POSITION, NEW_TOOLS_FAB_POSITION, 1)
        changed = True
    if OLD_TOOLS_FAB_BTN_STYLE in out:
        out = out.replace(OLD_TOOLS_FAB_BTN_STYLE, NEW_TOOLS_FAB_BTN_STYLE, 1)
        changed = True
    return out, changed


TRANSLATE_BAR_CSS_RE = re.compile(
    r'\n?[ \t]*\.translate-bar\s*\{[^}]*\}\n?', re.S
)
TRANSLATE_BAR_DIV_RE = re.compile(
    r'\n?<div class="translate-bar">.*?</div>\n?', re.S
)

def remove_legacy_translate_bar(out):
    """يشيل زر '🌐 ترجمة' العائم القديم (.translate-bar) من الصفحات
    القديمة اللي سبقت ودجت اللغة (LANG_WIDGET) وقائمة الأدوات الموحدة.
    الزر ده عنصر ميت تمامًا (مالوش onclick ولا أي JS بيستهدفه) وفضل
    باقي في بعض الصفحات (زي albaqara_p9/p26) لأنه مش جزء من أي نص
    ثابت بتشيله add_tools_menu — فبنشيله هنا بريجيكس مستقل، بغض النظر
    عن وجود قائمة الأدوات من عدمه، عشان يتغطى في أي صفحة لسه فيها."""
    changed = False
    if '.translate-bar' in out:
        out, n = TRANSLATE_BAR_CSS_RE.subn('', out, count=1)
        if n:
            changed = True
    if '<div class="translate-bar">' in out:
        out, n = TRANSLATE_BAR_DIV_RE.subn('', out, count=1)
        if n:
            changed = True
    return out, changed

def add_tools_menu(path, out):
    """يستبدل الودجتين المنفصلتين (شاركنا رأيك + اللغة) وزر المشاركة
    وزر QR المنفصلين من الشريط العلوي، وكمان الزر العائم القديم لـ☰
    الأدوات، بزر "☰" مدمج جوه الشريط العلوي نفسه جنب 🌙 مباشرة (مش
    عائم فوق المحتوى). نفس الدوال والمنطق بالظبط (fdbkOpen/fdbkSend/
    langSelect/shareApp/showQR)، بس مكان الزر اتغير. ميزة الـQR متاحة
    في كل الصفحات وبتولّد رابط الصفحة الحالية ديناميكيًا."""
    is_index = os.path.basename(path) == 'index.html'
    changed = False

    # إزالة الودجتين القديمتين المنفصلتين لو موجودين (نصوص طبق الأصل، آمن)
    if FEEDBACK_WIDGET in out:
        out = out.replace(FEEDBACK_WIDGET, '', 1)
        changed = True
    if LANG_WIDGET in out:
        out = out.replace(LANG_WIDGET, '', 1)
        changed = True

    # إزالة زر المشاركة 🔗 القديم من الشريط العلوي (دالة shareApp() فضلت
    # موجودة زي ما هي — بس نقطة استدعاءها بقت من قائمة الأدوات)
    if SHARE_BTN_ANY_RE.search(out):
        out = SHARE_BTN_ANY_RE.sub('', out, count=1)
        changed = True

    # index.html بس: إزالة زر QR ونافذة QR الثابتة القديمتين (كانت
    # بتولّد رابط الرئيسية دايمًا) — النسخة الجديدة في القائمة الموحدة
    # بتولّد رابط الصفحة الحالية ديناميكيًا وشغالة في كل الصفحات.
    # الشرط التاني هنا مهم: من غيره الحذف ده بيتكرر كل مرة ويشيل
    # qr-overlay بتاع القائمة الجديدة نفسها بالغلط بعد أول تشغيل
    if is_index and 'id="tools-fab"' not in out:
        if QR_NAV_BTN_RE.search(out):
            out = QR_NAV_BTN_RE.sub('', out, count=1)
            changed = True
        out, qr_removed = strip_div_block(out, '<div class="qr-overlay" id="qr-overlay"')
        if qr_removed:
            changed = True
        # الكود القديم المكتوب يدويًا (CSS + JS) قبل ما الميزة تتحول لودجت
        if OLD_INDEX_QR_CSS in out:
            out = out.replace(OLD_INDEX_QR_CSS, '', 1)
            changed = True
        if OLD_INDEX_QR_JS in out:
            out = out.replace(OLD_INDEX_QR_JS, '', 1)
            changed = True

    # نسخة قديمة من القائمة موجودة (عائمة position:fixed، من قبل — بـQR
    # أو من غيره) — نشيلها بالكامل (الـstyle + الزر العائم + المودالز +
    # السكربتات) ونحقن النسخة الجديدة المقسّمة (زر جوه الـnav + مودالز
    # قبل </body>) بدالها. لو النسخة الحالية أصلاً هي الجديدة
    # (position:relative) منلمسهاش خالص.
    _tools_needs_upgrade = (
        '.tools-fab{position:fixed' in out  # نسخة عائمة قديمة
        or 'class="tools-cur"' in out        # شكل قديم لسهم اللغة
        or '📤 مشاركة</button>' in out        # أيقونة مشاركة قديمة
        or '📱 QR Code</button>' in out       # أيقونة QR قديمة
    )
    if 'id="tools-fab"' in out and _tools_needs_upgrade:
        # الحالة القديمة العائمة: الزر + الـstyle + المودالز كانوا كتلة
        # واحدة قبل </body> مباشرة — شيلهم مع بعض
        start = out.find('<style>\n.tools-fab{')
        end_marker = 'langApplyLabel();\n</script>'
        end_i = out.find(end_marker, start) if start != -1 else -1
        if start != -1 and end_i != -1:
            end = end_i + len(end_marker)
            while end < len(out) and out[end] == '\n':
                end += 1
            out = out[:start] + out[end:]
            changed = True
        # الحالة الحالية (زر جوه الـnav + محتوى قديم): الزر منفصل عن
        # الـstyle، لازم يتشال لوحده كمان عشان منسيبش نسخة قديمة مكررة
        if 'id="tools-fab"' in out:
            out, nav_btn_removed = strip_div_block(out, '<div class="tools-fab" id="tools-fab">')
            if nav_btn_removed:
                changed = True

    if 'id="tools-fab"' in out:
        return out, changed  # القائمة الجديدة (الشريط العلوي) موجودة بالفعل

    if '</body>' not in out:
        return out, changed

    # 1) الزر نفسه — يتحط جنب 🌙 في الشريط العلوي
    m = THEME_BTN_RE.search(out)
    if m:
        out = out[:m.end()] + NAV_TOOLS_BTN + out[m.end():]
        changed = True
    else:
        # مفيش زر وضع ليلي؟ احتياطي: نحط الزر عائم زي الأول بدل ما يضيع
        out = out.replace('</body>', NAV_TOOLS_BTN + '\n</body>', 1)
        changed = True

    # 2) الأنماط + المودالز + السكربتات — تفضل قبل </body>
    out = out.replace('</body>', TOOLS_MENU_STYLE + '\n' + TOOLS_MODALS_TEMPLATE + '\n</body>', 1)
    return out, True

SHARE_OLD_SINGLELINE = "function shareApp(){var url='https://quran-darbi.github.io/Quran-test-/';if(navigator.share){navigator.share({title:'دربي لحفظ القرآن',url:url}).catch(function(){});}else{navigator.clipboard.writeText(url).then(function(){var b=document.querySelector('[onclick=\"shareApp()\"]');if(b){b.textContent='✅';setTimeout(function(){b.textContent='🔗';},2000);}}).catch(function(){});}}"
SHARE_NEW_SINGLELINE = "function shareApp(){var url=location.href;var t=document.title||'دربي لحفظ القرآن';if(navigator.share){navigator.share({title:t,url:url}).catch(function(){});}else if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){var b=document.getElementById('tools-fab-btn');if(b){var old=b.textContent;b.textContent='✅';setTimeout(function(){b.textContent=old;},1800);}}).catch(function(){});}}"

SHARE_OLD_RECITE = "function shareApp(){\n  const url='https://quran-darbi.github.io/Quran-test-/';\n  const title='دربي لحفظ القرآن';\n  if(navigator.share){\n    navigator.share({title,url}).catch(()=>{});\n  } else {\n    navigator.clipboard.writeText(url).then(()=>{\n      const btn=document.getElementById('share-btn');\n      btn.textContent='✅';\n      setTimeout(()=>btn.textContent='🔗',2000);\n    }).catch(()=>{});\n  }\n}"
SHARE_NEW_RECITE = "function shareApp(){\n  const url=location.href;\n  const title=(typeof SURAH_NAMES!=='undefined'&&currentKey&&SURAH_NAMES[currentKey])?('دربي لحفظ القرآن — '+SURAH_NAMES[currentKey]):'دربي لحفظ القرآن';\n  if(navigator.share){\n    navigator.share({title,url}).catch(()=>{});\n  } else {\n    navigator.clipboard.writeText(url).then(()=>{\n      const btn=document.getElementById('tools-fab-btn');\n      if(btn){const old=btn.textContent;btn.textContent='✅';setTimeout(()=>btn.textContent=old,1800);}\n    }).catch(()=>{});\n  }\n}"


def upgrade_share_current_page(out):
    """زر المشاركة كان بيشارك رابط الرئيسية دايمًا مهما كانت الصفحة
    المفتوحة. دلوقتي بيشارك رابط الصفحة الحالية نفسها (بما فيها
    ?surah= في اختبار التلاوة)، والعنوان بقى ديناميكي من عنوان الصفحة
    (أو اسم السورة الحالية في اختبار التلاوة) بدل نص ثابت. كمان بيصلح
    مرجع 'share-btn' اللي اتشال من الشريط العلوي (بقى 'tools-fab-btn')."""
    changed = False
    if SHARE_OLD_SINGLELINE in out and SHARE_NEW_SINGLELINE not in out:
        out = out.replace(SHARE_OLD_SINGLELINE, SHARE_NEW_SINGLELINE, 1)
        changed = True
    if SHARE_OLD_RECITE in out and SHARE_NEW_RECITE not in out:
        out = out.replace(SHARE_OLD_RECITE, SHARE_NEW_RECITE, 1)
        changed = True
    return out, changed


def upgrade_lang_switcher_languages(out):
    """ترقية رجعية: ودجت اللغة القديم (عربي/إنجليزي/فرنسي بس) بيتحدث
    للنسخة الجديدة اللي فيها تركي/فارسي/ألماني/إسباني كمان (يوليو ٢٠٢٦).
    idempotent — بيتخطى أي ملف مُرقّى بالفعل."""
    if 'lang-switch' not in out or "langSelect('tr'" in out:
        return out, False

    old_menu = """  <div class="lang-menu" id="lang-menu">
    <button onclick="langSelect('ar','🇸🇦','العربية')" data-code="ar">🇸🇦 العربية</button>
    <button onclick="langSelect('en','🇬🇧','English')" data-code="en">🇬🇧 English</button>
    <button onclick="langSelect('fr','🇫🇷','Français')" data-code="fr">🇫🇷 Français</button>
    <button onclick="langSelect('tr','🇹🇷','Türkçe')" data-code="tr">🇹🇷 Türkçe</button>
    <button onclick="langSelect('fa','🇮🇷','فارسی')" data-code="fa">🇮🇷 فارسی</button>
    <button onclick="langSelect('de','🇩🇪','Deutsch')" data-code="de">🇩🇪 Deutsch</button>
    <button onclick="langSelect('es','🇪🇸','Español')" data-code="es">🇪🇸 Español</button>
  </div>
</div>
<div id="google_translate_element"></div>
<script>
function googleTranslateElementInit(){
  new google.translate.TranslateElement({pageLanguage:'ar',includedLanguages:'en,fr,tr,fa,de,es',autoDisplay:false},'google_translate_element');
}
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit" async></script>
<script>
function langCookie(){var m=document.cookie.match(/googtrans=([^;]+)/);return m?decodeURIComponent(m[1]):'';}
function langApplyLabel(){
  var map={ar:['🇸🇦','العربية'],en:['🇬🇧','English'],fr:['🇫🇷','Français'],tr:['🇹🇷','Türkçe'],fa:['🇮🇷','فارسی'],de:['🇩🇪','Deutsch'],es:['🇪🇸','Español']};"""

    new_menu = """  <div class="lang-menu" id="lang-menu">
    <button onclick="langSelect('ar','🇸🇦','العربية')" data-code="ar">🇸🇦 العربية</button>
    <button onclick="langSelect('en','🇬🇧','English')" data-code="en">🇬🇧 English</button>
    <button onclick="langSelect('fr','🇫🇷','Français')" data-code="fr">🇫🇷 Français</button>
    <button onclick="langSelect('tr','🇹🇷','Türkçe')" data-code="tr">🇹🇷 Türkçe</button>
    <button onclick="langSelect('fa','🇮🇷','فارسی')" data-code="fa">🇮🇷 فارسی</button>
    <button onclick="langSelect('de','🇩🇪','Deutsch')" data-code="de">🇩🇪 Deutsch</button>
    <button onclick="langSelect('es','🇪🇸','Español')" data-code="es">🇪🇸 Español</button>
  </div>
</div>
<div id="google_translate_element"></div>
<script>
function googleTranslateElementInit(){
  new google.translate.TranslateElement({pageLanguage:'ar',includedLanguages:'en,fr,tr,fa,de,es',autoDisplay:false},'google_translate_element');
}
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit" async></script>
<script>
function langCookie(){var m=document.cookie.match(/googtrans=([^;]+)/);return m?decodeURIComponent(m[1]):'';}
function langApplyLabel(){
  var map={ar:['🇸🇦','العربية'],en:['🇬🇧','English'],fr:['🇫🇷','Français'],tr:['🇹🇷','Türkçe'],fa:['🇮🇷','فارسی'],de:['🇩🇪','Deutsch'],es:['🇪🇸','Español']};"""

    if old_menu not in out:
        return out, False
    out = out.replace(old_menu, new_menu, 1)
    return out, True

def protect_order_ayat_from_translation(out):
    """ترقية رجعية: الملفات اللي أُضيفت فيها ميزة الترتيب 🔀 قبل ودجت
    اللغة (يوليو ٢٠٢٦) كانت بتعرض نص الآية كامل من غير حماية من الترجمة.
    الدالة دي بتصحح الأنماط القديمة الثلاثة لو موجودة (idempotent)."""
    changed = False
    old1 = "return '<div class=\"mushaf-block\">'+AYAT.map((t,i)=>t+' <span class=\"ayah-end\">﴿'+toArabicNum(i+1)+'﴾</span>').join(' ')+'</div>';"
    new1 = "return '<div class=\"mushaf-block notranslate\" translate=\"no\">'+AYAT.map((t,i)=>t+' <span class=\"ayah-end\">﴿'+toArabicNum(i+1)+'﴾</span>').join(' ')+'</div>';"
    if old1 in out:
        out = out.replace(old1, new1, 1)
        changed = True

    old2 = "card.innerHTML='<span class=\"order-badge\">﴿'+toArabicNum(pos+1)+'﴾</span><span>'+AYAT[idx]+'</span>';"
    new2 = "card.setAttribute('translate','no');card.innerHTML='<span class=\"order-badge\">﴿'+toArabicNum(pos+1)+'﴾</span><span class=\"notranslate\">'+AYAT[idx]+'</span>';"
    if old2 in out:
        out = out.replace(old2, new2, 1)
        changed = True

    old3 = "btn.className='order-item';\n    btn.textContent=AYAT[idx];"
    new3 = "btn.className='order-item notranslate';\n    btn.setAttribute('translate','no');\n    btn.textContent=AYAT[idx];"
    if old3 in out:
        out = out.replace(old3, new3, 1)
        changed = True

    return out, changed

def protect_quiz_ayat_from_translation(out):
    """يحمي كل نص قرآني في محرك الاختبار العادي (سهل/متوسط/صعب) من
    الترجمة التلقائية (ودجت 🌐 اللغة). النص التعليمي (زي "اكتبي
    الآيات 1–3" في مستوى الصعب) يفضل قابل للترجمة، أما نص الآية نفسه
    (خيارات السهل، هدف المتوسط، إجابة الصعب، مقارنة wordDiff، تلميح
    المساعدة) فبيتحمى دايمًا. الدالة idempotent وbest-effort — بتتعامل
    مع نمطين معروفين من الكود (المضغوط الحديث + القديم المتباعد)."""
    changed = False

    # q-text: يُحمى في سهل/متوسط، ويُسمح بترجمته في صعب (نص تعليمي فقط)
    old = "document.getElementById('q-text').textContent=q.q;"
    if old in out:
        new = ("var __qt=document.getElementById('q-text');__qt.textContent=q.q;"
               "if(currentLevel==='hard'){__qt.classList.remove('notranslate');__qt.removeAttribute('translate');}"
               "else{__qt.classList.add('notranslate');__qt.setAttribute('translate','no');}")
        out = out.replace(old, new, 1)
        changed = True

    # review-q-text: نفس منطق q-text (نمط مضغوط + نمط قديم متباعد)
    for old in (
        "document.getElementById('review-q-text').textContent=q.q;",
        "document.getElementById('review-q-text').textContent = q.q;",
    ):
        if old in out:
            new = ("var __rqt=document.getElementById('review-q-text');__rqt.textContent=q.q;"
                   "if(currentLevel==='hard'){__rqt.classList.remove('notranslate');__rqt.removeAttribute('translate');}"
                   "else{__rqt.classList.add('notranslate');__rqt.setAttribute('translate','no');}")
            out = out.replace(old, new, 1)
            changed = True
            break

    # review-answer: دايمًا نص قرآني (إجابة صحيحة) — حماية دائمة
    for old in (
        "document.getElementById('review-answer').textContent='✓ '+answerText;",
        "document.getElementById('review-answer').textContent = '✓ ' + answerText;",
    ):
        if old in out:
            new = ("var __ra=document.getElementById('review-answer');__ra.textContent='✓ '+answerText;"
                   "__ra.classList.add('notranslate');__ra.setAttribute('translate','no');")
            out = out.replace(old, new, 1)
            changed = True
            break

    # أزرار اختيار من متعدد (سهل) — كلمات/عبارات قرآنية دائمًا
    old = "btn.className='choice-btn';btn.textContent=opt.text;"
    new = old + "btn.classList.add('notranslate');btn.setAttribute('translate','no');"
    if old in out and new not in out:
        out = out.replace(old, new, 1)
        changed = True

    # checkMCQ — عرض الإجابة الصحيحة بعد اختيار خاطئ (سهل)
    old = "fb.textContent=`✗ الإجابة الصحيحة: ${questions[qIndex].choices[correct]}`;"
    if old in out:
        new = "fb.innerHTML='✗ الإجابة الصحيحة: <span class=\"notranslate\" translate=\"no\">'+questions[qIndex].choices[correct]+'</span>';"
        out = out.replace(old, new, 1)
        changed = True

    # skipQuestion — تخطي في مستوى سهل (يعرض الاختيار الصحيح)
    old = "fb.innerHTML=`⬅ الإجابة الصحيحة: ${q.choices[q.answer]}`;"
    if old in out:
        new = "fb.innerHTML='⬅ الإجابة الصحيحة: <span class=\"notranslate\" translate=\"no\">'+q.choices[q.answer]+'</span>';"
        out = out.replace(old, new, 1)
        changed = True

    # skipQuestion (متوسط/صعب) + checkText (صعب) — span مشترك بينهم
    old = '<span style="font-size:18px;line-height:2">${q.answer}</span>'
    if old in out:
        new = '<span style="font-size:18px;line-height:2" class="notranslate" translate="no">${q.answer}</span>'
        out = out.replace(old, new)
        changed = True

    # زر المساعدة (💡 أول 3 كلمات) في مستوى الصعب
    old = "hBox.textContent=q.answer.split(' ').slice(0,3).join(' ')+' ...';"
    new = old + "hBox.classList.add('notranslate');hBox.setAttribute('translate','no');"
    if old in out and new not in out:
        out = out.replace(old, new, 1)
        changed = True

    # wordDiff — نمط حديث (aligned/x.ref بـ template literals)
    old = 'background:#c3e6cb;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;font-weight:bold;">${x.ref}</span>'
    if old in out:
        new = 'background:#c3e6cb;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;font-weight:bold;" translate="no" class="notranslate">${x.ref}</span>'
        out = out.replace(old, new, 1)
        changed = True
    old = 'background:#c0392b;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;">${x.ref}</span>'
    if old in out:
        new = 'background:#c0392b;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;" translate="no" class="notranslate">${x.ref}</span>'
        out = out.replace(old, new, 1)
        changed = True

    # wordDiff — نمط قديم (word بتجميع نصوص +word+)
    old = "background:#c3e6cb;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;font-weight:bold;\">'+word+'</span>'"
    if old in out:
        new = "background:#c3e6cb;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;font-weight:bold;\" translate=\"no\" class=\"notranslate\">'+word+'</span>'"
        out = out.replace(old, new, 1)
        changed = True
    old = "background:#c0392b;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;\">'+word+'</span>'"
    if old in out:
        new = "background:#c0392b;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;\" translate=\"no\" class=\"notranslate\">'+word+'</span>'"
        out = out.replace(old, new, 1)
        changed = True

    return out, changed

# ===== نظام تتبع التقدم الدائم عبر الصفحات (يوليو ٢٠٢٦) =====
def add_progress_tracking(out):
    """
    نظام تتبع تقدم دائم منفصل تمامًا عن RESUME_KEY (اللي بيتمسح فور
    انتهاء الاختبار ووظيفته بس "استكمل من حيث وقفتِ" داخل نفس الاختبار).

    هنا بنسجّل في مفتاح localStorage دائم واحد 'darbi_progress' (JSON):
      { "<page_key>": {
          easy:{done,score}, medium:{...}, hard:{...}, order:{...},
          lastVisited: "<ISO date>"
      }, ... }
    - "done" = وصل المستخدم لنسبة 70% فأكثر في المستوى ده.
    - "score" = أفضل نتيجة وصلها المستخدم في المستوى ده (نحتفظ بالأعلى
      لو حاول تاني وحسّن، مش بنستبدلها بنتيجة أقل).
    - page_key بيتاستخرج من RESUME_KEY نفسه (quranResume_XXX -> XXX)
      فمفيش داعي نحقن اسم الصفحة يدويًا لكل ملف.
    """
    changed = False

    # 1. حقن دالة الحفظ نفسها مرة واحدة فقط، بعد سطر RESUME_KEY مباشرة
    if 'function saveDarbiProgress' not in out:
        m = re.search(r"const RESUME_KEY=[^;]+;", out)
        if m:
            fn = (
                "function saveDarbiProgress(level,correct,total){"
                "try{"
                "var pk='darbi_progress';"
                "var all=JSON.parse(localStorage.getItem(pk)||'{}');"
                "var key=RESUME_KEY.replace('quranResume_','');"
                "var pct=total>0?Math.round((correct/total)*100):0;"
                "if(!all[key])all[key]={};"
                "var prev=(all[key][level]&&all[key][level].score)||0;"
                "all[key][level]={done:pct>=70,score:Math.max(pct,prev)};"
                "all[key].lastVisited=new Date().toISOString();"
                "localStorage.setItem(pk,JSON.stringify(all));"
                "}catch(e){}"
                "}\n"
            )
            insert_pos = m.end()
            out = out[:insert_pos] + "\n" + fn + out[insert_pos:]
            changed = True

    # 2. استدعاء الحفظ في نهاية showResult() (سهل/متوسط/صعب) — قبل ما
    #    RESUME_KEY المؤقت يتمسح، وبرضو قبل ما currentLevel يتصفّر
    SHOWRESULT_OLD = "try{localStorage.removeItem(RESUME_KEY);}catch(e){}const rb="
    SHOWRESULT_NEW = (
        "saveDarbiProgress(currentLevel,correctCount,questions.length);"
        "try{localStorage.removeItem(RESUME_KEY);}catch(e){}const rb="
    )
    if SHOWRESULT_OLD in out and 'saveDarbiProgress(currentLevel' not in out:
        out = out.replace(SHOWRESULT_OLD, SHOWRESULT_NEW, 1)
        changed = True

    # 3. استدعاء الحفظ في نهاية checkOrderAnswer() — مستوى "ترتيب" له
    #    منطق تصحيح منفصل بالكامل عن باقي المستويات (بيتحقق فورًا مش
    #    عبر showResult). بيشتغل مع النسختين: الممتدة بأسطر (add_ordering_
    #    feature) والمصغّرة سطر واحد (BAQARA_CLEAN_TEMPLATE)
    ORDER_RE = re.compile(
        r"(document\.getElementById\('order-check-btn'\)\.style\.display='none';)"
        r"(\s*)"
        r"(if\(allCorrect\)spawnConfetti\(\);)"
    )
    if "saveDarbiProgress('order'" not in out:
        new_out, n = ORDER_RE.subn(
            r"\1\2saveDarbiProgress('order',correct,AYAT.length);\2\3",
            out
        )
        if n:
            out = new_out
            changed = True

    return out, changed


def fix_missing_progress_save_calls(out):
    """إصلاح باج حقيقي في الملفات القديمة (نمط قبل التحديثات الحديثة):
    بعد الإجابة في مستوى سهل (checkMCQ) أو متوسط/كتابة الصعب (checkText)،
    الملفات دي ماكانتش بتستدعي renderDotProgress() و saveResumeState() —
    يعني نقط التقدم ما بتتحدثش فورًا، وأهم من كده: تقدم المستخدم مش بيتحفظ
    لو قفل الصفحة قبل ما يضغط 'التالي'. إضافة سطر واحد بس، من غير أي
    تغيير في البنية أو الترتيب أو أي منطق تاني — نفس الاستدعاء المستخدم
    بالفعل في كل مكان تاني بالملف."""
    old = ("fb.style.display='block';updateBadges();"
           "document.getElementById('next-btn').style.display='block';"
           "document.getElementById('skip-btn').style.display='none';}")
    if old not in out:
        return out, False
    new = ("fb.style.display='block';updateBadges();"
           "document.getElementById('next-btn').style.display='block';"
           "document.getElementById('skip-btn').style.display='none';"
           "renderDotProgress();saveResumeState();}")
    out = out.replace(old, new)
    return out, True

def fix_single_submit_btn_selector(out):
    """إصلاح باج قديم فعلي: بعض الملفات (خصوصًا صفحات البقرة القديمة زي
    p8) لسه فيها document.querySelector('.submit-btn') بصيغة المفرد بدل
    querySelectorAll. في مستوى الصعب فيه زرارين .submit-btn (واحد لوضع
    الكتابة وواحد لوضع الصوت)، فـquerySelector المفرد بيعطّل واحد بس
    ويسيب التاني شغال وقت التحقق — ممكن يسمح بإرسال إجابة مرتين أو
    يلخبط الحالة. الإصلاح آمن وidempotent: بيستهدف السطر بالظبط جوه
    checkText() وskipQuestion() من غير ما يلمس أي منطق تاني."""
    changed = False

    # 1. جوه checkText(): "document.querySelector('.submit-btn').disabled = true;"
    pattern1 = re.compile(r"document\.querySelector\(\s*['\"]\.submit-btn['\"]\s*\)\.disabled\s*=\s*true\s*;")
    if pattern1.search(out):
        out = pattern1.sub("document.querySelectorAll('.submit-btn').forEach(b => b.disabled = true);", out)
        changed = True

    # 2. جوه skipQuestion(): "const sub=document.querySelector('.submit-btn'); if(sub) sub.disabled=true;"
    pattern2 = re.compile(
        r"const\s+sub\s*=\s*document\.querySelector\(\s*['\"]\.submit-btn['\"]\s*\)\s*;\s*"
        r"if\s*\(\s*sub\s*\)\s*sub\.disabled\s*=\s*true\s*;"
    )
    if pattern2.search(out):
        out = pattern2.sub("document.querySelectorAll('.submit-btn').forEach(b=>b.disabled=true);", out)
        changed = True

    return out, changed

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
    ".order-filled-grid{display:flex;flex-direction:column;gap:10px;margin-bottom:10px;}"
    ".order-slot{display:flex;gap:8px;align-items:center;border-radius:12px;padding:12px 14px;font-size:16px;line-height:1.7;cursor:pointer;}"
    ".order-slot.filled{background:var(--surface3);border:2px solid var(--accent);box-shadow:0 1px 4px rgba(0,0,0,.07);}"
    ".order-slot.correct-slot{background:var(--correct-bg) !important;border-color:var(--accent) !important;color:var(--correct-text) !important;}"
    ".order-slot.wrong-slot{background:var(--wrong-bg) !important;border-color:var(--wrong-border) !important;color:var(--wrong-text) !important;}"
    ".order-empty-strip{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px;}"
    ".order-dot{display:flex;align-items:center;justify-content:center;min-width:34px;height:32px;padding:0 3px;flex-shrink:0;border-radius:50%;background:var(--surface2);border:1.5px dashed var(--border);color:var(--hint-btn-text);font-size:15px;font-family:'Amiri','Scheherazade New',serif;cursor:pointer;transition:all .15s;}"
    ".order-dot:hover{border-color:var(--accent);}"
    ".order-dot.active{border-style:solid;border-color:var(--accent);background:var(--hint-bg);color:var(--accent-dark);font-weight:700;box-shadow:0 0 0 3px var(--surface-hover);}"
    ".order-badge{color:var(--hint-btn-text);font-size:16px;font-family:'Amiri','Scheherazade New',serif;flex-shrink:0;cursor:pointer;min-width:34px;min-height:34px;display:inline-flex;align-items:center;justify-content:center;padding:4px;margin:-4px;border-radius:8px;}.order-slot.order-slot-selected{border-color:var(--gold,#C4A84A) !important;box-shadow:0 0 0 2px var(--gold,#C4A84A);}"
    ".mushaf-block{background:var(--surface3);border:1.5px solid var(--border);border-radius:12px;padding:18px 16px;margin-top:12px;font-size:19px;line-height:2.4;text-align:justify;direction:rtl;color:var(--text);}"
    ".ayah-end{color:var(--gold);font-size:15px;}"
)

# نسخة قديمة من CSS الترتيب (قبل التصميم المضغوط) — لازمة للترقية التلقائية
OLD_ORDER_CSS = (
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
  <div id="order-pool" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-bottom:14px;"></div>
  <div class="nav-row">
    <button class="nav-btn" id="order-reveal-btn" onclick="revealOrderAnswer()">💡 أظهر الترتيب الصحيح</button>
    <button class="nav-btn primary" id="order-check-btn" onclick="checkOrderAnswer()" style="display:none;">تحقق ✓</button>
  </div>
  <div id="order-reveal" style="display:none;"></div>
  <div class="feedback" id="order-feedback"></div>
  <button class="level-return-btn" onclick="returnToLevels()">🔄 اختر اختباراً آخر</button>
</div>
'''

ORDER_JS = '''
/* ===== ترتيب الآيات 🔀 ===== */
let orderPlaced=[],orderCursor=0,orderPoolOrder=[],orderSelected=-1;
function startOrderQuiz(){
  orderPlaced=new Array(AYAT.length).fill(null);
  orderCursor=0;orderSelected=-1;
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
  return '<div class="mushaf-block notranslate" translate="no">'+AYAT.map((t,i)=>t+' <span class="ayah-end">﴿'+toArabicNum(i+1)+'﴾</span>').join(' ')+'</div>';
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
  const filledGrid=document.createElement('div');
  filledGrid.className='order-filled-grid';
  const emptyStrip=document.createElement('div');
  emptyStrip.className='order-empty-strip';
  orderPlaced.forEach((idx,pos)=>{
    if(idx===null){
      const active=(pos===orderCursor);
      const dot=document.createElement('span');
      dot.className='order-dot'+(active?' active':'');
      dot.textContent='﴿'+toArabicNum(pos+1)+'﴾';
      dot.title=active?'الخانة النشطة الآن':'اضغط للمتابعة من هنا';
      dot.onclick=()=>{orderCursor=pos;renderOrderQuiz();};
      emptyStrip.appendChild(dot);
    }else{
      const card=document.createElement('div');
      card.className='order-slot filled'+(pos===orderSelected?' order-slot-selected':'');
      card.setAttribute('translate','no');
      card.innerHTML='<span class="order-badge">﴿'+toArabicNum(pos+1)+'﴾</span><span class="notranslate">'+AYAT[idx]+'</span>';
      card.onclick=(e)=>{if(e.target.closest('.order-badge')){if(orderSelected===pos){orderSelected=-1;renderOrderQuiz();return;}if(orderSelected===-1){orderSelected=pos;renderOrderQuiz();return;}const tmp=orderPlaced[orderSelected];orderPlaced[orderSelected]=orderPlaced[pos];orderPlaced[pos]=tmp;orderSelected=-1;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();return;}orderPlaced[pos]=null;orderCursor=pos;orderSelected=-1;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};
      filledGrid.appendChild(card);
    }
  });
  if(filledGrid.children.length)slotsDiv.appendChild(filledGrid);
  if(emptyStrip.children.length)slotsDiv.appendChild(emptyStrip);
  orderPoolOrder.forEach(idx=>{
    if(orderPlaced.includes(idx))return;
    const btn=document.createElement('button');
    btn.className='order-item notranslate';
    btn.setAttribute('translate','no');
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
    const ok=(orderPlaced[pos]!==null&&AYAT[orderPlaced[pos]]===AYAT[pos]);
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

def remove_broken_order_for_baqara(path, out):
    """يشيل ميزة الترتيب المكسورة اللي اتضافت غلط لصفحات البقرة
    (بسبب AYAT قديمة بصيغة {num,text} مش نص بسيط)."""
    fn = os.path.splitext(os.path.basename(path))[0]
    if not fn.startswith('albaqara_'):
        return out, False
    if 'order-area' not in out:
        return out, False
    if 'ORDER_AYAT' in out:
        return out, False  # التنفيذ الجديد الصحيح للبقرة — ماينفعش يتشال (يوليو ٢٠٢٦)
    changed = False

    # 1. الزر الرابع في منتقي المستوى
    new_out = re.sub(
        r"</button>\s*<button class=\"level-btn\" onclick=\"selectLevel\('order'\)\" id=\"btn-order\">.*?</button>",
        "</button>",
        out, count=1, flags=re.S
    )
    if new_out != out:
        out = new_out
        changed = True

    # 2. قسم order-area بالكامل
    new_out = re.sub(
        r'<div class="quiz-area" id="order-area">.*?</div>\s*(?=<div class="result-area")',
        '', out, count=1, flags=re.S
    )
    if new_out != out:
        out = new_out
        changed = True

    # 3. دوال JS الخاصة بالترتيب
    new_out = re.sub(
        r'/\* ===== ترتيب الآيات.*?===== نهاية ترتيب الآيات ===== \*/\s*',
        '', out, count=1, flags=re.S
    )
    if new_out != out:
        out = new_out
        changed = True

    # 4. CSS بتاع الترتيب
    new_out = re.sub(
        r'\.order-item\{.*?\.ayah-end\{color:var\(--gold\);font-size:15px;\}',
        '', out, count=1, flags=re.S
    )
    if new_out != out:
        out = new_out
        changed = True

    return out, changed


def ensure_order_wiring(path, out):
    """يتأكد إن startQuiz و selectLevel بيتعاملوا مع مستوى 'order' صح،
    حتى لو الملف مكتوب بتنسيق كود مختلف عن القالب المرجعي (زي annaziat.html)
    وده خلّى الاستبدال النصي الحرفي القديم يفشل بصمت."""
    fn = os.path.splitext(os.path.basename(path))[0]
    if fn.startswith('albaqara_'):
        return out, False
    if 'order-area' not in out:
        return out, False
    changed = False

    if "startOrderQuiz();return;}" not in out:
        m = re.search(r"function startQuiz\(\)\s*\{", out)
        if m:
            out = out[:m.end()] + "if(currentLevel==='order'){startOrderQuiz();return;}" + out[m.end():]
            changed = True

    if "textContent=toArabicNum(AYAT.length);return;}" not in out:
        m = re.search(r"function selectLevel\(lvl\)\s*\{", out)
        if m:
            patch = (
                "if(lvl==='order'){currentLevel=lvl;"
                "document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));"
                "var __ob=document.getElementById('btn-order');if(__ob)__ob.classList.add('active');"
                "document.getElementById('start-btn').classList.add('ready');"
                "document.getElementById('total-q').textContent=toArabicNum(AYAT.length);return;}"
            )
            out = out[:m.end()] + patch + out[m.end():]
            changed = True

    return out, changed



# ====================================================
# الحروف المقطعة (فواتح السور) — تُنطق أسماء حروف منفصلة
# ====================================================
# نفس الخريطة المستخدمة في recitation.html بالظبط. الحاجة ليها ظهرت مع
# albaqara_p2 (أول صفحة بقرة بتبدأ بـ"الٓمٓ"): المستخدم في الوضع الصوتي
# بينطق "الف لام ميم" فالتعرف الصوتي بيرجّع تلات كلمات، بينما نص الآية
# كلمة واحدة — فالمقارنة كانت هتفشل مهما كانت التلاوة صح.
# الوضع الكتابي مش متأثر: اللي بيكتب "الم" بتتطابق زي ما هي، والتوسيع
# بيتفعّل بس لو أول كلمة من المستخدم مش مطابقة للحروف كما هي مكتوبة.
MUQATTAAT_JS = """
/* ===== الحروف المقطعة: تُنطق أسماء حروف منفصلة ===== */
const MUQATTAAT={
  'الم':['الف','لام','ميم'],
  'المص':['الف','لام','ميم','صاد'],
  'الر':['الف','لام','را'],
  'المر':['الف','لام','ميم','را'],
  'كهيعص':['كاف','ها','يا','عين','صاد'],
  'طه':['طا','ها'],
  'طسم':['طا','سين','ميم'],
  'طس':['طا','سين'],
  'يس':['يا','سين'],
  'ص':['صاد'],
  'حم':['حا','ميم'],
  'عسق':['عين','سين','قاف'],
  'ق':['قاف'],
  'ن':['نون']
};
function collapseMuqattaat(words,correctAnswer){
  if(!words||!words.length||!correctAnswer)return words;
  const cw=correctAnswer.trim().split(/\\s+/);
  const names=MUQATTAAT[normalize(cw[0])];
  if(!names||words.length<names.length)return words;
  for(let k=0;k<names.length;k++){
    if(normalize(words[k])!==normalize(names[k]))return words;
  }
  return [cw[0]].concat(words.slice(names.length));
}
/* ===== نهاية الحروف المقطعة ===== */
"""


def add_muqattaat_support(out):
    """دعم الحروف المقطعة (فواتح السور) في المستوى الصعب.

    المستخدم بينطق "الف لام ميم" فالتعرف الصوتي بيرجّع تلات كلمات، بينما
    نص الآية كلمة واحدة "الٓمٓ". الحل: نجمّع كلمات المستخدم في صيغة المصحف
    بدل ما نفكّك نص الآية — كده المقارنة تظبط **والعرض يفضل بالرسم
    القرآني** (الٓمٓ) مش بالنطق (الف لام ميم).

    تلات نقاط تعديل، كلها جراحية:
      1. حقن الخريطة + collapseMuqattaat() قبل wordDiff
      2. wordDiff: تجميع كلمات المستخدم قبل المقارنة
      3. _fixWords + onresult: نفس التجميع وقت التقاط الصوت، عشان الكلمات
         اللي بتظهر للمستخدم أثناء التسجيل تبان بالرسم القرآني من الأول

    ولا قاعدة من قواعد normalize() اتغيّرت، ولا منطق المقارنة نفسه.
    الملفات اللي متبدأش بحروف مقطعة مبيتغيّرش سلوكها إطلاقًا."""
    if 'function wordDiff' not in out:
        return out, False

    changed = False

    # --- 1) الخريطة والدالة (مع ترقية نسخة expandMuqattaat القديمة) ---
    if 'function expandMuqattaat' in out:
        out = re.sub(r'/\* ===== الحروف المقطعة.*?\nfunction expandMuqattaat\(cWords,userVal\)\{.*?\n\}\n',
                     lambda _m: MUQATTAAT_JS.strip() + '\n', out, count=1, flags=re.S)
        changed = True
    elif 'MUQATTAAT' not in out:
        out = out.replace('function wordDiff',
                          MUQATTAAT_JS.strip() + '\nfunction wordDiff', 1)
        changed = True

    # --- 2) wordDiff: تجميع جهة المستخدم ---
    OLD_EXPAND = (r'const uWords=userVal.trim().split(/\s+/),'
                  r'cWords=expandMuqattaat(correctAnswer.split(/\s+/),userVal)')
    OLD_PLAIN  = r'const uWords=userVal.trim().split(/\s+/),cWords=correctAnswer.split(/\s+/)'
    NEW_DIFF   = (r'const uWords=collapseMuqattaat(userVal.trim().split(/\s+/),correctAnswer),'
                  r'cWords=correctAnswer.split(/\s+/)')
    for old in (OLD_EXPAND, OLD_PLAIN):
        if old in out:
            out = out.replace(old, NEW_DIFF, 1)
            changed = True
            break

    # --- 3) التقاط الصوت: التجميع وقت التسجيل عشان العرض الحي ---
    FIX_HEAD = 'function _fixWords(words){\n        const out=[];'
    # ملحوظة: الحارس لازم يكون النداء بالظبط — مجرد 'collapseMuqattaat(words'
    # موجود أصلاً في تعريف الدالة نفسها فبيدي إنذار كاذب ويتخطى الحقن
    if FIX_HEAD in out and 'words=collapseMuqattaat(words,' not in out:
        out = out.replace(FIX_HEAD,
                          'function _fixWords(words){\n        '
                          "words=collapseMuqattaat(words,"
                          "(typeof q!=='undefined'&&q&&q.answer)||'');\n"
                          '        const out=[];', 1)
        changed = True

    OLD_RES = ("_words=_words.concat(e.results[i][0].transcript.trim().split(/\\s+/));")
    NEW_RES = ("_words=_fixWords(_words.concat(e.results[i][0].transcript.trim().split(/\\s+/)));")
    if OLD_RES in out:
        out = out.replace(OLD_RES, NEW_RES, 1)
        changed = True

    return out, changed


def heal_missing_order_css(out):
    """يداوي أي ملف ميزة الترتيب فيه شغّالة (order-area + دوال JS كاملة)
    لكن كتلة CSS بتاعتها مفقودة تمامًا — فالخانات وبنك الآيات بيظهروا
    بشكل المتصفح الخام بدل التصميم (اتكشفت في albaqara_p4 يوليو ٢٠٢٦).

    السبب: الملف اترحّل لنسخة قديمة من القالب النضيف مكانش فيها الـCSS،
    وبعد كده الملف بقى مقفول في الحالة دي للأبد لأن:
      • add_ordering_feature_baqara() بتخرج فورًا (id="order-area" موجود)
      • migrate_baqara_to_clean_template() بتخرج فورًا ({ayah: موجودة)
      • upgrade_order_ui_to_compact() بتدوّر على CSS قديم مش موجود أصلًا
    فمحدش بيحقن الـCSS ومحدش بيعيد بناء الملف.

    الحقن بيتم في نهاية كتلة <style> الرئيسية (اللي فيها .quiz-area) مش
    أول كتلة، عشان مايتحطش في كتلة فرعية صغيرة زي darbi-locked."""
    if 'id="order-area"' not in out:
        return out, False              # مفيش ميزة ترتيب في الملف أصلًا
    if re.search(r'\.order-item\s*\{', out):
        return out, False              # الـCSS موجود بالفعل (idempotent)

    m = re.search(r'\.quiz-area\s*\{', out)
    close = out.find('</style>', m.end()) if m else out.rfind('</style>')
    if close == -1:
        return out, False              # مفيش كتلة style — مانلمسش حاجة

    return out[:close] + ORDER_CSS + '\n' + out[close:], True


# ====================================================
# لوحة شرح مستوى الترتيب 🔀 (أغسطس ٢٠٢٦)
# ------------------------------------------------------
# مستوى الترتيب فيه ٤ حركات مش كلها واضحة من نفسها:
#   • ضغط آية من البنك    → تتوضع في الخانة النشطة
#   • ضغط دائرة فاضية     → الخانة دي تبقى النشطة (تخطّي/رجوع)
#   • ضغط نصّ آية موضوعة  → ترجع للبنك (حذف من الترتيب)
#   • ضغط رقم آية موضوعة  → تحديد، وضغط رقم تاني → تبديل الآيتين
# اللوحة بتشرحهم بالترتيب ده، بتظهر تلقائيًا أول مرة بس (مفتاح
# localStorage واحد للموقع كله)، ومعاها زر '؟' دائم يفتحها ويقفلها.
# كل حاجة هنا نصّ واجهة بحت — مافيش أي حرف قرآني، والبصمة ما تتأثرش.
# ====================================================

# نسخة اللوحة — أي تغيير في CSS/HTML/JS لازم يزوّد الرقم ده، عشان
# add_order_help_panel() تشيل النسخة القديمة من الملفات وتحقن الجديدة
# بدل ما تفضل القديمة متعلّقة (الحقن بيتم مرة واحدة بس).
OH_VERSION = 'v5'

ORDER_HELP_CSS = (
    "/*OHCSS " + OH_VERSION + "*/"
    ".order-help{background:var(--hint-bg);border:1.5px solid var(--accent);"
    "border-radius:12px;padding:14px 14px 12px;margin-bottom:14px;text-align:right;direction:rtl;}"
    ".order-help-head{display:flex;align-items:center;gap:8px;margin-bottom:10px;}"
    ".order-help-head .t{font-weight:700;color:var(--accent-dark);font-size:16px;flex:1;}"
    ".oh-count{font-size:12.5px;color:var(--hint-btn-text);font-family:'Amiri',serif;"
    "white-space:nowrap;}"
    ".oh-dots{display:flex;gap:5px;align-items:center;}"
    ".oh-dots i{width:9px;height:9px;flex:0 0 auto;border-radius:50%;"
    "background:var(--hint-btn-text);opacity:.3;display:block;transition:all .3s;}"
    ".oh-dots i.done{background:var(--accent);opacity:.55;}"
    ".oh-dots i.on{background:var(--accent);opacity:1;transform:scale(1.45);"
    "box-shadow:0 0 0 3px var(--surface-hover);}"
    ".oh-cap{background:var(--surface2);border:1.5px solid var(--border);border-radius:10px;"
    "padding:11px 13px;margin-bottom:12px;min-height:76px;}"
    ".oh-cap .act{font-size:15.5px;font-weight:700;color:var(--accent-dark);margin-bottom:3px;}"
    ".oh-cap .why{font-size:13.5px;color:var(--hint-btn-text);line-height:1.65;}"
    ".oh-cap.in{animation:ohcap .3s ease-out;}"
    "@keyframes ohcap{from{opacity:0;transform:translateY(-4px);}to{opacity:1;transform:none;}}"
    ".oh-board{position:relative;}"
    ".order-help .order-item{font-size:16px;padding:11px 14px;cursor:default;}"
    ".order-help .order-item:hover{background:var(--surface2);border-color:var(--border);}"
    ".order-help .order-slot{font-size:15px;padding:10px 12px;cursor:default;transition:all .25s;}"
    ".order-help .order-dot{cursor:default;transition:all .25s;}"
    ".order-help .order-badge{cursor:default;}"
    ".oh-swap{border-color:var(--gold)!important;box-shadow:0 0 0 2px var(--gold);}"
    ".oh-flash{animation:ohflash 1.2s ease-out;}"
    "@keyframes ohflash{0%{box-shadow:0 0 0 0 var(--gold);}"
    "15%{box-shadow:0 0 0 4px var(--gold);}100%{box-shadow:0 0 0 0 rgba(196,168,74,0);}}"
    ".oh-tap{position:absolute;width:32px;height:32px;border-radius:50%;pointer-events:none;"
    "border:2.5px solid var(--accent);background:rgba(74,124,74,.16);z-index:5;opacity:0;"
    "transform:translate(-50%,-50%);transition:top .55s cubic-bezier(.4,0,.2,1),"
    "left .55s cubic-bezier(.4,0,.2,1),opacity .3s;}"
    ".oh-tap.on{opacity:1;}"
    ".oh-tap.press{animation:ohpress .55s ease-out;}"
    "@keyframes ohpress{0%{transform:translate(-50%,-50%) scale(1);}"
    "35%{transform:translate(-50%,-50%) scale(.5);background:rgba(74,124,74,.42);}"
    "100%{transform:translate(-50%,-50%) scale(1.6);background:rgba(74,124,74,0);}}"
    "@media (prefers-reduced-motion:reduce){.oh-tap{transition:none;}"
    ".oh-tap.press,.oh-flash,.oh-cap.in{animation:none;}}"
    ".oh-ctrls{display:flex;gap:7px;margin-top:12px;}"
    ".oh-ctrls button{flex:1;background:var(--surface2);border:1.5px solid var(--border);"
    "border-radius:10px;color:var(--accent-dark);padding:10px 8px;font-family:inherit;"
    "font-size:14px;cursor:pointer;min-height:44px;}"
    ".oh-ctrls button:hover{background:var(--surface-hover);border-color:var(--accent);}"
    ".order-help-close{margin-top:8px;width:100%;background:var(--accent);color:#fff;"
    "border:none;border-radius:10px;padding:11px;font-family:inherit;font-size:15px;"
    "cursor:pointer;min-height:44px;}"
    ".order-help-close:hover{filter:brightness(1.08);}"
    ".order-help-row{display:flex;justify-content:flex-start;margin-bottom:10px;}"
    ".order-help-btn{background:var(--surface2);border:1.5px solid var(--border);"
    "border-radius:10px;color:var(--hint-btn-text);padding:8px 14px;font-family:inherit;"
    "font-size:14px;cursor:pointer;min-height:40px;transition:all .15s;}"
    ".order-help-btn:hover{border-color:var(--accent);color:var(--accent-dark);}"
    "/*OHCSS-END*/"
)

# ملحوظة: ممنوع أرقام عربية-هندية حرفية هنا، لأن ar2en() في أول fix_file بتحوّلها
# لأرقام غربية فتبان غلط وسط واجهة عربية. أرقام الخانات وعدّاد الخطوات بيتولّدوا
# وقت التشغيل من toArabicNum().
ORDER_HELP_HTML = ('<!--OHHTML ' + OH_VERSION + '''-->
  <div class="order-help-row"><button type="button" class="order-help-btn" id="order-help-btn" onclick="toggleOrderHelp()" aria-controls="order-help" aria-expanded="false">؟ كيف يعمل الترتيب</button></div>
  <div class="order-help" id="order-help" role="note" style="display:none;">
    <div class="order-help-head">
      <span class="t">طريقة الترتيب</span>
      <span class="oh-count" id="oh-count"></span>
      <span class="oh-dots" id="oh-dots" aria-hidden="true"></span>
    </div>
    <div class="oh-cap" id="oh-cap" aria-live="polite"><div class="act"></div><div class="why"></div></div>
    <div class="oh-board" id="oh-board">
      <div id="oh-slots"></div>
      <div id="oh-pool" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:9px;"></div>
      <div class="oh-tap" id="oh-tap"></div>
    </div>
    <div class="oh-ctrls">
      <button type="button" onclick="ohPrev()">&#8592; السابق</button>
      <button type="button" onclick="ohToggle()" id="oh-play">&#9199; إيقاف</button>
      <button type="button" onclick="ohNext()">التالي &#8594;</button>
    </div>
    <button type="button" class="order-help-close" onclick="closeOrderHelp()">ابدأ الترتيب</button>
  </div>
  <!--OHHTML-END-->
  ''')

ORDER_HELP_JS = ('''
/*OHJS ''' + OH_VERSION + '''*/
/* ===== لوحة شرح الترتيب — عرض متحرك (يظهر تلقائيًا أول مرة فقط) ===== */
/* توقيت العرض بالملّي ثانية — كل الإيقاع من السطر ده:
   read = وقفة القراية قبل أي حركة | move = حركة المؤشّر | press = الضغطة
   hold = وقفة بعد التغيير عشان العين تشوف النتيجة
   link = وقفة أقصر بين ضغطتين في نفس الخطوة (الشرح واحد فمش محتاج قراية تاني) */
const OH_MS={read:4400,move:1100,press:600,hold:3400,link:1800};
const ORDER_HELP_KEY='darbi_order_help_seen';
const OH_SEG=['الآية الأولى','الآية الثانية','الآية الثالثة'];
function ohAr(n){return typeof toArabicNum==='function'?toArabicNum(n):String(n);}
function ohNum(i){return '﴿'+ohAr(i+1)+'﴾';}
function ohEmpty(p,f){for(let i=f;i<p.length;i++)if(p[i]===null)return i;for(let i=0;i<p.length;i++)if(p[i]===null)return i;return -1;}
function ohS0(){return {placed:[null,null,null],cursor:0,selected:-1,pool:[1,0,2]};}
let ohSt=ohS0(),ohStep=0,ohTap=0,ohTimer=null,ohPlaying=false,ohFlash=null;
/* كل خطوة = شرح واحد + ضغطة أو أكتر (taps). الخطوة اللي فيها ضغطتين
   بتاخد وقفة قراية واحدة بس في أولها، والوقفة اللي بين الضغطتين أقصر. */
const OH_STEPS=[
 {act:'ضَع آية في الترتيب',
  why:'اضغط على أي آية في الأسفل، فتُوضَع في الخانة النشطة (الدائرة الخضراء).',
  taps:[
   {at:function(){return document.querySelector('#oh-pool [data-p="1"]');},
    run:function(s){s.placed[s.cursor]=1;ohFlash='s'+s.cursor;s.cursor=ohEmpty(s.placed,s.cursor+1);}}
  ]},
 {act:'اختر خانة ثم ضَع فيها',
  why:'الدوائر المتقطّعة هي الخانات الفارغة. اضغط أي واحدة لتصبح هي النشطة، ثم اضغط آية فتُوضَع فيها هي — لا في التي تليها.',
  taps:[
   {at:function(){return document.querySelector('#oh-slots [data-d="2"]');},
    run:function(s){s.cursor=2;ohFlash='d2';}},
   {at:function(){return document.querySelector('#oh-pool [data-p="0"]');},
    run:function(s){s.placed[2]=0;ohFlash='s2';s.cursor=ohEmpty(s.placed,0);}}
  ]},
 {act:'حدِّد آية للتبديل',
  why:'اضغط على رقم الآية — لا على نصّها — فيظهر حوله إطار ذهبي.',
  taps:[
   {at:function(){return document.querySelector('#oh-slots [data-s="0"] .order-badge');},
    run:function(s){s.selected=0;ohFlash='s0';}}
  ]},
 {act:'بدِّل الآيتين',
  why:'اضغط رقم آية أخرى، فتتبادلان مكانهما. واضغط الرقم نفسه لإلغاء التحديد.',
  taps:[
   {at:function(){return document.querySelector('#oh-slots [data-s="2"] .order-badge');},
    run:function(s){const t=s.placed[0];s.placed[0]=s.placed[2];s.placed[2]=t;s.selected=-1;ohFlash='s0';}}
  ]},
 {act:'اسحب آية من الترتيب',
  why:'اضغط على نصّ الآية داخل مربّعها، فتعود إلى الأسفل وتفرغ خانتها.',
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
   const t=document.createElement('span');t.textContent=OH_SEG[idx];
   c.appendChild(b);c.appendChild(t);g.appendChild(c);
  }
 });
 if(g.children.length)sl.appendChild(g);
 if(st.children.length)sl.appendChild(st);
 ohSt.pool.forEach(function(idx){
  if(ohSt.placed.indexOf(idx)>-1)return;
  const b=document.createElement('div');
  b.className='order-item'+(ohFlash==='p'+idx?' oh-flash':'');
  b.setAttribute('data-p',idx);b.textContent=OH_SEG[idx];po.appendChild(b);
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
 if(b)b.innerHTML=v?'&#9199; إيقاف':'&#9654; تشغيل';
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
      ohSay('&#10003; وهذه كل الحركات','عند امتلاء جميع الخانات يظهر زر «تحقق &#10003;» لتصحيح الترتيب.');
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
function maybeShowOrderHelp(){_orderHelpSet(!_orderHelpSeen());}
/* ===== نهاية لوحة شرح الترتيب ===== */
/*OHJS-END*/
''')

_OH_CSS_RE  = re.compile(r'/\*OHCSS [^*]*\*/.*?/\*OHCSS-END\*/', re.S)
_OH_HTML_RE = re.compile(r'\s*<!--OHHTML [^>]*-->.*?<!--OHHTML-END-->\s*', re.S)
_OH_JS_RE   = re.compile(r'/\*OHJS [^*]*\*/.*?/\*OHJS-END\*/\s*', re.S)


def add_order_help_panel(out):
    """لوحة شرح مستوى الترتيب (عرض متحرك) + زر '؟' دائم يفتحها ويقفلها.

    كل كتلة (CSS / HTML / JS) متعلّمة بنسخة بين علامتين. لو الملف فيه نسخة
    قديمة بتتشال بالكامل وتتحقن الجديدة مكانها — وده اللي بيخلي أي تعديل
    مستقبلي على اللوحة ينتشر على كل الملفات من غير شغل يدوي.
    idempotent: تشغيلة تانية بنفس النسخة مابتغيّرش أي حرف."""
    if 'id="order-area"' not in out:
        return out, False              # مفيش ميزة ترتيب في الملف أصلًا

    changed = False
    tag_css, tag_html, tag_js = ('/*OHCSS %s*/' % OH_VERSION,
                                 '<!--OHHTML %s-->' % OH_VERSION,
                                 '/*OHJS %s*/' % OH_VERSION)

    # 1. CSS — في نهاية كتلة <style> الرئيسية (نفس منطق heal_missing_order_css)
    if tag_css not in out:
        out, n = _OH_CSS_RE.subn('', out)          # شيل النسخة القديمة لو موجودة
        if n:
            changed = True
        m = re.search(r'\.quiz-area\s*\{', out)
        close = out.find('</style>', m.end()) if m else out.rfind('</style>')
        if close != -1:
            out = out[:close] + ORDER_HELP_CSS + '\n' + out[close:]
            changed = True

    # 2. HTML — قبل خانات الترتيب مباشرة، جوّه order-area
    if tag_html not in out and '<div id="order-slots"' in out:
        out, n = _OH_HTML_RE.subn('\n  ', out)
        if n:
            changed = True
        out = out.replace('<div id="order-slots"',
                          ORDER_HELP_HTML + '<div id="order-slots"', 1)
        changed = True

    # 3. دوال JS — قبل تعريف startOrderQuiz
    if tag_js not in out and 'function startOrderQuiz(' in out:
        out, n = _OH_JS_RE.subn('', out)
        if n:
            changed = True
        out = out.replace('function startOrderQuiz(',
                          ORDER_HELP_JS + 'function startOrderQuiz(', 1)
        changed = True

    # 4. نداء العرض التلقائي جوّه startOrderQuiz — قبل أول رسم مباشرةً.
    #    الـregex متسامح مع فرق المسافات عشان يشتغل على القالب المسطّر
    #    (جزء عمّ) والقالب المضغوط في سطر واحد (البقرة) سوا.
    if not re.search(r"rb\.style\.opacity='1';\s*maybeShowOrderHelp\(\);", out):
        new_out, n = re.subn(
            r"(rb\.disabled=false;rb\.style\.opacity='1';\s*)(renderOrderQuiz\(\);)",
            lambda mm: mm.group(1) + 'maybeShowOrderHelp();' + mm.group(2),
            out, count=1)
        if n:
            out = new_out
            changed = True

    return out, changed



# ====================================================
# سلسلة ترتيب المصحف لزر "التالي ⏭️" — من البقرة p2 لحد الناس
# ====================================================
NEXT_SEQUENCE = (
    ['alfatiha'] +
    [f'albaqara_p{i}' for i in range(2, 50)] +
    [
        'annaba', 'annaziat', 'abasa', 'attakwir', 'alinfitar',
        'almutaffifin', 'alinshiqaq', 'alburuj', 'altariq', 'alaala',
        'alghasiya', 'alfajr', 'albalad', 'alshams', 'allayl', 'alduha',
        'alsharh', 'atteen', 'alalaq', 'alqadr', 'albayyina', 'alzalzala',
        'alaadiyat', 'alqaria', 'altakathur', 'alasr', 'alhumaza', 'alfiyl',
        'aquraysh', 'almaoon', 'alkawthur', 'alkafirun', 'alnnasr',
        'almasad', 'alikhlas', 'alfalaq', 'alnnas',
    ]
)
NEXT_MAP = {NEXT_SEQUENCE[i]: NEXT_SEQUENCE[i + 1] for i in range(len(NEXT_SEQUENCE) - 1)}
PREV_MAP = {NEXT_SEQUENCE[i]: NEXT_SEQUENCE[i - 1] for i in range(1, len(NEXT_SEQUENCE))}
NEXT_BTN_RE = re.compile(r'(<button class="start-btn"[^>]*>[^<]*</button>)')
LEVEL_RETURN_BTN_RE = re.compile(r'<button class="level-return-btn"[^>]*>[^<]*</button>')


PAGE_NAV_A_RE = re.compile(
    r'\s*<a href="[^"]*" (?:class|id)="(?:next|prev)-page-btn"[^>]*>[^<]*</a>'
)


def _page_nav_anchor_is_wrapped(out, start_idx):
    """بيتأكد إن الـ<a> عند الموضع ده جوه <div class="page-nav-row">...</div>
    سليم بالفعل (أول أو تاني زرار جواه) مش يتيم واقف لوحده من نسخة
    قديمة مكدّسة بعرض كامل. بيدوّر لآخر فتحة page-nav-row قبل الموضع
    ده ويتأكد إنها لسه مقفولاش قبل ما توصله."""
    div_open = out.rfind('<div class="page-nav-row"', 0, start_idx)
    if div_open == -1:
        return False
    # لازم مفيش </div> بين فتحة الصف دي والموضع الحالي (يعني لسه مقفولة)
    return '</div>' not in out[div_open:start_idx]


def add_page_nav_row(path, out):
    """يضيف صف واحد مضغوط فيه زرين جنب بعض: ⏮️ السابق و⏭️ التالي —
    بيتحط في شاشة اختيار المستوى وجنب كل زر 'اختر مستوى آخر' (الاختبار
    العادي وشاشة الترتيب). لو الملف فيه نسخة قديمة من الأزرار دي (شكل
    مكدّس بعرض كامل، أزرار يتيمة مش ملفوفة جوه page-nav-row)، الدالة
    بتشيلها وتستبدلها بالصف المضغوط الجديد. كل نقطة حقن (بعد 'ابدأ
    الاختبار' وبعد كل 'اختر مستوى آخر') بتتفحص لوحدها بدل فحص عام واحد
    للملف كله — عشان لو صفحة كان عندها بالفعل page-nav-row قبل ما ميزة
    الترتيب تتضاف لها، وبعدين اتضافت الميزة وجابت زر 'اختر مستوى آخر'
    جديد جوه order-area، الزر ده ياخد صف التنقل بتاعه هو كمان مش يتسيب
    فاضي. الأزرار السليمة الملفوفة بالفعل جوه page-nav-row متتلمسش خالص
    (يوليو ٢٠٢٦)."""
    fn = os.path.splitext(os.path.basename(path))[0]
    next_key = NEXT_MAP.get(fn)
    prev_key = PREV_MAP.get(fn)
    if not next_key and not prev_key:
        return out, False  # ملف مش داخل السلسلة أصلاً

    changed = False

    # تنظيف الأزرار اليتيمة بس (نسخة قديمة مكدّسة، مش ملفوفة جوه
    # page-nav-row) — الأزرار السليمة الملفوفة فعلًا متتلمسش
    matches = list(PAGE_NAV_A_RE.finditer(out))
    for mm in reversed(matches):
        if not _page_nav_anchor_is_wrapped(out, mm.start()):
            out = out[:mm.start()] + out[mm.end():]
            changed = True

    # تنظيف أي غلاف page-nav-row فاضي بقى من غير أزرار (بقايا الغلطة
    # القديمة، أو نتيجة تنظيف الأزرار اليتيمة فوق) — عشان نقدر نضيف
    # نسخة سليمة مكانه تحت من غير ما يتسيب صف فاضي ظاهر في الصفحة
    EMPTY_PAGE_NAV_RE = re.compile(r'\n?<div class="page-nav-row"[^>]*></div>')
    if EMPTY_PAGE_NAV_RE.search(out):
        out = EMPTY_PAGE_NAV_RE.sub('', out)
        changed = True

    btn_style = (
        'flex:1;text-align:center;text-decoration:none;padding:8px 4px;'
        'border-radius:10px;background:transparent;color:var(--soft,var(--text-faint,#6B8067));'
        'border:1.5px dashed var(--border);font-family:inherit;font-size:12.5px;'
    )
    inner = ''
    if prev_key:
        inner += ('<a href="' + prev_key + '.html" class="prev-page-btn" '
                   'style="' + btn_style + '">⏮️ الصفحة السابقة</a>')
    if next_key:
        inner += ('<a href="' + next_key + '.html" class="next-page-btn" '
                   'style="' + btn_style + '">الصفحة التالية ⏭️</a>')
    row_html = ('\n<div class="page-nav-row" '
                'style="display:flex;gap:8px;margin-top:10px;">' + inner + '</div>')

    # بعد زر "ابدأ الاختبار" في شاشة اختيار المستوى — فحص محلي: هل
    # فيه page-nav-row سليم (فيه أزرار) موجود فعلًا مباشرة بعد الزر ده؟
    m = NEXT_BTN_RE.search(out)
    if m and not out[m.end():m.end() + 30].lstrip().startswith('<div class="page-nav-row"'):
        out = out[:m.end()] + row_html + out[m.end():]
        changed = True

    # بعد كل زر "اختر مستوى آخر" (في شاشة الاختبار وشاشة الترتيب) —
    # نفس الفحص المحلي لكل زر لوحده، مش شرط عام على الملف كله
    return_matches = list(LEVEL_RETURN_BTN_RE.finditer(out))
    for mm in reversed(return_matches):
        if out[mm.end():mm.end() + 30].lstrip().startswith('<div class="page-nav-row"'):
            continue
        # صفحات البقرة: fix_baqara_page_nav_placement() بتنقل صف التنقل
        # لبعد صف "السابق/التالي" (عشان يظهر تحت تنقل الأسئلة مش فوقه).
        # من غير الفحص ده كنا نضيف صف جديد مكانه القديم كل تشغيلة،
        # فالدالتين يفضلوا يتخانقوا والملف يكبر ٦٩٦ بايت كل مرة
        # (اتكشفت في p19/p21/p30 — يوليو ٢٠٢٦).
        tail = out[mm.end():]
        trailer_m = BAQARA_TRAILER_RE.match(tail)
        if trailer_m and tail[trailer_m.end():].lstrip().startswith('<div class="page-nav-row"'):
            continue
        out = out[:mm.end()] + row_html + out[mm.end():]
        changed = True

    return out, changed


RESULT_HOME_LINK_RE = re.compile(
    r'<a href="[^"]*index\.html" class="home-link"[^>]*>[^<]*</a>'
)


def add_result_page_nav_row(path, out):
    """نفس صف التنقل المضغوط (⏮️ السابق / التالي ⏭️) بس في شاشة النتيجة
    النهائية جوه result-area — بعد زر "← الرئيسية" مباشرةً.

    الفكرة: بعد ما المستخدم يخلّص المستوى ويشوف نتيجته، يقدر ينتقل
    للصفحة اللي بعدها في ترتيب المصحف من غير ما يرجع للرئيسية. الروابط
    بتودّي على شاشة اختيار المستوى في الصفحة الجديدة (مش تبدأ اختبار
    تلقائي)، وده سلوك الروابط نفسه المستخدم في add_page_nav_row.

    الطرفين متحلّين أصلاً من NEXT_SEQUENCE: alfatiha → البقرة p2..p49 →
    النبأ → ... → الناس. يعني p49 «التالي» بتودّي على النبأ، وأول
    الفاتحة/آخر الناس بيتعرض فيها زر واحد بس (اللي له وجود في السلسلة).

    مفيش أي تعارض مع الدوال التانية:
      · add_page_nav_row: بتحقن بعد level-return-btn — شاشة النتيجة
        بتستخدم retry-btn، فمش هتتلمس.
      · fix_baqara_page_nav_placement: بتشترط إن اللي قبل الصف يكون
        </button>؛ اللي قبل صفنا </a> بتاع home-link → بتعديه.
      · fix_baqara_page_nav_visibility_js / fix_question_nav_...: بتشتغل
        على id="quiz-page-nav" بس، وصفنا id="result-page-nav".
      · تنظيف الأزرار اليتيمة: أزراره ملفوفة جوه page-nav-row → آمنة.
    (أغسطس ٢٠٢٦)"""
    fn = os.path.splitext(os.path.basename(path))[0]
    next_key = NEXT_MAP.get(fn)
    prev_key = PREV_MAP.get(fn)
    if not next_key and not prev_key:
        return out, False  # ملف مش داخل السلسلة أصلاً
    if 'id="result-page-nav"' in out:
        return out, False  # موجود بالفعل — idempotent
    if '<div class="result-area"' not in out:
        return out, False

    m = RESULT_HOME_LINK_RE.search(out)
    if not m:
        return out, False
    # نتأكد إن الرابط ده هو بتاع شاشة النتيجة فعلاً (بعد زر إعادة
    # الاختبار جوه result-area) مش أي رابط رئيسية تاني في الصفحة
    ra = out.rfind('<div class="result-area"', 0, m.start())
    if ra == -1 or 'retry-btn' not in out[ra:m.start()]:
        return out, False

    btn_style = (
        'flex:1;text-align:center;text-decoration:none;padding:8px 4px;'
        'border-radius:10px;background:transparent;color:var(--soft,var(--text-faint,#6B8067));'
        'border:1.5px dashed var(--border);font-family:inherit;font-size:12.5px;'
    )
    inner = ''
    if prev_key:
        inner += ('<a href="' + prev_key + '.html" class="prev-page-btn" '
                   'style="' + btn_style + '">⏮️ الصفحة السابقة</a>')
    if next_key:
        inner += ('<a href="' + next_key + '.html" class="next-page-btn" '
                   'style="' + btn_style + '">الصفحة التالية ⏭️</a>')
    row_html = ('\n  <div class="page-nav-row" id="result-page-nav" '
                'style="display:flex;gap:8px;margin-top:14px;">' + inner + '</div>')

    return out[:m.end()] + row_html + out[m.end():], True


def fix_missing_nav_btn_css(out):
    """يضيف كلاس .nav-btn لو مستخدم في الـHTML (زر تحقق/أظهر الترتيب)
    لكن تعريفه ناقص من الـCSS — بيخلي الزر يبان بشكل المتصفح الافتراضي
    (أبيض بحدود رفيعة) بدل تصميم الموقع (زي alfatiha_p1.html)."""
    if 'class="nav-btn' not in out:
        return out, False
    if '.nav-btn{' in out or '.nav-btn {' in out:
        return out, False
    if '</style>' not in out:
        return out, False
    css = (
        ".nav-btn{flex:1;background:var(--surface2);color:var(--accent);"
        "border:1.5px solid var(--border);border-radius:12px;padding:13px;"
        "font-size:17px;font-family:inherit;cursor:pointer;}"
        ".nav-btn:hover:not(:disabled){background:var(--surface-hover);}"
        ".nav-btn:disabled{opacity:0.4;cursor:default;}"
        ".nav-btn.primary{background:var(--accent);color:var(--card);border-color:var(--accent);}"
        ".nav-btn.primary:hover{background:var(--accent-dark);}"
    )
    out = out.replace('</style>', css + '\n</style>', 1)
    return out, True


def fix_missing_nav_row_css(out):
    """يضيف كلاس .nav-row لو مستخدم في الـHTML (class="nav-row")
    لكن تعريفه ناقص من الـCSS — بيخلي الأزرار جواه تاخد شكل افتراضي
    مختلف عن باقي الصفحات (زي annaziat.html)."""
    if 'class="nav-row"' not in out and "class='nav-row'" not in out:
        return out, False
    if '.nav-row{' in out or '.nav-row {' in out:
        return out, False
    if '</style>' not in out:
        return out, False
    out = out.replace('</style>', '.nav-row{display:flex;gap:10px;margin-top:14px;}\n</style>', 1)
    return out, True


OLD_CHECK_ORDER_ANSWER_LINE = "    const ok=(orderPlaced[pos]===pos);"
NEW_CHECK_ORDER_ANSWER_LINE = "    const ok=(orderPlaced[pos]!==null&&AYAT[orderPlaced[pos]]===AYAT[pos]);"


def upgrade_order_answer_check(out):
    """يرقّي منطق التحقق من الترتيب: المقارنة تبقى بنص الآية مش برقمها،
    عشان الآيات المتطابقة نصيًا (زي آية 3 و5 في الكافرون) تتقبل في أي
    ترتيب بينهم بدل ما تتحسب خطأ."""
    if OLD_CHECK_ORDER_ANSWER_LINE in out:
        out = out.replace(OLD_CHECK_ORDER_ANSWER_LINE, NEW_CHECK_ORDER_ANSWER_LINE, 1)
        return out, True
    return out, False


OLD_ORDER_BADGE_CSS = ".order-badge{color:var(--hint-btn-text);font-size:16px;font-family:'Amiri','Scheherazade New',serif;flex-shrink:0;cursor:pointer;}"
NEW_ORDER_BADGE_CSS = ".order-badge{color:var(--hint-btn-text);font-size:16px;font-family:'Amiri','Scheherazade New',serif;flex-shrink:0;cursor:pointer;min-width:34px;min-height:34px;display:inline-flex;align-items:center;justify-content:center;padding:4px;margin:-4px;border-radius:8px;}"

OLD_ORDER_FILLED_GRID_CSS = ".order-filled-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin-bottom:10px;}.order-slot{display:flex;gap:8px;align-items:center;border-radius:10px;padding:10px 12px;font-size:16px;line-height:1.7;cursor:pointer;}.order-slot.filled{background:var(--surface3);border:1.5px solid var(--accent);}"
NEW_ORDER_FILLED_GRID_CSS = ".order-filled-grid{display:flex;flex-direction:column;gap:10px;margin-bottom:10px;}.order-slot{display:flex;gap:8px;align-items:center;border-radius:12px;padding:12px 14px;font-size:16px;line-height:1.7;cursor:pointer;}.order-slot.filled{background:var(--surface3);border:2px solid var(--accent);box-shadow:0 1px 4px rgba(0,0,0,.07);}"

def upgrade_order_filled_grid_contrast(out):
    """المربعات 'المتوضّعة' في اختبار الترتيب كانت بترسم في شبكة عمودين
    بحدود رفيعة جدًا (1px) قريبة من لون الخلفية — مع آيات البقرة
    الطويلة اللي بتلف على أسطر كتير، الحدود الرفيعة دي بتضيع بصريًا
    وسط زحمة النص ويبان الكل كأنه فقرة واحدة متصلة (اتأكد بالتشغيل
    الفعلي جوه متصلح، مش تحليل كود بس — يوليو ٢٠٢٦). الحل: عمود واحد
    full-width بحدود أوضح (2px) وظل خفيف، زي مربعات الـpool بالظبط."""
    if OLD_ORDER_FILLED_GRID_CSS in out:
        out = out.replace(OLD_ORDER_FILLED_GRID_CSS, NEW_ORDER_FILLED_GRID_CSS)
        return out, True
    return out, False


def upgrade_order_badge_tap_target(out):
    """يكبّر مساحة اللمس لبادچ رقم الآية ﴿١﴾ في مربعات الترتيب (السويب).
    قبل كده حجم البادچ كان بيتحدد بحجم النص جواه بس (من غير min-width/
    min-height)، فرقم زي '١' مساحته أصغر بكتير من رقم زي '٨'، وأي لمسة
    خارج الدائرة الصغيرة دي بتتسجل كضغطة على النص اللي بتمسح المربع
    بدل التبديل — ده اللي حاسة بيه هند إنه 'بيشتغل أحيانًا ومش بيشتغل
    أحيانًا' حسب رقم الآية اللي بتضغط عليه (يوليو ٢٠٢٦)."""
    if OLD_ORDER_BADGE_CSS in out:
        out = out.replace(OLD_ORDER_BADGE_CSS, NEW_ORDER_BADGE_CSS)
        return out, True
    return out, False


def upgrade_order_ui_to_compact(out):
    """يرقّي أي ملف اتطبقت عليه ميزة الترتيب قبل التصميم المضغوط
    (annaba/annaziat/abasa/alburuj وغيرهم) للتصميم الجديد —
    دوائر مضغوطة للخانات الفاضية + شبكة للخانات المليانة."""
    changed = False
    if OLD_ORDER_CSS in out and '.order-filled-grid' not in out:
        out = out.replace(OLD_ORDER_CSS, ORDER_CSS, 1)
        changed = True
    if OLD_RENDER_ORDER_QUIZ in out:
        out = out.replace(OLD_RENDER_ORDER_QUIZ, NEW_RENDER_ORDER_QUIZ, 1)
        changed = True
    return out, changed


OLD_ORDER_POOL_STYLE = 'id="order-pool" style="display:flex;flex-direction:column;gap:10px;margin-bottom:14px;"'
NEW_ORDER_POOL_STYLE = 'id="order-pool" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-bottom:14px;"'


def upgrade_order_pool_layout(out):
    """يرقّي حاوية بنك آيات الترتيب (order-pool) من عمود واحد (flex-column)
    لشبكة (grid) — عشان الآيات القصيرة تقعد جنب بعض بدل سطر منفرد لكل
    آية، وده بيقلل طول السكرول في السور القصيرة. الآيات الطويلة هتاخد
    عرض أكبر تلقائيًا حسب مساحة الشبكة (auto-fill/minmax) من غير ما
    نلمس order-filled-grid أو أي جزء تاني."""
    if OLD_ORDER_POOL_STYLE in out:
        out = out.replace(OLD_ORDER_POOL_STYLE, NEW_ORDER_POOL_STYLE)
        return out, True
    return out, False


OLD_ORDER_SWAP_DECL = "let orderPlaced=[],orderCursor=0,orderPoolOrder=[];"
NEW_ORDER_SWAP_DECL = "let orderPlaced=[],orderCursor=0,orderPoolOrder=[],orderSelected=-1;"
OLD_ORDER_SWAP_RESET = "orderCursor=0;"
NEW_ORDER_SWAP_RESET = "orderCursor=0;orderSelected=-1;"
OLD_ORDER_SWAP_CLASS = "card.className='order-slot filled';"
NEW_ORDER_SWAP_CLASS = "card.className='order-slot filled'+(pos===orderSelected?' order-slot-selected':'');"
OLD_ORDER_SWAP_CLICK = "card.onclick=()=>{orderPlaced[pos]=null;orderCursor=pos;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};"
NEW_ORDER_SWAP_CLICK = (
    "card.onclick=(e)=>{if(e.target.closest('.order-badge')){"
    "if(orderSelected===pos){orderSelected=-1;renderOrderQuiz();return;}"
    "if(orderSelected===-1){orderSelected=pos;renderOrderQuiz();return;}"
    "const tmp=orderPlaced[orderSelected];orderPlaced[orderSelected]=orderPlaced[pos];orderPlaced[pos]=tmp;orderSelected=-1;"
    "document.getElementById('order-feedback').style.display='none';renderOrderQuiz();return;}"
    "orderPlaced[pos]=null;orderCursor=pos;orderSelected=-1;"
    "document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};"
)
ORDER_SWAP_CSS_RULE = ".order-slot.order-slot-selected{border-color:var(--gold,#C4A84A) !important;box-shadow:0 0 0 2px var(--gold,#C4A84A);}"


def upgrade_order_tap_swap(out):
    """يضيف خاصية "تبديل بالضغط 🔀" لمربعات الترتيب (يوليو ٢٠٢٦): الضغط على
    رقم الآية (البادج ﴿١﴾) في مربع مليان يحدده (تظليل ذهبي)، والضغط على
    بادج مربع مليان تاني يبدل مكان الآيتين فورًا — يحل مشكلة "آية اتحطت
    غلط ونفس ترجع تعدلها من غير ما تفرّغ الخانة وتضيع مكانها في البنك".
    الضغط على باقي المربع (مش البادج) يفضل زي ما هو تمامًا: يفرّغ الخانة
    ويرجّع الآية للبنك — الآلية القديمة متلمستش خالص، الجديدة إضافة بس."""
    if 'orderSelected' in out:
        return out, False  # الميزة مضافة بالفعل (idempotent)
    if OLD_ORDER_SWAP_CLICK not in out:
        return out, False  # مفيش ميزة ترتيب أصلًا، أو تصميم قديم غير مدعوم

    changed = False
    if OLD_ORDER_SWAP_DECL in out:
        out = out.replace(OLD_ORDER_SWAP_DECL, NEW_ORDER_SWAP_DECL, 1)
        changed = True
    if OLD_ORDER_SWAP_RESET in out:
        out = out.replace(OLD_ORDER_SWAP_RESET, NEW_ORDER_SWAP_RESET, 1)
        changed = True
    if OLD_ORDER_SWAP_CLASS in out:
        out = out.replace(OLD_ORDER_SWAP_CLASS, NEW_ORDER_SWAP_CLASS, 1)
        changed = True
    if OLD_ORDER_SWAP_CLICK in out:
        out = out.replace(OLD_ORDER_SWAP_CLICK, NEW_ORDER_SWAP_CLICK, 1)
        changed = True
    if '</style>' in out and ORDER_SWAP_CSS_RULE not in out:
        out = out.replace('</style>', ORDER_SWAP_CSS_RULE + '\n</style>', 1)
        changed = True
    return out, changed


OLD_CHECKMCQ_CORRECT_BRANCH = "if(chosen===correct){btn.classList.add('correct');correctCount++;statuses[qIndex]='correct';fb.className='feedback correct';fb.textContent='✓ أحسنتِ!';}else{"
NEW_CHECKMCQ_CORRECT_BRANCH = "if(chosen===correct){btn.classList.add('correct');correctCount++;statuses[qIndex]='correct';fb.className='feedback correct';fb.textContent='✓ أحسنتِ!';const __qi=qIndex;setTimeout(()=>{if(qIndex===__qi)nextQuestion();},1100);}else{"

OLD_CHECKTEXTVAL_CORRECT_BRANCH = "if(normalize(userVal)===normalize(q.answer)){correctCount++;statuses[qIndex]='correct';fb.className='feedback correct';fb.innerHTML='✓ أحسنتِ! إجابة صحيحة تماماً 🌟';}else{"
NEW_CHECKTEXTVAL_CORRECT_BRANCH = "if(normalize(userVal)===normalize(q.answer)){correctCount++;statuses[qIndex]='correct';fb.className='feedback correct';fb.innerHTML='✓ أحسنتِ! إجابة صحيحة تماماً 🌟';if(currentLevel==='hard'){const __qi=qIndex;setTimeout(()=>{if(qIndex===__qi)nextQuestion();},1100);}}else{"

OLD_CHECKTEXTVAL_FALLBACK_CORRECT = (
    "    fb.innerHTML = '✓ أحسنت! إجابة صحيحة تماماً 🌟';\n"
    "  } else {\n"
)
NEW_CHECKTEXTVAL_FALLBACK_CORRECT = (
    "    fb.innerHTML = '✓ أحسنت! إجابة صحيحة تماماً 🌟';\n"
    "    if (currentLevel === 'hard') {\n"
    "      const __qi = qIndex;\n"
    "      setTimeout(() => { if (qIndex === __qi) nextQuestion(); }, 1100);\n"
    "    }\n"
    "  } else {\n"
)

# احتياطي بالـregex (متسامح مع المسافات/الأسطر والصيغ المختلفة) — لصفحات
# البقرة القديمة اللي بتستخدم تنسيق "موسّع" (مش مضغوط) و/أو userNorm/
# ansNorm مع normalizeHurufMuqattaa بدل normalize() مباشرة، واللي
# المطابقة الحرفية فوق بتفوّتها بصمت (يوليو ٢٠٢٦)
CHECKMCQ_SUCCESS_ANCHOR_RE = re.compile(
    r"fb\.className\s*=\s*'feedback correct';\s*fb\.textContent\s*=\s*'✓ أحسنتِ!';"
)
CHECKTEXTVAL_SUCCESS_ANCHOR_RE = re.compile(
    r"fb\.className\s*=\s*'feedback correct';\s*fb\.innerHTML\s*=\s*'✓ أحسنت[ِ]?! إجابة صحيحة تماماً 🌟';"
)


def upgrade_auto_advance_correct(out):
    """ينقل تلقائيًا للسؤال التالي لو الإجابة صحيحة في مستويي سهل وصعب
    بس (بعد تأخير بسيط ١.١ ثانية عشان المستخدم يشوف علامة الصح) —
    الإجابة الغلط تفضل يدوية زي ما هي عشان يكون فيه وقت كافي لمراجعة
    التصحيح. المستوى المتوسط متلمسش خالص، يفضل يدوي في الحالتين
    (يوليو ٢٠٢٦). الحماية من التكرار: بنتأكد إن qIndex لسه زي وقت
    الجدولة قبل ما ننفّذ — لو المستخدم ضغط "التالي" يدوي قبلها، الجدولة
    القديمة بتبقى بلا أثر تلقائيًا.

    المطابقة الحرفية (fast path) بتغطي الصيغة المضغوطة القياسية. تحتها
    احتياطي بالـregex بيغطي صفحات قديمة بتنسيق موسّع أو منطق مقارنة
    مختلف (userNorm/ansNorm) كانت المطابقة الحرفية بتفوّتها بصمت."""
    changed = False
    if OLD_CHECKMCQ_CORRECT_BRANCH in out and 'setTimeout(()=>{if(qIndex===__qi)nextQuestion();}' not in out:
        out = out.replace(OLD_CHECKMCQ_CORRECT_BRANCH, NEW_CHECKMCQ_CORRECT_BRANCH, 1)
        changed = True
    if OLD_CHECKTEXTVAL_CORRECT_BRANCH in out and "if(currentLevel==='hard'){const __qi=qIndex;" not in out:
        out = out.replace(OLD_CHECKTEXTVAL_CORRECT_BRANCH, NEW_CHECKTEXTVAL_CORRECT_BRANCH, 1)
        changed = True
    if OLD_CHECKTEXTVAL_FALLBACK_CORRECT in out and "if (currentLevel === 'hard')" not in out:
        out = out.replace(OLD_CHECKTEXTVAL_FALLBACK_CORRECT, NEW_CHECKTEXTVAL_FALLBACK_CORRECT, 1)
        changed = True

    def _inject_if_missing(m, snippet):
        tail = out[m.end():m.end() + 120]
        if 'setTimeout' in tail or 'nextQuestion' in tail:
            return m.group(0)  # متضاف بالفعل قريب من هنا — من غيره
        return m.group(0) + snippet

    m1 = CHECKMCQ_SUCCESS_ANCHOR_RE.search(out)
    if m1:
        new_out = out[:m1.start()] + _inject_if_missing(
            m1, "const __qi=qIndex;setTimeout(()=>{if(qIndex===__qi)nextQuestion();},1100);"
        ) + out[m1.end():]
        if new_out != out:
            out = new_out
            changed = True

    m2 = CHECKTEXTVAL_SUCCESS_ANCHOR_RE.search(out)
    if m2:
        new_out = out[:m2.start()] + _inject_if_missing(
            m2,
            "if(currentLevel==='hard'){const __qi=qIndex;setTimeout(()=>{if(qIndex===__qi)nextQuestion();},1100);}"
        ) + out[m2.end():]
        if new_out != out:
            out = new_out
            changed = True

    return out, changed


def add_ordering_feature(out, filename=''):
    """يضيف ميزة ترتيب الآيات 🔀 للملفات اللي فيها AYAT (جزء عم).
    كل جزء (CSS/الزر/الـHTML/دوال الـJS) بيتفحص ويتضاف لوحده —
    عشان لو ملف اتوقف نصه في نص العملية قبل كده، الباقي يكمل صح
    مش يفضل ناقص للأبد."""
    # صفحات البقرة مستثناة تمامًا — AYAT عندها بصيغة {num,text} مختلفة
    # وغير متوافقة مع كود الترتيب اللي بيفترض إن كل عنصر نص بسيط
    if filename.startswith('albaqara_'):
        return out, False
    if 'const AYAT=' not in out and 'const AYAT =' not in out:
        return out, False  # مفيش AYAT (صفحات البقرة لسه)

    changed = False

    # 1. CSS
    if '</style>' in out and '.order-slot' not in out:
        out = out.replace('</style>', ORDER_CSS + '\n</style>', 1)
        changed = True

    # 2. زر رابع في منتقي المستوى
    if 'id="btn-order"' not in out:
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

    # 4. returnToLevels — إخفاء order-area كمان لما نرجع لمنتقي المستوى
    if OLD_RETURN_LEVELS in out and "order-area').style.display='none'" not in out:
        out = out.replace(OLD_RETURN_LEVELS, NEW_RETURN_LEVELS, 1)
        changed = True

    # 5. دوال JS للترتيب — قبل shareApp (الفحص على تعريف الدالة الفعلي
    #    مش استدعائها، عشان ensure_order_wiring ممكن يضيف نداء استدعاء
    #    قبل ما نوصل هنا في تشغيلات تانية)
    if 'function shareApp(' in out and 'function startOrderQuiz(' not in out:
        out = out.replace('function shareApp(', ORDER_JS + '\nfunction shareApp(', 1)
        changed = True

    return out, changed


# ====================================================
# ميزة ترتيب الآيات 🔀 لصفحات سورة البقرة (يوليو ٢٠٢٦)
# ------------------------------------------------------
# صفحات البقرة معندهاش AYAT array بصيغة نص بسيط زي جزء عم (بعضها
# مفيهوش AYAT خالص، وواحدة بس فيها AYAT بصيغة {num,text} غير مستخدمة).
# فبدل الاعتماد عليها، بنستخرج نص كل آيات الصفحة من HARD_Q نفسها
# (اللي أصلاً موثّقة ومتحقق منها من المصحف)، بعد استبعاد أي سؤال
# جزئي (زي "بداية الآية...حتى..."). العدد المستخرج لازم يطابق عدد
# آيات الصفحة الحقيقي (من "الآيات X إلى Y") قبل أي إضافة — لو مطابقش،
# الصفحة تتخطى تمامًا (تتسجل في تقرير آخر التشغيلة) بدل ما يترفع
# ترتيب ناقص. المصفوفة الناتجة اسمها ORDER_AYAT (مش AYAT) عشان أي
# استخدام قديم/غير متوافق لـAYAT في نفس الملف ما يتلخبطش معاها.
# ====================================================

BAQARA_ORDER_JS = '''
/* ===== ترتيب الآيات 🔀 (البقرة) ===== */
let orderPlaced=[],orderCursor=0,orderPoolOrder=[],orderSelected=-1;
function startOrderQuiz(){
  orderPlaced=new Array(ORDER_AYAT.length).fill(null);
  orderCursor=0;orderSelected=-1;
  orderPoolOrder=ORDER_AYAT.map((t,idx)=>idx);
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
  return '<div class="mushaf-block">'+ORDER_AYAT.map((t,i)=>t+' <span class="ayah-end">﴿'+toArabicNum(i+1)+'﴾</span>').join(' ')+'</div>';
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
  const filledGrid=document.createElement('div');
  filledGrid.className='order-filled-grid';
  const emptyStrip=document.createElement('div');
  emptyStrip.className='order-empty-strip';
  orderPlaced.forEach((idx,pos)=>{
    if(idx===null){
      const active=(pos===orderCursor);
      const dot=document.createElement('span');
      dot.className='order-dot'+(active?' active':'');
      dot.textContent='﴿'+toArabicNum(pos+1)+'﴾';
      dot.title=active?'الخانة النشطة الآن':'اضغط للمتابعة من هنا';
      dot.onclick=()=>{orderCursor=pos;renderOrderQuiz();};
      emptyStrip.appendChild(dot);
    }else{
      const card=document.createElement('div');
      card.className='order-slot filled'+(pos===orderSelected?' order-slot-selected':'');
      card.innerHTML='<span class="order-badge">﴿'+toArabicNum(pos+1)+'﴾</span><span>'+ORDER_AYAT[idx]+'</span>';
      card.onclick=(e)=>{if(e.target.closest('.order-badge')){if(orderSelected===pos){orderSelected=-1;renderOrderQuiz();return;}if(orderSelected===-1){orderSelected=pos;renderOrderQuiz();return;}const tmp=orderPlaced[orderSelected];orderPlaced[orderSelected]=orderPlaced[pos];orderPlaced[pos]=tmp;orderSelected=-1;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();return;}orderPlaced[pos]=null;orderCursor=pos;orderSelected=-1;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};
      filledGrid.appendChild(card);
    }
  });
  if(filledGrid.children.length)slotsDiv.appendChild(filledGrid);
  if(emptyStrip.children.length)slotsDiv.appendChild(emptyStrip);
  orderPoolOrder.forEach(idx=>{
    if(orderPlaced.includes(idx))return;
    const btn=document.createElement('button');
    btn.className='order-item';
    btn.textContent=ORDER_AYAT[idx];
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
    const ok=(orderPlaced[pos]!==null&&ORDER_AYAT[orderPlaced[pos]]===ORDER_AYAT[pos]);
    if(ok)correct++;
    el.classList.remove('correct-slot','wrong-slot');
    el.classList.add(ok?'correct-slot':'wrong-slot');
  });
  const fb=document.getElementById('order-feedback');
  const allCorrect=(correct===ORDER_AYAT.length);
  fb.className='feedback '+(allCorrect?'correct':'wrong');
  fb.innerHTML='<div style="margin-bottom:8px;">'+toArabicNum(correct)+' / '+toArabicNum(ORDER_AYAT.length)+' في الترتيب الصحيح'+(allCorrect?' 🌟':'')+'</div>'+(allCorrect?'':'<div style="font-size:14px;margin-bottom:4px;">الترتيب الصحيح للمراجعة:</div>'+mushafHtml());
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
/* ===== نهاية ترتيب الآيات (البقرة) ===== */
'''

BAQARA_ORDER_SKIPPED = []  # تقرير: صفحات بقرة اتخطّت لأن HARD_Q/AYAT عندها ناقصة


# انقسامات مُتحقق منها يدويًا من صورة المصحف لأسئلة HARD_Q بتجمع آيتين
# في سؤال واحد "اكتبي الآيتين X-Y كاملتين" (تيسيرًا على الحفظ) — نص
# السؤال والإجابة في HARD_Q يفضلوا زي ما هم بالظبط من غير أي تعديل،
# والانقسام ده بيتستخدم داخليًا بس لبناء ORDER_AYAT (كل آية برقمها
# الحقيقي لوحدها). النصوص هنا حرفية منسوخة من الملف نفسه (نسخ مش
# تأليف) بعد التأكد من حدود كل آية بصورة المصحف (صفحة ٤٧، يوليو ٢٠٢٦).
VERIFIED_MULTI_AYAH_SPLITS = {
    "يَمْحَقُ ٱللَّهُ ٱلرِّبَوٰا وَيُرْبِى ٱلصَّدَقَٰتِ وَٱللَّهُ لَا يُحِبُّ كُلَّ كَفَّارٍ أَثِيمٍ إِنَّ ٱلَّذِينَ ءَامَنُوا وَعَمِلُوا ٱلصَّٰلِحَٰتِ وَأَقَامُوا ٱلصَّلَوٰةَ وَءَاتَوُا ٱلزَّكَوٰةَ لَهُمْ أَجْرُهُمْ عِندَ رَبِّهِمْ وَلَا خَوْفٌ عَلَيْهِمْ وَلَا هُمْ يَحْزَنُونَ": (
        "يَمْحَقُ ٱللَّهُ ٱلرِّبَوٰا وَيُرْبِى ٱلصَّدَقَٰتِ وَٱللَّهُ لَا يُحِبُّ كُلَّ كَفَّارٍ أَثِيمٍ",
        "إِنَّ ٱلَّذِينَ ءَامَنُوا وَعَمِلُوا ٱلصَّٰلِحَٰتِ وَأَقَامُوا ٱلصَّلَوٰةَ وَءَاتَوُا ٱلزَّكَوٰةَ لَهُمْ أَجْرُهُمْ عِندَ رَبِّهِمْ وَلَا خَوْفٌ عَلَيْهِمْ وَلَا هُمْ يَحْزَنُونَ",
    ),
    "يَٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوا ٱتَّقُوا ٱللَّهَ وَذَرُوا مَا بَقِىَ مِنَ ٱلرِّبَوٰٓا إِن كُنتُم مُّؤْمِنِينَ فَإِن لَّمْ تَفْعَلُوا فَأْذَنُوا بِحَرْبٍ مِّنَ ٱللَّهِ وَرَسُولِهِۦ وَإِن تُبْتُمْ فَلَكُمْ رُءُوسُ أَمْوَٰلِكُمْ لَا تَظْلِمُونَ وَلَا تُظْلَمُونَ": (
        "يَٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوا ٱتَّقُوا ٱللَّهَ وَذَرُوا مَا بَقِىَ مِنَ ٱلرِّبَوٰٓا إِن كُنتُم مُّؤْمِنِينَ",
        "فَإِن لَّمْ تَفْعَلُوا فَأْذَنُوا بِحَرْبٍ مِّنَ ٱللَّهِ وَرَسُولِهِۦ وَإِن تُبْتُمْ فَلَكُمْ رُءُوسُ أَمْوَٰلِكُمْ لَا تَظْلِمُونَ وَلَا تُظْلَمُونَ",
    ),
}

def extract_baqara_order_ayat(out):
    """يستخرج نصوص آيات الصفحة بالترتيب الصحيح، من AYAT (لو بصيغة object
    زي p38) أو من HARD_Q. بيتعامل مع حالتين خاصتين قبل الاستبعاد
    الافتراضي: (1) زوج 'بداية الآية N...' + 'نهاية الآية N...' المتتالي
    (نفس N) — بيتدمج في نص كامل واحد (نسخ حرفي من الملف، مش تأليف).
    (2) سؤال بيجمع آيتين في نص واحد ('اكتبي الآيتين X-Y كاملتين') —
    بيتقسم لو مطابق تمامًا لـ VERIFIED_MULTI_AYAH_SPLITS (نص متحقق منه
    يدويًا من صورة المصحف). أي حالة تانية غير متعرف عليها تتسجّل
    كسؤال جزئي وتُستبعد زي الأول. يرجّع (None, سبب) لو العدد النهائي
    ما طابقش عدد آيات الصفحة الحقيقي المكتوب في ayat-range، عشان
    مايتضافش ترتيب ناقص أبدًا. حالة تالتة خاصة: صفحة آية واحدة طويلة
    جدًا (زي آية الدَّين 282) مكتوب فيها 'الآية N' مفرد مش 'الآيات X
    إلى Y' — هنا الترتيب مش بين آيات كاملة (مفيش غير آية واحدة) لكن
    بين مقاطع الإملاء الطبيعية اللي HARD_Q أصلاً مقسّم عليها الآية
    (بداية/من/نهاية)، وهي نص منسوخ حرفيًا وموجود ومتحقق منه بالفعل."""
    m_range = re.search(r'الآيات\s*(\d+)\s*إلى\s*(\d+)', out)
    if not m_range:
        m_single = re.search(r'<div class="ayat-range">الآية\s*(\d+)', out)
        if m_single:
            m_hard_single = re.search(r'const\s+HARD_Q\s*=\s*\[(.*?)\n\];', out, re.S)
            if not m_hard_single:
                return None, 'no-HARD_Q-single'
            items_single = re.findall(
                r'\{\s*(?:ayah:\s*\d+\s*,\s*)?q:\s*"((?:[^"\\]|\\.)*)"\s*,\s*answer:\s*"((?:[^"\\]|\\.)*)"\s*\}',
                m_hard_single.group(1)
            )
            if len(items_single) < 2:
                return None, 'single-ayah-not-segmented'
            if not all(('بداية' in q or 'نهاية' in q or 'من «' in q) for q, a in items_single):
                return None, 'single-ayah-mixed-questions'
            texts_single = [a.replace('\\"', '"') for q, a in items_single]
            return texts_single, 'ok-single-ayah-segments'
        return None, 'no-range'
    start, end = int(m_range.group(1)), int(m_range.group(2))
    expected = end - start + 1

    m_ayat = re.search(r'const\s+AYAT\s*=\s*\[(.*?)\n\];', out, re.S)
    if m_ayat:
        entries = re.findall(r'\{\s*num:\s*(\d+)\s*,\s*text:\s*"((?:[^"\\]|\\.)*)"\s*\}', m_ayat.group(1))
        if entries:
            entries = [(int(n), t.replace('\\"', '"')) for n, t in entries]
            entries.sort(key=lambda x: x[0])
            texts = [t for n, t in entries]
            if len(texts) == expected:
                return texts, 'ok-AYAT'
            return None, f'AYAT-count-mismatch:{len(texts)}/{expected}'

    m_hard = re.search(r'const\s+HARD_Q\s*=\s*\[(.*?)\n\];', out, re.S)
    if not m_hard:
        return None, 'no-HARD_Q'
    body = m_hard.group(1)
    items = re.findall(
        r'\{\s*(?:ayah:\s*\d+\s*,\s*)?q:\s*"((?:[^"\\]|\\.)*)"\s*,\s*answer:\s*"((?:[^"\\]|\\.)*)"\s*\}',
        body
    )
    if not items:
        return None, 'HARD_Q-parse-fail'

    # 1) دمج أزواج بداية/نهاية المتتالية لنفس رقم الآية
    merged = []
    i, n = 0, len(items)
    while i < n:
        q, ans = items[i]
        ans = ans.replace('\\"', '"')
        m_begin = re.search(r'بداية الآية (\d+)', q)
        if m_begin and i + 1 < n:
            q2, ans2 = items[i + 1]
            m_end = re.search(r'نهاية الآية (\d+)', q2)
            if m_end and m_end.group(1) == m_begin.group(1):
                merged.append(ans + ' ' + ans2.replace('\\"', '"'))
                i += 2
                continue
        merged.append((q, ans))
        i += 1

    # 2) فلترة الأجزاء الناقصة المتبقية + تقسيم الأزواج المدمجة المتحقق منها
    texts = []
    for entry in merged:
        if isinstance(entry, str):
            texts.append(entry)
            continue
        q, ans = entry
        if 'بداية' in q or 'حتى' in q:
            continue  # جزء ناقص من غير نظيره — لسه بيتستبعد زي الأول
        if ans in VERIFIED_MULTI_AYAH_SPLITS:
            texts.extend(VERIFIED_MULTI_AYAH_SPLITS[ans])
        elif '۞' in ans or 'الآيتين' in q or 'الآيتان' in q:
            # سؤال متشابهات بيجمع مقاطع من آيتين في نص واحد (الفاصل ۞) —
            # سؤال سليم في مستواه، لكنه مش آية كاملة فمينفعش يتحط ككارت
            # في اختبار الترتيب. من غير الاستبعاد ده كان بيدخل كأنه آية
            # وياخد مكان الآية الحقيقية فتختفي تمامًا من الاختبار
            # (اتكشفت في albaqara_p5: آية ٢٩ اختفت — يوليو ٢٠٢٦).
            continue
        else:
            texts.append(ans)

    if len(texts) == expected:
        return texts, 'ok-HARD_Q'
    return None, f'HARD_Q-count-mismatch:{len(texts)}/{expected}'


def fix_broken_order_area_reference(out):
    """تنظيف بقايا محاولة قديمة فشلت لبعض صفحات البقرة (زي p38): سطر
    كان بيحاول يخفي order-area وهي أصلًا مش موجودة، وده كان بيكسر
    returnToLevels() بخطأ JS فعلي (Cannot read properties of null) لما
    المستخدم يضغط 'اختر مستوى آخر'."""
    broken = "document.getElementById('order-area').style.display='none';"
    if broken in out and 'id="order-area"' not in out:
        out = out.replace(broken, '', 1)
        return out, True
    return out, False


def add_ordering_feature_baqara(path, out):
    """يضيف ميزة ترتيب الآيات 🔀 لصفحة بقرة واحدة، بعد التحقق البرمجي
    من اكتمال نص كل آياتها. لو الاستخراج فشل (نص ناقص عن عدد آيات
    الصفحة)، الصفحة تتخطّى تمامًا ومفيش أي تعديل، وتتسجل في تقرير
    آخر التشغيلة (BAQARA_ORDER_SKIPPED) عشان تُراجع يدويًا."""
    fn = os.path.splitext(os.path.basename(path))[0]
    if not fn.startswith('albaqara_'):
        return out, False
    if 'id="order-area"' in out:
        return out, False  # مضافة بالفعل وشغالة

    changed = False

    out, fixed_broken = fix_broken_order_area_reference(out)
    if fixed_broken:
        changed = True

    texts, status = extract_baqara_order_ayat(out)
    if texts is None:
        BAQARA_ORDER_SKIPPED.append(f'{os.path.basename(path)} ({status})')
        return out, changed

    # 1. CSS (نفس تصميم جزء عم بالظبط)
    if '</style>' in out and '.order-slot' not in out:
        out = out.replace('</style>', ORDER_CSS + '\n</style>', 1)
        changed = True

    # توسيع الشبكة لتستوعب 4 أزرار (تنسيقات البقرة مش موحّدة في المسافات)
    out = re.sub(
        r'\.levels-grid\s*\{\s*display:\s*flex;\s*gap:\s*10px;\s*justify-content:\s*center;\s*margin-bottom:\s*20px;\s*\}',
        '.levels-grid{display:flex;gap:8px;justify-content:center;margin-bottom:20px;flex-wrap:wrap;}',
        out
    )
    out = re.sub(
        r'\.level-btn\s*\{\s*flex:\s*1;\s*max-width:\s*100px;\s*background:\s*var\(--surface2\);\s*border:\s*1\.5px solid var\(--border\);\s*border-radius:\s*14px;\s*padding:\s*16px 8px;',
        '.level-btn{flex:1;min-width:76px;max-width:100px;background:var(--surface2);border:1.5px solid var(--border);border-radius:14px;padding:14px 6px;',
        out
    )

    # 2. الزر الرابع في منتقي المستوى
    if 'id="btn-order"' not in out:
        new_out, n = BTN_CLOSE_PATTERN.subn(lambda m: ORDER_BTN_HTML + m.group(2), out, count=1)
        if n:
            out = new_out
            changed = True

    # 3. قسم order-area كامل — قبل result-area
    if '<div class="result-area" id="result-area">' in out:
        out = out.replace(
            '<div class="result-area" id="result-area">',
            ORDER_AREA_HTML + '<div class="result-area" id="result-area">',
            1
        )
        changed = True

    # 4. returnToLevels — إخفاء order-area كمان لما نرجع لمنتقي المستوى
    if OLD_RETURN_LEVELS in out and "order-area').style.display='none'" not in out:
        out = out.replace(OLD_RETURN_LEVELS, NEW_RETURN_LEVELS, 1)
        changed = True

    # 5. حقن ORDER_AYAT بعد HARD_Q مباشرة (اسم مختلف عن AYAT عمدًا)
    if 'const ORDER_AYAT' not in out:
        m_hard = re.search(r'const\s+HARD_Q\s*=\s*\[.*?\n\];', out, re.S)
        if m_hard:
            ayat_js = "\nconst ORDER_AYAT=[\n" + ",\n".join(
                '  "' + t.replace('\\', '\\\\').replace('"', '\\"') + '"' for t in texts
            ) + "\n];\n"
            insert_pos = m_hard.end()
            out = out[:insert_pos] + ayat_js + out[insert_pos:]
            changed = True

    # 6. دوال JS الترتيب — قبل shareApp
    if 'function shareApp(' in out and 'function startOrderQuiz(' not in out:
        out = out.replace('function shareApp(', BAQARA_ORDER_JS + '\nfunction shareApp(', 1)
        changed = True

    # 7. الربط: selectLevel و startQuiz — تنسيق كود البقرة مش موحّد
    #    (بعضها ternary وبعضها if متتالية) فمحتاجين تصحيح بناءً على موقع
    #    القوس الافتتاحي مش استبدال نص حرفي كامل زي جزء عم
    if "startOrderQuiz();return;}" not in out:
        m = re.search(r'function\s+startQuiz\(\)\s*\{', out)
        if m:
            out = out[:m.end()] + "if(currentLevel==='order'){startOrderQuiz();return;}" + out[m.end():]
            changed = True

    if "ORDER_AYAT.length);return;}" not in out:
        m = re.search(r'function\s+selectLevel\(lvl\)\s*\{', out)
        if m:
            patch = (
                "if(lvl==='order'){currentLevel=lvl;"
                "document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));"
                "var __ob=document.getElementById('btn-order');if(__ob)__ob.classList.add('active');"
                "document.getElementById('start-btn').classList.add('ready');"
                "document.getElementById('total-q').textContent=toArabicNum(ORDER_AYAT.length);return;}"
            )
            out = out[:m.end()] + patch + out[m.end():]
            changed = True

    return out, changed


# ====================================================
# ترقية التسجيل الصوتي (مستوى الصعب) إلى الشكل الموحّد:
# كل كلمة متعرَّف عليها في span منفصل قابل للنقر لحذفها فرديًا،
# بدل النص الكامل اللي كان بيتمسح مرة واحدة. (يوليو ٢٠٢٦)
# ====================================================

VOICE_CSS_ADD = (
    ".rec-transcript{background:var(--surface3);border:1.5px solid var(--border);"
    "border-radius:12px;padding:12px 14px;font-size:17px;line-height:1.9;"
    "color:var(--text);direction:rtl;text-align:right;margin-bottom:10px;"
    "display:none;min-height:60px;white-space:pre-wrap;}"
    ".rec-word{display:inline-block;margin:2px 1px;padding:2px 6px;border-radius:5px;cursor:pointer;}"
    ".rec-word:hover{opacity:0.8;text-decoration:line-through;}"
)

# يلتقط كل نسخ الشكل القديم (المسافّة زي p37 بمتغيرات savedText/currentText،
# والمضغوطة زي p43 بمتغيرات _saved/_cur) — من إنشاء recBtn وحتى إغلاق
# الـ if/else الخاص بدعم/عدم دعم المتصفح، مهما اختلفت المسافات بينهم.
OLD_VOICE_RE = re.compile(
    r"const\s+recBtn\s*=\s*document\.createElement\('button'\);.*?"
    r"recBtn\.style\.opacity\s*=\s*['\"]0\.65['\"]\s*;\s*\}",
    re.DOTALL
)

NEW_VOICE_JS = r'''const recBtn=document.createElement('button');recBtn.className='rec-btn';
      recBtn.style.cssText='width:100%;padding:14px;border-radius:12px;font-size:16px;font-family:inherit;cursor:pointer;border:2px solid var(--border);background:var(--surface2);color:var(--text);margin-bottom:8px;';
      recBtn.textContent='🎤 اضغط للتسجيل';

      const txBox=document.createElement('div');txBox.className='rec-transcript';
      txBox.title='انقري على أي كلمة لحذفها';

      const clrBtn=document.createElement('button');
      clrBtn.style.cssText='width:100%;padding:9px;border-radius:10px;font-size:14px;font-family:inherit;cursor:pointer;border:1.5px solid var(--wrong-border);background:var(--wrong-bg);color:var(--wrong-text);margin-bottom:8px;display:none;';
      clrBtn.textContent='🗑️ مسح الكل والبدء من جديد';

      const vSub=document.createElement('button');vSub.className='submit-btn';vSub.textContent='تحقق ✓';vSub.style.display='none';

      vZone.appendChild(recBtn);vZone.appendChild(txBox);vZone.appendChild(clrBtn);vZone.appendChild(vSub);

      let _rec=null,_recog=false,_words=[],_cur='';
      const _SpeechAPI=window.SpeechRecognition||window.webkitSpeechRecognition;
      const _secure=location.protocol==='https:'||location.hostname==='localhost';

      function _fixWords(words){
        const out=[];
        for(let i=0;i<words.length;i++){
          if(i<words.length-2 && normalize(words[i])==='او' && normalize(words[i+1])==='كل' && normalize(words[i+2])==='ما'){
            out.push(words[i]+words[i+1]+words[i+2]);i+=2;continue;
          }
          if(i<words.length-1 && normalize(words[i])==='او' && normalize(words[i+1])==='كلما'){
            out.push(words[i]+words[i+1]);i++;continue;
          }
          if(i<words.length-1 && normalize(words[i])==='ولا' && normalize(words[i+1])==='تجدنهم'){
            out.push('ولتجدنهم');i++;continue;
          }
          if(words[i]==='ممنع'){out.push('ممن','منع');continue;}
          if(words[i]==='بلا'){out.push('بلى');continue;}
          if(words[i]==='بن'){out.push('ابن');continue;}
          out.push(words[i]);
        }
        return out;
      }

      function renderWords(){
        if(!_words.length&&!_cur){txBox.style.display='none';clrBtn.style.display='none';vSub.style.display='none';return;}
        txBox.style.display='block';
        txBox.innerHTML='';
        _words.forEach((w,i)=>{
          const span=document.createElement('span');span.className='rec-word';
          span.style.cssText='background:var(--surface-hover);border-radius:4px;padding:2px 5px;margin:2px;cursor:pointer;';
          span.textContent=w;span.title='انقري للحذف';
          span.onclick=()=>{_words.splice(i,1);renderWords();};
          txBox.appendChild(span);
        });
        if(_cur){
          const cur=document.createElement('span');cur.style.cssText='color:var(--text-soft);font-style:italic;';
          cur.textContent=' '+_cur;txBox.appendChild(cur);
        }
        clrBtn.style.display='block';
        vSub.style.display=_words.length?'block':'none';
      }

      function _setB(s){
        recBtn.disabled=false;
        if(s==='rec'){recBtn.textContent='⏸ إيقاف التسجيل';recBtn.style.background='#e74c3c';recBtn.style.color='#fff';recBtn.style.borderColor='#e74c3c';}
        else if(s==='pause'){recBtn.textContent='▶️ استمر في التسجيل';recBtn.style.background='#e67e22';recBtn.style.color='#fff';recBtn.style.borderColor='#e67e22';}
        else{recBtn.textContent='🎤 اضغط للتسجيل';recBtn.style.background='var(--surface2)';recBtn.style.color='var(--text)';recBtn.style.borderColor='var(--border)';}
      }

      function _mkRec(){
        const r=new _SpeechAPI();r.lang='ar-SA';r.continuous=true;r.interimResults=false;
        r.onstart=()=>{_recog=true;_cur='';_setB('rec');renderWords();};
        r.onresult=e=>{
          for(let i=e.resultIndex;i<e.results.length;i++){
            if(e.results[i].isFinal){
              const newWords=e.results[i][0].transcript.trim().split(/\s+/);
              _words=_fixWords(_words.concat(newWords));_cur='';
            }
          }
          renderWords();
        };
        r.onerror=e=>{if(e.error!=='no-speech'&&e.error!=='aborted'){_recog=false;_setB(_words.length?'pause':'idle');}};
        r.onend=()=>{_recog=false;if(_cur){_words=_fixWords(_words.concat(_cur.trim().split(/\s+/)));_cur='';}renderWords();_setB(_words.length?'pause':'idle');};
        return r;
      }

      clrBtn.onclick=()=>{
        if(_recog){try{_rec.stop();}catch(e){}}
        _recog=false;_rec=null;
        _words=[];_cur='';
        txBox.innerHTML='';txBox.style.display='none';
        clrBtn.style.display='none';
        vSub.style.display='none';
        _setB('idle');
        recBtn.disabled=false;
      };

      vSub.onclick=()=>{
        const t=_words.join(' ').trim();if(!t)return;
        vSub.disabled=true;
        checkTextVal(q,t);
        setTimeout(()=>{
          recBtn.disabled=false;
          vSub.disabled=false;
        },300);
      };

      if(_SpeechAPI&&_secure){
        recBtn.onclick=()=>{
          if(_recog){_recog=false;try{_rec.stop();}catch(e){}_setB('pause');return;}
          _rec=_mkRec();
          try{_rec.start();}catch(e){_setB(_words.length?'pause':'idle');}
        };
      }else{
        recBtn.textContent=_secure?'⚠️ المتصفح لا يدعم التسجيل':'🔒 يعمل على الموقع الرسمي فقط';
        recBtn.disabled=true;recBtn.style.opacity='0.65';
      }'''

def upgrade_voice_recording(out):
    """يستبدل كود التسجيل الصوتي القديم (نص كامل يتمسح مرة واحدة)
    بالنسخة الموحّدة (كل كلمة span منفصل قابل للحذف فرديًا)."""
    changed = False
    if 'const recBtn' in out and 'renderWords' not in out:
        new_out, n = OLD_VOICE_RE.subn(lambda m: NEW_VOICE_JS, out)
        if n > 0:
            out = new_out
            changed = True
    if changed and '.rec-transcript{' not in out and '</style>' in out:
        out = out.replace('</style>', VOICE_CSS_ADD + '\n</style>', 1)
    return out, changed


def retrofit_fixwords(out):
    """يضيف دالة _fixWords (تصحيح عرض بلا/بن/ولا+تجدنهم/ممنع في اختبار الصعب
    بالتسجيل الصوتي) للملفات اللي عندها renderWords بالفعل من ترقية سابقة
    قبل ما تُكتشف هذه الإصلاحات (يوليو ٢٠٢٦ الجزء ٤)."""
    if 'renderWords' not in out or '_fixWords' in out:
        return out, False
    FIXWORDS_FN = (
        "function _fixWords(words){\n"
        "        const out=[];\n"
        "        for(let i=0;i<words.length;i++){\n"
        "          if(i<words.length-2 && normalize(words[i])==='او' && normalize(words[i+1])==='كل' && normalize(words[i+2])==='ما'){\n"
        "            out.push(words[i]+words[i+1]+words[i+2]);i+=2;continue;\n"
        "          }\n"
        "          if(i<words.length-1 && normalize(words[i])==='او' && normalize(words[i+1])==='كلما'){\n"
        "            out.push(words[i]+words[i+1]);i++;continue;\n"
        "          }\n"
        "          if(i<words.length-1 && normalize(words[i])==='ولا' && normalize(words[i+1])==='تجدنهم'){\n"
        "            out.push('ولتجدنهم');i++;continue;\n"
        "          }\n"
        "          if(words[i]==='ممنع'){out.push('ممن','منع');continue;}\n"
        "          if(words[i]==='بلا'){out.push('بلى');continue;}\n"
        "          if(words[i]==='بن'){out.push('ابن');continue;}\n"
        "          out.push(words[i]);\n"
        "        }\n"
        "        return out;\n"
        "      }\n\n"
        "      function renderWords("
    )
    if 'function renderWords(' not in out:
        return out, False
    out2 = out.replace('function renderWords(', FIXWORDS_FN, 1)
    OLD_ONRESULT = "_words=_words.concat(newWords);_cur='';"
    NEW_ONRESULT = "_words=_fixWords(_words.concat(newWords));_cur='';"
    OLD_ONEND = "if(_cur){_words=_words.concat(_cur.trim().split(/\\s+/));_cur='';}"
    NEW_ONEND = "if(_cur){_words=_fixWords(_words.concat(_cur.trim().split(/\\s+/)));_cur='';}"
    changed = False
    if OLD_ONRESULT in out2:
        out2 = out2.replace(OLD_ONRESULT, NEW_ONRESULT)
        changed = True
    if OLD_ONEND in out2:
        out2 = out2.replace(OLD_ONEND, NEW_ONEND)
        changed = True
    return (out2, True) if changed else (out, False)


# ====================================================
# إصلاح تحميل خط Google Fonts (يوليو ٢٠٢٦):
# كان محمّل بطريقة @import جوه <style> — أسلوب بطيء وغير مضمون، أي
# تقطيع بسيط في النت بيخلي المتصفح "يستسلم" ويفضل شغال بالخط الاحتياطي
# (serif عادي) بدل ما يستنى الخط الأصلي (Amiri/Scheherazade New).
# الحل: <link rel="preconnect"> + <link rel="stylesheet"> جوه <head> —
# أسرع وأثبت بكتير. الدالة شغالة على أي ملف فيه @import لخطوط Google
# بغض النظر عن العائلات المطلوبة بالظبط، وآمنة idempotent (لو الملف
# اتصلح قبل كده، مفيش @import تاني تلاقيه، فمترجعش تضيف <link> تاني).
# ====================================================
FONT_IMPORT_RE = re.compile(r"@import\s+url\((['\"])(https://fonts\.googleapis\.com/css2\?[^'\")]+)\1\)\s*;?")

def fix_font_import_to_link(out):
    changed = False
    m = FONT_IMPORT_RE.search(out)
    if not m:
        return out, changed
    font_url = m.group(2)
    out = FONT_IMPORT_RE.sub('', out, 1)
    changed = True
    if f'href="{font_url}"' not in out:
        head_links = (
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'<link rel="stylesheet" href="{font_url}">\n'
        )
        if '</head>' in out:
            out = out.replace('</head>', head_links + '</head>', 1)
        elif '<style>' in out:
            out = out.replace('<style>', head_links + '<style>', 1)
    return out, changed

# ====================================================
# إصلاح قائمة "☰ الأدوات" (يوليو ٢٠٢٦):
# 1) .tools-menu كانت right:0 — وزر الأدوات نفسه قريب من حافة الشاشة
#    اليسرى (آخر عنصر في nav-right جوه dir=rtl)، فالقائمة كانت بتمتد
#    لليسار وتخرج بره حدود الشاشة → سكرول أفقي يزيح الموقع كله جنب.
#    الحل: left:0 (تمتد جوه الصفحة بأمان) + max-width احتياطي.
# 2) لون "العربية" في القائمة كان باهت (ذهبي فاتح #B8963A) بسبب قاعدة
#    CSS بتلون أول عنصر جوه tools-lang-inline، وهو نص اللغة نفسه مش
#    السهم بس. المفروض يبقى غامق زي باقي نصوص القائمة.
# 3) حجم "العربية" كان أصغر من "اللغة" (0.75em) — كبرناه لـ1em عشان
#    يبقى نفس حجم كلمة "اللغة" جنبه.
# الدالة idempotent وشغالة على أي ملف فيه نفس الكود القديم بالظبط،
# بغض النظر لو الملف اتعالج بـadd_tools_menu قبل كده أو لأ.
# ====================================================
def fix_tools_menu_ui_bugs(out):
    changed = False
    old_menu_css = ".tools-menu{display:none;position:absolute;top:calc(100% + 8px);right:0;background:var(--card,#fff);border:1.5px solid var(--border,#E4EAE4);border-radius:14px;box-shadow:0 6px 20px rgba(0,0,0,0.18);overflow:hidden;min-width:195px;border-top:3px solid #C4A84A;z-index:9998;}"
    new_menu_css = ".tools-menu{display:none;position:absolute;top:calc(100% + 8px);left:0;max-width:min(240px,calc(100vw - 24px));background:var(--card,#fff);border:1.5px solid var(--border,#E4EAE4);border-radius:14px;box-shadow:0 6px 20px rgba(0,0,0,0.18);overflow:hidden;min-width:195px;border-top:3px solid #C4A84A;z-index:9998;}"
    if old_menu_css in out:
        out = out.replace(old_menu_css, new_menu_css)
        changed = True
    lang_span_new = ".tools-item .tools-lang-inline span:first-child{font-size:1em;color:inherit;}"
    lang_span_variants = (
        ".tools-item .tools-lang-inline span:first-child{font-size:0.75em;color:#B8963A;}",
        ".tools-item .tools-lang-inline span:first-child{font-size:0.75em;color:inherit;}",
    )
    for old_lang_span in lang_span_variants:
        if old_lang_span in out:
            out = out.replace(old_lang_span, lang_span_new)
            changed = True
            break
    return out, changed

# ====================================================
# ترتيب اللغات + علامة ✓ بدل التلوين الأخضر (يوليو ٢٠٢٦):
# 1) العربية (اللغة الأساسية) فضلت الأولى، والباقي اترتب تقريبًا حسب
#    الأكثر انتشارًا عالميًا (إنجليزي، إسباني، فرنسي، ألماني، تركي،
#    فارسي).
# 2) بدل ما اللغة الحالية تتلوّن أخضر بس (مش واضح كفاية)، بقى جنبها
#    علامة ✓ ثابتة المكان (أقصى الطرف التاني من النص دايمًا، بمساعدة
#    margin-inline-start:auto) — أوضح ومتسقة بصريًا مهما كان طول اسم
#    اللغة.
# idempotent: بيستبدل النسخة القديمة الكاملة بالجديدة لو لقاها، وميعملش
# حاجة لو الملف اتحدث بالفعل.
# ====================================================
def fix_lang_list_order_and_checkmark(out):
    changed = False
    old_list = (
        '    <div class="tools-lang-list" id="tools-lang-list">\n'
        '      <button onclick="langSelect(\'ar\')" data-code="ar">العربية</button>\n'
        '      <button onclick="langSelect(\'fa\')" data-code="fa">🇮🇷 فارسی</button>\n'
        '      <button onclick="langSelect(\'en\')" data-code="en">🇬🇧 English</button>\n'
        '      <button onclick="langSelect(\'fr\')" data-code="fr">🇫🇷 Français</button>\n'
        '      <button onclick="langSelect(\'tr\')" data-code="tr">🇹🇷 Türkçe</button>\n'
        '      <button onclick="langSelect(\'de\')" data-code="de">🇩🇪 Deutsch</button>\n'
        '      <button onclick="langSelect(\'es\')" data-code="es">🇪🇸 Español</button>\n'
        '    </div>'
    )
    new_list = (
        '    <div class="tools-lang-list" id="tools-lang-list">\n'
        '      <button onclick="langSelect(\'ar\')" data-code="ar">العربية<span class="lang-check">✓</span></button>\n'
        '      <button onclick="langSelect(\'en\')" data-code="en">🇬🇧 English<span class="lang-check">✓</span></button>\n'
        '      <button onclick="langSelect(\'es\')" data-code="es">🇪🇸 Español<span class="lang-check">✓</span></button>\n'
        '      <button onclick="langSelect(\'fr\')" data-code="fr">🇫🇷 Français<span class="lang-check">✓</span></button>\n'
        '      <button onclick="langSelect(\'de\')" data-code="de">🇩🇪 Deutsch<span class="lang-check">✓</span></button>\n'
        '      <button onclick="langSelect(\'tr\')" data-code="tr">🇹🇷 Türkçe<span class="lang-check">✓</span></button>\n'
        '      <button onclick="langSelect(\'fa\')" data-code="fa">🇮🇷 فارسی<span class="lang-check">✓</span></button>\n'
        '    </div>'
    )
    if old_list in out:
        out = out.replace(old_list, new_list, 1)
        changed = True
    old_css = '.tools-lang-list button.lang-active{color:var(--green,#2E6B3E);font-weight:700;}'
    new_css = (
        '.tools-lang-list button.lang-active{font-weight:700;}\n'
        '.tools-lang-list button .lang-check{margin-inline-start:auto;color:var(--green,#2E6B3E);font-weight:700;visibility:hidden;}\n'
        '.tools-lang-list button.lang-active .lang-check{visibility:visible;}'
    )
    if old_css in out:
        out = out.replace(old_css, new_css, 1)
        changed = True
    return out, changed

def fix_page_nav_style_and_labels(out):
    """يوضّح ويصغّر شكل زر تنقل الصفحات (بين السور) عشان يبقى بصريًا
    مختلف عن زر تنقل الأسئلة جوه نفس شاشة الاختبار (كانا شكلهم متقارب
    وبيلخبطوا المستخدم)، ويوضح التسمية: 'الصفحة السابقة/التالية' بدل
    'السابق/التالي' العامة. idempotent — بيشتغل على الملفات اللي
    اتحقنلها page-nav-row بالتصميم القديم بس."""
    changed = False
    old_style = ('flex:1;text-align:center;text-decoration:none;padding:10px 4px;'
                 'border-radius:12px;background:var(--surface2);color:var(--accent);'
                 'border:1.5px solid var(--border);font-family:inherit;font-size:14px;')
    new_style = ('flex:1;text-align:center;text-decoration:none;padding:8px 4px;'
                 'border-radius:10px;background:transparent;color:var(--soft,var(--text-faint,#6B8067));'
                 'border:1.5px dashed var(--border);font-family:inherit;font-size:12.5px;')
    if old_style in out:
        out = out.replace(old_style, new_style)
        changed = True
    if '⏮️ السابق</a>' in out and 'class="prev-page-btn"' in out:
        out = out.replace('⏮️ السابق</a>', '⏮️ الصفحة السابقة</a>')
        changed = True
    if 'التالي ⏭️</a>' in out and 'class="next-page-btn"' in out:
        out = out.replace('التالي ⏭️</a>', 'الصفحة التالية ⏭️</a>')
        changed = True
    return out, changed

# ====================================================
# إصلاح محاذاة كروت المستوى (يوليو ٢٠٢٦):
# اسم كل مستوى (سهل/متوسط/صعب/ترتيب) ما كانش دايمًا على نفس الخط بين
# الكروت الأربعة، لأن الأيقونة (إيموجي) مالهاش ارتفاع سطر ثابت بين
# الخطوط المختلفة. الحل: صندوق ثابت الارتفاع للأيقونة + .level-btn
# نفسه flex column — كده اسم المستوى بيبدأ من نفس النقطة بالظبط في
# كل الكروت.
# لون أيقونة "ترتيب" 🔀 (برتقالي حسب نظام الإيموجي): جرّبنا في الأول
# نبدلها بـSVG، بس الشكل طلع مختلف عن شكل الإيموجي الأصلي ومش حلو.
# الحل الصح: نسيب الإيموجي 🔀 زي ما هو بالظبط، ونستخدم CSS filter
# (hue-rotate) يلوّنها أخضر بدل البرتقالي مع الحفاظ التام على شكلها
# الأصلي — مينفعش نلوّن إيموجي بـcolor العادي لأنه رسمة ملوّنة جاهزة
# مش نص عادي.
# ====================================================
LEVEL_CARD_CSS_RE = re.compile(
    r'([ \t]*)\.level-icon\{font-size:28px;display:block;margin-bottom:6px;\}\n'
    r'([ \t]*)\.level-name\{font-weight:700;font-size:15px;display:block;margin-bottom:6px;\}\n'
    r'([ \t]*)\.level-desc\{font-size:12px;color:var\(--text-faint\);line-height:1\.5;\}'
)
LEVEL_BTN_TAIL_RE = re.compile(
    r'font-family:inherit;color:var\(--text\);\}\n([ \t]*)\.level-btn:hover,\.level-btn\.active\{'
)

def fix_level_card_alignment(out):
    changed = False
    m = LEVEL_CARD_CSS_RE.search(out)
    if m:
        ind = m.group(1)
        new_css = (
            f"{ind}.level-icon{{font-size:28px;display:flex;align-items:center;justify-content:center;height:32px;margin-bottom:6px;}}\n"
            f"{ind}.level-icon svg{{width:1.15em;height:1.15em;}}\n"
            f"{ind}#btn-order .level-icon{{color:var(--accent);}}\n"
            f"{ind}.level-name{{font-weight:700;font-size:15px;display:block;margin-bottom:6px;line-height:1.2;}}\n"
            f"{ind}.level-desc{{font-size:12px;color:var(--text-faint);line-height:1.5;}}"
        )
        out = out[:m.start()] + new_css + out[m.end():]
        changed = True
    m2 = LEVEL_BTN_TAIL_RE.search(out)
    if m2:
        ind = m2.group(1)
        new_tail = f"font-family:inherit;color:var(--text);display:flex;flex-direction:column;align-items:center;}}\n{ind}.level-btn:hover,.level-btn.active{{"
        out = out[:m2.start()] + new_tail + out[m2.end():]
        changed = True
    return out, changed

def fix_order_icon_revert_to_emoji(out):
    """رجعة سريعة: لو ملف اتحقنله نسخة SVG قديمة (تجربة سابقة اتلغت)،
    رجّعها لإيموجي 🔀 عادي + فلتر اللون الأخضر — الشكل الأصلي بلون
    مختلف بس، مش رسمة جديدة. كمان بيظبط درجة اللون لو كانت لسه من
    نسخة قديمة زيادة في التشبع (شكلها فلورسنت بدل أخضر طبيعي زي باقي
    الأيقونات)."""
    changed = False
    old_svg = ('<span class="level-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
               'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
               '<polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/>'
               '<polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/>'
               '<line x1="4" y1="4" x2="9" y2="9"/></svg></span>')
    new_emoji = '<span class="level-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 8h3c3 0 5 6 8 6h5"/><path d="M2 16h3c3 0 5-6 8-6h2"/><polyline points="15 5 18 8 15 11"/><polyline points="15 13 18 16 15 19"/></svg></span>'
    if old_svg in out:
        out = out.replace(old_svg, new_emoji, 1)
        changed = True
    new_filter_rule = '#btn-order .level-icon{color:var(--accent);}'
    for old_rule in (
        '#btn-order .level-icon{color:var(--accent);}',
        '#btn-order .level-icon{filter:hue-rotate(85deg) saturate(1.5) brightness(0.9);}',
    ):
        if old_rule in out:
            out = out.replace(old_rule, new_filter_rule, 1)
            changed = True
            break
    return out, changed


OLD_ORDER_ICON_EMOJI_SPAN = '<span class="level-icon">🔀</span>'
NEW_ORDER_ICON_SVG_SPAN = ('<span class="level-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                            '<path d="M2 8h3c3 0 5 6 8 6h5"/><path d="M2 16h3c3 0 5-6 8-6h2"/>'
                            '<polyline points="15 5 18 8 15 11"/><polyline points="15 13 18 16 15 19"/>'
                            '</svg></span>')
OLD_ORDER_ICON_FILTER_RULES = (
    '#btn-order .level-icon{filter:hue-rotate(80deg) saturate(0.55) brightness(0.95);}',
    '#btn-order .level-icon{filter:hue-rotate(85deg) saturate(1.5) brightness(0.9);}',
)
NEW_ORDER_ICON_COLOR_RULE = '#btn-order .level-icon{color:var(--accent);}'


def upgrade_order_icon_to_svg(out):
    """يبدّل أيقونة "ترتيب" من إيموجي 🔀 (رسمة ملوّنة جاهزة من نظام
    كل جهاز، فبتبان بألوان فعلية مختلفة من جهاز لجهاز حتى بعد فلتر
    hue-rotate) لـSVG بخطوط بسيطة (سهمين متقاطعين) بلون
    var(--accent) مباشر — نفس اللون الأخضر بالضبط في كل جهاز
    ومتصفح، لأنه مش معتمد على خط إيموجي المنصة خالص (يوليو ٢٠٢٦)."""
    changed = False
    if OLD_ORDER_ICON_EMOJI_SPAN in out and NEW_ORDER_ICON_SVG_SPAN not in out:
        out = out.replace(OLD_ORDER_ICON_EMOJI_SPAN, NEW_ORDER_ICON_SVG_SPAN, 1)
        changed = True
    for old_rule in OLD_ORDER_ICON_FILTER_RULES:
        if old_rule in out:
            out = out.replace(old_rule, NEW_ORDER_ICON_COLOR_RULE, 1)
            changed = True
            break
    return out, changed

# ====================================================
# تصحيح لاحق (يوليو ٢٠٢٦): تجربة تحويل أيقونة "ترتيب" لـSVG (الدالة
# فوق) اتلغت — لأن السهمين المتقاطعين كانوا بيبانوا بسمك خط وحجم
# مختلفين عن باقي أيقونات المستويات (🌱🌿🌳)، وهي إيموجي ملوّنة عادية،
# فبقى شكل "ترتيب" شاذ وسط الكروت التانية. الحل: رجوع كامل للإيموجي
# 🔀 عشان تبقى نفس أسلوب وحجم باقي المستويات بالظبط. الدالة دي بتلغي
# أي نسخة SVG اتحقنت فعلاً (قديمة أو حديثة) في ملفات سابقة.
# ====================================================
OLD_STYLE_ORDER_ICON_SVG_SPAN = (
    '<span class="level-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/>'
    '<polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/>'
    '<line x1="4" y1="4" x2="9" y2="9"/></svg></span>'
)
ORDER_ICON_EMOJI_SPAN = '<span class="level-icon">🔀</span>'
ORDER_ICON_CSS_RULES_TO_STRIP = (
    NEW_ORDER_ICON_COLOR_RULE,
    '#btn-order .level-icon{filter:hue-rotate(80deg) saturate(0.55) brightness(0.95);}',
    '#btn-order .level-icon{filter:hue-rotate(85deg) saturate(1.5) brightness(0.9);}',
)

def unify_order_icon_style(out):
    changed = False
    for svg_span in (NEW_ORDER_ICON_SVG_SPAN, OLD_STYLE_ORDER_ICON_SVG_SPAN):
        if svg_span in out:
            out = out.replace(svg_span, ORDER_ICON_EMOJI_SPAN, 1)
            changed = True
    for css_rule in ORDER_ICON_CSS_RULES_TO_STRIP:
        if css_rule in out:
            out = out.replace(css_rule, '', 1)
            changed = True
    return out, changed
# اسم ملف الفاتحة الحقيقي هو alfatiha.html، بس سلسلة "السابق/التالي"
# كانت فيها alfatiha_p1 غلط (اسم مش موجود) — فزر "⏮️ الصفحة السابقة"
# في albaqara_p2.html كان بيودّي لصفحة 404. مصلّح دلوقتي في NEXT_SEQUENCE
# نفسها، وده بيصلح أي ملف جديد. الدالة دي بتصلح الملفات اللي الرابط
# الغلط اتحقن فيها بالفعل.
# ====================================================
def fix_alfatiha_broken_link(out):
    changed = False
    if 'alfatiha_p1.html' in out:
        out = out.replace('alfatiha_p1.html', 'alfatiha.html')
        changed = True
    return out, changed

# ====================================================
# إصلاح لخبطة زر تنقل الأسئلة مع زر تنقل الصفحات (يوليو ٢٠٢٦):
# 1) تسمية أزرار الأسئلة بقت أوضح: "السؤال السابق/التالي" بدل
#    "السابق/التالي" العامة (كانت شبه زر تنقل الصفحات). الـregex هنا
#    متسامح مع أي attributes زيادة (زي style=) عشان يشتغل على قوالب
#    مختلفة (جزء عم والبقرة).
# 2) زر تنقل الصفحات (بين السور) جوه شاشة الاختبار العادي بقى مخفي
#    بالبداية، ويظهر بس عند آخر سؤال في الاختبار — بدل ما يفضل ظاهر
#    طول الوقت جنب زر تنقل الأسئلة ويسبب لغبطة.
# ملحوظة: زر تنقل الصفحات في شاشة اختيار المستوى (قبل بدء الاختبار)
# وشاشة الترتيب 🔀 ما بيتلخبطوش مع حاجة تانية، فمتلمسوش.
# ====================================================
PREV_BTN_LABEL_RE = re.compile(r'(id="prev-btn" onclick="prevQuestion\(\)"[^>]*>)→ السابق(</button>)')
NEXT_BTN_LABEL_RE = re.compile(r'(id="next-btn" onclick="nextQuestion\(\)"[^>]*>)التالي ←(</button>)')

def fix_question_nav_and_page_nav_visibility(out):
    changed = False
    if PREV_BTN_LABEL_RE.search(out):
        out = PREV_BTN_LABEL_RE.sub(r'\1→ السؤال السابق\2', out, count=1)
        changed = True
    if NEXT_BTN_LABEL_RE.search(out):
        out = NEXT_BTN_LABEL_RE.sub(r'\1السؤال التالي ←\2', out, count=1)
        changed = True

    anchor_old = (
        '<div class="feedback" id="feedback"></div>\n'
        '  <button class="level-return-btn" onclick="returnToLevels()">🔄 اختر اختباراً آخر</button>\n'
        '<div class="page-nav-row" style="display:flex;gap:8px;margin-top:10px;">'
    )
    anchor_new = (
        '<div class="feedback" id="feedback"></div>\n'
        '  <button class="level-return-btn" onclick="returnToLevels()">🔄 اختر اختباراً آخر</button>\n'
        '<div class="page-nav-row" id="quiz-page-nav" style="display:none;gap:8px;margin-top:10px;">'
    )
    if anchor_old in out:
        out = out.replace(anchor_old, anchor_new, 1)
        changed = True

    js_old = "renderDotProgress();const zone=document.getElementById('answer-zone');"
    js_new = ("renderDotProgress();const qpn=document.getElementById('quiz-page-nav');"
              "if(qpn)qpn.style.display=(qIndex===questions.length-1)?'flex':'none';"
              "const zone=document.getElementById('answer-zone');")
    if js_old in out:
        out = out.replace(js_old, js_new, 1)
        changed = True
    return out, changed

# ====================================================
# نفس إصلاح ترتيب الأسئلة/الصفحات، بس لقالب صفحات البقرة القديم
# (albaqara_p*.html) — بنية مختلفة تمامًا عن جزء عم:
# الترتيب الحالي: feedback → 🔄 اختر مستوى آخر → [page-nav-row لو
# مضاف] → ⏭ تخطي → صف السابق/التالي. ده معناه زر تنقل الصفحات (بين
# صفحات البقرة) بيظهر *قبل* زر تنقل الأسئلة، عكس اللي المستخدم عايزه.
# الحل: ننقل page-nav-row (لو موجود) لبعد صف السابق/التالي مباشرة،
# ونضيفله نفس منطق الإخفاء إلا عند آخر سؤال.
# ====================================================
BAQARA_TRAILER_RE = re.compile(
    r'(\s*<button class="skip-btn"[^>]*>.*?</button>\s*'
    r'<div style="display:flex; gap:10px; margin-top:12px;">\s*'
    r'<button class="next-btn" id="prev-btn".*?</button>\s*'
    r'<button class="next-btn" id="next-btn".*?</button>\s*'
    r'</div>\s*)', re.S
)
BAQARA_PAGE_NAV_RE = re.compile(r'<div class="page-nav-row"[^>]*>.*?</div>\n?', re.S)

def fix_baqara_page_nav_placement(out):
    changed = False
    for nav_m in list(BAQARA_PAGE_NAV_RE.finditer(out)):
        before = out[:nav_m.start()]
        if not before.rstrip().endswith('</button>'):
            continue
        after = out[nav_m.end():]
        trailer_m = BAQARA_TRAILER_RE.match(after)
        if not trailer_m:
            continue  # مش النسخة اللي جوه شاشة الاختبار (يمكن شاشة اختيار المستوى) — منلمسوش
        page_nav_block = nav_m.group(0).rstrip('\n')
        if 'id="quiz-page-nav"' not in page_nav_block:
            page_nav_block = page_nav_block.replace(
                '<div class="page-nav-row"',
                '<div class="page-nav-row" id="quiz-page-nav"', 1
            ).replace('style="display:flex;', 'style="display:none;', 1)
        trailer = trailer_m.group(1)
        rest = after[trailer_m.end():]
        out = before + trailer + page_nav_block + '\n' + rest
        changed = True
        break  # اتصلح واحد بس (المفروض واحد بس بالنمط ده أصلاً) — نوقف هنا عشان انديكسات out اتغيرت
    return out, changed

BAQARA_SHOWQ_JS_RE = re.compile(
    r"(document\.getElementById\('skip-btn'\)\.style\.display\s*=\s*'block';\s*renderDotProgress\(\);)"
)

def fix_baqara_page_nav_visibility_js(out):
    changed = False
    if 'quiz-page-nav' not in out or 'const qpn=document' in out:
        return out, changed
    m = BAQARA_SHOWQ_JS_RE.search(out)
    if m:
        out = out[:m.end()] + (
            "const qpn=document.getElementById('quiz-page-nav');"
            "if(qpn)qpn.style.display=(qIndex===questions.length-1)?'flex':'none';"
        ) + out[m.end():]
        changed = True
    return out, changed

# ====================================================
# تقصير وصف مستوى "صعب" (يوليو ٢٠٢٦): بعض الملفات (صفحات البقرة
# القديمة) لسه فيها الوصف الطويل "اكتب الآية كاملة من الذاكرة بدون أي
# مساعدة" اللي بيكسر محاذاة الكرت مقارنة بباقي الكروت. نقصّره لنفس
# النص المستخدم في باقي الملفات: "اكتب الآية كاملة".
# ====================================================
HARD_DESC_RE = re.compile(
    r'(id="btn-hard".*?<span class="level-desc">)([^<]*)(</span>)', re.S
)

def fix_hard_level_desc(out):
    changed = False
    m = HARD_DESC_RE.search(out)
    if m and ('بدون' in m.group(2) or 'الذاكرة' in m.group(2)) and m.group(2) != 'اكتب الآية كاملة':
        out = out[:m.start(2)] + 'اكتب الآية كاملة' + out[m.end(2):]
        changed = True
    return out, changed


BAQARA_CLEAN_TEMPLATE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<script>
(function(){
  try{
    var p=new URLSearchParams(location.search);
    if(p.get('dev')==='1'){localStorage.setItem('darbi_dev','1');}
    if(localStorage.getItem('darbi_dev')!=='1'){
      document.documentElement.classList.add('darbi-locked');
    }
  }catch(e){}
})();
</script>
<style>html.darbi-locked #btn-hard,html.darbi-locked a[href*="recitation.html"]{display:none !important;}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-WFT6TYVB75"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-WFT6TYVB75");</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<link href="https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;700&family=Amiri:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#f0f4f0;--text:#2d4a2d;--card:#fff;--border:#c8d9c0;--gold:#c4a84a;--text-soft:#7a9a7a;--accent:#4a7c4a;--surface2:#f4f8f2;--surface-hover:#e0edd8;--correct-bg:#d4edda;--correct-text:#1a5c1a;--wrong-bg:#f8d7da;--wrong-text:#7a1a1a;--wrong-border:#c0392b;--surface3:#f8fbf6;--text-faint:#6a8a6a;--accent-light:#9db89d;--accent-dark:#3a6a3a;--hint-bg:#f0f5ec;--hint-border:#9bbf8a;--hint-btn-bg:#fff7e6;--hint-btn-text:#9a7b1f;--hint-btn-border:#e8d28a;}
html[data-theme="dark"]{--bg:#1c2420;--text:#d9ecd9;--card:#232f29;--border:#3a4d40;--gold:#d9b96a;--text-soft:#8fae8f;--accent:#5fae5f;--surface2:#2a3830;--surface-hover:#324438;--correct-bg:#234a30;--correct-text:#8fe0a0;--wrong-bg:#4a2328;--wrong-text:#e89a9a;--wrong-border:#c0392b;--surface3:#1f2a24;--text-faint:#9bb49b;--accent-light:#4a6a4a;--accent-dark:#7fcf7f;--hint-bg:#2a3424;--hint-border:#5a7a4a;--hint-btn-bg:#3a3324;--hint-btn-text:#d9b96a;--hint-btn-border:#5a4a2a;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Amiri','Scheherazade New','Traditional Arabic',serif;background:var(--bg);color:var(--text);min-height:100vh;direction:rtl;transition:background-color .3s,color .3s;}
.top-bar{background:var(--bg);padding:12px 20px;display:flex;align-items:center;gap:10px;}
.back-btn{background:none;border:none;color:var(--accent);font-size:18px;cursor:pointer;text-decoration:none;display:flex;align-items:center;gap:6px;font-family:inherit;}
.info-card{margin:0 16px 16px;background:var(--card);border:1.5px solid var(--border);border-radius:18px;padding:22px 20px 18px;text-align:center;position:relative;}
.info-card::before,.info-card::after{content:'✦';color:var(--gold);font-size:20px;position:absolute;top:16px;}
.info-card::before{right:18px;}.info-card::after{left:18px;}
.surah-title{font-size:28px;font-weight:700;color:var(--text);margin-bottom:4px;}
.ayat-range{font-size:15px;color:var(--accent);margin-bottom:4px;}
.page-info{font-size:14px;color:var(--text-soft);margin-bottom:14px;}
.stats-row{display:flex;gap:10px;justify-content:center;}
.stat-badge{background:var(--accent);color:var(--card);border-radius:12px;padding:8px 18px;font-size:14px;text-align:center;min-width:80px;line-height:1.4;}
.level-card{margin:0 16px 16px;background:var(--card);border:1.5px solid var(--border);border-radius:18px;padding:24px 20px 20px;text-align:center;}
.level-title{font-size:22px;color:var(--text);margin-bottom:6px;}
.level-sub{font-size:14px;color:var(--text-soft);margin-bottom:20px;}
.levels-grid{display:flex;gap:8px;justify-content:center;margin-bottom:20px;flex-wrap:wrap;}
.level-btn{flex:1;min-width:76px;max-width:100px;background:var(--surface2);border:1.5px solid var(--border);border-radius:14px;padding:14px 6px;cursor:pointer;transition:all .2s;font-family:inherit;color:var(--text);display:flex;flex-direction:column;align-items:center;}
.level-btn:hover,.level-btn.active{background:var(--surface-hover);border-color:var(--accent);}
.level-icon{font-size:28px;display:flex;align-items:center;justify-content:center;height:32px;margin-bottom:6px;}
.level-icon svg{width:1.15em;height:1.15em;}
#btn-order .level-icon{color:var(--accent);}
.level-name{font-weight:700;font-size:15px;display:block;margin-bottom:6px;line-height:1.2;}
.level-desc{font-size:12px;color:var(--text-faint);line-height:1.5;}
.start-btn{width:100%;max-width:260px;background:var(--accent-light);color:var(--card);border:none;border-radius:14px;padding:14px 20px;font-size:17px;font-family:inherit;cursor:pointer;transition:background .2s;}
.start-btn.ready{background:var(--accent);}
.quiz-area{margin:0 16px 16px;background:var(--card);border:1.5px solid var(--border);border-radius:18px;padding:24px 20px;display:none;}
.q-number{font-size:13px;color:var(--text-soft);margin-bottom:10px;text-align:center;}
.q-text{font-size:20px;line-height:2;color:var(--text);text-align:center;margin-bottom:20px;background:var(--surface3);border-radius:12px;padding:16px;}
.choices{display:flex;flex-direction:column;gap:10px;}
.choice-btn{background:var(--surface2);border:1.5px solid var(--border);border-radius:12px;padding:14px 18px;font-size:17px;font-family:inherit;color:var(--text);cursor:pointer;text-align:right;transition:all .15s;line-height:1.8;}
.choice-btn:hover:not(:disabled){background:var(--surface-hover);border-color:var(--accent);}
.choice-btn.correct{background:var(--correct-bg);border-color:var(--accent);color:var(--correct-text);}
.choice-btn.wrong{background:var(--wrong-bg);border-color:var(--wrong-border);color:var(--wrong-text);}
.answer-input{width:100%;border:1.5px solid var(--border);border-radius:12px;padding:14px 16px;font-size:18px;font-family:inherit;color:var(--text);background:var(--surface3);outline:none;resize:vertical;min-height:70px;text-align:right;direction:rtl;}
.answer-input:focus{border-color:var(--accent);}
.submit-btn{margin-top:14px;width:100%;background:var(--accent);color:var(--card);border:none;border-radius:12px;padding:13px;font-size:17px;font-family:inherit;cursor:pointer;}
.submit-btn:hover{background:var(--accent-dark);}
.submit-btn:disabled{opacity:0.5;cursor:default;}
.feedback{margin-top:14px;padding:14px;border-radius:12px;font-size:16px;line-height:1.9;display:none;text-align:center;}
.feedback.correct{background:var(--correct-bg);color:var(--correct-text);}
.feedback.wrong{background:var(--wrong-bg);color:var(--wrong-text);}
.nav-row{display:flex;gap:10px;margin-top:14px;}
.nav-btn{flex:1;background:var(--surface2);color:var(--accent);border:1.5px solid var(--border);border-radius:12px;padding:13px;font-size:17px;font-family:inherit;cursor:pointer;}
.nav-btn:hover:not(:disabled){background:var(--surface-hover);}
.nav-btn:disabled{opacity:0.4;cursor:default;}
.nav-btn.primary{background:var(--accent);color:var(--card);border-color:var(--accent);}
.nav-btn.primary:hover{background:var(--accent-dark);}
.q-dot{width:11px;height:11px;border-radius:50%;background:var(--border);transition:all .2s;}
.q-dot.current{width:15px;height:15px;box-shadow:0 0 0 3px var(--surface-hover);background:var(--accent);}
.q-dot.correct{background:var(--accent);}
.q-dot.wrong{background:var(--wrong-border);}
.progress-bar-wrap{background:var(--surface-hover);border-radius:8px;height:8px;margin-bottom:18px;overflow:hidden;}
.progress-bar-fill{height:100%;background:var(--accent);border-radius:8px;transition:width .3s;}
.result-area{margin:0 16px 16px;background:var(--card);border:1.5px solid var(--border);border-radius:18px;padding:30px 20px;text-align:center;display:none;}
.result-icon{font-size:52px;margin-bottom:12px;}
.result-title{font-size:24px;font-weight:700;color:var(--text);margin-bottom:8px;}
.result-score{font-size:18px;color:var(--accent);margin-bottom:20px;}
.result-msg{font-size:16px;color:var(--text-faint);margin-bottom:24px;}
.retry-btn{background:var(--accent);color:var(--card);border:none;border-radius:12px;padding:13px 30px;font-size:17px;font-family:inherit;cursor:pointer;margin:5px;}
.retry-btn:hover{background:var(--accent-dark);}
.home-link{display:inline-block;background:var(--surface2);color:var(--accent);border:1.5px solid var(--border);border-radius:12px;padding:12px 28px;font-size:17px;font-family:inherit;text-decoration:none;margin:5px;}
.confetti-piece{position:absolute;top:-20px;width:9px;height:14px;opacity:0.9;animation:confetti-fall linear forwards;}
@keyframes confetti-fall{to{transform:translateY(110vh) rotate(540deg);opacity:0.3;}}
.rec-transcript{background:var(--surface3);border:1.5px solid var(--border);border-radius:12px;padding:12px 14px;font-size:17px;line-height:1.9;color:var(--text);direction:rtl;text-align:right;margin-bottom:10px;display:none;min-height:60px;white-space:pre-wrap;}
.rec-word{display:inline-block;background:var(--surface-hover);border-radius:4px;padding:2px 6px;margin:2px 1px;cursor:pointer;}
.hint-btn{width:100%;background:var(--hint-btn-bg);color:var(--hint-btn-text);border:1.5px solid var(--hint-btn-border);border-radius:10px;padding:10px;font-size:15px;font-family:inherit;cursor:pointer;margin-top:10px;}
.hint-box{display:none;background:var(--hint-bg);border:1.5px dashed var(--hint-border);border-radius:10px;padding:10px 14px;margin-top:10px;font-size:18px;color:var(--accent-dark);text-align:center;direction:rtl;line-height:2;}
.level-return-btn{display:block;width:100%;margin-top:14px;padding:11px;background:var(--surface2);color:var(--text-soft);border:1.5px solid var(--border);border-radius:12px;font-size:15px;font-family:inherit;cursor:pointer;transition:all .2s;text-align:center;}
.level-return-btn:hover{background:var(--surface-hover);border-color:var(--accent);color:var(--accent);}
.order-item{background:var(--surface2);border:1.5px solid var(--border);border-radius:12px;padding:14px 18px;font-size:18px;font-family:inherit;color:var(--text);cursor:pointer;text-align:right;transition:all .15s;line-height:1.9;width:100%;}.order-item:hover{background:var(--surface-hover);border-color:var(--accent);}.order-filled-grid{display:flex;flex-direction:column;gap:10px;margin-bottom:10px;}.order-slot{display:flex;gap:8px;align-items:center;border-radius:12px;padding:12px 14px;font-size:16px;line-height:1.7;cursor:pointer;}.order-slot.filled{background:var(--surface3);border:2px solid var(--accent);box-shadow:0 1px 4px rgba(0,0,0,.07);}.order-slot.correct-slot{background:var(--correct-bg) !important;border-color:var(--accent) !important;color:var(--correct-text) !important;}.order-slot.wrong-slot{background:var(--wrong-bg) !important;border-color:var(--wrong-border) !important;color:var(--wrong-text) !important;}.order-empty-strip{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px;}.order-dot{display:flex;align-items:center;justify-content:center;min-width:34px;height:32px;padding:0 3px;flex-shrink:0;border-radius:50%;background:var(--surface2);border:1.5px dashed var(--border);color:var(--hint-btn-text);font-size:15px;font-family:'Amiri','Scheherazade New',serif;cursor:pointer;transition:all .15s;}.order-dot:hover{border-color:var(--accent);}.order-dot.active{border-style:solid;border-color:var(--accent);background:var(--hint-bg);color:var(--accent-dark);font-weight:700;box-shadow:0 0 0 3px var(--surface-hover);}.order-badge{color:var(--hint-btn-text);font-size:16px;font-family:'Amiri','Scheherazade New',serif;flex-shrink:0;cursor:pointer;min-width:34px;min-height:34px;display:inline-flex;align-items:center;justify-content:center;padding:4px;margin:-4px;border-radius:8px;}.order-slot.order-slot-selected{border-color:var(--gold,#C4A84A) !important;box-shadow:0 0 0 2px var(--gold,#C4A84A);}.mushaf-block{background:var(--surface3);border:1.5px solid var(--border);border-radius:12px;padding:18px 16px;margin-top:12px;font-size:19px;line-height:2.4;text-align:justify;direction:rtl;color:var(--text);}.ayah-end{color:var(--gold);font-size:15px;}
</style>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#4a7c4a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="دربي">
<link rel="apple-touch-icon" href="icons/icon-192x192.png">
</head>
<body>
<div class="top-bar">
  <a href="index.html" class="back-btn">← الرجوع</a>
  <button id="theme-toggle" onclick="toggleTheme()" style="background:var(--surface2);border:1.5px solid var(--border);border-radius:50%;width:36px;height:36px;font-size:16px;cursor:pointer;">🌙</button><div class="tools-fab" id="tools-fab">
  <button class="tools-fab-btn" id="tools-fab-btn" onclick="toolsToggle(event)" title="الأدوات">☰</button>
  <div class="tools-menu" id="tools-menu">
    <button class="tools-item" onclick="toolsLangToggle(event)">🌍 اللغة <span class="tools-lang-inline"><span id="tools-lang-cur">العربية</span><span class="tools-arrow" id="tools-lang-arrow">▾</span></span></button>
    <div class="tools-lang-list" id="tools-lang-list">
      <button onclick="langSelect('ar')" data-code="ar">🇸🇦 العربية</button>
      <button onclick="langSelect('en')" data-code="en">🇬🇧 English</button>
      <button onclick="langSelect('fr')" data-code="fr">🇫🇷 Français</button>
      <button onclick="langSelect('tr')" data-code="tr">🇹🇷 Türkçe</button>
      <button onclick="langSelect('fa')" data-code="fa">🇮🇷 فارسی</button>
      <button onclick="langSelect('de')" data-code="de">🇩🇪 Deutsch</button>
      <button onclick="langSelect('es')" data-code="es">🇪🇸 Español</button>
    </div>
    <button class="tools-item" onclick="toolsClose();fdbkOpen();">💬 الاقتراحات</button>
    <button class="tools-item" onclick="toolsClose();shareApp();"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.6" y1="10.5" x2="15.4" y2="6.5"/><line x1="8.6" y1="13.5" x2="15.4" y2="17.5"/></svg> مشاركة الصفحة</button>
    <button class="tools-item" onclick="toolsClose();showQR();"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><rect x="8" y="8" width="8" height="8" rx="1"/></svg> كود QR</button>
  </div>
</div>
</div>
<div class="info-card">
  <div class="surah-title">__SURAH_TITLE__</div>
  <div class="ayat-range">__AYAT_RANGE__</div>
  <div class="page-info">__PAGE_INFO__</div>
  <div class="stats-row">
    <div class="stat-badge" id="qnum-badge">السؤال 1 /<br><span id="total-q">-</span></div>
    <div class="stat-badge" id="wrong-badge">0 ✗<br>خطأ</div>
    <div class="stat-badge" id="correct-badge">0 ✓<br>صحيح</div>
  </div>
</div>
<div id="resume-banner" style="display:none;margin:0 16px 16px;background:var(--surface2);border:1.5px solid var(--gold);border-radius:14px;padding:14px 16px;text-align:center;">
  <div style="margin-bottom:10px;font-size:15px;color:var(--text);">📌 عندك اختبار لسه ما خلصتيهوش، عايزة تكملي منين وقفتِ؟</div>
  <div style="display:flex;gap:10px;">
    <button onclick="resumeQuiz()" style="flex:1;background:var(--accent);color:#fff;border:none;border-radius:10px;padding:10px;font-family:inherit;font-size:15px;cursor:pointer;">المتابعة من هنا</button>
    <button onclick="dismissResume()" style="flex:1;background:var(--surface3);color:var(--text-soft);border:1.5px solid var(--border);border-radius:10px;padding:10px;font-family:inherit;font-size:15px;cursor:pointer;">البدء من جديد</button>
  </div>
</div>
<div class="level-card" id="level-card">
  <div class="level-title">اختر مستوى الاختبار</div>
  <div class="level-sub">كل مستوى له طريقة مختلفة في الاختبار</div>
  <div class="levels-grid">
    <button class="level-btn" onclick="selectLevel('easy')" id="btn-easy"><span class="level-icon">🌱</span><span class="level-name">سهل</span><span class="level-desc">اختيار من متعدد</span></button>
    <button class="level-btn" onclick="selectLevel('medium')" id="btn-medium"><span class="level-icon">🌿</span><span class="level-name">متوسط</span><span class="level-desc">إكمال فراغ</span></button>
    <button class="level-btn" onclick="selectLevel('hard')" id="btn-hard"><span class="level-icon">🌳</span><span class="level-name">صعب</span><span class="level-desc">اكتب الآية كاملة</span></button>
    <button class="level-btn" onclick="selectLevel('order')" id="btn-order"><span class="level-icon">🔀</span><span class="level-name">ترتيب</span><span class="level-desc">رتّب الآيات</span></button>
  </div>
  <button class="start-btn" id="start-btn" onclick="startQuiz()">ابدأ الاختبار ←</button>
<div class="page-nav-row" style="display:flex;gap:8px;margin-top:10px;"><a href="__PREV_PAGE__" class="prev-page-btn" style="flex:1;text-align:center;text-decoration:none;padding:8px 4px;border-radius:10px;background:transparent;color:var(--soft,var(--text-faint,#6B8067));border:1.5px dashed var(--border);font-family:inherit;font-size:12.5px;">⏮️ الصفحة السابقة</a><a href="__NEXT_PAGE__" class="next-page-btn" style="flex:1;text-align:center;text-decoration:none;padding:8px 4px;border-radius:10px;background:transparent;color:var(--soft,var(--text-faint,#6B8067));border:1.5px dashed var(--border);font-family:inherit;font-size:12.5px;">الصفحة التالية ⏭️</a></div>
</div>
<div class="quiz-area" id="quiz-area">
  <div class="progress-bar-wrap"><div class="progress-bar-fill" id="progress-fill" style="width:0%"></div></div>
  <div id="dot-progress" style="display:flex;flex-wrap:wrap;gap:5px;justify-content:center;margin-bottom:14px;"></div>
  <div class="q-number" id="q-number">السؤال 1</div>
  <div class="q-text" id="q-text"></div>
  <div id="answer-zone"></div>
  <div class="nav-row">
    <button class="nav-btn" id="prev-btn" onclick="prevQuestion()">→ السؤال السابق</button>
    <button class="nav-btn" id="skip-btn" onclick="skipQuestion()">⏭ تخطي</button>
    <button class="nav-btn primary" id="next-btn" onclick="nextQuestion()" style="display:none;">السؤال التالي ←</button>
  </div>
  <div class="feedback" id="feedback"></div>
  <button class="level-return-btn" onclick="returnToLevels()">🔄 اختر اختباراً آخر</button>
<div class="page-nav-row" style="display:flex;gap:8px;margin-top:10px;"><a href="__PREV_PAGE__" class="prev-page-btn" style="flex:1;text-align:center;text-decoration:none;padding:8px 4px;border-radius:10px;background:transparent;color:var(--soft,var(--text-faint,#6B8067));border:1.5px dashed var(--border);font-family:inherit;font-size:12.5px;">⏮️ الصفحة السابقة</a><a href="__NEXT_PAGE__" class="next-page-btn" style="flex:1;text-align:center;text-decoration:none;padding:8px 4px;border-radius:10px;background:transparent;color:var(--soft,var(--text-faint,#6B8067));border:1.5px dashed var(--border);font-family:inherit;font-size:12.5px;">الصفحة التالية ⏭️</a></div>
</div>
<div class="quiz-area" id="order-area">
  <div class="q-number">رتّب الآيات — اضغط على الآية فتُوضَع بالتسلسل. تريد تخطّي خانة؟ اضغط على الخانة التي تريد المتابعة منها</div>
  <div id="order-slots" style="margin-bottom:16px;"></div>
  <div id="order-pool" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-bottom:14px;"></div>
  <div class="nav-row">
    <button class="nav-btn" id="order-reveal-btn" onclick="revealOrderAnswer()">💡 أظهر الترتيب الصحيح</button>
    <button class="nav-btn primary" id="order-check-btn" onclick="checkOrderAnswer()" style="display:none;">تحقق ✓</button>
  </div>
  <div id="order-reveal" style="display:none;"></div>
  <div class="feedback" id="order-feedback"></div>
  <button class="level-return-btn" onclick="returnToLevels()">🔄 اختر اختباراً آخر</button>
<div class="page-nav-row" style="display:flex;gap:8px;margin-top:10px;"><a href="__PREV_PAGE__" class="prev-page-btn" style="flex:1;text-align:center;text-decoration:none;padding:8px 4px;border-radius:10px;background:transparent;color:var(--soft,var(--text-faint,#6B8067));border:1.5px dashed var(--border);font-family:inherit;font-size:12.5px;">⏮️ الصفحة السابقة</a><a href="__NEXT_PAGE__" class="next-page-btn" style="flex:1;text-align:center;text-decoration:none;padding:8px 4px;border-radius:10px;background:transparent;color:var(--soft,var(--text-faint,#6B8067));border:1.5px dashed var(--border);font-family:inherit;font-size:12.5px;">الصفحة التالية ⏭️</a></div>
</div>
<div class="result-area" id="result-area">
  <div class="result-icon" id="result-icon">🌟</div>
  <div class="result-title" id="result-title">أحسنتِ!</div>
  <div class="result-score" id="result-score"></div>
  <div class="result-msg" id="result-msg"></div>
  <button class="retry-btn" id="review-mistakes-btn" onclick="startReview()" style="display:none;background:var(--wrong-border);">📝 راجع أخطائي</button>
  <button class="retry-btn" onclick="retryQuiz()">🔄 اختر اختباراً آخر</button>
  <a href="index.html" class="home-link">← الرئيسية</a>
</div>
<div class="quiz-area" id="review-area" style="display:none;">
  <div class="q-number" id="review-number"></div>
  <div class="q-text" id="review-q-text"></div>
  <div style="background:var(--surface3);border-radius:12px;padding:16px;text-align:center;font-size:19px;line-height:2;color:var(--correct-text);" id="review-answer"></div>
  <div class="nav-row" style="margin-top:14px;">
    <button class="nav-btn" onclick="reviewNav(-1)">→ السابق</button>
    <button class="nav-btn primary" onclick="reviewNav(1)">التالي ←</button>
  </div>
  <a href="#" onclick="endReview();return false;" style="display:block;text-align:center;margin-top:14px;color:var(--text-soft);font-size:14px;">إنهاء المراجعة</a>
</div>
<div id="confetti-container" style="position:fixed;inset:0;pointer-events:none;z-index:9999;overflow:hidden;display:none;"></div>
<script>
const RESUME_KEY='__RESUME_KEY__';
const AYAT=__AYAT_JSON__;
const AYAT_NUMS=__AYAT_NUMS_JSON__;
const EASY_Q=__EASY_Q_JSON__;
const MEDIUM_Q=__MEDIUM_Q_JSON__;
const HARD_Q=__HARD_Q_JSON__;
let currentLevel=null,statuses=[],wrongIndices=[],questions=[],qIndex=0,correctCount=0,wrongCount=0;
function normalize(str){if(!str)return'';return str.replace(/[\\u064B-\\u065F\\u0610-\\u061A\\u06D6-\\u06DC\\u06DF-\\u06E4\\u06E7\\u06E8\\u06EA-\\u06ED\\u08F0-\\u08F2]/g,'').replace(/[ىی]ٰ(?=\\S)/g,'ا').replace(/[ىی]ٰ/g,'ي').replace(/وٱ(?!ل)/g,'و').replace(/(?<=^|\\s)وا(?=سجد|قترب|دخل|دعو|ذكر|رحم|ستغفر|ستغن|غفر|عف|نحر|تق|ختلاف|مر[أا]|تبع|سمع|ستكبر|ستعين|ركع|صبر|صل|جتنب|هبط|ستبشر|ستقم|ضرب|عتصم|ئتلف|بتغ|حذر|شرب|صفح|تخذ)/g,'و').replace(/اٰ/g,'ا').replace(/نٰ/g,'نا').replace(/ٰ/g,'ا').replace(/ـۧ/g,'ي').replace(/يٓ?ـَٔ/g,'ي').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـ/g,'').replace(/[آأإٱا]/g,'ا').replace(/ها[ؤو]لاء|ها[ؤو]لا(?!\\S)/g,'هالا').replace(/ه[ؤو]لاء|ه[ؤو]لا(?!\\S)/g,'هالا').replace(/[ءئؤ]/g,'').replace(/ة/g,'ه').replace(/[ىی]/g,'ي').replace(/ه[ۥۦ]/g,'ه').replace(/ۦ(?=\\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'').replace(/واه(?=\\s|$)/g,'اه').replace(/رحمان/g,'رحمن').replace(/(?<=^|\\s)فازالهما(?=\\s|$)/g,'فازلهما').replace(/(?<=^|\\s)فاذلهما(?=\\s|$)/g,'فازلهما').replace(/(?<=^|\\s)فادراتم(?=\\s|$)/g,'فادارتم').replace(/(?<=^|\\s)فادرأتم(?=\\s|$)/g,'فادارتم').replace(/(?<=^|\\s)فاداراتم(?=\\s|$)/g,'فادارتم').replace(/(?<=^|\\s)بن(?=\\s|$)/g,'ابن').replace(/نصاري(?=\\s|$)/g,'نصارا').replace(/(?<=^|\\s)ناتي(?=\\s|$)/g,'نات').replace(/(?<=^|\\s)ولا تجدنهم(?=\\s|$)/g,'ولتجدنهم').replace(/(?<=^|\\s)ولاتجدنهم(?=\\s|$)/g,'ولتجدنهم').replace(/(?<=^|\\s)او كل ما(?=\\s|$)/g,'اوكلما').replace(/(?<=^|\\s)او كلما(?=\\s|$)/g,'اوكلما').replace(/(?<=^|\\s)بلي(?=\\s|$)/g,'بلا').replace(/مولانا/g,'مولنا').replace(/يا ايها/g,'يايها').replace(/يا ايتها/g,'يايتها').replace(/الاه/g,'اله').replace(/ارايت/g,'اريت').replace(/نب/g,'مب').replace(/لل/g,'ل').replace(/(?<=^|\\s)ممنع(?=\\s|$)/g,'ممن منع').replace(/(.)\\1+/g,'$1').replace(/ا(?=\\s|$)/g,'ي').replace(/\\s+/g,' ').trim();}
function wordDiff(userVal,correctAnswer){const nm=s=>{if(!s)return'';return s.replace(/[\\u064B-\\u065F\\u0610-\\u061A\\u06D6-\\u06DC\\u06DF-\\u06E4\\u06E7\\u06E8\\u06EA-\\u06ED\\u08F0-\\u08F2]/g,'').replace(/[ىی]ٰ(?=\\S)/g,'ا').replace(/[ىی]ٰ/g,'ي').replace(/وٱ(?!ل)/g,'و').replace(/اٰ/g,'ا').replace(/نٰ/g,'نا').replace(/ٰ/g,'ا').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـ/g,'').replace(/[آأإٱا]/g,'ا').replace(/ها[ؤو]لاء|ها[ؤو]لا(?!\\S)/g,'هالا').replace(/ه[ؤو]لاء|ه[ؤو]لا(?!\\S)/g,'هالا').replace(/[ءئؤ]/g,'').replace(/ة/g,'ه').replace(/[ىی]/g,'ي').replace(/ه[ۥۦ]/g,'ه').replace(/ۦ(?=\\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'').replace(/واه(?=\\s|$)/g,'اه').replace(/رحمان/g,'رحمن').replace(/مولانا/g,'مولنا').replace(/يا ايها/g,'يايها').replace(/يا ايتها/g,'يايتها').replace(/الاه/g,'اله').replace(/ارايت/g,'اريت').replace(/نب/g,'مب').replace(/لل/g,'ل').replace(/(.)\\1+/g,'$1').replace(/ا(?=\\s|$)/g,'ي').replace(/\\s+/g,' ').trim();};const uWords=userVal.trim().split(/\\s+/),cWords=correctAnswer.split(/\\s+/),n=cWords.length,m=uWords.length;const dp=Array.from({length:n+1},()=>new Array(m+1).fill(0));for(let i=1;i<=n;i++)for(let j=1;j<=m;j++){if(nm(cWords[i-1])===nm(uWords[j-1]))dp[i][j]=dp[i-1][j-1]+1;else dp[i][j]=Math.max(dp[i-1][j],dp[i][j-1]);}const aligned=[];let i=n,j=m;while(i>0||j>0){if(i>0&&j>0&&nm(cWords[i-1])===nm(uWords[j-1])){aligned.push({ref:cWords[i-1],ok:true});i--;j--;}else if(j>0&&(i===0||dp[i][j-1]>=dp[i-1][j])){j--;}else{aligned.push({ref:cWords[i-1],ok:false});i--;}}aligned.reverse();const correct=aligned.filter(x=>x.ok).length;const html=aligned.map(x=>x.ok?`<span style="color:#155724;background:#c3e6cb;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;font-weight:bold;" translate="no" class="notranslate">${x.ref}</span>`:`<span style="color:#fff;background:#c0392b;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;" translate="no" class="notranslate">${x.ref}</span>`).join(' ');return `<div style="margin-bottom:6px;font-size:13px;color:var(--text-soft);">${correct} / ${n} كلمة صحيحة</div><div style="font-size:18px;line-height:2.5;direction:rtl;text-align:right;">${html}</div>`;}
function toArabicNum(n){return n;}
function updateBadges(){document.getElementById('qnum-badge').innerHTML=`السؤال ${toArabicNum(qIndex+1)} /<br>${toArabicNum(questions.length)}`;document.getElementById('wrong-badge').innerHTML=`${toArabicNum(wrongCount)} ✗<br>خطأ`;document.getElementById('correct-badge').innerHTML=`${toArabicNum(correctCount)} ✓<br>صحيح`;}
function selectLevel(lvl){if(lvl==='order'){currentLevel=lvl;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));var __ob=document.getElementById('btn-order');if(__ob)__ob.classList.add('active');document.getElementById('start-btn').classList.add('ready');document.getElementById('total-q').textContent=toArabicNum(AYAT.length);return;}currentLevel=lvl;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));document.getElementById('btn-'+lvl).classList.add('active');document.getElementById('start-btn').classList.add('ready');if(lvl==='order'){document.getElementById('total-q').textContent=toArabicNum(AYAT.length);}else{document.getElementById('total-q').textContent=toArabicNum((lvl==='easy'?EASY_Q:lvl==='medium'?MEDIUM_Q:HARD_Q).length);}}
function startQuiz(){if(currentLevel==='order'){startOrderQuiz();return;}if(!currentLevel)return;questions=currentLevel==='easy'?[...EASY_Q]:currentLevel==='medium'?[...MEDIUM_Q]:[...HARD_Q];qIndex=correctCount=wrongCount=0;statuses=questions.map(()=>'pending');wrongIndices=[];document.getElementById('resume-banner').style.display='none';document.getElementById('level-card').style.display='none';document.getElementById('quiz-area').style.display='block';showQuestion();}
function shuffle(arr){for(let i=arr.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]];}return arr;}
function renderDotProgress(){const wrap=document.getElementById('dot-progress');if(!wrap)return;wrap.innerHTML='';statuses.forEach((st,i)=>{const dot=document.createElement('span');dot.className='q-dot'+(i===qIndex?' current':st!=='pending'?' '+st:'');wrap.appendChild(dot);});}
function saveResumeState(){try{localStorage.setItem(RESUME_KEY,JSON.stringify({level:currentLevel,qIndex,correctCount,wrongCount,statuses,wrongIndices,date:Date.now()}));}catch(e){}}
function dismissResume(){try{localStorage.removeItem(RESUME_KEY);}catch(e){}document.getElementById('resume-banner').style.display='none';}
function resumeQuiz(){let saved=null;try{saved=JSON.parse(localStorage.getItem(RESUME_KEY));}catch(e){}if(!saved)return;currentLevel=saved.level;questions=currentLevel==='easy'?[...EASY_Q]:currentLevel==='medium'?[...MEDIUM_Q]:[...HARD_Q];qIndex=saved.qIndex;correctCount=saved.correctCount;wrongCount=saved.wrongCount;statuses=saved.statuses||questions.map(()=>'pending');wrongIndices=saved.wrongIndices||[];document.getElementById('resume-banner').style.display='none';document.getElementById('level-card').style.display='none';document.getElementById('quiz-area').style.display='block';showQuestion();}
function showQuestion(){const q=questions[qIndex];updateBadges();document.getElementById('progress-fill').style.width=(qIndex/questions.length)*100+'%';document.getElementById('q-number').textContent=`السؤال ${toArabicNum(qIndex+1)} من ${toArabicNum(questions.length)}`;var __qt=document.getElementById('q-text');__qt.textContent=q.q;if(currentLevel==='hard'){__qt.classList.remove('notranslate');__qt.removeAttribute('translate');}else{__qt.classList.add('notranslate');__qt.setAttribute('translate','no');}const fb=document.getElementById('feedback');fb.style.display='none';fb.className='feedback';const prevBtn=document.getElementById('prev-btn');prevBtn.disabled=(qIndex===0);prevBtn.style.opacity=(qIndex===0)?'0.4':'1';document.getElementById('skip-btn').style.display='';document.getElementById('next-btn').style.display='none';renderDotProgress();const qpn=document.getElementById('quiz-page-nav');if(qpn)qpn.style.display=(qIndex===questions.length-1)?'flex':'none';const zone=document.getElementById('answer-zone');zone.innerHTML='';if(currentLevel==='easy')renderEasy(q,zone);else if(currentLevel==='medium')renderMedium(q,zone);else renderHard(q,zone);}
function renderEasy(q,zone){const div=document.createElement('div');div.className='choices';shuffle(q.choices.map((c,i)=>({text:c,idx:i}))).forEach(opt=>{const btn=document.createElement('button');btn.className='choice-btn';btn.textContent=opt.text;btn.classList.add('notranslate');btn.setAttribute('translate','no');btn.onclick=()=>checkMCQ(opt.idx,q.answer,btn);div.appendChild(btn);});zone.appendChild(div);}
function renderMedium(q,zone){const ta=document.createElement('textarea');ta.className='answer-input';ta.placeholder='اكتب الكلمة الناقصة...';ta.id='user-input';zone.appendChild(ta);const sub=document.createElement('button');sub.className='submit-btn';sub.textContent='تحقق ✓';sub.onclick=()=>checkText(q);zone.appendChild(sub);setTimeout(()=>{const el=document.getElementById('user-input');if(el)el.focus();},100);}
function renderHard(q,zone){
  const ayahNum=document.createElement('div');ayahNum.style.cssText='text-align:center;font-size:13px;color:var(--text-soft);margin-bottom:8px;';ayahNum.textContent=`الآية ${toArabicNum(q.ayah)}`;zone.appendChild(ayahNum);
  const modeRow=document.createElement('div');modeRow.style.cssText='display:flex;gap:10px;margin-bottom:12px;';
  const bVoice=document.createElement('button');bVoice.textContent='🎤 تسجيل صوتي';bVoice.style.cssText='flex:1;padding:11px;border-radius:11px;font-size:15px;font-family:inherit;cursor:pointer;background:var(--accent);color:#fff;border:1.5px solid var(--accent);';
  const bText=document.createElement('button');bText.textContent='⌨️ كتابة';bText.style.cssText='flex:1;padding:11px;border-radius:11px;font-size:15px;font-family:inherit;cursor:pointer;background:var(--surface2);color:var(--text);border:1.5px solid var(--border);';
  modeRow.appendChild(bVoice);modeRow.appendChild(bText);zone.appendChild(modeRow);
  const vZone=document.createElement('div');zone.appendChild(vZone);
  const tZone=document.createElement('div');tZone.style.display='none';zone.appendChild(tZone);
  let _rec=null,_recog=false,_words=[],_cur='';
  const _SpeechAPI=window.SpeechRecognition||window.webkitSpeechRecognition;
  const _secure=location.protocol==='https:'||location.hostname==='localhost';
  const recBtn=document.createElement('button');recBtn.style.cssText='width:100%;padding:14px;border-radius:12px;font-size:16px;font-family:inherit;cursor:pointer;border:2px solid var(--border);background:var(--surface2);color:var(--text);margin-bottom:8px;';recBtn.textContent='🎤 اضغط للتسجيل';
  const txBox=document.createElement('div');txBox.className='rec-transcript';
  const clrBtn=document.createElement('button');clrBtn.style.cssText='width:100%;padding:9px;border-radius:10px;font-size:14px;font-family:inherit;cursor:pointer;border:1.5px solid var(--wrong-border);background:var(--wrong-bg);color:var(--wrong-text);margin-bottom:8px;display:none;';clrBtn.textContent='🗑️ مسح الكل والبدء من جديد';
  const vSub=document.createElement('button');vSub.className='submit-btn';vSub.textContent='تحقق ✓';vSub.style.display='none';
  vZone.appendChild(recBtn);vZone.appendChild(txBox);vZone.appendChild(clrBtn);vZone.appendChild(vSub);
  function _fixWords(words){
        const out=[];
        for(let i=0;i<words.length;i++){
          if(i<words.length-2 && normalize(words[i])==='او' && normalize(words[i+1])==='كل' && normalize(words[i+2])==='ما'){
            out.push(words[i]+words[i+1]+words[i+2]);i+=2;continue;
          }
          if(i<words.length-1 && normalize(words[i])==='او' && normalize(words[i+1])==='كلما'){
            out.push(words[i]+words[i+1]);i++;continue;
          }
          if(i<words.length-1 && normalize(words[i])==='ولا' && normalize(words[i+1])==='تجدنهم'){
            out.push('ولتجدنهم');i++;continue;
          }
          if(words[i]==='ممنع'){out.push('ممن','منع');continue;}
          if(words[i]==='بلا'){out.push('بلى');continue;}
          if(words[i]==='بن'){out.push('ابن');continue;}
          out.push(words[i]);
        }
        return out;
      }
      function renderWords(){if(!_words.length&&!_cur){txBox.style.display='none';clrBtn.style.display='none';vSub.style.display='none';return;}txBox.style.display='block';txBox.innerHTML='';_words.forEach((w,i)=>{const span=document.createElement('span');span.className='rec-word';span.style.cssText='background:var(--surface-hover);border-radius:4px;padding:2px 5px;margin:2px;cursor:pointer;';span.textContent=w;span.onclick=()=>{_words.splice(i,1);renderWords();};txBox.appendChild(span);});if(_cur){const cur=document.createElement('span');cur.style.cssText='color:var(--text-soft);font-style:italic;';cur.textContent=' '+_cur;txBox.appendChild(cur);}clrBtn.style.display='block';vSub.style.display=_words.length?'block':'none';}
  function _setB(s){recBtn.disabled=false;if(s==='rec'){recBtn.textContent='⏸ إيقاف التسجيل';recBtn.style.background='#e74c3c';recBtn.style.color='#fff';recBtn.style.borderColor='#e74c3c';}else if(s==='pause'){recBtn.textContent='▶️ استمر في التسجيل';recBtn.style.background='#e67e22';recBtn.style.color='#fff';recBtn.style.borderColor='#e67e22';}else{recBtn.textContent='🎤 اضغط للتسجيل';recBtn.style.background='var(--surface2)';recBtn.style.color='var(--text)';recBtn.style.borderColor='var(--border)';}}
  function _mkRec(){const r=new _SpeechAPI();r.lang='ar-SA';r.continuous=true;r.interimResults=false;r.onstart=()=>{_recog=true;_cur='';_setB('rec');renderWords();};r.onresult=e=>{for(let i=e.resultIndex;i<e.results.length;i++){if(e.results[i].isFinal){_words=_words.concat(e.results[i][0].transcript.trim().split(/\\s+/));_cur='';}}renderWords();};r.onerror=e=>{if(e.error!=='no-speech'&&e.error!=='aborted'){_recog=false;_setB(_words.length?'pause':'idle');}};r.onend=()=>{_recog=false;if(_cur){_words=_fixWords(_words.concat(_cur.trim().split(/\\s+/)));_cur='';}renderWords();_setB(_words.length?'pause':'idle');};return r;}
  clrBtn.onclick=()=>{if(_recog){try{_rec.stop();}catch(e){}_recog=false;}_rec=null;_words=[];_cur='';txBox.innerHTML='';txBox.style.display='none';clrBtn.style.display='none';vSub.style.display='none';_setB('idle');recBtn.disabled=false;};
  vSub.onclick=()=>{const t=_words.join(' ').trim();if(!t)return;vSub.disabled=true;checkTextVal(q,t);setTimeout(()=>{recBtn.disabled=false;vSub.disabled=false;},300);};
  if(_SpeechAPI&&_secure){recBtn.onclick=()=>{if(_recog){_recog=false;try{_rec.stop();}catch(e){}_setB('pause');return;}_rec=_mkRec();try{_rec.start();}catch(e){_setB(_words.length?'pause':'idle');}};}else{recBtn.textContent=_secure?'⚠️ المتصفح لا يدعم التسجيل':'🔒 يعمل على الموقع الرسمي فقط';recBtn.disabled=true;recBtn.style.opacity='0.65';}
  function activateVoice(){vZone.style.display='';tZone.style.display='none';bVoice.style.background='var(--accent)';bVoice.style.color='#fff';bText.style.background='var(--surface2)';bText.style.color='var(--text)';if(_SpeechAPI&&_secure&&!_recog){_rec=_mkRec();try{_rec.start();}catch(e){_setB('idle');}}}
  function activateText(){vZone.style.display='none';tZone.style.display='';bText.style.background='var(--accent)';bText.style.color='#fff';bVoice.style.background='var(--surface2)';bVoice.style.color='var(--text)';if(_recog){try{_rec.stop();}catch(e){}_recog=false;}setTimeout(()=>{const el=document.getElementById('user-input');if(el)el.focus();},100);}
  bVoice.onclick=activateVoice;bText.onclick=activateText;
  const ta2=document.createElement('textarea');ta2.className='answer-input';ta2.placeholder='اكتب الآية كاملة...';ta2.id='user-input';tZone.appendChild(ta2);
  const tSub=document.createElement('button');tSub.className='submit-btn';tSub.textContent='تحقق ✓';tSub.onclick=()=>checkText(q);tZone.appendChild(tSub);
  const hBox=document.createElement('div');hBox.className='hint-box';zone.appendChild(hBox);
  const hBtn=document.createElement('button');hBtn.className='hint-btn';hBtn.textContent='💡 مساعدة (أول 3 كلمات)';hBtn.onclick=()=>{hBox.textContent=q.answer.split(' ').slice(0,3).join(' ')+' ...';hBox.classList.add('notranslate');hBox.setAttribute('translate','no');hBox.style.display='block';hBtn.disabled=true;hBtn.style.opacity='0.5';};zone.appendChild(hBtn);
}
function checkTextVal(q,userVal){const fb=document.getElementById('feedback');document.getElementById('skip-btn').style.display='none';document.getElementById('next-btn').style.display='';if(normalize(userVal)===normalize(q.answer)){correctCount++;statuses[qIndex]='correct';fb.className='feedback correct';fb.innerHTML='✓ أحسنتِ! إجابة صحيحة تماماً 🌟';if(currentLevel==='hard'){const __qi=qIndex;setTimeout(()=>{if(qIndex===__qi)nextQuestion();},1100);}}else{wrongCount++;statuses[qIndex]='wrong';wrongIndices.push(qIndex);fb.className='feedback wrong';fb.innerHTML='✗ الإجابة الصحيحة:<br><span style="font-size:18px;line-height:2.2;direction:rtl;display:block;text-align:right;">'+wordDiff(userVal,q.answer)+'</span>';}fb.style.display='block';updateBadges();renderDotProgress();saveResumeState();}
function checkText(q){const input=document.getElementById('user-input');const userVal=input?input.value.trim():'';if(!userVal)return;if(input)input.disabled=true;document.querySelectorAll('.submit-btn').forEach(s=>s.disabled=true);checkTextVal(q,userVal);}
function checkMCQ(chosen,correct,btn){document.querySelectorAll('.choice-btn').forEach(b=>b.disabled=true);const fb=document.getElementById('feedback');if(chosen===correct){btn.classList.add('correct');correctCount++;statuses[qIndex]='correct';fb.className='feedback correct';fb.textContent='✓ أحسنتِ!';const __qi=qIndex;setTimeout(()=>{if(qIndex===__qi)nextQuestion();},1100);}else{btn.classList.add('wrong');wrongCount++;statuses[qIndex]='wrong';wrongIndices.push(qIndex);document.querySelectorAll('.choice-btn').forEach(b=>{if(b.textContent===questions[qIndex].choices[correct])b.classList.add('correct');});fb.className='feedback wrong';fb.innerHTML='✗ الإجابة الصحيحة: <span class="notranslate" translate="no">'+questions[qIndex].choices[correct]+'</span>';}fb.style.display='block';document.getElementById('skip-btn').style.display='none';document.getElementById('next-btn').style.display='';updateBadges();renderDotProgress();saveResumeState();}
function skipQuestion(){const q=questions[qIndex];const fb=document.getElementById('feedback');if(currentLevel==='easy'){document.querySelectorAll('.choice-btn').forEach(b=>{b.disabled=true;if(b.textContent===q.choices[q.answer])b.classList.add('correct');});fb.className='feedback wrong';fb.innerHTML='⬅ الإجابة الصحيحة: <span class="notranslate" translate="no">'+q.choices[q.answer]+'</span>';}else{const inp=document.getElementById('user-input');if(inp)inp.disabled=true;document.querySelectorAll('.submit-btn').forEach(s=>s.disabled=true);fb.className='feedback wrong';fb.innerHTML=`⬅ الإجابة الصحيحة:<br><span style="font-size:18px;line-height:2" class="notranslate" translate="no">${q.answer}</span>`;}wrongCount++;statuses[qIndex]='wrong';wrongIndices.push(qIndex);fb.style.display='block';updateBadges();document.getElementById('skip-btn').style.display='none';document.getElementById('next-btn').style.display='';}
function prevQuestion(){if(qIndex===0)return;qIndex--;showQuestion();}
function nextQuestion(){qIndex++;if(qIndex>=questions.length)showResult();else showQuestion();}
function showResult(){document.getElementById('quiz-area').style.display='none';document.getElementById('result-area').style.display='block';const pct=Math.round((correctCount/questions.length)*100);document.getElementById('result-score').textContent=`${toArabicNum(correctCount)} / ${toArabicNum(questions.length)} — ${toArabicNum(pct)}%`;let icon,title,msg;if(pct===100){icon='🌟';title='ممتاز! حفظ مثالي';msg='ما شاء الله! أتقنتِ السورة بالكامل';}else if(pct>=80){icon='✨';title='أحسنتِ!';msg='نتيجة رائعة، استمري في المراجعة';}else if(pct>=60){icon='📖';title='جيد';msg='راجعي السورة مرة أخرى وأعيدي الاختبار';}else{icon='🌱';title='تحتاج مراجعة';msg='لا تيأسي، المراجعة المستمرة هي المفتاح';}document.getElementById('result-icon').textContent=icon;document.getElementById('result-title').textContent=title;document.getElementById('result-msg').textContent=msg;document.getElementById('progress-fill').style.width='100%';updateBadges();try{localStorage.removeItem(RESUME_KEY);}catch(e){}const rb=document.getElementById('review-mistakes-btn');if(rb)rb.style.display=(wrongIndices.length>0?'inline-block':'none');if(pct===100)spawnConfetti();}
function returnToLevels(){document.getElementById('quiz-area').style.display='none';document.getElementById('order-area').style.display='none';document.getElementById('level-card').style.display='block';currentLevel=null;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));document.getElementById('start-btn').classList.remove('ready');document.getElementById('total-q').textContent='-';document.getElementById('wrong-badge').innerHTML='&#x6F0; &#x2717;<br>&#x62E;&#x637;&#x623;';document.getElementById('correct-badge').innerHTML='&#x6F0; &#x2713;<br>&#x635;&#x62D;&#x64A;&#x62D;';document.getElementById('qnum-badge').innerHTML='&#x627;&#x644;&#x633;&#x624;&#x627;&#x644; &#x6F1; /<br>-';document.getElementById('progress-fill').style.width='0%';}
function retryQuiz(){document.getElementById('result-area').style.display='none';document.getElementById('level-card').style.display='block';currentLevel=null;document.querySelectorAll('.level-btn').forEach(b=>b.classList.remove('active'));document.getElementById('start-btn').classList.remove('ready');document.getElementById('total-q').textContent='-';document.getElementById('wrong-badge').innerHTML='0 ✗<br>خطأ';document.getElementById('correct-badge').innerHTML='0 ✓<br>صحيح';document.getElementById('qnum-badge').innerHTML='السؤال 1 /<br>-';document.getElementById('progress-fill').style.width='0%';}
let orderPlaced=[],orderCursor=0,orderPoolOrder=[],orderSelected=-1;
function startOrderQuiz(){orderPlaced=new Array(AYAT.length).fill(null);orderCursor=0;orderSelected=-1;orderPoolOrder=AYAT.map((t,idx)=>idx);shuffle(orderPoolOrder);document.getElementById('level-card').style.display='none';document.getElementById('order-area').style.display='block';document.getElementById('order-feedback').style.display='none';document.getElementById('order-reveal').style.display='none';document.getElementById('order-check-btn').style.display='none';const rb=document.getElementById('order-reveal-btn');rb.disabled=false;rb.style.opacity='1';renderOrderQuiz();}
function ayahNumAt(i){return (typeof AYAT_NUMS!=='undefined'&&AYAT_NUMS&&AYAT_NUMS.length===AYAT.length&&AYAT_NUMS[i])?AYAT_NUMS[i]:(i+1);}
function mushafHtml(){return '<div class="mushaf-block notranslate" translate="no">'+AYAT.map((t,i)=>t+' <span class="ayah-end">﴿'+toArabicNum(ayahNumAt(i))+'﴾</span>').join(' ')+'</div>';}
function nextEmptyFrom(start){for(let i=start;i<orderPlaced.length;i++){if(orderPlaced[i]===null)return i;}for(let i=0;i<orderPlaced.length;i++){if(orderPlaced[i]===null)return i;}return -1;}
function renderOrderQuiz(){const slotsDiv=document.getElementById('order-slots');const poolDiv=document.getElementById('order-pool');slotsDiv.innerHTML='';poolDiv.innerHTML='';const filledGrid=document.createElement('div');filledGrid.className='order-filled-grid';const emptyStrip=document.createElement('div');emptyStrip.className='order-empty-strip';orderPlaced.forEach((idx,pos)=>{if(idx===null){const active=(pos===orderCursor);const dot=document.createElement('span');dot.className='order-dot'+(active?' active':'');dot.textContent='﴿'+toArabicNum(pos+1)+'﴾';dot.title=active?'الخانة النشطة الآن':'اضغط للمتابعة من هنا';dot.onclick=()=>{orderCursor=pos;renderOrderQuiz();};emptyStrip.appendChild(dot);}else{const card=document.createElement('div');card.className='order-slot filled'+(pos===orderSelected?' order-slot-selected':'');card.setAttribute('translate','no');card.innerHTML='<span class="order-badge">﴿'+toArabicNum(pos+1)+'﴾</span><span class="notranslate">'+AYAT[idx]+'</span>';card.onclick=(e)=>{if(e.target.closest('.order-badge')){if(orderSelected===pos){orderSelected=-1;renderOrderQuiz();return;}if(orderSelected===-1){orderSelected=pos;renderOrderQuiz();return;}const tmp=orderPlaced[orderSelected];orderPlaced[orderSelected]=orderPlaced[pos];orderPlaced[pos]=tmp;orderSelected=-1;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();return;}orderPlaced[pos]=null;orderCursor=pos;orderSelected=-1;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};filledGrid.appendChild(card);}});if(filledGrid.children.length)slotsDiv.appendChild(filledGrid);if(emptyStrip.children.length)slotsDiv.appendChild(emptyStrip);orderPoolOrder.forEach(idx=>{if(orderPlaced.includes(idx))return;const btn=document.createElement('button');btn.className='order-item notranslate';btn.setAttribute('translate','no');btn.textContent=AYAT[idx];btn.onclick=()=>{if(orderCursor===-1||orderPlaced[orderCursor]!==null){orderCursor=nextEmptyFrom(0);}if(orderCursor===-1)return;orderPlaced[orderCursor]=idx;orderCursor=nextEmptyFrom(orderCursor+1);document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};poolDiv.appendChild(btn);});const allFilled=!orderPlaced.includes(null);document.getElementById('order-check-btn').style.display=allFilled?'block':'none';}
function checkOrderAnswer(){let correct=0;document.querySelectorAll('#order-slots .order-slot').forEach((el,pos)=>{const ok=(orderPlaced[pos]!==null&&AYAT[orderPlaced[pos]]===AYAT[pos]);if(ok)correct++;el.classList.remove('correct-slot','wrong-slot');el.classList.add(ok?'correct-slot':'wrong-slot');});const fb=document.getElementById('order-feedback');const allCorrect=(correct===AYAT.length);fb.className='feedback '+(allCorrect?'correct':'wrong');fb.innerHTML='<div style="margin-bottom:8px;">'+toArabicNum(correct)+' / '+toArabicNum(AYAT.length)+' في الترتيب الصحيح'+(allCorrect?' 🌟':'')+'</div>'+(allCorrect?'':'<div style="font-size:14px;margin-bottom:4px;">الترتيب الصحيح للمراجعة:</div>'+mushafHtml());fb.style.display='block';document.getElementById('order-check-btn').style.display='none';if(allCorrect)spawnConfetti();}
function revealOrderAnswer(){document.getElementById('order-reveal').innerHTML=mushafHtml();document.getElementById('order-reveal').style.display='block';const rb=document.getElementById('order-reveal-btn');rb.disabled=true;rb.style.opacity='0.5';}
function shareApp(){var url=location.href;var t=document.title||'دربي لحفظ القرآن';if(navigator.share){navigator.share({title:t,url:url}).catch(function(){});}else if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){var b=document.getElementById('tools-fab-btn');if(b){var old=b.textContent;b.textContent='✅';setTimeout(function(){b.textContent=old;},1800);}}).catch(function(){});}}
function applyTheme(mode){document.documentElement.setAttribute('data-theme',mode);document.getElementById('theme-toggle').textContent=mode==='dark'?'☀️':'🌙';}
function toggleTheme(){const cur=document.documentElement.getAttribute('data-theme');const next=cur==='dark'?'light':'dark';applyTheme(next);try{localStorage.setItem('quranTheme',next);}catch(e){}}
(function initTheme(){let saved=null;try{saved=localStorage.getItem('quranTheme');}catch(e){}if(!saved)saved=(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';applyTheme(saved);})();
let reviewQuestions=[],reviewIdx=0;
function startReview(){reviewQuestions=wrongIndices.map(i=>questions[i]);reviewIdx=0;if(!reviewQuestions.length)return;document.getElementById('result-area').style.display='none';document.getElementById('review-area').style.display='block';renderReviewQ();}
function renderReviewQ(){const q=reviewQuestions[reviewIdx];document.getElementById('review-number').textContent=`مراجعة ${toArabicNum(reviewIdx+1)} من ${toArabicNum(reviewQuestions.length)}`;var __rqt=document.getElementById('review-q-text');__rqt.textContent=q.q;if(currentLevel==='hard'){__rqt.classList.remove('notranslate');__rqt.removeAttribute('translate');}else{__rqt.classList.add('notranslate');__rqt.setAttribute('translate','no');}document.getElementById('review-answer').textContent='✓ '+((currentLevel==='easy')?q.choices[q.answer]:q.answer);}
function reviewNav(dir){reviewIdx=Math.max(0,Math.min(reviewQuestions.length-1,reviewIdx+dir));renderReviewQ();}
function endReview(){document.getElementById('review-area').style.display='none';document.getElementById('result-area').style.display='block';}
function spawnConfetti(){const colors=['#4a7c4a','#c4a84a','#9db89d','#e0edd8','#7a9a7a'];const container=document.getElementById('confetti-container');if(!container)return;container.innerHTML='';container.style.display='block';for(let i=0;i<45;i++){const piece=document.createElement('div');piece.className='confetti-piece';piece.style.left=Math.random()*100+'vw';piece.style.background=colors[Math.floor(Math.random()*colors.length)];piece.style.animationDuration=(2+Math.random()*1.5)+'s';piece.style.animationDelay=(Math.random()*0.4)+'s';container.appendChild(piece);}setTimeout(()=>{container.style.display='none';container.innerHTML='';},4000);}
(function enableSwipe(){const area=document.getElementById('quiz-area');if(!area)return;let startX=0,startY=0;area.addEventListener('touchstart',e=>{startX=e.touches[0].clientX;startY=e.touches[0].clientY;},{passive:true});area.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-startX;const dy=e.changedTouches[0].clientY-startY;if(Math.abs(dx)<60||Math.abs(dx)<Math.abs(dy))return;const nextBtn=document.getElementById('next-btn');if(dx<0&&nextBtn&&nextBtn.style.display!=='none'){nextQuestion();}else if(dx>0){prevQuestion();}},{passive:true});})();
(function checkResumeOnLoad(){let saved=null;try{saved=JSON.parse(localStorage.getItem(RESUME_KEY));}catch(e){}if(saved&&saved.qIndex>0){document.getElementById('resume-banner').style.display='block';}})();
</script>
<script>
if('serviceWorker' in navigator){
  window.addEventListener('load',()=>{
    navigator.serviceWorker.register('service-worker.js')
      .then(r=>console.log('SW:',r.scope))
      .catch(e=>console.log('SW err:',e));
  });
}
</script>
<style>
.tools-fab{position:fixed;top:14px;left:14px;z-index:9990;display:inline-flex;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;}
.tools-fab-btn{display:flex;align-items:center;justify-content:center;background:var(--green3,var(--surface2,#EAF2EA));color:var(--green,var(--accent,#2E6B3E));border:1px solid var(--border,#E4EAE4);border-radius:50%;width:34px;height:34px;font-size:1rem;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.15);}
.tools-fab-btn:hover{filter:brightness(1.05);}
.tools-menu{display:none;position:absolute;top:calc(100% + 8px);left:0;max-width:min(240px,calc(100vw - 24px));background:var(--card,#fff);border:1.5px solid var(--border,#E4EAE4);border-radius:14px;box-shadow:0 6px 20px rgba(0,0,0,0.18);overflow:hidden;min-width:195px;border-top:3px solid #C4A84A;z-index:9998;}
.tools-fab.open .tools-menu{display:block;}
.tools-item{display:flex;align-items:center;gap:8px;width:100%;background:none;border:none;padding:12px 14px;font-size:0.88rem;color:var(--text,#1A1A1A);cursor:pointer;text-align:right;font-family:inherit;}
.tools-item:hover{background:var(--green3,var(--surface2,#F0F7F2));}
.tools-item .tools-lang-inline{margin-inline-start:auto;display:flex;align-items:center;gap:4px;}
.tools-item .tools-lang-inline span:first-child{font-size:1em;color:inherit;}
.tools-item .tools-arrow{font-size:0.75em;color:#B8963A;transition:transform .2s;}
.tools-item svg{flex-shrink:0;}
.tools-lang-list{display:none;border-top:1px solid var(--border,#E4EAE4);background:var(--bg,#F7FAF7);}
.tools-lang-list.open{display:block;}
.tools-lang-list button{display:flex;align-items:center;gap:8px;width:100%;background:none;border:none;padding:10px 14px 10px 22px;font-size:0.82rem;color:var(--text,#1A1A1A);cursor:pointer;text-align:right;font-family:inherit;}
.tools-lang-list button:hover{background:var(--green3,var(--surface2,#F0F7F2));}
.tools-lang-list button.lang-active{font-weight:700;}
.tools-lang-list button .lang-check{margin-inline-start:auto;color:var(--green,#2E6B3E);font-weight:700;visibility:hidden;}
.tools-lang-list button.lang-active .lang-check{visibility:visible;}
#google_translate_element{display:none !important;}
.goog-te-banner-frame.skiptranslate{display:none !important;}
.goog-te-gadget{height:0;overflow:hidden;}
body{top:0 !important;}
.fdbk-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:10000;align-items:center;justify-content:center;padding:16px;}
.fdbk-overlay.open{display:flex;}
.fdbk-modal{background:#fff;border-radius:14px;max-width:380px;width:100%;padding:20px;border-top:4px solid #C4A84A;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;direction:rtl;text-align:right;}
html[data-theme="dark"] .fdbk-modal{background:#182018;color:#DCF0D8;}
.fdbk-modal h3{margin:0 0 12px;color:#2E6B3E;font-size:1.15rem;}
html[data-theme="dark"] .fdbk-modal h3{color:#6BBF5A;}
.fdbk-modal label{display:block;font-size:14px;margin:12px 0 6px;}
.fdbk-modal select,.fdbk-modal textarea{width:100%;padding:9px;border-radius:8px;border:1px solid #d8e0d8;background:#f7faf7;color:#222;font-family:inherit;font-size:14px;box-sizing:border-box;}
html[data-theme="dark"] .fdbk-modal select,html[data-theme="dark"] .fdbk-modal textarea{background:#101810;color:#DCF0D8;border-color:#2A4028;}
.fdbk-modal textarea{min-height:80px;resize:vertical;}
.fdbk-actions{display:flex;gap:8px;margin-top:16px;}
.fdbk-actions button{flex:1;padding:10px;border-radius:8px;border:none;font-size:14px;cursor:pointer;font-family:inherit;}
.fdbk-send{background:#2E6B3E;color:#fff;}
html[data-theme="dark"] .fdbk-send{background:#4A9E40;}
.fdbk-cancel{background:none;border:1px solid #d8e0d8;color:inherit;}
.qr-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.55);z-index:10001;align-items:center;justify-content:center;padding:16px;}
.qr-overlay.open{display:flex;}
.qr-modal{background:var(--card,#fff);border:1px solid var(--border,#E4EAE4);border-radius:18px;padding:22px;max-width:320px;width:100%;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,0.2);border-top:4px solid #C4A84A;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;}
.qr-title{font-size:1.05rem;color:#2E6B3E;font-weight:700;margin-bottom:14px;}
html[data-theme="dark"] .qr-title{color:#6BBF5A;}
.qr-img{border-radius:12px;border:1px solid var(--border,#E4EAE4);background:#fff;padding:8px;}
.qr-caption{font-size:0.8rem;color:var(--text,#1A1A1A);margin-top:12px;line-height:1.6;}
.qr-caption .qr-caption-en{direction:ltr;display:inline-block;font-size:0.72em;color:var(--soft,#888);margin-top:2px;}
.qr-url{font-size:0.72rem;color:var(--soft,#888);margin-top:8px;direction:ltr;word-break:break-all;}
.qr-actions{display:flex;gap:8px;margin-top:16px;}
.qr-actions button{flex:1;padding:10px;border-radius:10px;font-size:0.85rem;font-family:inherit;cursor:pointer;}
.qr-copy-btn{background:#2E6B3E;color:#fff;border:none;}
html[data-theme="dark"] .qr-copy-btn{background:#4A9E40;}
.qr-close-btn{background:none;border:1px solid var(--border,#E4EAE4);color:var(--text,#1A1A1A);}
</style>
<div class="fdbk-overlay" id="fdbk-overlay">
  <div class="fdbk-modal">
    <h3>💬 شاركنا رأيك</h3>
    <label>نوع الملاحظة</label>
    <select id="fdbk-type">
      <option>خطأ في النص القرآني</option>
      <option>خطأ في السؤال أو الإجابة</option>
      <option>مشكلة في التسجيل الصوتي</option>
      <option>مشكلة تصميم أو عرض</option>
      <option>اقتراح تحسين</option>
      <option>أخرى</option>
    </select>
    <label>تفاصيل الملاحظة (اختياري)</label>
    <textarea id="fdbk-note" placeholder="اكتب ملاحظتك هنا..."></textarea>
    <div class="fdbk-actions">
      <button class="fdbk-send" onclick="fdbkSend()">إرسال عبر واتساب</button>
      <button class="fdbk-cancel" onclick="fdbkClose()">إلغاء</button>
    </div>
  </div>
</div>
<div class="qr-overlay" id="qr-overlay" onclick="if(event.target===this)closeQR()">
  <div class="qr-modal">
    <div class="qr-title">🔲 امسح الكود لفتح الصفحة</div>
    <img class="qr-img" id="qr-img" src="" alt="QR كود لفتح هذه الصفحة على الموبايل" width="260" height="260" loading="lazy">
    <div class="qr-caption">امسح الكود لفتح الموقع على موبايلك<br><span class="qr-caption-en">Scan to open Quran Darbi</span></div>
    <div class="qr-url notranslate" translate="no" id="qr-url-text"></div>
    <div class="qr-actions">
      <button class="qr-copy-btn" onclick="copyQRLink()" id="qr-copy-btn">📋 نسخ الرابط</button>
      <button class="qr-close-btn" onclick="closeQR()">إغلاق</button>
    </div>
  </div>
</div>
<div id="google_translate_element"></div>
<script>
function googleTranslateElementInit(){
  new google.translate.TranslateElement({pageLanguage:'ar',includedLanguages:'en,fr,tr,fa,de,es',autoDisplay:false},'google_translate_element');
}
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit" async></script>
<script>
function toolsToggle(e){if(e)e.stopPropagation();document.getElementById('tools-fab').classList.toggle('open');}
function toolsClose(){document.getElementById('tools-fab').classList.remove('open');var l=document.getElementById('tools-lang-list');if(l)l.classList.remove('open');}
function toolsLangToggle(e){if(e)e.stopPropagation();var l=document.getElementById('tools-lang-list');var a=document.getElementById('tools-lang-arrow');l.classList.toggle('open');a.style.transform=l.classList.contains('open')?'rotate(180deg)':'rotate(0)';}
document.addEventListener('click',function(e){var w=document.getElementById('tools-fab');if(w&&!w.contains(e.target))toolsClose();});
function fdbkOpen(){toolsClose();document.getElementById('fdbk-overlay').classList.add('open');}
function fdbkClose(){document.getElementById('fdbk-overlay').classList.remove('open');}
function fdbkSend(){
  var type=document.getElementById('fdbk-type').value;
  var note=document.getElementById('fdbk-note').value.trim();
  var page=document.title||location.pathname.split('/').pop();
  var msg='ملاحظة من دربي لحفظ القرآن\\nالصفحة: '+page+'\\nالنوع: '+type+(note?'\\nالتفاصيل: '+note:'');
  window.open('https://wa.me/201034365326?text='+encodeURIComponent(msg),'_blank');
  fdbkClose();
}
function showQR(){
  var url=location.href;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&margin=10&data='+encodeURIComponent(url);
  document.getElementById('qr-url-text').textContent=url.replace(/^https?:\\/\\//,'');
  document.getElementById('qr-overlay').classList.add('open');
}
function closeQR(){document.getElementById('qr-overlay').classList.remove('open');}
function copyQRLink(){
  var url=location.href;
  var b=document.getElementById('qr-copy-btn');
  navigator.clipboard.writeText(url).then(function(){b.textContent='✅ تم النسخ';setTimeout(function(){b.textContent='📋 نسخ الرابط';},2000);}).catch(function(){b.textContent='تعذر النسخ';setTimeout(function(){b.textContent='📋 نسخ الرابط';},2000);});
}
function langCookie(){var m=document.cookie.match(/googtrans=([^;]+)/);return m?decodeURIComponent(m[1]):'';}
function langApplyLabel(){
  var map={ar:'العربية',en:'English',fr:'Français',tr:'Türkçe',fa:'فارسی',de:'Deutsch',es:'Español'};
  var c=langCookie();var code='ar';
  if(c){var parts=c.split('/');if(parts[2])code=parts[2];}
  var cur=document.getElementById('tools-lang-cur');
  if(cur)cur.textContent=map[code]||map.ar;
  document.querySelectorAll('#tools-lang-list button').forEach(function(b){b.classList.toggle('lang-active',b.dataset.code===code);});
}
function langSelect(code){
  if(code==='ar'){
    document.cookie='googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie='googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.'+location.hostname+';';
  }else{
    document.cookie='googtrans=/ar/'+code+'; path=/;';
  }
  location.reload();
}
langApplyLabel();
</script>
</body>
</html>
"""


# ====================================================
# ترحيل صفحات البقرة لقالب جزء عمّ النضيف (يوليو ٢٠٢٦):
#    كل صفحات البقرة القديمة اتبنت بقالبين مختلفين ومباشر عليهم
#    رقعات (patches) متراكمة على مر الوقت — ده اللي سبب باگات زي
#    زرار الترتيب اللي مش بيتحقن صح في بعض الصفحات. الحل الجذري:
#    إعادة بناء كل صفحة بقرة بنفس قالب جزء عمّ النظيف (نفس البنية،
#    نفس الدوال، بدون تراكم رقعات).
#
#    القاعدة المطلقة اللي الدالة دي بتلتزم بيها بدون أي استثناء:
#    نص EASY_Q وMEDIUM_Q وHARD_Q بينُسخ حرفيًا 100% من الملف القديم
#    زي ما هو — صفر إعادة صياغة، صفر تخمين. الدالة بتعمل self-check
#    بمقارنة حرفية كاملة قبل ما تقبل التغيير؛ لو في أي فرق ولو حرف
#    واحد، الترحيل بيتلغى تلقائيًا ويتسجل الملف في تقرير المراجعة
#    اليدوية بدل ما يترفع تغيير مش متأكد منه.
# ====================================================

BAQARA_MIGRATION_SKIPPED = []

def _baqara_extract_page_meta(old):
    m_surah = re.search(r'<div class="surah-title">([^<]+)</div>', old)
    m_range = re.search(r'<div class="ayat-range">([^<]+)</div>', old)
    m_info  = re.search(r'<div class="page-info">([^<]+)</div>', old)
    m_prev  = re.search(r'class="prev-page-btn"[^>]*href="([^"]+)"', old) \
              or re.search(r'href="([^"]+)"\s+class="prev-page-btn"', old)
    m_next  = re.search(r'class="next-page-btn"[^>]*href="([^"]+)"', old) \
              or re.search(r'href="([^"]+)"\s+class="next-page-btn"', old)
    m_title = re.search(r'<title>([^<]+)</title>', old)
    m_pageid = re.search(r"const PAGE_ID\s*=\s*'([^']+)'", old)
    return {
        'surah': m_surah.group(1) if m_surah else 'سورة البقرة',
        'range': m_range.group(1) if m_range else '',
        'info': m_info.group(1) if m_info else '',
        'prev': m_prev.group(1) if m_prev else '',
        'next': m_next.group(1) if m_next else '',
        'title': m_title.group(1) if m_title else '',
        'pageid': m_pageid.group(1) if m_pageid else '',
    }

def _baqara_parse_ayat_range(range_str):
    m = re.search(r'(\d+)\s*إلى\s*(\d+)', range_str)
    if not m:
        return None, None
    return int(m.group(1)), int(m.group(2))

def _baqara_js_str(s):
    return json.dumps(s, ensure_ascii=False)

def _baqara_get_array_body(text, name):
    m = re.search(r'const\s+' + name + r'\s*=\s*\[(.*?)\n\];', text, re.S)
    return m.group(1) if m else None

def _baqara_verify_migration(old, new):
    """مقارنة حرفية 100% — بترجع True بس لو كل نص قرآني مطابق تمامًا."""
    def gab(text, name):
        m = re.search(r'const\s+' + name + r'\s*=\s*\[(.*?)\n\];', text, re.S)
        return m.group(1) if m else ''

    easy_pat = re.compile(r'\{\s*q:\s*"((?:[^"\\]|\\.)*)"\s*,\s*choices:\s*\[((?:[^\]]*))\]\s*,\s*answer:\s*(\d)\s*\}')
    qa_pat = re.compile(r'\{\s*q:\s*"((?:[^"\\]|\\.)*)"\s*,\s*answer:\s*"((?:[^"\\]|\\.)*)"\s*(?:,\s*hint:\s*"(?:[^"\\]|\\.)*"\s*)?\}')
    hard_pat_new = re.compile(r'\{ayah:\d+,q:"((?:[^"\\]|\\.)*)",answer:"((?:[^"\\]|\\.)*)"\}')

    old_e = easy_pat.findall(gab(old, 'EASY_Q'))
    new_e = easy_pat.findall(gab(new, 'EASY_Q'))
    old_m = qa_pat.findall(gab(old, 'MEDIUM_Q'))
    new_m = qa_pat.findall(gab(new, 'MEDIUM_Q'))

    old_hard_body = gab(old, 'HARD_Q')
    old_ayat_body = gab(old, 'AYAT')
    old_ayat_texts = re.findall(r'text:\s*"((?:[^"\\]|\\.)*)"', old_ayat_body) if old_ayat_body else []
    old_hard_literal = qa_pat.findall(old_hard_body)
    old_hard_ayatref = re.findall(r'\{\s*q:\s*"((?:[^"\\]|\\.)*)"\s*,\s*answer:\s*AYAT\[(\d+)\]\.text\s*\}', old_hard_body)
    if old_hard_literal:
        old_h_answers = [a for q, a in old_hard_literal]
    elif old_hard_ayatref:
        old_h_answers = [old_ayat_texts[int(i)] for q, i in old_hard_ayatref]
    else:
        old_h_answers = []
    new_h_answers = [a for q, a in hard_pat_new.findall(gab(new, 'HARD_Q'))]

    return (old_e == new_e) and (old_m == new_m) and (old_h_answers == new_h_answers) and len(new_h_answers) > 0

def _baqara_parts_fit(parts, full):
    """بيتأكد إن إجابات HARD_Q الخاصة بآية واحدة مشروعة، من غير أي نص
    غريب. حالتان مقبولتان بس:
      (1) مقاطع متتابعة بتعيد تركيب الآية حرفيًا لما تتلزق بمسافة
          (زي 'بداية الآية' + 'نهاية الآية' في p9 وp49)
      (2) سؤال بالآية الكاملة + أسئلة إضافية كل واحدة نصّها جزء حرفي
          من نفس الآية (زي p42: الآية 253 كاملة + سؤال على بدايتها)
    أي حاجة تانية بترجع False والصفحة بتتخطّى للمراجعة اليدوية."""
    if ' '.join(parts) == full:
        return True
    return (full in parts) and all(p in full for p in parts)


def _baqara_hard_ayah_numbers(hard_pairs):
    """يستخرج رقم الآية الحقيقي من نص كل سؤال في HARD_Q.
    بيتعامل مع الصيغتين الموجودتين في القالب القديم:
        'اكتب الآية رقم N من سورة البقرة كاملة'
        'اكتب بداية/نهاية الآية N من «...»'
    يرجّع None لو أي سؤال مافيهوش رقم آية واضح — وساعتها الملف
    بيتخطّى زي الأول بدل ما نخمّن."""
    nums = []
    for q, ans in hard_pairs:
        m = re.search(r'الآي[ةه]\s*(?:رقم\s*)?(\d+)', q)
        if not m:
            return None
        nums.append(int(m.group(1)))
    return nums


def migrate_baqara_to_clean_template(path, out):
    """يحوّل صفحة بقرة من القالب القديم (بقالبيه المختلفين) لقالب جزء
    عمّ النضيف. بيتأكد أولًا إن النص القرآني بعد التحويل مطابق حرفيًا
    100% للنص قبل التحويل، وإلا الملف بيتسجل للمراجعة اليدوية ومفيش
    أي تعديل بيتطبق."""
    fn = os.path.splitext(os.path.basename(path))[0]
    if not fn.startswith('albaqara_'):
        return out, False

    # علامة إن الملف اتحول بالفعل — الصيغة الجديدة فيها {ayah: جوه HARD_Q
    if '{ayah:' in out:
        return out, False

    meta = _baqara_extract_page_meta(out)
    easy_body = _baqara_get_array_body(out, 'EASY_Q')
    med_body  = _baqara_get_array_body(out, 'MEDIUM_Q')
    hard_body = _baqara_get_array_body(out, 'HARD_Q')
    ayat_body = _baqara_get_array_body(out, 'AYAT')

    if easy_body is None or med_body is None or hard_body is None:
        BAQARA_MIGRATION_SKIPPED.append(f'{os.path.basename(path)} (EASY_Q/MEDIUM_Q/HARD_Q غير موجودة أو صيغة غير معروفة)')
        return out, False

    start, end = _baqara_parse_ayat_range(meta['range'])
    expected = (end - start + 1) if (start and end) else None

    hard_items_literal = re.findall(
        r'\{\s*q:\s*"((?:[^"\\]|\\.)*)"\s*,\s*answer:\s*"((?:[^"\\]|\\.)*)"\s*(?:,\s*hint:\s*"(?:[^"\\]|\\.)*"\s*)?\}', hard_body
    )
    hard_items_ayatref = re.findall(
        r'\{\s*q:\s*"((?:[^"\\]|\\.)*)"\s*,\s*answer:\s*AYAT\[(\d+)\]\.text\s*\}', hard_body
    )
    ayat_texts = re.findall(r'text:\s*"((?:[^"\\]|\\.)*)"', ayat_body) if ayat_body else []

    if hard_items_literal:
        hard_pairs = hard_items_literal
    elif hard_items_ayatref and ayat_texts:
        hard_pairs = [(q, ayat_texts[int(idx)]) for q, idx in hard_items_ayatref]
    else:
        BAQARA_MIGRATION_SKIPPED.append(f'{os.path.basename(path)} (صيغة HARD_Q غير مدعومة)')
        return out, False

    # آيات الصفحة الحقيقية: من AYAT بصيغة {num,text} لو موجودة، وإلا من
    # ORDER_AYAT (مصفوفة مسطّحة بترتيب الصفحة). لازمة عشان الترتيب وعرض
    # المصحف يفضلوا على عدد الآيات الحقيقي مش عدد أسئلة الصعب.
    ayat_by_num = {
        int(n): t for n, t in re.findall(
            r'\{\s*num:\s*(\d+)\s*,\s*text:\s*"((?:[^"\\]|\\.)*)"\s*\}', ayat_body
        )
    } if ayat_body else {}
    if not ayat_by_num and expected:
        m_ord = re.search(r'const\s+ORDER_AYAT\s*=\s*\[(.*?)\n\];', out, re.S)
        if m_ord:
            ord_texts = re.findall(r'"((?:[^"\\]|\\.)*)"', m_ord.group(1))
            if len(ord_texts) == expected:
                ayat_by_num = {start + k: t for k, t in enumerate(ord_texts)}

    seg_nums = None
    if expected is not None and len(hard_pairs) != expected:
        # عدد أسئلة الصعب مش مساوي لعدد الآيات. ده ليه سببين مشروعين:
        #   (1) آية طويلة متقسّمة لمقاطع (بداية/نهاية) — زي p9 وp49
        #   (2) سؤال إضافي على جزء من آية جنب سؤال الآية الكاملة — زي p42
        # الاتنين مقبولين بشرطين: كل آيات الصفحة مغطّاة بالظبط، وكل
        # إجابة في HARD_Q جزء حرفي من نص آيتها (مفيش نص غريب أبدًا).
        ok_seg = False
        reason = None
        nums = None
        if len(hard_pairs) < expected:
            reason = (f'HARD_Q غير مكتملة: {len(hard_pairs)}/{expected} — '
                      f'لازم تكمّل الآيات الناقصة من صور المصحف الأول')
        else:
            nums = _baqara_hard_ayah_numbers(hard_pairs)
            if nums is None:
                bad = [q[:45] for q, a in hard_pairs
                       if not re.search(r'الآي[ةه]\s*(?:رقم\s*)?(\d+)', q)]
                reason = ('مش لاقي رقم آية صريح في نص السؤال — '
                          f'أول سؤال من غير رقم: «{bad[0] if bad else "؟"}»')
            elif sorted(set(nums)) != list(range(start, end + 1)):
                reason = (f'الآيات المغطّاة {sorted(set(nums))} مش مطابقة '
                          f'لنطاق الصفحة {start}-{end}')
            elif not set(nums) <= set(ayat_by_num):
                miss = sorted(set(nums) - set(ayat_by_num))
                reason = ('مفيش AYAT بصيغة {num,text} ولا ORDER_AYAT بطول '
                          f'الصفحة — آيات ناقصة: {miss}')
            else:
                bad_num = [
                    num for num in sorted(set(nums))
                    if not _baqara_parts_fit(
                        [a for (q, a), n in zip(hard_pairs, nums) if n == num],
                        ayat_by_num[num])
                ]
                if bad_num:
                    reason = (f'في إجابة عن آية {bad_num[0]} نصّها مش جزء حرفي '
                              'من الآية — محتاجة مراجعة يدوية بصورة المصحف')
                else:
                    ok_seg = True
        if not ok_seg:
            BAQARA_MIGRATION_SKIPPED.append(
                f'{os.path.basename(path)} ({len(hard_pairs)}/{expected} — {reason})'
            )
            return out, False
        seg_nums = nums
    elif expected is not None:
        # العدد مظبوط — بس نتأكد إن أرقام الآيات المكتوبة جوه الأسئلة
        # نفسها مغطّية نطاق الصفحة، عشان مايتحطش رقم آية غلط.
        # (لو الأسئلة مافيهاش أرقام صريحة بنسيب السلوك القديم زي ما هو.)
        nums = _baqara_hard_ayah_numbers(hard_pairs)
        if nums is not None and sorted(nums) != list(range(start, end + 1)):
            BAQARA_MIGRATION_SKIPPED.append(
                f'{os.path.basename(path)} (أرقام آيات HARD_Q مش مطابقة لنطاق الصفحة: '
                f'{nums} مقابل {start}-{end} — محتاجة مراجعة يدوية)'
            )
            return out, False
        if nums is not None and nums != list(range(start, end + 1)):
            seg_nums = nums          # نفس الأرقام بترتيب مختلف — نسيبها زي ما هي

    if seg_nums is not None:
        ayah_numbers = seg_nums
    else:
        ayah_numbers = list(range(start, end + 1)) if expected else list(range(1, len(hard_pairs) + 1))

    hard_js = "[\n" + ",\n".join(
        "  {ayah:%d,q:%s,answer:%s}" % (a, _baqara_js_str(q), _baqara_js_str(ans))
        for a, (q, ans) in zip(ayah_numbers, hard_pairs)
    ) + "\n]"
    if seg_nums is not None:
        ordered = sorted(set(seg_nums))
        if set(ordered) <= set(ayat_by_num):
            ayat_list = [ayat_by_num[n] for n in ordered]
        else:
            # مفيش مصدر مستقل للآيات — هنا كل آية ليها سؤال واحد بالظبط
            # (فرع العدد المتساوي)، فبناخد إجابته ونرتّبها برقم الآية.
            byn = dict(zip(seg_nums, [a for q, a in hard_pairs]))
            ayat_list = [byn[n] for n in ordered]
    else:
        ayat_list = [ans for q, ans in hard_pairs]
    ayat_js = "[\n" + ",\n".join("  " + _baqara_js_str(a) for a in ayat_list) + "\n]"

    # أرقام الآيات الحقيقية من المصحف — بتتخزّن جنب النص عشان عرض
    # المصحف في مستوى الترتيب مايعتمدش على ترتيب الآية في المصفوفة.
    if seg_nums is not None:
        ayat_nums = sorted(set(seg_nums))
    elif expected:
        ayat_nums = list(range(start, end + 1))
    else:
        ayat_nums = list(range(1, len(ayat_list) + 1))
    ayat_nums_js = "[" + ",".join(str(n) for n in ayat_nums) + "]"

    new_out = BAQARA_CLEAN_TEMPLATE
    new_out = new_out.replace('__TITLE__', meta['title'] or f"اختبار حفظ {meta['surah']}")
    new_out = new_out.replace('__SURAH_TITLE__', meta['surah'])
    new_out = new_out.replace('__AYAT_RANGE__', meta['range'])
    new_out = new_out.replace('__PAGE_INFO__', meta['info'])
    new_out = new_out.replace('__PREV_PAGE__', meta['prev'])
    new_out = new_out.replace('__NEXT_PAGE__', meta['next'])
    new_out = new_out.replace('__RESUME_KEY__', f"quranResume_{meta['pageid']}" if meta['pageid'] else f"quranResume_{fn}")
    new_out = new_out.replace('__AYAT_JSON__', ayat_js)
    new_out = new_out.replace('__AYAT_NUMS_JSON__', ayat_nums_js)
    new_out = new_out.replace('__EASY_Q_JSON__', "[\n" + easy_body.strip() + "\n]")
    new_out = new_out.replace('__MEDIUM_Q_JSON__', "[\n" + med_body.strip() + "\n]")
    new_out = new_out.replace('__HARD_Q_JSON__', hard_js)

    # ===== self-check: لازم تطابق حرفي 100% قبل قبول التحويل =====
    if not _baqara_verify_migration(out, new_out):
        BAQARA_MIGRATION_SKIPPED.append(f'{os.path.basename(path)} (فشل التحقق الحرفي بعد الترحيل — لم يُطبَّق أي تغيير)')
        return out, False

    return new_out, True


BAQARA_AYAHNUM_FIXED = []
BAQARA_AYAHNUM_SKIPPED = []

_MUSHAF_OLD_FN = (
    'function mushafHtml(){return \'<div class="mushaf-block notranslate" translate="no">\''
    '+AYAT.map((t,i)=>t+\' <span class="ayah-end">﴿\'+toArabicNum(i+1)+\'﴾</span>\').join(\' \')+\'</div>\';}'
)
_AYAHNUM_HELPER = (
    "function ayahNumAt(i){return (typeof AYAT_NUMS!=='undefined'&&AYAT_NUMS&&"
    "AYAT_NUMS.length===AYAT.length&&AYAT_NUMS[i])?AYAT_NUMS[i]:(i+1);}\n"
)
_MUSHAF_NEW_FN = _AYAHNUM_HELPER + (
    'function mushafHtml(){return \'<div class="mushaf-block notranslate" translate="no">\''
    '+AYAT.map((t,i)=>t+\' <span class="ayah-end">﴿\'+toArabicNum(ayahNumAt(i))+\'﴾</span>\').join(\' \')+\'</div>\';}'
)


def fix_baqara_mushaf_ayah_numbers(path, out):
    """صفحات البقرة اللي اتحوّلت للقالب النضيف كانت بتعرض رقم الآية في
    مستوى الترتيب على إنه ترتيبها جوه المصفوفة (١، ٢، ٣...) بدل رقمها
    الحقيقي في المصحف (٥٨، ٥٩، ٦٠...). الدالة الأصلية اتكتبت لسور جزء
    عمّ — وهناك i+1 صح لأن كل سورة بتبدأ من آية ١ — لكنها اتورّثت
    لقالب البقرة اللي صفحاته بتبدأ من نُص السورة.

    الحل: نخزّن الأرقام الحقيقية في AYAT_NUMS ونخلّي العرض يقراها.
    النص القرآني نفسه مابيتلمسش خالص — الرقم اللي جوه ﴿﴾ بس."""
    fn = os.path.basename(path)
    if not fn.startswith('albaqara_'):
        return out, False          # جزء عمّ سليم — i+1 هناك هو الرقم الصح

    on_clean_template = (_MUSHAF_OLD_FN in out) or ('function ayahNumAt(' in out)
    if not on_clean_template:
        return out, False          # لسه على القالب القديم — مش شغل الدالة دي

    body, _st, en = _t_array_body(out, 'AYAT')
    if body is None:
        return out, False
    n_ayat = len(_T_STR.findall(body))

    changed = False
    if 'const AYAT_NUMS=' not in out:
        m = re.search(r'<div class="ayat-range">[^<]*?الآيات\s*(\d+)\s*إلى\s*(\d+)', out)
        if m:
            nums = list(range(int(m.group(1)), int(m.group(2)) + 1))
        else:
            m1 = re.search(r'<div class="ayat-range">[^<]*?الآية\s*(\d+)', out)
            nums = [int(m1.group(1))] if m1 else None
        if not nums or n_ayat == 0 or len(nums) != n_ayat:
            rng = f'{nums[0]}-{nums[-1]} ({len(nums)} آية)' if nums else 'مش لاقي نطاق في ayat-range'
            BAQARA_AYAHNUM_SKIPPED.append(
                f'{fn} (AYAT فيها {n_ayat} آية | النطاق المكتوب: {rng} — محتاجة مراجعة يدوية)'
            )
            return out, False
        semi = out.find(';', en)
        if semi == -1 or semi > en + 2:
            BAQARA_AYAHNUM_SKIPPED.append(f'{fn} (مش لاقي نهاية تعريف AYAT)')
            return out, False
        out = (out[:semi + 1]
               + '\nconst AYAT_NUMS=[' + ','.join(str(x) for x in nums) + '];'
               + out[semi + 1:])
        changed = True

    if _MUSHAF_OLD_FN in out:
        out = out.replace(_MUSHAF_OLD_FN, _MUSHAF_NEW_FN, 1)
        changed = True

    if changed:
        BAQARA_AYAHNUM_FIXED.append(fn)
    return out, changed


def add_open_tanween_to_normalize(out):
    """رسم التنوين في المصحف بيفرّق بين ثلاث حالات، ولكل واحدة كود مختلف:
        إظهار (متراكب)        → U+064B / U+064C / U+064D
        إدغام وإخفاء (متتابع) → U+08F0 / U+08F1 / U+08F2
        إقلاب                 → حركة مفردة + U+06E2 (فوق) أو U+06ED (تحت)
    النطاق 08F0–08F2 في بلوك Arabic Extended-A، وميم الإقلاب 06E2/06ED
    برّه نطاقات حذف التشكيل القديمة. لو النص القرآني اتكتب بيهم من غير
    التعديل ده، العلامة هتفضل بعد التطبيع وكل إجابة صحيحة هتتحسب خطأ.

    الإصلاح idempotent وبيلمس كلاس حذف التشكيل بس — مش بيغيّر أي قاعدة
    تطبيع تانية ولا يمسّ نص قرآني. بيتعامل مع الصيغتين: Unicode escapes
    (ملفات السور) وأحرف حرفية (recitation.html وملفات الجيل القديم).
    """
    changed = False

    # 1. صيغة Unicode escapes
    old_esc = r"[\u064B-\u065F\u0610-\u061A\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]"
    new_esc = r"[\u064B-\u065F\u0610-\u061A\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED\u08F0-\u08F2]"
    if old_esc in out:
        out = out.replace(old_esc, new_esc)
        changed = True

    # 2. صيغة الأحرف الحرفية — بتقبل '' و "" (ملفات زي albaqara_p47 بتستخدم "")
    pat = re.compile(r"""(replace\(/\[)([^\]]*)(\]/g,\s*(?:''|""))""")
    NEEDED = '\u08F0\u08F1\u08F2\u06E2\u06ED'

    def _add(m):
        cls = m.group(2)
        if '\u064B' not in cls or '\u0652' not in cls:
            return m.group(0)              # مش كلاس التشكيل الرئيسي (قاعدة الكشيدة مثلاً)
        add = ''.join(c for c in NEEDED if c not in cls)
        if not add:
            return m.group(0)
        return m.group(1) + cls + add + m.group(3)

    out2 = pat.sub(_add, out)
    if out2 != out:
        out = out2
        changed = True

    return out, changed


# ======================================================
# رسم التنوين — محرك سياقي (يوليو ٢٠٢٦)
# ------------------------------------------------------
# حكم التنوين بيتحدد من أول حرف في الكلمة *التالية*، مش من
# الكلمة نفسها. فخريطة "كلمة → بديل" غلط أصلاً: نفس الكلمة
# ممكن تيجي مرتين في نفس الصفحة بحكمين مختلفين، زي:
#     البلد ٥:  عَلَيۡهِ أَحَدٌ يَقُولُ   → (ي) متتابع
#     البلد ٧:  يَرَهُۥٓ  أَحَدٌ أَلَمۡ    → (أ) متراكب
# عشان كده كل كلمة بتتحسب من سياقها هي، ولو الكلمة التالية
# مش ظاهرة (قبل فراغ _____) بيرجع لـAYAT بالكلمة السابقة.
#
# الخوارزمية متحقَّق منها ضد ٩٩٥ حالة في recitation.html
# المصحح يدويًا من صور المصحف: تطابق ٩٩٤/٩٩٥.
# ======================================================
_T_OPEN  = {'F': '\u08F0', 'D': '\u08F1', 'K': '\u08F2'}   # متتابع: إدغام + إخفاء
_T_STACK = {'F': '\u064B', 'D': '\u064C', 'K': '\u064D'}   # متراكب: إظهار
_T_WRONG = {'\u0657': 'F', '\u065E': 'D', '\u0656': 'K'}   # هاكات خط KFGQPC — بترسم غلط في Amiri
_T_HARAKA = {'F': '\u064E', 'D': '\u064F', 'K': '\u0650'}
_T_MHI, _T_MLO = '\u06E2', '\u06ED'                        # ميم الإقلاب: فوق / تحت
_T_IZHAR = set('ءأإآؤئهعحغخ')                              # حروف الحلق
_T_DIAC = re.compile('[\u064B-\u065F\u0670\u06D6-\u06ED\u08F0-\u08F3\u0640]')
_T_AR = re.compile('[\u0621-\u064A]')
_T_PUNCT = '«»/—-·|,.…"'
_T_STR = re.compile(r'"((?:[^"\\]|\\.)*)"')

TANWEEN_SKIPPED = []
TANWEEN_UNRESOLVED = []
_BAQARA_FIRST_WORD = {}


def _t_bare(w):
    return _T_DIAC.sub('', w)


def _t_clean(t):
    return t.strip(_T_PUNCT)


def _t_is_word(t):
    t = _t_clean(t)
    return bool(t) and '_' not in t and bool(_T_AR.search(t))


def _t_rule(next_bare, at_surah_end):
    """الحكم من أول حرف في الكلمة التالية. الترتيب مهم: ألف الوصل تغلب اللام."""
    if at_surah_end:
        return 'IQLAB'                       # البسملة بعدها بتبدأ بباء
    if not next_bare:
        return None
    c = next_bare[0]
    if c == '\u0671':
        return 'STACK'                       # تنوين قبل ألف وصل = إظهار (التقاء الساكنين)
    if c == '\u0628':
        return 'IQLAB'
    if c in _T_IZHAR:
        return 'STACK'
    return 'OPEN'


def _t_find(w):
    """يرجّع (موضع, نوع, نوع الحركة) لتنوين آخر الكلمة، أو None."""
    for i in range(len(w) - 1, -1, -1):
        c = w[i]
        if c in (_T_MHI, _T_MLO):
            if (w[i + 1] if i + 1 < len(w) else '') == '\u0628':
                continue                     # نۢب داخلية (أنۢبِيَآء) — مش تنوين
            return (i, 'IQLAB', 'K' if c == _T_MLO else None)
        if c in _T_WRONG:
            return (i, 'OPEN', _T_WRONG[c])
        for h, ch in _T_OPEN.items():
            if c == ch:
                return (i, 'OPEN', h)
        for h, ch in _T_STACK.items():
            if c == ch:
                return (i, 'STACK', h)
    return None


def _t_rebuild(w, idx, kind, hk, target):
    if target == kind and not any(c in _T_WRONG for c in w):
        return w
    if kind == 'IQLAB':
        base = w[:idx] + w[idx + 1:]
        m = re.search('([\u064E\u064F\u0650])(\u0627?)$', base)
        if not m:
            return None
        h = {'\u064E': 'F', '\u064F': 'D', '\u0650': 'K'}[m.group(1)]
        return base[:m.start()] + (_T_OPEN if target == 'OPEN' else _T_STACK)[h] + m.group(2)
    if target in ('OPEN', 'STACK'):
        return w[:idx] + (_T_OPEN if target == 'OPEN' else _T_STACK)[hk] + w[idx + 1:]
    meem = _T_MLO if hk == 'K' else _T_MHI
    return w[:idx] + _T_HARAKA[hk] + meem + w[idx + 1:]


def _t_key(w):
    """مفتاح محايد للتنوين — عشان البحث في AYAT ينجح قبل التصحيح وبعده."""
    r = _t_find(w)
    if not r:
        return w
    return w[:r[0]] + w[r[0] + 1:]


def _t_skel(w):
    """هيكل الكلمة من غير أي تشكيل — بيتخطّى اختلاف الرسم بين المصفوفات.
    بعض الملفات AYAT بتاعتها متحقونة من AYAT_DATA وبتستخدم السكون العادي
    U+0652، بينما الأسئلة في نفس الملف بتستخدم U+06E1. من غير المفتاح ده
    البحث بيفشل وكلمات قرآنية حقيقية بتفضل بالكود القديم."""
    w = _T_DIAC.sub('', w)
    w = re.sub('[\u0622\u0623\u0625\u0671]', '\u0627', w)
    return w.replace('\u0649', '\u064A').replace('\u0629', '\u0647')


class _TanweenPage:
    def __init__(self, words, tail_next_word):
        self.ws = words
        self.tail = tail_next_word           # أول كلمة في الصفحة التالية، أو None = آخر السورة
        self.after, self.byword, self.byskel, self.afterskel = {}, {}, {}, {}
        self.pos_by_key, self.pos_by_skel = {}, {}
        for n, w in enumerate(words):
            nxt = words[n + 1] if n + 1 < len(words) else tail_next_word
            prev = _t_key(words[n - 1]) if n > 0 else None
            pskel = _t_skel(words[n - 1]) if n > 0 else None
            self.pos_by_key.setdefault(_t_key(w), []).append(n)
            self.pos_by_skel.setdefault(_t_skel(w), []).append(n)
            self.after.setdefault((prev, _t_key(w)), set()).add(nxt)
            self.byword.setdefault(_t_key(w), set()).add(nxt)
            self.byskel.setdefault(_t_skel(w), set()).add(nxt)
            self.afterskel.setdefault((pskel, _t_skel(w)), set()).add(nxt)

    def _longest_ctx(self, w, prevs):
        """أطول سياق يساري مطابق.

        بعض الكلمات بتتكرر في نفس السورة بحكمين مختلفين وسياقها القريب
        واحد. مثال الشرح: «فَإِنَّ مَعَ ٱلۡعُسۡرِ يُسۡرًا» و«إِنَّ مَعَ ٱلۡعُسۡرِ
        يُسۡرًا» — الكلمتين السابقتين متطابقتين والفرق في التالتة. فبنقارن
        أطول سياق متاح وناخد الموضع صاحب أطول تطابق.
        """
        cand = self.pos_by_key.get(_t_key(w)) or self.pos_by_skel.get(_t_skel(w))
        if not cand or len(cand) < 2 or not prevs:
            return None
        pk = [(_t_key(x) if x else None) for x in prevs]
        ps = [(_t_skel(x) if x else None) for x in prevs]
        best, score = [], 0
        for n in cand:
            d = 0
            while d < len(pk) and n - 1 - d >= 0:
                a = self.ws[n - 1 - d]
                if (pk[-1 - d] is None                       # فراغ = أي كلمة
                        or _t_key(a) == pk[-1 - d]
                        or _t_skel(a) == ps[-1 - d]):
                    d += 1
                else:
                    break
            if d > score:
                best, score = [n], d
            elif d == score:
                best.append(n)
        if score == 0 or len(best) != 1:
            return None
        n = best[0]
        return self.ws[n + 1] if n + 1 < len(self.ws) else self.tail

    def want(self, w, nextword, prevs):
        """الكلمة التالية لو ظاهرة، وإلا بحث متدرّج في AYAT.

        كل مصدر بيتجرّب لوحده: لو أدّى إجابة واحدة نرجّعها، ولو ملتبس
        نكمّل للمصدر اللي بعده. المستويات بالهيكل المجرّد بتتخطّى اختلاف
        الرسم بين AYAT والأسئلة (ْ U+0652 مقابل ۡ U+06E1).
        """
        if nextword is not None:
            return _t_rule(_t_bare(_t_clean(nextword)), False)
        if isinstance(prevs, str) or prevs is None:
            prevs = [prevs] if prevs else []
        prevword = next((x for x in reversed(prevs) if x), None)
        kw, sk = _t_key(w), _t_skel(w)
        pk = _t_key(prevword) if prevword else None
        ps = _t_skel(prevword) if prevword else None

        def _pref(idx, k, gap):
            hits = [v for k2, v in idx.items()
                    if k2.endswith(k) and 0 < len(k2) - len(k) <= gap]
            return hits[0] if len(hits) == 1 else None

        lc = self._longest_ctx(w, prevs)
        for cands in ({lc} if lc is not None else None,
                      self.after.get((pk, kw)),
                      self.afterskel.get((ps, sk)),
                      self.byword.get(kw),
                      self.byskel.get(sk),
                      _pref(self.byword, kw, 6),
                      _pref(self.byskel, sk, 3)):
            if not cands:
                continue
            outs = {(_t_rule(_t_bare(c), False) if c is not None else 'IQLAB')
                    for c in cands}
            outs.discard(None)
            if len(outs) == 1:
                return outs.pop()
        return None

def _t_fix_tokens(tokens, page, tail_next, tail_prev, unresolved):
    out = list(tokens)
    for i, t in enumerate(tokens):
        w = _t_clean(t)
        r = _t_find(w)
        if not r:
            continue
        nxt = None
        for j in range(i + 1, len(tokens)):
            if '_' in tokens[j]:
                break
            if _t_is_word(tokens[j]):
                nxt = _t_clean(tokens[j])
                break
        if nxt is None:
            nxt = tail_next
        prevs = [(None if '_' in t2 else _t_clean(t2))
                 for t2 in tokens[:i] if _t_is_word(t2) or '_' in t2]
        if not prevs and tail_prev:
            prevs = tail_prev if isinstance(tail_prev, list) else [tail_prev]
        elif tail_prev and isinstance(tail_prev, list):
            prevs = tail_prev + prevs
        target = page.want(w, nxt, prevs)
        if target is None:
            if any(c in _T_WRONG for c in w):
                unresolved.append(w)
            continue
        nw = _t_rebuild(w, r[0], r[1], r[2], target)
        if nw and nw != w:
            out[i] = t.replace(w, nw)
    return out


def _t_split_q(q):
    """سياق الفراغ — من جوّه «» بس. التعليقات بره (— آية ٢٢٦) مش نص قرآني."""
    m = re.search(r'«([^»]*)»', q)
    if m:
        q = m.group(1)
    toks = q.split()
    for i, t in enumerate(toks):
        if '_' in t:
            return ([_t_clean(x) for x in toks[:i] if _t_is_word(x)],
                    next((_t_clean(x) for x in toks[i + 1:] if _t_is_word(x)), None))
    return ([_t_clean(x) for x in toks if _t_is_word(x)], None)


def _t_array_body(text, name):
    """قصّ محتوى مصفوفة JS بمطابقة الأقواس — بيشتغل مع الصيغتين المضغوطة والمتباعدة."""
    m = re.search(r'const\s+' + name + r'\s*=\s*\[', text)
    if not m:
        return None, None, None
    st = text.index('[', m.start())
    d, q, j = 0, None, st
    while j < len(text):
        c = text[j]
        if q:
            if c == '\\':
                j += 2
                continue
            if c == q:
                q = None
        elif c in '"\'`':
            q = c
        elif c == '[':
            d += 1
        elif c == ']':
            d -= 1
            if d == 0:
                j += 1
                break
        j += 1
    return text[st:j], st, j


def _t_ayat_words(out):
    """كلمات AYAT بالترتيب. بيقبل صيغة النص المجرّد وصيغة {num,text}."""
    for name in ('AYAT', 'ORDER_AYAT'):
        body, _, _ = _t_array_body(out, name)
        if not body:
            continue
        strs = [s for s in _T_STR.findall(body) if _T_AR.search(s)]
        if strs:
            return ' '.join(strs).split()
    return None


def _t_load_baqara_first_words(root):
    """أول كلمة في كل صفحة بقرة — لازمة لحكم آخر كلمة في الصفحة اللي قبلها."""
    if _BAQARA_FIRST_WORD:
        return
    for fn in os.listdir(root):
        m = re.match(r'albaqara_p(\d+)\.html$', fn)
        if not m:
            continue
        try:
            with open(os.path.join(root, fn), encoding='utf-8') as f:
                ws = _t_ayat_words(f.read())
            if ws:
                _BAQARA_FIRST_WORD[int(m.group(1))] = ws[0]
        except Exception:
            pass


def fix_tanween_rasm(path, out):
    """تصحيح رسم التنوين في AYAT وEASY_Q وMEDIUM_Q وHARD_Q وORDER_AYAT.

    idempotent: التصحيح محسوب من القاعدة مش من الحالة الحالية، فتشغيله
    مرتين بيدّي نفس النتيجة. لا يمس أي حرف — علامة التنوين بس، فالتطبيع
    قبل وبعد بيفضل متطابق ١٠٠٪.
    """
    fn = os.path.basename(path)
    words = _t_ayat_words(out)
    if not words:
        TANWEEN_SKIPPED.append(fn + ' (مفيش AYAT/ORDER_AYAT)')
        return out, False

    # آخر كلمة في صفحة البقرة حكمها من أول كلمة في الصفحة اللي بعدها
    tail = None
    m = re.match(r'albaqara_p(\d+)\.html$', fn)
    if m:
        _t_load_baqara_first_words(os.path.dirname(os.path.abspath(path)))
        tail = _BAQARA_FIRST_WORD.get(int(m.group(1)) + 1)
        if tail is None and (int(m.group(1)) + 1) <= 49:
            TANWEEN_SKIPPED.append(fn + ' (الصفحة التالية مش متاحة — آخر كلمة اتساب)')
    page = _TanweenPage(words, tail)

    lines = out.split('\n')
    idxs = [i for i, l in enumerate(lines)
            if re.search(r'const\s+(AYAT|EASY_Q|MEDIUM_Q|HARD_Q|ORDER_AYAT)\s*=', l)]
    if not idxs:
        TANWEEN_SKIPPED.append(fn + ' (مفيش مصفوفات أسئلة)')
        return out, False
    lo = min(idxs)
    j = max(idxs)
    while j < len(lines) and not re.match(r'^\s*\];\s*$', lines[j]):
        j += 1
    hi = min(j, len(lines) - 1)

    unresolved = []
    for li in range(lo, hi + 1):
        line = lines[li]
        if not _T_AR.search(line):
            continue
        qm = re.search(r'q\s*:\s*"((?:[^"\\]|\\.)*)"', line)
        tail_ctx = _t_split_q(qm.group(1)) if qm else (None, None)

        def _one(mm, _qm=qm, _tc=tail_ctx):
            s = mm.group(1)
            if not _T_AR.search(s):
                return mm.group(0)
            is_q = _qm is not None and s == _qm.group(1)
            tn, tp = (None, None) if is_q else (_tc[1], _tc[0])
            return '"' + ' '.join(_t_fix_tokens(s.split(), page, tn, tp, unresolved)) + '"'

        lines[li] = _T_STR.sub(_one, line)

    # توحيد شكل تنوين المشتتات المخترَعة — الإجابة الصح مالهاش تبقى مميزة
    # شكليًا. أي اختيار موجود في AYAT = نص قرآني ويُترك على حكمه الصحيح.
    corrected = ' ' + ' '.join(
        ' '.join(_t_fix_tokens(a.split(), page, None, None, []))
        for a in [' '.join(words)]) + ' '
    corrected_skel = ' ' + ' '.join(_t_skel(x) for x in corrected.split()) + ' '

    def _unify(mm):
        items = re.findall(r'"([^"]*)"', mm.group(1))
        if len(items) < 2:
            return mm.group(0)
        tgt = None
        for it in items:
            for w in it.split():
                r = _t_find(w)
                if r and not any(c in _T_WRONG for c in w):
                    tgt = r[1]
                    break
            if tgt:
                break
        if not tgt:
            return mm.group(0)
        new = []
        for it in items:
            it_s = ' ' + ' '.join(_t_skel(x) for x in it.split()) + ' '
            if it.strip() and ((' ' + it.strip() + ' ') in corrected
                               or it_s.strip() and it_s in corrected_skel):
                new.append(it)                 # نص قرآني — لا يُمسّ
                continue
            ws = []
            for w in it.split():
                r = _t_find(w)
                if r:
                    nw = _t_rebuild(w, r[0], r[1], r[2], tgt)
                    if nw:
                        w = nw
                ws.append(w)
            new.append(' '.join(ws))
        return 'choices:[' + ','.join('"%s"' % x for x in new) + ']'

    for li in range(lo, hi + 1):
        lines[li] = re.sub(r'choices:\s*\[([^\]]*)\]', _unify, lines[li])

    if unresolved:
        TANWEEN_UNRESOLVED.append((fn, sorted(set(unresolved))))
    new_out = '\n'.join(lines)
    return new_out, new_out != out


_U_ARRAYS = ('AYAT', 'ORDER_AYAT', 'EASY_Q', 'MEDIUM_Q', 'HARD_Q')

# (اسم القاعدة, بصمة وجودها في الكود, الحالة اللي تخلّيها لازمة في النص)
# (اسم القاعدة, حروف لازم تظهر كلها جوه *نفس* الـreplace,
#  بديل مطلوب أو None, الحالة اللي تخلّي السورة محتاجاها)
# ملحوظة: القواعد بتتكتب كفئات حروف زي [ىی]ٰ فالحرفين مش
# متلاصقين — عشان كده الفحص بيتم على محتوى كل replace على حدة
# مش بالبحث في النص الخام (ده كان بيدّي إنذارات كاذبة).
_U_RULES = [
    ('١ كشيدة',  ['\u0640'],           None,     '\u0640'),
    ('٣ هؤلاء',  [],                    'هالا',   'ه[ؤو]لا|ها[ؤو]لا'),
    ('٤ وٱ وصل', ['\u0648', '\u0671'], None,     '\u0648\u0671'),
    ('٥ وٰ→وا',  ['\u0648', '\u0670'], None,     '\u0648\u0670'),
    ('٦ يٰ→يا',  ['\u064A', '\u0670'], 'يا',     '\u064A\u0670'),
    ('٧ ىٰ',     ['\u0649', '\u0670'], None,     '\u0649\u0670'),
    ('٩ ۥ/ۦ',    ['\u06E5'],           None,     '\u06E5'),
    ('٩ ۦ',      ['\u06E6'],           None,     '\u06E6'),
    ('١٠ ئؤ→ا',  ['\u0626'],           None,     '\u0626|\u0624'),
    ('١١ رحمان', ['رحمان'],             None,     'رَّحۡمَٰن|رَحۡمَٰن|رحمٰن|رَّحْمَٰن'),
    ('١٣ اولئك', [],                    'اولاك',  'ولَٰٓئِك|أولئك|أُوْلَٰٓئِك'),
]

_U_REPL = re.compile(r"\.replace\(\s*/((?:[^/\\\n]|\\.)+)/[a-z]*\s*,\s*(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")")


def _u_rule_present(body, chars, repl):
    """القاعدة موجودة لو فيه replace واحد بيحقق الشرطين."""
    for m in _U_REPL.finditer(body):
        pat = m.group(1)
        rep = m.group(2) if m.group(2) is not None else (m.group(3) or '')
        if chars and not all(ch in pat for ch in chars):
            continue
        if repl is not None and repl not in rep:
            continue
        return True
    return False



# كائنات النص القرآني في recitation.html — قيمها مكتوبة بـbackticks
# مش بعلامات تنصيص، وبتتعرّف كـ{} مش []، فـ_t_array_body و_T_STR
# مابيشوفوهاش. من غير الإضافة دي بصمة recitation.html كانت بصمة نص
# فاضي، يعني كل دالة محروسة بالبصمة بتشتغل عليه بدون أي حماية.
_U_OBJECTS = ('TEXTS', 'AYAHS', 'AYAH_START')
_T_TPL = re.compile(r'`((?:[^`\\]|\\.)*)`', re.S)
_T_NUM = re.compile(r':\s*(\d+)')


def _t_object_body(text, name):
    """قصّ محتوى كائن JS بمطابقة الأقواس {} — نظير _t_array_body."""
    m = re.search(r'(?:const|let|var)\s+' + name + r'\s*=\s*\{', text)
    if not m:
        return None, None, None
    st = text.index('{', m.start())
    d, q, j = 0, None, st
    while j < len(text):
        c = text[j]
        if q:
            if c == '\\':
                j += 2
                continue
            if c == q:
                q = None
        elif c in '"\'`':
            q = c
        elif c == '{':
            d += 1
        elif c == '}':
            d -= 1
            if d == 0:
                j += 1
                break
        j += 1
    return text[st:j], st, j


def quran_text_fingerprint(html):
    """بصمة كل النص القرآني — أي خطوة توحيد لازم تسيبها زي ما هي."""
    parts = []
    for name in _U_ARRAYS:
        body, _, _ = _t_array_body(html, name)
        if body:
            parts.append(name + '\x00' + '\x01'.join(_T_STR.findall(body)))
    # إضافة بحتة: ملفات الاختبار مافيهاش الكائنات دي، فبصمتها
    # بتفضل بنفس القيمة بالحرف — والتلاوة بتكسب حماية حقيقية
    for name in _U_OBJECTS:
        body, _, _ = _t_object_body(html, name)
        if body:
            vals = _T_STR.findall(body) + _T_TPL.findall(body)
            if not vals:
                vals = _T_NUM.findall(body)
            parts.append(name + '\x00' + '\x01'.join(vals))
    return hashlib.md5('\x02'.join(parts).encode('utf-8')).hexdigest()


def _u_quran_text(html):
    out = []
    for name in _U_ARRAYS:
        body, _, _ = _t_array_body(html, name)
        if body:
            out.extend(s for s in _T_STR.findall(body) if _T_AR.search(s))
    return ' '.join(out)


def _u_probe(html, is_rec):
    lines = html.split('\n')
    p = {}
    p['قالب'] = 'مضغوط' if sum(1 for l in lines if len(l) > 400) >= 25 else 'متباعد'
    esc = bool(re.search(r'\\u064B-\\u065F', html))
    lit = bool(re.search(r'replace\(/\[[ًٌٍَُِّْ]', html))
    p['كلاس-التشكيل'] = ('escapes' if esc and not lit else 'حرفي' if lit and not esc
                         else 'الاتنين' if esc and lit else 'غير معروف')
    if is_rec:
        p['دالة-التطبيع'] = 'norm' if 'function norm' in html else 'مفقودة'
    else:
        p['دالة-التطبيع'] = 'normalize' if 'function normalize(str){' in html else 'مفقودة'
        p['nm'] = bool(re.search(r'const\s+nm\s*=', html)) or 'function nm' in html
        p['wordDiff'] = 'function wordDiff' in html
        p['returnToLevels'] = 'returnToLevels' in html
        p['ترتيب'] = bool(re.search(r'const\s+ORDER_AYAT\s*=', html))
        p['AYAT-كائن'] = bool(re.search(r'const\s+AYAT\s*=\s*\[\s*\{\s*num', html))
        p['تنقّل'] = ('⏮️' in html) or ('nav-row' in html)
    p['أدوات'] = 'tools-fab' in html
    p['notranslate'] = html.count('notranslate') > 3

    fname = 'function norm' if is_rec else 'function normalize'
    i = html.find(fname)
    seg = html[i:i + 8000] if i >= 0 else ''
    txt = _u_quran_text(html) if not is_rec else html
    need = []
    for name, chars, repl, trig in _U_RULES:
        if not re.search(trig, txt):
            continue                       # السورة مش محتاجة القاعدة دي
        if not _u_rule_present(seg, chars, repl):
            need.append(name)
    p['_ناقص_ومطلوب'] = need
    a = b = 0
    for nm2 in _U_ARRAYS:
        body, _, _ = _t_array_body(html, nm2)
        if body:
            a += body.count('\u0652'); b += body.count('\u06E1')
    p['سكون'] = 'مختلط' if a and b else ('0652' if a else ('06E1' if b else '—'))
    return p


def audit_uniformity(root):
    """مسح كل ملفات HTML وطباعة خريطة الاختلافات. لا يكتب أي ملف إطلاقًا."""
    files = sorted(f for f in os.listdir(root) if f.endswith('.html'))
    quiz, rec = [], []
    for fn in files:
        if fn == 'index.html':
            continue
        try:
            with open(os.path.join(root, fn), encoding='utf-8') as fh:
                html = fh.read()
        except Exception as e:
            print('  تعذّرت قراءة', fn, e); continue
        isr = (fn == 'recitation.html')
        (rec if isr else quiz).append((fn, _u_probe(html, isr)))

    print('\n=== مسح التوحيد (قراءة فقط — لم يتغيّر أي ملف) ===')
    print('ملفات الاختبارات: %d   |   recitation: %d' % (len(quiz), len(rec)))

    def show(title, key, rows):
        d = {}
        for fn, p in rows:
            if key in p:
                d.setdefault(str(p[key]), []).append(fn)
        if not d:
            return
        print('\n-- %s --' % title)
        for val, fs in sorted(d.items(), key=lambda x: -len(x[1])):
            print('   %-12s : %3d' % (val, len(fs)))
            if len(fs) <= 14:
                print('      ' + ' · '.join(fs))

    for t, k in (('جيل القالب', 'قالب'), ('كلاس حذف التشكيل', 'كلاس-التشكيل'),
                 ('دالة التطبيع', 'دالة-التطبيع'), ('صيغة AYAT', 'AYAT-كائن'),
                 ('السكون في النص', 'سكون')):
        show(t, k, quiz)

    print('\n-- ميزات ناقصة --')
    any_miss = False
    for key in ('nm', 'wordDiff', 'returnToLevels', 'ترتيب', 'تنقّل',
                'أدوات', 'notranslate'):
        miss = [fn for fn, p in quiz if p.get(key) is False]
        if miss:
            any_miss = True
            print('   %-15s ناقصة في %3d' % (key, len(miss)))
            if len(miss) <= 15:
                print('      ' + ' · '.join(miss))
    if not any_miss:
        print('   مفيش ✅')

    print('\n-- قواعد normalize ناقصة *والسورة محتاجاها* --')
    bad = {}
    for fn, p in quiz + rec:
        for r in p.get('_ناقص_ومطلوب', []):
            bad.setdefault(r, []).append(fn)
    if not bad:
        print('   كل الملفات كاملة ✅')
    for r, fs in sorted(bad.items(), key=lambda x: -len(x[1])):
        print('   %-14s ناقصة في %3d ملف' % (r, len(fs)))
        if len(fs) <= 15:
            print('      ' + ' · '.join(fs))
    print('=== نهاية المسح ===\n')


# ======================================================
# توحيد قواعد normalize — إضافات وترتيب فقط، صفر حذف
# ------------------------------------------------------
# أربع مشاكل موثّقة بالاختبار في الملفات القديمة:
#   ١) الكشيدة و ـۧ و ـَٔ بتتعالج *بعد* حذف التشكيل، فقاعدة
#      ـۧ→ي بتموت (U+06E7 بتتحذف مع التشكيل) و"إِبْرَٰهِـۧمَ"
#      بتطلع "ابراهم" بدل "ابراهيم"
#   ٢) قواعد ناقصة: هاذا→هذا · ذالك→ذلك · لاكن→لكن · اولك→اولاك
#   ٣) [ءئؤ]→'' بتحذف ئ و ؤ بدل ما تحوّلهم لألف
#   ٤) (.)()+ بدل (.)\1+ — الـbackreference ضايعة فقاعدة
#      تقليص التكرار بلا فعل
# كلها بتخلّي إجابة صحيحة تتحسب خطأ. لا تمسّ أي نص قرآني.
# ======================================================
NORM_FIXED = []
RECIT_NORM_FIXED = []

_NF_KASHIDA = re.compile(
    r"\.replace\(/ـۧ/g,'ي'\).*?\.replace\(/ـ/g,''\)", re.S)
_NF_TASHKEEL = re.compile(
    r"\.replace\(/\[(?:\\u064B-\\u065F|ً)[^\]]*\]/g,\s*(?:''|\"\")\)")


def _nf_one(body):
    """يصلّح جسم دالة تطبيع واحدة. يرجّع (الجسم الجديد, قائمة الإصلاحات)."""
    done = []

    # ملحوظة: abasa فيها (.)()+ بدل (.)\1+ — الـbackreference ضايعة.
    # بنسيبها مكسورة عن قصد: تصليحها بيبلع واو العطف فتبقى آية ٣٨
    # «وُجُوهࣱ» وآية ٤٠ «وَوُجُوهࣱ» متطابقين عند التصحيح. الحالات اللي
    # كانت محتاجاها اتعالجت بقواعد مستهدفة فوق.

    # ٣) [ءئؤ] → '' يبقى [ئؤ] → ا ثم ء → ''
    #    فيه صيغتين بيعملوا نفس الحذف الغلط:
    #      أ) [ءئؤ] → ''            (الصيغة الصريحة)
    #      ب) [ئؤ] → ء ثم ء → ''    (نفس النتيجة بالظبط، بس متخفية على
    #         خطوتين — الفاحص القديم كان بيعدّي عليها وبيقول "سليمة")
    if r"replace(/[ئؤ]/g,'ء').replace(/ء/g,'')" in body:
        body = body.replace(r"replace(/[ئؤ]/g,'ء').replace(/ء/g,'')",
                            r"replace(/[ئؤ]/g,'ا').replace(/ء/g,'')")
        done.append('ئؤ→ا')
    if r"replace(/[ءئؤ]/g,'')" in body:
        body = body.replace(r"replace(/[ءئؤ]/g,'')",
                            r"replace(/[ئؤ]/g,'ا').replace(/ء/g,'')")
        done.append('ئؤ→ا')

    # ١) نقل كتلة الكشيدة قبل حذف التشكيل
    mk = _NF_KASHIDA.search(body)
    mt = _NF_TASHKEEL.search(body)
    if mk and mt and mt.start() < mk.start():
        blk = mk.group(0)
        body = body[:mk.start()] + body[mk.end():]
        mt = _NF_TASHKEEL.search(body)          # الموضع اتغيّر بعد القص
        body = body[:mt.start()] + blk + body[mt.start():]
        done.append('ترتيب-الكشيدة')

    # ٢) القواعد الناقصة — تتحط بعد ارايت→اريت (آخر السلسلة النصية)
    # ملاحظة: بعض الصيغ فيها ألف زيادة بتتولّد أثناء التطبيع نفسه —
    # الألف الخنجرية بتبقى ألف والهمزة بتبقى ألف، فيطلع ألفين ورا بعض
    # (يَٰٓأَيُّهَا ← ياايها ، أُوْلَٰٓئِكَ ← اولااك). بنعالجها بقواعد مستهدفة
    # مش بتقليص تكرار عام، عشان مانبلعش واو العطف (ووجوه ← وجوه).
    add = []
    for pat, rep, sig in ((r'هاذا', 'هذا', 'هاذا'), (r'ذالك', 'ذلك', 'ذالك'),
                          (r'لاكن', 'لكن', 'لاكن'), (r'اولك', 'اولاك', 'اولك'),
                          (r'اولااك', 'اولاك', 'اولااك'),
                          (r'ياايها', 'يايها', 'ياايها'),
                          (r'ياايتها', 'يايتها', 'ياايتها')):
        if ("/%s/g" % sig) not in body:
            add.append(".replace(/%s/g,'%s')" % (pat, rep))
    if add:
        anchor = r".replace(/ارايت/g,'اريت')"
        if anchor in body:
            body = body.replace(anchor, anchor + ''.join(add), 1)
            done.append('قواعد-ناقصة×%d' % len(add))
        else:
            add = []
    return body, done


def _nf_span(out, head):
    """حدود جسم دالة بمطابقة الأقواس، مع تخطّي النصوص والـregex."""
    i = out.find(head)
    if i < 0:
        return None
    j = out.index('{', i)
    st, d, q = j, 0, None
    while j < len(out):
        c = out[j]
        if q:
            if c == '\\':
                j += 2; continue
            if c == q:
                q = None
        elif c == '/' and out[j - 1] == '(':
            q = '/'
        elif c in '"\'`':
            q = c
        elif c == '{':
            d += 1
        elif c == '}':
            d -= 1
            if d == 0:
                j += 1; break
        j += 1
    return st, j


def unify_normalize_rules(path, out):
    """يطبّق الإصلاحات الأربعة على normalize و nm. idempotent."""
    fn = os.path.basename(path)
    before = quran_text_fingerprint(out)
    allfix = []
    for head in ('function normalize(str){', 'const nm=', 'function nm('):
        sp = _nf_span(out, head)
        if not sp:
            continue
        st, en = sp
        nb, done = _nf_one(out[st:en])
        if done:
            out = out[:st] + nb + out[en:]
            allfix += done
    if not allfix:
        return out, False
    if quran_text_fingerprint(out) != before:      # حارس: مستحيل يحصل
        print('⛔ %s: البصمة اتغيّرت — التعديل اتلغى' % fn)
        return out, False
    NORM_FIXED.append((fn, sorted(set(allfix))))
    return out, True


# ======================================================
# إصلاح expandMuqattaat المفقودة
# ------------------------------------------------------
# wordDiff بتنادي expandMuqattaat لكن الدالة اتنقلت لبعض
# الملفات من غير تعريفها (الموجود اسمه collapseMuqattaat).
# النتيجة: أول ما المستخدم يضغط "تحقق" وإجابته غلط،
# checkText بتقفل كل أزرار .submit-btn الأول وبعدين
# checkTextVal بترمي ReferenceError — فمفيش نتيجة بتظهر
# والزرارين (صوت + كتابة) بيفضلوا مقفولين للأبد.
# التعريف منقول حرفيًا من recitation.html مع تبديل norm
# بـ normalize (اسم الدالة في ملفات الاختبارات).
# ======================================================
MUQ_FIXED = []
MUQ_OK = []

_MUQ_DEF = """function expandMuqattaat(words){
  const out=[];let i=0;
  while(i<words.length&&i<2){
    const key=normalize(words[i]);
    if(MUQATTAAT[key]){out.push(...MUQATTAAT[key]);i++;}
    else break;
  }
  for(;i<words.length;i++)out.push(words[i]);
  return out;
}
"""


def fix_missing_expand_muqattaat(path, out):
    """يضيف expandMuqattaat لو الملف بينادها من غير ما يعرّفها."""
    if 'expandMuqattaat(' not in out:
        return out, False
    if re.search(r'function\s+expandMuqattaat', out):
        MUQ_OK.append(os.path.basename(path))
        return out, False
    if 'MUQATTAAT' not in out:
        MUQ_FIXED.append((os.path.basename(path), 'اتخطّى — MUQATTAAT مش موجودة'))
        return out, False
    anchor = 'function wordDiff'
    i = out.find(anchor)
    if i < 0:
        MUQ_FIXED.append((os.path.basename(path), 'اتخطّى — wordDiff مش موجودة'))
        return out, False
    out = out[:i] + _MUQ_DEF + out[i:]
    MUQ_FIXED.append((os.path.basename(path), 'اتصلحت ✅'))
    return out, True


# ======================================================
# نقل ميزة "تحديد الكلمة" من التلاوة لمستوى الصعب
# ------------------------------------------------------
# في recitation.html: الضغط على كلمة بيحدّدها (مش بيحذفها)،
# ويظهر شريط فيه زر "✕ حذف" — ولو سجّلتِ والكلمة محدّدة،
# التسجيل الجديد بيحلّ محلها *في مكانها* حتى لو وسط النص.
# في ملفات الاختبارات كان الضغط بيحذف على طول من غير خيار.
# القاعدة: أي تحديث في التلاوة يتطبّق على الصعب.
# ======================================================
SELWORD_FIXED = []
SELWORD_ALREADY = []
SELWORD_NOMATCH = []

_SW_OLD_DECL = "let _rec=null,_recog=false,_words=[],_cur='';"
_SW_NEW_DECL = "let _rec=null,_recog=false,_words=[],_cur='',_sel=null;"

_SW_OLD_CLICK = ("span.textContent=w;span.title='انقري للحذف';\n"
                 "      span.onclick=()=>{_words.splice(i,1);renderWords();};")
_SW_NEW_CLICK = """span.textContent=w;
      if(i===_sel){span.style.outline='2px solid var(--gold)';span.style.background='var(--hint-btn-bg)';span.style.fontWeight='700';span.title='اضغطي لإلغاء التحديد';}
      else{span.title='اضغطي لتحديدها ثم سجّلي البديل';}
      span.onclick=()=>{_sel=(_sel===i)?null:i;renderWords();};"""

_SW_BAR = """    if(_sel!==null&&_sel>=_words.length)_sel=null;
    if(_sel!==null){
      const bar=document.createElement('div');
      bar.style.cssText='width:100%;box-sizing:border-box;background:var(--hint-btn-bg);border:1px solid var(--gold);border-radius:8px;padding:6px 10px;margin-bottom:8px;font-size:14px;display:flex;align-items:center;gap:8px;justify-content:space-between;';
      const t=document.createElement('span');
      t.appendChild(document.createTextNode('المحدَّدة: '));
      const b=document.createElement('b');b.className='notranslate';b.setAttribute('translate','no');
      b.textContent=_words[_sel];t.appendChild(b);
      t.appendChild(document.createTextNode(' — سجّلي البديل'));
      const x=document.createElement('button');x.type='button';x.textContent='✕ حذف';
      x.style.cssText='background:var(--wrong-border);color:#fff;border:0;border-radius:6px;padding:3px 10px;font-size:13px;cursor:pointer;font-family:inherit;flex:0 0 auto;';
      x.onclick=()=>{_words.splice(_sel,1);_sel=null;renderWords();};
      bar.appendChild(t);bar.appendChild(x);txBox.appendChild(bar);
    }
"""

# إدخال الكلمات: تحلّ محل المحدَّدة بدل ما تتضاف في الآخر
_SW_ADD = """  function _addWords(nw){
    if(!nw||!nw.length)return;
    nw=_fixWords(nw);
    if(_sel!==null&&_sel<_words.length){_words.splice(_sel,1);_words.splice(_sel,0,...nw);_sel=null;}
    else{_words=_fixWords([].concat(_words,nw));}
  }
"""


def port_selword_feature(path, out):
    """ينقل ميزة تحديد الكلمة من التلاوة لدالة renderHard.

    فيه أكتر من جيل قالب (مضغوط ومتباعد، وبعضها بيستخدم متغيّر
    وسيط للكلمات الجديدة)، فالمطابقة بـregex مرن مش نص حرفي.
    """
    fn = os.path.basename(path)
    if '_sel=null' in out or 'المحدَّدة' in out:
        SELWORD_ALREADY.append(fn)             # اتطبّقت في تشغيلة سابقة
        return out, False
    before = quran_text_fingerprint(out)
    n = 0

    out, c = re.subn(r"let _rec=null,_recog=false,_words=\[\],_cur='';",
                     "let _rec=null,_recog=false,_words=[],_cur='',_sel=null;", out, count=1)
    n += c
    if not c:
        if 'renderHard' in out:
            SELWORD_NOMATCH.append(fn)         # فيه مستوى صعب بس القالب مختلف
        return out, False

    out, c = re.subn(
        r"span\.textContent=w;(?:\s*span\.title='[^']*';)?\s*"
        r"span\.onclick=\(\)=>\{_words\.splice\(i,1\);renderWords\(\);\};",
        lambda m: _SW_NEW_CLICK, out, count=1)
    n += c

    out, c = re.subn(r"(txBox\.style\.display='block';\s*txBox\.innerHTML='';)",
                     lambda m: m.group(1) + '\n' + _SW_BAR, out, count=1)
    n += c


    # التقاط الصوت: بالصيغة المباشرة أو عبر متغيّر وسيط
    out, c = re.subn(
        r"_words=_fixWords\(_words\.concat\(e\.results\[i\]\[0\]\.transcript\.trim\(\)\.split\(/\\s\+/\)\)\);",
        lambda m: "_addWords(e.results[i][0].transcript.trim().split(/\\s+/));", out, count=1)
    n += c
    out, c = re.subn(r"_words=_fixWords\(_words\.concat\((\w+)\)\);",
                     lambda m: '_addWords(%s);' % m.group(1), out, count=1)
    n += c

    out, c = re.subn(r"if\(_cur\)\{_words=_fixWords\(_words\.concat\(_cur\.trim\(\)\.split\(/\\s\+/\)\)\);_cur='';\}",
                     lambda m: "if(_cur){_addWords(_cur.trim().split(/\\s+/));_cur='';}", out, count=1)
    n += c

    # الإدخال لازم يجي *بعد* كل الاستبدالات فوق، وإلا الـregex
    # بتاعة الاحتياطي بتطابق السطر اللي جوه _addWords نفسها
    # وتحوّله لاستدعاء ذاتي لا نهائي (اتكشف على الموقع — يوليو ٢٠٢٦)
    out, c = re.subn(r"(\n\s*)function renderWords\(\)\{",
                     lambda m: m.group(1) + _SW_ADD + m.group(1) + 'function renderWords(){',
                     out, count=1)
    n += c
    out = re.sub(r"_rec=null;_words=\[\];_cur='';", "_rec=null;_words=[];_cur='';_sel=null;", out, count=1)

    if quran_text_fingerprint(out) != before:
        print('⛔ %s: البصمة اتغيّرت — التعديل اتلغى' % fn)
        return out, False
    SELWORD_FIXED.append((fn, n))
    return out, True

# ======================================================
# رسم التنوين في recitation.html
# ------------------------------------------------------
# بنية مختلفة عن ملفات الاختبارات: TEXTS قاموس بنصوص
# backtick، ودالة التطبيع اسمها norm، وصفحات البقرة الـ48
# كلها جوّه الملف الواحد فالربط بينها داخلي.
# ======================================================
REC_TANWEEN = []
_REC_ENTRY = re.compile(r'(\w+)(\s*:\s*`)([^`]*)(`)')


def fix_tanween_recitation(path, out):
    i = out.find('const TEXTS')
    if i < 0:
        return out, False
    j = out.find('const AYAH_START', i)
    if j < 0:
        j = len(out)
    block = out[i:j]
    texts = {m.group(1): m.group(3) for m in _REC_ENTRY.finditer(block)}
    if not texts:
        return out, False

    def tail_for(key):
        m = re.match(r'baqara_p(\d+)$', key)
        if m:
            nk = 'baqara_p%d' % (int(m.group(1)) + 1)
            if nk in texts:
                return texts[nk].split()[0]
        return None                      # آخر السورة → إقلاب

    changes = []

    def fix_one(m):
        key, sep, txt, end = m.groups()
        ws = txt.split()
        page = _TanweenPage(ws, tail_for(key))
        out_ws = list(ws)
        for n, w in enumerate(ws):
            r = _t_find(w)
            if not r:
                continue
            nxt = ws[n + 1] if n + 1 < len(ws) else page.tail
            want = (_t_rule(_t_bare(nxt), False) if nxt is not None
                    else 'IQLAB')
            if not want:
                continue
            nw = _t_rebuild(w, r[0], r[1], r[2], want)
            if nw and nw != w:
                out_ws[n] = nw
                changes.append((key, w, nw, nxt or '<آخر السورة>'))
        return key + sep + ' '.join(out_ws) + end

    newblock = _REC_ENTRY.sub(fix_one, block)
    if not changes:
        return out, False
    REC_TANWEEN.extend(changes)
    return out[:i] + newblock + out[j:], True



# ======================================================
# إصلاح روابط تنقل مكسورة
# ------------------------------------------------------
# NEXT_SEQUENCE كان فيه 'al-infitar' بشرطة والملف الحقيقي
# اسمه alinfitar.html. النتيجة: alinfitar نفسه مكانش بياخد
# صف تنقل خالص (المفتاح مش في الخريطة)، و attakwir/almutaffifin
# كان عندهم روابط لملف مش موجود (404). دالة add_page_nav_row
# بتسيب الأزرار الملفوفة صح من غير ما تلمسها، فالروابط الغلط
# كانت هتفضل حتى بعد تصليح الاسم — عشان كده الإصلاح ده منفصل.
# ======================================================
BROKEN_NAV_FIXED = []
_VALID_PAGE_KEYS = set(NEXT_SEQUENCE)


def fix_broken_page_nav_links(path, out):
    """يصلّح أي href في صف التنقل بيشاور على مفتاح مش في السلسلة."""
    fn = os.path.basename(path)
    fixed = []

    def _one(m):
        key = m.group(2)
        if key in _VALID_PAGE_KEYS:
            return m.group(0)
        cand = key.replace('-', '')
        if cand in _VALID_PAGE_KEYS:
            fixed.append(key + ' → ' + cand)
            return m.group(1) + cand + m.group(3)
        fixed.append('⚠ ' + key + ' (مش معروف)')
        return m.group(0)

    out2 = re.sub(r'(href=")([\w\-]+)(\.html"[^>]*class="(?:next|prev)-page-btn")',
                  _one, out)
    out2 = re.sub(r'(href=")([\w\-]+)(\.html" class="(?:next|prev)-page-btn")',
                  _one, out2)
    if fixed:
        BROKEN_NAV_FIXED.append((fn, sorted(set(fixed))))
    return out2, out2 != out



SELWORD_REPAIRED = []


def repair_broken_addwords(path, out):
    """يصلّح _addWords اللي بتنادي نفسها (استدعاء ذاتي لا نهائي).

    نسخة سابقة من port_selword_feature كانت بتولّد
    else{_addWords(nw);} بدل ضم الكلمات — فأي تسجيل من غير كلمة
    محدَّدة كان بيرمي RangeError ويوقف زر التسجيل.
    """
    if 'else{_addWords(nw);}' not in out:
        return out, False
    out = out.replace('else{_addWords(nw);}',
                      'else{_words=_fixWords([].concat(_words,nw));}')
    SELWORD_REPAIRED.append(os.path.basename(path))
    return out, True



# ======================================================
# تصادم شريط الأدوات مع الوضع الليلي في index.html
# ------------------------------------------------------
# .tools-fab بـ position:fixed;left:14px بتطلع برّه تدفّق
# الصفحة وتقف في أقصى الشمال فوق. في صفحات السور المكان ده
# فاضي (زر الرجوع على اليمين في RTL) فمافيش مشكلة — لكن في
# index.html زر 🌙 آخر عنصر في nav-right يعني أقصى الشمال،
# فالاتنين بيركبوا على بعض. الحل: نحجز مساحة على شمال الـnav
# قد عرض الزرار العائم (14 + 34 + فاصل) فالمحتوى يبدأ بعده.
# ======================================================
INDEX_NAV_FIXED = []
_NAV_RULE_RE = re.compile(r'(\bnav\s*\{[^}]*?padding:)(10px 18px)([^}]*\})')


TOPBAR_OVERLAP_FIXED = []
_TOPBAR_RULE_RE = re.compile(r'(\.top-bar\s*\{[^}]*?padding\s*:\s*)([^;}]+?)(\s*[;}])')


def fix_topbar_tools_overlap(path, out):
    """زر ☰ (قائمة الأدوات) بقى position:fixed في الركن الشمال، فطلع
    بره تدفّق الصفحة وبقى يقع فوق زر 🌙 في الصفحات الداخلية.

    index.html اتصلحت قبل كده بحجز مساحة في الترويسة
    (nav{padding:10px 18px 10px 58px}) — الدالة دي بتعمل نفس الحاجة
    بالظبط للصفحات الداخلية: .top-bar تاخد padding يسار 58px (14px
    مسافة الزر من الحافة + 34px عرضه + 10px فاصل) فالعناصر تتزحزح
    لجنبه بدل ما تتراكب معاه. مفيش أي تغيير في مكان ☰ ولا شكل أي زر.

    idempotent: لو الحجز موجود بالفعل بتخرج من غير تغيير. (أغسطس ٢٠٢٦)"""
    m = _TOPBAR_RULE_RE.search(out)
    if not m:
        return out, False
    pad = m.group(2).strip()
    if '58px' in pad:
        return out, False                      # اتصلح قبل كده
    parts = pad.split()
    if len(parts) == 2:                        # الشكل المتوقع: 12px 20px
        new_pad = '%s %s %s 58px' % (parts[0], parts[1], parts[0])
    elif len(parts) == 4:
        new_pad = '%s %s %s 58px' % (parts[0], parts[1], parts[2])
    else:
        TOPBAR_OVERLAP_FIXED.append(
            (os.path.basename(path), '\u26a0 padding مش بالشكل المتوقع: ' + pad))
        return out, False
    out = out[:m.start(2)] + new_pad + out[m.end(2):]
    TOPBAR_OVERLAP_FIXED.append((os.path.basename(path), pad + ' \u2192 ' + new_pad))
    return out, True


def fix_index_tools_overlap(path, out):
    if os.path.basename(path) != 'index.html':
        return out, False
    if 'padding:10px 18px 10px 58px' in out:
        return out, False                      # اتصلح قبل كده
    new, n = _NAV_RULE_RE.subn(lambda m: m.group(1) + '10px 18px 10px 58px' + m.group(3),
                               out, count=1)
    if not n:
        INDEX_NAV_FIXED.append('⚠ قاعدة nav مش متطابقة — اتخطّى')
        return out, False
    INDEX_NAV_FIXED.append('nav padding-left = 58px ✅')
    return new, True


# ======================================================
# اتساق الحكم مع العرض + نسبة واحتفال لكل سؤال
# ------------------------------------------------------
# ١) wordDiff كانت بتتخطّى الكلمات الزيادة من غير ما تعرضها،
#    فالعداد يقول "23/23 صحيحة" والحكم يقول غلط. دلوقتي
#    الكلمات الزيادة بتتعرض بلون مميز، والإحصاء بيتخزن.
# ٢) الحكم بقى: تطابق الجملة كاملة *أو* كل كلمات الإجابة
#    اتطابقت ومفيش كلمة زيادة — فمستحيل يظهر تناقض.
# ٣) نسبة النجاح الجارية + احتفال بعد كل إجابة صحيحة.
# ======================================================
VERDICT_FIXED = []
VERDICT_SKIPPED = []

_VD_ALIGN_OLD = """  const aligned=[];let i=n,j=m;
  while(i>0||j>0){
    if(i>0&&j>0&&nm(cWords[i-1])===nm(uWords[j-1])){aligned.push({ref:cWords[i-1],ok:true});i--;j--;}
    else if(j>0&&(i===0||dp[i][j-1]>=dp[i-1][j])){j--;}
    else{aligned.push({ref:cWords[i-1],ok:false});i--;}
  }"""
_VD_ALIGN_NEW = """  const aligned=[];let i=n,j=m;
  while(i>0||j>0){
    if(i>0&&j>0&&nm(cWords[i-1])===nm(uWords[j-1])){aligned.push({ref:cWords[i-1],ok:true});i--;j--;}
    else if(j>0&&(i===0||dp[i][j-1]>=dp[i-1][j])){aligned.push({ref:uWords[j-1],extra:true});j--;}
    else{aligned.push({ref:cWords[i-1],ok:false});i--;}
  }"""

_VD_HTML_OLD = """  const correct=aligned.filter(x=>x.ok).length;
  const html=aligned.map(x=>x.ok
    ?`<span style="color:#155724;background:#c3e6cb;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;font-weight:bold;" translate="no" class="notranslate">${x.ref}</span>`
    :`<span style="color:#fff;background:#c0392b;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;" translate="no" class="notranslate">${x.ref}</span>`
  ).join(' ');"""
_VD_HTML_NEW = """  const correct=aligned.filter(x=>x.ok).length;
  const extra=aligned.filter(x=>x.extra).length;
  window._lastDiff={matched:correct,total:n,extra:extra};
  const html=aligned.map(x=>x.extra
    ?`<span style="color:#7a4a00;background:#ffe0a3;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;text-decoration:line-through;" translate="no" class="notranslate">${x.ref}</span>`
    :x.ok
    ?`<span style="color:#155724;background:#c3e6cb;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;font-weight:bold;" translate="no" class="notranslate">${x.ref}</span>`
    :`<span style="color:#fff;background:#c0392b;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;" translate="no" class="notranslate">${x.ref}</span>`
  ).join(' ');"""

_VD_COUNT_OLD = """  return `<div style="margin-bottom:6px;font-size:13px;color:var(--text-soft);">${correct} / ${n} كلمة صحيحة</div>`"""
_VD_COUNT_NEW = """  return `<div style="margin-bottom:6px;font-size:13px;color:var(--text-soft);">${correct} / ${n} كلمة صحيحة${extra?` — و${extra} كلمة زيادة`:''}</div>`"""

# الحكم: الجملة كاملة أو المطابقة الكاملة كلمة كلمة
_VD_JUDGE_OLD = """  const userNorm=normalize(userVal);
  const ansNorm=normalize(q.answer);
  if(userNorm===ansNorm){"""
_VD_JUDGE_NEW = """  const userNorm=normalize(userVal);
  const ansNorm=normalize(q.answer);
  const _dh=wordDiff(userVal,q.answer);
  const _st=window._lastDiff||{};
  // الحكم من نفس مصدر العرض: لو كل كلمات الإجابة اتطابقت ومفيش
  // كلمة زيادة، تبقى صح — عشان مايحصلش تناقض بين "٢٣/٢٣ صحيحة"
  // والنتيجة "خطأ"
  const _ok=(userNorm===ansNorm)||(_st.total>0&&_st.matched===_st.total&&!_st.extra);
  if(_ok){"""

_VD_WRONG_OLD = """    fb.innerHTML='✗ الإجابة الصحيحة:<br><span style="font-size:18px;line-height:2.2;direction:rtl;display:block;text-align:right;">'+wordDiff(userVal,q.answer)+'</span>';"""
_VD_WRONG_NEW = """    fb.innerHTML='✗ الإجابة الصحيحة:<br><span style="font-size:18px;line-height:2.2;direction:rtl;display:block;text-align:right;">'+_dh+'</span>';"""


def _vd_progress_snippet(correct_msg):
    """رسالة النجاح + النسبة الجارية + احتفال"""
    return (correct_msg[:-1] + "+_pctNow();spawnConfetti(18);")


def fix_verdict_and_progress(path, out):
    """يخلي الحكم من نفس مصدر العرض، ويضيف نسبة واحتفال لكل سؤال.

    فيه تلات أجيال قالب (مضغوط، متباعد، ومتباعد بحقل user زيادة)
    فالمطابقة بـregex.
    """
    fn = os.path.basename(path)
    if 'const _ok=(userNorm===ansNorm)' in out:
        return out, False                      # اتطبّق قبل كده
    before_src = out
    before = quran_text_fingerprint(out)
    n = 0

    # ١) الكلمات الزيادة تتسجّل بدل ما تتخطّى بصمت
    _already_modern = 'window._lastDiff' in out
    if not _already_modern:
        out, c = re.subn(
            r"else\s*if\(j>0&&\(i===0\|\|dp\[i\]\[j-1\]>=dp\[i-1\]\[j\]\)\)\s*\{\s*j--;\s*\}",
            lambda m: "else if(j>0&&(i===0||dp[i][j-1]>=dp[i-1][j]))"
                      "{aligned.push({ref:uWords[j-1],user:uWords[j-1],extra:true});j--;}", out, count=1)
        n += c
        if not c:
            VERDICT_SKIPPED.append((fn, 6))
            return before_src, False

    # ٢) الإحصاء يتخزن عالميًا عشان الحكم يستخدمه
    out, c = (out, 0) if _already_modern else re.subn(r"const correct=aligned\.filter\(x=>x\.ok\)\.length;",
                     lambda m: "const correct=aligned.filter(x=>x.ok).length;"
                               "const extra=aligned.filter(x=>x.extra).length;"
                               "window._lastDiff={matched:correct,total:n,extra:extra};",
                     out, count=1)
    n += c

    # ٣) عرض الكلمات الزيادة بلون مميز
    out, c = (out, 0) if _already_modern else re.subn(r"aligned\.map\(x\s*=>\s*x\.ok\s*\n?\s*\?",
                     lambda m: "aligned.map(x=>x.extra?`<span style=\"color:#7a4a00;"
                               "background:#ffe0a3;border-radius:5px;padding:2px 6px;margin:2px 1px;"
                               "display:inline-block;text-decoration:line-through;\" translate=\"no\" "
                               "class=\"notranslate\">${x.ref}</span>`:x.ok?", out, count=1)
    n += c

    out, c = (out, 0) if _already_modern else re.subn(r"\$\{correct\} / \$\{n\} كلمة صحيحة",
                     lambda m: "${correct} / ${n} كلمة صحيحة${extra?` — و${extra} كلمة زيادة`:''}",
                     out, count=1)
    n += c
    if not c:
        out, c = re.subn(r"'\+correct\+' / '\+(n|cWords\.length)\+' كلمة صحيحة",
                         lambda m: "'+correct+' / '+" + m.group(1) +
                                   "+' كلمة صحيحة'+(extra?' — و'+extra+' كلمة زيادة':'')+'",
                         out, count=1)
        n += c

    # ٤) الحكم: تطابق كامل أو كل الكلمات مطابقة ومفيش زيادة
    _JUDGE_BODY = ("const userNorm=normalize(userVal),ansNorm=normalize(q.answer);"
                   "const _dh=wordDiff(userVal,q.answer);const _st=window._lastDiff||{};"
                   "const _ok=(userNorm===ansNorm)||(_st.total>0&&_st.matched===_st.total&&!_st.extra);"
                   "if(_ok){")
    out, c = re.subn(
        r"if\(normalize\(userVal\)===normalize\(q\.answer\)\)\s*\{",
        lambda m: _JUDGE_BODY, out, count=1)
    n += c
    # صيغة عامة: أي تعريفين لـuserNorm/ansNorm مهما كان اللي جواهم
    # (بعض الملفات بتلفّ التطبيع بدالة زيادة زي normalizeHurufMuqattaa)
    if not c:
        out, c = re.subn(
            r"(const\s+userNorm\s*=\s*[^;]+;\s*const\s+ansNorm\s*=\s*[^;]+;)\s*"
            r"if\s*\(\s*userNorm\s*===\s*ansNorm\s*\)\s*\{",
            lambda m: m.group(1) +
                      "const _dh=wordDiff(userVal,q.answer);const _st=window._lastDiff||{};"
                      "const _ok=(userNorm===ansNorm)||"
                      "(_st.total>0&&_st.matched===_st.total&&!_st.extra);if(_ok){",
            out, count=1)
        n += c
    # جيل تالت: const correct = normalize(q.answer); const user = normalize(userVal); if (user === correct) {
    if not c:
        out, c = re.subn(
            r"const\s+correct\s*=\s*normalize\(q\.answer\);\s*"
            r"const\s+user\s*=\s*normalize\(userVal\);\s*"
            r"if\s*\(\s*user\s*===\s*correct\s*\)\s*\{",
            lambda m: _JUDGE_BODY, out, count=1)
        n += c
    out, c = re.subn(
        r"const userNorm=normalize\(userVal\)[,;]\s*(?:const\s+)?ansNorm=normalize\(q\.answer\);\s*"
        r"if\(userNorm===ansNorm\)\{",
        lambda m: "const userNorm=normalize(userVal),ansNorm=normalize(q.answer);"
                  "const _dh=wordDiff(userVal,q.answer);const _st=window._lastDiff||{};"
                  "const _ok=(userNorm===ansNorm)||(_st.total>0&&_st.matched===_st.total&&!_st.extra);"
                  "if(_ok){", out, count=1)
    n += c

    out = re.sub(r"\+\s*wordDiff\(\s*userVal\s*,\s*q\.answer\s*\)\s*\+", "+_dh+", out, count=1)

    # ٥) النسبة الجارية
    if '_pctNow' not in out:
        helper = "\n" + _PCT_FN + "\n"
        out, c = re.subn(r"\nfunction checkTextVal\(", lambda m: helper + "\nfunction checkTextVal(",
                         out, count=1)
        n += c

    # ٦) احتفال بعدد قابل للتحكم
    out = out.replace('function spawnConfetti(){const colors=',
                      'function spawnConfetti(count){const colors=', 1)
    out = out.replace('for(let i=0;i<45;i++){const piece=',
                      'for(let i=0;i<(count||45);i++){const piece=', 1)

    # ٧) النسبة + الاحتفال في رسائل النجاح والخطأ
    out, _c2 = re.subn(r"(fb\.className\s*=\s*'feedback correct';\s*"
                       r"fb\.innerHTML\s*=\s*'✓ أحسنتِ?! إجابة صحيحة تماماً 🌟')",
                       lambda m: m.group(1) + "+_pctNow();spawnConfetti(18);", out, count=1)
    out = re.sub(r"fb\.className='feedback correct';fb\.textContent='✓ أحسنتِ!';",
                 lambda m: "fb.className='feedback correct';fb.innerHTML='✓ أحسنتِ! 🌟'+_pctNow();"
                           "spawnConfetti(18);", out, count=1)
    out = re.sub(r"(\+_dh\+'</span>')(;)", lambda m: m.group(1) + "+_pctNow()" + m.group(2),
                 out, count=1)

    # كل التعديلات المطلوبة أو لا شيء — ملف نصّه متعدّل بيبقى
    # أخطر من ملف مالوش تعديل خالص
    required = (['const _ok=(userNorm===ansNorm)', 'function _pctNow()']
                if _already_modern else
                ['extra:true});j--;}', 'window._lastDiff', 'x.extra?', 'كلمة زيادة',
                 'const _ok=(userNorm===ansNorm)', 'function _pctNow()'])
    missing = [r for r in required if r not in out]
    if missing:
        VERDICT_SKIPPED.append((fn, len(missing)))
        return before_src, False
    if quran_text_fingerprint(out) != before:
        print('⛔ %s: البصمة اتغيّرت — التعديل اتلغى' % fn)
        return before_src, False
    VERDICT_FIXED.append((fn, n))
    return out, True

# ======================================================
# ترقية wordDiff القديمة (مقارنة بالموضع) للنسخة الحديثة
# ------------------------------------------------------
# الجيل القديم بيقارن الكلمة رقم i بالكلمة رقم i — فكلمة
# زيادة واحدة في الأول بتخلي كل اللي بعدها يبان غلط. النسخة
# الحديثة بتعمل محاذاة (LCS) وبتحسب الزيادة والنقص بدقة.
# الدالة عرض وحساب بس — مافيهاش نص قرآني، والبصمة بتتفحص.
# ======================================================
LEGACY_WD_UPGRADED = []

_MODERN_WD = r'''function wordDiff(userVal, correctAnswer) {
  const nm = s => normalize(s||'');
  const uWords = nm(userVal).trim().split(/\s+/).filter(Boolean);
  const cRaw = correctAnswer.trim().split(/\s+/).filter(Boolean);
  const cWords = (typeof expandMuqattaat === 'function') ? expandMuqattaat(cRaw) : cRaw;
  const n = cWords.length, m = uWords.length;
  const dp = Array.from({length:n+1}, () => new Array(m+1).fill(0));
  for (let i=1;i<=n;i++) for (let j=1;j<=m;j++) {
    if (nm(cWords[i-1]) === nm(uWords[j-1])) dp[i][j] = dp[i-1][j-1] + 1;
    else dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
  }
  const aligned = []; let i=n, j=m;
  while (i>0 || j>0) {
    if (i>0 && j>0 && nm(cWords[i-1]) === nm(uWords[j-1])) { aligned.push({ref:cWords[i-1],ok:true}); i--; j--; }
    else if (j>0 && (i===0 || dp[i][j-1] >= dp[i-1][j])) { aligned.push({ref:uWords[j-1],extra:true}); j--; }
    else { aligned.push({ref:cWords[i-1],ok:false}); i--; }
  }
  aligned.reverse();
  const correct = aligned.filter(x=>x.ok).length;
  const extra = aligned.filter(x=>x.extra).length;
  window._lastDiff = {matched:correct, total:n, extra:extra};
  const html = aligned.map(x => x.extra
    ? '<span style="color:#7a4a00;background:#ffe0a3;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;text-decoration:line-through;" translate="no" class="notranslate">'+x.ref+'</span>'
    : x.ok
    ? '<span style="color:#155724;background:#c3e6cb;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;font-weight:bold;" translate="no" class="notranslate">'+x.ref+'</span>'
    : '<span style="color:#fff;background:#c0392b;border-radius:5px;padding:2px 6px;margin:2px 1px;display:inline-block;" translate="no" class="notranslate">'+x.ref+'</span>'
  ).join(' ');
  return '<div style="margin-bottom:6px;font-size:13px;color:var(--text-soft,#666);">'+correct+' / '+n+' كلمة صحيحة'+(extra?' — و'+extra+' كلمة زيادة':'')+'</div>'
       + '<div style="font-size:18px;line-height:2.5;direction:rtl;text-align:right;">'+html+'</div>';
}'''


def upgrade_legacy_worddiff(path, out):
    """يستبدل wordDiff القديمة (بدون محاذاة) بالنسخة الحديثة."""
    fn = os.path.basename(path)
    if 'window._lastDiff' in out:
        return out, False                      # حديثة أصلاً
    i = out.find('function wordDiff')
    if i < 0:
        return out, False
    if 'const aligned' in out[i:i+2500]:
        return out, False                      # فيها محاذاة — مش الجيل القديم
    sp = _nf_span(out, 'function wordDiff')
    if not sp:
        return out, False
    st, en = sp
    before = quran_text_fingerprint(out)
    new = out[:i] + _MODERN_WD + out[en:]
    if quran_text_fingerprint(new) != before:
        print('⛔ %s: البصمة اتغيّرت — الترقية اتلغت' % fn)
        return out, False
    LEGACY_WD_UPGRADED.append(fn)
    return new, True



_PCT_FN = 'function _pctNow(){const d=correctCount+wrongCount;const st=window._lastDiff||{};let a=\'\';if(st.total){const wp=Math.round(st.matched*100/st.total);a=`<div style="margin-top:6px;font-size:14px;opacity:.9;">دقة هذه الإجابة: ${wp}% (${st.matched} من ${st.total} كلمة)</div>`;}if(!d)return a;return a+`<div style="margin-top:2px;font-size:13px;opacity:.7;">الأسئلة الصحيحة: ${correctCount} من ${d}</div>`;}'
PCT_UPGRADED = []


def upgrade_pct_display(path, out):
    """النسبة القديمة كانت بتحسب الأسئلة بس — فإجابة فيها كلمة غلط
    واحدة كانت بتطلّع 0% جنب "18/19 كلمة صحيحة". النسخة الجديدة
    بتعرض دقة الإجابة الحالية بالكلمات + عدد الأسئلة الصحيحة."""
    m = re.search(r"function _pctNow\(\)\{.*?\}\n", out, re.S)
    if not m or 'دقة هذه الإجابة' in out:
        return out, False
    before = quran_text_fingerprint(out)
    out = out[:m.start()] + _PCT_FN + '\n' + out[m.end():]
    if quran_text_fingerprint(out) != before:
        return out, False
    PCT_UPGRADED.append(os.path.basename(path))
    return out, True


# ======================================================
# النسبة على أساس الكلمات بدل الأسئلة
# ------------------------------------------------------
# كان: نسبة = الأسئلة الصحيحة / إجمالي الأسئلة — فسؤال فيه
# كلمة واحدة غلط بياخد صفر، و7/8 كلمة صحيحة بتظهر جنب 0%.
# بقى: نسبة = إجمالي الكلمات الصحيحة / إجمالي الكلمات.
# السهل (اختيار من متعدد) بيتحسب كلمة واحدة لكل سؤال.
# ======================================================
WORDSCORE_FIXED = []
WORDSCORE_SKIPPED = []

_WS_PCT = 'function _pctNow(){const st=window._lastDiff||{};let a=\'\';if(st.total){const wp=Math.round(st.matched*100/st.total);a=`<div style="margin-top:6px;font-size:14px;opacity:.9;">دقة هذه الإجابة: ${wp}% (${st.matched} من ${st.total} كلمة)</div>`;}// السطر التاني يظهر بس لو فيه أسئلة سابقة — من غير كده الرقمين واحد\nif(!wTotal||wTotal===st.total)return a;const p=Math.round(wCorrect*100/wTotal);return a+`<div style="margin-top:2px;font-size:13px;opacity:.75;">الإجمالي: ${p}% (${wCorrect} من ${wTotal} كلمة)</div>`;}'


def switch_to_word_based_score(path, out):
    fn = os.path.basename(path)
    if 'wTotal' in out:
        return out, False
    if 'function _pctNow()' not in out:
        WORDSCORE_SKIPPED.append(fn)
        return out, False
    before_src, before = out, quran_text_fingerprint(out)
    n = 0

    # ١) عدّادات الكلمات
    out, c = re.subn(r"(let currentLevel\s*=\s*null[^;]*;)",
                     lambda m: m.group(1) + 'let wCorrect=0,wTotal=0;', out, count=1)
    n += c

    # ٢) التصفير مع بداية أي اختبار
    out, c = re.subn(r"qIndex\s*=\s*correctCount\s*=\s*wrongCount\s*=\s*0;",
                     lambda m: m.group(0) + 'wCorrect=wTotal=0;', out, count=1)
    n += c

    # ٣) تجميع كلمات كل سؤال نصّي
    out, c = re.subn(r"(const _st=window\._lastDiff\|\|\{\};)",
                     lambda m: m.group(1) + 'if(_st.total){wCorrect+=_st.matched;wTotal+=_st.total;}',
                     out, count=1)
    n += c

    # ٤) السهل: كلمة واحدة لكل سؤال
    out, c = re.subn(r"function checkMCQ\(\s*chosen\s*,\s*correct\s*,\s*btn\s*\)\s*\{",
                     lambda m: m.group(0) + 'wTotal++;if(chosen===correct)wCorrect++;', out, count=1)
    n += c

    # ٥) التخطي: الكلمات تتحسب ناقصة
    out, c = re.subn(r"(function skipQuestion\(\)\s*\{\s*const\s+q\s*=\s*questions\[qIndex\];)",
                     lambda m: m.group(1) + "wTotal+=(currentLevel==='easy'?1:"
                                            "String(q.answer||'').trim().split(/\\s+/).filter(Boolean).length||1);",
                     out, count=1)
    n += c

    # ٦) عرض النسبة
    out, c = re.subn(r"function _pctNow\(\)\{.*?\}\n", lambda m: _WS_PCT + '\n', out, count=1, flags=re.S)
    n += c

    # ٧) النتيجة النهائية بالكلمات
    out, c = re.subn(r"const\s+pct\s*=\s*Math\.round\(\(\s*correctCount\s*/\s*questions\.length\s*\)\s*\*\s*100\);",
                     lambda m: "const pct=wTotal?Math.round(wCorrect*100/wTotal):0;", out, count=1)
    n += c
    out = re.sub(r"(document\.getElementById\('result-score'\)\.textContent\s*=\s*)`[^`]*`;",
                 lambda m: m.group(1) + "`${toArabicNum(wCorrect)} / ${toArabicNum(wTotal)} كلمة — "
                                        "${toArabicNum(pct)}%  |  ${toArabicNum(correctCount)} / "
                                        "${toArabicNum(questions.length)} سؤال`;", out, count=1)

    required = ('let wCorrect=0,wTotal=0;', 'wCorrect+=_st.matched', 'wTotal++',
                'wCorrect*100/wTotal')
    if any(r not in out for r in required):
        WORDSCORE_SKIPPED.append(fn)
        return before_src, False
    if quran_text_fingerprint(out) != before:
        print('⛔ %s: البصمة اتغيّرت — التعديل اتلغى' % fn)
        return before_src, False
    WORDSCORE_FIXED.append((fn, n))
    return out, True


# ======================================================
# مدة عرض نتيجة السؤال قبل الانتقال التلقائي
# ------------------------------------------------------
# كانت 1100ms — كفاية أيام ما كانت الرسالة سطر واحد. دلوقتي
# بنعرض تفصيل الكلمات + دقة الإجابة + النسبة الجارية + احتفال،
# فالوقت ده مش كافي للقراءة. الانتقال التلقائي بيحصل في حالة
# الإجابة الصحيحة بس؛ الغلط بيستنى ضغطة "التالي".
# ======================================================
DELAY_FIXED = []
_HARD_MS = 3500      # الصعب: آية كاملة + تفصيل كلمة كلمة
_MCQ_MS = 2200       # السهل: كلمة واحدة


def widen_autoadvance_delay(path, out):
    fn = os.path.basename(path)
    before_src, before = out, quran_text_fingerprint(out)
    n = 0
    # الصعب: جوه checkTextVal
    i = out.find('function checkTextVal')
    if i >= 0:
        seg_end = out.find('function checkText(', i)
        if seg_end < 0:
            seg_end = i + 4000
        seg = out[i:seg_end]
        seg2, c = re.subn(r"(if\(qIndex===__qi\)nextQuestion\(\);\},)\s*1100\s*\)",
                          lambda m: m.group(1) + str(_HARD_MS) + ')', seg, count=1)
        if c:
            out = out[:i] + seg2 + out[seg_end:]
            n += c
    # السهل: باقي المواضع
    out, c = re.subn(r"(if\(qIndex===__qi\)nextQuestion\(\);\},)\s*1100\s*\)",
                     lambda m: m.group(1) + str(_MCQ_MS) + ')', out)
    n += c
    if not n:
        return before_src, False
    if quran_text_fingerprint(out) != before:
        return before_src, False
    DELAY_FIXED.append((fn, n))
    return out, True



PCT_DEDUP = []


def dedup_pct_lines(path, out):
    """السطرين كانوا بيطلعوا نفس الرقم لو السؤال هو الأول — دلوقتي
    سطر الإجمالي يظهر بس لما يبقى فيه أسئلة سابقة فعلًا."""
    if 'wTotal===st.total' in out or 'function _pctNow()' not in out:
        return out, False
    before = quran_text_fingerprint(out)
    new, c = re.subn(r"function _pctNow\(\)\{.*?\n?\}\n", _WS_PCT + '\n', out, count=1, flags=re.S)
    if not c or quran_text_fingerprint(new) != before:
        return out, False
    PCT_DEDUP.append(os.path.basename(path))
    return new, True


# ======================================================
# مكتبة الدوال القياسية
# ------------------------------------------------------
# بدل ما نلاحق ٥–٩ صيغ مختلفة بالـregex كل مرة، فيه نسخة
# واحدة معتمدة لكل دالة والسكربت بيستبدلها في كل الملفات.
# بعد كده أي تعديل = تعديل نص واحد هنا.
# الدوال دي منطق عرض وتصحيح — مافيهاش نص قرآني، والبصمة
# بتتفحص قبل وبعد كضمانة.
# ======================================================
CANON_APPLIED = {}
CANON_SKIPPED = {}

CANON_FN = {}

CANON_FN['checkTextVal'] = r'''function checkTextVal(q,userVal){
  const fb=document.getElementById('feedback');
  const _sk=document.getElementById('skip-btn');if(_sk)_sk.style.display='none';
  const _nx=document.getElementById('next-btn');if(_nx)_nx.style.display='block';
  // بعض الصفحات بتلفّ التطبيع بدالة زيادة (الحروف المقطعة)
  const _pre=(typeof normalizeHurufMuqattaa==='function')?normalizeHurufMuqattaa:(x=>x);
  const userNorm=normalize(_pre(userVal));
  const ansNorm=normalize(_pre(q.answer));
  const _dh=wordDiff(userVal,q.answer);
  const _st=window._lastDiff||{};
  if(_st.total){wCorrect+=_st.matched;wTotal+=_st.total;}
  // الحكم من نفس مصدر العرض: تطابق كامل أو كل الكلمات مطابقة ومفيش زيادة
  const _ok=(userNorm===ansNorm)||(_st.total>0&&_st.matched===_st.total&&!_st.extra);
  if(_ok){
    correctCount++;statuses[qIndex]='correct';
    fb.className='feedback correct';
    fb.innerHTML='✓ أحسنت! إجابة صحيحة تماماً 🌟';
    if(currentLevel==='hard'){const __qi=qIndex;setTimeout(()=>{if(qIndex===__qi)nextQuestion();},3500);}
  }else{
    wrongCount++;statuses[qIndex]='wrong';wrongIndices.push(qIndex);
    fb.className='feedback wrong';
    fb.innerHTML='✗ الإجابة الصحيحة:<br><span style="font-size:18px;line-height:2.2;direction:rtl;display:block;text-align:right;">'+_dh+'</span>';
  }
  fb.style.display='block';
  if(typeof updateBadges==='function')updateBadges();
  if(typeof renderDotProgress==='function')renderDotProgress();
  if(typeof saveResumeState==='function')saveResumeState();
}'''

CANON_FN['normalize'] = 'function normalize(str)' + "{\n  if(!str)return'';\n  return str\n    .replace(/ي\\u0653?ـ\\u064E\\u0654/g,'ي')\n    .replace(/ي\\u0653?ـ\\u064E\\u0654/g,'ي').replace(/ـ\\u064E\\u0654/g,'ا')\n    .replace(/ـ[\\u064B-\\u065F]*[\\u0654\\u0655]/g,'')\n    .replace(/ـۧ/g,'ي').replace(/يٓ?ـَٔ/g,'ي').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـ/g,'')\n    .replace(/[\\u064B-\\u065F\\u0610-\\u061A\\u06D6-\\u06DC\\u06DF-\\u06E4\\u06E7\\u06E8\\u06EA-\\u06ED\\u08F0-\\u08F2]/g,'')\n    .replace(/ها[ؤو]لاء|ها[ؤو]لا(?!\\S)/g,'هالا').replace(/ه[ؤو]لاء|ه[ؤو]لا(?!\\S)/g,'هالا')\n    .replace(/وٱ(?!ل)/g,'و')\n    .replace(/(?<=^|\\s)وا(?=سجد|قترب|دخل|دعو|ذكر|رحم|ستغفر|ستغن|غفر|عف|نحر|تق|ختلاف|مر[أا]|تبع|سمع|ستكبر|ستعين|ركع|صبر|صل|جتنب|هبط|ستبشر|ستقم|ضرب|عتصم|ئتلف|بتغ|حذر|شرب|صفح|تخذ)/g,'و')\n    .replace(/وٰ(?=ة)/g,'ا').replace(/وٰ/g,'وا')\n    .replace(/اٰ/g,'ا').replace(/يٰ/g,'يا')\n    .replace(/نٰ/g,'نا')\n    .replace(/(?<=^|\\s)بلىٰ(?=\\s|$)/g,'بلا').replace(/ىٰ(?=\\S)/g,'ا').replace(/ىٰ/g,'ي')\n    .replace(/(.)ٰ/g,'$1ا')\n    .replace(/هۥ/g,'ه').replace(/هۦ/g,'ه')\n    .replace(/ۦ(?=\\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'')\n    .replace(/ه[ۥۦ]/g,'ه')\n    .replace(/[ئؤ]/g,'ا').replace(/ء/g,'')\n    .replace(/[آأإٱا]/g,'ا')\n    .replace(/[ىی]/g,'ي')\n    .replace(/ة/g,'ه')\n    .replace(/(?<=^|\\s)ممنع(?=\\s|$)/g,'ممن منع').replace(/(.)\\1+/g,'$1')\n    .replace(/الربوا/g,'الربا').replace(/رحمان/g,'رحمن').replace(/(?<=^|\\s)فازالهما(?=\\s|$)/g,'فازلهما').replace(/(?<=^|\\s)فاذلهما(?=\\s|$)/g,'فازلهما').replace(/(?<=^|\\s)فادراتم(?=\\s|$)/g,'فادارتم').replace(/(?<=^|\\s)فادرأتم(?=\\s|$)/g,'فادارتم').replace(/(?<=^|\\s)فاداراتم(?=\\s|$)/g,'فادارتم').replace(/(?<=^|\\s)بن(?=\\s|$)/g,'ابن').replace(/نصاري(?=\\s|$)/g,'نصارا').replace(/(?<=^|\\s)ناتي(?=\\s|$)/g,'نات').replace(/(?<=^|\\s)ولا تجدنهم(?=\\s|$)/g,'ولتجدنهم').replace(/(?<=^|\\s)ولاتجدنهم(?=\\s|$)/g,'ولتجدنهم').replace(/(?<=^|\\s)او كل ما(?=\\s|$)/g,'اوكلما').replace(/(?<=^|\\s)او كلما(?=\\s|$)/g,'اوكلما').replace(/(?<=^|\\s)بلي(?=\\s|$)/g,'بلا')\n    .replace(/مولانا/g,'مولنا').replace(/يا ايها/g,'يايها').replace(/يا ايتها/g,'يايتها').replace(/الاه/g,'اله').replace(/ارايت/g,'اريت').replace(/اولااك/g,'اولاك').replace(/ياايها/g,'يايها').replace(/ياايتها/g,'يايتها').replace(/نب/g,'مب').replace(/وا(?=\\s|$)/g,'و').replace(/اولك/g,'اولاك').replace(/يا ?ايها/g,'يايها').replace(/يا ?ايتها/g,'يايتها')\n    .replace(/الاه/g,'اله').replace(/ارايت/g,'اريت')\n    .replace(/هاذا/g,'هذا').replace(/هاذه/g,'هذه').replace(/ذالك/g,'ذلك').replace(/لاكن/g,'لكن')\n    .replace(/\\s+/g,' ')\n    .trim();\n}"



# ------------------------------------------------------
# checkMCQ / checkText / skipQuestion — يوليو ٢٠٢٦
# الأساس: نسخة الجيل الحديث (٧ ملفات) بعد أربع تصحيحات:
#  · صيغة الخطاب مذكر رسمي (أحسنت)
#  · next-btn بـ'block' مش '' — الكلاس .next-btn في
#    p47/annaba فيه display:none، فـ'' كانت هتخفي الزر نهائيًا
#  · حراسة typeof على كل نداء خارجي (منع ReferenceError)
#  · renderDotProgress/saveResumeState في skipQuestion —
#    التخطي ماكانش بيحفظ التقدم في أي نسخة من الخمسة
# checkText بقت غلاف لـcheckTextVal بس: تلات ملفات (p25،
# p47، annaba) كانت بتصحّح جوّها ومابتناديهاش خالص، يعني
# توحيد checkTextVal ماكانش له أي أثر فيهم.
# ------------------------------------------------------
CANON_FN['checkMCQ'] = r'''function checkMCQ(chosen,correct,btn){wTotal++;if(chosen===correct)wCorrect++;document.querySelectorAll('.choice-btn').forEach(b=>b.disabled=true);const fb=document.getElementById('feedback');const _ans=questions[qIndex].choices[correct];if(chosen===correct){if(btn)btn.classList.add('correct');correctCount++;statuses[qIndex]='correct';fb.className='feedback correct';fb.innerHTML='✓ أحسنت! 🌟';const __qi=qIndex;setTimeout(()=>{if(qIndex===__qi)nextQuestion();},2200);}else{if(btn)btn.classList.add('wrong');wrongCount++;statuses[qIndex]='wrong';wrongIndices.push(qIndex);document.querySelectorAll('.choice-btn').forEach(b=>{if(b.textContent===_ans)b.classList.add('correct');});fb.className='feedback wrong';fb.innerHTML='✗ الإجابة الصحيحة: <span class="notranslate" translate="no">'+_ans+'</span>';}fb.style.display='block';document.getElementById('skip-btn').style.display='none';document.getElementById('next-btn').style.display='block';if(typeof updateBadges==='function')updateBadges();if(typeof renderDotProgress==='function')renderDotProgress();if(typeof saveResumeState==='function')saveResumeState();}'''

CANON_FN['checkText'] = r'''function checkText(q){const input=document.getElementById('user-input');const userVal=input?input.value.trim():'';if(!userVal)return;if(input)input.disabled=true;document.querySelectorAll('.submit-btn').forEach(s=>s.disabled=true);checkTextVal(q,(typeof markBadSpelling==='function')?markBadSpelling(userVal):userVal);}'''

CANON_FN['skipQuestion'] = r'''function skipQuestion(){const q=questions[qIndex];const fb=document.getElementById('feedback');wTotal+=(currentLevel==='easy'?1:String(q.answer||'').trim().split(/\s+/).filter(Boolean).length||1);if(currentLevel==='easy'){document.querySelectorAll('.choice-btn').forEach(b=>{b.disabled=true;if(b.textContent===q.choices[q.answer])b.classList.add('correct');});fb.className='feedback wrong';fb.innerHTML='⬅ الإجابة الصحيحة: <span class="notranslate" translate="no">'+q.choices[q.answer]+'</span>';}else{const inp=document.getElementById('user-input');if(inp)inp.disabled=true;document.querySelectorAll('.submit-btn').forEach(s=>s.disabled=true);fb.className='feedback wrong';fb.innerHTML='⬅ الإجابة الصحيحة:<br><span style="font-size:18px;line-height:2.2;direction:rtl;display:block;text-align:right;" class="notranslate" translate="no">'+q.answer+'</span>';}wrongCount++;statuses[qIndex]='wrong';wrongIndices.push(qIndex);fb.style.display='block';document.getElementById('skip-btn').style.display='none';document.getElementById('next-btn').style.display='block';if(typeof updateBadges==='function')updateBadges();if(typeof renderDotProgress==='function')renderDotProgress();if(typeof saveResumeState==='function')saveResumeState();}'''


# ======================================================
# توحيد صيغة الخطاب — مذكر رسمي في كل نصوص الواجهة
# ------------------------------------------------------
# كل نص يخاطب المستخدم يبقى مذكرًا. الترتيب مهم: العبارات
# الأطول الأول، وبعدين الكلمة المفردة (وافتحي قبل افتحي،
# وأعيدي قبل أعيدي) وإلا الاستبدال الأقصر يقطع الأطول.
# النص القرآني ممنوع يتلمس — البصمة بتتفحص قبل وبعد،
# وأي تغيير فيها بيلغي التعديل كله للملف ده.
# ======================================================
MASC_FIXED = []

_MASC_BANNER_OLD = '\u200f📌 عندك اختبار لسه ما خلصتيهوش، عايزة تكملي منين وقفتِ؟'.replace('\u200f', '')
_MASC_BANNER_NEW = ('📌 لديك اختبار لم يكتمل. هل ترغب في المتابعة من حيث '
                    'توقفتَ، أم البدء من جديد؟')

_MASC_PAIRS = [
    # لافتة استكمال الاختبار: النسخة الفصحى المذكّرة معتمدة بالفعل
    # في ٣ ملفات — التوحيد بيوصّل الباقي لنفس النص
    (_MASC_BANNER_OLD, _MASC_BANNER_NEW),
    # ماضي المخاطب
    ('أحسنتِ', 'أحسنت'), ('أتقنتِ', 'أتقنت'), ('وقفتِ', 'وقفت'),
    ('بدأتِ', 'بدأت'), ('أنجزتِ', 'أنجزت'), ('قلتِ', 'قلت'),
    # أمر المخاطب — الأطول قبل الأقصر
    ('وأعيدي', 'وأعد'), ('أعيدي', 'أعد'),
    ('وافتحي', 'وافتح'), ('افتحي', 'افتح'),
    ('والصقيه', 'والصقه'),
    ('اضغطي', 'اضغط'), ('سجّلي', 'سجّل'), ('راجعي', 'راجع'),
    ('استمري', 'استمر'), ('تيأسي', 'تيأس'), ('انقري', 'انقر'),
    ('اختاري', 'اختر'), ('انسخي', 'انسخ'), ('حمّلي', 'حمّل'),
    ('ابحثي', 'ابحث'),
    # مضارع المخاطب
    ('تحتاجين', 'تحتاج'),
]


# كلمة فيها علامة قرآنية بحتة (ألف خنجرية / علامة صغيرة / مدّة /
# تنوين متتابع). العلامات دي ما بتظهرش في عربي الواجهة أبدًا، فالبصمة
# دي بتغطي النص القرآني في *أي* مكان في الملف — يشمل المكتوب inline في
# HTML، اللي quran_text_fingerprint مابيشوفهوش (بيقرا المصفوفات بس)
_Q_MARKED = re.compile(
    r'[\u0621-\u064A][\u064B-\u0652]*'
    r'[\u0670\u0653\u0654\u0655\u06D6-\u06ED\u08F0-\u08F2]'
    r'[\u0621-\u0652\u0670\u06D6-\u06ED\u08F0-\u08F2]*')


def _q_marked_fingerprint(html):
    """بصمة كل كلمة مشكّلة بعلامة قرآنية، في كل الملف."""
    return hashlib.md5(
        '\x01'.join(_Q_MARKED.findall(html)).encode('utf-8')).hexdigest()


def unify_masculine_address(path, out):
    """كل نص واجهة يخاطب المستخدم يتحول لمذكر رسمي."""
    before_src = out
    before = quran_text_fingerprint(out)
    before_q = _q_marked_fingerprint(out)
    n = 0
    for old, new in _MASC_PAIRS:
        c = out.count(old)
        if c:
            out = out.replace(old, new)
            n += c
    if not n:
        return before_src, False
    if quran_text_fingerprint(out) != before:
        print('⛔ %s: البصمة اتغيّرت — توحيد صيغة الخطاب اتلغى'
              % os.path.basename(path))
        return before_src, False
    if _q_marked_fingerprint(out) != before_q:
        print('⛔ %s: كلمة قرآنية اتغيّرت — توحيد صيغة الخطاب اتلغى'
              % os.path.basename(path))
        return before_src, False
    MASC_FIXED.append((os.path.basename(path), n))
    return out, True


def apply_canonical_functions(path, out, names=None):
    """يستبدل الدوال المشتركة بالنسخة القياسية الواحدة."""
    fn = os.path.basename(path)
    before_src = out
    before = quran_text_fingerprint(out)
    done = []
    for name in (names or CANON_FN):
        head = 'function %s(' % name
        sp = _nf_span(out, head)
        if not sp:
            CANON_SKIPPED.setdefault(name, []).append(fn)
            continue
        st, en = sp
        i = out.find(head)
        cur = out[i:en]
        new = CANON_FN[name]
        if re.sub(r'\s+', '', cur) == re.sub(r'\s+', '', new):
            continue                            # مطابقة أصلاً
        out = out[:i] + new + out[en:]
        done.append(name)
    if not done:
        return out, False
    if quran_text_fingerprint(out) != before:
        # لازم نرجّع النص الأصلي، مش المعدّل — وإلا التحذير يروح
        # في اللوج والتلف يعدّي للملف
        print('⛔ %s: البصمة اتغيّرت — التوحيد اتلغى' % fn)
        return before_src, False
    for d in done:
        CANON_APPLIED.setdefault(d, []).append(fn)
    return out, True


# ======================================================
# فحص جودة الأسئلة — قراءة فقط
# ------------------------------------------------------
# القواعد الموثّقة:
#  · السهل والمتوسط يكمّلوا بعض — صفر تكرار في الكلمة المستهدفة
#  · اختيارات السهل مايتكررش فيها كلمة
#  · إجابة المتوسط كلمة أو كلمتين، بلا علامات ترقيم
#  · الإجابة الصحيحة مايبقاش شكلها مميز عن المشتتات
# ======================================================
QUALITY_ISSUES = []


def _qa_arrays(html):
    out = {}
    for name in ('EASY_Q', 'MEDIUM_Q', 'AYAT', 'ORDER_AYAT'):
        body, _, _ = _t_array_body(html, name)
        out[name] = body
    return out


def _qa_easy_targets(body):
    """(نص السؤال, الاختيارات, فهرس الإجابة) لكل سؤال سهل."""
    res = []
    for m in re.finditer(r'\{[^{}]*choices\s*:\s*\[([^\]]*)\][^{}]*\}', body or ''):
        blk = m.group(0)
        ch = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        am = re.search(r'answer\s*:\s*(\d+)', blk)
        qm = re.search(r'q\s*:\s*"((?:[^"\\]|\\.)*)"', blk)
        res.append((qm.group(1) if qm else '', ch, int(am.group(1)) if am else 0))
    return res


def _qa_medium_answers(body):
    return re.findall(r'answer\s*:\s*"((?:[^"\\]|\\.)*)"', body or '')


def audit_question_quality(root):
    files = sorted(f for f in os.listdir(root)
                   if f.endswith('.html') and f not in ('index.html', 'recitation.html'))
    dup_files, over_files, long_files, punct_files = [], [], [], []
    for fn in files:
        try:
            with open(os.path.join(root, fn), encoding='utf-8') as fh:
                html = fh.read()
        except Exception:
            continue
        a = _qa_arrays(html)
        easy = _qa_easy_targets(a['EASY_Q'])
        med = _qa_medium_answers(a['MEDIUM_Q'])

        # ١) اختيارات مكررة
        dups = [(i, [c for c in set(ch) if ch.count(c) > 1])
                for i, (_, ch, _) in enumerate(easy) if len(set(ch)) != len(ch)]
        if dups:
            dup_files.append((fn, dups))

        # ٢) تداخل الكلمة المستهدفة
        et = [ch[ai] for _, ch, ai in easy if ai < len(ch)]
        inter = sorted({x for x in et if x in med})
        if inter:
            over_files.append((fn, len(inter), len(et), inter))

        # ٣) إجابة المتوسط أطول من كلمتين
        lng = [x for x in med if len(x.split()) > 2]
        if lng:
            long_files.append((fn, lng))

        # ٤) علامات ترقيم في إجابة المتوسط
        pn = [x for x in med if re.search(r'[،,\-—()\.]', x)]
        if pn:
            punct_files.append((fn, pn))

    print('\n=== فحص جودة الأسئلة (قراءة فقط) ===')
    print('ملفات مفحوصة: %d' % len(files))

    print('\n-- اختيارات مكررة في السهل: %d ملف --' % len(dup_files))
    for fn, d in dup_files[:20]:
        print('   %s : %s' % (fn, ' · '.join('EASY_Q[%d] %s' % (i, ' '.join(w)) for i, w in d)))

    print('\n-- تداخل الكلمة المستهدفة بين السهل والمتوسط: %d ملف --' % len(over_files))
    for fn, n, tot, words in sorted(over_files, key=lambda x: -x[1])[:25]:
        print('   %-22s %d من %d   %s' % (fn, n, tot, ' · '.join(words[:4])))

    print('\n-- إجابة متوسط أطول من كلمتين: %d ملف --' % len(long_files))
    for fn, w in long_files[:15]:
        print('   %-22s %s' % (fn, ' · '.join(w[:3])))

    print('\n-- علامات ترقيم في إجابة المتوسط: %d ملف --' % len(punct_files))
    for fn, w in punct_files[:15]:
        print('   %-22s %s' % (fn, ' · '.join(w[:3])))
    print('=== نهاية فحص الجودة ===\n')


SITE_ORIGIN = 'https://quran-darbi.com'


def build_sitemap_and_robots(root):
    """توليد sitemap.xml و robots.txt من الملفات الموجودة فعلًا.

    بيتولّدوا آليًا في كل تشغيل، فأي صفحة جديدة تدخل الخريطة من غير
    أي تدخّل يدوي. index.html بيتسجّل على الجذر / مش /index.html
    عشان ما يبقاش فيه رابطين لنفس الصفحة.

    بترجع (changed_files, count) وبتكتب بس لو المحتوى اتغيّر فعلًا.
    """
    from datetime import date
    today = date.today().isoformat()

    names = sorted(
        fn for fn in os.listdir(root)
        if fn.endswith('.html') and os.path.isfile(os.path.join(root, fn))
    )

    entries = []
    for fn in names:
        if fn == 'index.html':
            loc, prio = SITE_ORIGIN + '/', '1.0'
        elif fn == 'recitation.html':
            loc, prio = SITE_ORIGIN + '/' + fn, '0.9'
        else:
            loc, prio = SITE_ORIGIN + '/' + fn, '0.8'
        entries.append(
            '  <url>\n'
            f'    <loc>{loc}</loc>\n'
            f'    <lastmod>{today}</lastmod>\n'
            '    <changefreq>weekly</changefreq>\n'
            f'    <priority>{prio}</priority>\n'
            '  </url>'
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(entries) + '\n</urlset>\n'
    )

    robots = (
        'User-agent: *\n'
        'Allow: /\n\n'
        f'Sitemap: {SITE_ORIGIN}/sitemap.xml\n'
    )

    changed = []
    for name, content in (('sitemap.xml', sitemap), ('robots.txt', robots)):
        p = os.path.join(root, name)
        old = ''
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                old = f.read()
        # تجاهُل lastmod في المقارنة: لو الصفحات ما اتغيّرتش، ما نعملش
        # كوميت جديد كل يوم بسبب التاريخ لوحده
        if re.sub(r'<lastmod>.*?</lastmod>', '', old) != \
           re.sub(r'<lastmod>.*?</lastmod>', '', content):
            with open(p, 'w', encoding='utf-8') as f:
                f.write(content)
            changed.append(name)
    return changed, len(entries)


def fix_add_canonical(path, out):
    """إضافة <link rel="canonical"> لكل صفحة.

    بيمنع جوجل يعتبر نفس الصفحة محتوى مكرر لما توصلها من روابط مختلفة
    (بـ www أو من الدومين القديم). idempotent.
    """
    if 'rel="canonical"' in out or "rel='canonical'" in out:
        return out, False
    fn = os.path.basename(path)
    loc = SITE_ORIGIN + '/' + ('' if fn == 'index.html' else fn)
    tag = f'<link rel="canonical" href="{loc}">'
    if '</head>' in out:
        return out.replace('</head>', tag + '\n</head>', 1), True
    return out, False


OG_IMAGE_BLOCK = (
    '<meta property="og:image" content="https://quran-darbi.com/og-image.png">\n'
    '<meta property="og:image:width" content="1200">\n'
    '<meta property="og:image:height" content="630">\n'
    '<meta property="og:image:alt" content="دربي لحفظ القرآن — اختبارات تفاعلية لحفظ كتاب الله ومراجعته">\n'
    '<meta property="og:site_name" content="دربي لحفظ القرآن">\n'
    '<meta name="twitter:card" content="summary_large_image">'
)


def fix_add_og_image(out):
    """إضافة صورة معاينة الروابط (og:image) + بطاقة تويتر.

    بتُحقن بعد og:type لو موجود، وإلا قبل </head> مباشرة. الرابط مطلق
    عن قصد: زاحفات فيسبوك وتويتر ما بتحلّش المسارات النسبية.
    idempotent: الحارس بيمنع أي تكرار.
    """
    if 'og:image' in out:
        return out, False
    anchor = '<meta property="og:type" content="website">'
    if anchor in out:
        return out.replace(anchor, anchor + '\n' + OG_IMAGE_BLOCK, 1), True
    if '</head>' in out:
        return out.replace('</head>', OG_IMAGE_BLOCK + '\n</head>', 1), True
    return out, False


def fix_retry_btn_label(out):
    """توحيد نص زرَّي العودة إلى قائمة الاختبارات.

    الزرّان بيوصّلوا لنفس المكان (level-card) فلازم يتطابقوا:
      - level-return-btn: جوّه الاختبار أثناء الأسئلة
      - retry-btn: في شاشة النتيجة بعد الانتهاء

    "أعد الاختبار" كان مضلّلًا (retryQuiz ما بتعيدش شيئًا، هي بترجّع
    القائمة)، و"مستوى" كانت ناقصة لأن القائمة فيها اختبار الترتيب
    وهو ليس مستوى. فـ"اختبار" هي الوصف الأدق والأشمل.

    اسم الدالة retryQuiz() متساب زي ما هو عن قصد — تغييره كان هيتطلّب
    تتبّع كل استدعاءاته في ٨٦ ملف بلا فايدة للمستخدم.

    idempotent: مطابقة النصوص القديمة بس.
    """
    NEW = '🔄 اختر اختباراً آخر'
    olds = (
        '>أعد الاختبار<',
        '>🔄 اختر مستوى آخر<',
        # نسخة الكيانات المرمّزة (ملفات مولّدة بـHTML entities)
        '>&#x1F504; &#x627;&#x62E;&#x62A;&#x631; &#x645;&#x633;&#x62A;&#x648;&#x649; &#x622;&#x62E;&#x631;<',
    )
    changed = False
    for old in olds:
        if old in out:
            out = out.replace(old, '>' + NEW + '<')
            changed = True
    return out, changed


def fix_confetti_on_level_end_only(out):
    """نقل الاحتفال من كل سؤال إلى نهاية المستوى.

    الاحتفال بعد كل إجابة صحيحة بيفقد قيمته بالتكرار، وبيشتّت المستخدم
    وهو بيقرأ الآية الصحيحة. الأنسب إنه يبقى مكافأة على إنهاء المستوى.

    التغيير:
      1) حذف spawnConfetti(18) من مسار الإجابة الفردية (بصيغتيه:
         المباشر والمحمي بـ typeof)
      2) إضافته في showResult() مع تدرّج حسب النتيجة:
         100% = احتفال كامل (45)، 80%+ = متوسط (22)، أقل = بدون

    ملاحظة: مستوى الترتيب بيستدعي spawnConfetti() عند اكتمال الترتيب،
    وده أصلًا نهاية المستوى مش سؤال فردي — فبيتساب زي ما هو.
    idempotent: الحارس بيمنع التكرار.
    """
    changed = False

    # ١) شيل الاحتفال من الإجابة الفردية
    for pat in (
        "if(typeof spawnConfetti==='function')spawnConfetti(18);",
        "spawnConfetti(18);",
    ):
        if pat in out:
            out = out.replace(pat, "")
            changed = True

    # ٢) حطّه في نهاية المستوى (مرة واحدة)
    if 'spawnConfetti(_cf)' not in out:
        anchor = ("function showResult(){document.getElementById('quiz-area')"
                  ".style.display='none';")
        if anchor in out:
            out = out.replace(
                anchor,
                anchor + "const _cf=(correctCount===questions.length)?45:"
                         "((correctCount/questions.length)>=0.8?22:0);"
                         "if(_cf&&typeof spawnConfetti==='function')"
                         "setTimeout(()=>spawnConfetti(_cf),260);",
                1)
            changed = True

    return out, changed


def fix_recitation_norm_hamza(path, out):
    """يوحّد قاعدة الهمزة في norm() بتاعة recitation.html.

    recitation.html مابيمرّش على fix_file()، فمابياخدش لا
    unify_normalize_rules ولا apply_canonical_functions. النتيجة إن
    norm() فضلت على الصيغة القديمة [ئؤ]→ء→'' (اللي بتحذف الهمزة على
    نبرة وعلى واو خالص) بينما الـ86 ملف اتصلّحوا لـ [ئؤ]→ا.

    الاختلاف ده بيخلي نفس الكلمة تتقارن بطريقتين مختلفين بين صفحة
    التلاوة وصفحات الاختبار — وده مخالف لقاعدة "أي تعديل على التطبيع
    يتطبّق في التلات أماكن مع بعض".

    idempotent: بعد أول تطبيق الصيغة القديمة مابقتش موجودة.
    """
    old = r".replace(/[ئؤ]/g,'ء').replace(/ء/g,'')"
    new = r".replace(/[ئؤ]/g,'ا').replace(/ء/g,'')"
    if old not in out:
        return out, False
    before = quran_text_fingerprint(out)
    out = out.replace(old, new)
    if quran_text_fingerprint(out) != before:
        print('⛔ %s: البصمة اتغيّرت — تصحيح الهمزة اتلغى'
              % os.path.basename(path))
        return out.replace(new, old), False
    RECIT_NORM_FIXED.append(os.path.basename(path))
    return out, True


def fix_pwa_paths_to_relative(out):
    """ترحيل مسارات الـPWA من مسار المستودع المطلق إلى مسارات نسبية.

    بعد ربط الدومين المخصّص quran-darbi.com بقى الموقع يُقدَّم من الجذر /
    بدل /Quran-test-/، فالمسارات المطلقة القديمة كانت هتدي 404. المسارات
    النسبية تشتغل صح على العنوانين معًا (الدومين الجديد وgithub.io).

    دالة جراحية وidempotent: تشتغل مرة واحدة ومفيش أثر لو اتكررت.
    """
    pairs = (
        ('/Quran-test-/manifest.json',      'manifest.json'),
        ('/Quran-test-/icons/',             'icons/'),
        ('/Quran-test-/service-worker.js',  'service-worker.js'),
    )
    changed = False
    for old, new in pairs:
        if old in out:
            out = out.replace(old, new)
            changed = True
    return out, changed


def fix_og_url_to_custom_domain(out):
    """تحديث og:url للدومين المخصّص (index.html فقط عمليًا).

    مطابقة حرفية للوسم بالكامل عن قصد: الرابط القديم موجود كمان جوّه
    نسخ shareApp() القديمة، واستبدال عام كان هيكسر مطابقة
    SHARE_OLD_* في مراحل لاحقة من خط الأنابيب.
    """
    old = '<meta property="og:url" content="https://quran-darbi.github.io/Quran-test-/">'
    new = '<meta property="og:url" content="https://quran-darbi.com/">'
    if old in out:
        return out.replace(old, new), True
    return out, False


MEDIUM_BLANKS_FIXED = []
RASM_SNAP_ADDED = []
SPELL_GUARD_ADDED = []
REPEAT_COUNT_FIXED = []
DAGGER_UNIFIED = []


# ============================================================
# أغسطس ٢٠٢٦ — أربع إصلاحات من مراجعة جزء عمّ
# ============================================================

_MQ_ITEM = re.compile(r'\{\s*q\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*answer\s*:\s*"((?:[^"\\]|\\.)*)"\s*\}')
_MQ_BLANK = re.compile(r'_{3,}')


def add_medium_word_count_blanks(out):
    """المستوى المتوسط: عدد مجموعات الفراغ = عدد كلمات الإجابة.

    الإجابة اللي كلمتين كانت بتتعرض بفراغ واحد، فالمستخدم مايعرفش
    إنه مطلوب منه كلمتين. بنكرّر نفس علامة الفراغ بعدد الكلمات.

    - النص القرآني ما بيتلمسش — الإبدال في علامة الفراغ بس.
    - idempotent: لو عدد الفراغات بقى مساوي لعدد الكلمات، بيتخطّى.
    """
    body, st, en = _t_array_body(out, 'MEDIUM_Q')
    if not body:
        return out, False
    hits = [0]

    def rep(m):
        q, a = m.group(1), m.group(2)
        n = len(a.split())
        blanks = _MQ_BLANK.findall(q)
        if n < 2 or len(blanks) != 1:
            return m.group(0)
        new_q = _MQ_BLANK.sub(' '.join([blanks[0]] * n), q, count=1)
        if new_q == q:
            return m.group(0)
        hits[0] += 1
        return m.group(0).replace('"' + q + '"', '"' + new_q + '"', 1)

    nb = _MQ_ITEM.sub(rep, body)
    if not hits[0]:
        return out, False
    MEDIUM_BLANKS_FIXED.append(hits[0])
    return out[:st] + nb + out[en:], True


# ------------------------------------------------------------
# محاذاة رسم التلاوة على المصحف — مسار الصوت وحده
# ------------------------------------------------------------
_SNAP_FN = r'''

/* ===== محاذاة رسم التلاوة على المصحف (الصوت فقط) =====
   محرك التعرّف بيكتب الكلمة برسم إملائي عادي: «امنهم» بدل
   «وَءَامَنَهُم»، «ترى» بدل «تَرَ». بنقارن كل كلمة منطوقة بكلمات
   *الآية الحالية وحدها*، ولو طابقت واحدة بنرجّع رسم المصحف.

   المحاذاة المتساهلة محكومة بقواعد الرسم — نطقًا لا كتابةً:
     · ىٰ  ياء عليها ألف خنجرية: تُنطق ألفًا وتُكتب ياء
     · ○  صفر مستدير (U+06DF): الحرف مكتوب رسمًا ولا يُنطق أبدًا،
          لا وصلًا ولا وقفًا  (قَالُوا۟ ، أُو۟لَٰٓئِكَ)
     · ▯  صفر مستطيل (U+06E0): الألف تثبت وقفًا وتسقط وصلًا
          (الألفات السبع، ومنها أَنَا۠)
   أي نهاية أخرى — ألف مدية، ياء متحركة، همزة — خارج القاعدة
   ولا تُحاذى إطلاقًا، فـ«إلى» لا تساوي «إلا» ولا «ولا» تساوي «ولي».
   أي مفتاح بيوصّل لأكتر من كلمة قرآنية بيتشال من الخريطة.
   normalize و wordDiff مابيتلمسوش. */
function _rasmVoiceForms(w){
  const out=[];
  if(/\u0649\u0670[^\u0621-\u064A]*$/.test(w))
    out.push(w.replace(/\u0649\u0670([^\u0621-\u064A]*)$/,'\u0627$1'));
  if(/[\u06DF\u06E0]/.test(w))
    out.push(w.replace(/[\u0627\u0648\u064A\u0649][\u06DF\u06E0]/g,''));
  return out;
}
function _rasmMaps(ans){
  const ws=String(ans||'').trim().split(/\s+/);
  const E=Object.create(null),L=Object.create(null),bE=[],bL=[];
  const put=function(map,bad,k,w){
    if(!k)return;
    if(k in map){if(map[k]!==w)bad.push(k);}else map[k]=w;
  };
  for(const w of ws){
    put(E,bE,normalize(w),w);
    const vs=_rasmVoiceForms(w);
    for(const v of vs)put(L,bL,normalize(v),w);
  }
  for(const k of bE)delete E[k];
  for(const k of bL)delete L[k];
  return {E:E,L:L};
}
function snapToRasm(words,ans){
  if(!words||!words.length||!ans)return words;
  const m=_rasmMaps(ans);
  return words.map(function(w){
    const e=normalize(w);
    if(!e)return w;
    if(e in m.E)return m.E[e];
    if(e in m.L)return m.L[e];
    return w;
  });
}
'''

_SNAP_OLD = "        return out;\n      }"
_SNAP_NEW = ("        return snapToRasm(out,(typeof q!=='undefined'&&q&&q.answer)||'');\n"
             "      }")


def add_rasm_snap_to_voice(path, out):
    """يحقن snapToRasm ويوصّلها بآخر _fixWords (مسار التسجيل الصوتي)."""
    fn = os.path.basename(path)
    if 'function _fixWords(words){' not in out:
        return out, False
    added = False
    if 'function snapToRasm(' not in out:
        anchor = 'function wordDiff(userVal,correctAnswer){'
        if anchor not in out:
            return out, False
        out = out.replace(anchor, _SNAP_FN.strip() + '\n' + anchor, 1)
        added = True
    if _SNAP_OLD in out and 'snapToRasm(out,' not in out:
        out = out.replace(_SNAP_OLD, _SNAP_NEW, 1)
        added = True
    if not added:
        return out, False
    RASM_SNAP_ADDED.append(fn)
    return out, True


# ------------------------------------------------------------
# حارس الإملاء — مسار الكتابة وحده
# ------------------------------------------------------------
_SPELL_FN = r'''
/* ===== حارس الإملاء (الكتابة فقط) =====
   «ٱلَّذِينَ» بلام واحدة هي الرسم الوحيد في المصحف، لكن تقليص
   الحروف المكرّرة جوّه normalize بيخلّي «اللذين» تعدّي كإجابة صحيحة.
   القاعدة دي لازم تفضل زي ما هي عشان التلاوة الصوتية (بتصلّح
   «إنن» → «إنَّ»)، فبدل ما نلمسها بنعلّم الكلمة المكتوبة غلط بفاصل
   صفري العرض U+200B قبل المقارنة: بيمنع التطابق من غير ما يغيّر
   شكل الكلمة قدام المستخدم. الصوت مابيمرّش من هنا فبيفضل متساهل. */
const BAD_SPELL=/^(اللذين|اللذي|اللتي|اللذان|اللذين|اللتين|اللتان|اللاتي|اللائي|اللواتي)$/;
function markBadSpelling(t){
  return String(t||'').trim().split(/\s+/).map(function(w){
    const bare=w.replace(/[\u064B-\u065F\u0610-\u061A\u06D6-\u06ED\u08F0-\u08F2\u0640\u200B-\u200F]/g,'').replace(/[آأإٱ]/g,'ا').replace(/[ىی]/g,'ي');
    return BAD_SPELL.test(bare)?w+'\u200B':w;
  }).join(' ');
}
'''


def add_typing_spell_guard(path, out):
    """يحقن markBadSpelling. توصيلها بـ checkText بيتم عبر CANON_FN."""
    fn = os.path.basename(path)
    if 'function markBadSpelling(' in out:
        return out, False
    anchor = 'function checkText(q){'
    if anchor not in out:
        return out, False
    out = out.replace(anchor, _SPELL_FN.strip() + '\n' + anchor, 1)
    SPELL_GUARD_ADDED.append(fn)
    return out, True


# ------------------------------------------------------------
# أسئلة التكرار: تصحيح المفتاح بالعدّ الفعلي من AYAT
# ------------------------------------------------------------
_U_STRIP = re.compile(r'[\u064B-\u065F\u0610-\u061A\u06D6-\u06ED\u08F0-\u08F2\u0640]')
_AR_COUNT = {'مرة واحدة': 1, 'مرتين': 2, 'مرّتين': 2}
_PREFIXES = ('', 'و', 'ف', 'ب', 'ل', 'ك')


def _u_norm_py(w):
    """تطبيع مبسّط للعدّ — كافي لمطابقة كلمة جوّه سورة واحدة."""
    w = _U_STRIP.sub('', w)
    w = re.sub(r'[آأإٱ]', 'ا', w)
    w = re.sub(r'[ىی]', 'ي', w)
    return w.replace('ة', 'ه').strip('«»()[]،. ')


def _count_word(words, target):
    """عدد مرات ورود الكلمة، مع قبول حرف عطف أو جرّ سابق (وَٱلنَّاسِ)."""
    n = 0
    for w in words:
        b = _u_norm_py(w)
        if not b.endswith(target):
            continue
        if b[:len(b) - len(target)] in _PREFIXES:
            n += 1
    return n


def _choice_count(c):
    """«5 مرات» → 5 ، «مرتين» → 2"""
    m = re.search(r'(\d+)', c)
    if m:
        return int(m.group(1))
    for k, v in _AR_COUNT.items():
        if k in c:
            return v
    return None


def fix_repeat_count_answers(path, out):
    """يصحّح مفتاح أي سؤال «كلمة تكررت كم مرة؟» بعدّها فعليًا من AYAT.

    مابيلمسش أي نص إطلاقًا — بيعدّل رقم answer بس، فبصمة النص
    القرآني بتفضل ثابتة بالحرف. idempotent بطبيعته: لو المفتاح
    مطابق للعدّ الحقيقي مايتغيّرش حاجة.
    """
    fn = os.path.basename(path)
    body, st, en = _t_array_body(out, 'EASY_Q')
    ay, _, _ = _t_array_body(out, 'AYAT')
    if not body or not ay:
        return out, False
    words = ' '.join(_T_STR.findall(ay)).split()
    hits = []

    def rep(blk):
        qm = re.search(r'q\s*:\s*"((?:[^"\\]|\\.)*)"', blk)
        cm = re.search(r'choices\s*:\s*\[([^\]]*)\]', blk)
        am = re.search(r'answer\s*:\s*(\d+)', blk)
        if not (qm and cm and am):
            return blk
        km = re.search(r'«([^»]*)»\s*تكرر', qm.group(1))
        if not km:
            return blk
        target = _u_norm_py(km.group(1))
        if not target:
            return blk
        n = _count_word(words, target)
        if not n:
            return blk
        ch = re.findall(r'"((?:[^"\\]|\\.)*)"', cm.group(1))
        want = next((i for i, c in enumerate(ch) if _choice_count(c) == n), None)
        if want is None or want == int(am.group(1)):
            return blk
        hits.append((km.group(1), int(am.group(1)), want, n))
        return re.sub(r'answer\s*:\s*\d+', 'answer:%d' % want, blk, count=1)

    nb = re.sub(r'\{[^{}]*تكرر[^{}]*\}', lambda m: rep(m.group(0)), body)
    if not hits:
        return out, False
    REPEAT_COUNT_FIXED.append((fn, hits))
    return out[:st] + nb + out[en:], True



# ------------------------------------------------------------
# توحيد الألف الخنجرية بين مصفوفات الملف الواحد
# ------------------------------------------------------------
def _dagger_key(w):
    """مفتاح يساوي بين الألف العادية والخنجرية — للمطابقة فقط."""
    return w.replace('\u0670', '\u0627')


def unify_dagger_alef_with_ayat(path, out):
    """يصحّح رسم الألف الخنجرية في EASY_Q/MEDIUM_Q من AYAT.

    بعض الأسئلة اتكتبت بألف عادية (ٱلصَّٰلِحَاتِ) بينما المصحف وAYAT
    وHARD_Q فيهم الخنجرية (ٱلصَّٰلِحَٰتِ). الدالة بتاخد الرسم من AYAT
    نفسها — مصدر النص الموثّق جوّه الملف — مش من أي مكان تاني.

    بتمشي كلمة كلمة على أسئلة السهل والمتوسط وتقارن بمفتاح بيساوي
    بين ٱ0627 وٱ0670، فبتمسك حتى الأشكال المختلطة (خنجرية على حرف
    وعادية على حرف تاني في نفس الكلمة).

    · الإبدال بيحصل بس لو الكلمتين متطابقتين حرفًا بحرف بعد التسوية،
      يعني الفرق في نوع الألف وحده لا غير.
    · أي مفتاح بيوصّل لأكتر من رسم في AYAT بيتشال — مفيش تخمين.
    · المقارنة ما بتتأثرش: normalize بتحوّل الاتنين لألف واحدة.
    """
    fn_name = os.path.basename(path)
    ay, _, _ = _t_array_body(out, 'AYAT')
    if not ay:
        return out, False

    forms, dup = {}, set()
    for s in _T_STR.findall(ay):
        for w in s.split():
            w = w.strip('«»()[]،.')
            if '\u0670' not in w:
                continue
            k = _dagger_key(w)
            if k in forms and forms[k] != w:
                dup.add(k)
            else:
                forms[k] = w
    for k in dup:
        forms.pop(k, None)
    if not forms:
        return out, False

    hits, changed = [], False
    for name in ('EASY_Q', 'MEDIUM_Q'):
        body, st, en = _t_array_body(out, name)
        if not body:
            continue

        def repl(m):
            s = m.group(1)
            parts = s.split(' ')
            for idx, tok in enumerate(parts):
                core = tok.strip('«»()[]،.…؟')
                if not core:
                    continue
                right = forms.get(_dagger_key(core))
                if right and right != core:
                    parts[idx] = tok.replace(core, right, 1)
                    hits.append((name, core, right))
            return '"' + ' '.join(parts) + '"'

        nb = _T_STR.sub(repl, body)
        if nb != body:
            out = out[:st] + nb + out[en:]
            changed = True

    if not changed:
        return out, False
    DAGGER_UNIFIED.append((fn_name, hits))
    return out, True


RECIT_BTN_ADDED = []
RECIT_BTN_SKIPPED = []

# نفس تصميم الزر الموجود في سور جزء عمّ حرفيًا (alghasiya نموذجًا)
_RECIT_BTN_TPL = (
    '<div style="margin:0 16px 16px;">\n'
    '  <a href="recitation.html?surah=%s" style="display:flex;'
    'align-items:center;justify-content:center;gap:8px;'
    'background:var(--surface2);border:1.5px solid var(--border);'
    'border-radius:14px;padding:13px 20px;font-size:16px;'
    'font-family:inherit;color:var(--accent);text-decoration:none;">\n'
    '    🎤 اختبر تلاوتك\n'
    '  </a>\n'
    '</div>\n\n'
)

_RECIT_ANCHOR = '<div class="level-card" id="level-card">'


def _recit_key_for(filename):
    """مفتاح السورة/الصفحة في recitation.html من اسم الملف."""
    base = os.path.basename(filename)
    if base.endswith('.html'):
        base = base[:-5]
    if base.startswith('albaqara_p'):
        return 'baqara_p' + base[len('albaqara_p'):]
    if base == 'alfatiha':
        return 'fatiha'
    return base


def _recit_available_keys(root):
    """مفاتيح TEXTS الموجودة فعليًا في recitation.html."""
    rp = os.path.join(root, 'recitation.html')
    if not os.path.isfile(rp):
        return None
    with open(rp, encoding='utf-8') as f:
        rec = f.read()
    m = re.search(r'TEXTS\s*=\s*\{', rec)
    if not m:
        return None
    i, d = m.end() - 1, 0
    while i < len(rec):
        if rec[i] == '{':
            d += 1
        elif rec[i] == '}':
            d -= 1
            if d == 0:
                break
        i += 1
    return set(re.findall(r'([A-Za-z0-9_]+)\s*:\s*`', rec[m.end():i]))


def add_recitation_button(path, out):
    """يضيف زر 🎤 اختبر تلاوتك قبل بطاقة اختيار المستوى.

    جراحي وidempotent: لو الزر موجود بالفعل مايعملش حاجة، ولو المفتاح
    مش موجود في recitation.html بيتخطّى الملف بدل ما يضيف رابط مكسور.
    """
    fn = os.path.basename(path)

    # موجود بالفعل — مافيش تغيير
    if 'recitation.html?surah=' in out:
        return out, False

    # نقطة الإدراج مش موجودة — قالب مختلف، اتساب زي ما هو
    if _RECIT_ANCHOR not in out:
        RECIT_BTN_SKIPPED.append((fn, 'نقطة الإدراج غير موجودة'))
        return out, False

    key = _recit_key_for(fn)

    root = os.path.dirname(os.path.abspath(path))
    keys = _recit_available_keys(root)
    if keys is not None and key not in keys:
        RECIT_BTN_SKIPPED.append((fn, 'المفتاح %s غير موجود في recitation.html' % key))
        return out, False

    new = out.replace(_RECIT_ANCHOR,
                      (_RECIT_BTN_TPL % key) + _RECIT_ANCHOR, 1)
    if new == out:
        RECIT_BTN_SKIPPED.append((fn, 'فشل الإدراج'))
        return out, False

    RECIT_BTN_ADDED.append((fn, key))
    return new, True


BLANKS_FIXED = []
BLANKS_SKIPPED = []

_BLANK_STD = '_____'


def fix_medium_blank_count(path, out):
    """يخلّي عدد فراغات _____ في سؤال المتوسط مطابقًا لعدد كلمات الإجابة.

    المستخدم بيشوف الفراغ فبيعرف كام كلمة مطلوبة. لو الإجابة كلمتين
    والفراغ واحد، بيكتب كلمة واحدة ويتحسب عليه غلط.

    جراحي: بيمسّ نص السؤال (q) بس، ومابيقربش للإجابة ولا للنص القرآني.
    idempotent: لو العدد مطابق أصلاً مايعملش حاجة.
    """
    fn = os.path.basename(path)

    m = re.search(r'(?:const|let|var)\s+MEDIUM_Q\s*=\s*\[', out)
    if not m:
        return out, False

    # حدود المصفوفة
    i = m.end() - 1
    depth = 0
    quote = None
    while i < len(out):
        c = out[i]
        if quote:
            if c == '\\':
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in '"\'`':
            quote = c
        elif c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                break
        i += 1
    else:
        return out, False

    start, end = m.end(), i
    body = out[start:end]
    hits = []

    def repl_obj(match):
        obj = match.group(0)
        qm = re.search(r'q\s*:\s*"((?:[^"\\]|\\.)*)"', obj)
        am = re.search(r'answer\s*:\s*"((?:[^"\\]|\\.)*)"', obj)
        if not qm or not am:
            return obj
        q, a = qm.group(1), am.group(1)
        need = len(a.split())
        have = re.findall(r'_+', q)
        if need < 1 or len(have) == need:
            return obj
        # لازم يكون فيه فراغ واحد بالظبط عشان نوسّعه بأمان؛
        # أي حالة تانية بتتساب للمراجعة اليدوية
        if len(have) != 1:
            BLANKS_SKIPPED.append((fn, a, '%d فراغ' % len(have)))
            return obj
        new_q = q.replace(have[0], ' '.join([_BLANK_STD] * need), 1)
        hits.append((a, 1, need))
        return obj.replace(qm.group(0), 'q:"' + new_q + '"', 1)

    new_body = re.sub(r'\{[^{}]*\}', repl_obj, body)
    if not hits:
        return out, False

    BLANKS_FIXED.append((fn, hits))
    return out[:start] + new_body + out[end:], True


NEXTBTN_FIXED = []

def fix_next_btn_display(path, out):
    """يصلّح ظهور زر «السؤال التالي» بعد الإجابة.

    الباگ: كلاس .next-btn في الـCSS فيه display:none، والكود كان بيعمل
    _nx.style.display='' — والقيمة الفاضية بتمسح النمط السطري فالعنصر
    بيرجع لـ display:none بتاعة الكلاس، يعني الزر يفضل مخفي.
    الحل: قيمة صريحة 'block' زي ما checkMCQ بيعمل بالظبط.
    idempotent: لو متصلَّح خلاص مايعملش حاجة.
    """
    old = "if(_nx)_nx.style.display='';"
    new = "if(_nx)_nx.style.display='block';"
    if old not in out:
        return out, False
    n = out.count(old)
    out = out.replace(old, new)
    NEXTBTN_FIXED.append((os.path.basename(path), n))
    return out, True


# قاعدة قاتلة جوّه دالة nm (المقارنة كلمة-كلمة في wordDiff):
# تحويل الألف في آخر الكلمة إلى ياء. بتخلي كلمات قرآنية مختلفة
# تبقى متساوية عند المقارنة:
#     إِلَىٰ = إِلَّا   |   شَآءَ = شَىْءٍ
#     وَلَا = وَلِيࣲّ    |   أَذࣰى = إِذَا   |   أَنَا۠ = أَنَّىٰ
# وبما إن شرط القبول في checkTextVal فيه OR على نتيجة nm:
#     _ok = (userNorm===ansNorm) || (matched===total && !extra)
# فالكلمة الغلط كانت بتعدّي و«إجابة صحيحة تماماً» تظهر للمستخدم.
# مؤكَّد عمليًا: albaqara_p47 آية الربا — كتابة «إِلَّا» مكان
# «إِلَى ٱللَّهِ» كانت بتترصد ٤٥/٤٥ وتتقبل.
NM_FINAL_ALEF_RULE = ".replace(/\u0627(?=\\s|$)/g,'\u064a')"


def drop_nm_final_alef_rule(path, out):
    """يشيل قاعدة (ألف آخر الكلمة → ياء) من nm جوّه wordDiff فقط.

    · لا تمسّ أي نص قرآني إطلاقًا — تعديل داخل دالة مقارنة.
    · لا تمسّ normalize ولا nm خارج wordDiff.
    · idempotent: لو القاعدة مش موجودة بترجع (out, False).
    """
    i = out.find('function wordDiff(')
    if i < 0:
        return out, False
    j = out.index('{', i)
    depth, k = 0, j
    while k < len(out):
        if out[k] == '{':
            depth += 1
        elif out[k] == '}':
            depth -= 1
            if depth == 0:
                break
        k += 1
    body = out[i:k + 1]
    if NM_FINAL_ALEF_RULE not in body:
        return out, False
    before = quran_text_fingerprint(out)
    new = out[:i] + body.replace(NM_FINAL_ALEF_RULE, '') + out[k + 1:]
    if quran_text_fingerprint(new) != before:      # حارس: مستحيل يحصل
        return out, False
    return new, True


def upgrade_rasm_voice_rules(path, out):
    """يرقّي محاذاة الصوت للنسخة المحكومة بقواعد الرسم.

    القديمة كانت بتشيل آخر حرف [اي] من *كل* كلمة، فبتخلط بين
    كلمات مختلفة رسمًا ونطقًا:
        «ولا» → «وَلِيࣲّ»   |   «إلى» → «إِلَّا»
    الجديدة بتحاذي بس لما القاعدة تسمح فعلًا (ىٰ ، ○ ، ▯).
    لا تمسّ نصًا قرآنيًا — دوال محاذاة فقط.
    """
    if 'function _rasmMaps(' not in out or 'function snapToRasm(' not in out:
        return out, False
    if 'function _rasmVoiceForms(' in out:      # مرقّاة خلاص
        return out, False
    start = out.index('function _rasmMaps(')
    end = out.index('function snapToRasm(')
    depth, k = 0, out.index('{', end)
    while k < len(out):
        if out[k] == '{':
            depth += 1
        elif out[k] == '}':
            depth -= 1
            if depth == 0:
                break
        k += 1
    before = quran_text_fingerprint(out)
    new = out[:start] + _SNAP_FN.strip() + out[k + 1:]
    if quran_text_fingerprint(new) != before:      # حارس
        return out, False
    return new, True


_REC_VOICE_FN = r'''
/* قواعد الرسم في المحاذاة الصوتية — نطقًا لا كتابةً:
     · ىٰ  ياء عليها ألف خنجرية: تُنطق ألفًا وتُكتب ياء
     · ○  صفر مستدير (U+06DF): مكتوب رسمًا ولا يُنطق أبدًا
     · ▯  صفر مستطيل (U+06E0): يثبت وقفًا ويسقط وصلًا
   أي نهاية أخرى (ألف مدية، ياء متحركة، همزة) خارج القاعدة. */
function _rasmVoiceForms(w){
  const out=[];
  if(/\u0649\u0670[^\u0621-\u064A]*$/.test(w))
    out.push(w.replace(/\u0649\u0670([^\u0621-\u064A]*)$/,'\u0627$1'));
  if(/[\u06DF\u06E0]/.test(w))
    out.push(w.replace(/[\u0627\u0648\u064A\u0649][\u06DF\u06E0]/g,''));
  return out;
}
function _rasmMatch(refWord,refNorm,u){
  if(refNorm===u)return true;
  const vs=_rasmVoiceForms(refWord);
  for(const v of vs)if(norm(v)===u)return true;
  return false;
}
'''


def upgrade_recitation_rasm_rules(out):
    """نفس القواعد داخل snapWordsToRasm في recitation.html.

    كانت بتطابق تطابقًا تامًا بعد norm فقط، فـ«الأعلا» بتترفض رغم
    إن النطق سليم (ىٰ تُنطق ألفًا).
    """
    if 'function snapWordsToRasm(' not in out:
        return out, False
    if 'function _rasmVoiceForms(' in out:      # مرقّاة خلاص
        return out, False
    old_a = 'dp[i][j]=(R[i-1]===U[j-1])?dp[i-1][j-1]+1:Math.max(dp[i-1][j],dp[i][j-1]);'
    old_b = 'if(R[i-1]===U[j-1]){out[j-1]=refWords[i-1];i--;j--;}'
    if old_a not in out or old_b not in out:
        return out, False
    before = quran_text_fingerprint(out)
    new = out.replace(
        old_a,
        'dp[i][j]=_rasmMatch(refWords[i-1],R[i-1],U[j-1])'
        '?dp[i-1][j-1]+1:Math.max(dp[i-1][j],dp[i][j-1]);', 1)
    new = new.replace(
        old_b,
        'if(_rasmMatch(refWords[i-1],R[i-1],U[j-1])){'
        'out[j-1]=refWords[i-1];i--;j--;}', 1)
    new = new.replace('function snapWordsToRasm(',
                      _REC_VOICE_FN.strip() + '\nfunction snapWordsToRasm(', 1)
    if quran_text_fingerprint(new) != before:      # حارس
        return out, False
    return new, True


def port_rasm_snap_to_legacy_voice(path, out):
    """ينقل محاذاة الرسم لصفحات القالب الصوتي الأقدم.

    الصفحتان دول (الغاشية والمطففين) بيوصّلوا مخرجات المحرك لـ_words
    مباشرة من غير أي محاذاة، فالتسجيل بيفشل في أغلب الكلمات.
    بنحقن snapToRasm ونمرّر عليها الكلمات في الموضعين (onresult, onend).
    لا تمسّ نصًا قرآنيًا.
    """
    if 'function _mkRec(){' not in out:
        return out, False
    if 'function snapToRasm(' in out:            # عندها المحاذاة خلاص
        return out, False
    if 'function collapseMuqattaat(' not in out or 'function wordDiff(' not in out:
        return out, False

    on_result = ('_words=_words.concat(e.results[i][0].transcript'
                 '.trim().split(/\\s+/).filter(Boolean));')
    on_end = ("if(_cur){_words=_words.concat(_cur.trim()"
              ".split(/\\s+/).filter(Boolean));_cur='';}")
    if out.count(on_result) != 1 or out.count(on_end) != 1:
        return out, False

    before = quran_text_fingerprint(out)
    new = out.replace('function wordDiff(',
                      _SNAP_FN.strip() + '\nfunction wordDiff(', 1)
    fixw = (
        "  function _fixWords(words){\n"
        "    const _a=(typeof q!=='undefined'&&q&&q.answer)||'';\n"
        "    return snapToRasm(collapseMuqattaat(words,_a),_a);\n"
        "  }\n")
    new = new.replace('  function _mkRec(){', fixw + '  function _mkRec(){', 1)
    new = new.replace(
        on_result,
        '_words=_fixWords(_words.concat(e.results[i][0].transcript'
        '.trim().split(/\\s+/).filter(Boolean)));', 1)
    new = new.replace(
        on_end,
        "if(_cur){_words=_fixWords(_words.concat(_cur.trim()"
        ".split(/\\s+/).filter(Boolean)));_cur='';}", 1)
    if quran_text_fingerprint(new) != before:      # حارس
        return out, False
    return new, True


def add_ayah_marks_to_transcript(out):
    """يضيف فواصل الآيات ﴿١﴾ في منطقة الكلمات المسجّلة (عرض فقط).

    الفواصل بتتضاف كـspan مستقل في renderTranscript، ومابتدخلش
    مصفوفة savedWords إطلاقًا — فالتصحيح والمقارنة مايشوفوهاش.
    بتستفيد من ayahBounds/refWords الموجودين خلاص.
    """
    if 'function renderTranscript(){' not in out:
        return out, False
    if 'function _savedToRefIdx(' in out:      # مضافة خلاص
        return out, False
    anchor = ("    sp.onclick=()=>{selWord=(selWord===i)?null:i;"
              "renderTranscript();updateBtns();};\n"
              "    box.appendChild(sp);\n  });")
    if out.count(anchor) != 1 or out.count('function renderTranscript(){') != 1:
        return out, False

    helpers = r'''
/* ===== فواصل الآيات في منطقة التسجيل (عرض فقط) =====
   بنحاذي كلمات المستخدم على refWords بمشية أمامية، وبنحط ﴿رقم﴾
   بعد الكلمة اللي بتقفل الآية. مافيش أي أثر على savedWords ولا على
   المقارنة — دي عناصر عرض بحتة. */
function _savedToRefIdx(){
  const map=new Array(savedWords.length).fill(-1);
  if(!refWords.length)return map;
  let p=0;
  for(let i=0;i<savedWords.length;i++){
    const u=norm(savedWords[i]);
    if(!u)continue;
    for(let k=p;k<refWords.length&&k<p+8;k++){
      if(norm(refWords[k])===u){map[i]=k;p=k+1;break;}
    }
  }
  return map;
}
function _ayahEndMap(){
  const m=Object.create(null);
  if(!ayahBounds.length||!refWords.length)return m;
  for(let j=0;j<ayahBounds.length;j++){
    const nx=(j+1<ayahBounds.length)?ayahBounds[j+1].start:refWords.length;
    if(nx-1>=0)m[nx-1]=ayahBounds[j].num;
  }
  return m;
}
function _ayahSepEl(num){
  const ar='\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669';
  const toAr=n=>String(n).split('').map(d=>ar[+d]).join('');
  const el=document.createElement('span');
  el.className='ayah-num';
  el.setAttribute('translate','no');
  el.style.cssText='margin:2px 4px;align-self:center;';
  el.textContent='\uFD3F'+toAr(num)+'\uFD3E';
  return el;
}
'''
    new = out.replace('function renderTranscript(){',
                      helpers.strip() + '\nfunction renderTranscript(){', 1)
    new = new.replace(anchor,
                      "    sp.onclick=()=>{selWord=(selWord===i)?null:i;"
                      "renderTranscript();updateBtns();};\n"
                      "    box.appendChild(sp);\n"
                      "    if(_refMap[i]>=0&&_ayEnd[_refMap[i]]!==undefined)"
                      "box.appendChild(_ayahSepEl(_ayEnd[_refMap[i]]));\n  });", 1)
    new = new.replace("  const _g=muqGroupLen();\n  savedWords.forEach((w,i)=>{",
                      "  const _g=muqGroupLen();\n"
                      "  const _refMap=_savedToRefIdx(),_ayEnd=_ayahEndMap();\n"
                      "  savedWords.forEach((w,i)=>{", 1)
    if 'const _refMap=_savedToRefIdx()' not in new:
        return out, False
    return new, True


def fix_file(path):
    with open(path, encoding='utf-8') as f:
        src = f.read()
    out = ar2en(src)

    # ترحيل مسارات الـPWA للنسبي (بعد ربط الدومين المخصّص)
    out, _pwa_rel = fix_pwa_paths_to_relative(out)
    out, _canon = fix_add_canonical(path, out)
    out, _cf = fix_confetti_on_level_end_only(out)
    out, _rtl = fix_retry_btn_label(out)
    out, _recbtn = add_recitation_button(path, out)
    out, _blanks = fix_medium_blank_count(path, out)
    out, _nxb = fix_next_btn_display(path, out)

    # ====================================================
    # ترحيل صفحات البقرة لقالب جزء عمّ النضيف — أول خطوة قبل أي حاجة
    # تانية. لو نجح الترحيل، الملف الجديد مبني نظيف من الأول ومحتاجش
    # أي رقعة من الرقعات القديمة تحت، فبنرجع فورًا. لو اتخطّى (مش
    # بقرة، أو صيغة مش مدعومة، أو HARD_Q ناقصة، أو فشل التحقق الحرفي)
    # كمّل على باقي خط الأنابيب القديم زي ما هو بالظبط.
    migrated_out, migrated = migrate_baqara_to_clean_template(path, out)
    if migrated:
        # الملف المرحَّل بيخرج فورًا من غير باقي خط الأنابيب، فبنضيفله
        # لوحة شرح الترتيب هنا عشان مايستناش تشغيلة جاية
        migrated_out, _ = add_order_help_panel(migrated_out)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(migrated_out)
        return True

    # ====================================================
    # 0أ. أرقام الآيات الحقيقية في عرض المصحف (مستوى الترتيب) —
    #     للصفحات اللي اتحوّلت للقالب النضيف في تشغيلات سابقة.
    out, _ayahnum_fixed = fix_baqara_mushaf_ayah_numbers(path, out)

    # ====================================================
    # -1. تصحيح صيغة الأمر المؤنث لمذكر رسمي (يوليو ٢٠٢٦):
    #    بعض أسئلة "الصعب" في دفعة قديمة من صفحات البقرة كانت بصيغة
    #    "اكتبي" (مؤنث) بدل "اكتب" — مخالف لقاعدة الذكر الرسمي فصحى.
    #    الكلمة دي بس تظهر في نص التعليمات اللي كتبناه احنا، مش في
    #    القرآن نفسه، فالاستبدال المباشر آمن ومايلمسش النص القرآني.
    out = out.replace('اكتبي', 'اكتب')

    # إصلاح تحميل خط Google Fonts البطيء (@import → <link>)
    out, _font_fixed = fix_font_import_to_link(out)

    # إصلاح تراكب/تجاوز قائمة الأدوات ولون "العربية"
    out, _tools_ui_fixed = fix_tools_menu_ui_bugs(out)

    # ترتيب اللغات + علامة ✓ بدل التلوين الأخضر بس
    out, _lang_list_fixed = fix_lang_list_order_and_checkmark(out)

    # توضيح شكل وتسمية زر تنقل الصفحات (بين السور) عشان مايتلخبطش مع
    # زر تنقل الأسئلة
    out, _page_nav_fixed = fix_page_nav_style_and_labels(out)

    # محاذاة كروت المستوى (سهل/متوسط/صعب/ترتيب) + لون أيقونة "ترتيب"
    out, _level_card_fixed = fix_level_card_alignment(out)

    # ترقية أيقونة "ترتيب" من إيموجي 🔀 (لونه بيختلف حسب نظام كل جهاز)
    # لـSVG بلون أخضر ثابت مطابق تمامًا في كل الأجهزة (يوليو ٢٠٢٦)
    out, _order_icon_unified = unify_order_icon_style(out)

    # إصلاح رابط 404 (alfatiha_p1.html الغلط بدل alfatiha.html)
    out, _fatiha_link_fixed = fix_alfatiha_broken_link(out)

    # تقصير وصف مستوى "صعب" لو لسه بالنسخة الطويلة القديمة
    out, _hard_desc_fixed = fix_hard_level_desc(out)


    # توضيح تسمية زر تنقل الأسئلة + إخفاء زر تنقل الصفحات جوه الاختبار
    # إلا عند آخر سؤال
    out, _qnav_fixed = fix_question_nav_and_page_nav_visibility(out)

    # نفس الفكرة بس لقالب صفحات البقرة (بنية مختلفة عن جزء عم)
    out, _baqara_nav_fixed = fix_baqara_page_nav_placement(out)
    out, _baqara_nav_js_fixed = fix_baqara_page_nav_visibility_js(out)

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

    # ====================================================
    # 0ب. حذف قاعدة قديمة مكسورة (يوليو ٢٠٢٦): بعض الملفات القديمة فيها
    #      قاعدة إضافية زيادة .replace(/ـ[كشيدة+حركة]*[همزة]/g,'ا') بتحوّل
    #      كشيدة+كسرة+همزة لألف بدل ما تتحذف، فبتخلي كلمة زي "ٱلۡأَفۡـِٔدَةِ"
    #      (الافئدة) تتحسب غلط لأنها بتتفرد عن الشكل اللي المستخدم بيكتبه
    #      عادي. القاعدة دي زيادة عن الحاجة أصلاً (فيه قاعدة تانية أصح
    #      بتحذفها تمامًا شوية سطور تحت) فبنشيلها بالكامل.
    BROKEN_KASHIDA_HAMZA_RULE = r".replace(/ـ[\u064B-\u065F]*[\u0654\u0655]/g,'ا')"
    if BROKEN_KASHIDA_HAMZA_RULE in out:
        out = out.replace(BROKEN_KASHIDA_HAMZA_RULE, "")

    # ====================================================
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
    # نسخة أحدث (يوليو ٢٠٢٦ الجزء ٢): بتستخدم lookbehind بدل ^ عشان تشتغل مع أي كلمة
    # في وسط الجملة مش بس أول كلمة (المستوى الصعب بيتحقق من الآية كاملة مش كلمة كلمة)
    # + إضافة شرب/صفح/تخذ (واشربوا، واصفحوا، واتخذوا)
    NEWEST_WA_RULE = r".replace(/(?<=^|\s)وا(?=سجد|قترب|دخل|دعو|ذكر|رحم|ستغفر|ستغن|غفر|عف|نحر|تق|ختلاف|مر[أا]|تبع|سمع|ستكبر|ستعين|ركع|صبر|صل|جتنب|هبط|ستبشر|ستقم|ضرب|عتصم|ئتلف|بتغ|حذر|شرب|صفح|تخذ)/g,'و')"
    if OLD_WA_RULE in out:
        out = out.replace(OLD_WA_RULE, NEWEST_WA_RULE)
    elif NEW_WA_RULE in out:
        out = out.replace(NEW_WA_RULE, NEWEST_WA_RULE)
    elif NEWER_WA_RULE in out:
        out = out.replace(NEWER_WA_RULE, NEWEST_WA_RULE)
    elif r"وٱ(?!ل)/g,'و')" in out and r"^وا(?=" not in out and r"|\s)وا(?=" not in out:
        # ملفات فيها وٱ(?!ل) بس من غير قاعدة وا خالص (زي annaba.html) —
        # فضلت ماشية على واتبعوا/واسمعوا غلط لأنها مش من غير القاعدة أصلاً
        out = out.replace(
            r".replace(/وٱ(?!ل)/g,'و')",
            r".replace(/وٱ(?!ل)/g,'و')" + NEWEST_WA_RULE,
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
    SHARE_FN = """function shareApp(){var url=location.href;var t=document.title||'دربي لحفظ القرآن';if(navigator.share){navigator.share({title:t,url:url}).catch(function(){});}else if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){var b=document.getElementById('tools-fab-btn');if(b){var old=b.textContent;b.textContent='✅';setTimeout(function(){b.textContent=old;},1800);}}).catch(function(){});}}"""
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
        btn = '\n  <button class="level-return-btn" onclick="returnToLevels()">🔄 اختر اختباراً آخر</button>'
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
        "    .replace(/ـۧ/g,'ي')\n"
        "    .replace(/يٓ?ـَٔ/g,'ي')\n"
        "    .replace(/ـَٔ/g,'ا')\n"
        "    .replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'')\n"
        "    .replace(/ـ/g,'')\n"
        "    .replace(/[ًٌٍَؘُؙِؚّْٕٖٜٟۣ۪ۭٓٔٗ٘ٙٚٛٝٞؐؑؒؓؔؕؖؗۖۗۘۙۚۛۜ۟۠ۡۢۤۧۨ۫۬]/g,'')\n"
        "    .replace(/ها[ؤو]لاء|ها[ؤو]لا(?!\\S)/g,'هالا').replace(/ه[ؤو]لاء|ه[ؤو]لا(?!\\S)/g,'هالا')\n"
        "    .replace(/وٱ(?!ل)/g,'و')\n"
        "    " + NEWEST_WA_RULE + "\n"
        "    .replace(/وٰ(?=ة)/g,'ا').replace(/وٰ/g,'وا')\n"
        "    .replace(/اٰ/g,'ا').replace(/يٰ/g,'يا')\n"
        "    .replace(/نٰ/g,'نا')\n"
        "    .replace(/(?<=^|\\s)بلىٰ(?=\\s|$)/g,'بلا')\n"
        "    .replace(/ىٰ(?=\\S)/g,'ا').replace(/ىٰ/g,'ي')\n"
        "    .replace(/(.)ٰ/g,'$1ا')\n"
        "    .replace(/هۥ/g,'ه').replace(/هۦ/g,'ه')\n"
        "    .replace(/ۦ(?=\\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'')\n"
        "    .replace(/ه[ۥۦ]/g,'ه')\n"
        "    .replace(/[ئؤ]/g,'ا').replace(/ء/g,'')\n"
        "    .replace(/[آأإٱا]/g,'ا')\n"
        "    .replace(/[ىی]/g,'ي')\n"
        "    .replace(/ة/g,'ه')\n"
        "    .replace(/(?<=^|\\s)ممنع(?=\\s|$)/g,'ممن منع')\n"
        "    .replace(/(.)\\1+/g,'$1')\n"
        "    .replace(/رحمان/g,'رحمن')\n"
        "    .replace(/مولانا/g,'مولنا').replace(/يا ?ايها/g,'يايها').replace(/يا ?ايتها/g,'يايتها')\n"
        "    .replace(/الاه/g,'اله').replace(/ارايت/g,'اريت')\n"
        "    .replace(/هاذا/g,'هذا').replace(/هاذه/g,'هذه').replace(/ذالك/g,'ذلك').replace(/لاكن/g,'لكن')\n"
        "    .replace(/(?<=^|\\s)فازالهما(?=\\s|$)/g,'فازلهما')\n"
        "    .replace(/(?<=^|\\s)فاذلهما(?=\\s|$)/g,'فازلهما')\n"
        "    .replace(/(?<=^|\\s)فادراتم(?=\\s|$)/g,'فادارتم').replace(/(?<=^|\\s)فادرأتم(?=\\s|$)/g,'فادارتم').replace(/(?<=^|\\s)فاداراتم(?=\\s|$)/g,'فادارتم')\n"
        "    .replace(/(?<=^|\\s)بن(?=\\s|$)/g,'ابن')\n"
        "    .replace(/نصاري(?=\\s|$)/g,'نصارا')\n"
        "    .replace(/(?<=^|\\s)ناتي(?=\\s|$)/g,'نات')\n"
        "    .replace(/(?<=^|\\s)ولا تجدنهم(?=\\s|$)/g,'ولتجدنهم').replace(/(?<=^|\\s)ولاتجدنهم(?=\\s|$)/g,'ولتجدنهم')\n"
        "    .replace(/(?<=^|\\s)او كل ما(?=\\s|$)/g,'اوكلما').replace(/(?<=^|\\s)او كلما(?=\\s|$)/g,'اوكلما')\n"
        "    .replace(/(?<=^|\\s)بلي(?=\\s|$)/g,'بلا')\n"
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
            "    if (currentLevel === 'hard') {\n"
            "      const __qi = qIndex;\n"
            "      setTimeout(() => { if (qIndex === __qi) nextQuestion(); }, 1100);\n"
            "    }\n"
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
    # 7د. ترقية idempotent لـnormalize() الموجودة أصلاً (اللي اتصلحت في تشغيلة
    #      سابقة ومروحتش على مسار إعادة البناء الكامل فوق) — نفس إصلاحات
    #      يوليو ٢٠٢٦ الجزء ٢: الياء المعكوفة، بلىٰ، نصارى، ناتي، فأزلهما،
    #      فادراتم، ابن، ولتجدنهم، أوكلما، ممنع (مِمَّن مَّنَعَ)
    if 'function normalize(' in out:
        # الياء المعكوفة (ـۧ) = ي مدية — لازم قبل قواعد حذف الكشيدة
        if ".replace(/ـۧ/g,'ي')" not in out and ".replace(/يٓ?ـَٔ/g,'ي')" in out:
            out = out.replace(
                ".replace(/يٓ?ـَٔ/g,'ي')",
                ".replace(/ـۧ/g,'ي').replace(/يٓ?ـَٔ/g,'ي')",
                1
            )
        # بَلَىٰ: استثناء خاص قبل قاعدة ىٰ العامة — لازم يتحط قبلها بالظبط
        if "بلىٰ" not in out and ".replace(/ىٰ(?=\\S)/g,'ا').replace(/ىٰ/g,'ي')" in out:
            out = out.replace(
                ".replace(/ىٰ(?=\\S)/g,'ا').replace(/ىٰ/g,'ي')",
                ".replace(/(?<=^|\\s)بلىٰ(?=\\s|$)/g,'بلا').replace(/ىٰ(?=\\S)/g,'ا').replace(/ىٰ/g,'ي')",
                1
            )
        # مِمَّن مَّنَعَ: لازم تتفكك قبل قاعدة دمج الحروف المتكررة (.)\1+ وإلا هتتاكل
        if "ممن منع" not in out and ".replace(/(.)\\1+/g,'$1')" in out:
            out = out.replace(
                ".replace(/(.)\\1+/g,'$1')",
                ".replace(/(?<=^|\\s)ممنع(?=\\s|$)/g,'ممن منع').replace(/(.)\\1+/g,'$1')",
                1
            )
        # باقي الاستثناءات: تتحط بعد أي علامة ثابتة موجودة في كل نسخ normalize()
        if "فازالهما" not in out and ".replace(/رحمان/g,'رحمن')" in out:
            EXTRA_ALIASES = (
                ".replace(/(?<=^|\\s)فازالهما(?=\\s|$)/g,'فازلهما')"
                ".replace(/(?<=^|\\s)فاذلهما(?=\\s|$)/g,'فازلهما')"
                ".replace(/(?<=^|\\s)فادراتم(?=\\s|$)/g,'فادارتم').replace(/(?<=^|\\s)فادرأتم(?=\\s|$)/g,'فادارتم').replace(/(?<=^|\\s)فاداراتم(?=\\s|$)/g,'فادارتم')"
                ".replace(/(?<=^|\\s)بن(?=\\s|$)/g,'ابن')"
                ".replace(/نصاري(?=\\s|$)/g,'نصارا')"
                ".replace(/(?<=^|\\s)ناتي(?=\\s|$)/g,'نات')"
                ".replace(/(?<=^|\\s)ولا تجدنهم(?=\\s|$)/g,'ولتجدنهم').replace(/(?<=^|\\s)ولاتجدنهم(?=\\s|$)/g,'ولتجدنهم')"
                ".replace(/(?<=^|\\s)او كل ما(?=\\s|$)/g,'اوكلما').replace(/(?<=^|\\s)او كلما(?=\\s|$)/g,'اوكلما')"
                ".replace(/(?<=^|\\s)بلي(?=\\s|$)/g,'بلا')"
            )
            out = out.replace(
                ".replace(/رحمان/g,'رحمن')",
                ".replace(/رحمان/g,'رحمن')" + EXTRA_ALIASES,
                1
            )
        # فاذلهما: قد تكون مضافة لملفات جديدة (السطر فوق) لكن ناقصة من ملفات
        # اتصلحت في تشغيلة سابقة قبل ما تُكتشف هذه الصيغة (يوليو ٢٠٢٦ الجزء ٣)
        if "فاذلهما" not in out and ".replace(/(?<=^|\\s)فازالهما(?=\\s|$)/g,'فازلهما')" in out:
            out = out.replace(
                ".replace(/(?<=^|\\s)فازالهما(?=\\s|$)/g,'فازلهما')",
                ".replace(/(?<=^|\\s)فازالهما(?=\\s|$)/g,'فازلهما').replace(/(?<=^|\\s)فاذلهما(?=\\s|$)/g,'فازلهما')",
                1
            )
        # بلي: العرض دلوقتي بيصحح "بلا" لـ"بلى" (يوليو ٢٠٢٦ الجزء ٤) فمحتاجين
        # نتأكد إن "بلي" (بعد قاعدة ى→ي العامة) برضه توصل لنفس مرجع بَلَىٰ
        if "بلي(?=\\s|$)" not in out:
            marker = ".replace(/(?<=^|\\s)او كل ما(?=\\s|$)/g,'اوكلما').replace(/(?<=^|\\s)او كلما(?=\\s|$)/g,'اوكلما')"
            if marker in out:
                out = out.replace(
                    marker,
                    marker + ".replace(/(?<=^|\\s)بلي(?=\\s|$)/g,'بلا')",
                    1
                )
        # فادراتم/فادرأتم: كانوا بيوصلوا لهدف غلط "فاداراتم" (رسم الكلمة مختلف
        # شوية بين الملفات — بعضها فيه ألف خنجرية زيادة عن غيره)، الهدف الصح
        # الموحّد هو "فادارتم" (يوليو ٢٠٢٦ الجزء ٣)
        OLD_FADARATM_TARGET = r".replace(/(?<=^|\s)فادراتم(?=\s|$)/g,'فاداراتم').replace(/(?<=^|\s)فادرأتم(?=\s|$)/g,'فاداراتم')"
        NEW_FADARATM_TARGET = r".replace(/(?<=^|\s)فادراتم(?=\s|$)/g,'فادارتم').replace(/(?<=^|\s)فادرأتم(?=\s|$)/g,'فادارتم').replace(/(?<=^|\s)فاداراتم(?=\s|$)/g,'فادارتم')"
        if OLD_FADARATM_TARGET in out:
            out = out.replace(OLD_FADARATM_TARGET, NEW_FADARATM_TARGET)

    # ====================================================
    # 8ج. تنظيف ميزة الترتيب المكسورة من صفحات البقرة (لو اتضافت غلط)
    out, order_removed = remove_broken_order_for_baqara(path, out)

    # ====================================================
    # 8ب. حقن AYAT تلقائيًا للسور الـ٢٠ الناقصة (يوليو ٢٠٢٦)
    out, ayat_injected = inject_ayat_from_data(path, out)

    # ====================================================
    # 9. ميزة ترتيب الآيات 🔀 (جزء عم فقط — الملفات اللي فيها AYAT)
    out, order_changed = add_ordering_feature(out, os.path.basename(path))

    # ====================================================
    # 9أ. ميزة ترتيب الآيات 🔀 لصفحات البقرة (تحقق برمجي من اكتمال
    # النص قبل الإضافة — الصفحات الناقصة تتخطى وتتسجل في تقرير)
    out, baqara_order_changed = add_ordering_feature_baqara(path, out)

    # ====================================================
    # 9ب. تصحيح قوي: تأكيد ربط startQuiz/selectLevel بالترتيب
    # حتى لو الاستبدال النصي الحرفي فوق فشل بصمت بسبب اختلاف التنسيق
    out, wiring_fixed = ensure_order_wiring(path, out)

    # ====================================================
    # 9بأ. مداواة كتلة CSS الترتيب المفقودة (يوليو ٢٠٢٦) — للملفات اللي
    # اترحّلت لقالب قديم مكانش فيه الـCSS وبقت مقفولة على الحالة دي
    out, order_css_healed = heal_missing_order_css(out)

    # ====================================================
    # 9بب. لوحة شرح مستوى الترتيب — تلقائيًا أول مرة + زر '؟' دائم
    out, order_help_added = add_order_help_panel(out)

    # دعم الحروف المقطعة في مقارنة المستوى الصعب (يوليو ٢٠٢٦)
    out, muqattaat_added = add_muqattaat_support(out)

    # ====================================================
    # 9ج. ترقية تصميم الترتيب للنسخة المضغوطة (لو ملف قديم بالتصميم الأول)
    out, order_ui_upgraded = upgrade_order_ui_to_compact(out)

    # ====================================================
    # 9جأ. تكبير مساحة لمس بادچ رقم الآية في مربعات الترتيب (السويب)
    # كانت متغيّرة الحجم حسب رقم الآية — بتسبب فشل عشوائي في التبديل
    out, order_badge_tap_upgraded = upgrade_order_badge_tap_target(out)

    # ====================================================
    # 9جب. تحسين تباين مربعات الترتيب "المتوضّعة" — كانت بتضيع وسط
    # الآيات الطويلة وتبان كأنها فقرة متصلة (يوليو ٢٠٢٦)
    out, order_grid_contrast_upgraded = upgrade_order_filled_grid_contrast(out)

    # ====================================================
    # 9ز. ترقية منطق فحص الترتيب لمقارنة بالنص (يقبل الآيات المتطابقة نصيًا)
    out, order_answer_upgraded = upgrade_order_answer_check(out)

    # ====================================================
    # 9زأ. ترقية حاوية بنك آيات الترتيب لشبكة (grid) بدل عمود واحد —
    # الآيات القصيرة تقعد جنب بعض فيقل طول السكرول (يوليو ٢٠٢٦)
    out, order_pool_grid_upgraded = upgrade_order_pool_layout(out)

    # ====================================================
    # 9زب. إضافة خاصية التبديل بالضغط على البادج (رقم الآية) — تصحيح
    # آية اتحطت غلط بضغطتين بدل تفريغ الخانة (يوليو ٢٠٢٦)
    out, order_swap_added = upgrade_order_tap_swap(out)

    # ====================================================
    # 9د. تصحيح كلاس nav-row الناقص (بيوضّح شكل أزرار الترتيب/التنقل)
    out, navrow_fixed = fix_missing_nav_row_css(out)

    # ====================================================
    # 9و. تصحيح كلاس nav-btn الناقص (زر تحقق/أظهر الترتيب الصحيح)
    out, navbtn_fixed = fix_missing_nav_btn_css(out)

    # ====================================================
    # 9هـ. صف مضغوط: ⏮️ السابق / التالي ⏭️ — انتقال مباشر بين الصفحات
    out, page_nav_added = add_page_nav_row(path, out)

    # 9هـ٢. نفس الصف في شاشة النتيجة النهائية (بعد "← الرئيسية") عشان
    # المستخدم ينتقل للصفحة اللي بعدها فور ما يخلّص المستوى
    out, result_nav_added = add_result_page_nav_row(path, out)

    out, nav_links_fixed = fix_broken_page_nav_links(path, out)


    # ====================================================
    # 9ح. ترقية التسجيل الصوتي (الصعب) لشكل الكلمات القابلة للحذف فرديًا
    out, voice_upgraded = upgrade_voice_recording(out)

    # 9ط. ترقية رجعية: حقن _fixWords للملفات اللي عندها renderWords بالفعل
    #      لكن من غير تصحيحات العرض (بلا/بن/ولا+تجدنهم/ممنع)
    out, fixwords_added = retrofit_fixwords(out)

    # 9ي. وضع المطوّر: إخفاء مستوى "صعب" وزر التلاوة عن الزوار العاديين
    out, dev_mode_added = add_dev_mode(out)

    # 9ك. ترقية ودجت اللغة القديم (3 لغات) للجديد (7 لغات) — لازم قبل
    # قائمة الأدوات عشان تقدر تشيل النسخة القديمة بأمان لو موجودة
    out, lang_upgraded = upgrade_lang_switcher_languages(out)

    # 9ك٢. زر المشاركة يشارك رابط الصفحة الحالية بدل الرئيسية دايمًا
    out, share_upgraded = upgrade_share_current_page(out)

    # 9ل. قائمة "☰ الأدوات" الموحدة (شاركنا رأيك + اللغة + مشاركة) —
    # بتشيل الودجتين القديمتين المنفصلتين وزر المشاركة القديم لو موجودين
    out, tools_menu_added = add_tools_menu(path, out)

    # 9لب. تنظيف بقايا زر '🌐 ترجمة' العائم القديم (.translate-bar) من
    # صفحات ما قبل ودجت اللغة — عنصر ميت مالوش JS، لازم يتشال أينما وجد
    out, translate_bar_removed = remove_legacy_translate_bar(out)

    # 9لأ. تثبيت زر الأدوات في مكان عائم ثابت (أعلى الشاشة يسار) في كل
    # الصفحات — بدل ما يتزحلق حسب هيدر كل صفحة (يوليو ٢٠٢٦)
    out, tools_fab_fixed = upgrade_tools_fab_fixed_position(out)

    # 9م. حماية نص الآيات الكامل في ميزة الترتيب من الترجمة (ملفات قديمة)
    out, order_translate_protected = protect_order_ayat_from_translation(out)

    # 9ن. حماية نص الآيات في محرك الاختبار العادي (سهل/متوسط/صعب) من الترجمة
    out, quiz_translate_protected = protect_quiz_ayat_from_translation(out)

    # 9س. إصلاح باج: استدعاءات renderDotProgress/saveResumeState الناقصة
    # في الملفات القديمة (سهل/متوسط) — بدون أي تغيير في البنية
    out, progress_save_fixed = fix_missing_progress_save_calls(out)

    # 9ش. إصلاح باج: querySelector('.submit-btn') بصيغة المفرد بدل
    # querySelectorAll — بيسيب زرار واحد من زرارين شغال وقت التحقق
    out, submit_btn_fixed = fix_single_submit_btn_selector(out)

    # 9ت. انتقال تلقائي للسؤال التالي لو الإجابة صحيحة (سهل وصعب بس،
    # المتوسط يفضل يدوي في الحالتين) — يوليو ٢٠٢٦
    out, auto_advance_added = upgrade_auto_advance_correct(out)

    # 9خ. نظام تتبع التقدم الدائم عبر الصفحات — مفتاح localStorage دائم
    # منفصل تمامًا عن RESUME_KEY المؤقت (يوليو ٢٠٢٦)
    out, progress_tracking_added = add_progress_tracking(out)

    # 9ث. رسم التنوين: إضافة نطاق U+08F0–U+08F2 (تنوين الإدغام والإخفاء
    # المتتابع) لكلاس حذف التشكيل — مانع تقني لازم يسبق أي نص متغيّر
    out, open_tanween_added = add_open_tanween_to_normalize(out)

    # 9ج. رسم التنوين نفسه: تحويل كل تنوين لشكله الصحيح حسب الكلمة
    # التالية (متراكب / متتابع / إقلاب). لازم يجي *بعد* توسعة كلاس
    # حذف التشكيل فوق، وإلا الكلمات المصححة هتفشل في المقارنة.
    out, tanween_rasm_fixed = fix_tanween_rasm(path, out)

    # 9د. توحيد قواعد normalize: ترتيب الكشيدة + القواعد الناقصة +
    # إصلاح [ءئؤ] و (.)()+ . كلها إضافات — لا تمسّ أي نص قرآني،
    # والبصمة بتتفحص قبل وبعد كضمانة.
    out, norm_rules_unified = unify_normalize_rules(path, out)

    # 9هـ. expandMuqattaat المفقودة — بتكسر زر "تحقق" بالكامل
    out, muq_fixed = fix_missing_expand_muqattaat(path, out)

    # 9و. ميزة تحديد الكلمة من التلاوة → مستوى الصعب
    out, selword_ported = port_selword_feature(path, out)
    out, addwords_repaired = repair_broken_addwords(path, out)

    # 9ز. اتساق الحكم مع العرض + نسبة واحتفال لكل سؤال
    out, legacy_wd = upgrade_legacy_worddiff(path, out)
    out, verdict_fixed = fix_verdict_and_progress(path, out)
    out, pct_upgraded = upgrade_pct_display(path, out)
    out, word_score = switch_to_word_based_score(path, out)
    out, delay_widened = widen_autoadvance_delay(path, out)
    out, pct_dedup = dedup_pct_lines(path, out)

    # 9ي. مراجعة جزء عمّ (أغسطس ٢٠٢٦) — أربع إصلاحات:
    #   · المتوسط: عدد مجموعات الفراغ = عدد كلمات الإجابة
    #   · أسئلة التكرار: تصحيح المفتاح بالعدّ الفعلي من AYAT
    #   · الصوت: محاذاة رسم المحرك على رسم المصحف (قريش/الفيل/العاديات)
    #   · الكتابة: رفض «اللذين» وأخواتها من غير لمس normalize
    # لازم تسبق apply_canonical_functions عشان checkText القياسية
    # بتنادي markBadSpelling، والحاقن ده هو اللي بيعرّفها.
    out, dagger_unified = unify_dagger_alef_with_ayat(path, out)
    out, medium_blanks = add_medium_word_count_blanks(out)
    out, repeat_fixed = fix_repeat_count_answers(path, out)
    out, rasm_snapped = add_rasm_snap_to_voice(path, out)
    out, spell_guarded = add_typing_spell_guard(path, out)

    # 9ك. تسرّب القبول في مستوى الصعب: قاعدة (ألف آخر الكلمة → ياء)
    # جوّه nm كانت بتساوي بين كلمات قرآنية مختلفة (إلى/إلا، شاء/شيء).
    out, nm_alef_fixed = drop_nm_final_alef_rule(path, out)

    # 9ل. محاذاة الصوت محكومة بقواعد الرسم (ىٰ ، الصفر المستدير،
    # الصفر المستطيل) بدل حذف آخر حرف [اي] من كل كلمة.
    out, rasm_rules = upgrade_rasm_voice_rules(path, out)
    out, rasm_ported = port_rasm_snap_to_legacy_voice(path, out)

    # 9ح. توحيد الدوال المشتركة من نسخة قياسية واحدة
    out, canon_done = apply_canonical_functions(path, out)

    # 9ط. صيغة الخطاب: مذكر رسمي في كل نصوص الواجهة
    out, masc_unified = unify_masculine_address(path, out)

    # 8. أضف Service Worker لو مش موجود
    if 'service-worker.js' not in out:
        out = out.replace('</body>', PWA_SW + '\n</body>', 1)

    if out != src:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(out)
        return True
    return False

def fix_index_recitation(path):
    """index.html و recitation.html — PWA + زر مشاركة + وضع المطوّر"""
    with open(path, encoding='utf-8') as f:
        src = f.read()
    out = ar2en(src)

    # ترحيل مسارات الـPWA للنسبي + تحديث og:url للدومين المخصّص
    out, _pwa_rel = fix_pwa_paths_to_relative(out)
    out, _og_url = fix_og_url_to_custom_domain(out)
    out, _og_img = fix_add_og_image(out)
    out, _canon = fix_add_canonical(path, out)

    out, _idx_nav = fix_index_tools_overlap(path, out)

    # نفس الإصلاح للصفحات الداخلية: حجز مساحة الزر ☰ العائم في
    # .top-bar عشان مايقعش فوق زر 🌙
    out, _topbar_nav = fix_topbar_tools_overlap(path, out)

    # إصلاح تحميل خط Google Fonts البطيء (@import → <link>)
    out, _font_fixed = fix_font_import_to_link(out)

    # رسم التنوين: نطاق U+08F0–U+08F2 لكلاس حذف التشكيل في norm()
    out, _open_tanween = add_open_tanween_to_normalize(out)

    # قاعدة الهمزة في norm() — لازم تطابق الـ86 ملف
    out, _recit_hamza = fix_recitation_norm_hamza(path, out)

    # إصلاح تراكب/تجاوز قائمة الأدوات ولون "العربية"
    out, _tools_ui_fixed = fix_tools_menu_ui_bugs(out)

    # ترتيب اللغات + علامة ✓ بدل التلوين الأخضر بس
    out, _lang_list_fixed = fix_lang_list_order_and_checkmark(out)

    # إصلاح رابط 404 (alfatiha_p1.html الغلط بدل alfatiha.html) لو موجود هنا كمان
    out, _fatiha_link_fixed = fix_alfatiha_broken_link(out)

    # وضع المطوّر: recitation.html بترجّع أي زائر من غير الفلاج لـ index.html
    # (الصفحة كلها ميزة واحدة)، وindex.html بتخفي أي رابط/زر تلاوة فيها لو موجود
    if 'darbi_dev' not in out and '<head>' in out:
        if os.path.basename(path) == 'recitation.html':
            out = out.replace('<head>', '<head>\n' + DEV_MODE_REDIRECT, 1)
        else:
            out = out.replace('<head>', '<head>\n' + DEV_MODE_LOCK, 1)

    SHARE_FN = """function shareApp(){var url=location.href;var t=document.title||'دربي لحفظ القرآن';if(navigator.share){navigator.share({title:t,url:url}).catch(function(){});}else if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){var b=document.getElementById('tools-fab-btn');if(b){var old=b.textContent;b.textContent='✅';setTimeout(function(){b.textContent=old;},1800);}}).catch(function(){});}}"""
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

    # ترقية ودجت اللغة القديم (3 لغات) للجديد (7 لغات) — قبل قائمة الأدوات
    out, lang_upgraded = upgrade_lang_switcher_languages(out)

    # زر المشاركة يشارك رابط الصفحة الحالية بدل الرئيسية دايمًا (يشمل
    # ?surah= في اختبار التلاوة)
    out, share_upgraded = upgrade_share_current_page(out)

    # قائمة "☰ الأدوات" الموحدة (شاركنا رأيك + اللغة + مشاركة + QR في
    # index.html فقط) — بتشيل الودجتين القديمتين المنفصلتين لو موجودين
    out, tools_menu_added = add_tools_menu(path, out)

    # 9لب. تنظيف بقايا زر '🌐 ترجمة' العائم القديم (.translate-bar) من
    # صفحات ما قبل ودجت اللغة — عنصر ميت مالوش JS، لازم يتشال أينما وجد
    out, translate_bar_removed = remove_legacy_translate_bar(out)

    # تثبيت زر الأدوات في مكان عائم ثابت (أعلى الشاشة يسار) — بدل ما
    # يتزحلق حسب هيدر كل صفحة (يوليو ٢٠٢٦)
    out, tools_fab_fixed = upgrade_tools_fab_fixed_position(out)

    # صيغة الخطاب: مذكر رسمي (index.html و recitation.html
    # مابيمروش على apply_canonical_functions)
    out, masc_unified = unify_masculine_address(path, out)

    # قواعد الرسم في محاذاة التلاوة الصوتية
    out, rec_rasm_rules = upgrade_recitation_rasm_rules(out)

    # فواصل الآيات في منطقة التسجيل (عرض فقط)
    out, rec_ayah_marks = add_ayah_marks_to_transcript(out)

    if 'service-worker.js' not in out:
        out = out.replace('</body>', PWA_SW + '\n</body>', 1)

    if out != src:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(out)
        return True
    return False


# ============================================================================
# ==  وضع الفحص --audit : تقرير تشخيصي فقط، لا يعدّل أي ملف إطلاقًا           ==
# ==  الاستخدام:  python Scripts/fix_files.py --audit                         ==
# ==  المخرجات:   audit_report.txt في جذر المستودع                            ==
# ============================================================================

# علامات الترقيم اللي بتلغبط المستخدم لو اتكررت جوه إجابة واحدة
_AUD_PUNCT = re.compile(r'[،؛,;:\-–—/\\|]')

_AUD_TASHKIL = re.compile(
    r'[\u064B-\u0652\u0653-\u065F\u0670\u06D6-\u06ED\u08F0-\u08F3\u0640]')


def _aud_norm(t):
    """تطبيع خفيف للمقارنة الدلالية فقط (مش normalize بتاعة الموقع)."""
    t = _AUD_TASHKIL.sub('', t)
    t = re.sub(r'[ٱآأإ]', 'ا', t)
    t = re.sub(r'[ىی]', 'ي', t)
    t = t.replace('ة', 'ه')
    t = re.sub(r'[ءئؤ]', '', t)
    return re.sub(r'\s+', ' ', t).strip()


def _aud_array(src, name):
    """يرجّع جسم مصفوفة JS بالاسم ده، أو None."""
    m = re.search(r'(?:const|let|var)\s+' + name + r'\s*=\s*\[', src)
    if not m:
        return None
    i = m.end() - 1
    depth = 0
    quote = None
    while i < len(src):
        c = src[i]
        if quote:
            if c == '\\':
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in '"\'`':
            quote = c
        elif c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return src[m.end():i]
        i += 1
    return None


def _aud_objects(body):
    """يقسّم جسم المصفوفة لكائنات {...} على المستوى الأعلى."""
    out = []
    depth = 0
    start = None
    quote = None
    i = 0
    while i < len(body):
        c = body[i]
        if quote:
            if c == '\\':
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in '"\'`':
            quote = c
        elif c == '{':
            if depth == 0:
                start = i
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0 and start is not None:
                out.append(body[start:i + 1])
        i += 1
    return out


def _aud_field(obj, key):
    m = re.search(key + r'\s*:\s*"((?:[^"\\]|\\.)*)"', obj)
    if not m:
        m = re.search(key + r'\s*:\s*`([^`]*)`', obj)
    if not m:
        m = re.search(key + r"\s*:\s*'((?:[^'\\]|\\.)*)'", obj)
    return m.group(1).replace('\\"', '"') if m else None


def _aud_choices(obj):
    m = re.search(r'choices\s*:\s*\[(.*?)\]', obj, re.S)
    if not m:
        return []
    return re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))


def _aud_items(src):
    """يرجّع [(المستوى, نص السؤال, الإجابة)] من EASY_Q و MEDIUM_Q."""
    items = []
    eb = _aud_array(src, 'EASY_Q')
    if eb:
        for o in _aud_objects(eb):
            ch = _aud_choices(o)
            idx = re.search(r'answer\s*:\s*(\d+)', o)
            if ch and idx and int(idx.group(1)) < len(ch):
                items.append(('سهل', _aud_field(o, 'q'), ch[int(idx.group(1))]))
    mb = _aud_array(src, 'MEDIUM_Q')
    if mb:
        for o in _aud_objects(mb):
            items.append(('متوسط', _aud_field(o, 'q'), _aud_field(o, 'answer')))
    return items


def _aud_page_freq(src):
    """تكرار كل كلمة في نص الصفحة (AYAT) — لتمييز التسريب القاطع."""
    ab = _aud_array(src, 'AYAT')
    if not ab:
        return {}
    txt = re.findall(r'`([^`]*)`', ab) or re.findall(r'"((?:[^"\\]|\\.)*)"', ab)
    freq = {}
    for w in _aud_norm(' '.join(txt)).split():
        freq[w] = freq.get(w, 0) + 1
    return freq


def _aud_contains(hay_words, needle_words):
    n = len(needle_words)
    if not n or n > len(hay_words):
        return False
    return any(hay_words[k:k + n] == needle_words
               for k in range(len(hay_words) - n + 1))


def run_audit(root):
    """يفحص كل الملفات ويكتب audit_report.txt. لا يعدّل شيئًا."""
    skip = {'index.html', 'recitation.html'}
    files = [f for f in sorted(os.listdir(root))
             if f.endswith('.html') and f not in skip
             and os.path.isfile(os.path.join(root, f))]

    L = []           # سطور التقرير
    problems = 0

    def add(s=''):
        L.append(s)

    # ---------- 1. روابط index.html ----------
    idx_path = os.path.join(root, 'index.html')
    broken, orphan = [], []
    if os.path.isfile(idx_path):
        with open(idx_path, encoding='utf-8') as f:
            idx = f.read()
        refs = set(re.findall(r"['\"]([A-Za-z0-9_]+\.html)['\"]", idx))
        present = set(files) | {'index.html', 'recitation.html'}
        broken = sorted(refs - present)
        orphan = sorted(present - refs - {'index.html'})

    # ---------- 2. تجميع بيانات كل ملف ----------
    rec_keys = set()
    rec_path = os.path.join(root, 'recitation.html')
    if os.path.isfile(rec_path):
        with open(rec_path, encoding='utf-8') as f:
            rec = f.read()
        m = re.search(r'TEXTS\s*=\s*\{', rec)
        if m:
            i, d = m.end() - 1, 0
            while i < len(rec):
                if rec[i] == '{':
                    d += 1
                elif rec[i] == '}':
                    d -= 1
                    if d == 0:
                        break
                i += 1
            rec_keys = set(re.findall(r'([A-Za-z0-9_]+)\s*:\s*`', rec[m.end():i]))

    leak_hard, leak_soft, cross_level = {}, {}, {}
    leak_example = {}
    xleak_hard, xleak_soft, xleak_example = {}, {}, {}
    overlap, long_ans, hard_bad, no_mic, bad_key = [], [], [], [], []
    blank_mismatch, many_words = [], []
    no_norm, nm_diff, fem_hits = [], [], []
    FEM = re.compile(r'اضغطي|اختاري|اكتبي|رتّبي|رتبي|سجّلي|سجلي|جرّبي|جربي|'
                     r'ابدئي|احفظي|راجعي|تابعي|حاولي|ادخلي|اسمعي')

    for fn in files:
        with open(os.path.join(root, fn), encoding='utf-8') as f:
            src = f.read()

        # --- زر التلاوة ---
        ks = re.findall(r'recitation\.html\?surah=([A-Za-z0-9_]+)', src)
        if not ks:
            no_mic.append(fn)
        for k in ks:
            if rec_keys and k not in rec_keys:
                bad_key.append((fn, k))

        # --- صيغة المؤنث ---
        hits = sorted(set(FEM.findall(src)))
        if hits:
            fem_hits.append((fn, hits))

        # --- normalize / nm ---
        if 'function normalize' not in src and 'normalize(' in src:
            no_norm.append(fn)

        # --- HARD_Q ---
        hb = _aud_array(src, 'HARD_Q')
        if hb is None:
            hard_bad.append((fn, 'HARD_Q مفقودة'))
        else:
            ho = _aud_objects(hb)
            if not ho:
                hard_bad.append((fn, 'HARD_Q فاضية'))
            else:
                nums = [int(m.group(1)) for o in ho
                        for m in [re.search(r'ayah\s*:\s*(\d+)', o)] if m]
                if len(nums) != len(ho):
                    hard_bad.append(
                        (fn, 'حقل ayah ناقص في %d سؤال' % (len(ho) - len(nums))))
                elif nums != sorted(nums):
                    bad_seq = [str(n) for n in nums]
                    hard_bad.append((fn, 'أرقام الآيات غير تصاعدية: ' +
                                     '، '.join(bad_seq)))

        # --- الأسئلة ---
        items = _aud_items(src)
        if not items:
            continue
        easy = [_aud_norm(a) for lv, q, a in items if lv == 'سهل' and a]
        med = [_aud_norm(a) for lv, q, a in items if lv == 'متوسط' and a]
        ov = sorted(set(easy) & set(med))
        if ov:
            overlap.append((fn, ov))
        # القاعدة الحقيقية: ممنوع إجابة فيها فواصل ترقيم متعددة (بتلغبط
        # المستخدم وقت التصحيح). الإجابة الطويلة النضيفة من غير ترقيم
        # مقبولة طالما عدد الفراغات بيوضّح عدد الكلمات المطلوبة.
        for lv, q, a in items:
            if lv != 'متوسط' or not a:
                continue
            marks = _AUD_PUNCT.findall(a)
            if len(marks) >= 2:
                long_ans.append((fn, a, ' '.join(marks)))
            if not q:
                continue
            need = len(a.split())
            have = len(re.findall(r'_+', q))
            if have != need:
                blank_mismatch.append((fn, a, have, need))
            elif need > 2:
                many_words.append((fn, a, need))

        # تعريف التسريب: إجابة سؤال ظاهرة في نص سؤال آخر *في نفس
        # الاختبار*. تكرار الآية بين السهل والمتوسط مش تسريب — ده
        # ترسيخ للحفظ (المستخدم بيمرّ على الآية مرتين بفراغ مختلف).
        # الاعتبار: زر «السؤال السابق» موجود، فأي سؤالين في نفس
        # المستوى يعتبروا مكشوفين لبعض مش المتجاورين بس.
        freq = _aud_page_freq(src)
        for i, (lv, q, a) in enumerate(items):
            if not a or not q:
                continue
            aw = _aud_norm(a).split()
            if not aw:
                continue
            unique = all(freq.get(w, 0) <= 1 for w in aw) if freq else True
            for j, (lv2, q2, a2) in enumerate(items):
                if i == j or not q2:
                    continue
                # أسئلة «تكررت كم مرة؟» معتمدة من هند — مابتتحسبش
                # كمضيفة للتسريب.
                if re.search(r'كم مرة|كم عدد', q2):
                    continue
                qw = _aud_norm(q2).replace('_', ' ').split()
                if not _aud_contains(qw, aw):
                    continue
                if lv != lv2:
                    # تسريب بين المستويين: إجابة سؤال في مستوى ظاهرة
                    # مكتوبة في نص سؤال بمستوى تاني. ده تسريب حقيقي —
                    # المستخدم بيشوف الإجابة قدامه قبل ما يجاوب.
                    cross_level[fn] = cross_level.get(fn, 0) + 1
                    if unique:
                        xleak_hard[fn] = xleak_hard.get(fn, 0) + 1
                        xleak_example.setdefault(fn, (a, lv, lv2, q2))
                    else:
                        xleak_soft[fn] = xleak_soft.get(fn, 0) + 1
                    continue
                if unique:
                    leak_hard[fn] = leak_hard.get(fn, 0) + 1
                    leak_example.setdefault(fn, (a, lv, j + 1, q2))
                else:
                    leak_soft[fn] = leak_soft.get(fn, 0) + 1

    # ---------- 3. كتابة التقرير ----------
    add('=' * 66)
    add('  تقرير فحص موقع دربي لحفظ القرآن')
    add('  ' + time.strftime('%Y-%m-%d %H:%M'))
    add('  عدد ملفات الاختبار المفحوصة: %d' % len(files))
    add('=' * 66)
    add()

    def section(title, rows, fmt, note=''):
        nonlocal problems
        add('── %s ──' % title)
        if not rows:
            add('   ✅ سليم')
        else:
            problems += len(rows)
            if note:
                add('   ' + note)
            for r in rows:
                add('   ' + fmt(r))
        add()

    section('روابط مكسورة في index.html', broken, lambda x: '❌ %s' % x)
    section('ملفات غير مربوطة في index.html', orphan, lambda x: '⚠️  %s' % x)
    section('دالة normalize مفقودة', no_norm, lambda x: '❌ %s' % x)
    section('مفتاح ?surah= غير موجود في recitation.html',
            bad_key, lambda x: '❌ %s → %s' % x)
    section('صيغة مؤنث (يجب المذكر الرسمي)',
            fem_hits, lambda x: '⚠️  %s : %s' % (x[0], ' · '.join(x[1])))
    section('مشاكل HARD_Q', hard_bad, lambda x: '❌ %s : %s' % x)
    section('تكرار الكلمة المستهدفة بين سهل ومتوسط',
            overlap, lambda x: '⚠️  %s : %s' % (x[0], ' · '.join(x[1])))
    section('إجابات متوسط فيها فواصل ترقيم متعددة',
            long_ans, lambda x: '⚠️  %s : «%s»  (%s)' % x)
    section('عدد الفراغات لا يطابق عدد كلمات الإجابة',
            blank_mismatch,
            lambda x: '❌ %s : «%s»  %d فراغ / %d كلمة' % x,
            note='(المستخدم بيعرف عدد الكلمات من عدد الفراغات)')
    section('إجابات متوسط أكثر من كلمتين (يفضَّل تقصيرها في الملفات الجديدة)',
            many_words, lambda x: 'ℹ️  %s : «%s» (%d كلمات)' % x)
    section('زر 🎤 اختبر تلاوتك مفقود', no_mic, lambda x: '⚠️  %s' % x,
            note='(النصوص موجودة في recitation.html — الزر فقط غير مضاف)')

    # التسريب — أهم قسم
    # تصحيح (أغسطس ٢٠٢٦): التسريب بين السهل والمتوسط كان مصنّفًا هنا
    # «مقصود — ترسيخ للحفظ» ومستبعَدًا من العدّ. ده غلط: المستخدم
    # بيقرا إجابة سؤال مكتوبة قدامه في سؤال تاني، بغضّ النظر عن
    # المستوى. اتصنّف تسريبًا حقيقيًا وبيتحسب في الإجمالي.
    add('── تسريب الإجابات بين السهل والمتوسط ──')
    if not xleak_hard and not xleak_soft:
        add('   ✅ سليم')
    else:
        problems += sum(xleak_hard.values())
        add('   🔴 تسريب قاطع (الكلمة فريدة في الصفحة): %d حالة في %d ملف'
            % (sum(xleak_hard.values()), len(xleak_hard)))
        for fn, c in sorted(xleak_hard.items(), key=lambda x: -x[1])[:20]:
            a, lv, lv2, q2 = xleak_example[fn]
            add('      %-24s %3d   «%s» إجابة %s مكشوفة في سؤال %s'
                % (fn, c, a, lv, lv2))
            add('      %-24s       %s' % ('', q2[:70]))
        if len(xleak_hard) > 20:
            add('      … و%d ملف آخر' % (len(xleak_hard) - 20))
        add()
        add('   🟡 تسريب ضعيف (كلمة متكررة في الصفحة): %d حالة في %d ملف'
            % (sum(xleak_soft.values()), len(xleak_soft)))
    add()

    add('── تسريب الإجابات داخل المستوى الواحد ──')
    if not leak_hard and not leak_soft:
        add('   ✅ سليم')
    else:
        problems += sum(leak_hard.values())
        add('   🔴 تسريب قاطع (الكلمة فريدة في الصفحة): %d حالة في %d ملف'
            % (sum(leak_hard.values()), len(leak_hard)))
        for fn, c in sorted(leak_hard.items(), key=lambda x: -x[1]):
            a, lv, lv2, q2 = leak_example[fn]
            add('      %-24s %3d   «%s» مكشوفة في سؤال %s رقم %d'
                % (fn, c, a, lv, lv2))
            add('      %-24s       %s' % ('', q2[:70]))
        add()
        add('   🟡 تسريب ضعيف (كلمة متكررة في الصفحة): %d حالة في %d ملف'
            % (sum(leak_soft.values()), len(leak_soft)))
        clean = [f for f in files
                 if f not in leak_hard and f not in leak_soft
                 and f not in xleak_hard and f not in xleak_soft]
        add()
        add('   ✅ ملفات نظيفة تمامًا: %d' % len(clean))
        for f in clean:
            add('      · %s' % f)
    add()

    add('=' * 66)
    if problems == 0:
        add('  ✅ لا توجد مشاكل — جاهز للنشر')
    else:
        add('  إجمالي البنود المرصودة: %d' % problems)
    add('=' * 66)

    report = '\n'.join(L)
    out_path = os.path.join(root, 'audit_report.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report + '\n')
    print(report)
    print('\n📄 اتكتب التقرير في: audit_report.txt')
    return problems


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

    # ====================================================
    # خريطة الموقع + robots.txt — بيتولّدوا آليًا من الملفات الموجودة
    sm_changed, sm_count = build_sitemap_and_robots(root)
    if sm_changed:
        print(f'SITEMAP: تم تحديث {", ".join(sm_changed)} ({sm_count} صفحة)')
    else:
        print(f'SITEMAP: OK ({sm_count} صفحة)')

    # ====================================================
    # تقرير تشخيصي: أي ملفات جزء عم لسه ناقصة AYAT
    # (يطبع في لوج الـ GitHub Action في كل تشغيل، مفيش داعي بحث يدوي)
    missing_ayat = []
    for fn in sorted(os.listdir(root)):
        if fn.endswith('.html') and fn not in skip and not fn.startswith('albaqara_'):
            fp = os.path.join(root, fn)
            if os.path.isfile(fp):
                with open(fp, encoding='utf-8') as f:
                    c = f.read()
                if 'const AYAT=' not in c and 'const AYAT =' not in c:
                    missing_ayat.append(fn)
    print('\n=== تقرير AYAT (جزء عم) ===')
    if missing_ayat:
        print(f'{len(missing_ayat)} ملف لسه ناقص AYAT (ميزة الترتيب مش هتشتغل عليهم):')
        for fn in missing_ayat:
            print('  -', fn)
    else:
        print('كل ملفات جزء عم فيها AYAT ✅')

    # ====================================================
    # تقرير تشخيصي: صفحات البقرة اللي اتخطّت ميزة الترتيب لأن نص
    # الآيات عندها ناقص (HARD_Q ما بيغطيش كل آيات الصفحة) — محتاجة
    # صور مصحف لإكمالها يدويًا
    # ====================================================
    print('\n=== تقرير ترتيب البقرة 🔀 ===')
    if BAQARA_ORDER_SKIPPED:
        print(f'{len(BAQARA_ORDER_SKIPPED)} صفحة بقرة اتخطّت (محتاجة مراجعة/صور مصحف):')
        for s in BAQARA_ORDER_SKIPPED:
            print('  -', s)
    else:
        print('كل صفحات البقرة اللي اتفحصت اكتمل فيها الترتيب ✅')

    # ====================================================
    # تقرير تشخيصي: صفحات بقرة اتخطّت ترحيلها لقالب جزء عمّ النضيف —
    # إما صيغة غير مدعومة، أو HARD_Q ناقصة، أو فشل التحقق الحرفي بعد
    # المحاولة (نادر جدًا؛ لو حصل يبقى فيه فرق حقيقي محتاج عين بشرية)
    # ====================================================
    audit_uniformity(root)
    audit_question_quality(root)

    if INDEX_NAV_FIXED or REC_TANWEEN:
        print('\n=== تقرير index/recitation ===')
        for x in INDEX_NAV_FIXED: print('  - index.html :', x)
        for k, a, b, nx in REC_TANWEEN:
            print('  - recitation %s : %s → %s (التالية: %s)' % (k, a, b, nx))

    if LEGACY_WD_UPGRADED:
        print('\n=== ترقية wordDiff القديمة ===')
        print('اترقّت في %d ملف' % len(LEGACY_WD_UPGRADED))

    if PCT_UPGRADED:
        print('\n=== ترقية عرض النسبة ===')
        print('اترقّت في %d ملف' % len(PCT_UPGRADED))

    if DELAY_FIXED:
        print('\n=== مدة عرض النتيجة ===')
        print('اتوسّعت في %d ملف (صعب 3.5ث · سهل 2.2ث)' % len(DELAY_FIXED))

    print('\n=== توحيد الدوال القياسية ===')
    for k in CANON_FN:
        print('  %-16s اتوحّدت في %3d ملف | مش موجودة في %d'
              % (k, len(CANON_APPLIED.get(k, [])), len(CANON_SKIPPED.get(k, []))))

    print('\n=== النسبة على أساس الكلمات ===')
    print('اتطبّق في %d ملف | اتخطّى %d' % (len(WORDSCORE_FIXED), len(WORDSCORE_SKIPPED)))
    if WORDSCORE_SKIPPED:
        print('  ', ' · '.join(WORDSCORE_SKIPPED[:15]))

    print('\n=== تقرير الحكم والنسبة ===')
    print('اتطبّق كامل : %d ملف' % len(VERDICT_FIXED))
    print('اتخطّى      : %d ملف (قالب مختلف — اتساب زي ما هو)' % len(VERDICT_SKIPPED))
    if VERDICT_SKIPPED:
        print('  ', ' · '.join(x[0] for x in VERDICT_SKIPPED[:20]))

    print('\n=== تقرير روابط التنقل ===')
    if BROKEN_NAV_FIXED:
        for fn2, w in BROKEN_NAV_FIXED:
            print('  -', fn2, ':', ' · '.join(w))
    else:
        print('كل الروابط سليمة ✅')

    print('\n=== تقرير ميزة تحديد الكلمة (صعب) ===')
    print('اتطبّقت دلوقتي   : %d ملف' % len(SELWORD_FIXED))
    if SELWORD_REPAIRED:
        print('⛔ اتصلح استدعاء ذاتي مكسور في %d ملف' % len(SELWORD_REPAIRED))
    print('كانت مطبّقة قبل  : %d ملف' % len(SELWORD_ALREADY))
    print('القالب مااتطابقش : %d ملف' % len(SELWORD_NOMATCH))
    if SELWORD_NOMATCH:
        print('   ⚠', ' · '.join(SELWORD_NOMATCH[:15]))
    low=[x for x in SELWORD_FIXED if x[1]<6]
    if low:
        print('  ⚠ ملفات اتطبّق فيها جزء بس:')
        for fn2,c2 in low: print('   -',fn2,'(%d/7)'%c2)

    print('\n=== تقرير expandMuqattaat ===')
    print('سليمة أصلاً: %d ملف' % len(MUQ_OK))
    if MUQ_FIXED:
        for fn2, st in MUQ_FIXED:
            print('  -', fn2, ':', st)
    else:
        print('مفيش ملفات محتاجة إصلاح ✅')

    print('\n=== تقرير توحيد قواعد normalize ===')
    if NORM_FIXED:
        print('%d ملف اتصلح:' % len(NORM_FIXED))
        for fn2, w in NORM_FIXED:
            print('  -', fn2, ':', ' · '.join(w))
    else:
        print('مفيش تعديلات مطلوبة ✅')
    if RECIT_NORM_FIXED:
        print('  + قاعدة الهمزة في norm(): ' + ' · '.join(RECIT_NORM_FIXED))

    print('\n=== تقرير رسم التنوين ===')
    if TANWEEN_SKIPPED:
        print(f'{len(TANWEEN_SKIPPED)} ملف اتخطّى تصحيح التنوين:')
        for s in TANWEEN_SKIPPED:
            print('  -', s)
    else:
        print('كل الملفات اتفحصت ✅')
    if TANWEEN_UNRESOLVED:
        print('كلمات فيها كود تنوين قديم ومش متحدد حكمها (مشتتات مخترَعة غالبًا):')
        for fn, ws in TANWEEN_UNRESOLVED:
            print('  -', fn, ':', ' '.join(ws))

    print('\n=== تقرير ترحيل قالب البقرة النضيف ===')
    if BAQARA_MIGRATION_SKIPPED:
        print(f'{len(BAQARA_MIGRATION_SKIPPED)} صفحة بقرة اتخطّت الترحيل:')
        for s in BAQARA_MIGRATION_SKIPPED:
            print('  -', s)
    else:
        print('كل صفحات البقرة اللي اتفحصت اترحّلت للقالب النضيف ✅')

    print('\n=== تقرير زر «السؤال التالي» ===')
    print('اتصلّح في: %d ملف' % len(NEXTBTN_FIXED))

    print('\n=== تقرير عدد فراغات المتوسط ===')
    print('اتصلّح في: %d ملف' % len(BLANKS_FIXED))
    for fn2, hits in BLANKS_FIXED:
        for a, o, n in hits:
            print('  - %s : «%s»  %d → %d فراغ' % (fn2, a, o, n))
    if BLANKS_SKIPPED:
        print('اتخطّى (مراجعة يدوية): %d' % len(BLANKS_SKIPPED))
        for fn2, a, why in BLANKS_SKIPPED:
            print('  -', fn2, ':', a, '|', why)

    print('\n=== تقرير زر 🎤 اختبر تلاوتك ===')
    print('اتضاف في: %d ملف' % len(RECIT_BTN_ADDED))
    if RECIT_BTN_ADDED:
        print('  ', ' · '.join(f for f, k in RECIT_BTN_ADDED[:20]))
    if RECIT_BTN_SKIPPED:
        print('اتخطّى: %d ملف' % len(RECIT_BTN_SKIPPED))
        for fn2, why in RECIT_BTN_SKIPPED:
            print('  -', fn2, ':', why)

    print('\n=== أرقام الآيات في عرض المصحف (مستوى الترتيب) ===')
    print('اتصلّح: %d صفحة' % len(BAQARA_AYAHNUM_FIXED))
    if BAQARA_AYAHNUM_FIXED:
        print('  ', ' · '.join(BAQARA_AYAHNUM_FIXED))
    if BAQARA_AYAHNUM_SKIPPED:
        print('اتخطّى: %d صفحة' % len(BAQARA_AYAHNUM_SKIPPED))
        for s in BAQARA_AYAHNUM_SKIPPED:
            print('  -', s)

if __name__ == '__main__':
    if '--audit' in sys.argv:
        _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        run_audit(_root)
    else:
        main()
