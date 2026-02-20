<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>سیستم خبره برای تحلیل و پیش‌بینی نتایج آزمایش‌های مکانیک کوانتوم</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root {
      --bg: #050816;
      --bg-alt: #0b1020;
      --accent: #38bdf8;
      --accent-soft: rgba(56, 189, 248, 0.12);
      --text: #e5e7eb;
      --muted: #9ca3af;
      --border: #1f2937;
      --code-bg: #020617;
      --radius-lg: 16px;
      --radius-md: 12px;
      --radius-sm: 8px;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: radial-gradient(circle at top, #0b1120, #020617 55%, #000 100%);
      color: var(--text);
      line-height: 1.7;
    }

    a {
      color: var(--accent);
      text-decoration: none;
    }

    a:hover {
      text-decoration: underline;
    }

    .container {
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px 16px 64px;
    }

    header {
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 32px;
      padding: 24px 20px;
      border-radius: 24px;
      background: radial-gradient(circle at top left, #0f172a, #020617);
      border: 1px solid var(--border);
      box-shadow:
        0 0 40px rgba(15, 23, 42, 0.9),
        0 0 0 1px rgba(148, 163, 184, 0.08);
    }

    header h1 {
      margin: 0;
      font-size: 1.8rem;
      letter-spacing: -0.03em;
    }

    header p {
      margin: 0;
      color: var(--muted);
      max-width: 650px;
    }

    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 8px 16px;
      font-size: 0.85rem;
      color: var(--muted);
    }

    .meta span {
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(55, 65, 81, 0.9);
    }

    nav {
      position: sticky;
      top: 0;
      z-index: 20;
      backdrop-filter: blur(16px);
      background: linear-gradient(to bottom, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.85), transparent);
      margin: 0 -16px 24px;
      padding: 8px 16px 12px;
      border-bottom: 1px solid rgba(31, 41, 55, 0.9);
    }

    .nav-inner {
      max-width: 1100px;
      margin: 0 auto;
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
      justify-content: flex-start;
    }

    .nav-title {
      font-size: 0.85rem;
      color: var(--muted);
      margin-left: 8px;
    }

    .nav-link {
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 0.85rem;
      border: 1px solid rgba(55, 65, 81, 0.9);
      background: rgba(15, 23, 42, 0.95);
      color: var(--muted);
      text-decoration: none;
      transition: 0.15s ease;
    }

    .nav-link:hover {
      color: var(--accent);
      border-color: rgba(56, 189, 248, 0.7);
      box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.3);
      text-decoration: none;
    }

    main {
      display: grid;
      grid-template-columns: minmax(0, 2.1fr) minmax(0, 1.2fr);
      gap: 24px;
    }

    @media (max-width: 900px) {
      main {
        grid-template-columns: minmax(0, 1fr);
      }
    }

    section {
      margin-bottom: 24px;
      padding: 20px 18px;
      border-radius: var(--radius-lg);
      background: linear-gradient(145deg, rgba(15, 23, 42, 0.97), rgba(15, 23, 42, 0.92));
      border: 1px solid var(--border);
      box-shadow:
        0 18px 40px rgba(0, 0, 0, 0.7),
        0 0 0 1px rgba(15, 23, 42, 0.9);
    }

    section h2 {
      margin-top: 0;
      margin-bottom: 12px;
      font-size: 1.2rem;
      letter-spacing: -0.01em;
    }

    h3 {
      margin-top: 16px;
      margin-bottom: 8px;
      font-size: 1rem;
    }

    p {
      margin: 0 0 8px;
      font-size: 0.95rem;
    }

    ul {
      margin: 6px 0 10px;
      padding-right: 18px;
      font-size: 0.92rem;
    }

    li {
      margin-bottom: 4px;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 0.8rem;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(75, 85, 99, 0.9);
      color: var(--muted);
    }

    .pill-dot {
      width: 7px;
      height: 7px;
      border-radius: 999px;
      background: #22c55e;
      box-shadow: 0 0 8px rgba(34, 197, 94, 0.7);
    }

    pre {
      margin: 10px 0;
      padding: 10px 12px;
      background: var(--code-bg);
      border-radius: var(--radius-md);
      border: 1px solid rgba(31, 41, 55, 0.9);
      overflow-x: auto;
      font-size: 0.82rem;
      direction: ltr;
      text-align: left;
    }

    code {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }

    .tag-list {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      font-size: 0.78rem;
      margin-top: 6px;
    }

    .tag {
      padding: 3px 8px;
      border-radius: 999px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(55, 65, 81, 0.9);
      color: var(--muted);
    }

    .card-muted {
      background: radial-gradient(circle at top left, #020617, #020617);
      border-style: dashed;
    }

    .screens {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 10px;
      margin-top: 6px;
    }

    .screen {
      border-radius: var(--radius-md);
      background: #020617;
      border: 1px solid rgba(31, 41, 55, 0.9);
      padding: 8px;
      font-size: 0.8rem;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 3px 8px;
      border-radius: 999px;
      font-size: 0.78rem;
      background: rgba(8, 47, 73, 0.9);
      color: #e0f2fe;
      border: 1px solid rgba(56, 189, 248, 0.5);
    }

    footer {
      margin-top: 24px;
      padding-top: 16px;
      border-top: 1px solid rgba(31, 41, 55, 0.9);
      font-size: 0.8rem;
      color: var(--muted);
      display: flex;
      flex-wrap: wrap;
      gap: 8px 16px;
      justify-content: space-between;
    }
  </style>
</head>
<body>
  <nav>
    <div class="nav-inner">
      <span class="nav-title">مستندات پروژه</span>
      <a class="nav-link" href="#overview">نمای کلی</a>
      <a class="nav-link" href="#goals">اهداف</a>
      <a class="nav-link" href="#methodology">روش‌شناسی</a>
      <a class="nav-link" href="#experiments">آزمایش‌ها</a>
      <a class="nav-link" href="#rules">گزارش‌های کیفی</a>
      <a class="nav-link" href="#feasibility">گزارش امکان‌سنجی</a>
      <a class="nav-link" href="#usage">نحوه اجرا</a>
    </div>
  </nav>

  <div class="container">
    <header id="overview">
      <h1>سیستم خبره برای تحلیل و پیش‌بینی نتایج آزمایش‌های مکانیک کوانتوم</h1>
      <p>
        این مخزن شامل کدها و مستندات یک سیستم خبره مبتنی بر قواعد است که نتایج کیفی مجموعه‌ای از آزمایش‌های مشهور مکانیک کوانتوم را تحلیل و پیش‌بینی می‌کند.[file:1]
      </p>
      <div class="meta">
        <span>درس: سیستم‌های خبره[file:1]</span>
        <span>دامنه: محاسبات کوانتومی و آزمایش‌های کلاسیک[file:1]</span>
        <span>پیاده‌سازی: Python + Experta[file:1]</span>
      </div>
    </header>

    <main>
      <!-- Left column: conceptual docs -->
      <div>
        <section id="goals">
          <h2>اهداف پروژه</h2>
          <h3>هدف آموزشی</h3>
          <p>
            هدف، ایجاد بستری است که دانشجو تفاوت منطق کلاسیک و منطق کوانتومی، مدل‌سازی دانش و نقش قواعد و موتور استنتاج را در قالب یک سیستم خبره تجربه کند.[file:1]
          </p>
          <h3>هدف علمی</h3>
          <p>
            سیستم نشان می‌دهد چگونه مفاهیمی مانند برهم‌نهی، احتمال‌های کوانتومی، تداخل و رفتار غیرقطعی را می‌توان به صورت قواعد قابل استنتاج مدل کرد.[file:1]
          </p>
          <h3>هدف پژوهشی و کاربردی</h3>
          <p>
            پروژه به عنوان مطالعه موردی کاربرد سیستم‌های خبره در علوم نوین عمل می‌کند و امکان‌پذیری، محدودیت‌ها و کارکرد آموزشی چنین سامانه‌ای را بررسی می‌کند.[file:1]
          </p>
        </section>

        <section id="methodology">
          <h2>روش‌شناسی و پیاده‌سازی</h2>
          <ul>
            <li>جمع‌آوری و تحلیل داده‌ها از منابع علمی و مقالات درباره آزمایش‌های منتخب کوانتومی.[file:1]</li>
            <li>استخراج دانش به صورت Facts و Rules و ساختاربندی آن به صورت پایگاه دانش.[file:1]</li>
            <li>پیاده‌سازی سیستم خبره با Python و کتابخانه Experta و تعریف موتور استنتاج.[file:1]</li>
            <li>طراحی سناریوهای آزمایشی، ارزیابی خروجی سیستم و اصلاح قواعد بر اساس نتایج.[file:1]</li>
            <li>توسعه و افزودن قواعد جدید برای پوشش سناریوهای بیشتر و بهبود دقت پیش‌بینی.[file:1]</li>
          </ul>

          <h3>ساختار کد در مخزن</h3>
          <ul>
            <li><code>engine.py</code>: تعریف کلاس‌های Fact، Rule و موتور استنتاج.</li>
            <li><code>knowledge_base.py</code>: قواعد مرتبط با هر آزمایش (دوشکاف، تونل‌زنی، Stern–Gerlach و ...).[file:1]</li>
            <li><code>ui_cli.py</code> یا <code>main.py</code>: رابط خط فرمان برای دریافت ورودی‌ها و نمایش تحلیل.[file:1]</li>
          </ul>

          <h3>نمونه حداقلی استفاده از Experta</h3>
          <pre><code>from experta import KnowledgeEngine, Fact, Rule

class QuantumExperiment(Fact):
    pass

class QuantumExpertSystem(KnowledgeEngine):
    @Rule(QuantumExperiment(type='double_slit', detector=False))
    def interference_pattern(self):
        # استنتاج وجود الگوی تداخل
        pass
</code></pre>
        </section>

        <section id="experiments">
          <h2>آزمایش‌های پوشش‌داده‌شده</h2>
          <ul>
            <li>آزمایش دوشکاف (Double-Slit Experiment)[file:1]</li>
            <li>تونل‌زنی کوانتومی (Quantum Tunneling)[file:1]</li>
            <li>آزمایش Stern–Gerlach[file:1]</li>
            <li>اندازه‌گیری تابع موج (Wave Function Measurement)[file:1]</li>
            <li>برهم‌نهی کوانتومی (Quantum Superposition)[file:1]</li>
            <li>اثر مشاهده‌گر (Observer Effect)[file:1]</li>
            <li>گربه شرودینگر، ماخ–زندر، انتخاب تأخیری، پاک‌کن کوانتومی (در بخش گزارش‌ها به‌صورت کیفی).[file:1]</li>
          </ul>
        </section>

        <section id="rules">
          <h2>گزارش‌های کیفی و قواعد مفهومی</h2>
          <p>
            برای هر آزمایش، مجموعه‌ای از جملات کیفی (حدوداً ۱۵ قاعده) در مستندات آمده که به عنوان راهنمای استخراج قواعد در پایگاه دانش استفاده می‌شوند.[file:1]
          </p>
          <h3>نمونه: دوشکاف</h3>
          <ul>
            <li>در نبود آشکارساز مسیر، ذره رفتار موجی دارد و الگوی تداخل شکل می‌گیرد.[file:1]</li>
            <li>نصب آشکارساز مسیر باعث از بین رفتن الگوی تداخل می‌شود.[file:1]</li>
            <li>افزایش نویز محیطی می‌تواند تداخل را تضعیف کند.[file:1]</li>
          </ul>
          <h3>نمونه: گربه شرودینگر</h3>
          <ul>
            <li>پیش از مشاهده، سامانه در برهم‌نهی حالت زنده و مرده است.[file:1]</li>
            <li>مشاهده منجر به فروپاشی تابع موج به یکی از دو حالت ممکن می‌شود.[file:1]</li>
            <li>برهم‌کنش با محیط باعث دکوهرنس سریع سیستم‌های پیچیده می‌شود.[file:1]</li>
          </ul>
        </section>

        <section id="feasibility">
          <h2>گزارش امکان‌سنجی</h2>
          <h3>ساخت‌یافتگی و ماهیت مسئله</h3>
          <p>
            مسئله تفسیر کیفی آزمایش‌های کوانتومی غیرساخت‌یافته است و به قضاوت مفهومی و هیورستیک متکی است، بنابراین برای پیاده‌سازی با سیستم خبره مناسب است.[file:1]
          </p>
          <h3>وجود دانش خبره و منابع</h3>
          <p>
            دانش مورد نیاز از طریق کتاب‌های مرجع، مقالات و متخصصان فیزیک کوانتومی قابل استخراج است و برای بسیاری از زیرمسائل، ساخت قواعد مستقل امکان‌پذیر است.[file:1]
          </p>
          <h3>پذیرش خطا و explainability</h3>
          <p>
            با نمایش توضیحات متنی و ضریب اطمینان برای هر نتیجه، کاربران می‌توانند محدودیت‌ها و اعتبار استنتاج‌ها را درک و خروجی سیستم را بهتر بپذیرند.[file:1]
          </p>
        </section>
      </div>

      <!-- Right column: usage & UI -->
      <div>
        <section id="usage">
          <h2>نحوه اجرا و ساخت</h2>
          <span class="pill"><span class="pill-dot"></span> وضعیت: نسخه بتا[file:1]</span>
          <h3>پیش‌نیازها</h3>
          <ul>
            <li>Python 3.10 یا بالاتر</li>
            <li>نصب کتابخانه <code>experta</code> و سایر وابستگی‌ها</li>
          </ul>
          <pre><code># نصب وابستگی‌ها
pip install experta

# اجرای سیستم خبره (نمونه)
python main.py</code></pre>

          <h3>نحوه استفاده</h3>
          <ul>
            <li>نوع آزمایش، شرایط محیطی، وضعیت آشکارساز و ویژگی‌های ذره را به عنوان ورودی تنظیم کنید.[file:1]</li>
            <li>سیستم مجموعه‌ای از نتایج کیفی، توضیح متنی و یک ضریب اطمینان ارائه می‌دهد.[file:1]</li>
          </ul>
        </section>

        <section>
          <h2>رابط کاربری و خروجی سیستم</h2>
          <p>
            مستندات شامل اسکرین‌شات‌هایی از رابط «Quantum Expert System» است که برای هر آزمایش، تحلیل متخصص، توضیحات و یک نمودار یا گراف بصری نمایش می‌دهد.[file:1]
          </p>
          <div class="screens">
            <div class="screen">
              <div class="badge">Double-Slit</div>
              <p>فرینج‌های تداخل پهن‌تر شده‌اند، توضیح مبتنی بر تابع موج و عدم قطعیت تکانه.[file:1]</p>
            </div>
            <div class="screen">
              <div class="badge">Photoelectric</div>
              <p>وابستگی انرژی الکترون‌ها به فرکانس نور، نه شدت؛ مناسب بودن فلزات قلیایی.[file:1]</p>
            </div>
            <div class="screen">
              <div class="badge">Quantum Tunneling</div>
              <p>عبور جزئی موج از سد انرژی با احتمال وابسته به ضخامت سد و انرژی ذره.[file:1]</p>
            </div>
          </div>
          <div class="tag-list">
            <span class="tag">Expert Analysis[file:1]</span>
            <span class="tag">Confidence Score[file:1]</span>
            <span class="tag">Visual Result[file:1]</span>
          </div>
        </section>

        <section class="card-muted">
          <h2>وضعیت فعلی و توسعه آینده</h2>
          <p>
            نسخه فعلی سیستم یک نسخه اولیه (بتا) است که برای آزمایش‌ها و سناریوهای منتخب قواعد تعریف کرده و قابلیت توسعه به دامنه‌های بیشتر را دارد.[file:1]
          </p>
          <ul>
            <li>افزودن قواعد دقیق‌تر برای Stern–Gerlach و سناریوهای بدون قاعده فعال.[file:1]</li>
            <li>ادغام روش‌های عدم قطعیت پیشرفته‌تر (مثلاً فازی یا CF).[file:1]</li>
            <li>گسترش رابط کاربری گرافیکی و مستندسازی مثال‌های بیشتر.[file:1]</li>
          </ul>
        </section>
      </div>
    </main>

    <footer>
      <span>© ۱۴۰۴ — سیستم خبره آزمایش‌های مکانیک کوانتوم[file:1]</span>
      <span>این فایل به عنوان صفحه مستندات GitHub Repo قابل استفاده است.[file:1]</span>
    </footer>
  </div>
</body>
</html>
