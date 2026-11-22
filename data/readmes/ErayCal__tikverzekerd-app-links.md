# tikverzekerd-app-links

Statische site voor `app.tikverzekerd.nl` (GitHub Pages). Ze bevat alleen wat de Android-app van Assurantie CRM nodig heeft om in te loggen via een geverifieerde App Link:

- `.well-known/assetlinks.json`: welke app (pakketnaam en certificaat) bij dit domein hoort. Nu nog leeg. Het acceptatiepakket komt erbij zodra de ondertekeningssleutel voor acceptatie er is. Nooit een debug- of ontwikkelsleutel.
- `index.html` en `404.html`: statisch, zonder scripts of externe bronnen.
- `.nojekyll`: anders slaat GitHub Pages de map `.well-known` over.

Een wijziging hier is een beveiligingswijziging: wie deze site of het DNS-record beheert, bepaalt welke app de login-codes ontvangt. Alleen na review, met 2FA op GitHub en bij de DNS-aanbieder.
