/* دربي — توحيد مفاتيح التقدّم عند القراءة فقط (لا يغيّر ما في التخزين).
   صفحات اختبار البقرة والفاتحة حفظت تقدّمها قديماً بمفتاح قصير (p10 / fatiha)،
   بينما تسمية الصفحات في «تقدّمي» والرئيسية هي الاسم الكامل (albaqara_p10 / alfatiha).
   هذا الملف يدمج المفتاحين عند العرض حتى يظهر التقدّم كاملاً. */
(function(w){
  'use strict';
  function keyToStem(k){
    k=String(k||'');
    if(k==='fatiha')return 'alfatiha';
    if(/^p\d+$/.test(k))return 'albaqara_'+k;
    return k;
  }
  function mergeEntry(a,b){ // a: الموجود، b: الوارد — نحتفظ بالأفضل
    var o={},k;
    for(k in a)o[k]=a[k];
    for(k in b){
      if(k==='lastVisited'){if(!o.lastVisited||String(b.lastVisited)>String(o.lastVisited))o.lastVisited=b.lastVisited;}
      else if(o[k]&&typeof o[k]==='object'&&b[k]&&typeof b[k]==='object'){
        o[k]={done:!!(o[k].done||b[k].done),score:Math.max(o[k].score||0,b[k].score||0)};
        for(var f in b[k])if(!(f in o[k]))o[k][f]=b[k][f];
      }else if(!(k in o))o[k]=b[k];
    }
    return o;
  }
  function normProgress(raw){
    var out={};
    Object.keys(raw||{}).forEach(function(k){
      var s=keyToStem(k),e=raw[k];
      if(!e||typeof e!=='object')return;
      out[s]=out[s]?mergeEntry(out[s],e):e;
    });
    return out;
  }
  w.darbiKeyToStem=keyToStem;
  w.darbiNormProgress=normProgress;
})(window);
