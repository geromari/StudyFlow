"""Internationalization (i18n) module supporting Uzbek, English, and Russian."""

from typing import Any

SUPPORTED_LANGUAGES = {
    "uz": "🇺🇿 O'zbekcha",
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
}

DEFAULT_LANGUAGE = "uz"

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ------------------ Navigation & Common ------------------
    "please_start_first": {
        "uz": "Iltimos, avval botni ishga tushirish uchun /start buyrug'ini yuboring.",
        "en": "Please send /start to begin.",
        "ru": "Пожалуйста, отправьте /start для начала работы.",
    },
    "btn_back": {
        "uz": "⬅️ Ortga",
        "en": "⬅️ Back",
        "ru": "⬅️ Назад",
    },
    "btn_cancel": {
        "uz": "❌ Bekor qilish",
        "en": "❌ Cancel",
        "ru": "❌ Отмена",
    },
    "btn_confirm": {
        "uz": "✅ Tasdiqlash",
        "en": "✅ Confirm",
        "ru": "✅ Подтвердить",
    },
    "action_cancelled": {
        "uz": "Amal bekor qilindi.",
        "en": "Action cancelled.",
        "ru": "Действие отменено.",
    },
    "generic_error": {
        "uz": "Kutilmagan xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
        "en": "Something went wrong. Please try again.",
        "ru": "Что-то пошло не так. Пожалуйста, попробуйте еще раз.",
    },
    "rate_limit_exceeded": {
        "uz": "⚠️ So'rovlar juda ko'p! Iltimos, biroz kutib turing.",
        "en": "⚠️ Too many requests! Please wait a moment.",
        "ru": "⚠️ Слишком много запросов! Пожалуйста, подождите немного.",
    },

    # ------------------ Main Menu Buttons ------------------
    "menu_subjects": {
        "uz": "📚 Fanlarim",
        "en": "📚 My Subjects",
        "ru": "📚 Мои предметы",
    },
    "menu_ai": {
        "uz": "🤖 AI Yordamchi",
        "en": "🤖 AI Assistant",
        "ru": "🤖 AI Помощник",
    },
    "menu_quiz": {
        "uz": "📝 Quiz",
        "en": "📝 Quiz",
        "ru": "📝 Викторина",
    },
    "menu_study_plan": {
        "uz": "📅 O'quv rejasi",
        "en": "📅 Study Plan",
        "ru": "📅 План учебы",
    },
    "menu_goals": {
        "uz": "🎯 Maqsadlarim",
        "en": "🎯 My Goals",
        "ru": "🎯 Мои цели",
    },
    "menu_progress": {
        "uz": "📊 Statistika",
        "en": "📊 Progress",
        "ru": "📊 Прогресс",
    },
    "menu_streak": {
        "uz": "🔥 Streak",
        "en": "🔥 Streak",
        "ru": "🔥 Серия",
    },
    "menu_focus": {
        "uz": "⏱ Diqqat rejimi",
        "en": "⏱ Focus Mode",
        "ru": "⏱ Режим фокуса",
    },
    "menu_pdf": {
        "uz": "📄 PDF O'rganish",
        "en": "📄 PDF Learning",
        "ru": "📄 Обучение по PDF",
    },
    "menu_achievements": {
        "uz": "🏆 Yutuqlar",
        "en": "🏆 Achievements",
        "ru": "🏆 Достижения",
    },
    "menu_settings": {
        "uz": "⚙️ Sozlamalar",
        "en": "⚙️ Settings",
        "ru": "⚙️ Настройки",
    },
    "main_menu_title": {
        "uz": "🎓 **StudyFlow Asosiy Menyu**\nQuyidagi bo'limlardan birini tanlang:",
        "en": "🎓 **StudyFlow Main Menu**\nChoose an option below to continue:",
        "ru": "🎓 **Главное меню StudyFlow**\nВыберите раздел ниже:",
    },

    # ------------------ Registration Flow ------------------
    "welcome_new_user": {
        "uz": "Assalomu alaykum, {name}! 🌟\n**StudyFlow** ga xush kelibsiz — sizning shaxsiy AI ta'lim yordamchingiz.\n\nTilni tanlang / Choose your language / Выберите язык:",
        "en": "Welcome, {name}! 🌟\nWelcome to **StudyFlow** — your personal AI study assistant.\n\nPlease choose your language / Tilni tanlang / Выберите язык:",
        "ru": "Добро пожаловать, {name}! 🌟\nДобро пожаловать в **StudyFlow** — вашего личного ИИ-помощника в учебе.\n\nВыберите язык / Choose language / Tilni tanlang:",
    },
    "reg_ask_interests": {
        "uz": "Ajoyib! Qaysi fanlarni yoki yo'nalishlarni o'rganmoqchisiz?\n(Masalan: Matematika, Dasturlash, Ingliz tili)",
        "en": "Great! What subjects or areas do you want to study?\n(e.g., Mathematics, Programming, English)",
        "ru": "Отлично! Какие предметы или сферы вы хотите изучать?\n(Например: Математика, Программирование, Английский)",
    },
    "reg_ask_daily_target": {
        "uz": "Kuniga necha daqiqa shug'ullanmoqchisiz?",
        "en": "What is your daily study target in minutes?",
        "ru": "Сколько минут в день вы планируете учиться?",
    },
    "reg_completed": {
        "uz": "🎉 Ro'yxatdan muvaffaqiyatli o'tdingiz!\nKeling, maqsadlarga birga erishamiz!",
        "en": "🎉 Registration complete!\nLet's achieve your study goals together!",
        "ru": "🎉 Регистрация завершена!\nДавайте достигать учебных целей вместе!",
    },

    # ------------------ Profile ------------------
    "profile_title": {
        "uz": "👤 **Sizning profilingiz**\n\n"
              "🆔 ID: `{telegram_id}`\n"
              "👤 Ism: {first_name}\n"
              "🌐 Til: {language}\n"
              "🕒 Vaqt mintaqasi: {timezone}\n"
              "🎯 Kunlik maqsad: {daily_target} daqiqa\n"
              "⭐ XP: {xp}\n"
              "🏅 Daraja: {level}\n"
              "🔥 Streak: {streak} kun\n"
              "📅 Qo'shilgan sana: {created_at}\n"
              "⏱ Oxirgi faollik: {last_activity}",
        "en": "👤 **Your Profile**\n\n"
              "🆔 ID: `{telegram_id}`\n"
              "👤 Name: {first_name}\n"
              "🌐 Language: {language}\n"
              "🕒 Timezone: {timezone}\n"
              "🎯 Daily Target: {daily_target} min\n"
              "⭐ XP: {xp}\n"
              "🏅 Level: {level}\n"
              "🔥 Streak: {streak} days\n"
              "📅 Joined: {created_at}\n"
              "⏱ Last Activity: {last_activity}",
        "ru": "👤 **Ваш профиль**\n\n"
              "🆔 ID: `{telegram_id}`\n"
              "👤 Имя: {first_name}\n"
              "🌐 Язык: {language}\n"
              "🕒 Часовой пояс: {timezone}\n"
              "🎯 Цель на день: {daily_target} мин\n"
              "⭐ XP: {xp}\n"
              "🏅 Уровень: {level}\n"
              "🔥 Серия: {streak} дн.\n"
              "📅 Дата регистрации: {created_at}\n"
              "⏱ Последняя активность: {last_activity}",
    },

    # ------------------ Subjects & Topics ------------------
    "subjects_list_title": {
        "uz": "📚 **Sizning fanlaringiz** ({count} ta):",
        "en": "📚 **Your Subjects** ({count}):",
        "ru": "📚 **Ваши предметы** ({count}):",
    },
    "no_subjects": {
        "uz": "Sizda hali fanlar yo'q. Yangi fan qo'shish uchun pastdagi tugmani bosing.",
        "en": "You don't have any subjects yet. Click below to add your first subject.",
        "ru": "У вас пока нет предметов. Нажмите кнопку ниже, чтобы добавить предмет.",
    },
    "btn_add_subject": {
        "uz": "➕ Fan qo'shish",
        "en": "➕ Add Subject",
        "ru": "➕ Добавить предмет",
    },
    "btn_delete_subject": {
        "uz": "🗑 O'chirish",
        "en": "🗑 Delete",
        "ru": "🗑 Удалить",
    },
    "btn_rename_subject": {
        "uz": "✏️ Nomini o'zgartirish",
        "en": "✏️ Rename",
        "ru": "✏️ Переименовать",
    },
    "btn_topics": {
        "uz": "📑 Mavzular",
        "en": "📑 Topics",
        "ru": "📑 Темы",
    },
    "btn_add_topic": {
        "uz": "➕ Mavzu qo'shish",
        "en": "➕ Add Topic",
        "ru": "➕ Добавить тему",
    },
    "btn_start_study_subject": {
        "uz": "📖 O'rganishni boshlash",
        "en": "📖 Start Studying",
        "ru": "📖 Начать изучение",
    },
    "prompt_enter_subject_name": {
        "uz": "Yangi fan nomini kiriting:",
        "en": "Enter the name of the new subject:",
        "ru": "Введите название нового предмета:",
    },
    "prompt_enter_new_subject_name": {
        "uz": "Yangi nomni kiriting:",
        "en": "Enter the new name:",
        "ru": "Введите новое название:",
    },
    "prompt_enter_topic_name": {
        "uz": "Mavzu nomini kiriting:",
        "en": "Enter the topic name:",
        "ru": "Введите название темы:",
    },
    "subject_created": {
        "uz": "✅ '{name}' fani muvaffaqiyatli yaratildi!",
        "en": "✅ Subject '{name}' created successfully!",
        "ru": "✅ Предмет '{name}' успешно создан!",
    },
    "subject_deleted": {
        "uz": "🗑 Fan o'chirildi.",
        "en": "🗑 Subject deleted.",
        "ru": "🗑 Предмет удален.",
    },
    "confirm_delete_subject": {
        "uz": "Rostdan ham '{name}' fanini va barcha mavzularini o'chirmoqchimisiz?",
        "en": "Are you sure you want to delete '{name}' and all its topics?",
        "ru": "Вы уверены, что хотите удалить '{name}' и все его темы?",
    },
    "subject_view_progress": {
        "uz": "📊 O'zlashtirish: {percent}%\n📑 Mavzular: {completed}/{total} ta bajarildi",
        "en": "📊 Progress: {percent}%\n📑 Topics: {completed}/{total} completed",
        "ru": "📊 Прогресс: {percent}%\n📑 Темы: {completed}/{total} выполнено",
    },
    "subject_not_found": {
        "uz": "Fan topilmadi.",
        "en": "Subject not found.",
        "ru": "Предмет не найден.",
    },
    "topics_list_title": {
        "uz": "📑 **{name}** fani mavzulari:\n\nMavzuni tanlang yoki yangisini qo'shing:",
        "en": "📑 **{name}** topics:\n\nSelect a topic or add a new one:",
        "ru": "📑 Темы предмета **{name}**:\n\nВыберите тему или добавьте новую:",
    },
    "study_subject_title": {
        "uz": "⏱ **{name}** fanini o'rganish\n\nQanday usulda o'rganishni xohlaysiz? Variantlardan birini tanlang:",
        "en": "⏱ Study **{name}**\n\nHow would you like to study? Choose an option below:",
        "ru": "⏱ Изучение предмета **{name}**\n\nКак вы хотите учиться? Выберите вариант ниже:",
    },
    "btn_study_focus_15": {
        "uz": "⏱ 15 daqiqa (Tezkor)",
        "en": "⏱ 15 min (Quick)",
        "ru": "⏱ 15 мин (Быстро)",
    },
    "btn_study_focus_25": {
        "uz": "🍅 25 daqiqa (Pomodoro)",
        "en": "🍅 25 min (Pomodoro)",
        "ru": "🍅 25 мин (Помидоро)",
    },
    "btn_study_focus_45": {
        "uz": "⏱ 45 daqiqa (Chuqur)",
        "en": "⏱ 45 min (Deep)",
        "ru": "⏱ 45 мин (Глубоко)",
    },
    "btn_study_quiz": {
        "uz": "📝 Fan bo'yicha Test (Quiz)",
        "en": "📝 Subject Quiz",
        "ru": "📝 Тест по предмету",
    },
    "btn_study_ai_explain": {
        "uz": "🤖 AI dan tushuntirish so'rash",
        "en": "🤖 Ask AI to Explain",
        "ru": "🤖 Объяснить через ИИ",
    },

    # ------------------ AI Assistant ------------------
    "ai_assistant_intro": {
        "uz": "🤖 **AI Yordamchi**\n\nSavolingizni yozing yoki amal tanlang:\n• Tushuntirish\n• Xulosa qilish\n• Misollar keltirish\n• Qadam-baqadam yechim\n• O'quv konspekti tuzish",
        "en": "🤖 **AI Assistant**\n\nAsk any question or pick an action:\n• Explain concepts\n• Summarize texts\n• Provide examples\n• Step-by-step guidance\n• Create study notes",
        "ru": "🤖 **ИИ Помощник**\n\nЗадайте вопрос или выберите действие:\n• Объяснить concept\n• Составить конспект\n• Привести примеры\n• Пошаговое объяснение\n• Сделать резюме",
    },
    "ai_mode_explain_btn": {
        "uz": "💡 Tushuntirish",
        "en": "💡 Explain",
        "ru": "💡 Объяснить",
    },
    "ai_mode_summarize_btn": {
        "uz": "📝 Xulosa qilish",
        "en": "📝 Summarize",
        "ru": "📝 Кратко",
    },
    "ai_mode_examples_btn": {
        "uz": "🔍 Misollar",
        "en": "🔍 Examples",
        "ru": "🔍 Примеры",
    },
    "ai_mode_study_notes_btn": {
        "uz": "📑 Konspekt",
        "en": "📑 Study Notes",
        "ru": "📑 Конспект",
    },
    "ai_mode_step_by_step_btn": {
        "uz": "🔢 Qadamma-qadam",
        "en": "🔢 Step-by-Step",
        "ru": "🔢 Пошагово",
    },
    "ai_clear_history_btn": {
        "uz": "🧹 Tarixni tozalash",
        "en": "🧹 Clear History",
        "ru": "🧹 Очистить историю",
    },
    "ai_prompt_enter": {
        "uz": "Savolingizni yoki o'rganmoqchi bo'lgan mavzungizni yozing:",
        "en": "Type your question or study topic below:",
        "ru": "Напишите ваш вопрос или тему для изучения:",
    },
    "ai_mode_activated": {
        "uz": "✅ **{mode}** rejimi faollashdi. Mavzuni yoki savolingizni yuboring:",
        "en": "✅ **{mode}** mode active. Enter your topic or question:",
        "ru": "✅ Режим **{mode}** активирован. Отправьте тему или вопрос:",
    },
    "ai_thinking": {
        "uz": "🤔 AI javob tayyorlamoqda...",
        "en": "🤔 AI is thinking...",
        "ru": "🤔 ИИ готовит ответ...",
    },
    "ai_context_cleared": {
        "uz": "🧹 Suhbat tarixi tozalandi.",
        "en": "🧹 Conversation context cleared.",
        "ru": "🧹 История диалога очищена.",
    },
    "btn_clear_ai_context": {
        "uz": "🧹 Tarixni tozalash",
        "en": "🧹 Clear History",
        "ru": "🧹 Очистить историю",
    },

    # ------------------ Quiz ------------------
    "quiz_intro": {
        "uz": "📝 **Quiz Yaratish**\nTest boshlash uchun fanni tanlang:",
        "en": "📝 **Quiz Generator**\nSelect a subject to start a quiz:",
        "ru": "📝 **Генератор викторин**\nВыберите предмет для начала теста:",
    },
    "quiz_select_difficulty": {
        "uz": "Qiyinlik darajasini tanlang:",
        "en": "Select difficulty level:",
        "ru": "Выберите уровень сложности:",
    },
    "diff_easy": {"uz": "🟢 Oson", "en": "🟢 Easy", "ru": "🟢 Легкий"},
    "diff_medium": {"uz": "🟡 O'rtacha", "en": "🟡 Medium", "ru": "🟡 Средний"},
    "diff_hard": {"uz": "🔴 Qiyin", "en": "🔴 Hard", "ru": "🔴 Сложный"},
    "quiz_select_count": {
        "uz": "Savollar sonini tanlang:",
        "en": "Select number of questions:",
        "ru": "Выберите количество вопросов:",
    },
    "quiz_generating": {
        "uz": "⚡ AI test savollarini tuzmoqda...",
        "en": "⚡ AI is generating quiz questions...",
        "ru": "⚡ ИИ генерирует вопросы викторины...",
    },
    "quiz_correct": {
        "uz": "✅ To'g'ri javob!\n\n💡 {explanation}",
        "en": "✅ Correct!\n\n💡 {explanation}",
        "ru": "✅ Правильно!\n\n💡 {explanation}",
    },
    "quiz_wrong": {
        "uz": "❌ Noto'g'ri! To'g'ri javob: **{correct}**\n\n💡 {explanation}",
        "en": "❌ Incorrect! Correct answer: **{correct}**\n\n💡 {explanation}",
        "ru": "❌ Неверно! Правильный ответ: **{correct}**\n\n💡 {explanation}",
    },
    "quiz_finished": {
        "uz": "🏁 **Quiz yakunlandi!**\n\n"
              "📊 Natija: {score}/{total} ({percentage}%)\n"
              "✅ To'g'ri: {correct_count}\n"
              "❌ Noto'g'ri: {wrong_count}\n"
              "⭐ Olingan XP: +{xp} XP",
        "en": "🏁 **Quiz Complete!**\n\n"
              "📊 Score: {score}/{total} ({percentage}%)\n"
              "✅ Correct: {correct_count}\n"
              "❌ Incorrect: {wrong_count}\n"
              "⭐ XP Earned: +{xp} XP",
        "ru": "🏁 **Викторина завершена!**\n\n"
              "📊 Результат: {score}/{total} ({percentage}%)\n"
              "✅ Верно: {correct_count}\n"
              "❌ Неверно: {wrong_count}\n"
              "⭐ Получено XP: +{xp} XP",
    },
    "btn_quiz_next": {
        "uz": "Keyingi savol ({next}/{total}) ➡️",
        "en": "Next Question ({next}/{total}) ➡️",
        "ru": "Следующий вопрос ({next}/{total}) ➡️",
    },
    "quiz_question_header": {
        "uz": "Savol",
        "en": "Question",
        "ru": "Вопрос",
    },
    "quiz_options_title": {
        "uz": "Variantlar:",
        "en": "Options:",
        "ru": "Варианты:",
    },
    "quiz_select_answer": {
        "uz": "Javobingizni tanlang:",
        "en": "Select your answer:",
        "ru": "Выберите ответ:",
    },
    "quiz_general_knowledge": {
        "uz": "🌐 Umumiy bilimlar",
        "en": "🌐 General Knowledge",
        "ru": "🌐 Общие знания",
    },
    "quiz_keep_it_up": {
        "uz": "🎓 Ajoyib natija! O'qishda davom eting!",
        "en": "🎓 Keep up the great work!",
        "ru": "🎓 Отличная работа! Продолжайте в том же духе!",
    },
    "achievement_unlocked_notification": {
        "uz": "🏆 Yangi yutuq: {icon} {title} (+{xp} XP)!",
        "en": "🏆 Achievement Unlocked: {icon} {title} (+{xp} XP)!",
        "ru": "🏆 Новое достижение: {icon} {title} (+{xp} XP)!",
    },

    # ------------------ Study Plan ------------------
    "plan_intro": {
        "uz": "📅 **Bugungi o'quv rejasi**\n\n{tasks}\n\nTopshiriq ustiga bosib uni bajarildi deb belgilang.",
        "en": "📅 **Today's Study Plan**\n\n{tasks}\n\nClick a task to mark it as completed.",
        "ru": "📅 **План учебы на сегодня**\n\n{tasks}\n\nНажмите на задачу, чтобы отметить её выполненной.",
    },
    "no_plan_today": {
        "uz": "📅 Bugun uchun reja yo'q. Yangi reja yaratish uchun AI dan foydalanishingiz mumkin.",
        "en": "📅 No study plan for today yet. You can generate one with AI.",
        "ru": "📅 На сегодня плана пока нет. Вы можете сгенерировать его с помощью ИИ.",
    },
    "btn_generate_plan": {
        "uz": "✨ AI Reja tuzish",
        "en": "✨ Generate AI Plan",
        "ru": "✨ Создать план с ИИ",
    },
    "btn_add_task": {
        "uz": "➕ Topshiriq qo'shish",
        "en": "➕ Add Task",
        "ru": "➕ Добавить задачу",
    },
    "task_completed": {
        "uz": "🎉 Topshiriq bajarildi! +{xp} XP",
        "en": "🎉 Task completed! +{xp} XP",
        "ru": "🎉 Задача выполнена! +{xp} XP",
    },

    # ------------------ Goals ------------------
    "goals_title": {
        "uz": "🎯 **Sizning maqsadlaringiz** ({count} ta):",
        "en": "🎯 **Your Goals** ({count}):",
        "ru": "🎯 **Ваши цели** ({count}):",
    },
    "no_goals": {
        "uz": "Sizda hali maqsadlar yo'q. Birinchi maqsadingizni qo'shing!",
        "en": "You don't have any goals yet. Add your first goal!",
        "ru": "У вас пока нет целей. Добавьте свою первую цель!",
    },
    "btn_add_goal": {
        "uz": "➕ Maqsad qo'shish",
        "en": "➕ Add Goal",
        "ru": "➕ Добавить цель",
    },
    "prompt_goal_title": {
        "uz": "Maqsadingiz nomini kiriting (masalan: 'Python asoslarini o'rganish'):",
        "en": "Enter goal title (e.g. 'Learn Python basics'):",
        "ru": "Введите название цели (например: 'Освоить основы Python'):",
    },
    "prompt_goal_deadline": {
        "uz": "Muddatni kiriting (kunlarda, masalan: 30):",
        "en": "Enter deadline in days (e.g. 30):",
        "ru": "Введите срок в днях (например: 30):",
    },
    "goal_created": {
        "uz": "🎯 Maqsad qo'shildi: **{title}** ({days} kun muddat)",
        "en": "🎯 Goal created: **{title}** ({days} days deadline)",
        "ru": "🎯 Цель создана: **{title}** (срок {days} дн.)",
    },
    "goal_completed_msg": {
        "uz": "🏆 Tabriklaymiz! '{title}' maqsadi bajarildi! +{xp} XP",
        "en": "🏆 Congratulations! Goal '{title}' completed! +{xp} XP",
        "ru": "🏆 Поздравляем! Цель '{title}' достигнута! +{xp} XP",
    },

    # ------------------ Progress & Stats ------------------
    "progress_summary": {
        "uz": "📊 **Sizning statistikangiz**\n\n"
              "⏱ Jami o'qish vaqti: {study_time}\n"
              "✅ Bajarilgan topshiriqlar: {tasks_count}\n"
              "📝 Test o'rtacha ko'rsatkichi: {quiz_avg}%\n"
              "🔥 Joriy streak: {streak} kun\n"
              "⭐ Jami XP: {xp}\n"
              "🏅 Daraja: {level}\n\n"
              "📚 **Fanlar bo'yicha rivojlanish:**\n{subject_stats}",
        "en": "📊 **Your Progress**\n\n"
              "⏱ Total study time: {study_time}\n"
              "✅ Completed tasks: {tasks_count}\n"
              "📝 Quiz average: {quiz_avg}%\n"
              "🔥 Current streak: {streak} days\n"
              "⭐ Total XP: {xp}\n"
              "🏅 Level: {level}\n\n"
              "📚 **Subject Breakdown:**\n{subject_stats}",
        "ru": "📊 **Ваш прогресс**\n\n"
              "⏱ Общее время учебы: {study_time}\n"
              "✅ Выполнено задач: {tasks_count}\n"
              "📝 Средний балл викторин: {quiz_avg}%\n"
              "🔥 Текущая серия: {streak} дн.\n"
              "⭐ Всего XP: {xp}\n"
              "🏅 Уровень: {level}\n\n"
              "📚 **По предметам:**\n{subject_stats}",
    },

    # ------------------ Streak ------------------
    "streak_info": {
        "uz": "🔥 **O'quv ketma-ketligi (Streak): {streak} kun!**\n\n"
              "💡 Har kuni kamida bitta dars, test yoki mashg'ulot bajaring va o'z o'rganish odatingizni shakllantiring!\n"
              "Bugungi holat: {today_status}",
        "en": "🔥 **Study Streak: {streak} days!**\n\n"
              "💡 Complete at least one study session, task, or quiz each day to build consistency!\n"
              "Today's status: {today_status}",
        "ru": "🔥 **Серия занятий: {streak} дн.!**\n\n"
              "💡 Занимайтесь каждый день (сессия, задача или тест), чтобы выработать привычку!\n"
              "Статус за сегодня: {today_status}",
    },
    "streak_done_today": {
        "uz": "✅ Bugun dars qilindi!",
        "en": "✅ Studied today!",
        "ru": "✅ Сегодня вы занимались!",
    },
    "streak_pending_today": {
        "uz": "⏳ Bugun hali faollik qilinmadi.",
        "en": "⏳ Not studied yet today.",
        "ru": "⏳ Сегодня занятий еще не было.",
    },

    # ------------------ Focus Mode ------------------
    "focus_menu": {
        "uz": "⏱ **Diqqat rejimi (Pomodoro)**\n\nChalg'imasdan dars qilish vaqtini tanlang:",
        "en": "⏱ **Focus Mode (Pomodoro)**\n\nSelect your study duration:",
        "ru": "⏱ **Режим фокуса (Pomodoro)**\n\nВыберите время для продуктивной учебы:",
    },
    "focus_running": {
        "uz": "⏱ **Diqqat sessiyasi davom etmoqda!**\n\nDavomiyligi: {minutes} daqiqa\nBoshlangan vaqt: {start_time}\n\nO'qishdan chalg'imang!",
        "en": "⏱ **Focus session in progress!**\n\nDuration: {minutes} minutes\nStarted at: {start_time}\n\nStay focused on your studies!",
        "ru": "⏱ **Сессия фокуса активна!**\n\nДлительность: {minutes} минут\nНачало: {start_time}\n\nНе отвлекайтесь!",
    },
    "focus_completed": {
        "uz": "🔔 **Diqqat sessiyasi yakunlandi!**\n\nSiz {minutes} daqiqa mukammal shug'ullandingiz!\n⭐ +{xp} XP qo'shildi!",
        "en": "🔔 **Focus session completed!**\n\nYou studied for {minutes} minutes!\n⭐ +{xp} XP earned!",
        "ru": "🔔 **Сессия фокуса завершена!**\n\nВы продуктивно занимались {minutes} минут!\n⭐ +{xp} XP начислено!",
    },
    "focus_break_alert": {
        "uz": "☕ 5 daqiqa dam oling va chuqur nafas oling!",
        "en": "☕ Take a deep breath and relax for 5 minutes!",
        "ru": "☕ Сделайте перерыв на 5 минут и отдохните!",
    },
    "btn_stop_focus": {
        "uz": "⏹ To'xtatish",
        "en": "⏹ Stop",
        "ru": "⏹ Остановить",
    },

    # ------------------ PDF Learning ------------------
    "pdf_intro": {
        "uz": "📄 **PDF O'rganish**\n\nO'rganmoqchi bo'lgan PDF faylingizni botga yuboring (maksimal 200 MB gacha qo'llab-quvvatlanadi).\nAI uni tahlil qiladi va sizga savollarga javob berish, xulosalash hamda test tuzishda yordam beradi.",
        "en": "📄 **PDF Learning**\n\nSend a PDF file to the bot (supports up to 200 MB).\nAI will process it and help you ask questions, generate summaries, or create quizzes.",
        "ru": "📄 **Обучение по PDF**\n\nОтправьте боту PDF-документ (поддерживается до 200 МБ).\nИИ проанализирует его, поможет с ответами на вопросы, кратким содержанием и созданием тестов.",
    },
    "pdf_downloading": {
        "uz": "⏳ Hujjat yuklab olinmoqda va matn ajratilmoqda...",
        "en": "⏳ Downloading and extracting document text...",
        "ru": "⏳ Загрузка документа и извлечение текста...",
    },
    "pdf_telegram_size_limit": {
        "uz": "⚠️ Telegram Bot API cheklovi: Botlar standart holda 20 MB gacha fayllarni yuklay oladi (tizimda 200 MB gacha ruxsat berilgan). Iltimos, 20 MB gacha bo'lgan PDF fayl yuboring.",
        "en": "⚠️ Telegram Bot API limit: Bots can download files up to 20 MB directly (system supports up to 200 MB). Please send a PDF under 20 MB.",
        "ru": "⚠️ Ограничение Telegram Bot API: Боты могут напрямую загружать файлы до 20 МБ (в системе разрешено до 200 МБ). Пожалуйста, отправьте PDF размером до 20 МБ.",
    },
    "pdf_not_found": {
        "uz": "Hujjat topilmadi.",
        "en": "Document not found.",
        "ru": "Документ не найден.",
    },
    "pdf_deleted": {
        "uz": "Hujjat o'chirildi.",
        "en": "Document deleted.",
        "ru": "Документ удален.",
    },
    "pdf_processed": {
        "uz": "✅ **Hujjat qabul qilindi!**\nFayl: `{filename}` ({pages} sahifa)\n\nEndi nima qilmoqchisiz?",
        "en": "✅ **Document processed!**\nFile: `{filename}` ({pages} pages)\n\nWhat would you like to do?",
        "ru": "✅ **Документ обработан!**\nФайл: `{filename}` ({pages} стр.)\n\nЧто вы хотите сделать?",
    },
    "btn_pdf_summary": {
        "uz": "📝 Xulosa qilish",
        "en": "📝 Summarize",
        "ru": "📝 Резюме",
    },
    "btn_pdf_qa": {
        "uz": "❓ Savol berish",
        "en": "❓ Ask Question",
        "ru": "❓ Задать вопрос",
    },
    "btn_pdf_quiz": {
        "uz": "📝 Test tuzish",
        "en": "📝 Create Quiz",
        "ru": "📝 Создать тест",
    },

    # ------------------ Achievements ------------------
    "achievements_title": {
        "uz": "🏆 **Sizning yutuqlaringiz** ({unlocked}/{total}):\n\n{list}",
        "en": "🏆 **Your Achievements** ({unlocked}/{total}):\n\n{list}",
        "ru": "🏆 **Ваши достижения** ({unlocked}/{total}):\n\n{list}",
    },
    "achievement_unlocked": {
        "uz": "🎉 **Yangi yutuq ochildi!**\n\n{icon} **{title}**\n_{description}_\n⭐ +{xp} XP",
        "en": "🎉 **Achievement Unlocked!**\n\n{icon} **{title}**\n_{description}_\n⭐ +{xp} XP",
        "ru": "🎉 **Достижение разблокировано!**\n\n{icon} **{title}**\n_{description}_\n⭐ +{xp} XP",
    },

    # ------------------ Reminders ------------------
    "reminders_menu": {
        "uz": "⏰ **Eslatmalar**\n\nHolat: {status}\nVaqt: {time} ({timezone})\n\nEslatmani yoqish, o'chirish yoki vaqtini o'zgartirishingiz mumkin:",
        "en": "⏰ **Study Reminders**\n\nStatus: {status}\nTime: {time} ({timezone})\n\nYou can enable, disable, or adjust your reminder time:",
        "ru": "⏰ **Напоминания об учебе**\n\nСтатус: {status}\nВремя: {time} ({timezone})\n\nВы можете включить, выключить или изменить время напоминания:",
    },
    "reminder_alert": {
        "uz": "⏰ **O'qish vaqti keldi!**\nO'quv rejangizni davom ettiring va bugungi streakni saqlab qoling! 📚🔥",
        "en": "⏰ **Time to study!**\nContinue your study plan and maintain your streak today! 📚🔥",
        "ru": "⏰ **Время учиться!**\nПродолжайте план учебы и поддержите сегодняшнюю серию! 📚🔥",
    },

    # ------------------ Referral ------------------
    "referral_title": {
        "uz": "🎁 **Do'stlarni taklif qiling**\n\nSizning taklif havolangiz:\n`{link}`\n\n"
              "👥 Taklif qilingan do'stlar: {count}\n"
              "⭐ Ishlangan XP: +{xp} XP\n\nHar bir taklif qilingan do'st uchun +50 XP beriladi!",
        "en": "🎁 **Invite Friends**\n\nYour referral link:\n`{link}`\n\n"
              "👥 Invited friends: {count}\n"
              "⭐ XP earned: +{xp} XP\n\nEarn +50 XP for each friend who joins!",
        "ru": "🎁 **Пригласите друзей**\n\nВаша реферальная ссылка:\n`{link}`\n\n"
              "👥 Приглашено друзей: {count}\n"
              "⭐ Заработано XP: +{xp} XP\n\nПолучайте +50 XP за каждого приглашенного друга!",
    },

    # ------------------ Leaderboard ------------------
    "leaderboard_title": {
        "uz": "🏆 **Haftalik PesHQadamlar**\n\n{ranking}\n\nSizning o'rningiz: #{user_rank} ({user_xp} XP)",
        "en": "🏆 **Weekly Leaderboard**\n\n{ranking}\n\nYour rank: #{user_rank} ({user_xp} XP)",
        "ru": "🏆 **Еженедельная таблица лидеров**\n\n{ranking}\n\nВаше место: #{user_rank} ({user_xp} XP)",
    },

    # ------------------ Settings ------------------
    "settings_menu": {
        "uz": "⚙️ **Sozlamalar**\n\n🌐 Til: {language}\n🕒 Vaqt mintaqasi: {timezone}\n🎯 Kunlik maqsad: {daily_target} daqiqa\n⏰ Eslatmalar: {reminders_status}",
        "en": "⚙️ **Settings**\n\n🌐 Language: {language}\n🕒 Timezone: {timezone}\n🎯 Daily Target: {daily_target} min\n⏰ Reminders: {reminders_status}",
        "ru": "⚙️ **Настройки**\n\n🌐 Язык: {language}\n🕒 Часовой пояс: {timezone}\n🎯 Цель на день: {daily_target} мин\n⏰ Напоминания: {reminders_status}",
    },
    "btn_change_language": {
        "uz": "🌐 Tilni o'zgartirish",
        "en": "🌐 Change Language",
        "ru": "🌐 Сменить язык",
    },
    "btn_change_timezone": {
        "uz": "🕒 Vaqt mintaqasini o'zgartirish",
        "en": "🕒 Change Timezone",
        "ru": "🕒 Сменить часовой пояс",
    },
    "btn_change_target": {
        "uz": "🎯 Kunlik maqsadni o'zgartirish",
        "en": "🎯 Change Daily Target",
        "ru": "🎯 Изменить цель",
    },
    "btn_enable_reminders": {
        "uz": "🔔 Eslatmalarni yoqish",
        "en": "🔔 Enable Reminders",
        "ru": "🔔 Включить напоминания",
    },
    "btn_disable_reminders": {
        "uz": "🔕 Eslatmalarni o'chirish",
        "en": "🔕 Disable Reminders",
        "ru": "🔕 Отключить напоминания",
    },
    "btn_change_rem_time": {
        "uz": "⏰ Vaqtni o'zgartirish",
        "en": "⏰ Change Time",
        "ru": "⏰ Изменить время",
    },
    "btn_admin_stats": {
        "uz": "📊 Statistika",
        "en": "📊 Statistics",
        "ru": "📊 Статистика",
    },
    "btn_admin_broadcast": {
        "uz": "📢 Xabar yuborish",
        "en": "📢 Broadcast",
        "ru": "📢 Рассылка",
    },
    "btn_admin_ban": {
        "uz": "🚫 Bloklash",
        "en": "🚫 Ban User",
        "ru": "🚫 Заблокировать",
    },
    "btn_admin_unban": {
        "uz": "✅ Blokdan chiqarish",
        "en": "✅ Unban User",
        "ru": "✅ Разблокировать",
    },

    # ------------------ Admin ------------------
    "admin_menu_title": {
        "uz": "🛡 **Admin Panel**\nBoshqaruv bo'limini tanlang:",
        "en": "🛡 **Admin Panel**\nChoose management section:",
        "ru": "🛡 **Панель администратора**\nВыберите раздел:",
    },
    "admin_stats_title": {
        "uz": "📊 **Bot Statistikasi**\n\n"
              "👥 Jami foydalanuvchilar: {total_users}\n"
              "⚡ Faol foydalanuvchilar (7 kun): {active_users}\n"
              "🆕 Yangi (bugun): {new_today}\n"
              "📝 Yechilgan testlar: {quizzes_count}\n"
              "⏱ O'quv sessiyalari: {sessions_count}\n"
              "🤖 AI so'rovlari: {ai_requests}\n"
              "📄 PDF yuklamalari: {pdf_requests}",
        "en": "📊 **Bot Analytics**\n\n"
              "👥 Total Users: {total_users}\n"
              "⚡ Active Users (7d): {active_users}\n"
              "🆕 New Today: {new_today}\n"
              "📝 Completed Quizzes: {quizzes_count}\n"
              "⏱ Study Sessions: {sessions_count}\n"
              "🤖 AI Requests: {ai_requests}\n"
              "📄 PDF Uploads: {pdf_requests}",
        "ru": "📊 **Аналитика бота**\n\n"
              "👥 Всего пользователей: {total_users}\n"
              "⚡ Активных (7 дней): {active_users}\n"
              "🆕 Новых сегодня: {new_today}\n"
              "📝 Пройдено тестов: {quizzes_count}\n"
              "⏱ Учебных сессий: {sessions_count}\n"
              "🤖 Запросов к ИИ: {ai_requests}\n"
              "📄 Обработано PDF: {pdf_requests}",
    },
    "admin_broadcast_prompt": {
        "uz": "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabarni yozing:",
        "en": "Enter the message to broadcast to all users:",
        "ru": "Введите сообщение для рассылки всем пользователям:",
    },
    "admin_broadcast_result": {
        "uz": "📢 Xabar yuborildi!\n✅ Muvaffaqiyatli: {sent}\n❌ Yetib bormadi: {failed}",
        "en": "📢 Broadcast completed!\n✅ Sent: {sent}\n❌ Failed: {failed}",
        "ru": "📢 Рассылка завершена!\n✅ Отправлено: {sent}\n❌ Ошибок: {failed}",
    },
    "choose_lang_title": {
        "uz": "Tilni tanlang / Choose language / Выберите язык:",
        "en": "Choose language / Tilni tanlang / Выберите язык:",
        "ru": "Выберите язык / Choose language / Tilni tanlang:",
    },
    "lang_updated": {
        "uz": "Til muvaffaqiyatli o'zgartirildi: {lang}",
        "en": "Language successfully updated to: {lang}",
        "ru": "Язык успешно изменен на: {lang}",
    },
    "settings_select_target": {
        "uz": "Kunlik o'rganish maqsadingizni tanlang (daqiqa):",
        "en": "Select your daily study target (minutes):",
        "ru": "Выберите ежедневную цель обучения (в минутах):",
    },
    "target_updated": {
        "uz": "Kunlik maqsad {target} daqiqaga o'zgartirildi!",
        "en": "Daily target updated to {target} minutes!",
        "ru": "Дневная цель обновлена на {target} минут!",
    },
    "reminders_enabled_alert": {
        "uz": "Eslatmalar yoqildi!",
        "en": "Reminders enabled!",
        "ru": "Напоминания включены!",
    },
    "reminders_disabled_alert": {
        "uz": "Eslatmalar o'chirildi!",
        "en": "Reminders disabled!",
        "ru": "Напоминания отключены!",
    },
    "settings_change_rem_prompt": {
        "uz": "Kunlik eslatma vaqtini HH:MM formatida yuboring (masalan, 18:00 yoki 09:30):",
        "en": "Enter new daily reminder time in HH:MM format (e.g., 18:00 or 09:30):",
        "ru": "Введите время ежедневного напоминания в формате ЧЧ:ММ (например, 18:00 или 09:30):",
    },
    "time_invalid_format": {
        "uz": "⚠️ Iltimos, vaqtni HH:MM formatida to'g'ri kiriting (masalan, 18:00):",
        "en": "⚠️ Please enter a valid time in HH:MM format (e.g., 18:00):",
        "ru": "⚠️ Пожалуйста, введите корректное время в формате ЧЧ:ММ (например, 18:00):",
    },
    "time_invalid_range": {
        "uz": "⚠️ Soat 0-23, daqiqa esa 0-59 oralig'ida bo'lishi kerak. Qayta urinib ko'ring:",
        "en": "⚠️ Hours must be 0-23 and minutes 0-59. Please try again:",
        "ru": "⚠️ Часы должны быть от 0 до 23, а минуты от 0 до 59. Попробуйте еще раз:",
    },
    "rem_time_saved": {
        "uz": "✅ Kunlik o'quv eslatmasi vaqti {time} ga belgilandi!",
        "en": "✅ Daily study reminder time set to {time}!",
        "ru": "✅ Время ежедневного напоминания установлено на {time}!",
    },
    "plan_goal_prompt": {
        "uz": "Bugungi o'quv maqsadingiz nima?\n(Masalan: 'Fizika midtermga tayyorlanish', 'Python algoritmlarini o'rganish'):",
        "en": "What is your study goal for today?\n(e.g., 'Prepare for English midterm', 'Understand dynamic programming'):",
        "ru": "Какова ваша цель учебы на сегодня?\n(Например: 'Подготовка к зачету по физике', 'Изучение алгоритмов Python'):",
    },
    "plan_generating": {
        "uz": "⚡ AI bilan siz uchun shaxsiy kunlik o'quv rejasi tuzilmoqda...",
        "en": "⚡ Generating your personalized daily study schedule with AI...",
        "ru": "⚡ Составляем ваш персональный учебный план с помощью ИИ...",
    },
    "plan_schedule_intro": {
        "uz": "🎓 Mana sizning bugungi rejangiz! Har bir vazifani bajargach, ustiga bosing.",
        "en": "🎓 Here is your schedule! Tap each task when done.",
        "ru": "🎓 Вот ваш план на сегодня! Нажимайте на задания по мере их выполнения.",
    },
    "plan_task_pending": {
        "uz": "Vazifa kutilmoqda deb belgilandi.",
        "en": "Task marked as pending.",
        "ru": "Задание отмечено как ожидающее.",
    },
    "plan_task_add_prompt": {
        "uz": "Yangi vazifa nomini kiriting:\n(Masalan: '10 ta masala yechish - 30 daqiqa')",
        "en": "Enter task title:\n(e.g., 'Solve 10 algebra problems - 30 min')",
        "ru": "Введите название задания:\n(Например: 'Решить 10 задач по физике - 30 минут')",
    },
    "plan_task_added": {
        "uz": "✅ Vazifa bugungi rejaga qo'shildi!",
        "en": "✅ Task added to today's plan!",
        "ru": "✅ Задание добавлено в план на сегодня!",
    },
    "btn_leaderboard": {
        "uz": "🏆 Yetakchilar jadvali",
        "en": "🏆 View Leaderboard",
        "ru": "🏆 Таблица лидеров",
    },
    "leaderboard_empty": {
        "uz": "Hozircha yetakchilar yo'q.",
        "en": "No rankings yet.",
        "ru": "Пока нет рейтинга.",
    },
    "admin_ban_prompt": {
        "uz": "Bloklash uchun foydalanuvchining Telegram ID sini kiriting:",
        "en": "Enter Telegram ID to ban:",
        "ru": "Введите Telegram ID для блокировки:",
    },
    "admin_unban_prompt": {
        "uz": "Blokdan chiqarish uchun Telegram ID sini kiriting:",
        "en": "Enter Telegram ID to unban:",
        "ru": "Введите Telegram ID для разблокировки:",
    },
    "admin_enter_numeric_id": {
        "uz": "⚠️ Iltimos, faqat raqamlardan iborat Telegram ID kiriting.",
        "en": "⚠️ Please enter a numeric Telegram ID.",
        "ru": "⚠️ Пожалуйста, введите числовой Telegram ID.",
    },
    "admin_user_banned": {
        "uz": "🚫 Foydalanuvchi `{target_id}` bloklandi.",
        "en": "🚫 User `{target_id}` has been suspended.",
        "ru": "🚫 Пользователь `{target_id}` заблокирован.",
    },
    "admin_user_unbanned": {
        "uz": "✅ Foydalanuvchi `{target_id}` blokdan chiqarildi.",
        "en": "✅ User `{target_id}` has been unbanned.",
        "ru": "✅ Пользователь `{target_id}` разблокирован.",
    },
    "admin_user_not_found": {
        "uz": "⚠️ Foydalanuvchi `{target_id}` topilmadi.",
        "en": "⚠️ User `{target_id}` not found.",
        "ru": "⚠️ Пользователь `{target_id}` не найден.",
    },
}


def t(key: str, lang: str | None = None, **kwargs: Any) -> str:
    """Retrieve translated string with formatting placeholders. Fallback to English if not found."""
    language = lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key

    text = entry.get(language) or entry.get(DEFAULT_LANGUAGE) or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
