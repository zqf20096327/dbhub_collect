# SQLite - Kategoriyalar jadvali (Hierarxik) + 6 ta masala yechimi

Ushbu fayl kategoriyalarning hierarxik tuzilmasini (asosiy va ichki kategoriyalar) saqlash uchun `categories` jadvalini yaratadi, realistik test ma'lumotlarini qo'shadi va berilgan **6 ta masalani** to'liq yechib beradi.

Hozirgi sana: **20-noyabr, 2025-yil**

## Jadval tuzilishi (`categories`)

| Ustun        | Turi    | Tavsif                                      |
|--------------|---------|---------------------------------------------|
| id           | INTEGER | Avto-inkrement ID                           |
| name         | TEXT    | Kategoriya nomi                             |
| description  | TEXT    | Tavsif (ixtiyoriy)                          |
| parent_id    | INTEGER | Asosiy kategoriya ID (NULL → asosiy)        |
| created_at   | DATE    | Yaratilgan sana (default: bugun)            |

## Masalalar

1. Asosiy kategoriyalar (parent_id yo‘q)  
2. Har bir asosiy kategoriya ostida nechta ichki kategoriya bor  
3. 2024-yil 16-yanvardan keyin yaratilganlar (sana bo‘yicha)  
4. "Elektronika" ga tegishli barcha ichki kategoriyalar  
5. Nomi "lar" bilan tugaydigan kategoriyalar  
6. Eng eski 3 ta kategoriya (to‘liq ma’lumot)  

## Ishlatish

1. DB Browser for SQLite oching → New Database → `categories.db`  
2. Yuqoridagi butun kodni "Execute SQL" oynasiga joylashtiring → Run  
Yoki terminalda:

```bash
sqlite3 categories.db < categories.sql
