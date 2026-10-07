# Mini-projet PDO — Injection SQL

Application PHP d’authentification sécurisée par requête PDO préparée, basée sur `sql_injection.user`.

## Installation sur linserv

1. Dans phpMyAdmin, créer la base **`pj509414_sql_injection`** si elle n’existe pas.
2. Importer `db_simple.sql`. Si phpMyAdmin interdit `CREATE DATABASE` ou `USE`, retirer les deux premières lignes et importer le reste après avoir sélectionné la base.
3. Copier `config.example.php` vers `config.local.php`.
4. Renseigner dans `config.local.php` le nom exact de la base, le login et le mot de passe linserv.
5. Déposer le projet dans le répertoire web et ouvrir `index.php`.

`config.local.php` est ignoré par Git afin de ne pas publier le mot de passe.

## Comptes pédagogiques

- `Satya` / `SatyaPwd`
- `Prakash` / `PrakashPwd`

Les mots de passe en clair sont imposés par le jeu de données du TD. En production, utiliser `password_hash()` à l’inscription et `password_verify()` à la connexion, comme expliqué dans `responses.md`.

## Fichiers principaux

- `index.php` : formulaire de connexion ;
- `auth.php` : validation et authentification préparée ;
- `dashboard.php` : espace protégé ;
- `logout.php` : déconnexion protégée par jeton CSRF ;
- `pdo.php` : connexion PDO ;
- `db_simple.sql` : schéma et données corrigés ;
- `responses.md` : réponses du TD.
