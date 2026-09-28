## DigitalKeyHub Platform

<p align="center">
  <img src="https://raw.githubusercontent.com/BogdanPryadko4853/online-shop-spring-boot/main/image.png" alt="DigitalKeyHub Logo" width="400">
</p>


A modular monolithic digital marketplace platform with integrated payment processing, user management, and product storage capabilities.

## � Project Structure

This is a modular monolithic application where each component is developed as a separate module within a single codebase:

# 🏗️ Module structure

```bash
digitalkeyhub/
├── 📁 digitalkeyhub-api/           # 🛠️  Core API 
│
├── 📁 digitalkeyhub-app/           # 🚀 Main application
│
├── 📁 digitalkeyhub-comment/       # 💬 Comment system
│
├── 📁 digitalkeyhub-common-config/ # ⚙️ Shared configs
│
├── 📁 digitalkeyhub-notification/  # ✉️ Notifications
│
├── 📁 digitalkeyhub-order/         # 📦 Order management
│
├── 📁 digitalkeyhub-payment/       # 💳 Payments
│
├── 📁 digitalkeyhub-product/       # 🛍️ Products
│
├── 📁 digitalkeyhub-security/      # 🔐 Security
│
├── 📁 digitalkeyhub-storage/       # 📂 File storage
│ 
└── 📁 digitalkeyhub-user/          # 👥 Users
    ├── 📄 UserService.java         # User management
    └── 📄 ProfileService.java      # Profile logic

```


## 🚀 Key Features

- **Modular Architecture**: Single codebase with clearly separated modules
- **Payment Processing**: Full Stripe integration with webhook support
- **User Management**: Complete authentication and profile system
- **Product Management**: Digital product storage with MinIO
- **Order Processing**: End-to-end order lifecycle management
- **Email Notifications**: Transactional email system with Thymeleaf templates

## 🛠 Technology Stack

- **Core**: Java 21, Spring Boot 3, Spring Security
- **Database**: PostgreSQL
- **Storage**: MinIO for object storage
- **Payment**: Stripe API integration
- **Email**: SMTP with Gmail (test configuration included)
- **Templates**: Thymeleaf for email templates
- **Containerization**: Docker with Docker Compose

## ⚙️ Configuration Requirements

### Stripe Configuration
```properties
stripe.secret-key= your key
stripe.webhook-secret= your key
```

## Email Configuration
properties
```
spring.mail.host=smtp.gmail.com
spring.mail.port=587
spring.mail.username=bogdanpryadko1@gmail.com
spring.mail.password=vrjf xgth yjsz jxbr
spring.mail.protocol=smtp
spring.mail.properties.mail.smtp.auth=true
spring.mail.properties.mail.smtp.starttls.enable=true
spring.mail.properties.mail.smtp.ssl.trust=smtp.gmail.com
```


## 🐳 Running with Docker
Clone the repository:

```bash
git clone https://github.com/BogdanPryadko4853/online-shop-spring-boot.git
cd online-shop-spring-boot
```
Build and start containers:

```bash
docker-compose up --build -d
```

Verify services:

App: http://localhost:8080

MinIO Console: http://localhost:9001 (Login: minioadmin/minioadmin)

PostgreSQL: localhost:5432


## 💳 Payment Integration
To test Stripe payments locally:

Install Stripe CLI:

```bash
brew install stripe/stripe-cli/stripe  # Mac
choco install stripe-cli              # Windows
```
Forward webhooks:

``` bash
stripe listen --forward-to localhost:8080/api/payments/webhook
```
Test payment confirmation::
```bash
stripe payment_intents confirm pi_3RrzUm2UEvzpXWoY18tA2LYx --payment-method=pm_card_visa --off-session=true
```


## 📧 Email Configuration
The system uses Thymeleaf templates for emails located in:

Configuration properties:
```
properties
spring.thymeleaf.email.prefix=classpath:/templates/email/
spring.thymeleaf.cache=false
spring.thymeleaf.encoding=UTF-8
spring.thymeleaf.mode=HTML
spring.thymeleaf.suffix=.html
```

## 🤝 Contributing
Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

## 📜 License
Distributed under the MIT License. See LICENSE for more information.
