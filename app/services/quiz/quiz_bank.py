"""Curated and dynamic quiz question generator with 3 difficulty levels and randomized options.

Supports Uzbek, English, and Russian across various academic subjects and general knowledge.
Fully supports 3 distinct difficulty tiers (easy, medium, hard) with dynamic variation.
"""

import random
from typing import Any


def _create_q(
    question: str,
    correct: str,
    distractors: list[str],
    explanation: str,
) -> dict[str, Any]:
    """Helper to shuffle options and assign randomized correct_option letter (A, B, C, D)."""
    options_raw = [(correct, True)] + [(d, False) for d in distractors[:3]]
    random.shuffle(options_raw)

    letters = ["A", "B", "C", "D"]
    options: dict[str, str] = {}
    correct_option = "A"

    for i, (text, is_correct) in enumerate(options_raw):
        letter = letters[i]
        options[letter] = text
        if is_correct:
            correct_option = letter

    return {
        "question": question,
        "options": options,
        "correct_option": correct_option,
        "explanation": explanation,
    }


# Catalog organized by language -> category -> difficulty (easy, medium, hard)
QUESTIONS_BANK: dict[str, dict[str, dict[str, list[dict[str, Any]]]]] = {
    "uz": {
        "physics": {
            "easy": [
                _create_q(
                    "Xalqaro birliklar sistemasida (SI) bosimning asosiy o'lchov birligi nima?",
                    "Paskal (Pa)",
                    ["Nyuton (N)", "Joul (J)", "Vatt (W)"],
                    "Bosim birligi Paskal (Pa) bo'lib, 1 Pa = 1 N/m² ga teng.",
                ),
                _create_q(
                    "Mexanikada to'g'ri chiziqli tekis harakat tezligini topish formulasi qaysi?",
                    "v = s / t",
                    ["v = s * t", "v = a * t²", "v = m / s"],
                    "Tezlik masofani vaqtga nisbatiga teng: v = s / t.",
                ),
                _create_q(
                    "Vakuumda yorug'likning tarqalish tezligi taxminan qanchaga teng?",
                    "300 000 km/s",
                    ["150 000 km/s", "30 000 km/s", "1 000 000 km/s"],
                    "Yorug'likning vakuumdagi tezligi c ≈ 300 000 km/s (3×10⁸ m/s) dir.",
                ),
                _create_q(
                    "Normal atmosfera bosimida toza suv necha gradus Selsiyda qaynaydi?",
                    "100°C",
                    ["80°C", "90°C", "120°C"],
                    "Normal bosimda (101.3 kPa) suv 100°C da qaynash holatiga o'tadi.",
                ),
                _create_q(
                    "Jismga ta'sir qiluvchi og'irlik kuchi qaysi formula bilan aniqlanadi?",
                    "F = m * g",
                    ["F = m / g", "F = m * v", "F = g / m"],
                    "Og'irlik kuchi jism massasi va erkin tushish tezlanishi ko'paytmasiga teng: F = mg.",
                ),
                _create_q(
                    "Tovush to'lqinlari quyidagi qaysi muhitda tarqala olmaydi?",
                    "Vakuumda (havosiz bo'shliqda)",
                    ["Suvda", "Temirda", "Havoda"],
                    "Tovush mexanik to'lqin bo'lganligi uchun uning tarqalishi uchun moddiy muhit zarur, vakuumda tarqala olmaydi.",
                ),
            ],
            "medium": [
                _create_q(
                    "Paskal qonuniga ko'ra, yopiq idishdagi suyuqlik yoki gazga berilgan tashqi bosim qanday tarqaladi?",
                    "Barcha yo'nalishlar bo'ylab o'zgarishsiz bir xil tarqaladi",
                    [
                        "Faqat idishning pastki qismiga yo'naladi",
                        "Suyuqlik chuqurlashgan sari bosim yo'qoladi",
                        "Faqat idish devorlariga to'g'ri burchak ostida ta'sir qiladi",
                    ],
                    "Paskal qonuniga binoan, suyuqlik yoki gazga berilgan bosim har bir nuqtaga bir xil va o'zgarishsiz uzatiladi.",
                ),
                _create_q(
                    "Suyuqlikka botirilgan jismga ta'sir etuvchi Arximed kuchi qaysi kattaliklarga to'g'ri mutanosib?",
                    "Suyuqlik zichligi va jismning botgan qismi hajmiga",
                    [
                        "Faqat jismning umumiy og'irligiga",
                        "Idish shakli va undagi suyuqlik massasiga",
                        "Jismning tayyorlangan moddasiga",
                    ],
                    "F_A = ρ * g * V formulasi bo'yicha Arximed kuchi suyuqlik zichligi va botgan hajmga to'g'ri mutanosibdir.",
                ),
                _create_q(
                    "Nyutonning ikkinchi qonunining matematik ifodasi qaysi?",
                    "F = m * a",
                    ["E = m * c²", "P = F / S", "A = F * s"],
                    "Nyutonning II qonuniga ko'ra, kuch massa va tezlanish ko'paytmasiga teng: F = ma.",
                ),
                _create_q(
                    "Elektr zanjiri qismidagi Om qonunining ifodasi qaysi?",
                    "I = U / R",
                    ["U = I / R", "R = I * U", "P = I² / R"],
                    "Om qonuniga ko'ra tok kuchi kuchlanishga to'g'ri, qarshilikka teskari mutanosib: I = U/R.",
                ),
                _create_q(
                    "Jismning kinetik energiyasini hisoblash formulasi qaysi?",
                    "E = (m * v²) / 2",
                    ["E = m * g * h", "E = m * v", "E = (m² * v) / 2"],
                    "Kinetik energiya jism massasi va tezligi kvadratining yarmiga teng: E_k = mv²/2.",
                ),
                _create_q(
                    "Ketma-ket ulangan ikkita rezistorning (R1=4 Om, R2=6 Om) umumiy qarshiligi qancha?",
                    "10 Om",
                    ["2.4 Om", "24 Om", "2 Om"],
                    "Ketma-ket ulanishda qarshiliklar qo'shiladi: R = R1 + R2 = 4 + 6 = 10 Om.",
                ),
            ],
            "hard": [
                _create_q(
                    "Kvant mexanikasida statsionar holatdagi zarracha uchun Shredinger tenglamasi nimani tavsiflaydi?",
                    "Zarrachaning fazoviy to'lqin funksiyasi va energiya sathlarini",
                    [
                        "Zarrachaning aniq trayektoriyasini",
                        "Zarrachaning klassik tezligi va bosib o'tgan yo'lini",
                        "Fotonlarning yorug'lik tezligidagi geometrik sinishini",
                    ],
                    "Shredinger tenglamasi mikrodunyo zarrachalarining to'lqin funksiyasi (holati) va energiya spektri o'zgarishini tavsiflaydi.",
                ),
                _create_q(
                    "Ideal Karno siklining foydali ish koeffitsiyenti (FIK) qaysi ifoda orqali aniqlanadi?",
                    "η = (T1 - T2) / T1",
                    ["η = (T2 - T1) / T2", "η = T1 / T2", "η = 1 - (T1 / T2)"],
                    "Karno siklining FIKi isitgich (T1) va sovitgich (T2) mutlaq haroratlariga bog'liq: η = (T1 - T2) / T1.",
                ),
                _create_q(
                    "Eynshteynning fotoeffekt tenglamasi qaysi asosiy saqlanish qonuniga tayanadi?",
                    "Energiyaning saqlanish qonuniga (hν = A + E_k)",
                    [
                        "Impulsning saqlanish qonuniga",
                        "Elektr zaryadining saqlanish qonuniga",
                        "Massaning saqlanish qonuniga",
                    ],
                    "Eynshteyn tenglamasi yutilgan foton energiyasi elektronning chiqish ishi va kinetik energiyasiga sarflanishini (energiyaning saqlanishini) ifodalaydi.",
                ),
                _create_q(
                    "Kirxgofning ikkinchi qoidasiga (konturlar qoidasi) ko'ra qaysi tasdiq to'g'ri?",
                    "Har qanday yopiq konturdagi EYuKlar yig'indisi zanjir qismlaridagi kuchlanish tushuvlari yig'indisiga teng",
                    [
                        "Tugunga kiruvchi toklar chiquvchi toklardan doim katta bo'ladi",
                        "Har qanday konturdagi to'liq quvvat nolga teng bo'ladi",
                        "Kondensator zaryadi zanjir qarshiligiga teskari mutanosib bo'ladi",
                    ],
                    "Kirxgofning 2-qonuniga binoan: ΣE = Σ(I * R), ya'ni yopiq konturda EYuKlar yig'indisi potensiallar tushuvlari yig'indisiga teng.",
                ),
                _create_q(
                    "Ideal tebranish konturidagi elektromagnit tebranishlar davri (Tomson formulasi) qaysi?",
                    "T = 2π * √(L * C)",
                    ["T = 2π * √(g / l)", "T = 2π / √(L * C)", "T = √(L / C)"],
                    "Tomson formulasi bo'yicha erkin tebranishlar davri induktivlik va sig'imga bog'liq: T = 2π√(LC).",
                ),
                _create_q(
                    "Mutlaq qora jismning to'liq nurlanish qobiliyati uning mutlaq haroratining nechanchi darajasiga mutanosib (Stefan-Bolsman qonuni)?",
                    "To'rtinchi darajasiga (T⁴)",
                    ["Ikkinchi darajasiga (T²)", "Birinchi darajasiga (T)", "Uchinchi darajasiga (T³)"],
                    "Stefan-Bolsman qonuniga ko'ra nurlanish intensivligi jismning mutlaq haroratining to'rtinchi darajasiga mutanosibdir (j = σT⁴).",
                ),
            ],
        },
        "programming": {
            "easy": [
                _create_q(
                    "Python dasturlash tilida konsolga ma'lumot chiqarish uchun qaysi funksiya ishlatiladi?",
                    "print()",
                    ["echo()", "console.log()", "write()"],
                    "Python tilida ekranga matn yoki ma'lumot chiqarish uchun print() standart funksiyasi qo'llaniladi.",
                ),
                _create_q(
                    "Python'da yangi funksiya e'lon qilish uchun qaysi kalit so'z ishlatiladi?",
                    "def",
                    ["function", "func", "define"],
                    "Python'da funksiyalar 'def' (define) kalit so'zi bilan e'lon qilinadi.",
                ),
                _create_q(
                    "Quyidagi ma'lumot turlaridan qaysi biri o'zgarmas (immutable) hisoblanadi?",
                    "tuple (kortej)",
                    ["list (ro'yxat)", "dict (lug'at)", "set (to'plam)"],
                    "Tuple yaratilgandan so'ng uning elementlarini o'zgartirish, qo'shish yoki o'chirish mumkin emas.",
                ),
                _create_q(
                    "Python'da ro'yxat (list) oxiriga yangi element qo'shish uchun qaysi metod ishlatiladi?",
                    "append()",
                    ["add()", "push()", "insert_last()"],
                    "Ro'yxatning append(item) metodi bitta yangi elementni ro'yxat oxiriga qo'shadi.",
                ),
                _create_q(
                    "Python tilida bir qatorli izoh (kommentariya) qaysi belgi bilan boshlanadi?",
                    "#",
                    ["//", "/*", "<!--"],
                    "Python'da bir qatorli izohlar panjara (#) belgisi bilan boshlanadi.",
                ),
                _create_q(
                    "Python'da butun sonli qiymatlarning ma'lumot turi nima deb ataladi?",
                    "int",
                    ["float", "str", "bool"],
                    "Butun sonlar 'int' (integer) turi sifatida saqlanadi.",
                ),
            ],
            "medium": [
                _create_q(
                    "Python'da '==' va 'is' operatorlari o'rtasidagi asosiy farq nima?",
                    "'==' qiymatlarni tekshiradi, 'is' esa xotiradagi ayni bitta ob'ektligini (id)",
                    [
                        "'==' faqat sonlar uchun, 'is' esa matnlar uchun",
                        "Ularning farqi yo'q, ikkisi to'liq ekvivalent",
                        "'is' qiymatni, '==' faqat ma'lumot turini tekshiradi",
                    ],
                    "'==' qiymatlar tengligini tekshiradi, 'is' esa ikkala o'zgaruvchi xotiradagi bir xil manzilga ishora qilishini bildiradi.",
                ),
                _create_q(
                    "Lug'atdan (dict) bir vaqtning o'zida ham kalit, ham qiymatlarni olish uchun qaysi metod ishlatiladi?",
                    "items()",
                    ["keys()", "values()", "pairs()"],
                    "dict.items() metodi (kalit, qiymat) juftliklaridan iborat ob'ekt qaytaradi.",
                ),
                _create_q(
                    "Kodni bajarish jarayonida yuzaga keladigan xatoliklarni (exception) xavfsiz tutib qolish qaysi blok yordamida amalga oshiriladi?",
                    "try ... except",
                    ["try ... catch", "do ... while", "try ... finally_catch"],
                    "Python sintaksisida kutilmagan istisnolarni ushlash try va except bloklari orqali amalga oshiriladi.",
                ),
                _create_q(
                    "Quyidagi list comprehension `[x for x in [1, 2, 3, 4] if x % 2 == 0]` natijasi nima bo'ladi?",
                    "[2, 4]",
                    ["[1, 3]", "[2]", "[4]"],
                    "Shart x % 2 == 0 faqat juft sonlarni (2 va 4) tanlab oladi.",
                ),
                _create_q(
                    "Python'da 'set' (to'plam) ma'lumot turining asosiy xususiyati nima?",
                    "Unda barcha elementlar unikal (takrorlanmas) bo'ladi",
                    [
                        "U har doim indeks bo'yicha qat'iy tartiblangan",
                        "Elementlar faqat matn ko'rinishida bo'lishi shart",
                        "U o'zgarmas (immutable) tur hisoblanadi",
                    ],
                    "Set to'plamidagi elementlar takrorlanmaydi va dublikatlar avtomatik filtrlanadi.",
                ),
                _create_q(
                    "Funksiya parametrlarida `*args` va `**kwargs` nima uchun qo'llaniladi?",
                    "`*args` ixtiyoriy sondagi pozitsion, `**kwargs` esa nomlangan kalitli argumentlarni qabul qilish uchun",
                    [
                        "`*args` faqat sonlarni, `**kwargs` faqat satrlarni qabul qiladi",
                        "`*args` global o'zgaruvchilarni, `**kwargs` lokal o'zgaruvchilarni bildiradi",
                        "Faqat generator funksiyalarda xotirani tejash uchun ishlatiladi",
                    ],
                    "`*args` o'zgaruvchan sondagi pozitsion argumentlarni tuple sifatida, `**kwargs` esa nomlangan argumentlarni dict sifatida uzatadi.",
                ),
            ],
            "hard": [
                _create_q(
                    "CPython implementatsiyasida GIL (Global Interpreter Lock) qanday asosiy vazifani bajaradi?",
                    "Bir vaqtning o'zida faqat bitta oqim (thread) Python baytkodini bajarishini ta'minlaydi",
                    [
                        "Barcha xotirani qattiq diskka avtomatik yozib boradi",
                        "Asinxron dasturlashdagi barcha coroutinelarni to'xtatib turadi",
                        "Koddagi sintaktik xatolarni tekshirib kompilyatsiya qiladi",
                    ],
                    "GIL CPython'da xotirani xavfsiz boshqarish (reference counting) uchun kiritilgan bo'lib, bir vaqtda faqat 1 ta thread baytkodni ijro etishini ta'minlaydi.",
                ),
                _create_q(
                    "Python'da Metaklass (Metaclass) nima va uning asosiy vazifasi nima?",
                    "Klasslarni yaratuvchi va ularning xulq-atvorini belgilovchi 'klassning klassi'",
                    [
                        "Faqat ma'lumotlar bazasi jadvallarini tuzuvchi maxsus modul",
                        "Oddiy funksiyalarni tezlatish uchun C tilidagi bog'lama",
                        "Meros olish zanjirida eng so'nggi instansiya",
                    ],
                    "Metaklass — bu klasslarni yaratuvchi shablon bo'lib, Python'da standart barcha klasslarning metaklassi `type` hisoblanadi.",
                ),
                _create_q(
                    "Python'da xotira tozalagich (Garbage Collector) qaysi ikki asosiy mexanizmga tayanadi?",
                    "Reference counting (havolalar sanog'i) va davriy havolalar (cyclic references) uchun siklik detektor",
                    [
                        "Faqat mark-and-sweep mexanizmi",
                        "Faqat operativ xotirani majburiy qayta yuklash",
                        "Tranzaksiyalar jurnali va xotira snapshots",
                    ],
                    "Python xotira boshqaruvida birlamchi havola sanog'i (ref count=0 bo'lganda o'chirish) va bir-biriga havola qiluvchi ob'ektlar uchun siklik GC ishlatiladi.",
                ),
                _create_q(
                    "Python'da generator funksiyalarda `yield` operatorining `return` dan asosiy farqi nima?",
                    "Holatni saqlab qiymat qaytaradi va keyingi `next()` chaqiruvida qolgan joyidan davom etadi",
                    [
                        "Xotiradan ro'yxatni to'liq yuklab darhol funksiyadan chiqadi",
                        "Faqat cheksiz sikllarni to'xtatish uchun xizmat qiladi",
                        "Hech qanday farqi yo'q, faqat sintaktik qulaylik",
                    ],
                    "Yield qiymatni qaytargan holda lokal o'zgaruvchilar holatini saqlaydi va lazy evaluation (kechiktirilgan hisoblash) ni ta'minlaydi.",
                ),
                _create_q(
                    "Python'da `__new__` va `__init__` metodlari orasidagi farq nima?",
                    "`__new__` ob'ekt instansiyasini xotirada yaratadi va qaytaradi, `__init__` esa mavjud ob'ektni initsializatsiya qiladi",
                    [
                        "`__init__` yangi ob'ekt yaratadi, `__new__` esa uni o'chiradi",
                        "`__new__` faqat statik metodlarda chaqiriladi, `__init__` chaqirilmaydi",
                        "Ularning ikkisi ham bir xil vazifani bajaradi va farqlanmaydi",
                    ],
                    "`__new__` — bu konstruktor bo'lib, yangi instansiya yaratadi; `__init__` esa initsializator bo'lib, yaratilgan ob'ektga boshlang'ich atributlarni beradi.",
                ),
                _create_q(
                    "Funksiya closure'larida (yopiq muhit) 'late binding' muammosi qanday namoyon bo'ladi?",
                    "Lokal funksiyalar tashqi o'zgaruvchini yaratilish vaqtida emas, chaqirilish vaqtidagi oxirgi qiymatini o'qiydi",
                    [
                        "Funksiya xotiradan juda kech o'chiriladi",
                        "Meros olingan metodlar chaqirilishda kechikadi",
                        "Import qilingan modullar navbatda kutib qoladi",
                    ],
                    "Late binding sababli loop ichida yaratilgan lambda yoki closure'lar o'zgaruvchining chaqirilgan paytdagi yakuniy qiymatiga ega bo'ladi.",
                ),
            ],
        },
        "mathematics": {
            "easy": [
                _create_q(
                    "To'g'ri burchak necha gradusga teng?",
                    "90°",
                    ["45°", "60°", "180°"],
                    "To'g'ri burchak o'lchovi aynan 90 gradusga teng.",
                ),
                _create_q(
                    "Tub son nima?",
                    "Faqat 1 ga va o'ziga bo'linadigan 1 dan katta natural son",
                    ["Har qanday toq son", "Faqat 2 ga bo'linadigan son", "Noldan kichik butun son"],
                    "Tub sonlar faqat ikkita bo'luvchiga ega: 1 va o'zi (masalan, 2, 3, 5, 7, 11...).",
                ),
                _create_q(
                    "Radiusi r bo'lgan doira yuzini hisoblash formulasi qaysi?",
                    "S = π * r²",
                    ["S = 2 * π * r", "S = π * d", "S = 4 * π * r²"],
                    "Doira yuzi radiusi r bo'lsa S = πr² formula orqali topiladi.",
                ),
                _create_q(
                    "Matematikada har qanday sonni nolga bo'lish mumkinmi?",
                    "Mumkin emas (aniqlanmagan)",
                    ["Har doim nol chiqadi", "Bir chiqadi", "Faqat manfiy sonlar uchun mumkin"],
                    "Haqiqiy sonlar maydonida nolga bo'lish amali aniqlanmagan va mumkin emas.",
                ),
                _create_q(
                    "Tomoni 5 sm bo'lgan kvadratning yuzi necha kvadrat santimetrga teng?",
                    "25 sm²",
                    ["20 sm²", "10 sm²", "15 sm²"],
                    "Kvadrat yuzi S = a² = 5² = 25 sm² ga teng.",
                ),
                _create_q(
                    "Ko'pburchakning barcha tomonlari uzunliklari yig'indisi nima deyiladi?",
                    "Perimetr",
                    ["Yuza", "Diagonal", "Median"],
                    "Barcha tomonlar uzunliklari yig'indisi perimetr deb ataladi.",
                ),
            ],
            "medium": [
                _create_q(
                    "To'g'ri burchakli uchburchakda gipotenuza kvadratining katetlar kvadratlari yig'indisiga tengligi qaysi teorema?",
                    "Pifagor teoremasi",
                    ["Fales teoremasi", "Viyet teoremasi", "Kosinuslar teoremasi"],
                    "Pifagor teoremasi: to'g'ri burchakli uchburchakda c² = a² + b².",
                ),
                _create_q(
                    "Kvadrat tenglamaning (ax² + bx + c = 0) diskriminanti qaysi formula bilan hisoblanadi?",
                    "D = b² - 4ac",
                    ["D = b² + 4ac", "D = 2b - 4ac", "D = b² - 2ac"],
                    "Kvadrat tenglama diskriminanti formulasi: D = b² - 4ac.",
                ),
                _create_q(
                    "Arifmetik progressiyaning n-hadi qaysi formula bilan topiladi?",
                    "a_n = a_1 + (n - 1) * d",
                    ["a_n = a_1 * q^(n-1)", "a_n = a_1 + n * d", "a_n = (a_1 + a_n) / 2"],
                    "Arifmetik progressiya n-hadi formulasi: a_n = a_1 + (n - 1)d.",
                ),
                _create_q(
                    "Trigonometriyaning asosiy ayniyati qaysi?",
                    "sin²α + cos²α = 1",
                    ["sin²α - cos²α = 1", "tgα * ctgα = 0", "sinα + cosα = 1"],
                    "Barcha burchaklar uchun asosiy trigonometrik ayniyat: sin²α + cos²α = 1.",
                ),
                _create_q(
                    "Logarifmlarning ko'paytma xossasi qanday ifodalanadi?",
                    "log_a(x * y) = log_a(x) + log_a(y)",
                    ["log_a(x * y) = log_a(x) * log_a(y)", "log_a(x * y) = log_a(x) - log_a(y)", "log_a(x / y) = log_a(x) + log_a(y)"],
                    "Ko'paytmaning logarifmi ko'paytuvchilar logarifmlarining yig'indisiga teng.",
                ),
                _create_q(
                    "Keltirilgan kvadrat tenglamada (x² + px + q = 0) ildizlar yig'indisi nimaga teng (Viyet teoremasi)?",
                    "-p ga",
                    ["p ga", "q ga", "-q ga"],
                    "Viyet teoremasiga binoan keltirilgan kvadrat tenglama ildizlar yig'indisi x1 + x2 = -p ga teng.",
                ),
            ],
            "hard": [
                _create_q(
                    "0/0 yoki ∞/∞ ko'rinishidagi noaniqliklarni ochish uchun hosiladan foydalaniladigan qoida qaysi?",
                    "L'Opital (L'Hôpital) qoidasi",
                    ["Kramer qoidasi", "Rolle teoremasi", "Koshy teoremasi"],
                    "L'Opital qoidasiga ko'ra f(x)/g(x) ning limiti f'(x)/g'(x) ning limitiga teng (noaniqliklarda).",
                ),
                _create_q(
                    "Aniqli integralning geometrik ma'nosi nimani anglatadi?",
                    "Egri chiziqli trapetsiyaning yuzini",
                    ["Funksiya grafigiga o'tkazilgan urinmaning burchak koeffitsiyentini", "Funksiyaning ikkinchi hosilasini", "Uchburchak gipotenuzasini"],
                    "a dan b gacha bo'lgan aniqli integral f(x) funksiya ostidagi soha yuzini (egri chiziqli trapetsiya) ifodalaydi.",
                ),
                _create_q(
                    "Eyler formulasi kompleks sonlarda qaysi ko'rinishda bo'ladi?",
                    "e^(iθ) = cos(θ) + i * sin(θ)",
                    ["e^(iθ) = sin(θ) + i * cos(θ)", "e^(iθ) = cos(θ) - sin(θ)", "e^(θ) = i * (cosθ + sinθ)"],
                    "Eyler formulasi kompleks eksponenta va trigonometrik funksiyalarni bog'laydi: e^(iθ) = cosθ + i*sinθ.",
                ),
                _create_q(
                    "Kombinatorikada n elementdan k tadan takrorlanmas guruhlash (kombinatsiya) formulasi qaysi?",
                    "C_n^k = n! / (k! * (n - k)!)",
                    ["A_n^k = n! / (n - k)!", "P_n = n!", "C_n^k = n! / k!"],
                    "Kombinatsiyalar soni formulasi: C_n^k = n! / (k! * (n - k)!).",
                ),
                _create_q(
                    "Agar matritsaning ikkita satri o'zaro teng yoki mutanosib bo'lsa, uning determinanti nimaga teng bo'ladi?",
                    "0 ga",
                    ["1 ga", "-1 ga", "Cheksizlikka"],
                    "Chiziqli algebrada ikkita satri chiziqli bog'langan matritsa determinanti har doim nolga teng bo'ladi.",
                ),
                _create_q(
                    "Ehtimollar nazariyasida yangi ma'lumotlar olingandan keyin gipoteza ehtimolini qayta hisoblash formulasi qaysi?",
                    "Bayes formulasi",
                    ["Bernulli formulasi", "Puasson taqsimoti", "Chebishev tengsizligi"],
                    "Bayes teoremasi aposterior ehtimolliklarni aprior ehtimolliklar va shartli ehtimolliklar orqali qayta baholash imkonini beradi.",
                ),
            ],
        },
        "general": {
            "easy": [
                _create_q(
                    "Quyosh sistemasidagi eng katta va eng massiv sayyora qaysi?",
                    "Yupiter",
                    ["Saturn", "Mars", "Neptun"],
                    "Yupiter Quyosh sistemasidagi eng ulkan gaz giganti sayyorasidir.",
                ),
                _create_q(
                    "O'simliklarda quyosh nuri yordamida organik modda va kislorod hosil bo'lish jarayoni nima deb ataladi?",
                    "Fotosintez",
                    ["Diffuziya", "Fermentatsiya", "Transpiratsiya"],
                    "Xlorofill ishtirokida quyosh nuri energiyasidan foydalanib oziq ishlab chiqarish jarayoni fotosintez deyiladi.",
                ),
                _create_q(
                    "Inson tanasidagi eng katta ichki a'zo va asosiy biokimyoviy filtr qaysi?",
                    "Jigar",
                    ["Yurak", "O'pka", "Oshqozon"],
                    "Jigar inson organizmidagi eng yirik va 500 dan ortiq funksiyani bajaruvchi ichki a'zodir.",
                ),
                _create_q(
                    "Yer yuzasining taxminan qancha qismini suv (dunyo okeani) egallaydi?",
                    "Taxminan 71%",
                    ["Taxminan 50%", "Taxminan 85%", "Taxminan 60%"],
                    "Sayyoramiz yuzasining taxminan 71 foizi suv havzalari va okeanlar bilan qoplangan.",
                ),
                _create_q(
                    "Dunyo bo'yicha dengiz sathidan eng baland cho'qqi qaysi?",
                    "Everest (Jomolungma)",
                    ["K2 (Chogori)", "Elbrus", "Kilimanjaro"],
                    "Everest cho'qqisi balandligi 8848 metr bo'lib, dunyoning eng baland nuqtasidir.",
                ),
                _create_q(
                    "Yer atmosferasida eng ko'p ulushni egallagan gaz qaysi?",
                    "Azot (taxminan 78%)",
                    ["Kislorod (taxminan 21%)", "Karbonat angidrid", "Argon"],
                    "Atmosfera havosining 78% ga yaqini azot (N2) gazidan iborat.",
                ),
            ],
            "medium": [
                _create_q(
                    "Tirik organizmlar irsiy axborotini saqlovchi DNK molekulasi qanday fazoviy shaklga ega?",
                    "Qo'shaloq spiral (Double helix)",
                    ["Bir qatlamli halqa", "Tekis panjara", "Uch o'lchamli kub"],
                    "1953-yilda Uotson va Krik tomonidan aniqlanganidek, DNK qo'shaloq spiral shaklida tuzilgan.",
                ),
                _create_q(
                    "Biologiyada hujayraning 'energiya stansiyasi' deb qaysi organoid ataladi?",
                    "Mitoxondriya",
                    ["Ribosoma", "Lizosoma", "Golji majmuasi"],
                    "Mitoxondriya ATF sintez qilib, hujayrani zarur biologik energiya bilan ta'minlaydi.",
                ),
                _create_q(
                    "Yer po'stidagi litosfera plitalarining siljishi va to'qnashuvi natijasida nima hosil bo'ladi?",
                    "Zilzilalar va tog' tizmalari",
                    ["Tsunami to'lqinlarining kamayishi", "Atmosfera qatlamining yo'qolishi", "Okean suvining bug'lanishi"],
                    "Tektonik plitalar harakati tog'lar paydo bo'lishi (orogenez) va kuchli seysmik faollikka sabab bo'ladi.",
                ),
                _create_q(
                    "Ozon qatlami (O₃) Yerdagi hayotni quyoshning qaysi zararli nurlaridan himoya qiladi?",
                    "Ultrabinafsha (UV) nurlardan",
                    ["Infraqizil nurlardan", "Rentgen nurlaridan", "Mikroto'lqinli nurlardan"],
                    "Stratosferadagi ozon qatlami zararli ultrabinafsha nurlanishning asosiy qismini yutadi.",
                ),
                _create_q(
                    "Dunyo okeanidagi eng chuqur joy qaysi botiq hisoblanadi?",
                    "Mariana botig'i (taxminan 11 000 m)",
                    ["Yava botig'i", "Puerto-Riko botig'i", "Filippin botig'i"],
                    "Tinch okeanidagi Mariana botig'i chuqurligi qariyb 11 kilometrga yetadi.",
                ),
                _create_q(
                    "Qon guruhlari bo'yicha AB0 sistemasida universal donor deb qaysi guruh hisoblanadi?",
                    "I (0) guruh Rh-",
                    ["IV (AB) guruh", "II (A) guruh", "III (B) guruh"],
                    "I (0) manfiy qon guruhida agglyutinogenlar yo'qligi sababli favqulodda universal donor hisoblanadi.",
                ),
            ],
            "hard": [
                _create_q(
                    "Kvant mexanikasida Plank doimiysining (h) fundamental roli nimadan iborat?",
                    "Kvantlangan energiya va to'lqin chastotasini bog'lash (E = hν)",
                    [
                        "Yorug'likning to'liq sinishini ta'minlash",
                        "Klassik mexanikadagi tezlanishni nolga tenglashtirish",
                        "Elektronning massasini o'zgarmas saqlash",
                    ],
                    "Plank doimiysi mikrodunyo jarayonlarining diskret (kvant) tabiatini belgilovchi universal fizik kattalikdir.",
                ),
                _create_q(
                    "Molekulyar biologiyada CRISPR-Cas9 texnologiyasining ishlash mexanizmi nima?",
                    "Yo'naltiruvchi RNK yordamida DNKning ma'lum qismini aniqlab, nishon kesim hosil qilish",
                    [
                        "Bakteriyalarning barchasini yo'q qiluvchi antibiotik ishlab chiqarish",
                        "Hujayra yadrosini to'liq ko'chirib o'tkazish",
                        "Oqsillarni sintez qiluvchi ribosomalar hosil qilish",
                    ],
                    "CRISPR-Cas9 tizimi gid-RNK orqali DNKning kerakli gen ketma-ketligini topib, aniq tahrirlash imkonini beradi.",
                ),
                _create_q(
                    "Termodinamikaning ikkinchi qonuniga ko'ra yopiq (izolyatsiyalangan) tizimda qaysi fizik kattalik kamaymaydi?",
                    "Entropiya (tartibsizlik o'lchovi)",
                    ["Temperatura", "Bosim", "Ichki energiya"],
                    "Termodinamikaning 2-qonuniga binoan o'z-o'zidan sodir bo'ladigan jarayonlarda izolyatsiyalangan tizimning entropiyasi faqat ortadi yoki o'zgarmaydi.",
                ),
                _create_q(
                    "Neyronlar orasidagi sinaps orqali nerv impulsi qaysi moddalar vositasida uzatiladi?",
                    "Neyromediatorlar (masalan, atsetilxolin, dofamin)",
                    ["Faqat qon plazmasi", "Faqat temir ionlari", "Gemoglobin oqsillari"],
                    "Kimyoviy sinapslarda elektr signali neyromediatorlar (kimyoviy vositachilar) orqali keyingi neyronga uzatiladi.",
                ),
                _create_q(
                    "Epigenetika fani nimani o'rganadi?",
                    "DNK nukleotid ketma-ketligi o'zgarmagan holda genlar faolligi va ifodalanishining (ekspressiyasining) o'zgarishini",
                    [
                        "Yangi turdagi organizmlarni klonlashni",
                        "Faqat qazilma qoldiqlarning genetik yoshini",
                        "Viruslarning sun'iy sintezini",
                    ],
                    "Epigenetika DNKning birlamchi kodi o'zgarmagan holda metillanish va giston modifikatsiyalari orqali genlar yoqilishi/o'chirilishini o'rganadi.",
                ),
                _create_q(
                    "Koinotning 'Katta portlash' (Big Bang) modeli orqali paydo bo'lganini isbotlovchi asosiy qoldiq nurlanish nima deyiladi?",
                    "Relikt (kosmik mikroto'lqinli fon) nurlanishi",
                    ["Quyosh shamoli nurlanishi", "Rentgen pulsarlari", "Lazer interferensiyasi"],
                    "1965-yilda Penzias va Vilson tomonidan kashf etilgan relikt nurlanish (2.7 K) Katta portlashning asosiy dalilidir.",
                ),
            ],
        },
    },
    "en": {
        "physics": {
            "easy": [
                _create_q(
                    "What is the SI unit of pressure?",
                    "Pascal (Pa)",
                    ["Newton (N)", "Joule (J)", "Watt (W)"],
                    "The SI unit of pressure is the Pascal (Pa), equivalent to 1 N/m².",
                ),
                _create_q(
                    "What is the formula for calculating speed in uniform motion?",
                    "v = d / t",
                    ["v = d * t", "v = a * t²", "v = m / s"],
                    "Speed is calculated by dividing distance traveled by time taken: v = d / t.",
                ),
                _create_q(
                    "What is the approximate speed of light in a vacuum?",
                    "300,000 km/s",
                    ["150,000 km/s", "30,000 km/s", "1,000,000 km/s"],
                    "Light travels at approximately 300,000 km/s (3×10⁸ m/s) in a vacuum.",
                ),
                _create_q(
                    "At standard atmospheric pressure, at what temperature does pure water boil?",
                    "100°C",
                    ["80°C", "90°C", "120°C"],
                    "Pure water boils at 100°C under 1 atmosphere of pressure.",
                ),
                _create_q(
                    "Which medium cannot transmit sound waves?",
                    "Vacuum",
                    ["Water", "Steel", "Air"],
                    "Sound is a mechanical wave requiring a physical medium, so it cannot propagate through a vacuum.",
                ),
            ],
            "medium": [
                _create_q(
                    "According to Pascal's principle, how is pressure applied to an enclosed fluid transmitted?",
                    "Equally in all directions without diminution",
                    [
                        "Only toward the bottom of the container",
                        "Decreases with increasing depth",
                        "Only perpendicular to side walls",
                    ],
                    "Pascal's law states that pressure exerted on a confined fluid is transmitted undiminished in all directions.",
                ),
                _create_q(
                    "What factors determine the magnitude of Archimedes' buoyant force?",
                    "Fluid density and submerged volume of the body",
                    [
                        "Total mass of the object only",
                        "Shape of the container and water mass",
                        "Chemical composition of the body",
                    ],
                    "Archimedes' buoyant force is F_b = ρ * g * V, directly proportional to fluid density and submerged volume.",
                ),
                _create_q(
                    "What is the mathematical formulation of Newton's Second Law of Motion?",
                    "F = m * a",
                    ["E = m * c²", "P = F / A", "W = F * d"],
                    "Newton's second law states that net force equals mass multiplied by acceleration (F = ma).",
                ),
                _create_q(
                    "What is Ohm's law for an electric circuit component?",
                    "I = V / R",
                    ["V = I / R", "R = I * V", "P = I² / R"],
                    "Ohm's law states that current is directly proportional to voltage and inversely proportional to resistance.",
                ),
            ],
            "hard": [
                _create_q(
                    "In quantum mechanics, what does the time-independent Schrödinger equation describe?",
                    "The spatial wave function and stationary energy states of a quantum particle",
                    [
                        "The exact classical trajectory of a particle",
                        "The geometric refraction index of photons",
                        "The gravitational redshift of distant galaxies",
                    ],
                    "The Schrödinger equation describes the wave function and corresponding energy eigenvalues of quantum systems.",
                ),
                _create_q(
                    "What is the maximum theoretical efficiency of a Carnot heat engine?",
                    "η = (T_hot - T_cold) / T_hot",
                    ["η = (T_cold - T_hot) / T_cold", "η = T_hot / T_cold", "η = 1 - (T_hot / T_cold)"],
                    "The Carnot efficiency depends solely on the absolute temperatures of the heat source and sink: η = (Th - Tc) / Th.",
                ),
                _create_q(
                    "What does the Stefan-Boltzmann law state regarding blackbody radiant energy?",
                    "Total radiant energy is proportional to the fourth power of absolute temperature (T⁴)",
                    ["Proportional to T²", "Proportional to T", "Proportional to T³"],
                    "The Stefan-Boltzmann law states that radiant power per unit area of a blackbody is proportional to T⁴.",
                ),
            ],
        },
        "programming": {
            "easy": [
                _create_q(
                    "Which function is used to output data to the console in Python?",
                    "print()",
                    ["echo()", "console.log()", "write()"],
                    "The print() function is Python's standard output mechanism.",
                ),
                _create_q(
                    "Which keyword is used to define a function in Python?",
                    "def",
                    ["function", "func", "define"],
                    "The 'def' keyword is used to declare user-defined functions.",
                ),
                _create_q(
                    "Which of the following built-in types in Python is immutable?",
                    "tuple",
                    ["list", "dict", "set"],
                    "Tuples cannot be modified after instantiation.",
                ),
                _create_q(
                    "Which method appends an item to the end of a list in Python?",
                    "append()",
                    ["add()", "push()", "insert_last()"],
                    "The append() method adds an element to the end of an existing list.",
                ),
            ],
            "medium": [
                _create_q(
                    "What is the difference between '==' and 'is' operators in Python?",
                    "'==' compares values for equality, whereas 'is' checks object identity (same memory address)",
                    [
                        "'==' is only for numbers, 'is' is only for strings",
                        "They are completely identical and interchangeable",
                        "'is' compares types while '==' compares values",
                    ],
                    "'==' checks if values are equal, while 'is' checks whether two variables refer to the identical object in memory.",
                ),
                _create_q(
                    "Which dictionary method returns both keys and values as pairs?",
                    "items()",
                    ["keys()", "values()", "pairs()"],
                    "dict.items() returns an iterable of (key, value) tuples.",
                ),
                _create_q(
                    "How are exceptions handled safely in Python?",
                    "try ... except blocks",
                    ["try ... catch blocks", "do ... while blocks", "guard ... handle blocks"],
                    "Python uses try and except statements to catch and handle runtime exceptions.",
                ),
            ],
            "hard": [
                _create_q(
                    "What is the primary role of the Global Interpreter Lock (GIL) in CPython?",
                    "It ensures that only one native thread executes Python bytecode at a time",
                    [
                        "It prevents syntax errors during interpretation",
                        "It writes memory snapshots to disk automatically",
                        "It optimizes recursive algorithms into iteration",
                    ],
                    "The GIL protects CPython memory management and reference counting by restricting bytecode execution to one thread at a time.",
                ),
                _create_q(
                    "What is the role of a metaclass in Python?",
                    "A blueprint that defines how classes themselves are constructed and behaved",
                    [
                        "A database ORM adapter for SQL queries",
                        "A compiler flag for faster math operations",
                        "A base exception class for system exits",
                    ],
                    "A metaclass is the class of a class; in Python, the default metaclass is 'type'.",
                ),
                _create_q(
                    "What is the difference between `__new__` and `__init__` in Python class instantiation?",
                    "`__new__` creates and returns the instance, while `__init__` initializes the created instance",
                    [
                        "`__init__` creates memory space, `__new__` destroys it",
                        "`__new__` is only for static methods, `__init__` is for classes",
                        "They perform the exact same task with no differences",
                    ],
                    "`__new__` is the actual constructor method that returns a new instance, whereas `__init__` initializes its attributes.",
                ),
            ],
        },
        "mathematics": {
            "easy": [
                _create_q(
                    "What is the measure of a right angle in degrees?",
                    "90°",
                    ["45°", "60°", "180°"],
                    "A right angle measures exactly 90 degrees.",
                ),
                _create_q(
                    "What is a prime number?",
                    "A natural number greater than 1 having only two factors: 1 and itself",
                    ["Any odd number", "A number divisible by 2", "Any negative integer"],
                    "Prime numbers have exactly two distinct natural number divisors: 1 and themselves.",
                ),
                _create_q(
                    "What is the formula for the area of a circle with radius r?",
                    "A = π * r²",
                    ["A = 2 * π * r", "A = π * d", "A = 4 * π * r²"],
                    "The area of a circle of radius r is given by A = πr².",
                ),
            ],
            "medium": [
                _create_q(
                    "What theorem states that in a right triangle, the square of the hypotenuse equals the sum of squares of the legs?",
                    "Pythagorean theorem",
                    ["Thales theorem", "Vieta's formulas", "Cosine law"],
                    "The Pythagorean theorem states: c² = a² + b².",
                ),
                _create_q(
                    "What is the discriminant formula for a quadratic equation ax² + bx + c = 0?",
                    "D = b² - 4ac",
                    ["D = b² + 4ac", "D = 2b - 4ac", "D = b² - 2ac"],
                    "The discriminant of a quadratic equation is D = b² - 4ac.",
                ),
                _create_q(
                    "What is the fundamental trigonometric identity relating sine and cosine?",
                    "sin²θ + cos²θ = 1",
                    ["sin²θ - cos²θ = 1", "tanθ * cotθ = 0", "sinθ + cosθ = 1"],
                    "For all angles, sin²θ + cos²θ = 1.",
                ),
            ],
            "hard": [
                _create_q(
                    "Which rule uses derivatives to evaluate indeterminate limits of the form 0/0 or ∞/∞?",
                    "L'Hôpital's rule",
                    ["Cramer's rule", "Rolle's theorem", "Cauchy's integral formula"],
                    "L'Hôpital's rule states that lim f(x)/g(x) = lim f'(x)/g'(x) under 0/0 or ∞/∞ conditions.",
                ),
                _create_q(
                    "What is Euler's formula connecting complex exponentiation and trigonometry?",
                    "e^(iθ) = cos(θ) + i * sin(θ)",
                    ["e^(iθ) = sin(θ) + i * cos(θ)", "e^(iθ) = cos(θ) - sin(θ)", "e^(θ) = i * (cosθ + sinθ)"],
                    "Euler's formula establishes the fundamental link between complex numbers and trigonometry: e^(iθ) = cosθ + i*sinθ.",
                ),
            ],
        },
        "general": {
            "easy": [
                _create_q(
                    "What is the largest planet in our Solar System?",
                    "Jupiter",
                    ["Saturn", "Mars", "Neptune"],
                    "Jupiter is the largest and most massive planet in the Solar System.",
                ),
                _create_q(
                    "What process do green plants use to convert sunlight into organic energy?",
                    "Photosynthesis",
                    ["Fermentation", "Transpiration", "Cellular respiration"],
                    "Photosynthesis synthesizes glucose and oxygen using solar energy and chlorophyll.",
                ),
            ],
            "medium": [
                _create_q(
                    "Which organelle is often termed the 'powerhouse of the cell'?",
                    "Mitochondria",
                    ["Ribosome", "Lysosome", "Golgi apparatus"],
                    "Mitochondria generate the majority of cellular chemical energy in the form of ATP.",
                ),
                _create_q(
                    "Which blood type is considered the universal red cell donor in the ABO/Rh system?",
                    "O negative (O-)",
                    ["AB positive (AB+)", "A positive (A+)", "B negative (B-)"],
                    "O negative red blood cells lack A, B, and Rh surface antigens, minimizing transfusion reactions.",
                ),
            ],
            "hard": [
                _create_q(
                    "What fundamental property of an isolated system never decreases according to the Second Law of Thermodynamics?",
                    "Entropy",
                    ["Internal energy", "Temperature", "Pressure"],
                    "The second law states that the total entropy of an isolated system always increases or remains constant in reversible processes.",
                ),
                _create_q(
                    "What is the mechanism of the CRISPR-Cas9 genome editing tool?",
                    "A guide RNA directs Cas9 endonuclease to introduce targeted double-strand breaks in DNA",
                    [
                        "Direct methylation of ribosomal subunits",
                        "Broad-spectrum chemical mutagenesis",
                        "Whole nucleus transplantation",
                    ],
                    "CRISPR-Cas9 utilizes a single guide RNA sequence to specifically bind and cleave targeted DNA strands.",
                ),
            ],
        },
    },
    "ru": {
        "physics": {
            "easy": [
                _create_q(
                    "Какова основная единица измерения давления в Международной системе единиц (СИ)?",
                    "Паскаль (Па)",
                    ["Ньютон (Н)", "Джоуль (Дж)", "Ватт (Вт)"],
                    "Единицей давления в СИ является Паскаль (Па), равный 1 Н/м².",
                ),
                _create_q(
                    "По какой формуле определяется скорость при прямолинейном равномерном движении?",
                    "v = s / t",
                    ["v = s * t", "v = a * t²", "v = m / s"],
                    "Скорость равна отношению пройденного пути ко времени: v = s / t.",
                ),
                _create_q(
                    "В какой среде звуковые волны не могут распространяться?",
                    "В вакууме",
                    ["В воде", "В воздухе", "В стали"],
                    "Звук является механической волной и требует материальной среды для передачи колебаний.",
                ),
            ],
            "medium": [
                _create_q(
                    "Согласно закону Паскаля, как передается давление, производимое на жидкость или газ?",
                    "Во все стороны одинаково без изменений",
                    ["Только ко дну сосуда", "Уменьшается с глубиной", "Только перпендикулярно стенкам"],
                    "Закон Паскаля: давление на жидкость или газ передается в любую точку без изменений во всех направлениях.",
                ),
                _create_q(
                    "От каких величин зависит выталкивающая сила Архимеда?",
                    "От плотности жидкости и объема погруженной части тела",
                    ["Только от массы тела", "От формы сосуда", "От материала тела"],
                    "Сила Архимеда F = ρ * g * V прямо пропорциональна плотности жидкости и погруженному объему.",
                ),
                _create_q(
                    "Какова математическая запись второго закона Ньютона?",
                    "F = m * a",
                    ["E = m * c²", "P = F / S", "A = F * s"],
                    "Второй закон Ньютона: сила равна произведению массы на ускорение (F = ma).",
                ),
            ],
            "hard": [
                _create_q(
                    "Что описывает стационарное уравнение Шрёдингера в квантовой механике?",
                    "Пространственную волновую функцию и уровни энергии квантовой системы",
                    ["Точную траекторию классической частицы", "Скорость свободного падения", "Гравитационный коллапс"],
                    "Уравнение Шрёдингера описывает состояние и спектр энергии микрочастиц через волновую функцию.",
                ),
                _create_q(
                    "Каков максимальный теоретический КПД теплового двигателя в цикле Карно?",
                    "η = (T1 - T2) / T1",
                    ["η = (T2 - T1) / T2", "η = T1 / T2", "η = 1 - (T1 / T2)"],
                    "КПД идеального цикла Карно определяется температурами нагревателя (T1) и холодильника (T2).",
                ),
            ],
        },
        "programming": {
            "easy": [
                _create_q(
                    "Какая функция используется для вывода информации в консоль в Python?",
                    "print()",
                    ["echo()", "console.log()", "write()"],
                    "Стандартная функция print() выводит переданные объекты в консоль.",
                ),
                _create_q(
                    "С помощью какого ключевого слова объявляется функция в Python?",
                    "def",
                    ["function", "func", "define"],
                    "Функции в Python объявляются с помощью ключевого слова 'def'.",
                ),
                _create_q(
                    "Какой из перечисленных типов данных в Python является неизменяемым (immutable)?",
                    "tuple (кортеж)",
                    ["list (список)", "dict (словарь)", "set (множество)"],
                    "Кортежи не могут быть модифицированы после создания.",
                ),
            ],
            "medium": [
                _create_q(
                    "В чем разница между операторами '==' и 'is' в Python?",
                    "'==' сравнивает значения, а 'is' проверяет идентичность объектов в памяти (id)",
                    ["Они полностью идентичны", "'is' только для чисел, '==' для строк", "'is' сравнивает типы"],
                    "'==' проверяет равенство значений, а 'is' указывает на один и тот же участок памяти.",
                ),
                _create_q(
                    "Какой метод словаря возвращает одновременно ключи и значения в виде пар?",
                    "items()",
                    ["keys()", "values()", "pairs()"],
                    "Метод dict.items() возвращает итератор кортежей вида (ключ, значение).",
                ),
            ],
            "hard": [
                _create_q(
                    "Какова основная функция Global Interpreter Lock (GIL) в CPython?",
                    "Обеспечивать выполнение байт-кода Python только одним потоком единовременно",
                    ["Оптимизировать код в машинные инструкции", "Автоматически очищать диск", "Блокировать сетевые пакеты"],
                    "GIL защищает внутреннее управление памятью CPython, запрещая параллельное выполнение байт-кода в разных потоках.",
                ),
                _create_q(
                    "В чем различие между `__new__` и `__init__` в Python?",
                    "`__new__` создает и возвращает экземпляр класса, а `__init__` инициализирует его атрибуты",
                    ["`__init__` создает память, а `__new__` удаляет ее", "Различий нет, это алиасы", "`__new__` вызывается только при наследовании"],
                    "`__new__` является фактическим конструктором, а `__init__` инициализирует уже созданный объект.",
                ),
            ],
        },
        "mathematics": {
            "easy": [
                _create_q(
                    "Чему равна градусная мера прямого угла?",
                    "90°",
                    ["45°", "60°", "180°"],
                    "Прямой угол равен ровно 90 градусам.",
                ),
                _create_q(
                    "Что такое простое число?",
                    "Натуральное число больше 1, имеющее ровно два делителя: 1 и само себя",
                    ["Любое нечетное число", "Число, делящееся на 2", "Любое отрицательное число"],
                    "Простые числа делятся только на единицу и на самих себя (2, 3, 5, 7, 11...).",
                ),
            ],
            "medium": [
                _create_q(
                    "По какой формуле вычисляется дискриминант квадратного уравнения ax² + bx + c = 0?",
                    "D = b² - 4ac",
                    ["D = b² + 4ac", "D = 2b - 4ac", "D = b² - 2ac"],
                    "Дискриминант квадратного уравнения равен: D = b² - 4ac.",
                ),
                _create_q(
                    "Какая теорема связывает катеты и гипотенузу прямоугольного треугольника?",
                    "Теорема Пифагора",
                    ["Теорема Фалеса", "Теорема Виета", "Теорема косинусов"],
                    "Теорема Пифагора: c² = a² + b².",
                ),
            ],
            "hard": [
                _create_q(
                    "Какое правило используется для раскрытия неопределенностей вида 0/0 и ∞/∞ с помощью производных?",
                    "Правило Лопиталя",
                    ["Правило Крамера", "Теорема Ролля", "Формула Коши"],
                    "Правило Лопиталя: предел отношения функций равен пределу отношения их производных при неопределенностях.",
                ),
                _create_q(
                    "Формула Эйлера в комплексном анализе связывает тригонометрию и комплексную экспоненту как:",
                    "e^(iθ) = cos(θ) + i * sin(θ)",
                    ["e^(iθ) = sin(θ) + i * cos(θ)", "e^(iθ) = cos(θ) - sin(θ)", "e^(θ) = i * (cosθ + sinθ)"],
                    "Формула Эйлера: e^(iθ) = cosθ + i*sinθ.",
                ),
            ],
        },
        "general": {
            "easy": [
                _create_q(
                    "Какая планета является крупнейшей в Солнечной системе?",
                    "Юпитер",
                    ["Сатурн", "Марс", "Нептун"],
                    "Юпитер — самая массивная и крупная планета Солнечной системы.",
                ),
            ],
            "medium": [
                _create_q(
                    "Какой клеточный органоид называют 'энергетической станцией клетки'?",
                    "Митохондрия",
                    ["Рибосома", "Лизосома", "Аппарат Гольджи"],
                    "Митохондрии синтезируют АТФ — основной источник химической энергии клетки.",
                ),
            ],
            "hard": [
                _create_q(
                    "Какая физическая величина изолированной системы не убывает согласно второму началу термодинамики?",
                    "Энтропия",
                    ["Температура", "Давление", "Внутренняя энергия"],
                    "Второе начало термодинамики утверждает, что энтропия изолированной системы не может уменьшаться.",
                ),
            ],
        },
    },
}


def _match_category(subject: str) -> str:
    subj_lower = subject.lower()
    if any(k in subj_lower for k in [
        "fizika", "physic", "физик", "paskal", "pascal", "arximed", "archimed",
        "nyuton", "newton", "bosim", "давлен", "optik", "mexanik", "termodin",
    ]):
        return "physics"
    if any(k in subj_lower for k in [
        "python", "dastur", "program", "программ", "kod", "code", "dev",
        "algoritm", "java", "c++", "frontend", "backend", "web",
    ]):
        return "programming"
    if any(k in subj_lower for k in [
        "matem", "math", "алгебр", "geometr", "hisob", "son", "tenglama",
        "uchburchak", "integral", "arifmetik",
    ]):
        return "mathematics"
    return "general"


def _synthesize_dynamic_question(
    subject: str,
    difficulty: str,
    index: int,
    language: str,
) -> dict[str, Any]:
    """Synthesize dynamic, difficulty-aware academic questions with varied templates."""
    lang_key = language if language in ("uz", "en", "ru") else "uz"

    templates = {
        "uz": {
            "easy": [
                (
                    f"{subject} fanida eng asosiy va boshlang'ich tushuncha qaysi?",
                    f"{subject}ning fundamental ta'rifi va asosiy qonuniyatlari",
                    [
                        f"{subject} faqat gipotezalardan iborat bo'lib, isbotlanmagan",
                        f"{subject}da aniq qoidalar mavjud emas",
                        f"{subject} o'rganish amaliyotda foydasiz hisoblanadi",
                    ],
                    f"{subject} kursi doirasida dastlab uning fundamental ta'rif va qoidalari o'rganiladi.",
                ),
                (
                    f"{subject} sohasida yangi o'rganuvchilar uchun eng muhim boshlang'ich tamoyil nima?",
                    "Baza terminlari va asosiy prinsiplarni to'g'ri tushunish",
                    [
                        "Murakkab matematik hisoblashlarni darhol yodlash",
                        "Nazariyani e'tiborsiz qoldirib faqat taxmin qilish",
                        "Asosiy formulalarni qo'llamaslik",
                    ],
                    f"Har qanday yo'nalish kabi {subject}da ham boshlang'ich tushunchalarni mustahkamlash hal qiluvchi ahamiyatga ega.",
                ),
                (
                    f"{subject} bo'yicha eng sodda qoida yoki qonuniyat qanday tavsiflanadi?",
                    "Elementar shartlar va to'g'ridan-to'g'ri mantiqiy bog'liqlik",
                    [
                        "Ko'p o'lchamli differensial noaniqliklar",
                        "Tasodifiy o'zgaruvchilarning betartib harakati",
                        "Isbotsiz empirik taxminlar yig'indisi",
                    ],
                    f"Boshlang'ich darajada {subject} qoidalari to'g'ridan-to'g'ri mantiqiy bog'liqlikka asoslanadi.",
                ),
            ],
            "medium": [
                (
                    f"{subject} sohasida amaliy masalalarni yechishda qaysi uslub eng samarali hisoblanadi?",
                    "Nazariy qoidalarni amaliy vaziyatlar va modellarga bosqichma-bosqich tatbiq etish",
                    [
                        "Faqat tayyor javoblarni tahlilsiz ko'chirib olish",
                        "O'lchov va birliklarni inobatga olmaslik",
                        "Tizimli tahlil o'rniga faqat intuitiv taxmin qilish",
                    ],
                    f"{subject} bo'yicha o'rtacha murakkablikdagi masalalar qonuniyatlarni amaliy vaziyatlarga tatbiq qilishni talab etadi.",
                ),
                (
                    f"{subject} yo'nalishidagi o'zaro bog'liq omillar tahlilida nima muhim?",
                    "Sabab-oqibat aloqadorligi va standart formulalarni to'g'ri bog'lay olish",
                    [
                        "Faqat bitta omilni hisobga olib, qolganlarini rad etish",
                        "Har qanday empirik natijani istisno deb e'lon qilish",
                        "Qonuniyatlarning o'zgaruvchanligini inkor etish",
                    ],
                    f"{subject} tahlilida sabab-oqibat zanjirini to'g'ri aniqlash o'rta darajadagi eng muhim ko'nikmadir.",
                ),
            ],
            "hard": [
                (
                    f"{subject} sohasida chuqur nazariy va murakkab masalalar qaysi mezon orqali hal qilinadi?",
                    "Ko'p bosqichli sintez, nozik istisnolar (edge cases) va tizimli tahlil orqali",
                    [
                        "Faqat sodda ta'riflarni takrorlash orqali",
                        "Barcha murakkab o'zgaruvchilarni e'tibordan chetda qoldirish orqali",
                        "Standart chiziqli mantiqqa qat'iy cheklanib qolish orqali",
                    ],
                    f"Murakkab (hard) darajada {subject} ko'p bosqichli tahlil, chekka holatlar va ilg'or nazariyalarni sintez qilishni talab etadi.",
                ),
                (
                    f"{subject} fanining ilg'or tushunchalari va chegaraviy holatlarida qaysi omil muhim o'rin tutadi?",
                    "Tizimning ichki dinamikasi va nostandart istisnolarning o'zaro murakkab ta'siri",
                    [
                        "Hech qanday nozik istisno yoki chegaraviy holat mavjud emas",
                        "Faqat boshlang'ich maktab darajasidagi ta'riflar yetarli bo'ladi",
                        "Barcha qonuniyatlar o'z kuchini butunlay yo'qotadi",
                    ],
                    f"Ilg'or darajadagi {subject} masalalarida chegaraviy shartlar va nostandart istisnolar hal qiluvchi rol o'ynaydi.",
                ),
            ],
        },
        "en": {
            "easy": [
                (
                    f"What is a fundamental introductory concept in {subject}?",
                    f"Core foundational definitions and empirical principles of {subject}",
                    [
                        f"{subject} is completely speculative without rules",
                        f"{subject} has no real-world applicability",
                        f"{subject} excludes all forms of systematic study",
                    ],
                    f"Foundational concepts in {subject} introduce key terms and direct principles.",
                ),
            ],
            "medium": [
                (
                    f"In practical applications of {subject}, which approach yields optimal results?",
                    "Applying established theorems and cause-and-effect reasoning to concrete scenarios",
                    [
                        "Ignoring fundamental constraints and parameters",
                        "Relying purely on arbitrary guesses without verification",
                        "Bypassing standard empirical methods",
                    ],
                    f"Intermediate study of {subject} requires connecting theory to practical problems.",
                ),
            ],
            "hard": [
                (
                    f"When analyzing advanced, non-trivial problems in {subject}, what is essential?",
                    "Multi-step synthesis, rigorous boundary condition analysis, and resolving subtle edge cases",
                    [
                        "Relying solely on elementary definitions",
                        "Discarding non-linear variables without justification",
                        "Assuming all systems behave uniformly under extreme conditions",
                    ],
                    f"Advanced problem solving in {subject} demands deep analytical synthesis and edge-case mastery.",
                ),
            ],
        },
        "ru": {
            "easy": [
                (
                    f"Что является фундаментальным базовым понятием в предмете {subject}?",
                    f"Ключевые определения и основные принципы предмета {subject}",
                    [
                        f"{subject} является чисто гипотетическим направлением без правил",
                        f"{subject} не имеет практического применения",
                        f"{subject} не поддается научному анализу",
                    ],
                    f"На базовом уровне в {subject} изучаются ключевые термины и первоосновы.",
                ),
            ],
            "medium": [
                (
                    f"Что является ключевым при решении прикладных задач по направлению {subject}?",
                    "Применение стандартных формул и установление причинно-следственных связей",
                    [
                        "Полное игнорирование граничных условий",
                        "Использование случайных предположений без проверки",
                        "Отказ от систематического анализа",
                    ],
                    f"Средний уровень сложности в {subject} предполагает практическое применение законов.",
                ),
            ],
            "hard": [
                (
                    f"Какой подход необходим для решения сложных и углубленных задач по предмету {subject}?",
                    "Многоэтапный синтез, учет граничных условий и анализ тонких исключений (edge cases)",
                    [
                        "Ограничение исключительно базовыми школьными определениями",
                        "Игнорирование многофакторных нелинейных зависимостей",
                        "Предположение об абсолютной линейности всех процессов",
                    ],
                    f"Продвинутый уровень {subject} требует комплексного системного анализа и нестандартного мышления.",
                ),
            ],
        },
    }

    lang_dict = templates.get(lang_key, templates["uz"])
    diff_dict = lang_dict.get(difficulty, lang_dict["medium"])
    chosen_template = random.choice(diff_dict)

    q_text, correct, distractors, explanation = chosen_template
    if index > 1:
        prefix = f"[{subject} #{index}] "
    else:
        prefix = ""
    return _create_q(f"{prefix}{q_text}", correct, distractors, explanation)


def generate_curated_quiz(
    subject: str,
    difficulty: str = "medium",
    count: int = 5,
    language: str = "uz",
    exclude_questions: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Generate high-quality questions filtered specifically by difficulty with dynamic variation."""
    lang_key = language if language in QUESTIONS_BANK else "uz"
    norm_diff = (difficulty or "medium").lower().strip()
    if norm_diff not in ("easy", "medium", "hard"):
        norm_diff = "medium"

    cat = _match_category(subject)
    exclude_set = {q.strip().lower() for q in (exclude_questions or [])}

    lang_pool = QUESTIONS_BANK.get(lang_key, QUESTIONS_BANK["uz"])
    cat_pool = lang_pool.get(cat, {})
    diff_pool = cat_pool.get(norm_diff, [])

    # Filter out excluded questions
    available = [
        item for item in diff_pool
        if item.get("question", "").strip().lower() not in exclude_set
    ]

    # If pool for specific category is small, augment with general knowledge of the SAME difficulty
    if len(available) < count and cat != "general":
        general_diff_pool = lang_pool.get("general", {}).get(norm_diff, [])
        for gq in general_diff_pool:
            if gq.get("question", "").strip().lower() not in exclude_set and gq not in available:
                available.append(gq)

    # If still small or empty and language is not 'uz', fallback to 'uz' pool with same difficulty
    if len(available) < count and lang_key != "uz":
        uz_pool = QUESTIONS_BANK["uz"].get(cat, {}).get(norm_diff, [])
        for uq in uz_pool:
            if uq.get("question", "").strip().lower() not in exclude_set and uq not in available:
                available.append(uq)

    # Shuffle pool and clone with randomized options
    selected: list[dict[str, Any]] = []
    shuffled_pool = list(available)
    random.shuffle(shuffled_pool)

    for item in shuffled_pool[:count]:
        correct_text = item["options"][item["correct_option"]]
        wrong_texts = [
            text for opt_key, text in item["options"].items() if opt_key != item["correct_option"]
        ]
        q = _create_q(
            question=item["question"],
            correct=correct_text,
            distractors=wrong_texts,
            explanation=item.get("explanation", ""),
        )
        selected.append(q)

    # If count requested is greater than preset catalog, synthesize difficulty-aware questions
    synthetic_idx = 1
    while len(selected) < count:
        syn_q = _synthesize_dynamic_question(
            subject=subject,
            difficulty=norm_diff,
            index=synthetic_idx,
            language=lang_key,
        )
        if syn_q["question"].strip().lower() not in exclude_set:
            selected.append(syn_q)
        synthetic_idx += 1

    return selected
