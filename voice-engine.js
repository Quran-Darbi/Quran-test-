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

// مَـَٔابًا (النبأ): التسجيل الصوتي بيكتب همزة الوسط بصورة "مئابا" (ئ)، وقاعدة
// ئ→ي العامة (المصممة لخطيئته/متكئين) بتحوّلها غلط لـ"ميابا" بدل "مابا"
// الصحيحة (الهمزة هنا صوتها ألف مد مش ياء) — استثناء بعد القاعدة العامة (2026-09-27)
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
    .replace(/الربوا/g,'الربا').replace(/رحمان/g,'رحمن').replace(/(?<=^|\s)فازالهما(?=\s|$)/g,'فازلهما').replace(/(?<=^|\s)فاذلهما(?=\s|$)/g,'فازلهما').replace(/(?<=^|\s)فادراتم(?=\s|$)/g,'فادارتم').replace(/(?<=^|\s)فادرأتم(?=\s|$)/g,'فادارتم').replace(/(?<=^|\s)فاداراتم(?=\s|$)/g,'فادارتم').replace(/(?<=^|\s)بن(?=\s|$)/g,'ابن').replace(/نصاري(?=\s|$)/g,'نصارا').replace(/(?<=^|\s)ناتي(?=\s|$)/g,'نات').replace(/(?<=^|\s)ولا تجدنهم(?=\s|$)/g,'ولتجدنهم').replace(/(?<=^|\s)ولاتجدنهم(?=\s|$)/g,'ولتجدنهم').replace(/(?<=^|\s)او كل ما(?=\s|$)/g,'اوكلما').replace(/(?<=^|\s)او كلما(?=\s|$)/g,'اوكلما').replace(/(?<=^|\s)بلي(?=\s|$)/g,'بلا').replace(/(?<=^|\s)اهاني(?=\s|$)/g,'اهان').replace(/(?<=^|\s)تكفروني(?=\s|$)/g,'تكفرون').replace(/(?<=^|\s)فاتقوني(?=\s|$)/g,'فاتقون').replace(/(?<=^|\s)فارهبوني(?=\s|$)/g,'فارهبون').replace(/(?<=^|\s)وتقوني(?=\s|$)/g,'وتقون').replace(/(?<=^|\s)يقضي(?=\s|$)/g,'يقض').replace(/(?<=^|\s)ينتهي(?=\s|$)/g,'ينته').replace(/(?<=^|\s)اوفي(?=\s|$)/g,'اوف').replace(/(?<=^|\s)يسري(?=\s|$)/g,'يسر').replace(/(?<=^|\s)ميابا(?=\s|$)/g,'مابا')
    // يَسْـَٔلُ (القيامة): همزة الوسط ممكن تُكتب/تُسمع "يسئل" (بالياء)، وقاعدة
    // ئ→ي العامة بتحوّلها لـ"يسيل" (كلمة تانية معناها "يجري")، فبنستثنيها هنا
    // لترجع لنفس صورة "يسأل" الصحيحة (2026-09-27)
    .replace(/^يسيل$/,'يسال')
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
  const out=words.map(function(w){
    const e=normalize(w);
    if(!e)return w;
    if(e in m.E)return m.E[e];
    if(e in m.L)return m.L[e];
    return w;
  });
  // كلمات المفتاح المشترك (مِن/مَن/مِنۡ → «من»، ٱللَّهُ/ٱللَّهِ → «الله»): المفتاح الملتبس بيتشال من
  // الخريطة فالكلمة كانت بتفضل كما نطقها التسجيل. بنحاذيها بالترتيب مع كلمات الإجابة (LCS) فتظهر برسم المصحف
  const aw=String(ans).trim().split(/\s+/).filter(function(x){return normalize(x)!=='';});
  const A=aw.map(normalize),U=words.map(normalize);
  const n=A.length,k=words.length;
  if(!n||n*k>40000)return out;
  const dp=[];for(let i=0;i<=n;i++)dp.push(new Int32Array(k+1));
  for(let i=1;i<=n;i++)for(let j=1;j<=k;j++)
    dp[i][j]=(U[j-1]&&A[i-1]===U[j-1])?dp[i-1][j-1]+1:Math.max(dp[i-1][j],dp[i][j-1]);
  let i=n,j=k;
  const matchI=new Array(n).fill(-1);
  while(i>0&&j>0){
    if(U[j-1]&&A[i-1]===U[j-1]){out[j-1]=aw[i-1];matchI[i-1]=j-1;i--;j--;}
    else if(dp[i][j-1]>=dp[i-1][j])j--;
    else i--;
  }
  // المرحلة الثانية: بدائل التعرف الصوتي (جدول STT_WORD_ALTS + قواعد التاء/التثنية/الإقلاب/ص-س) داخل الفجوات فقط
  for(const [ri,uj] of sttRelaxedMatch(aw,U,matchI,normalize))out[uj]=aw[ri];
  return out;
}

function _numWordValue(w){const n=normalize(w);return NUM_WORDS.hasOwnProperty(n)?NUM_WORDS[n]:null;}

function _combineNumVals(vals){
  if(vals.length===1)return vals[0];
  const a=vals[0],b=vals[1],c=vals[2];
  // خَمۡسِينَ أَلۡفَ = 50×1000 (مش 50+1000)، ثَلَـٰثَ مِائَةࣲ = 3×100
  const mul=(b===100||b===1000)&&a>=1&&a<b;
  if(vals.length===2)return mul?a*b:a+b;
  return mul?a*b+c:a+b+c;
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
function _mergedForms(r1,r2,raw1,raw2){
  const dd=x=>x.replace(/(.)\1+/g,'$1');
  const c=[r1+r2,dd(r1+r2)];
  if(r1.endsWith('ن')&&r1.length>1){
    const h=r1.slice(0,-1);
    c.push(h+r2,dd(h+r2));
    if(r2.charAt(0)==='ب')c.push(h+'م'+r2,dd(h+'م'+r2));
  }
  // فَلَا ٱقْتَحَمَ ← «فلقتحم»: التقاء الساكنين (ألف "لا" + همزة الوصل) بيسقط الألفين نطقًا
  if(r1.endsWith('ا')&&r1.length>1&&raw2&&raw2.charAt(0)==='ٱ')
    c.push(r1.slice(0,-1)+r2.slice(1));
  // إدغام التنوين في (ي ر م ل و ن): «أَذࣰى لَّهُمۡ» ← «اذلهم» — حرف التنوين الحامل (ا/ى) يسقط نطقًا
  if(raw1&&/[\u064B-\u064D\u08F0-\u08F2][اى]?$/.test(raw1)&&/^[يرملون]/.test(r2)&&r1.length>2&&/[اي]$/.test(r1)){
    const t=r1.slice(0,-1)+r2;c.push(t,dd(t));
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
    if(_mergedForms(r1,r2,ansWords[k],ansWords[k+1]).indexOf(a)>=0)return [ansWords[k],ansWords[k+1]];
  }
  return null;
}

// تنظيف كلمات التعرف الصوتي من الشوائب (أحرف الاتجاه/العرض الصفري، الترقيم، أشكال العرض، الياء/الكاف الفارسيتين).
// النجمة (*) بتفضل عشان فلتر الألفاظ (انظر _unmaskFromAns)
function _cleanSTT(words){
  const out=[];
  for(const w of words){
    let x=String(w);
    try{x=x.normalize('NFKC');}catch(e){}
    x=x.replace(/[\u200B-\u200F\u202A-\u202E\u2066-\u2069\uFEFF]/g,'')
       .replace(/[،؛؟,;:!?.…"'“”‘’«»()\[\]{}<>\-–—_]/g,'')
       .replace(/ک/g,'ك').replace(/ی/g,'ى').replace(/ھ/g,'ه');
    if(x)out.push(x);
  }
  return out;
}
// فلتر الألفاظ: «زُبَرَ» بيكتبها التعرف الصوتي «ز**» (أول حرف + نجوم بعدد الحروف الباقية).
// بنرجّعها لكلمة الإجابة اللي بتطابق الحروف الظاهرة وعدد الحروف الكلي (الأقرب لموضعها لو تعدّدت)
function _unmaskFromAns(w,ansWords,pos){
  if(String(w).indexOf('*')<0||!ansWords.length)return null;
  const t=_pkey(String(w).replace(/\*/g,'\u0001')).replace(/\u0001/g,'*');
  if(!t||t.charAt(0)==='*')return null;
  const re=new RegExp('^'+t.replace(/[.+?^${}()|[\]\\]/g,'\\$&').replace(/\*/g,'.')+'$');
  const idxs=[];
  for(let i=0;i<ansWords.length;i++)if(re.test(_pkey(ansWords[i])))idxs.push(i);
  if(!idxs.length)return null;
  const distinct=new Set(idxs.map(i=>_pkey(ansWords[i])));
  if(distinct.size===1)return ansWords[idxs[0]];
  let best=idxs[0];
  for(const i of idxs)if(Math.abs(i-pos)<Math.abs(best-pos))best=i;
  return Math.abs(best-pos)<=6?ansWords[best]:null;
}

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
  {ref:'يوف',heard:['وف','وفق','يوفي','يوفا']},
  {ref:'يأب',heard:['يابى','يابي','يابا']},
  {ref:'لبثت',heard:['لبست']},
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

function _fixWordsCore(words, answer){
  words = _cleanSTT(words);
  words = collapseMuqattaat(words, answer || '');
  const _ansWords = answer ? answer.trim().split(/\s+/) : [];
  const out = [];
  for(let i=0; i<words.length; i++){
    // نداء: «يا» + الكلمة التالية كلمة واحدة في المصحف (يَٰٓأَيُّهَا، يَٰلَيۡتَنِي، يَٰٓأَبَتِ) — مطابق لـ mergeYaAyyuha في recitation.html
    if(i<words.length-1 && normalize(words[i])==='يا' && normalize(words[i+1])!=='عين' && normalize(words[i+1])!=='سين'){
      out.push(words[i]+words[i+1]); i++; continue;
    }
    if(i<words.length-2 && normalize(words[i])==='او' && normalize(words[i+1])==='كل' && normalize(words[i+2])==='ما'){
      out.push(words[i]+words[i+1]+words[i+2]); i+=2; continue;
    }
    if(i<words.length-1 && normalize(words[i])==='او' && normalize(words[i+1])==='كلما'){
      out.push(words[i]+words[i+1]); i++; continue;
    }
    if(i<words.length-1 && normalize(words[i])==='ولا' && normalize(words[i+1])==='تجدنهم'){
      out.push('ولتجدنهم'); i++; continue;
    }
    if(_ansWords.length&&words[i].indexOf('*')>=0){
      const _um=_unmaskFromAns(words[i],_ansWords,out.length);
      if(_um){ out.push(_um); continue; }
    }
    if(words[i]==='ممنع'){ out.push('ممن','منع'); continue; }
    if(words[i]==='بلا'){ out.push('بلى'); continue; }
    if(words[i]==='بن'){ out.push('ابن'); continue; }
    // أَن طَهِّرَا: إخفاء النون عند الطاء بيخلي التعرف الصوتي يلزقهم كلمة واحدة
    // "انطهر" (وبيسقط ألف التثنية كمان)، فبنفصلها لرسمها الصحيح
    if(normalize(words[i])==='انطهر'){ out.push('أَن','طَهِّرَا'); continue; }
    // عَن مِّلَّةِ ← «عمله»: إدغام النون بيلزق الكلمتين (وبنفس الفكرة كل نون ساكنة قبل ي ر م ل و ن ب)
    if(_ansWords.length>1){
      const _sp=_splitMergedFromAns(words[i],_ansWords.filter(function(x){return normalize(x)!=='';}));
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
      // حرف المد لا يسقط إلا نطقًا: الكلمة التالية بهمزة وصل (التقاء ساكنين)
      const _wa=_ansWords.find((aw,ai)=>normalize(aw)===normalize(words[i])+'ا'&&_ansWords[ai+1]&&/^[\u064B-\u065F\u06D6-\u06ED]*ٱ/.test(_ansWords[ai+1]));
      if(_wa){ out.push(_wa); continue; }
    }
    out.push(words[i]);
  }
  const _ansClean=_ansWords.filter(function(x){return normalize(x)!=='';});
  return snapToRasm(sttPhrasePass(out, _ansClean, normalize), answer || '');
}


// ===== أرقام الآيات وعلامات الوقف في الاختبار الصعب (عرض فقط — لا يمس المطابقة) =====
// القاعدة: كل نص قرآني يُعرض بآياته ووقفاته. نتيجة الاختبار الصعب (wordDiff) كانت بتعرض رقمًا واحدًا في
// آخر الإجابة ومن غير علامات وقف. هنا بنغلّف wordDiff من برّه (من غير ما نلمس منطقها في الصفحات) بحيث:
//   • أرقام الآيات الحقيقية بعد آخر كلمة في كل آية داخل الإجابة (من AYAT/AYAT_NUMS في الصفحة)
//   • علامات الوقف (ۖ ۗ ۚ ۛ ...) وعلامة السجدة ۩ بعد كلماتها بدل ما تختفي
//   • ۩ مش كلمة مطلوب نطقها: بتتشال من المرجع المقارَن (كانت بتخلي آية السجدة في مريم ص٣٠٩ والنجم ص٥٢٨ مستحيل تكتمل)
//   • مقاطع الآية (البقرة ص٤٨) ما بيتحطش بعدها رقم إلا في آخر مقطع من الآية
function _darbiCleanAns(a){return String(a||'').replace(/\s*۩/g,'');}
function _darbiAyahNum(e){
  if(typeof AYAT_NUMS!=='undefined'&&AYAT_NUMS&&typeof AYAT!=='undefined'&&AYAT_NUMS.length===AYAT.length)return AYAT_NUMS[e]>0?AYAT_NUMS[e]:0;
  return e+1;
}
function _darbiPlan(answer){
  const toks=String(answer||'').trim().split(/\s+/).filter(Boolean);
  const words=[],waqf=Object.create(null);let idx=-1;
  for(const t of toks){
    if(normalize(t)!==''&&t!=='۩'){idx++;words.push(t);}
    else if(idx>=0&&t!=='۞'){waqf[idx]=(waqf[idx]?waqf[idx]+' ':'')+t;}
  }
  let ends=Object.create(null),aligned=false;
  try{
    if(typeof AYAT!=='undefined'&&Array.isArray(AYAT)&&AYAT.length){
      const A=AYAT.map(function(t){return String(t).trim().split(/\s+/).filter(function(x){return normalize(x)!==''&&x!=='۩';}).map(normalize);});
      const T=words.map(normalize);
      for(let s=0;s<A.length&&!aligned;s++){
        let pos=0;const tmp=Object.create(null);
        for(let e=s;e<A.length;e++){
          let ok=A[e].length>0;
          for(let k=0;ok&&k<A[e].length;k++)if(T[pos+k]!==A[e][k])ok=false;
          if(!ok)break;
          pos+=A[e].length;
          const num=_darbiAyahNum(e);
          if(num)tmp[pos-1]=num;
          if(pos===T.length){aligned=true;ends=tmp;break;}
        }
      }
    }
  }catch(err){aligned=false;}
  return {words:words,waqf:waqf,ends:ends,aligned:aligned};
}
function _darbiMark(cls,text){
  const el=document.createElement('span');
  el.className=cls;el.setAttribute('translate','no');
  if(cls==='waqf-mark')el.style.cssText='color:var(--gold,#c4a84a);margin:0 2px;font-size:.95em;';
  el.textContent=text;
  return el;
}
function _darbiDecorateDiff(html,correctAnswer){
  const plan=_darbiPlan(correctAnswer);
  const holder=document.createElement('div');holder.innerHTML=html;
  const box=holder.querySelector('div[style*="font-size:18px"]');
  if(!box)return html;
  if(plan.aligned)Array.prototype.slice.call(box.children).forEach(function(k){if(k.classList.contains('ayah-end'))k.remove();});
  let refI=-1;
  Array.prototype.slice.call(box.children).forEach(function(el){
    if(el.classList.contains('ayah-end'))return;
    if(/line-through/.test(el.getAttribute('style')||''))return;            // كلمة زيادة قالها المستخدم
    refI++;
    let last=el;
    if(plan.waqf[refI]){const m=_darbiMark('waqf-mark',plan.waqf[refI]);last.after(document.createTextNode(' '),m);last=m;}
    if(plan.aligned&&plan.ends[refI]){const a=_darbiMark('ayah-end','﴿'+plan.ends[refI]+'﴾');last.after(document.createTextNode(' '),a);}
  });
  return holder.innerHTML;
}
function _darbiDecorateTranscript(box){
  const q=(typeof questions!=='undefined'&&typeof qIndex!=='undefined')?questions[qIndex]:null;
  if(!q||!q.answer)return;
  Array.prototype.slice.call(box.querySelectorAll('.darbi-mark')).forEach(function(n){n.remove();});
  const spans=Array.prototype.slice.call(box.querySelectorAll('.rec-word'));
  if(!spans.length)return;
  const plan=_darbiPlan(q.answer);
  const R=plan.words.map(normalize),U=spans.map(function(sp){return normalize(sp.textContent);});
  const n=R.length,m=U.length;
  if(!n||n*m>40000)return;
  const dp=[];for(let i=0;i<=n;i++)dp.push(new Int32Array(m+1));
  for(let i=1;i<=n;i++)for(let j=1;j<=m;j++)
    dp[i][j]=(U[j-1]&&R[i-1]===U[j-1])?dp[i-1][j-1]+1:Math.max(dp[i-1][j],dp[i][j-1]);
  const refOf=new Array(m).fill(-1);
  let i=n,j=m;
  while(i>0&&j>0){
    if(U[j-1]&&R[i-1]===U[j-1]){refOf[j-1]=i-1;i--;j--;}
    else if(dp[i][j-1]>=dp[i-1][j])j--;
    else i--;
  }
  spans.forEach(function(sp,k){
    const r=refOf[k];
    if(r<0)return;
    let last=sp;
    if(plan.waqf[r]){const w=_darbiMark('waqf-mark darbi-mark',plan.waqf[r]);last.after(w);last=w;}
    if(plan.aligned&&plan.ends[r]){const a=_darbiMark('ayah-end darbi-mark','﴿'+plan.ends[r]+'﴾');last.after(a);}
  });
}
(function _darbiInstallDisplay(){
  function go(){
    try{
      if(typeof wordDiff==='function'&&!wordDiff.__darbi){
        const orig=wordDiff;
        const wrapped=function(userVal,correctAnswer,q){
          const html=orig.call(this,userVal,_darbiCleanAns(correctAnswer),q);
          try{return _darbiDecorateDiff(html,correctAnswer);}catch(e){return html;}
        };
        wrapped.__darbi=true;
        window.wordDiff=wrapped;
      }
      const zone=document.getElementById('answer-zone')||document.body;
      const obs=new MutationObserver(function(){
        obs.disconnect();
        try{Array.prototype.slice.call(document.querySelectorAll('.rec-transcript')).forEach(_darbiDecorateTranscript);}catch(e){}
        obs.observe(zone,{childList:true,subtree:true});
      });
      obs.observe(zone,{childList:true,subtree:true});
    }catch(e){}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
