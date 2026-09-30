# ملف README - تطبيق Tikvibe

## نظرة عامة

Tikvibe هو تطبيق مشاركة فيديوهات قصيرة مبتكر مصمم خصيصاً للسوق العربي. يجمع التطبيق بين الترفيه والتفاعل الاجتماعي مع نظام اقتصادي متطور يمكّن المستخدمين من دعم صناع المحتوى من خلال الهدايا المالية.

## المميزات الرئيسية

### 🔐 نظام مصادقة متعدد
- تسجيل الدخول عبر Google
- تسجيل الدخول عبر Facebook  
- تسجيل الدخول بالبريد الإلكتروني
- تسجيل الدخول برقم الهاتف مع OTP

### 👥 أنواع الحسابات
- **حساب خاص**: خصوصية عالية مع محتوى محدود للمتابعين المقبولين
- **حساب عام**: محتوى عام يمكن لأي شخص مشاهدته ومتابعته
- **حساب تجاري**: للشركات وصناع المحتوى مع ميزات متقدمة

### 💰 نظام المحفظة والهدايا
- تعبئة الرصيد عبر PayPal
- إرسال هدايا مالية لصناع المحتوى
- عمولة 11% على المعاملات
- سحب الأموال إلى PayPal

### 🎥 ميزات الفيديو
- رفع ومشاركة الفيديوهات القصيرة
- تفاعل كامل (لايك، تعليق، مشاركة، حفظ)
- البث المباشر مع التفاعل الفوري
- هدايا مباشرة أثناء البث

### 🤖 ذكاء اصطناعي
- توصيات شخصية للمحتوى
- فلترة المحتوى غير المناسب
- تحليل الاتجاهات والهاشتاغات
- تصنيف المحتوى تلقائياً

## التقنيات المستخدمة

### Frontend
- **React Native 0.76.5**: إطار العمل الأساسي
- **React Navigation**: للتنقل بين الشاشات
- **React Native Vector Icons**: للأيقونات
- **React Native Linear Gradient**: للتدرجات اللونية

### Backend & Database
- **Firebase Authentication**: نظام المصادقة
- **Cloud Firestore**: قاعدة البيانات
- **Firebase Storage**: تخزين الملفات
- **PayPal API**: معالجة المدفوعات

### أدوات التطوير
- **TypeScript**: للكتابة الآمنة
- **Jest**: للاختبارات
- **ESLint**: لجودة الكود
- **Prettier**: لتنسيق الكود

## هيكل المشروع

```
TikvibeApp/
├── src/
│   ├── screens/          # شاشات التطبيق
│   │   ├── LoginScreen.tsx
│   │   ├── AccountTypeScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── WalletScreen.tsx
│   │   ├── LiveStreamScreen.tsx
│   │   └── ProfileScreen.tsx
│   ├── services/         # خدمات التطبيق
│   │   ├── AuthService.ts
│   │   ├── VideoService.ts
│   │   ├── WalletService.ts
│   │   ├── LiveStreamService.ts
│   │   ├── AIService.ts
│   │   └── PayPalService.ts
│   ├── components/       # مكونات قابلة للإعادة
│   └── utils/           # أدوات مساعدة
├── android/             # ملفات Android
├── ios/                 # ملفات iOS
└── __tests__/          # ملفات الاختبار
```

## التثبيت والإعداد

### المتطلبات الأساسية
- Node.js 18+
- React Native CLI
- Android Studio (للتطوير على Android)
- Xcode (للتطوير على iOS)

### خطوات التثبيت

1. **استنساخ المشروع**
```bash
git clone https://github.com/your-repo/tikvibe-app.git
cd tikvibe-app
```

2. **تثبيت التبعيات**
```bash
npm install
```

3. **إعداد Firebase**
- إنشاء مشروع Firebase جديد
- تفعيل Authentication و Firestore و Storage
- تحديث ملف `src/services/firebase.ts` بإعدادات مشروعك

4. **إعداد PayPal**
- إنشاء حساب مطور PayPal
- الحصول على Client ID و Client Secret
- تحديث ملف `src/services/PayPalService.ts`

5. **تشغيل التطبيق**

للتطوير على Android:
```bash
npx react-native run-android
```

للتطوير على iOS:
```bash
npx react-native run-ios
```

## بناء APK للإنتاج

### إعداد البيئة
```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export ANDROID_HOME=/usr/lib/android-sdk
```

### بناء APK
```bash
cd android
./gradlew assembleRelease
```

سيتم إنشاء ملف APK في:
`android/app/build/outputs/apk/release/app-release.apk`

## الاختبار

### تشغيل الاختبارات
```bash
npm test
```

### اختبار التطبيق
```bash
npm run test:e2e
```

## إعدادات Firebase

### Authentication
تفعيل طرق تسجيل الدخول التالية:
- Google
- Facebook
- Email/Password
- Phone

### Firestore Rules
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users collection
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Videos collection
    match /videos/{videoId} {
      allow read: if resource.data.isPublic == true || request.auth.uid == resource.data.userId;
      allow write: if request.auth != null && request.auth.uid == resource.data.userId;
    }
    
    // Comments collection
    match /comments/{commentId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == resource.data.userId;
    }
  }
}
```

### Storage Rules
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /videos/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    match /thumbnails/{userId}/{allPaths=**} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## إعدادات PayPal

### متغيرات البيئة
```env
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_ENVIRONMENT=sandbox  # أو production
```

### Webhook Configuration
إعداد webhooks في PayPal لمعالجة الأحداث:
- PAYMENT.SALE.COMPLETED
- PAYMENT.SALE.DENIED
- PAYMENTS.PAYMENT.CREATED

## الأمان والخصوصية

### حماية البيانات
- تشفير جميع البيانات الحساسة
- استخدام HTTPS لجميع الاتصالات
- تطبيق مبدأ الحد الأدنى من الصلاحيات

### مراجعة الكود
- فحص أمني دوري للكود
- استخدام أدوات تحليل الثغرات الأمنية
- مراجعة التبعيات للثغرات المعروفة

## المساهمة في المشروع

### إرشادات المساهمة
1. Fork المشروع
2. إنشاء branch جديد للميزة
3. Commit التغييرات مع رسائل واضحة
4. Push إلى branch
5. إنشاء Pull Request

### معايير الكود
- استخدام TypeScript لجميع الملفات
- اتباع ESLint rules المحددة
- كتابة اختبارات للميزات الجديدة
- توثيق الكود بوضوح

## الدعم والمساعدة

### التواصل
- البريد الإلكتروني: support@tikvibe.com
- الموقع الإلكتروني: https://tikvibe.com
- التوثيق: https://docs.tikvibe.com

### الإبلاغ عن المشاكل
استخدم GitHub Issues للإبلاغ عن:
- الأخطاء البرمجية
- طلبات الميزات الجديدة
- مشاكل الأداء

## الترخيص

هذا المشروع مرخص تحت رخصة MIT. راجع ملف [LICENSE](LICENSE) للتفاصيل.

## الشكر والتقدير

شكر خاص لجميع المساهمين في تطوير هذا التطبيق:
- فريق التطوير
- مصممي واجهة المستخدم
- فريق ضمان الجودة
- مجتمع المطورين

---

© 2025 Tikvibe. جميع الحقوق محفوظة.

