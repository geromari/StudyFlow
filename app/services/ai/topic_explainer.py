"""Comprehensive educational topic explanation engine.

Provides in-depth, structured academic explanations with definitions, formulas,
real-world examples, and study takeaways in Uzbek, English, and Russian.
"""

import json
import logging
import urllib.parse
import urllib.request
from typing import Any

from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

# Curated high-yield knowledge entries for common core academic topics
CURATED_KNOWLEDGE: dict[str, dict[str, dict[str, Any]]] = {
    "paskal": {
        "uz": {
            "title": "Paskal qonuni (Gidrostatika)",
            "definition": (
                "Paskal qonuni — gidrostatika va aerostatikaning poydevor qonunlaridan biridir. "
                "U 1653-yilda fransuz olimi Blez Paskal tomonidan kashf etilgan.\n\n"
                "**Qonun ta'rifi:** Yopiq idishdagi suyuqlik yoki gaz sirtiga berilgan tashqi bosim "
                "suyuqlik (yoki gaz)ning barcha nuqtalariga barcha yo'nalishlar bo'yicha o'zgarishsiz, teng uzatiladi."
            ),
            "formula": "p = F / S  yoki  p₁ = p₂  =>  F₁ / S₁ = F₂ / S₂",
            "formula_desc": (
                "Bu yerda:\n"
                "• `p` — bosim (Paskal, Pa yoki N/m²)\n"
                "• `F` — ta'sir etuvchi kuch (Nyuton, N)\n"
                "• `S` — yuza sathi (m²)\n\n"
                "Gidravlik mashinada kichik porshenga F₁ kuch berilsa, katta porshenda F₂ = F₁ * (S₂ / S₁) barobar katta kuch hosil bo'ladi."
            ),
            "examples": [
                "**Gidravlik domkrat:** Avtomobilni ta'mirlashda inson qo'li bilan kichik kuch berib, 2-3 tonnalik og'ir avtomobilni oson ko'tarish imkonini beradi.",
                "**Avtomobil tormoz tizimi:** Haydovchi tormoz pedalini yengil bosganda, tormoz suyuqligi orqali bu bosim barcha g'ildiraklardagi kolodkalarga teng uzatilib, katta tezlikdagi mashinani to'xtatadi.",
                "**Paskal shari tajribasi:** Suv bilan to'ldirilgan teshikli sharcha porsheni bosilganda, suv barcha teshiklardan bir xil kuch va tezlikda favvora bo'lib otilib chiqadi.",
            ],
            "applications": [
                "Og'ir sanoatdagi gidravlik presslar (metall va plastmassalarni qolipga solish).",
                "Ekskavator, kran va yuk ko'targichlarning gidravlik boshqaruv tutqichlari.",
                "Suv osti kemalari va gidro-tizimlarining germetik bosim hisob-kitoblari.",
            ],
            "takeaways": [
                "Bosim barcha yo'nalishda TENG tarqaladi (faqat pastga emas!).",
                "Qattiq jismlar bosimni faqat kuch yo'nalishi bo'ylab uzatsa, suyuqlik va gazlar barcha tomonga uzatadi.",
                "SI tizimida bosim birligi Paskal (Pa) = 1 N / m².",
            ],
        },
        "en": {
            "title": "Pascal's Principle (Hydrostatics)",
            "definition": (
                "Pascal's law states that when there is an increase in pressure at any point in a confined incompressible fluid, "
                "there is an equal increase at every other point in the container.\n\n"
                "Discovered by Blaise Pascal in 1653, it is the foundational principle behind fluid mechanics and hydraulic power."
            ),
            "formula": "Δp = F₁ / A₁ = F₂ / A₂",
            "formula_desc": (
                "Where `F` is force in Newtons and `A` is the cross-sectional piston area in m².\n"
                "Because pressure is constant throughout, a small force applied to a small area yields a proportional large force on a larger area."
            ),
            "examples": [
                "**Hydraulic Lift:** Allows a single mechanic to easily lift heavy vehicles by transmitting pressure through fluid conduits.",
                "**Hydraulic Car Brakes:** Depressing the brake pedal creates pressure that spreads uniformly to all four brake calipers.",
            ],
            "applications": ["Heavy manufacturing presses", "Airplane control hydraulics", "Construction machinery"],
            "takeaways": [
                "Pressure is transmitted undiminished in all directions.",
                "Force multiplication does not violate conservation of energy (Work in = Work out).",
            ],
        },
        "ru": {
            "title": "Закон Паскаля (Гидростатика)",
            "definition": (
                "Закон Паскаля — основной закон гидростатики: давление, производимое на жидкость или газ, "
                "передается в любую точку жидкости или газа одинаково по всем направлениям без изменения."
            ),
            "formula": "p = F / S  =>  F₁ / S₁ = F₂ / S₂",
            "formula_desc": "p — давление (Па), F — сила (Н), S — площадь поршня (м²).",
            "examples": [
                "**Гидравлический домкрат:** Подъем тяжелых автомобилей малой мускульной силой.",
                "**Тормозная система автомобиля:** Равномерное торможение всех колес через гидравлическую жидкость.",
            ],
            "applications": ["Гидравлические прессы", "Строительные подъемники", "Пневматические механизмы"],
            "takeaways": [
                "Давление передается во все стороны, а не только по направлению силы.",
                "Единица давления в СИ — Паскаль (Па = Н/м²).",
            ],
        },
    },
    "arximed": {
        "uz": {
            "title": "Arximed qonuni (Suzish qonuni)",
            "definition": (
                "Arximed qonuni — suyuqlik va gazlar mexanikasining asosiy qonunidir. "
                "Miloddan avvalgi III asrda yunon olimi Arximed tomonidan kashf etilgan.\n\n"
                "**Qonun ta'rifi:** Suyuqlikka (yoki gazga) botirilgan jismga uning botgan qismi siqib chiqargan "
                "suyuqlik (gaz) og'irligiga teng bo'lgan yuqoriga yo'nalgan itaruvchi kuch (Arximed kuchi) ta'sir qiladi."
            ),
            "formula": "F_A = ρ * g * V",
            "formula_desc": (
                "Bu yerda:\n"
                "• `F_A` — Arximed (itaruvchi) kuchi (Nyuton, N)\n"
                "• `ρ` (ro) — suyuqlik yoki gazning zichligi (kg/m³)\n"
                "• `g` — erkin tushish tezlanishi (~9.8 m/s²)\n"
                "• `V` — jismning suyuqlikka botgan qismi hajmi (m³)"
            ),
            "examples": [
                "**Gigant po'lat kemalarning suzishi:** Temir suvdan og'ir bo'lsa-da, ichki bo'shliqlar hisobiga kemaning o'rtacha zichligi suvnikidan ancha kichik bo'ladi va ulkan kema cho'kmaydi.",
                "**Havo sharlari:** Geliy yoki issiq havo bilan to'ldirilgan havo sharlari havoning Arximed kuchi hisobiga osmonga ko'tariladi.",
                "**Suvda jismning yengillashishi:** Suvga tushgan odam yoki tosh havoga qaraganda ancha yengil tuyuladi.",
            ],
            "applications": ["Kemachilik va suv osti kemalari", "Aereonavtika (havo sharlari, dirijabllar)", "Arometrlar (zichlik o'lchov asboblari)"],
            "takeaways": [
                "Agar jism zichligi suyuqlik zichligidan kichik bo'lsa (ρ_j < ρ_s) — jism suzadi.",
                "Agar zichliklar teng bo'lsa (ρ_j = ρ_s) — jism suyuqlik ichida muallaq turadi.",
                "Agar jism zichligi katta bo'lsa (ρ_j > ρ_s) — jism cho'kadi.",
            ],
        },
        "en": {
            "title": "Archimedes' Principle (Buoyancy)",
            "definition": (
                "Archimedes' principle indicates that the upward buoyant force that is exerted on a body immersed in a fluid, "
                "whether fully or partially submerged, is equal to the weight of the fluid that the body displaces."
            ),
            "formula": "F_b = ρ * g * V_submerged",
            "formula_desc": "ρ is fluid density, g is gravity, and V is the displaced liquid volume.",
            "examples": [
                "**Floating steel cargo ships:** Internal empty air spaces lower the vessel's average density below that of seawater.",
                "**Hot Air Balloons:** Rising into the sky because heated air is less dense than ambient air.",
            ],
            "applications": ["Naval architecture", "Submarine ballast systems", "Hydrometers"],
            "takeaways": ["Buoyant force depends solely on displaced volume and fluid density, not object mass."],
        },
        "ru": {
            "title": "Закон Архимеда (Гидростатика)",
            "definition": (
                "Закон Архимеда: на тело, погруженное в жидкость или газ, действует выталкивающая сила, "
                "равная весу вытесненной этим телом жидкости или газа."
            ),
            "formula": "F_A = ρ * g * V",
            "formula_desc": "ρ — плотность жидкости, g — ускорение свободного падения, V — объем погруженной части.",
            "examples": [
                "**Плавание кораблей:** Огромные металлические суда держатся на воде за счет вытеснения большого объема воды.",
                "**Воздушные шары:** Подъем за счет архимедовой силы воздуха.",
            ],
            "applications": ["Судостроение", "Подводные лодки", "Ареометры"],
            "takeaways": ["Если сила тяжести больше силы Архимеда — тело тонет, если меньше — всплывает."],
        },
    },
    "python": {
        "uz": {
            "title": "Python dasturlash tili asoslari",
            "definition": (
                "Python — yuqori darajadagi, sodda o'qiluvchan sintaksisga ega bo'lgan, interpretatsiya qilinadigan dasturlash tilidir. "
                "U 1991-yilda Gvido van Rossum tomonidan yaratilgan bo'lib, bugungi kunda sun'iy intellekt, veb-dasturlash va avtomatlashtirishda 1-o'rinda turadi."
            ),
            "formula": "print('Hello, StudyFlow!')\ndef func(x):\n    return x * 2",
            "formula_desc": (
                "Python'da kod bloklari jingalak qavslar `{}` bilan emas, balki to'g'ri bo'shliqlar (indentation / 4 ta probel) orqali belgilanadi.\n"
                "Asosiy ma'lumot turlari: int, float, str, bool, list, tuple, dict, set."
            ),
            "examples": [
                "**Ro'yxatlar (List):** `mevalar = ['olma', 'anor']; mevalar.append('uzum')`",
                "**Lug'atlar (Dict):** `talaba = {'ism': 'Ali', 'yosh': 20}`",
                "**Shart va Sikllar:** `for i in range(5): print(i)`",
            ],
            "applications": ["Sun'iy Intellekt va Machine Learning (TensorFlow, PyTorch)", "Telegram Botlar (Aiogram, Telebot)", "Veb dasturlash (Django, FastAPI)"],
            "takeaways": [
                "O'rganish oson, qulay va tezkor yoziladi.",
                "Dinamik tiplashtirilgan va keng kutubxonalar ekotizimiga ega.",
            ],
        },
        "en": {
            "title": "Python Programming Language",
            "definition": (
                "Python is a high-level, interpreted programming language emphasizing code readability and simplicity. "
                "It is the global standard for AI, data science, web services, and automation."
            ),
            "formula": "def calculate(a, b):\n    return a + b",
            "formula_desc": "Indentation defines code execution blocks. Supports procedural, functional, and object-oriented paradigms.",
            "examples": ["Web APIs with FastAPI", "Telegram bots with Aiogram", "Machine Learning with PyTorch"],
            "applications": ["Data Science", "Backend Development", "Automation Scripts"],
            "takeaways": ["Extensive standard library (batteries included)", "Massive global developer community"],
        },
        "ru": {
            "title": "Язык программирования Python",
            "definition": (
                "Python — высокоуровневый язык программирования с понятным синтаксисом и динамической типизацией. "
                "Широко используется в машинном обучении, веб-разработке и автоматизации."
            ),
            "formula": "for item in [1, 2, 3]:\n    print(item * 2)",
            "formula_desc": "Блоки кода выделяются отступами (4 пробела).",
            "examples": ["Создание Telegram-ботов", "Анализ данных", "Веб-сервисы на FastAPI"],
            "applications": ["Искусственный интеллект", "Автоматизация процессов", "Бэкенд-разработка"],
            "takeaways": ["Простота чтения кода", "Крупнейшая экосистема библиотек"],
        },
    },
}


def _search_wiki(query: str, lang: str = "uz") -> str | None:
    """Fetch encyclopedia summary from Wikipedia."""
    try:
        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(query)
        req = urllib.request.Request(url, headers={"User-Agent": "StudyFlowBot/1.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            extract = data.get("extract")
            if extract and len(extract) > 40:
                return extract
    except Exception:
        pass

    # Fallback to wikipedia search
    try:
        search_url = (
            f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch="
            + urllib.parse.quote(query)
            + "&format=json"
        )
        req = urllib.request.Request(search_url, headers={"User-Agent": "StudyFlowBot/1.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("query", {}).get("search", [])
            if results:
                title = results[0]["title"]
                url2 = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title)
                req2 = urllib.request.Request(url2, headers={"User-Agent": "StudyFlowBot/1.0"})
                with urllib.request.urlopen(req2, timeout=3) as resp2:
                    data2 = json.loads(resp2.read().decode("utf-8"))
                    return data2.get("extract")
    except Exception:
        pass

    return None


def _search_ddgs(query: str) -> list[str]:
    """Fetch top search snippets via DDGS."""
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=3))
        snippets = [r["body"] for r in results if r.get("body")]
        return snippets
    except Exception as e:
        logger.warning(f"DDGS snippet fetch failed: {e}")
        return []


def explain_topic_comprehensively(
    topic: str,
    mode: str | None = None,
    language: str = "uz",
) -> str:
    """Generate a rich, thorough, beautifully formatted educational explanation."""
    lang = language if language in ["uz", "en", "ru"] else "uz"
    topic_clean = topic.strip()
    topic_lower = topic_clean.lower()

    # 1. Check curated high-yield topics first
    matched_entry = None
    for key, data in CURATED_KNOWLEDGE.items():
        if key in topic_lower:
            matched_entry = data.get(lang, data.get("uz"))
            break

    if matched_entry:
        title = matched_entry["title"]
        definition = matched_entry["definition"]
        formula = matched_entry.get("formula", "")
        formula_desc = matched_entry.get("formula_desc", "")
        examples = matched_entry.get("examples", [])
        applications = matched_entry.get("applications", [])
        takeaways = matched_entry.get("takeaways", [])

        if mode == "summarize":
            if lang == "uz":
                return (
                    f"📝 **{title} — Qisqacha Xulosa:**\n\n"
                    f"{definition}\n\n"
                    f"📌 **Asosiy qoidalar:**\n"
                    + "\n".join(f"• {t}" for t in takeaways)
                )
            elif lang == "ru":
                return (
                    f"📝 **{title} — Краткое резюме:**\n\n"
                    f"{definition}\n\n"
                    f"📌 **Ключевые пункты:**\n"
                    + "\n".join(f"• {t}" for t in takeaways)
                )
            else:
                return (
                    f"📝 **{title} — High-Yield Summary:**\n\n"
                    f"{definition}\n\n"
                    f"📌 **Key Takeaways:**\n"
                    + "\n".join(f"• {t}" for t in takeaways)
                )

        if mode == "examples":
            if lang == "uz":
                return (
                    f"🔍 **{title} — Amaliy va hayotiy misollar:**\n\n"
                    + "\n\n".join(f"{i+1}. {ex}" for i, ex in enumerate(examples))
                )
            elif lang == "ru":
                return (
                    f"🔍 **{title} — Практические примеры:**\n\n"
                    + "\n\n".join(f"{i+1}. {ex}" for i, ex in enumerate(examples))
                )
            else:
                return (
                    f"🔍 **{title} — Real-world Examples:**\n\n"
                    + "\n\n".join(f"{i+1}. {ex}" for i, ex in enumerate(examples))
                )

        # Default full thorough explanation
        if lang == "uz":
            return (
                f"📚 **{title} haqida to'liq tushuncha:**\n\n"
                f"📖 **1. Ta'rif va nazariy mohiyat:**\n{definition}\n\n"
                f"🔬 **2. Asosiy qonuniyat va formula:**\n"
                f"```\n{formula}\n```\n"
                f"{formula_desc}\n\n"
                f"💡 **3. Hayotiy va amaliy misollar:**\n"
                + "\n".join(f"• {ex}" for ex in examples)
                + "\n\n⚙️ **4. Amaliyotda va texnikada qo'llanilishi:**\n"
                + "\n".join(f"• {app}" for app in applications)
                + "\n\n📌 **5. Imtihon va darslar uchun muhim xulosalar:**\n"
                + "\n".join(f"• {t}" for t in takeaways)
            )
        elif lang == "ru":
            return (
                f"📚 **{title} — Подробное объяснение:**\n\n"
                f"📖 **1. Определение и суть:**\n{definition}\n\n"
                f"🔬 **2. Формула и математический смысл:**\n"
                f"```\n{formula}\n```\n"
                f"{formula_desc}\n\n"
                f"💡 **3. Практические примеры из жизни:**\n"
                + "\n".join(f"• {ex}" for ex in examples)
                + "\n\n⚙️ **4. Применение в технике:**\n"
                + "\n".join(f"• {app}" for app in applications)
                + "\n\n📌 **5. Главные выводы:**\n"
                + "\n".join(f"• {t}" for t in takeaways)
            )
        else:
            return (
                f"📚 **Comprehensive Guide: {title}**\n\n"
                f"📖 **1. Definition & Core Concept:**\n{definition}\n\n"
                f"🔬 **2. Formula & Principles:**\n"
                f"```\n{formula}\n```\n"
                f"{formula_desc}\n\n"
                f"💡 **3. Real-world Examples:**\n"
                + "\n".join(f"• {ex}" for ex in examples)
                + "\n\n⚙️ **4. Practical Applications:**\n"
                + "\n".join(f"• {app}" for app in applications)
                + "\n\n📌 **5. Key Study Takeaways:**\n"
                + "\n".join(f"• {t}" for t in takeaways)
            )

    # 2. Dynamic synthesis via Wikipedia + Search
    wiki_info = _search_wiki(topic_clean, lang)
    if not wiki_info and lang != "en":
        wiki_info = _search_wiki(topic_clean, "en")

    snippets = _search_ddgs(f"{topic_clean} {lang}")
    combined_snippet = " ".join(snippets[:2]) if snippets else ""

    content = wiki_info or combined_snippet or (
        f"{topic_clean} fanining asosiy tamoyillari va amaliy qonuniyatlari."
        if lang == "uz"
        else f"Core concepts and foundational principles of {topic_clean}."
    )

    if lang == "uz":
        return (
            f"📚 **{topic_clean} haqida to'liq tushuncha:**\n\n"
            f"📖 **1. Asosiy ta'rif va mohiyat:**\n"
            f"{content}\n\n"
            f"🔬 **2. Muhim qonuniyatlar va tamoyillar:**\n"
            f"• Ushbu mavzu ta'lim tizimida fundamental ahamiyatga ega bo'lib, nazariya va amaliyotni birlashtiradi.\n"
            f"• Mavzuni o'rganishda asosiy ta'riflar, xossalar va formulalarni aniq ajratib olish zarur.\n\n"
            f"💡 **3. Amaliy qo'llanilishi va misollar:**\n"
            f"• {topic_clean} bo'yicha masalalar yechishda dastlab berilgan ma'lumotlarni tartiblash va mos formulani tanlash talab etiladi.\n"
            f"• Texnologiya, muhandislik va kundalik hayotda ushbu tamoyillar keng qo'llaniladi.\n\n"
            f"📌 **4. Xulosa va eslab qolish:**\n"
            f"• Asosiy qoidalarni mustahkamlash uchun mavzu bo'yicha botdagi **Quiz** bo'limida test topshirishingiz tavsiya etiladi."
        )
    elif lang == "ru":
        return (
            f"📚 **Полное объяснение: {topic_clean}**\n\n"
            f"📖 **1. Определение и ключевая суть:**\n"
            f"{content}\n\n"
            f"🔬 **2. Принципы и структура:**\n"
            f"• Данная тема является фундаментальной в образовательном процессе.\n"
            f"• Рекомендуется обратить внимание на основные определения и формулы.\n\n"
            f"💡 **3. Практическое применение:**\n"
            f"• При решении задач структурируйте исходные данные и применяйте базовые правила темы.\n\n"
            f"📌 **4. Заключение:**\n"
            f"• Закрепите материал, пройдя тест в разделе **Quiz** нашего бота."
        )
    else:
        return (
            f"📚 **Comprehensive Explanation: {topic_clean}**\n\n"
            f"📖 **1. Core Concept & Definition:**\n"
            f"{content}\n\n"
            f"🔬 **2. Key Principles & Rules:**\n"
            f"• This subject is fundamental for conceptual academic mastery.\n"
            f"• Focus on distinguishing core definitions and governing principles.\n\n"
            f"💡 **3. Practical Applications:**\n"
            f"• Apply these concepts systematically by working through targeted problems.\n\n"
            f"📌 **4. Summary & Next Steps:**\n"
            f"• Reinforce your knowledge by taking a practice quiz in the **Quiz** section."
        )
