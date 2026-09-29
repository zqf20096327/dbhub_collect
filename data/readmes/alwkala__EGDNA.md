# مستكشف الجينوم المصري | Egyptian Genomic Explorer (EGDNA)

## العربية

منصة تفاعلية مفتوحة المصدر لاستكشاف علم الوراثة السكانية في مصر، تاريخ وادي النيل، وعينات الحمض النووي القديم. تعرض الواجهة الخرائط والرسوم البيانية وبيانات المصادر العلمية مع تمييز واضح بين البيانات المنشورة والبيانات غير المتاحة.

### المتطلبات والتشغيل

- PHP 8.2+ مع `pdo_sqlite` و`json`، وComposer، وNode.js 18+ مع npm.
- خادم Apache/WampServer أو خادم PHP محلي.

```bash
composer install
npm install
php scripts/validate.php
php tests/api_test.php
npm run build
```

افتح `http://localhost/EGDNA/` بعد تشغيل Apache. للتطوير استخدم `npm run dev`.

### إعداد CORS

CORS مغلق افتراضياً. للسماح بأصل موثوق، عرّف `EGDNA_ALLOWED_ORIGINS` بقائمة مفصولة بفواصل:

```text
EGDNA_ALLOWED_ORIGINS=http://localhost:5173,http://localhost/EGDNA
```

### السياسة العلمية

- لا تُقارن المقاييس إلا داخل لوحات SNP وخطوط معالجة متوافقة.
- القياسات غير المتاحة تُعرض كـ «البيانات غير متوفرة» ولا تُخمن.
- إحداثيات PCA القديمة غير المقاسة تعود كـ `null` مع `coordinates_available: false`.
- تُعرض معلومات DOI/الوصول وحالة التحكيم عند توفرها.

## English

EGDNA is an open-source interactive explorer for Egyptian population genetics, Nile Valley history, and ancient DNA. It provides maps, scientific charts, provenance metadata, and explicit unavailable-data fallbacks instead of inventing measurements.

### Requirements and local setup

PHP 8.2+ with `pdo_sqlite` and `json`, Composer, Node.js 18+, npm, and Apache/WampServer are recommended.

```bash
composer install
npm install
php scripts/validate.php
php tests/api_test.php
npm run build
```

Open `http://localhost/EGDNA/` with Apache running. Use `npm run dev` for frontend development.

### CORS

CORS is closed by default. To allow a trusted frontend origin, set the comma-separated `EGDNA_ALLOWED_ORIGINS` environment variable:

```text
EGDNA_ALLOWED_ORIGINS=http://localhost:5173,http://localhost/EGDNA
```

### Scientific data policy

- Compare metrics only within compatible SNP panels and QC pipelines.
- Missing measurements return `Data not available`; no substitute values are inferred.
- Ancient PCA points without measured coordinates return `null` coordinates and `coordinates_available: false`.
- DOI/accession and peer-review status are exposed where available.

## API and tests

The JSON API is available under `/api/` and uses `{ success, data, meta, error }`. Endpoints cover populations, comparisons, PCA, ancient individuals, haplogroups, sources, metrics, and geography. Run `php scripts/validate.php` for provenance checks, `php tests/api_test.php` for API smoke tests, and `npm run build` for the production bundle.

## License

MIT
