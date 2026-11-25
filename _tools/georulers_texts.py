# Geo-Rulers (25 November 2026): its privacy policy and its page for deleting
# an account, /geo-rulers/privacy/ and /geo-rulers/delete-account/.
#
# Geo-Rulers is a sister app of PetroGram with the same code and the same
# kinds of outside services, so its two pages are PetroGram's pages with:
#   - the name of the app and the date;
#   - sections 6b to 6g read from the Geo-Rulers app folder
#     (docs/ACCOUNT_SETUP.md part 3 and docs/PRIVACY_ADDITIONS.md);
#   - the differences listed here, in all seven languages.
#
# What differs from PetroGram's policy, and why:
#   - what the app is about (geology and mining, not oil and gas): sections 1, 9;
#   - prices: no EIA. The app downloads one small file of monthly metal and
#     mineral prices from this website (GitHub Pages) about once a week:
#     sections 1, 3 and 8;
#   - the update check (Firebase Remote Config at every start) is named:
#     sections 1, 3 and 8. PetroGram's policy does not name it yet;
#   - section 2 says plainly that the data on the phone is sent when the
#     optional scoreboard or sync is used.
#
# build.py runs this file after delete_texts.py. Every pair below is
# (PetroGram's text with the name already changed, Geo-Rulers' text); the
# build stops if a text is not found exactly once, so a change in PetroGram's
# policy cannot silently break this one.

GEO_NAME = 'Geo-Rulers'    # the name people see (with a hyphen)
GEO_APP = 'geo-rulers'     # the app's folder on the site
GEO_DAY = 25               # November 2026: the date of both pages

# How each language writes a date of November 2026.
GEO_DATE = {
    'en': '{} November 2026', 'az': '{} noyabr 2026', 'ru': '{} ноября 2026 г.',
    'ar': '{} نوفمبر 2026', 'es': '{} de noviembre de 2026', 'fr': '{} novembre 2026',
    'zh': '2026 年 11 月 {} 日',
}


def geo_adapt(sec, pairs, l, day):
    """PetroGram's section in language l, turned into Geo-Rulers': the name,
    the date (day is the day of November on PetroGram's page) and the pairs."""
    assert 'PetroGram' in sec, l
    sec = sec.replace('PetroGram', GEO_NAME)
    for x, y in [(GEO_DATE[l].format(day), GEO_DATE[l].format(GEO_DAY))] + list(pairs):
        assert sec.count(x) == 1, ('georulers_texts.py', l, x[:60], sec.count(x))
        sec = sec.replace(x, y)
    return sec


# The page for deleting an account needs only the name and the date.
GEO_DELETE = {}

GEO_PRIV = {
'en': [
  # 1. what the app is, prices, update check
  ('a reference and learning app for the oil and gas industry,', 'a reference and learning app for geology and mining,'),
  ('The Market page downloads public price data from the U.S. Energy Information Administration (EIA).',
   'The Market page downloads one small file of public price data from our own website. When it starts, the app also asks Google Firebase whether an update is required (section 3).'),
  # 2. what leaves the phone
  ('This information stays on your device and is never sent to us. We cannot see your notes or progress.',
   'This information stays on your device. It is sent only if you use the optional features that need it: the scoreboard (section 6) and sync between your phones (section 6f). Otherwise we cannot see your notes or progress.'),
  # 3. prices
  ('<li><strong>Market prices.</strong> When you open the Market page, the app downloads public price data from the EIA at api.eia.gov. The request contains only the list of prices requested and the app\'s access key. It contains no personal data and nothing you have typed. As with any internet connection, the EIA\'s servers receive your device\'s IP address; the EIA handles it under its own privacy policy, published at eia.gov.</li>',
   '<li><strong>Market prices.</strong> The prices on the Market page are monthly averages of metal and mineral prices; a copy is built into the app. When you open the Market page, about once a week the app downloads a newer copy of this one small file from our own website, which is hosted by GitHub Pages (GitHub, Inc.). The request contains no access key, no personal data and nothing you have typed. As with any internet connection, the servers of the host, GitHub, receive your device\'s IP address; GitHub handles it under its own privacy statement, published at docs.github.com.</li>'),
  # 3. update check (new, before the scoreboard)
  ('<li><strong>Scoreboard.</strong>',
   '<li><strong>Update check.</strong> When the app starts, it asks Google Firebase (Remote Config) which is the oldest version of the app that may still be used, so that it can tell you when an update is necessary. The request carries a random number that Firebase creates for this installation, the app version, the system version, and the language, country and time zone set on your phone; it contains no name, no email and nothing you have typed. As with any internet connection, Google\'s servers receive your device\'s IP address. This check cannot be turned off.</li>\n    <li><strong>Scoreboard.</strong>'),
  # 8. the list of services
  ('<li>U.S. Energy Information Administration (EIA): public price data (section 3);</li>',
   '<li>GitHub Pages (GitHub, Inc.): hosting of our website, from which the price file is downloaded (section 3);</li>'),
  ('<li>Google Firebase (Authentication and Cloud Firestore): the optional scoreboard (section 6);</li>',
   '<li>Google Firebase (Authentication and Cloud Firestore): the optional scoreboard (section 6);</li>\n    <li>Google Firebase Remote Config: the update check (section 3);</li>'),
  # 9. who the app is for
  ('professionals and students of the oil and gas industry,', 'professionals and students of geology and mining,'),
],
'az': [
  ('Geo-Rulers neft-qaz sənayesi üçün Android və iPhone-da işləyən', 'Geo-Rulers geologiya və dağ-mədən işi üçün Android və iPhone-da işləyən'),
  ('«Bazar» səhifəsi ABŞ Energetika İnformasiya İdarəsindən (EIA) açıq qiymət məlumatlarını yükləyir.',
   '«Bazar» səhifəsi açıq qiymət məlumatları olan kiçik bir faylı öz saytımızdan yükləyir. Tətbiq açılanda həmçinin Google Firebase-dən yeniləmənin vacib olub-olmadığını soruşur (3-cü bənd).'),
  ('Bu məlumat cihazınızda qalır və bizə heç vaxt göndərilmir. Biz qeydlərinizi və irəliləyişinizi görə bilmirik.',
   'Bu məlumat cihazınızda qalır. O, yalnız bunu tələb edən könüllü funksiyalardan istifadə etdikdə göndərilir: reytinq (6-cı bənd) və telefonlarınız arasında sinxronizasiya (6f bəndi). Əks halda biz qeydlərinizi və irəliləyişinizi görə bilmirik.'),
  ('<li><strong>Bazar qiymətləri.</strong> «Bazar» səhifəsini açdıqda tətbiq EIA-dan (api.eia.gov) açıq qiymət məlumatlarını yükləyir. Sorğuda yalnız tələb olunan qiymətlərin siyahısı və tətbiqin giriş açarı olur; şəxsi məlumat və yazdığınız heç nə yoxdur. Hər internet bağlantısında olduğu kimi, EIA serverləri cihazınızın IP ünvanını görür; EIA onu eia.gov saytında dərc olunmuş öz məxfilik siyasətinə uyğun idarə edir.</li>',
   '<li><strong>Bazar qiymətləri.</strong> «Bazar» səhifəsindəki qiymətlər metalların və mineralların aylıq orta qiymətləridir; onların bir nüsxəsi tətbiqin içindədir. «Bazar» səhifəsini açdıqda tətbiq təxminən həftədə bir dəfə bu kiçik faylın daha yeni nüsxəsini GitHub Pages-də (GitHub, Inc.) yerləşən öz saytımızdan yükləyir. Sorğuda giriş açarı, şəxsi məlumat və yazdığınız heç nə yoxdur. Hər internet bağlantısında olduğu kimi, saytı yerləşdirən GitHub-ın serverləri cihazınızın IP ünvanını görür; GitHub onu docs.github.com saytında dərc olunmuş öz məxfilik bəyanatına uyğun idarə edir.</li>'),
  ('<li><strong>Reytinq.</strong>',
   '<li><strong>Yenilənmənin yoxlanması.</strong> Tətbiq açılanda Google Firebase-dən (Remote Config) tətbiqin hələ istifadə oluna bilən ən köhnə versiyasını soruşur ki, yeniləmə vacib olduqda sizə bildirə bilsin. Sorğuda Firebase-in bu quraşdırma üçün yaratdığı təsadüfi nömrə, tətbiqin versiyası, sistemin versiyası, həmçinin telefonunuzda seçilmiş dil, ölkə və saat qurşağı olur; ad, e-poçt və yazdığınız heç nə olmur. Hər internet bağlantısında olduğu kimi, Google serverləri cihazınızın IP ünvanını görür. Bu yoxlamanı söndürmək olmur.</li>\n    <li><strong>Reytinq.</strong>'),
  ('<li>ABŞ Energetika İnformasiya İdarəsi (EIA): açıq qiymət məlumatları (3-cü bənd);</li>',
   '<li>GitHub Pages (GitHub, Inc.): qiymət faylının yükləndiyi saytımızın yerləşdirilməsi (3-cü bənd);</li>'),
  ('<li>Google Firebase (Authentication və Cloud Firestore): könüllü reytinq (6-cı bənd);</li>',
   '<li>Google Firebase (Authentication və Cloud Firestore): könüllü reytinq (6-cı bənd);</li>\n    <li>Google Firebase Remote Config: yenilənmənin yoxlanması (3-cü bənd);</li>'),
  ('Tətbiq neft-qaz sənayesinin mütəxəssisləri və tələbələri üçündür,', 'Tətbiq geologiya və dağ-mədən işi üzrə mütəxəssislər və tələbələr üçündür,'),
],
'ru': [
  ('справочное и обучающее приложение для нефтегазовой отрасли для Android и iPhone.', 'справочное и обучающее приложение по геологии и горному делу для Android и iPhone.'),
  ('Страница «Рынок» загружает общедоступные данные о ценах Управления энергетической информации США (EIA).',
   'Страница «Рынок» загружает один небольшой файл с общедоступными данными о ценах с нашего собственного сайта. При запуске приложение также спрашивает у Google Firebase, не требуется ли обновление (раздел 3).'),
  ('Эти данные остаются на устройстве и никогда не передаются нам. Мы не видим ваших заметок и прогресса.',
   'Эти данные остаются на устройстве. Они отправляются, только если вы пользуетесь необязательными функциями, которым они нужны: рейтингом (раздел 6) и синхронизацией между вашими телефонами (раздел 6f). В остальных случаях мы не видим ваших заметок и прогресса.'),
  ('<li><strong>Рыночные цены.</strong> Когда вы открываете страницу «Рынок», приложение загружает общедоступные данные о ценах EIA с api.eia.gov. Запрос содержит только список запрашиваемых цен и ключ доступа приложения — никаких персональных данных и ничего из того, что вы ввели. Как и при любом подключении к интернету, серверы EIA получают IP-адрес вашего устройства; EIA обрабатывает его согласно своей политике конфиденциальности, опубликованной на eia.gov.</li>',
   '<li><strong>Рыночные цены.</strong> Цены на странице «Рынок» — это среднемесячные цены на металлы и минеральное сырьё; их копия встроена в приложение. Когда вы открываете страницу «Рынок», приложение примерно раз в неделю загружает более новую копию этого небольшого файла с нашего собственного сайта, размещённого на GitHub Pages (GitHub, Inc.). Запрос не содержит ни ключа доступа, ни персональных данных, ни чего-либо из того, что вы ввели. Как и при любом подключении к интернету, серверы GitHub, на которых размещён сайт, получают IP-адрес вашего устройства; GitHub обрабатывает его согласно своему заявлению о конфиденциальности, опубликованному на docs.github.com.</li>'),
  ('<li><strong>Рейтинг.</strong>',
   '<li><strong>Проверка обновления.</strong> При запуске приложение спрашивает у Google Firebase (Remote Config), какая самая старая версия приложения ещё может использоваться, чтобы сообщить вам, когда обновление необходимо. Запрос содержит случайный номер, который Firebase создаёт для этой установки, версию приложения, версию системы, а также язык, страну и часовой пояс, заданные на телефоне; в нём нет имени, почты и ничего из того, что вы ввели. Как и при любом подключении к интернету, серверы Google получают IP-адрес вашего устройства. Отключить эту проверку нельзя.</li>\n    <li><strong>Рейтинг.</strong>'),
  ('<li>Управление энергетической информации США (EIA): общедоступные данные о ценах (раздел 3);</li>',
   '<li>GitHub Pages (GitHub, Inc.): размещение нашего сайта, с которого загружается файл с ценами (раздел 3);</li>'),
  ('<li>Google Firebase (Authentication и Cloud Firestore): необязательный рейтинг (раздел 6);</li>',
   '<li>Google Firebase (Authentication и Cloud Firestore): необязательный рейтинг (раздел 6);</li>\n    <li>Google Firebase Remote Config: проверка обновления (раздел 3);</li>'),
  ('для специалистов и студентов нефтегазовой отрасли и не рассчитано', 'для специалистов и студентов в области геологии и горного дела и не рассчитано'),
],
'ar': [
  ('تطبيق مرجعي وتعليمي لصناعة النفط والغاز على Android وiPhone.', 'تطبيق مرجعي وتعليمي في الجيولوجيا والتعدين على Android وiPhone.'),
  ('وتنزّل صفحة السوق بيانات أسعار عامة من إدارة معلومات الطاقة الأمريكية (EIA).',
   'وتنزّل صفحة السوق ملفًا صغيرًا واحدًا لبيانات أسعار عامة من موقعنا الخاص. وعند التشغيل يسأل التطبيق أيضًا Google Firebase عمّا إذا كان التحديث مطلوبًا (البند 3).'),
  ('تبقى هذه المعلومات على جهازك ولا تُرسل إلينا أبدًا، ولا يمكننا رؤية ملاحظاتك أو تقدّمك.',
   'تبقى هذه المعلومات على جهازك. ولا تُرسَل إلا إذا استخدمت الميزات الاختيارية التي تحتاج إليها: لوحة المتصدرين (البند 6) والمزامنة بين هواتفك (البند 6و). وفيما عدا ذلك لا يمكننا رؤية ملاحظاتك أو تقدّمك.'),
  ('<li><strong>أسعار السوق.</strong> عند فتح صفحة «السوق» يحمّل التطبيق بيانات أسعار عامة من EIA عبر api.eia.gov. يحتوي الطلب فقط على قائمة الأسعار المطلوبة ومفتاح الوصول الخاص بالتطبيق، ولا يحتوي على أي بيانات شخصية أو أي شيء كتبته. وكما في أي اتصال بالإنترنت، تتلقى خوادم EIA عنوان IP لجهازك، وتتعامل معه وفق سياسة الخصوصية الخاصة بها المنشورة على eia.gov.</li>',
   '<li><strong>أسعار السوق.</strong> الأسعار في صفحة «السوق» هي متوسطات شهرية لأسعار المعادن والخامات المعدنية، وتوجد نسخة منها داخل التطبيق. عند فتح صفحة «السوق» ينزّل التطبيق مرة في الأسبوع تقريبًا نسخة أحدث من هذا الملف الصغير من موقعنا الخاص المستضاف على GitHub Pages (من GitHub, Inc.). لا يحتوي الطلب على مفتاح وصول ولا على أي بيانات شخصية أو أي شيء كتبته. وكما في أي اتصال بالإنترنت، تتلقى خوادم GitHub التي تستضيف الموقع عنوان IP لجهازك، وتتعامل معه GitHub وفق بيان الخصوصية الخاص بها المنشور على docs.github.com.</li>'),
  ('<li><strong>لوحة المتصدرين.</strong>',
   '<li><strong>التحقق من التحديث.</strong> عند تشغيل التطبيق يسأل Google Firebase (Remote Config) عن أقدم إصدار من التطبيق ما زال استخدامه ممكنًا، حتى يخبرك عندما يصبح التحديث ضروريًا. يحمل الطلب رقمًا عشوائيًا تنشئه Firebase لهذا التثبيت، وإصدار التطبيق، وإصدار النظام، واللغة والبلد والمنطقة الزمنية المضبوطة على هاتفك؛ ولا يحتوي على اسم أو بريد إلكتروني أو أي شيء كتبته. وكما في أي اتصال بالإنترنت، تتلقى خوادم Google عنوان IP لجهازك. لا يمكن إيقاف هذا التحقق.</li>\n    <li><strong>لوحة المتصدرين.</strong>'),
  ('<li>إدارة معلومات الطاقة الأمريكية (EIA): بيانات أسعار عامة (البند 3)؛</li>',
   '<li>GitHub Pages (من GitHub, Inc.): استضافة موقعنا الذي يُنزَّل منه ملف الأسعار (البند 3)؛</li>'),
  ('<li>Google Firebase (Authentication وCloud Firestore): لوحة المتصدرين الاختيارية (البند 6)؛</li>',
   '<li>Google Firebase (Authentication وCloud Firestore): لوحة المتصدرين الاختيارية (البند 6)؛</li>\n    <li>Google Firebase Remote Config: التحقق من التحديث (البند 3)؛</li>'),
  ('التطبيق موجّه للمهنيين والطلاب في قطاع النفط والغاز،', 'التطبيق موجّه للمهنيين والطلاب في مجال الجيولوجيا والتعدين،'),
],
'es': [
  ('una aplicación de consulta y aprendizaje para la industria del petróleo y el gas, para Android y iPhone.', 'una aplicación de consulta y aprendizaje sobre geología y minería, para Android y iPhone.'),
  ('La página Mercado descarga datos públicos de precios de la Administración de Información Energética de EE. UU. (EIA).',
   'La página Mercado descarga un pequeño archivo de datos públicos de precios desde nuestro propio sitio web. Al iniciarse, la aplicación también pregunta a Google Firebase si hace falta una actualización (sección 3).'),
  ('Esta información permanece en tu dispositivo y nunca se nos envía. No podemos ver tus notas ni tu progreso.',
   'Esta información permanece en tu dispositivo. Solo se envía si usas las funciones opcionales que la necesitan: la clasificación (sección 6) y la sincronización entre tus teléfonos (sección 6f). En los demás casos no podemos ver tus notas ni tu progreso.'),
  ('<li><strong>Precios de mercado.</strong> Cuando abres la página Mercado, la aplicación descarga datos públicos de precios de la EIA desde api.eia.gov. La solicitud solo contiene la lista de precios solicitados y la clave de acceso de la aplicación; no contiene datos personales ni nada de lo que hayas escrito. Como en cualquier conexión a internet, los servidores de la EIA reciben la dirección IP de tu dispositivo, que la EIA trata según su propia política de privacidad, publicada en eia.gov.</li>',
   '<li><strong>Precios de mercado.</strong> Los precios de la página Mercado son promedios mensuales de precios de metales y minerales; la aplicación incluye una copia. Cuando abres la página Mercado, aproximadamente una vez por semana la aplicación descarga una copia más reciente de este pequeño archivo desde nuestro propio sitio web, alojado en GitHub Pages (GitHub, Inc.). La solicitud no contiene ninguna clave de acceso, ni datos personales, ni nada de lo que hayas escrito. Como en cualquier conexión a internet, los servidores de GitHub, que aloja el sitio, reciben la dirección IP de tu dispositivo, que GitHub trata según su propia declaración de privacidad, publicada en docs.github.com.</li>'),
  ('<li><strong>Clasificación.</strong>',
   '<li><strong>Comprobación de actualización.</strong> Al iniciarse, la aplicación pregunta a Google Firebase (Remote Config) cuál es la versión más antigua de la aplicación que todavía se puede usar, para poder avisarte cuando una actualización sea necesaria. La solicitud lleva un número aleatorio que Firebase crea para esta instalación, la versión de la aplicación, la versión del sistema y el idioma, el país y la zona horaria configurados en tu teléfono; no contiene nombre, correo ni nada de lo que hayas escrito. Como en cualquier conexión a internet, los servidores de Google reciben la dirección IP de tu dispositivo. Esta comprobación no se puede desactivar.</li>\n    <li><strong>Clasificación.</strong>'),
  ('<li>Administración de Información Energética de EE. UU. (EIA): datos públicos de precios (sección 3);</li>',
   '<li>GitHub Pages (GitHub, Inc.): alojamiento de nuestro sitio web, desde el que se descarga el archivo de precios (sección 3);</li>'),
  ('<li>Google Firebase (Authentication y Cloud Firestore): la clasificación opcional (sección 6);</li>',
   '<li>Google Firebase (Authentication y Cloud Firestore): la clasificación opcional (sección 6);</li>\n    <li>Google Firebase Remote Config: la comprobación de actualización (sección 3);</li>'),
  ('para profesionales y estudiantes de la industria del petróleo y el gas,', 'para profesionales y estudiantes de geología y minería,'),
],
'fr': [
  ('une application de référence et d’apprentissage pour l’industrie pétrolière et gazière, sur Android et iPhone.', 'une application de référence et d’apprentissage sur la géologie et les mines, sur Android et iPhone.'),
  ('La page Marché télécharge des données de prix publiques de l’Energy Information Administration des États-Unis (EIA).',
   'La page Marché télécharge un petit fichier de données de prix publiques depuis notre propre site web. Au démarrage, l’application demande aussi à Google Firebase si une mise à jour est nécessaire (section 3).'),
  ('Ces informations restent sur votre appareil et ne nous sont jamais envoyées. Nous ne pouvons voir ni vos notes ni votre progression.',
   'Ces informations restent sur votre appareil. Elles ne sont envoyées que si vous utilisez les fonctions facultatives qui en ont besoin : le classement (section 6) et la synchronisation entre vos téléphones (section 6f). Dans les autres cas, nous ne pouvons voir ni vos notes ni votre progression.'),
  ('<li><strong>Prix du marché.</strong> Lorsque vous ouvrez la page Marché, l’application télécharge des données de prix publiques de l’EIA depuis api.eia.gov. La requête contient uniquement la liste des prix demandés et la clé d’accès de l’application ; elle ne contient aucune donnée personnelle ni rien de ce que vous avez saisi. Comme pour toute connexion internet, les serveurs de l’EIA reçoivent l’adresse IP de votre appareil, que l’EIA traite selon sa propre politique de confidentialité, publiée sur eia.gov.</li>',
   '<li><strong>Prix du marché.</strong> Les prix de la page Marché sont des moyennes mensuelles des prix des métaux et des minéraux ; une copie est intégrée à l’application. Lorsque vous ouvrez la page Marché, l’application télécharge environ une fois par semaine une copie plus récente de ce petit fichier depuis notre propre site web, hébergé par GitHub Pages (GitHub, Inc.). La requête ne contient ni clé d’accès, ni donnée personnelle, ni rien de ce que vous avez saisi. Comme pour toute connexion internet, les serveurs de GitHub, qui héberge le site, reçoivent l’adresse IP de votre appareil, que GitHub traite selon sa propre déclaration de confidentialité, publiée sur docs.github.com.</li>'),
  ('<li><strong>Classement.</strong>',
   '<li><strong>Vérification de mise à jour.</strong> Au démarrage, l’application demande à Google Firebase (Remote Config) quelle est la plus ancienne version de l’application encore utilisable, afin de vous prévenir lorsqu’une mise à jour est nécessaire. La requête contient un numéro aléatoire que Firebase crée pour cette installation, la version de l’application, la version du système, ainsi que la langue, le pays et le fuseau horaire réglés sur votre téléphone ; elle ne contient ni nom, ni e-mail, ni rien de ce que vous avez saisi. Comme pour toute connexion internet, les serveurs de Google reçoivent l’adresse IP de votre appareil. Cette vérification ne peut pas être désactivée.</li>\n    <li><strong>Classement.</strong>'),
  ('<li>Energy Information Administration des États-Unis (EIA) : données de prix publiques (section 3) ;</li>',
   '<li>GitHub Pages (GitHub, Inc.) : hébergement de notre site web, d’où le fichier de prix est téléchargé (section 3) ;</li>'),
  ('<li>Google Firebase (Authentication et Cloud Firestore) : le classement facultatif (section 6) ;</li>',
   '<li>Google Firebase (Authentication et Cloud Firestore) : le classement facultatif (section 6) ;</li>\n    <li>Google Firebase Remote Config : la vérification de mise à jour (section 3) ;</li>'),
  ('aux professionnels et aux étudiants de l’industrie pétrolière et gazière,', 'aux professionnels et aux étudiants de la géologie et des mines,'),
],
'zh': [
  ('是一款面向石油天然气行业的参考与学习应用，', '是一款面向地质与采矿领域的参考与学习应用，'),
  ('“市场”页面会从美国能源信息署（EIA）下载公开的价格数据。',
   '“市场”页面会从我们自己的网站下载一个包含公开价格数据的小文件。应用启动时还会向 Google Firebase 查询是否必须更新（见第 3 节）。'),
  ('这些信息保存在您的设备上，不会发送给我们。我们看不到您的笔记或进度（除非您创建账号并使用同步，见第 6f 节）。',
   '这些信息保存在您的设备上。只有在您使用需要这些信息的可选功能时才会发送：排行榜（见第 6 节）和手机之间的同步（见第 6f 节）。除此之外，我们看不到您的笔记或进度。'),
  ('<li><strong>市场价格。</strong>当您打开“市场”页面时，应用会从 api.eia.gov 下载 EIA 的公开价格数据。请求中只包含所需的价格列表和应用的访问密钥，不含任何个人数据或您输入的内容。与任何网络连接一样，EIA 的服务器会收到您设备的 IP 地址；EIA 依据其在 eia.gov 上公布的隐私政策处理该地址。</li>',
   '<li><strong>市场价格。</strong>“市场”页面上的价格是金属和矿产品的月平均价格，应用内已附带一份。当您打开“市场”页面时，应用大约每周一次从我们自己的网站下载这个小文件的较新版本；该网站托管在 GitHub Pages（GitHub, Inc.）上。请求中不含访问密钥、任何个人数据或您输入的内容。与任何网络连接一样，托管网站的 GitHub 的服务器会收到您设备的 IP 地址；GitHub 依据其在 docs.github.com 上公布的隐私声明处理该地址。</li>'),
  ('<li><strong>排行榜。</strong>',
   '<li><strong>更新检查。</strong>应用启动时会向 Google Firebase（Remote Config）查询仍可使用的最低应用版本，以便在必须更新时提醒您。请求中包含 Firebase 为本次安装创建的一个随机编号、应用版本、系统版本，以及您手机上设置的语言、国家/地区和时区；不含姓名、电子邮件或您输入的任何内容。与任何网络连接一样，Google 的服务器会收到您设备的 IP 地址。此项检查无法关闭。</li>\n    <li><strong>排行榜。</strong>'),
  ('<li>美国能源信息署（EIA）：公开价格数据（见第 3 节）；</li>',
   '<li>GitHub Pages（GitHub, Inc.）：托管我们的网站，价格文件从该网站下载（见第 3 节）；</li>'),
  ('<li>Google Firebase（Authentication 和 Cloud Firestore）：可选的排行榜、账号以及手机之间的同步（见第 6、6b、6f 节）；</li>',
   '<li>Google Firebase（Authentication 和 Cloud Firestore）：可选的排行榜、账号以及手机之间的同步（见第 6、6b、6f 节）；</li>\n    <li>Google Firebase Remote Config：更新检查（见第 3 节）；</li>'),
  ('本应用面向石油天然气行业的从业人员和学生，', '本应用面向地质与采矿领域的从业人员和学生，'),
],
}
assert list(GEO_PRIV) == list(DOC_LANGS), 'georulers_texts.py: one list per language, in the order of DOC_LANGS'
assert all(len(v) == len(GEO_PRIV['en']) for v in GEO_PRIV.values()), 'georulers_texts.py: the same changes in every language'
