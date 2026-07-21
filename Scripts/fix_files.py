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
.tools-fab{position:relative;display:inline-flex;z-index:60;font-family:'Amiri','Scheherazade New',Tahoma,sans-serif;}
.tools-fab-btn{display:flex;align-items:center;justify-content:center;background:var(--green3,var(--surface2,#EAF2EA));color:var(--green,var(--accent,#2E6B3E));border:1px solid var(--border,#E4EAE4);border-radius:50%;width:34px;height:34px;font-size:1rem;cursor:pointer;}
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
    if is_index and '.tools-fab{position:relative' not in out:
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
      card.className='order-slot filled';
      card.setAttribute('translate','no');
      card.innerHTML='<span class="order-badge">﴿'+toArabicNum(pos+1)+'﴾</span><span class="notranslate">'+AYAT[idx]+'</span>';
      card.onclick=()=>{orderPlaced[pos]=null;orderCursor=pos;document.getElementById('order-feedback').style.display='none';renderOrderQuiz();};
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
PREV_MAP = {NEXT_SEQUENCE[i]: NEXT_SEQUENCE[i - 1] for i in range(1, len(NEXT_SEQUENCE))}
NEXT_BTN_RE = re.compile(r'(<button class="start-btn"[^>]*>[^<]*</button>)')
LEVEL_RETURN_BTN_RE = re.compile(r'<button class="level-return-btn"[^>]*>[^<]*</button>')


PAGE_NAV_OLD_A_RE = re.compile(
    r'\s*<a href="[^"]*" (?:class|id)="(?:next|prev)-page-btn"[^>]*>[^<]*</a>'
)


def add_page_nav_row(path, out):
    """يضيف صف واحد مضغوط فيه زرين جنب بعض: ⏮️ السابق و⏭️ التالي —
    بيتحط في شاشة اختيار المستوى وجنب كل زر 'اختر مستوى آخر' (الاختبار
    العادي وشاشة الترتيب). لو الملف فيه نسخة قديمة من الأزرار دي (شكل
    مكدّس بعرض كامل)، الدالة بتشيلها وتستبدلها بالصف المضغوط الجديد —
    آمن ويعمل مرة واحدة بس (idempotent)."""
    fn = os.path.splitext(os.path.basename(path))[0]
    next_key = NEXT_MAP.get(fn)
    prev_key = PREV_MAP.get(fn)
    if not next_key and not prev_key:
        return out, False  # ملف مش داخل السلسلة أصلاً

    if 'page-nav-row' in out:
        return out, False  # مضاف بالفعل (الصف الجديد موجود) — منلمسش الملف تاني

    changed = False

    # تنظيف أي نسخة قديمة (مكدّسة بعرض كامل) قبل الإضافة من جديد
    # ملحوظة: بيتنفذ بس لو page-nav-row مش موجود أصلاً (فوق)، فمستحيل
    # يمسح أزرار مضافة حديثًا بالغلط
    if PAGE_NAV_OLD_A_RE.search(out):
        out = PAGE_NAV_OLD_A_RE.sub('', out)
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

    # بعد زر "ابدأ الاختبار" في شاشة اختيار المستوى
    m = NEXT_BTN_RE.search(out)
    if m:
        out = out[:m.end()] + row_html + out[m.end():]
        changed = True

    # بعد كل زر "اختر مستوى آخر" (في شاشة الاختبار وشاشة الترتيب)
    matches = list(LEVEL_RETURN_BTN_RE.finditer(out))
    for mm in reversed(matches):
        out = out[:mm.end()] + row_html + out[mm.end():]
        changed = True

    return out, changed


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
let orderPlaced=[],orderCursor=0,orderPoolOrder=[];
function startOrderQuiz(){
  orderPlaced=new Array(ORDER_AYAT.length).fill(null);
  orderCursor=0;
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
      card.className='order-slot filled';
      card.innerHTML='<span class="order-badge">﴿'+toArabicNum(pos+1)+'﴾</span><span>'+ORDER_AYAT[idx]+'</span>';
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


def extract_baqara_order_ayat(out):
    """يستخرج نصوص آيات الصفحة بالترتيب الصحيح، من AYAT (لو بصيغة object
    زي p38) أو من HARD_Q (بعد استبعاد أي سؤال جزئي زي 'بداية الآية...حتى...').
    يرجّع (None, سبب) لو العدد ما طابقش عدد آيات الصفحة الحقيقي المكتوب في
    ayat-range، عشان مايتضافش ترتيب ناقص أبدًا."""
    m_range = re.search(r'الآيات\s*(\d+)\s*إلى\s*(\d+)', out)
    if not m_range:
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
    texts = []
    for q, ans in items:
        if 'بداية' in q or 'حتى' in q:
            continue
        texts.append(ans.replace('\\"', '"'))
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
    if 'btn-order' not in out:
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
            f"{ind}#btn-order .level-icon{{filter:hue-rotate(85deg) saturate(1.5) brightness(0.9);}}\n"
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
    مختلف بس، مش رسمة جديدة."""
    changed = False
    old_svg = ('<span class="level-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
               'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
               '<polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/>'
               '<polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/>'
               '<line x1="4" y1="4" x2="9" y2="9"/></svg></span>')
    new_emoji = '<span class="level-icon">🔀</span>'
    if old_svg in out:
        out = out.replace(old_svg, new_emoji, 1)
        changed = True
    old_color_rule = '#btn-order .level-icon{color:var(--accent);}'
    new_filter_rule = '#btn-order .level-icon{filter:hue-rotate(85deg) saturate(1.5) brightness(0.9);}'
    if old_color_rule in out:
        out = out.replace(old_color_rule, new_filter_rule, 1)
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
        '  <button class="level-return-btn" onclick="returnToLevels()">🔄 اختر مستوى آخر</button>\n'
        '<div class="page-nav-row" style="display:flex;gap:8px;margin-top:10px;">'
    )
    anchor_new = (
        '<div class="feedback" id="feedback"></div>\n'
        '  <button class="level-return-btn" onclick="returnToLevels()">🔄 اختر مستوى آخر</button>\n'
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

def fix_file(path):
    with open(path, encoding='utf-8') as f:
        src = f.read()
    out = ar2en(src)

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

    # رجعة أيقونة "ترتيب" لشكل الإيموجي الأصلي (بدل SVG) مع فلتر اللون
    out, _order_icon_fixed = fix_order_icon_revert_to_emoji(out)

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
        "    .replace(/[ئؤ]/g,'ء').replace(/ء/g,'')\n"
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
    # 9ج. ترقية تصميم الترتيب للنسخة المضغوطة (لو ملف قديم بالتصميم الأول)
    out, order_ui_upgraded = upgrade_order_ui_to_compact(out)

    # ====================================================
    # 9ز. ترقية منطق فحص الترتيب لمقارنة بالنص (يقبل الآيات المتطابقة نصيًا)
    out, order_answer_upgraded = upgrade_order_answer_check(out)

    # ====================================================
    # 9د. تصحيح كلاس nav-row الناقص (بيوضّح شكل أزرار الترتيب/التنقل)
    out, navrow_fixed = fix_missing_nav_row_css(out)

    # ====================================================
    # 9و. تصحيح كلاس nav-btn الناقص (زر تحقق/أظهر الترتيب الصحيح)
    out, navbtn_fixed = fix_missing_nav_btn_css(out)

    # ====================================================
    # 9هـ. صف مضغوط: ⏮️ السابق / التالي ⏭️ — انتقال مباشر بين الصفحات
    out, page_nav_added = add_page_nav_row(path, out)

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

    # 9م. حماية نص الآيات الكامل في ميزة الترتيب من الترجمة (ملفات قديمة)
    out, order_translate_protected = protect_order_ayat_from_translation(out)

    # 9ن. حماية نص الآيات في محرك الاختبار العادي (سهل/متوسط/صعب) من الترجمة
    out, quiz_translate_protected = protect_quiz_ayat_from_translation(out)

    # 9س. إصلاح باج: استدعاءات renderDotProgress/saveResumeState الناقصة
    # في الملفات القديمة (سهل/متوسط) — بدون أي تغيير في البنية
    out, progress_save_fixed = fix_missing_progress_save_calls(out)

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

    # إصلاح تحميل خط Google Fonts البطيء (@import → <link>)
    out, _font_fixed = fix_font_import_to_link(out)

    # إصلاح تراكب/تجاوز قائمة الأدوات ولون "العربية"
    out, _tools_ui_fixed = fix_tools_menu_ui_bugs(out)

    # ترتيب اللغات + علامة ✓ بدل التلوين الأخضر بس
    out, _lang_list_fixed = fix_lang_list_order_and_checkmark(out)

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

if __name__ == '__main__':
    main()
