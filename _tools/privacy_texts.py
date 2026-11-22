# Changes to the PetroGram privacy policy for the Vatani Labs website
# (21 November 2026): new studio contact, account / sync / sign-in, crash
# reports and statistics, in six languages, plus a full Chinese version.
# 22 November 2026: the phone's own backup (Google on Android) includes the
# app's data: section 2 and the summary, in all seven languages.

MAIL_OLD = '<a href="mailto:vatanifardin@gmail.com">vatanifardin@gmail.com</a>'
MAIL_NEW = '<a href="mailto:support@vatanilabs.com">support@vatanilabs.com</a>'
CONTACT = ('<p>Fardin Vatani<br>', '<p>Vatani Labs (Fardin Vatani)<br>')

PRIV = {
'en': dict(
  label6b='English', heading6c='English', semi=';',
  sum_start='We, the developer,', sum_end='(section 6). ',
  summary='Your notes and progress stay on your phone, and in your phone\'s own backup if you have it turned on (section 2). Some optional features send data only when you choose to use them: the quiz scoreboard, where the name you choose and your quiz results are stored with <strong>Google Firebase</strong> and shown to other users (section 6), and an account with sign-in by email, Google or Apple and sync between your phones (sections 6b, 6e, 6f). Anonymous crash reports (<strong>Sentry</strong>) and usage statistics (<strong>PostHog</strong>) help us fix and improve the app; they contain no name, email or anything you type, and you can turn them off in Settings → Privacy (sections 6c, 6d). ',
  replace=[
    ('19 November 2026', '22 November 2026'),
    ("If Android backup is turned on for your phone, Android may include this data in your own Google account backup; we have no access to that backup.", "If Android backup is turned on for your phone, Android includes the app's saved data (your notes, progress and settings and, if you created an account, your sign-in) in your phone's backup in your own Google account. Google stores that backup; we cannot see or access it. The data is restored when you install the app on a new phone. You can turn the backup off in your phone's settings (Settings → Google → Backup; the wording varies by phone); Google then removes the copy under its own rules."),
    ('Developer: Fardin Vatani,', 'Developer: Vatani Labs (Fardin Vatani),'),
    CONTACT, (MAIL_OLD, MAIL_NEW),
    ('The app contains no analytics of its own.', 'Crash reports and statistics are used only to fix and improve the app, never for ads.'),
    ('it is not linked to your email, phone number, or Google or Apple account;', 'it is not linked to your email, phone number, or Google or Apple account unless you create an account (section 6b);'),
    ('<h2>11.', '<p>If you create an account, you can delete it at any time in Settings → Account and check mark → Delete my account; this deletes your email, your scoreboard lines and your synced copy in the cloud. You can turn crash reports and usage statistics off at any time in Settings → Privacy.</p>\n\n  <h2>11.'),
  ],
  sec3='<h2>3.', sec8='<h2>8.',
  bullet3='<li><strong>Account and sync.</strong> Only if you create an account, the app signs in with Google Firebase (by email, Google or Apple) and syncs your data between your phones (sections 6b, 6e, 6f).</li>\n    <li><strong>Crash reports and statistics.</strong> Crash reports go to Sentry unless you turn them off in Settings → Privacy; anonymous usage counts go to PostHog only if you allow it (sections 6c, 6d).</li>',
  bullets8='<li>Google Firebase Authentication and Cloud Firestore: the optional account and sync between phones (sections 6b, 6f);</li>\n    <li>Google Sign-In and Sign in with Apple: optional sign-in (section 6e);</li>\n    <li>Sentry (Functional Software, Inc., EU data region): crash reports (section 6c);</li>\n    <li>PostHog (PostHog Inc., EU Cloud): anonymous usage statistics (section 6d).</li>',
),
'az': dict(
  label6b='Azərbaycanca', heading6c='Azərbaycanca', semi=';',
  sum_start='Biz, tərtibatçı,', sum_end='(6-cı bənd). ',
  summary='Qeydləriniz və irəliləyişiniz telefonunuzda qalır; telefonun öz ehtiyat nüsxəsi aktivdirsə, orada da saxlanılır (2-ci bənd). Bəzi könüllü funksiyalar məlumatı yalnız onlardan istifadə etməyi seçdikdə göndərir: test reytinqi, burada seçdiyiniz ad və test nəticələriniz <strong>Google Firebase</strong>-də saxlanılır və digər istifadəçilərə göstərilir (6-cı bənd), həmçinin e-poçt, Google və ya Apple ilə daxil olunan və telefonlarınız arasında sinxronizasiya edən hesab (6b, 6e, 6f bəndləri). Anonim xəta hesabatları (<strong>Sentry</strong>) və istifadə statistikası (<strong>PostHog</strong>) tətbiqi düzəltməyə və yaxşılaşdırmağa kömək edir; onlarda ad, e-poçt və ya yazdıqlarınız olmur və onları Ayarlar → Məxfilik bölməsində söndürə bilərsiniz (6c, 6d bəndləri). ',
  replace=[
    ('19 noyabr 2026', '22 noyabr 2026'),
    ("Telefonunuzda Android ehtiyat nüsxəsi aktivdirsə, Android bu məlumatı sizin öz Google hesabınızın ehtiyat nüsxəsinə daxil edə bilər; həmin nüsxəyə bizim çıxışımız yoxdur.", "Telefonunuzda Android ehtiyat nüsxəsi aktivdirsə, Android tətbiqin saxladığı məlumatı (qeydləriniz, irəliləyişiniz və ayarlarınız, hesab yaratmısınızsa, həm də hesaba daxil olma məlumatınız) telefonun sizin öz Google hesabınızdakı ehtiyat nüsxəsinə daxil edir. Həmin nüsxəni Google saxlayır; biz onu görə bilmirik və ona çıxışımız yoxdur. Tətbiqi yeni telefona quraşdırdıqda bu məlumat bərpa olunur. Ehtiyat nüsxəsini telefonun ayarlarında söndürə bilərsiniz (Ayarlar → Google → Ehtiyat nüsxəsi; adlar telefondan asılı olaraq fərqlənə bilər); bundan sonra Google nüsxəni öz qaydalarına uyğun olaraq silir."),
    ('Tərtibatçı: Fardin Vatani,', 'Tərtibatçı: Vatani Labs (Fardin Vatani),'),
    CONTACT, (MAIL_OLD, MAIL_NEW),
    ('Tətbiqin öz analitikası yoxdur.', 'Xəta hesabatları və statistika yalnız tətbiqi düzəltmək və yaxşılaşdırmaq üçün istifadə olunur, heç vaxt reklam üçün yox.'),
    ('Google və Apple hesabınızla əlaqələndirilmir;', 'Google və Apple hesabınızla əlaqələndirilmir, hesab yaratmasanız (6b bəndi);'),
    ('<h2>11.', '<p>Hesab yaratsanız, onu istənilən vaxt Ayarlar → Hesab və təsdiq nişanı → Hesabımı sil bölməsində silə bilərsiniz; bu, e-poçtunuzu, reytinq sətirlərinizi və buluddakı sinxron nüsxəni silir. Xəta hesabatlarını və istifadə statistikasını istənilən vaxt Ayarlar → Məxfilik bölməsində söndürə bilərsiniz.</p>\n\n  <h2>11.'),
  ],
  sec3='<h2>3.', sec8='<h2>8.',
  bullet3='<li><strong>Hesab və sinxronizasiya.</strong> Yalnız hesab yaratsanız, tətbiq Google Firebase ilə (e-poçt, Google və ya Apple ilə) daxil olur və məlumatlarınızı telefonlarınız arasında sinxronlaşdırır (6b, 6e, 6f bəndləri).</li>\n    <li><strong>Xəta hesabatları və statistika.</strong> Ayarlar → Məxfilik bölməsində söndürməsəniz, xəta hesabatları Sentry-yə göndərilir; anonim istifadə sayları isə yalnız icazə versəniz PostHog-a göndərilir (6c, 6d bəndləri).</li>',
  bullets8='<li>Google Firebase Authentication və Cloud Firestore: könüllü hesab və telefonlar arasında sinxronizasiya (6b, 6f bəndləri);</li>\n    <li>Google Sign-In və Sign in with Apple: könüllü daxil olma (6e bəndi);</li>\n    <li>Sentry (Functional Software, Inc., AB məlumat regionu): xəta hesabatları (6c bəndi);</li>\n    <li>PostHog (PostHog Inc., EU Cloud): anonim istifadə statistikası (6d bəndi).</li>',
),
'ru': dict(
  label6b='Русский', heading6c='Русский', semi=';',
  sum_start='Мы, разработчик,', sum_end='(раздел 6). ',
  summary='Ваши заметки и прогресс остаются на телефоне, а если включено резервное копирование телефона, то и в его резервной копии (раздел 2). Некоторые необязательные функции отправляют данные, только если вы решите ими пользоваться: рейтинг тестов, где выбранное вами имя и результаты хранятся в <strong>Google Firebase</strong> и видны другим пользователям (раздел 6), а также аккаунт со входом по почте, через Google или Apple и синхронизацией между вашими телефонами (разделы 6b, 6e, 6f). Анонимные отчёты о сбоях (<strong>Sentry</strong>) и статистика использования (<strong>PostHog</strong>) помогают нам исправлять и улучшать приложение; в них нет имени, почты или того, что вы вводите, и их можно отключить в разделе Настройки → Конфиденциальность (разделы 6c, 6d). ',
  replace=[
    ('19 ноября 2026 г.', '22 ноября 2026 г.'),
    ("Если на телефоне включено резервное копирование Android, система может включить эти данные в резервную копию вашего собственного аккаунта Google; у нас нет доступа к этой копии.", "Если на телефоне включено резервное копирование Android, система включает сохранённые данные приложения (заметки, прогресс и настройки, а если вы создали аккаунт, то и вход в него) в резервную копию телефона в вашем собственном аккаунте Google. Эту копию хранит Google; мы не видим её и не имеем к ней доступа. Данные восстанавливаются, когда вы устанавливаете приложение на новый телефон. Резервное копирование можно отключить в настройках телефона (Настройки → Google → Резервное копирование; названия зависят от телефона); после этого Google удаляет копию по своим правилам."),
    ('Разработчик: Fardin Vatani,', 'Разработчик: Vatani Labs (Fardin Vatani),'),
    CONTACT, (MAIL_OLD, MAIL_NEW),
    ('Собственной аналитики в приложении нет.', 'Отчёты о сбоях и статистика используются только для исправления и улучшения приложения, но не для рекламы.'),
    ('или аккаунтом Google или Apple;', 'или аккаунтом Google или Apple, если вы не создадите аккаунт (раздел 6b);'),
    ('<h2>11.', '<p>Если вы создали аккаунт, его можно удалить в любой момент: Настройки → Аккаунт и галочка → Удалить аккаунт; при этом удаляются ваша почта, строки в рейтинге и синхронизированная копия в облаке. Отчёты о сбоях и статистику использования можно в любой момент отключить в разделе Настройки → Конфиденциальность.</p>\n\n  <h2>11.'),
  ],
  sec3='<h2>3.', sec8='<h2>8.',
  bullet3='<li><strong>Аккаунт и синхронизация.</strong> Только если вы создадите аккаунт, приложение выполняет вход через Google Firebase (по почте, через Google или Apple) и синхронизирует ваши данные между телефонами (разделы 6b, 6e, 6f).</li>\n    <li><strong>Отчёты о сбоях и статистика.</strong> Отчёты о сбоях отправляются в Sentry, если вы не отключите их в разделе Настройки → Конфиденциальность; анонимные счётчики использования отправляются в PostHog, только если вы это разрешите (разделы 6c, 6d).</li>',
  bullets8='<li>Google Firebase Authentication и Cloud Firestore: необязательный аккаунт и синхронизация между телефонами (разделы 6b, 6f);</li>\n    <li>Google Sign-In и Sign in with Apple: необязательный вход (раздел 6e);</li>\n    <li>Sentry (Functional Software, Inc., регион данных ЕС): отчёты о сбоях (раздел 6c);</li>\n    <li>PostHog (PostHog Inc., EU Cloud): анонимная статистика использования (раздел 6d).</li>',
),
'ar': dict(
  label6b='العربية', heading6c='العربية', semi='؛',
  sum_start='نحن، المطوّر،', sum_end='(البند 6). ',
  summary='تبقى ملاحظاتك وتقدّمك على هاتفك، وكذلك في النسخة الاحتياطية الخاصة بهاتفك إذا كان النسخ الاحتياطي مفعّلًا (البند 2). بعض الميزات الاختيارية لا ترسل بيانات إلا إذا اخترت استخدامها: لوحة متصدري الاختبارات، حيث يُخزَّن الاسم الذي تختاره ونتائج اختباراتك لدى <strong>Google Firebase</strong> ويظهران للمستخدمين الآخرين (البند 6)، والحساب مع تسجيل الدخول بالبريد الإلكتروني أو Google أو Apple والمزامنة بين هواتفك (البنود 6ب و6هـ و6و). وتساعدنا تقارير الأعطال المجهولة (<strong>Sentry</strong>) وإحصاءات الاستخدام (<strong>PostHog</strong>) على إصلاح التطبيق وتحسينه؛ فهي لا تحتوي على اسم أو بريد إلكتروني أو أي شيء تكتبه، ويمكنك إيقافها من الإعدادات ← الخصوصية (البندان 6ج و6د). ',
  replace=[
    ('19 نوفمبر 2026', '22 نوفمبر 2026'),
    ("إذا كان النسخ الاحتياطي في Android مفعّلًا على هاتفك، فقد يضمّن Android هذه البيانات في النسخة الاحتياطية لحسابك الخاص على Google، ولا يمكننا الوصول إلى تلك النسخة.", "إذا كان النسخ الاحتياطي في Android مفعّلًا على هاتفك، فإن Android يضمّن بيانات التطبيق المحفوظة (ملاحظاتك وتقدّمك وإعداداتك، وكذلك تسجيل دخولك إذا أنشأت حسابًا) في النسخة الاحتياطية لهاتفك في حسابك الخاص على Google. تحتفظ Google بهذه النسخة، ولا يمكننا رؤيتها أو الوصول إليها. وتُستعاد البيانات عند تثبيت التطبيق على هاتف جديد. يمكنك إيقاف النسخ الاحتياطي من إعدادات هاتفك (الإعدادات ← Google ← النسخ الاحتياطي؛ وقد تختلف التسميات من هاتف إلى آخر)، وبعد ذلك تحذف Google النسخة وفق قواعدها."),
    ('المطوّر: Fardin Vatani،', 'المطوّر: Vatani Labs (Fardin Vatani)،'),
    CONTACT, (MAIL_OLD, MAIL_NEW),
    ('ولا يحتوي التطبيق على أدوات تحليل خاصة به.', 'وتُستخدم تقارير الأعطال والإحصاءات فقط لإصلاح التطبيق وتحسينه، وليس للإعلانات أبدًا.'),
    ('أو حسابك في Google أو Apple؛', 'أو حسابك في Google أو Apple، ما لم تنشئ حسابًا (البند 6ب)؛'),
    ('<h2>11.', '<p>إذا أنشأت حسابًا، يمكنك حذفه في أي وقت من الإعدادات ← الحساب وعلامة التوثيق ← احذف حسابي؛ ويؤدي ذلك إلى حذف بريدك وأسطرك في لوحة المتصدرين ونسختك المتزامنة في السحابة. ويمكنك إيقاف تقارير الأعطال وإحصاءات الاستخدام في أي وقت من الإعدادات ← الخصوصية.</p>\n\n  <h2>11.'),
  ],
  sec3='<h2>3.', sec8='<h2>8.',
  bullet3='<li><strong>الحساب والمزامنة.</strong> فقط إذا أنشأت حسابًا، يسجّل التطبيق الدخول عبر Google Firebase (بالبريد الإلكتروني أو Google أو Apple) ويزامن بياناتك بين هواتفك (البنود 6ب و6هـ و6و).</li>\n    <li><strong>تقارير الأعطال والإحصاءات.</strong> تُرسَل تقارير الأعطال إلى Sentry ما لم توقفها من الإعدادات ← الخصوصية؛ أما أعداد الاستخدام المجهولة فلا تُرسَل إلى PostHog إلا إذا سمحت بذلك (البندان 6ج و6د).</li>',
  bullets8='<li>Google Firebase Authentication وCloud Firestore: الحساب الاختياري والمزامنة بين الهواتف (البندان 6ب و6و)؛</li>\n    <li>Google Sign-In وSign in with Apple: تسجيل الدخول الاختياري (البند 6هـ)؛</li>\n    <li>Sentry (من Functional Software, Inc.، منطقة بيانات الاتحاد الأوروبي): تقارير الأعطال (البند 6ج)؛</li>\n    <li>PostHog (من PostHog Inc.، EU Cloud): إحصاءات استخدام مجهولة الهوية (البند 6د).</li>',
),
'es': dict(
  label6b='Español', heading6c='Español', semi=';',
  sum_start='Nosotros, el desarrollador,', sum_end='(sección 6). ',
  summary='Tus notas y tu progreso se quedan en tu teléfono y, si la tienes activada, en la copia de seguridad del propio teléfono (sección 2). Algunas funciones opcionales envían datos solo si decides usarlas: la clasificación de tests, donde el nombre que elijas y tus resultados se guardan en <strong>Google Firebase</strong> y se muestran a otros usuarios (sección 6), y una cuenta con inicio de sesión por correo, Google o Apple y sincronización entre tus teléfonos (secciones 6b, 6e, 6f). Los informes de fallos anónimos (<strong>Sentry</strong>) y las estadísticas de uso (<strong>PostHog</strong>) nos ayudan a corregir y mejorar la app; no contienen nombre, correo ni nada de lo que escribes, y puedes desactivarlos en Ajustes → Privacidad (secciones 6c, 6d). ',
  replace=[
    ('19 de noviembre de 2026', '22 de noviembre de 2026'),
    ("Si la copia de seguridad de Android está activada en tu teléfono, Android puede incluir estos datos en la copia de seguridad de tu propia cuenta de Google; no tenemos acceso a esa copia.", "Si la copia de seguridad de Android está activada en tu teléfono, Android incluye los datos guardados de la aplicación (tus notas, tu progreso y tus ajustes y, si has creado una cuenta, tu inicio de sesión) en la copia de seguridad del teléfono, en tu propia cuenta de Google. Google guarda esa copia; no podemos verla ni acceder a ella. Los datos se restauran cuando instalas la aplicación en un teléfono nuevo. Puedes desactivar la copia de seguridad en los ajustes del teléfono (Ajustes → Google → Copia de seguridad; los nombres varían según el teléfono); después, Google elimina la copia según sus propias normas."),
    ('Desarrollador: Fardin Vatani,', 'Desarrollador: Vatani Labs (Fardin Vatani),'),
    CONTACT, (MAIL_OLD, MAIL_NEW),
    ('La aplicación no tiene analíticas propias.', 'Los informes de fallos y las estadísticas solo se usan para corregir y mejorar la app, nunca para publicidad.'),
    ('ni tu cuenta de Google o Apple;', 'ni tu cuenta de Google o Apple, salvo que crees una cuenta (sección 6b);'),
    ('<h2>11.', '<p>Si creas una cuenta, puedes eliminarla en cualquier momento en Ajustes → Cuenta e insignia → Eliminar mi cuenta; así se borran tu correo, tus líneas en la clasificación y tu copia sincronizada en la nube. Puedes desactivar los informes de fallos y las estadísticas de uso en cualquier momento en Ajustes → Privacidad.</p>\n\n  <h2>11.'),
  ],
  sec3='<h2>3.', sec8='<h2>8.',
  bullet3='<li><strong>Cuenta y sincronización.</strong> Solo si creas una cuenta, la app inicia sesión con Google Firebase (por correo, Google o Apple) y sincroniza tus datos entre tus teléfonos (secciones 6b, 6e, 6f).</li>\n    <li><strong>Informes de fallos y estadísticas.</strong> Los informes de fallos se envían a Sentry salvo que los desactives en Ajustes → Privacidad; los recuentos de uso anónimos se envían a PostHog solo si lo permites (secciones 6c, 6d).</li>',
  bullets8='<li>Google Firebase Authentication y Cloud Firestore: la cuenta opcional y la sincronización entre teléfonos (secciones 6b, 6f);</li>\n    <li>Google Sign-In e Iniciar sesión con Apple: el inicio de sesión opcional (sección 6e);</li>\n    <li>Sentry (Functional Software, Inc., región de datos de la UE): informes de fallos (sección 6c);</li>\n    <li>PostHog (PostHog Inc., EU Cloud): estadísticas de uso anónimas (sección 6d).</li>',
),
'fr': dict(
  label6b='Français', heading6c='Français', semi=' ;',
  sum_start='Nous, le développeur,', sum_end='(section 6). ',
  summary='Vos notes et vos progrès restent sur votre téléphone, ainsi que dans la sauvegarde de votre téléphone si elle est activée (section 2). Certaines fonctions facultatives n’envoient des données que si vous choisissez de les utiliser : le classement des quiz, où le nom que vous choisissez et vos résultats sont enregistrés chez <strong>Google Firebase</strong> et affichés aux autres utilisateurs (section 6), et un compte avec connexion par e-mail, Google ou Apple et synchronisation entre vos téléphones (sections 6b, 6e, 6f). Les rapports de plantage anonymes (<strong>Sentry</strong>) et les statistiques d’utilisation (<strong>PostHog</strong>) nous aident à corriger et à améliorer l’app ; ils ne contiennent ni nom, ni e-mail, ni rien de ce que vous saisissez, et vous pouvez les désactiver dans Paramètres → Confidentialité (sections 6c, 6d). ',
  replace=[
    ('19 novembre 2026', '22 novembre 2026'),
    ("Si la sauvegarde Android est activée sur votre téléphone, Android peut inclure ces données dans la sauvegarde de votre propre compte Google ; nous n’avons pas accès à cette sauvegarde.", "Si la sauvegarde Android est activée sur votre téléphone, Android inclut les données enregistrées par l’application (vos notes, votre progression et vos réglages et, si vous avez créé un compte, votre connexion à ce compte) dans la sauvegarde du téléphone, sur votre propre compte Google. Google conserve cette sauvegarde ; nous ne pouvons ni la voir ni y accéder. Les données sont restaurées lorsque vous installez l’application sur un nouveau téléphone. Vous pouvez désactiver la sauvegarde dans les paramètres du téléphone (Paramètres → Google → Sauvegarde ; les intitulés varient selon le téléphone) ; Google supprime ensuite la copie selon ses propres règles."),
    ('Développeur : Fardin Vatani,', 'Développeur : Vatani Labs (Fardin Vatani),'),
    CONTACT, (MAIL_OLD, MAIL_NEW),
    ('L’application ne contient aucun outil d’analyse propre.', 'Les rapports de plantage et les statistiques servent uniquement à corriger et à améliorer l’app, jamais à la publicité.'),
    ('ni à votre compte Google ou Apple ;', 'ni à votre compte Google ou Apple, sauf si vous créez un compte (section 6b) ;'),
    ('<h2>11.', '<p>Si vous créez un compte, vous pouvez le supprimer à tout moment dans Paramètres → Compte et badge → Supprimer mon compte ; cela efface votre e-mail, vos lignes au classement et votre copie synchronisée dans le cloud. Vous pouvez désactiver les rapports de plantage et les statistiques d’utilisation à tout moment dans Paramètres → Confidentialité.</p>\n\n  <h2>11.'),
  ],
  sec3='<h2>3.', sec8='<h2>8.',
  bullet3='<li><strong>Compte et synchronisation.</strong> Seulement si vous créez un compte, l’app se connecte via Google Firebase (par e-mail, Google ou Apple) et synchronise vos données entre vos téléphones (sections 6b, 6e, 6f).</li>\n    <li><strong>Rapports de plantage et statistiques.</strong> Les rapports de plantage sont envoyés à Sentry sauf si vous les désactivez dans Paramètres → Confidentialité ; les comptages d’utilisation anonymes ne sont envoyés à PostHog que si vous l’autorisez (sections 6c, 6d).</li>',
  bullets8='<li>Google Firebase Authentication et Cloud Firestore : le compte facultatif et la synchronisation entre téléphones (sections 6b, 6f) ;</li>\n    <li>Google Sign-In et Se connecter avec Apple : la connexion facultative (section 6e) ;</li>\n    <li>Sentry (Functional Software, Inc., région de données UE) : rapports de plantage (section 6c) ;</li>\n    <li>PostHog (PostHog Inc., EU Cloud) : statistiques d’utilisation anonymes (section 6d).</li>',
),
}

ZH_SECTION = '''<section id="zh" lang="zh-Hans">
  <h1>PetroGram 隐私政策</h1>
  <p class="meta">生效日期：2026 年 11 月 22 日<br>
  开发者：Vatani Labs（Fardin Vatani），阿塞拜疆巴库</p>

  <h2>1. 概要</h2>
  <p>PetroGram 是一款面向石油天然气行业的参考与学习应用，支持 Android 和 iPhone。您的笔记和学习进度保存在您的手机上；如果您开启了手机自带的备份，备份中也会有一份（见第 2 节）。部分可选功能只有在您选择使用时才会发送数据：测验排行榜（您选择的名称和测验成绩保存在 <strong>Google Firebase</strong> 中，并向其他用户显示，见第 6 节），以及可通过电子邮件、Google 或 Apple 登录并在您的手机之间同步的账号（见第 6b、6e、6f 节）。匿名崩溃报告（<strong>Sentry</strong>）和使用统计（<strong>PostHog</strong>）帮助我们修复和改进应用；其中不含姓名、电子邮件或您输入的任何内容，您可以在“设置 → 隐私”中关闭它们（见第 6c、6d 节）。<strong>Google AdMob</strong> 向未购买“去除广告”的用户显示横幅广告；AdMob 可能为这些广告收集设备数据，在法律要求时会先征得您的同意；在 iPhone 上，只有在您允许跟踪时才会使用 Apple 的广告标识符。<strong>Google Play</strong>（Android）和 <strong>App Store</strong>（iPhone）处理可选的一次性“去除广告”购买。“市场”页面会从美国能源信息署（EIA）下载公开的价格数据。</p>

  <h2>2. 保存在您设备上的信息</h2>
  <p>应用会在手机的本地存储中保存以下内容：</p>
  <ul>
    <li>您的设置：语言、浅色或深色主题、提醒时间、振动、学习目标和领域，以及信息栏选项；</li>
    <li>您收藏的术语、最近的搜索，以及您在“我的笔记”中写下的笔记；</li>
    <li>您的学习进度：闪卡、测验成绩、待复习的错题、徽章和最近的活动；</li>
    <li>“市场”页面最近下载的价格，以便在没有网络时显示；</li>
    <li>您是否已购买“去除广告”，以便离线时也不显示广告；</li>
    <li>您的广告同意选择，由 Google 的同意工具保存（见第 4 节）；</li>
    <li>如果您加入了排行榜：您的随机用户 ID、您选择的名称、尚未发送的成绩以及您选择隐藏的人（见第 6 节）。</li>
  </ul>
  <p>这些信息保存在您的设备上，不会发送给我们。我们看不到您的笔记或进度（除非您创建账号并使用同步，见第 6f 节）。当您在应用中删除这些信息、清除应用数据或卸载应用时，它们会被删除。您导出的备份文件只会保存或分享到您选择的位置。如果您的手机开启了 Android 备份，Android 会将应用保存的数据（您的笔记、学习进度和设置；如果您创建了账号，还包括登录状态）包含在手机备份中，保存在您自己的 Google 账号里。该备份由 Google 保存，我们无法查看或访问。当您在新手机上安装应用时，这些数据会被恢复。您可以在手机设置中关闭备份（设置 → Google → 备份；不同手机上的名称可能不同）；关闭后，Google 会按其自身规则删除该备份。在 iPhone 上，iOS 可能会将这些数据包含在您自己的 iCloud 或电脑备份中；我们同样无法访问。</p>

  <h2>3. 网络使用</h2>
  <ul>
    <li><strong>市场价格。</strong>当您打开“市场”页面时，应用会从 api.eia.gov 下载 EIA 的公开价格数据。请求中只包含所需的价格列表和应用的访问密钥，不含任何个人数据或您输入的内容。与任何网络连接一样，EIA 的服务器会收到您设备的 IP 地址；EIA 依据其在 eia.gov 上公布的隐私政策处理该地址。</li>
    <li><strong>广告。</strong>如果您没有购买“去除广告”，应用会连接 Google 以显示广告（见第 4 节）。</li>
    <li><strong>Google Play 和 App Store。</strong>应用会向 Google Play（Android）或 App Store（iPhone）查询“去除广告”的价格以及您是否已拥有它（见第 5 节）。</li>
    <li><strong>排行榜。</strong>只有在您加入可选的排行榜时，应用才会将您选择的名称和测验成绩发送到 Google Firebase，并加载排行榜（见第 6 节）。</li>
    <li><strong>账号和同步。</strong>只有在您创建账号时，应用才会通过 Google Firebase 登录（使用电子邮件、Google 或 Apple），并在您的手机之间同步数据（见第 6b、6e、6f 节）。</li>
    <li><strong>崩溃报告和统计。</strong>崩溃报告会发送到 Sentry，除非您在“设置 → 隐私”中关闭；匿名使用计数只有在您允许后才会发送到 PostHog（见第 6c、6d 节）。</li>
  </ul>
  <p>其他所有功能无需联网即可使用；离线时不会显示广告。如果您点击“联系”“报告问题”“拨打电话”或“隐私政策”，应用会转到您手机上的其他应用（邮件、电话或浏览器）。这些应用有各自的隐私做法。</p>

  <h2>4. 广告（Google AdMob）</h2>
  <p>未购买“去除广告”的用户会在顶部栏下方看到由 Google AdMob（Google LLC；在欧洲经济区、英国和瑞士为 Google Ireland Limited）提供的横幅广告。为了展示、衡量广告并防止欺诈，应用中的 AdMob 软件可能会收集以下数据并发送给 Google：</p>
  <ul>
    <li>设备标识符，例如 Android 广告 ID；在 iPhone 上，如果您允许跟踪，则为 Apple 的广告标识符（IDFA）；</li>
    <li>IP 地址及据此推断的大致位置；</li>
    <li>设备和应用信息，例如型号、操作系统、语言和应用版本；</li>
    <li>广告互动，例如浏览和点击的广告，以及诊断数据。</li>
  </ul>
  <p>在欧洲经济区、英国和瑞士，应用会在加载任何广告之前显示 Google 的同意表单。您可以选择 Google 是否可以使用您的数据投放个性化广告，并可随时在<strong>设置 → 广告 → 隐私和广告设置</strong>中更改选择。在未获同意的情况下，Google 仍可能显示非个性化或有限广告，这类广告会为频次控制、效果衡量和防止欺诈等目的使用数据。您也可以在手机的 Android 设置（Google → 广告）中重置或删除广告 ID。</p>
  <p>在 iPhone 上，应用随后会显示 Apple 的“允许跟踪？”提示。如果您选择“要求 App 不跟踪”，Apple 的广告标识符不会与 Google 共享。您可以随时在 iPhone 的<strong>设置 → 隐私与安全性 → 跟踪</strong>中更改。</p>
  <p>Google 依据其自身政策处理这些数据：<a href="https://policies.google.com/privacy">policies.google.com/privacy</a> 和 <a href="https://policies.google.com/technologies/partner-sites">policies.google.com/technologies/partner-sites</a>。我们不会收到关于您的这些数据；AdMob 只向我们提供汇总数据，例如广告展示次数和收入。</p>
  <p>您写的笔记、学习进度以及您在应用中输入的任何内容都不会与 AdMob 共享。</p>

  <h2>5. “去除广告”购买（Google Play 和 App Store）</h2>
  <p>“去除广告”是一项可选的一次性购买。在 Android 上通过 Google Play 结算完成：Google 依据 Google Play 条款和 Google 隐私政策处理付款，并向我们提供每笔订单的记录，例如订单号、日期、产品、价格和国家/地区，我们仅用其管理购买，例如处理退款。在 iPhone 上通过 Apple 的 App Store 完成：Apple 依据其自身条款和隐私政策处理付款，只向我们提供销售报告，不提供您的姓名或联系方式。我们绝不会收到您的银行卡或付款信息。应用只在您的手机上保存是否已去除广告，并向 Google Play 或 App Store 核实购买是否仍然有效。</p>

  <h2>6. 测验排行榜（可选）</h2>
  <p>“测验”标签页中有一个可选的全球排行榜。除非您点击“加入排行榜”，否则不会发送任何内容，且无需电子邮件地址、电话号码或密码。加入后，应用会使用 Google Firebase（Firebase Authentication 和 Cloud Firestore，由 Google LLC 提供）保存：</p>
  <ul>
    <li>Firebase 为您安装的应用创建的随机用户 ID（匿名登录）；除非您创建账号（见第 6b 节），它不会与您的电子邮件、电话号码或 Google、Apple 账号关联；</li>
    <li>您选择显示的名称：您的名字和姓氏，或仅首字母，由您决定。<strong>所有使用 PetroGram 的人都能看到这个名称；</strong></li>
    <li>您加入后的测验成绩：今天、本周和全部时间的积分与用时、答对的题数，以及最后更新时间；</li>
    <li>如果您举报某个名称：您举报的名称和您的随机用户 ID，以便我们审核。</li>
  </ul>
  <p>您的成绩会先保存在手机上，联网时再发送。与任何网络连接一样，Google 的服务器会收到您设备的 IP 地址。您的笔记、闪卡和其他输入内容永远不会被发送，您隐藏的人只记录在您的手机上。我们仅将这些数据用于运行排行榜和删除违反规则的名称。它们不会用于广告，AdMob 也不会收到。</p>
  <p>您可以随时更改名称，也可以通过排行榜菜单中的<strong>退出排行榜</strong>离开：您的名称和成绩会立即从排行榜服务器中删除。如果您未退出就卸载了应用，您的条目会一直保留，直到您要求我们删除（见第 12 节）。我们处理这些数据是因为您选择加入（您的同意）；您可以随时通过退出来撤回同意。Google 作为我们的服务提供商代表我们处理这些数据，其服务器可能位于您所在国家/地区以外，包括美国。详见 <a href="https://firebase.google.com/support/privacy">firebase.google.com/support/privacy</a>。</p>

  <h2>6b. 可选账号</h2>
  <p>如果您创建账号，我们会保存您的电子邮件地址和密码（由 Google Firebase Authentication 以我们无法读取的形式保存）。它们仅用于让您登录、确认该地址属于您，以及在该地址属于公司时，在您的排行榜名称旁显示蓝色认证标记。您的电子邮件绝不会显示给其他用户。您可以随时在“设置 → 账号与认证标记 → 删除我的账号”中删除账号；这会删除电子邮件、密码以及您在排行榜中的记录。</p>

  {BLOCKS6CF}

  <h2>7. 您发给我们的邮件</h2>
  <p>如果您向我们发送报告或消息，我们会收到您发送的内容：您的电子邮件地址、消息、您附上的截图，以及邮件模板中包含的应用版本、语言和页面名称。我们仅将其用于回复您和修复问题。我们不会出售或与第三方共享这些内容，并会在不再需要时删除。</p>

  <h2>8. 第三方服务</h2>
  <ul>
    <li>美国能源信息署（EIA）：公开价格数据（见第 3 节）；</li>
    <li>Google AdMob，包括 Google 的同意工具（User Messaging Platform）：广告（见第 4 节）；</li>
    <li>Google Firebase（Authentication 和 Cloud Firestore）：可选的排行榜、账号以及手机之间的同步（见第 6、6b、6f 节）；</li>
    <li>Google Play 结算（Android）和 Apple 的 App Store（iPhone）：“去除广告”购买（见第 5 节）；</li>
    <li>Google Sign-In 和“通过 Apple 登录”：可选登录（见第 6e 节）；</li>
    <li>Sentry（Functional Software, Inc.，欧盟数据区域）：崩溃报告（见第 6c 节）；</li>
    <li>PostHog（PostHog Inc.，EU Cloud）：匿名使用统计（见第 6d 节）。</li>
  </ul>
  <p>我们不出售个人数据。崩溃报告和统计仅用于修复和改进应用，绝不用于广告。</p>

  <h2>9. 儿童</h2>
  <p>本应用面向石油天然气行业的从业人员和学生，不针对 13 岁以下的儿童。我们不会在知情的情况下收集儿童的个人数据。</p>

  <h2>10. 您的权利</h2>
  <p>通过应用，我们只在您加入排行榜或创建账号时持有您的个人数据：您选择的名称、成绩和随机用户 ID（见第 6 节），以及账号的电子邮件和同步副本（见第 6b、6f 节）。您可以在应用中查看并更改名称，通过“退出排行榜”立即删除排行榜数据，也可以写信给我们要求访问或删除。如果您创建了账号，可以随时在“设置 → 账号与认证标记 → 删除我的账号”中删除；这会删除您的电子邮件、排行榜记录以及云端的同步副本。您可以随时在“设置 → 隐私”中关闭崩溃报告和使用统计。设备上的数据由您掌控，可随时删除。您可以在“设置 → 广告 → 隐私和广告设置”中更改广告同意，在 Android 设置中重置广告 ID，在 iPhone 的“设置 → 隐私与安全性 → 跟踪”中更改跟踪权限，或通过购买“去除广告”停止所有广告。对于 Google 或 Apple 处理的数据，请参阅它们的隐私政策，其中说明了如何向它们行使您的权利。您也可以联系我们，要求删除您发给我们的任何邮件。如果您居住在欧洲经济区或英国，还可以向您所在地的数据保护机构投诉。</p>

  <h2>11. 变更</h2>
  <p>我们可能会更新本政策。顶部的生效日期表示最后一次更改的时间。</p>

  <h2>12. 联系方式</h2>
  <p>Vatani Labs（Fardin Vatani）<br>
  电子邮件：<a href="mailto:support@vatanilabs.com">support@vatanilabs.com</a><br>
  电话：+994 70 294 19 98</p>
</section>'''
