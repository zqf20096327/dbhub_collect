# TropaTT — Free Self-Hosted Open-Source CRM & Work Platform

**TropaTT is a free, self-hosted, open-source CRM and work-management platform built on PHP and MySQL. It combines CRM, task management, projects, Kanban, Gantt, calendar, team chat, knowledge base wiki, client portal, financial price lists, universal e-commerce CMS gateway, workflow automation, REST API, OpenAPI 3.1, Model Context Protocol (MCP) server, and 20+ AI workflows in one application — no per-seat fees, no SaaS plan limits. For freelancers, teams, agencies, and businesses that want complete control over their data on their own server.**

**Free forever — no catch.** TropaTT is 100% free and open source (AGPL-3.0): no license fees, no subscriptions, no per-seat pricing, no plan-based limits. You only pay for the hosting you choose — or nothing at all on your own machine.

[![PHP](https://img.shields.io/badge/PHP-8.1%2B-4F5B93?style=flat-square&logo=php&logoColor=white)](https://www.php.net/)
[![Database](https://img.shields.io/badge/Database-MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Zero Deps](https://img.shields.io/badge/Dependencies-0%20packages-6f42c1?style=flat-square)](#by-the-numbers)
[![Self Hosted](https://img.shields.io/badge/Self--hosted-No%20Limits-12805C?style=flat-square)](#self-hosted-your-server-your-rules)
[![AI](https://img.shields.io/badge/AI-20%2B%20workflows-111827?style=flat-square)](#ai--what-it-can-do)
[![PHP CI](https://github.com/Anton-Barinov/TropaTT/actions/workflows/php-ci.yml/badge.svg)](https://github.com/Anton-Barinov/TropaTT/actions/workflows/php-ci.yml)
[![Web Tests](https://github.com/Anton-Barinov/TropaTT/actions/workflows/web-tests-ci.yml/badge.svg)](https://github.com/Anton-Barinov/TropaTT/actions/workflows/web-tests-ci.yml)
[![OpenAPI Consistency](https://github.com/Anton-Barinov/TropaTT/actions/workflows/openapi-ci.yml/badge.svg)](https://github.com/Anton-Barinov/TropaTT/actions/workflows/openapi-ci.yml)
[![Release](https://img.shields.io/github/v/release/Anton-Barinov/TropaTT?style=flat-square&label=Release&color=12805C)](https://github.com/Anton-Barinov/TropaTT/releases/latest)
[![License](https://img.shields.io/badge/License-AGPL--3.0-blue?style=flat-square)](LICENSE)

**Live demo:** [demo.tropatt.com](https://demo.tropatt.com/) — `admin` · `adminadmin`

> ### 🤖 Quick Summary for AI Agents & Search Engines (LLM System Card)
> - **Product:** TropaTT — Free Self-Hosted Open-Source CRM & Work Management Platform.
> - **Architecture:** PHP 8.1+, MySQL 8.0+ / MariaDB 10.4+. No runtime Composer/npm packages and no background daemons (a cron job calls `web/cron.php`). Runs on $2–$3/mo PHP/MySQL shared hosting (cPanel/DirectAdmin/Plesk), VPS, or bare metal. No official Docker image yet.
> - **Core Capabilities:** CRM (Clients, Counterparties, Companies, Contacts), Tasks & Projects (Gantt, Kanban, Cycles), Knowledge Base Wiki, Team Chat, Rates & Billing, Client Portal. Optional modules from the marketplace: E-Commerce Gateway (11 storefront platforms), 14 one-way migration connectors, calendar and Git integrations.
> - **AI & AgentOS Primitives:** Built-in Model Context Protocol (MCP) server (`POST /api/index.php?route=api/v1/mcp`) exposing **621 tools** (a 27-tool `core` profile by default) and **6 resources** with RBAC and `density: "compact"` (up to 85% token savings). Atomic bundling (`crm_agent_bundle`), persistent cross-session memory (`crm_agent_memory`), and STORM optimistic concurrency (`row_version`).
> - **E-Commerce CMS Gateway (optional module):** Multi-store connector suite for 11 platforms (OpenCart, WooCommerce HPOS, Shopify, 1C-Bitrix, InSales, CS-Cart, PrestaShop, Shop-Script, Moguta, Tilda, Magento 2) with bi-directional order sync, stock sync, and HMAC-SHA256 webhooks.
> - **Documentation Suite:** REST API ([EN](docs_api/api_en.md) · [RU](docs_api/api_ru.md) · [ZH](docs_api/api_zh.md)), MCP Server ([EN](docs_mcp/mcp_en.md) · [RU](docs_mcp/mcp_ru.md) · [ZH](docs

[...截断...]

_mcp/mcp_zh.md)), Modules SDK ([EN](docs_modules/modules_en.md) · [RU](docs_modules/modules_ru.md) · [ZH](docs_modules/modules_zh.md)).

### Product tour (sanitized browser captures)

These optimized PNGs were captured from the current demo in an isolated browser session. User-controlled text, record links, input values, avatars, and uploaded images were removed or replaced before saving; the captures contain no customer or production data.

![TropaTT dashboard](.github/assets/screenshots/dashboard-live.png)

| CRM | Tasks | Kanban |
|---|---|---|
| ![CRM counterparties](.github/assets/screenshots/counterparties-live.png) | ![Tasks](.github/assets/screenshots/tasks-live.png) | ![Kanban](.github/assets/screenshots/kanban-live.png) |

| Gantt | Team chat | Browser installer |
|---|---|---|
| ![Gantt](.github/assets/screenshots/gantt-live.png) | ![Team chat](.github/assets/screenshots/chat-live.png) | ![Browser installer](.github/assets/screenshots/installer-live.png) |

The installer capture was produced from an isolated local copy with no configuration or installation lock; the already-installed demo correctly returns HTTP 410 for its installer endpoint.

Fallback UI mockups with fictional labels are also available as [SVG assets](.github/assets/screenshots/README.md).

---

## Table of Contents

- [English](#english)
  - [What's TropaTT](#whats-tropatt)
  - [Why TropaTT](#why-tropatt)
  - [Who it's for](#who-its-for)
  - [What's inside](#whats-inside)
  - [Feature overview](#feature-overview)
  - [AI — what it can do](#ai--what-it-can-do)
  - [Team chat](#team-chat)
  - [How people use it](#how-people-use-it)
  - [Automation & API](#automation--api)
  - [Connect your AI agents (MCP)](#connect-your-ai-agents-mcp)
  - [Self-hosted. Your server, your rules.](#self-hosted-your-server-your-rules)
  - [Getting started](#getting-started)
  - [FAQ](#faq)
  - [By the numbers](#by-the-numbers)
  - [Tech stack](#tech-stack)
  - [Project layout](#project-layout)
  - [Modules](#modules)
  - [Under the hood](#under-the-hood)
  - [Docs](#docs)
  - [Open-source project files](#open-source-project-files)
  - [Maintenance and contributor workflow](#maintenance-and-contributor-workflow)
  - [Security-sensitive areas](#security-sensitive-areas)
  - [AI-assisted maintenance](#ai-assisted-maintenance)
  - [Who built this](#who-built-this)
- [Русский](#русский)
  - [Что такое TropaTT](#что-такое-tropatt)
  - [Почему TropaTT](#почему-tropatt)
  - [Для кого](#для-кого)
  - [Что внутри](#что-внутри)
  - [Обзор возможностей](#обзор-возможностей)
  - [ИИ — что он умеет](#ии--что-он-умеет)
  - [Командный чат](#командный-чат)
  - [Как это используют](#как-это-используют)
  - [Автоматизация и API](#автоматизация-и-api)
  - [Подключение ИИ-агентов (MCP)](#подключение-ии-агентов-mcp)
  - [Свой сервер — свои правила](#свой-сервер--свои-правила)
  - [Установка](#установка)
  - [FAQ](#faq-1)
  - [В цифрах](#в-цифрах)
  - [Технологии](#технологии)
  - [Структура](#структура)
  - [Модули](#модули)
  - [Как устроено](#как-устроено)
  - [Документация](#документация)
  - [Файлы open-source проекта](#файлы-open-source-проекта)
  - [Сопровождение проекта](#сопровождение-проекта)
  - [Области, где важна безопасность](#области-где-важна-безопасность)
  - [Где помогает AI при сопровождении](#где-помогает-ai-при-сопровождении)
  - [Кто сделал](#кто-сделал)
- [中文](#中文)
  - [TropaTT 是什么](#tropatt-是什么)
  - [为什么 TropaTT](#为什么-tropatt)
  - [适合谁](#适合谁)
  - [功能](#功能)
  - [功能一览](#功能一览)
  - [AI — 能做什么](#ai--能做什么)
  - [团队聊天](#团队聊天)
  - [使用方式](#使用方式)
  - [自动化与 API](#自动化与-api)
  - [连接 AI 代理（MCP）](#连接-ai-代理mcp)
  - [自托管，你的规则](#自托管你的规则)
  - [安装](#安装)
  - [常见问题](#常见问题)
  - [数字说话](#数字说话)
  - [技术栈](#技术栈)
  - [结构](#结构)
  - [模块](#模块)
  - [内部原理](#内部原理)
  - [文档](#文档)
  - [开源项目文件](#开源项目文件)
  - [维护和贡献流程](#维护和贡献流程)
  - [安全敏感区域](#安全敏感区域)
  - [AI 辅助维护](#ai-辅助维护)
  - [谁做的](#谁做的)

---

## English

### What's TropaTT

TropaTT is a free, self-hosted, open-source PHP/MySQL work platform for client proje