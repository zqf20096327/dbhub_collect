<div align="center">

<h1>STRATAGEMA</h1>

**Движок бэктестинга торговых стратегий на данных MOEX**

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![httpx](https://img.shields.io/badge/httpx-0.28-2A6DB2?logo=python&logoColor=white)
![MOEX ISS](https://img.shields.io/badge/data-MOEX_ISS-1E4C8A)

<sub>в планах:</sub>
![FastAPI](https://img.shields.io/badge/FastAPI-planned-lightgrey?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-planned-lightgrey?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-planned-lightgrey?logo=sqlalchemy&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-planned-lightgrey?logo=docker&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-planned-lightgrey?logo=pytest&logoColor=white)

</div>

---

## Что это такое

**STRATAGEMA** отвечает на вопрос: *«а сработала бы моя торговая идея на реальной истории рынка?»*

Пользователь пишет класс-стратегию, движок берёт исторические дневные свечи с Московской биржи, проигрывает их день за днём и считает, сколько бы стратегия заработала или потеряла с учётом комиссий, проскальзывания.

## Прогресс

```
Общий прогресс   ███████░░░░░░░░░░░░░░░░░░░   33%
```

| # | Этап | Статус |
|:-:|------|:------:|
| 1 | Загрузчик свечей с MOEX ISS | ✅ Готов |
| 2 | Событийный движок, портфель, модель исполнения | ✅ Готов |
| 3 | Стратегии-плагины: SMA-кроссовер ✅, RSI | 🔧 В работе |
| 4 | Метрики: max drawdown, Sharpe, win rate | ⬜ Не начат |
| 5 | Сохранение свечей и прогонов в PostgreSQL | ⬜ Не начат |
| 6 | REST API на FastAPI + Swagger | ⬜ Не начат |
| 7 | Тесты на синтетических данных, Docker, CI | ⬜ Не начат |

## Запуск

```bash
pip install httpx
python main.py
```

Данные берутся из открытого [MOEX ISS API](https://iss.moex.com/iss/reference/) 

Пример вывода:

```
SBER: загружено свечей — 501
период: 2023-01-03 — 2024-12-28

стратегия: sma_cross
сделок: 12
комиссий уплачено: 587.31 ₽
итоговый капитал: 118,204.65 ₽
доходность стратегии: +18.20%
купить и держать:     +24.51%
```

## Архитектура

```
   MOEX ISS API          ┌──────────────────┐
   (открытый)  ────────▶│  datasources/    │  httpx, пагинация по 500 свечей
                         │  moex.py         │
                         └────────┬─────────┘
                                  │ list[Candle]
                                  ▼
   ┌──────────────┐   свеча   ┌──────────────────┐
   │ strategies/  │◀──────────│   engine/        │  событийный цикл,
   │ (плагины)    │──────────▶│   backtester.py  │  портфель, издержки
   └──────────────┘  Signal   └────────┬─────────┘
                                       │ Portfolio
                                       ▼
                              equity curve, сделки
```

## Ключевые решения

Во-первых, стратегия видит только текущую свечу. `Strategy.on_candle` принимает одну свечу; историю стратегия копит сама. Заглянуть в будущее нельзя, так как будущих свечей нет в области видимости.

Во-вторых, сигнал исполняется по[]() открытию следующей свечи. 

В-третьих, намерение отделено от исполнения. Стратегия возвращает `Signal`, движок решает, исполним ли он, считает количество и комиссию. Неисполнимые сигналы (покупка при открытой позиции, продажа при пустой) игнорируются.

В-четвертых, издержки вынесены в `ExecutionModel`. Проскальзывание, комиссия с оборота, минимальная комиссия за сделку, размер лота, лимит на долю объёма свечи. Меняя только эти параметры, видно, насколько стратегия чувствительна к издержкам, ведь та, что перестаёт зарабатывать при их удвоении, на реальном счёте не выживет.

## Чего модель не учитывает

Дивиденды, налоги и дивидендные гэпы; стоимость маржинального плеча; торговые паузы и аукционы открытия; изменение размера лота в истории бумаги; шорты. Если заявка упирается в лимит ликвидности, она исполняется частично, а остаток не переносится на следующую свечу.

## Структура проекта

```
stratagema/
├── app/
│   ├── datasources/
│   │   └── moex.py          # клиент MOEX ISS fetch_candles
│   ├── engine/
│   │   ├── models.py        # Candle, Signal, Trade, Portfolio
│   │   └── backtester.py    # ExecutionModel + Backtester
│   └── strategies/
│       ├── base.py          # абстрактный Strategy
│       └── sma.py           # SmaCrossStrategy
├── main.py                  # ручной прогон
└── README.md
```

