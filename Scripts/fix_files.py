#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re

# ====================================================
# بيانات AYAT للسور اللي كانت ناقصة (يوليو ٢٠٢٦)
# مستخرجة من صور المصحف مباشرة، مقسّمة آية بآية.
# بتتحقن تلقائيًا في الملف المناسب لو الملف من غير AYAT أصلاً.
# ====================================================
AYAT_DATA = {
"alfatiha_p1": [
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
    "      card.className='order-slot filled';\n"
    "      card.innerHTML='<span class=\"order-badge\">﴿'+toArabicNum(pos+1)+'﴾</span><span>'+AYAT[idx]+'</span>';\n"
    "      card.onclick=()=>{orderPlaced[pos]=null;orderCursor=pos;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};\n"
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
    ".order-filled-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin-bottom:10px;}"
    ".order-slot{display:flex;gap:8px;align-items:center;border-radius:10px;padding:10px 12px;font-size:16px;line-height:1.7;cursor:pointer;}"
    ".order-slot.filled{background:var(--surface3);border:1.5px solid var(--accent);}"
    ".order-slot.correct-slot{background:var(--correct-bg) !important;border-color:var(--accent) !important;color:var(--correct-text) !important;}"
    ".order-slot.wrong-slot{background:var(--wrong-bg) !important;border-color:var(--wrong-border) !important;color:var(--wrong-text) !important;}"
    ".order-empty-strip{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px;}"
    ".order-dot{display:flex;align-items:center;justify-content:center;min-width:34px;height:32px;padding:0 3px;flex-shrink:0;border-radius:50%;background:var(--surface2);border:1.5px dashed var(--border);color:var(--hint-btn-text);font-size:15px;font-family:'Amiri','Scheherazade New',serif;cursor:pointer;transition:all .15s;}"
    ".order-dot:hover{border-color:var(--accent);}"
    ".order-dot.active{border-style:solid;border-color:var(--accent);background:var(--hint-bg);color:var(--accent-dark);font-weight:700;box-shadow:0 0 0 3px var(--surface-hover);}"
    ".order-badge{color:var(--hint-btn-text);font-size:16px;font-family:'Amiri','Scheherazade New',serif;flex-shrink:0;}"
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
      card.className='order-slot filled';
      card.innerHTML='<span class="order-badge">﴿'+toArabicNum(pos+1)+'﴾</span><span>'+AYAT[idx]+'</span>';
      card.onclick=()=>{orderPlaced[pos]=null;orderCursor=pos;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};
      filledGrid.appendChild(card);
    }
  });
  if(filledGrid.children.length)slotsDiv.appendChild(filledGrid);
  if(emptyStrip.children.length)slotsDiv.appendChild(emptyStrip);
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

def remove_broken_order_for_baqara(path, out):
    """يشيل ميزة الترتيب المكسورة اللي اتضافت غلط لصفحات البقرة
    (بسبب AYAT قديمة بصيغة {num,text} مش نص بسيط)."""
    fn = os.path.splitext(os.path.basename(path))[0]
    if not fn.startswith('albaqara_'):
        return out, False
    if 'order-area' not in out:
        return out, False
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
# سلسلة ترتيب المصحف لزر "التالي ⏭️" — من البقرة p2 لحد الناس
# ====================================================
NEXT_SEQUENCE = (
    ['alfatiha_p1'] +
    [f'albaqara_p{i}' for i in range(2, 50)] +
    [
        'annaba', 'annaziat', 'abasa', 'attakwir', 'al-infitar',
        'almutaffifin', 'alinshiqaq', 'alburuj', 'altariq', 'alaala',
        'alghasiya', 'alfajr', 'albalad', 'alshams', 'allayl', 'alduha',
        'alsharh', 'atteen', 'alalaq', 'alqadr', 'albayyina', 'alzalzala',
        'alaadiyat', 'alqaria', 'altakathur', 'alasr', 'alhumaza', 'alfiyl',
        'aquraysh', 'almaoon', 'alkawthur', 'alkafirun', 'alnnasr',
        'almasad', 'alikhlas', 'alfalaq', 'alnnas',
    ]
)
NEXT_MAP = {NEXT_SEQUENCE[i]: NEXT_SEQUENCE[i + 1] for i in range(len(NEXT_SEQUENCE) - 1)}

NEXT_BTN_RE = re.compile(r'(<button class="start-btn"[^>]*>[^<]*</button>)')


def add_next_page_button(path, out):
    """يضيف زر ⏭️ التالي في شاشة اختيار المستوى، للانتقال مباشرة
    للصفحة/السورة التالية في ترتيب المصحف من غير الرجوع للفهرس."""
    fn = os.path.splitext(os.path.basename(path))[0]
    if fn not in NEXT_MAP:
        return out, False  # آخر ملف في السلسلة (الناس) أو ملف مش داخل السلسلة
    if 'id="next-page-btn"' in out:
        return out, False  # مضاف بالفعل
    m = NEXT_BTN_RE.search(out)
    if not m:
        return out, False
    next_file = NEXT_MAP[fn] + '.html'
    btn_html = (
        '\n<a href="' + next_file + '" id="next-page-btn" '
        'style="display:block;text-align:center;text-decoration:none;'
        'margin-top:10px;padding:12px;border-radius:12px;'
        'background:var(--surface2);color:var(--accent);'
        'border:1.5px solid var(--border);font-family:inherit;font-size:15px;">'
        '⏭️ التالي</a>'
    )
    out = out[:m.end()] + btn_html + out[m.end():]
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
    if 'btn-order' not in out:
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
    # 8ج. تنظيف ميزة الترتيب المكسورة من صفحات البقرة (لو اتضافت غلط)
    out, order_removed = remove_broken_order_for_baqara(path, out)

    # ====================================================
    # 8ب. حقن AYAT تلقائيًا للسور الـ٢٠ الناقصة (يوليو ٢٠٢٦)
    out, ayat_injected = inject_ayat_from_data(path, out)

    # ====================================================
    # 9. ميزة ترتيب الآيات 🔀 (جزء عم فقط — الملفات اللي فيها AYAT)
    out, order_changed = add_ordering_feature(out, os.path.basename(path))

    # ====================================================
    # 9ب. تصحيح قوي: تأكيد ربط startQuiz/selectLevel بالترتيب
    # حتى لو الاستبدال النصي الحرفي فوق فشل بصمت بسبب اختلاف التنسيق
    out, wiring_fixed = ensure_order_wiring(path, out)

    # ====================================================
    # 9ج. ترقية تصميم الترتيب للنسخة المضغوطة (لو ملف قديم بالتصميم الأول)
    out, order_ui_upgraded = upgrade_order_ui_to_compact(out)

    # ====================================================
    # 9د. تصحيح كلاس nav-row الناقص (بيوضّح شكل أزرار الترتيب/التنقل)
    out, navrow_fixed = fix_missing_nav_row_css(out)

    # ====================================================
    # 9هـ. زر ⏭️ التالي — انتقال مباشر للصفحة/السورة التالية
    out, next_btn_added = add_next_page_button(path, out)

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

if __name__ == '__main__':
    main()
