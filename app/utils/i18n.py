"""Internationalization (i18n) module supporting Uzbek, English, and Russian."""

from typing import Any

SUPPORTED_LANGUAGES = {
    "uz": "🇺🇿 O'zbekcha",
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
}

DEFAULT_LANGUAGE = "en"

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ------------------ Navigation & Common ------------------
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

    # ------------------ AI Assistant ------------------
    "ai_assistant_intro": {
        "uz": "🤖 **AI Yordamchi**\n\nSavolingizni yozing yoki amal tanlang:\n• Tushuntirish\n• Xulosa qilish\n• Misollar keltirish\n• Qadam-baqadam yechim\n• O'quv konspekti tuzish",
        "en": "🤖 **AI Assistant**\n\nAsk any question or pick an action:\n• Explain concepts\n• Summarize texts\n• Provide examples\n• Step-by-step guidance\n• Create study notes",
        "ru": "🤖 **ИИ Помощник**\n\nЗадайте вопрос или выберите действие:\n• Объяснить concept\n• Составить конспект\n• Привести примеры\n• Пошаговое объяснение\n• Сделать резюме",
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
    "btn_stop_focus": {
        "uz": "⏹ To'xtatish",
        "en": "⏹ Stop",
        "ru": "⏹ Остановить",
    },

    # ------------------ PDF Learning ------------------
    "pdf_intro": {
        "uz": "📄 **PDF O'rganish**\n\nO'rganmoqchi bo'lgan PDF faylingizni botga yuboring (maksimal 10 MB).\nAI uni tahlil qiladi va sizga savollarga javob berish, xulosalash hamda test tuzishda yordam beradi.",
        "en": "📄 **PDF Learning**\n\nSend a PDF file to the bot (max 10 MB).\nAI will process it and help you ask questions, generate summaries, or create quizzes.",
        "ru": "📄 **Обучение по PDF**\n\nОтправьте боту PDF-документ (до 10 МБ).\nИИ проанализирует его, поможет с ответами на вопросы, кратким содержанием и созданием тестов.",
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
