// ===== voice-engine.js — محرك تصحيح النطق والتعرف الصوتي المشترك =====
// دربي لحفظ القرآن — هذا الملف يجمّع منطق التطبيع (normalize) ومطابقة
// الرسم القرآني (snapToRasm/_rasmVoiceForms) المستخدم في كل صفحات
// "سؤال الصعب" بدل ما يتكرر نسخة منفصلة جوه كل ملف HTML على حدة.
// أي تصحيح مستقبلي لمشاكل التعرف الصوتي (زي كلمة بتتكتب غلط) يتعدّل
// هنا مرة واحدة بس، وبينطبق تلقائيًا على كل الصفحات اللي بتحمّل الملف ده.


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
}

const NUM_WORDS={
  'واحد':1,'واحده':1,'احد':1,'اثنان':2,'اثنين':2,'اثنتان':2,'اثنتين':2,
  'ثلاثه':3,'ثلاث':3,'اربعه':4,'اربع':4,'خمسه':5,'خمس':5,'سته':6,'ست':6,
  'سبعه':7,'سبع':7,'ثمانيه':8,'ثمان':8,'تسعه':9,'تسع':9,'تسعا':9,
  'عشره':10,'عشر':10,
  'عشرون':20,'عشرين':20,'ثلاثون':30,'ثلاثين':30,'اربعون':40,'اربعين':40,
  'خمسون':50,'خمسين':50,'ستون':60,'ستين':60,'سبعون':70,'سبعين':70,
  'ثمانون':80,'ثمانين':80,'تسعون':90,'تسعين':90,
  'مايه':100,'مئه':100,'مايتان':200,'مايتين':200,'مئتان':200,'مئتين':200,
  'الف':1000,'الفين':2000,'الفان':2000
}

function normalize(str){
  if(!str)return'';
  return str
    .replace(/ـ([ٕٔ])([ً-ٟ])/g,'ـ$2$1')
    .replace(/ي\u0653?ـ\u064E\u0654/g,'ي')
    .replace(/ي\u0653?ـ\u064E\u0654/g,'ي').replace(/ـ\u064E\u0654/g,'ا')
    .replace(/ـِ[\u0654\u0655]/g,'ي').replace(/ـ[\u064B-\u065F]*[\u0654\u0655]/g,'')
    .replace(/ـۧ/g,'ي').replace(/يٓ?ـَٔ/g,'ي').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـَٔ/g,'ا').replace(/ـ[ًٌٍَُِّْٕٖٜٟٓٔٗ٘ٙٚٛٝٞ]*[ٕٔ]/g,'').replace(/ـ/g,'')
    .replace(/[\u064B-\u065F\u0610-\u061A\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED\u08F0-\u08F2]/g,'')
    .replace(/ها[ؤو]لاء|ها[ؤو]لا(?!\S)/g,'هالا').replace(/ه[ؤو]لاء|ه[ؤو]لا(?!\S)/g,'هالا')
    
    .replace(/(?<=^|\s)وا(?=سجد|قترب|دخل|دعو|ذكر|رحم|ستغفر|ستغن|غفر|عف|نحر|تق|ختلاف|مر[أا]|تبع|سمع|ستكبر|ستعين|ركع|صبر|صل|جتنب|هبط|ستبشر|ستقم|ضرب|عتصم|ئتلف|بتغ|حذر|شرب|صفح|تخذ|علم|رزق|جعل|خش|شكر|نظر|بعث|قتل|نصر|ستشهد|جتب|متاز)/g,'و')
    .replace(/وٰ(?=ة)/g,'ا').replace(/وٰ/g,'وا')
    .replace(/اٰ/g,'ا').replace(/يٰ/g,'يا')
    .replace(/نٰ/g,'نا')
    .replace(/(?<=^|\s)بلىٰ(?=\s|$)/g,'بلا').replace(/ىٰ(?=\S)/g,'ا').replace(/ىٰ/g,'ي')
    .replace(/(.)ٰ/g,'$1ا')
    .replace(/هۥ/g,'ه').replace(/هۦ/g,'ه')
    .replace(/ۦ(?=\S)/g,'ي').replace(/ۦ/g,'').replace(/ۥ/g,'')
    .replace(/ه[ۥۦ]/g,'ه')
    .replace(/(?<=^|\s)لشئ(?=\s|$)/g,'لشاي').replace(/ئ(?=و)/g,'').replace(/ئ/g,'ي').replace(/ؤ/g,'و').replace(/ء/g,'')
    .replace(/[آأإٱا]/g,'ا')
    .replace(/[ىی]/g,'ي')
    .replace(/ة/g,'ه')
    .replace(/(?<=^|\s)ممنع(?=\s|$)/g,'ممن منع').replace(/(.)\1+/g,'$1')
    .replace(/الربوا/g,'الربا').replace(/رحمان/g,'رحمن').replace(/(?<=^|\s)فازالهما(?=\s|$)/g,'فازلهما').replace(/(?<=^|\s)فاذلهما(?=\s|$)/g,'فازلهما').replace(/(?<=^|\s)فادراتم(?=\s|$)/g,'فادارتم').replace(/(?<=^|\s)فادرأتم(?=\s|$)/g,'فادارتم').replace(/(?<=^|\s)فاداراتم(?=\s|$)/g,'فادارتم').replace(/(?<=^|\s)بن(?=\s|$)/g,'ابن').replace(/نصاري(?=\s|$)/g,'نصارا').replace(/(?<=^|\s)ناتي(?=\s|$)/g,'نات').replace(/(?<=^|\s)ولا تجدنهم(?=\s|$)/g,'ولتجدنهم').replace(/(?<=^|\s)ولاتجدنهم(?=\s|$)/g,'ولتجدنهم').replace(/(?<=^|\s)او كل ما(?=\s|$)/g,'اوكلما').replace(/(?<=^|\s)او كلما(?=\s|$)/g,'اوكلما').replace(/(?<=^|\s)بلي(?=\s|$)/g,'بلا').replace(/(?<=^|\s)اهاني(?=\s|$)/g,'اهان').replace(/(?<=^|\s)تكفروني(?=\s|$)/g,'تكفرون').replace(/(?<=^|\s)فاتقوني(?=\s|$)/g,'فاتقون').replace(/(?<=^|\s)فارهبوني(?=\s|$)/g,'فارهبون').replace(/(?<=^|\s)وتقوني(?=\s|$)/g,'وتقون').replace(/(?<=^|\s)يقضي(?=\s|$)/g,'يقض').replace(/(?<=^|\s)ينتهي(?=\s|$)/g,'ينته').replace(/(?<=^|\s)اوفي(?=\s|$)/g,'اوف').replace(/(?<=^|\s)يسري(?=\s|$)/g,'يسر')
    .replace(/مولانا/g,'مولنا').replace(/يا ايها/g,'يايها').replace(/يا ايتها/g,'يايتها').replace(/الاه/g,'اله').replace(/ارايت/g,'اريت').replace(/اولااك/g,'اولاك').replace(/ياايها/g,'يايها').replace(/ياايتها/g,'يايتها').replace(/نب/g,'مب').replace(/وا(?=\s|$)/g,'و').replace(/اولك/g,'اولاك').replace(/يا ?ايها/g,'يايها').replace(/يا ?ايتها/g,'يايتها')
    .replace(/الاه/g,'اله').replace(/ارايت/g,'اريت')
    .replace(/هاذا/g,'هذا').replace(/هاذه/g,'هذه').replace(/ذالك/g,'ذلك').replace(/لاكن/g,'لكن')
    .replace(/(?<=^|\s)تراني(?=\s|$)/g,'ترن').replace(/(?<=^|\s)ياتيني(?=\s|$)/g,'ياتين').replace(/(?<=^|\s)تعلمني(?=\s|$)/g,'تعلمن').replace(/(?<=^|\s)تسالني(?=\s|$)/g,'تسالن').replace(/(?<=^|\s)تسالنى(?=\s|$)/g,'تسالن')
    .replace(/(?<=^|\s)وراي(?=\s|$)/g,'ورا').replace(/(?<=^|\s)لاتخذت(?=\s|$)/g,'لتخذت').replace(/(?<=^|\s)تستطيع(?=\s|$)/g,'تستطع')
    .replace(/(?<=^|\s)فانطلق(?=\s|$)/g,'فانطلقا').replace(/(?<=^|\s)فوجد(?=\s|$)/g,'فوجدا')
    .replace(/^اولايك$/,'اوليك').replace(/^هاولا$/,'هالا').replace(/^يوتيني$/,'يوتين')
    .replace(/\s+/g,' ')
    .trim();
}

function isRealMuqattaa(w){
  if(!MUQATTAAT[normalize(w)])return false;
  if(/[\u064B-\u0652\u06E1]/.test(w))return false;
  if(/[\u0623\u0625\u0624\u0626\u0621]/.test(w))return false;
  return true;
}

function collapseMuqattaat(words,correctAnswer){
  if(!words||!words.length||!correctAnswer)return words;
  const cw=correctAnswer.trim().split(/\s+/);
  if(!isRealMuqattaa(cw[0]))return words;
  const names=MUQATTAAT[normalize(cw[0])];
  if(!names||words.length<names.length)return words;
  for(let k=0;k<names.length;k++){
    if(normalize(words[k])!==normalize(names[k]))return words;
  }
  return [cw[0]].concat(words.slice(names.length));
}

// مفتاح "رسم" مبسّط للمقارنة بين كلمتين حقيقيتين: بلا تشكيل لكن بدون دمج الحروف المكررة
// (norm بتدمج «ٱللَّهَ» و«إِلَٰهَ» في «اله» رغم إنهم كلمتين مختلفتين) والخنجرية بتتحسب ألف
function _pkey(x){
  return String(x).replace(/\u0670/g,'ا')
    .replace(/[\u0640\u064B-\u065F\u06D6-\u06ED\u08F0-\u08F2]/g,'')
    .replace(/[آأإٱ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه');
}
function _rasmVoiceForms(w,nextW,skip){
  const out=[];
  // skip(alt): لو رجّعت true معناه الصيغة البديلة دي بتساوي كلمة تانية حقيقية في نفس الإجابة —
  // فمانقبلهاش بديل (عشان ما نقبلش كلمة غلط مكان كلمة صح: كفر/كافر، قتل/قاتل)
  const weak=alt=>{if(!(skip&&skip(alt)))out.push(alt);};
  if(/ى\u0670[^ء-ي]*$/.test(w))
    out.push(w.replace(/ى\u0670([^ء-ي]*)$/,'ا$1'));
  if(/[\u06DF\u06E0]/.test(w))
    out.push(w.replace(/[اويى][\u06DF\u06E0]/g,''));
  if(/ن\u064E$/.test(w))
    out.push(w+'ا');
  if(/ه[\u0652\u06E1]$/.test(w))
    out.push(w.replace(/ه[\u0652\u06E1]$/,''));
  if(/^[وف][\u064B-\u065F]?ٱ(?!ل)/.test(w))
    out.push(w.replace(/^([وف])[\u064B-\u065F]?ٱ/,'$1'));
  // ياء المتكلم المحذوفة رسمًا بعد نون مثل «يَهۡدِيَنِ»: قد تُنطق فيسمعها التسجيل ياء زيادة
  if(/ن\u0650$/.test(w))
    out.push(w+'ي');
  if(/ن[\u064B\u064C\u064D\u08F0\u08F1\u08F2]$/.test(w))
    out.push(w+'ا');
  // تنوين الفتح على الألف بيتسمع أحيانًا ألف مقصورة (نُّكۡرًا → نكرى)
  if(/[\u064B\u08F0]ا$/.test(w))
    out.push(w.replace(/[\u064B\u08F0]ا$/,'ى'));
  // ...وأحيانًا تسقط ألف التنوين كليًّا وصلًا (إِلَٰهࣰا وَٰحِدࣰا → «إله واحدا»)
  if(/[\u064B\u08F0]ا$/.test(w))
    weak(w.replace(/ا$/,''));
  // ألف خنجرية + [حركة] + مدة قبل همزة (أُو۟لَٰٓئِكَ، وَأُولَٰٓئِكَ، هَـٰٓؤُلَاءِ...): قاعدة تطبيع
  // (.)ٰ→ا العامة بتضيف ألف زيادة عن الرسم المعتاد اللي بيكتبها
  // التعرف الصوتي (واولئك مش واولايك) — بنحذفها كبديل فقط قبل حرف همزة.
  // الحركة ممكن تيجي بين الخنجرية والمدة (لَٰٓ) أو قبلها، فبنسمح بأي حركة بينهم
  if(/\u0670[\u064B-\u0652]*\u0653(?=[ءأؤإئ])/.test(w))
    out.push(w.replace(/\u0670([\u064B-\u0652]*)\u0653/g,'$1'));
  // همزة القطع بعد واو/فاء الوصل (وَأَسۡمِعۡ) أحيانًا بيلخبطها التعرف
  // الصوتي فبيكتبها بألف عادية بس من غير همزة أصلًا (واسمع) — بنولّد
  // بديل بحذف الهمزة زي ما بيكتبها التعرف، مش بتحويلها لألف عادي
  // (عشان محرف الوصل التلقائي بيدمجها فيبقى الناتج مختلف عن اللي اتسمع)
  if(/^[وف][\u064B-\u065F]?أ/.test(w))
    out.push(w.replace(/^([وف])[\u064B-\u065F]?أ/,'$1'));
  // كرسي الهمزة بعد ألف المد وقبل ضمير متصل (شُهَدَآءَكُم، أَبۡنَآءَكُمۡ، نِسَآءَكُمۡ):
  // المصحف بيكتب الهمزة على السطر (آء)، أما التعرف الصوتي بيكتبها بكرسي
  // حسب الإعراب اللي هو مابيسمعوش (شهدائكم / أبنائكم / نسائكم / نساؤكم)
  const _hz=/(ا\u0653|آ)([ءؤئ])(?=[\u064B-\u065F\u0670\u06E1\u08F0-\u08F2]*[ء-ي])/;
  const _hm=_hz.exec(w);
  if(_hm){
    for(const seat of ['ئ','ؤ','ء']){
      if(seat===_hm[2])continue;
      out.push(w.replace(new RegExp(_hz.source,'g'),'ا'+seat));
    }
  }
  // ألف المد المكتوبة خنجرية (خَلَٰقࣲ، كِتَٰب...): التعرف الصوتي أحيانًا بيسقط ألف المد
  // ويكتبها بدونها (خلق). ىٰ (ياء بخنجرية) ليها قاعدتها المستقلة فوق، ومدّة الهمزة (ٰٓ) فوق برضه
  for(let k=w.indexOf('\u0670');k>=0;k=w.indexOf('\u0670',k+1)){
    let b=k-1;
    while(b>=0&&/[ـ\u064B-\u065F\u06E1\u08F0-\u08F2]/.test(w.charAt(b)))b--;
    if(b<0||/[ىي]/.test(w.charAt(b)))continue;
    if(w.charAt(k+1)==='\u0653')continue;
    weak(w.slice(0,k)+w.slice(k+1));
  }
  // حذف ياء المتكلم/حرف المد الياء وصلًا قبل همزة الوصل (عَهۡدِى ٱلظَّٰلِمِينَ → «عهد الظالمين»):
  // الياء بتفضل مكتوبة في المصحف وبتسقط نطقًا لالتقاء الساكنين، فالتعرف الصوتي بيكتبها بدونها.
  // الشرط: كسرة + ياء بلا حركة في آخر الكلمة، والكلمة اللي بعدها بهمزة وصل، وأصل الكلمة ٣ حروف فأكتر
  if(nextW&&nextW.charAt(0)==='ٱ'&&/\u0650ى$/.test(w)){
    const base=w.replace(/[ـ\u064B-\u065F\u0670\u06D6-\u06ED\u08F0-\u08F2]/g,'');
    if(base.length-1>=3)out.push(w.replace(/ى$/,''));
  }
  // «لَهُمۡ / وَلَهُمۡ» بيسمعها التعرف الصوتي «ما له» (ملزوقة «ماله»)
  if(/^[وف]?لهم$/.test(_pkey(w)))out.push('ماله');
  return out;
}

function _rasmMaps(ans){
  const ws=String(ans||'').trim().split(/\s+/);
  const E=Object.create(null),L=Object.create(null),bE=[],bL=[];
  const put=function(map,bad,k,w){
    if(!k)return;
    if(k in map){if(map[k]!==w)bad.push(k);}else map[k]=w;
  };
  const _own=new Set(ws.map(_pkey));
  const _skip=alt=>_own.has(_pkey(alt));
  for(let wi=0;wi<ws.length;wi++){
    const w=ws[wi];
    put(E,bE,normalize(w),w);
    const vs=_rasmVoiceForms(w,ws[wi+1],_skip);
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

function _numWordValue(w){const n=normalize(w);return NUM_WORDS.hasOwnProperty(n)?NUM_WORDS[n]:null;}

function _combineNumVals(vals){
  if(vals.length===1)return vals[0];
  const a=vals[0],b=vals[1],c=vals[2];
  if(vals.length===2)return((b===100||b===1000)&&a>=1&&a<=9)?a*b:a+b;
  return((b===100||b===1000)&&a>=1&&a<=9)?a*b+c:a+b+c;
}

function _expandDigitWord(raw,ansWords){
  const val=parseInt(raw.replace(/[٠-٩]/g,d=>String(d.charCodeAt(0)-0x0660)),10);
  if(isNaN(val))return null;
  for(let start=0;start<ansWords.length;start++){
    for(let len=1;len<=3&&start+len<=ansWords.length;len++){
      const seq=ansWords.slice(start,start+len);
      const vals=seq.map(_numWordValue);
      if(vals.some(v=>v===null))continue;
      if(_combineNumVals(vals)===val)return seq;
    }
  }
  return null;
}

// إدغام/إخفاء النون: التعرف الصوتي بيلزق كلمتين متجاورتين في الإجابة في كلمة واحدة
// والنون مبلوعة («عَن مِّلَّةِ» ← «عمله»، «مِن رَّبِّهِمۡ» ← «مربهم»). بنجرّب صيغ الالتصاق
// الممكنة (مع حذف النون وبدونه، والإقلاب قبل الباء) وبنرجّع الكلمتين برسمهم الأصلي لو طابقت
function _mergedForms(r1,r2){
  const dd=x=>x.replace(/(.)\1+/g,'$1');
  const c=[r1+r2,dd(r1+r2)];
  if(r1.endsWith('ن')&&r1.length>1){
    const h=r1.slice(0,-1);
    c.push(h+r2,dd(h+r2));
    if(r2.charAt(0)==='ب')c.push(h+'م'+r2,dd(h+'م'+r2));
  }
  return c;
}
function _splitMergedFromAns(word,ansWords){
  const a=normalize(word);
  if(!a)return null;
  for(const aw of ansWords)if(normalize(aw)===a)return null;   // موجودة بذاتها — مش ملزوقة
  for(let k=0;k<ansWords.length-1;k++){
    const r1=normalize(ansWords[k]),r2=normalize(ansWords[k+1]);
    if(!r1||!r2)continue;
    if(_mergedForms(r1,r2).indexOf(a)>=0)return [ansWords[k],ansWords[k+1]];
  }
  return null;
}

function _fixWordsCore(words, answer){
  words = collapseMuqattaat(words, answer || '');
  const _ansWords = answer ? answer.trim().split(/\s+/) : [];
  const out = [];
  for(let i=0; i<words.length; i++){
    if(i<words.length-2 && normalize(words[i])==='او' && normalize(words[i+1])==='كل' && normalize(words[i+2])==='ما'){
      out.push(words[i]+words[i+1]+words[i+2]); i+=2; continue;
    }
    if(i<words.length-1 && normalize(words[i])==='او' && normalize(words[i+1])==='كلما'){
      out.push(words[i]+words[i+1]); i++; continue;
    }
    if(i<words.length-1 && normalize(words[i])==='ولا' && normalize(words[i+1])==='تجدنهم'){
      out.push('ولتجدنهم'); i++; continue;
    }
    if(words[i]==='ممنع'){ out.push('ممن','منع'); continue; }
    if(words[i]==='بلا'){ out.push('بلى'); continue; }
    if(words[i]==='بن'){ out.push('ابن'); continue; }
    // أَن طَهِّرَا: إخفاء النون عند الطاء بيخلي التعرف الصوتي يلزقهم كلمة واحدة
    // "انطهر" (وبيسقط ألف التثنية كمان)، فبنفصلها لرسمها الصحيح
    if(normalize(words[i])==='انطهر'){ out.push('أَن','طَهِّرَا'); continue; }
    // عَن مِّلَّةِ ← «عمله»: إدغام النون بيلزق الكلمتين (وبنفس الفكرة كل نون ساكنة قبل ي ر م ل و ن ب)
    if(_ansWords.length>1){
      const _sp=_splitMergedFromAns(words[i],_ansWords);
      if(_sp){ out.push(..._sp); continue; }
    }
    // يَسُومُونَكُمۡ: كلمة نادرة على التعرف الصوتي، بيسمعها (يصومنكم / يسومنكم / يسمونكم) رغم النطق الصحيح بالسين
    if(_ansWords.length && /^ي[سص](?:وم|م)(?:و?ن)كم$/.test(normalize(words[i]))){
      const _ya=_ansWords.find(aw=>normalize(aw)==='يسومونكم');
      if(_ya){ out.push(_ya); continue; }
    }
    // لَهُمۡ / وَلَهُمۡ: التعرف الصوتي بيسمعها «ما له» (كلمتين) أو «ماله» — بنرجّعها لرسمها من الإجابة
    // حسب أقرب موضع «لهم» في الإجابة. الحماية: مفيش «ما له» متجاورين في الإجابة نفسها
    if(_ansWords.length){
      const _nw=normalize(words[i]);
      const _two=(_nw==='ما'&&i+1<words.length&&normalize(words[i+1])==='له');
      if(_two||_nw==='ماله'){
        const _isL=w=>/^[وف]?لهم$/.test(_pkey(w));
        const _cands=[];let _blocked=false;
        for(let k=0;k<_ansWords.length;k++){
          if(_isL(_ansWords[k]))_cands.push(k);
          if(k>0&&normalize(_ansWords[k-1])==='ما'&&/^[وف]?له$/.test(_pkey(_ansWords[k])))_blocked=true;
        }
        if(_cands.length&&!_blocked){
          let c=_cands[0];
          for(const k of _cands)if(Math.abs(k-out.length)<Math.abs(c-out.length))c=k;
          if(Math.abs(c-out.length)<=3||_cands.length===1){
            // «مَا لَهُمۡ» أصلاً في الإجابة: «ما» موجودة قبلها فنحتفظ بها
            if(c>0&&normalize(_ansWords[c-1])==='ما'&&_two)out.push(words[i]);
            out.push(_ansWords[c]);
            if(_two)i++;
            continue;
          }
        }
      }
    }
    if(_ansWords.length && /^[0-9٠-٩]+$/.test(words[i])){
      const _exp=_expandDigitWord(words[i],_ansWords);
      if(_exp){ out.push(..._exp); continue; }
    }
    if(_ansWords.length && normalize(words[i]) && !_ansWords.some(aw=>normalize(aw)===normalize(words[i]))){
      const _wa=_ansWords.find(aw=>normalize(aw)===normalize(words[i])+'ا');
      if(_wa){ out.push(_wa); continue; }
    }
    out.push(words[i]);
  }
  return snapToRasm(out, answer || '');
}
