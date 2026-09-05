"""Curated and dynamic quiz question generator with randomized options.

Supports Uzbek, English, and Russian across various academic subjects and general knowledge.
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


# Catalog organized by subject category and language
QUESTIONS_BANK: dict[str, dict[str, list[dict[str, Any]]]] = {
    "uz": {
        "physics": [
            _create_q(
                "Paskal qonuniga ko'ra, suyuqlik yoki gazga berilgan tashqi bosim qanday tarqaladi?",
                "Barcha yo'nalishlar bo'ylab o'zgarishsiz bir xil tarqaladi",
                [
                    "Faqat idishning pastki qismiga yo'naladi",
                    "Suyuqlik chuqurlashgan sari bosim yo'qoladi",
                    "Faqat idish devorlariga to'g'ri burchak ostida ta'sir qiladi",
                ],
                "Paskal qonuniga binoan, yopiq idishdagi suyuqlik yoki gazga berilgan bosim barcha yo'nalishlarga teng va o'zgarishsiz uzatiladi.",
            ),
            _create_q(
                "Arximed kuchining kattaligi qaysi kattaliklarga bog'liq?",
                "Suyuqlik zichligi va jismning botgan qismi hajmiga",
                [
                    "Faqat jismning umumiy og'irligiga",
                    "Idish shakli va undagi suyuqlik miqdoriga",
                    "Jismning tayyorlangan moddasiga",
                ],
                "F_A = ρ * g * V formulasi bo'yicha Arximed kuchi suyuqlik zichligi va botgan hajmga to'g'ri mutanosib.",
            ),
            _create_q(
                "Nyutonning ikkinchi qonunining matematik ifodasi qaysi?",
                "F = m * a",
                ["E = m * c²", "P = F / S", "A = F * s"],
                "Nyutonning II qonuniga ko'ra jismga ta'sir etuvchi natijaviy kuch uning massasi va olgan tezlanishi ko'paytmasiga teng.",
            ),
            _create_q(
                "Bosimning Xalqaro birliklar sistemasidagi (SI) asosiy birligi nima?",
                "Paskal (Pa)",
                ["Nyuton (N)", "Joul (J)", "Vatt (W)"],
                "Bosim birligi Paskal (Pa) bo'lib, 1 Pa = 1 N/m² ga teng.",
            ),
            _create_q(
                "Gidravlik press va gidravlik tormozlar qaysi qonun asosida ishlaydi?",
                "Paskal qonuni",
                ["Arximed qonuni", "Om qonuni", "Boyle-Mariotte qonuni"],
                "Gidravlik mashinalar suyuqlik orqali bosimning barcha yo'nalishda bir xil uzatilishiga (Paskal qonuniga) asoslangan.",
            ),
            _create_q(
                "Elektr zanjiridagi Om qonunining ifodasi qaysi?",
                "I = U / R",
                ["U = I / R", "R = I * U", "P = I² / R"],
                "Om qonuniga binoan, zanjir qismidagi tok kuchi kuchlanishga to'g'ri, qarshilikka teskari mutanosibdir.",
            ),
        ],
        "programming": [
            _create_q(
                "Python dasturlash tilida ro'yxat (list) oxiriga yangi element qaysi metod bilan qo'shiladi?",
                "append()",
                ["add()", "push()", "insert_last()"],
                "Python'da list ob'ektining append(element) metodi yangi qiymatni ro'yxat oxiriga qo'shadi.",
            ),
            _create_q(
                "Python'da quyidagi ma'lumot turlaridan qaysi biri o'zgarmas (immutable) hisoblanadi?",
                "tuple (kortej)",
                ["list (ro'yxat)", "dict (lug'at)", "set (to'plam)"],
                "Tuple (kortej) yaratilgandan so'ng uning elementlarini o'zgartirib bo'lmaydi (immutable).",
            ),
            _create_q(
                "Python tilida funksiya e'lon qilish uchun qaysi kalit so'z ishlatiladi?",
                "def",
                ["function", "func", "define"],
                "Python'da funksiyalar 'def' kalit so'zi bilan boshlanadi.",
            ),
            _create_q(
                "Lug'atdan (dict) bir vaqtning o'zida kalit va qiymatlarni olish uchun qaysi metod ishlatiladi?",
                "items()",
                ["keys()", "values()", "pairs()"],
                "dict.items() metodi (kalit, qiymat) juftliklaridan iborat ob'ekt qaytaradi.",
            ),
            _create_q(
                "Python'da xatoliklarni (exception) xavfsiz ushlash qaysi blok orqali bajariladi?",
                "try ... except",
                ["try ... catch", "do ... while", "try ... handle"],
                "Python sintaksisida xatoliklarni tutish uchun try va except bloklari qo'llaniladi.",
            ),
            _create_q(
                "Python'da '==' va 'is' operatorlari orasidagi farq nima?",
                "'==' qiymatlarni solishtiradi, 'is' esa xotiradagi identifikatorni (id)",
                [
                    "'==' faqat sonlar uchun, 'is' matnlar uchun",
                    "Ularning hech qanday farqi yo'q, ikkisi bir xil",
                    "'is' qiymatni, '==' turni tekshiradi",
                ],
                "'==' ob'ektlarning qiymatlari tengligini, 'is' esa ikkala o'zgaruvchi xotiradagi ayni bitta ob'ektga ishora qilishini tekshiradi.",
            ),
        ],
        "mathematics": [
            _create_q(
                "To'g'ri burchakli uchburchakda gipotenuza kvadratining katetlar kvadratlari yig'indisiga tengligi nima deyiladi?",
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
                "Tub son nima?",
                "Faqat 1 ga va o'ziga bo'linadigan 1 dan katta natural son",
                [
                    "Har qanday toq son",
                    "Faqat 2 ga qoldiqsiz bo'linadigan son",
                    "Noldan kichik manfiy son",
                ],
                "Tub sonlar faqat ikkita natural bo'luvchiga ega: 1 va sonning o'zi (masalan: 2, 3, 5, 7, 11...).",
            ),
            _create_q(
                "Doiraning yuzini hisoblash formulasi qaysi?",
                "S = π * r²",
                ["S = 2 * π * r", "S = π * d", "S = (π * r²) / 2"],
                "Doira yuzi radiusi r bo'lsa S = πr² formula bilan hisoblanadi.",
            ),
        ],
        "general": [
            _create_q(
                "Quyosh sistemasidagi eng katta sayyora qaysi?",
                "Yupiter",
                ["Saturn", "Mars", "Neptun"],
                "Yupiter Quyosh sistemasidagi eng katta va eng massiv sayyoradir.",
            ),
            _create_q(
                "O'simliklarda quyosh nuri yordamida organik modda va kislorod hosil bo'lish jarayoni nima deb ataladi?",
                "Fotosintez",
                ["Diffuziya", "Fermentatsiya", "Transpiratsiya"],
                "Xlorofill yordamida yorug'lik energiyasini kimyoviy energiyaga aylantirish jarayoni fotosintez deyiladi.",
            ),
            _create_q(
                "Inson tanasidagi eng katta ichki a'zo qaysi?",
                "Jigar",
                ["Yurak", "O'pka", "Oshqozon"],
                "Jigar inson tanasidagi eng yirik va ko'p funksiyali ichki bez va a'zodir.",
            ),
            _create_q(
                "Yer sharining qancha qismini suv (dunyo okeani) egallaydi?",
                "Taxminan 71%",
                ["Taxminan 50%", "Taxminan 85%", "Taxminan 60%"],
                "Yer yuzasining qariyb 71 foizi suv havzalari va okeanlar bilan qoplangan.",
            ),
        ],
    },
    "en": {
        "physics": [
            _create_q(
                "According to Pascal's principle, how is pressure applied to a confined fluid transmitted?",
                "Equally in all directions without loss of intensity",
                [
                    "Only towards the bottom of the vessel",
                    "Decreases with increasing depth",
                    "Only perpendicular to side walls",
                ],
                "Pascal's law states that pressure applied to an enclosed fluid is transmitted undiminished to every portion of the fluid and walls.",
            ),
            _create_q(
                "What factors determine the magnitude of Archimedes' buoyant force?",
                "Fluid density and the submerged volume of the object",
                [
                    "Only the total mass of the object",
                    "Shape of the container and depth",
                    "Material composition of the object",
                ],
                "Archimedes' buoyant force is F_b = ρ * g * V_submerged, proportional to fluid density and submerged volume.",
            ),
            _create_q(
                "What is Newton's Second Law of Motion represented as?",
                "F = m * a",
                ["E = m * c²", "P = F / A", "W = F * d"],
                "Newton's Second Law states that force equals mass times acceleration (F = ma).",
            ),
            _create_q(
                "What is the SI unit of pressure?",
                "Pascal (Pa)",
                ["Newton (N)", "Joule (J)", "Watt (W)"],
                "The SI unit of pressure is the Pascal (Pa), equivalent to 1 N/m².",
            ),
        ],
        "programming": [
            _create_q(
                "In Python, which method is used to add an item to the end of a list?",
                "append()",
                ["add()", "push()", "insert_last()"],
                "The append() method adds an element to the end of an existing list in Python.",
            ),
            _create_q(
                "Which of the following data types in Python is immutable?",
                "tuple",
                ["list", "dict", "set"],
                "Tuples cannot be modified after creation, making them immutable.",
            ),
            _create_q(
                "Which keyword is used to define a function in Python?",
                "def",
                ["func", "function", "define"],
                "The 'def' keyword is used to declare user-defined functions in Python.",
            ),
        ],
        "general": [
            _create_q(
                "What is the largest planet in our Solar System?",
                "Jupiter",
                ["Saturn", "Neptune", "Mars"],
                "Jupiter is the largest planet in the Solar System by both mass and volume.",
            ),
            _create_q(
                "What process do plants use to convert sunlight into glucose and oxygen?",
                "Photosynthesis",
                ["Respiration", "Fermentation", "Transpiration"],
                "Photosynthesis is the photochemical process by which green plants produce nutrients from light.",
            ),
        ],
    },
    "ru": {
        "physics": [
            _create_q(
                "Согласно закону Паскаля, как передается давление, производимое на жидкость или газ?",
                "Во все стороны одинаково без изменений",
                [
                    "Только ко дну сосуда",
                    "Уменьшается с глубиной",
                    "Только перпендикулярно боковым стенкам",
                ],
                "Закон Паскаля гласит: давление, производимое на жидкость или газ, передается в любую точку без изменений во всех направлениях.",
            ),
            _create_q(
                "От каких величин зависит выталкивающая сила Архимеда?",
                "От плотности жидкости и объема погруженной части тела",
                [
                    "Только от массы всего тела",
                    "От формы сосуда и глубины",
                    "От материала, из которого изготовлено тело",
                ],
                "Сила Архимеда F = ρ * g * V зависит от плотности среды и объема погруженной части тела.",
            ),
            _create_q(
                "Какова математическая запись второго закона Ньютона?",
                "F = m * a",
                ["E = m * c²", "P = F / S", "A = F * s"],
                "Второй закон Ньютона: сила равна произведению массы тела на его ускорение (F = ma).",
            ),
        ],
        "programming": [
            _create_q(
                "Какой метод используется для добавления элемента в конец списка в Python?",
                "append()",
                ["add()", "push()", "insert()"],
                "Метод append() добавляет элемент в конец существующего списка в Python.",
            ),
            _create_q(
                "Какой из перечисленных типов данных в Python является неизменяемым (immutable)?",
                "tuple (кортеж)",
                ["list (список)", "dict (словарь)", "set (множество)"],
                "Кортеж (tuple) не может быть изменен после создания.",
            ),
        ],
        "general": [
            _create_q(
                "Какая планета является крупнейшей в Солнечной системе?",
                "Юпитер",
                ["Сатурн", "Марс", "Нептун"],
                "Юпитер — самая большая планета Солнечной системы по массе и объему.",
            ),
        ],
    },
}


def _match_category(subject: str) -> str:
    subj_lower = subject.lower()
    if any(k in subj_lower for k in ["fizika", "physic", "физик", "paskal", "pascal", "arximed", "archimed", "nyuton", "newton", "bosim", "давлен"]):
        return "physics"
    if any(k in subj_lower for k in ["python", "dastur", "program", "программ", "kod", "code", "dev", "algoritm"]):
        return "programming"
    if any(k in subj_lower for k in ["matem", "math", "алгебр", "geometr", "hisob", "son"]):
        return "mathematics"
    return "general"


def generate_curated_quiz(
    subject: str,
    difficulty: str = "medium",
    count: int = 5,
    language: str = "uz",
) -> list[dict[str, Any]]:
    """Generate high-quality questions with guaranteed randomized options across A, B, C, D."""
    lang_key = language if language in QUESTIONS_BANK else "uz"
    cat = _match_category(subject)

    lang_pool = QUESTIONS_BANK.get(lang_key, QUESTIONS_BANK["uz"])
    questions = lang_pool.get(cat, [])

    # If pool for specific category is small, augment with general knowledge
    if len(questions) < count and cat != "general":
        general_qs = lang_pool.get("general", [])
        questions = questions + general_qs

    # If still small or empty, fallback to uz bank
    if len(questions) < count and lang_key != "uz":
        questions = QUESTIONS_BANK["uz"].get(cat, QUESTIONS_BANK["uz"]["general"])

    # Shuffle pool and clone with randomized options
    selected: list[dict[str, Any]] = []
    shuffled_pool = list(questions)
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

    # If count requested is greater than preset catalog, synthesize topic-specific questions
    while len(selected) < count:
        idx = len(selected) + 1
        if lang_key == "uz":
            question_text = f"{subject} fani bo'yicha {idx}-savol: Ushbu yo'nalishning asosiy qoidasi nima?"
            correct = f"{subject} asosiy nazariyasi va amaliy qonuniyatlari"
            wrongs = [
                f"{subject} faqat nazariyaga asoslangan bo'lib, amaliyotda qo'llanilmaydi",
                f"{subject} qoidalari faqat sun'iy sharoitda amal qiladi",
                f"{subject} formulasida massaning ahamiyati yo'q",
            ]
            expl = f"{subject} fani bo'yicha asosiy tushuncha va tamoyillar amaliyotda keng qo'llaniladi."
        elif lang_key == "ru":
            question_text = f"Вопрос {idx} по предмету {subject}: В чем заключается ключевой принцип?"
            correct = f"Фундаментальные законы и практические правила {subject}"
            wrongs = [
                f"{subject} является чисто теоретическим направлением",
                f"Законы {subject} действуют только в лабораторных условиях",
                f"Правила {subject} не имеют математического обоснования",
            ]
            expl = f"Ключевые принципы предмета {subject} лежат в основе его практического применения."
        else:
            question_text = f"Question {idx} on {subject}: What is a core principle of this subject?"
            correct = f"Foundational theory and core practical laws of {subject}"
            wrongs = [
                f"{subject} is purely theoretical without application",
                f"The rules of {subject} only hold in artificial environments",
                f"{subject} does not follow standard empirical methodology",
            ]
            expl = f"The core principles of {subject} are essential for conceptual mastery."

        selected.append(_create_q(question_text, correct, wrongs, expl))

    return selected
