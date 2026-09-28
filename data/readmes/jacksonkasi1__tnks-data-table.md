# Advanced Data Table Component

> [!IMPORTANT]
> **Recommendation:** Check out **[TableCraft](https://github.com/jacksonkasi1/TableCraft)**! It is the spiritual successor to this repository, offering almost all the same functionality but with a vastly simplified, adapter-driven architecture that is easier to use and maintain.

**Compatible with:** Next.js, Vite, Remix, TanStack Start, and all modern React frameworks.  
👉 **Check out the [Vite Example Repository](https://github.com/jacksonkasi1/tnks-table-vite-example) for a quick integration guide.**

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/jacksonkasi1/tnks-data-table)

> **📖 Complete Documentation:** **[tnks-docs.vercel.app/docs](https://tnks-docs.vercel.app/docs)** - Comprehensive guides, API reference, and interactive examples built with Fumadocs.

**Version:** 0.5.0
**Updated:** 2026-02-08
**Author:** Jackson Kasi

---

## 🔗 Quick Links

- **📚 Live Documentation:** [tnks-docs.vercel.app/docs](https://tnks-docs.vercel.app/docs)
- **📂 Documentation Repo:** [github.com/jacksonkasi1/tnks-docs](https://github.com/jacksonkasi1/tnks-docs)
- **🚀 Live Demo:** [tnks-data-table.vercel.app](https://tnks-data-table.vercel.app)
- **📦 NPM Package:** Coming soon
- **💬 Discussions:** [GitHub Discussions](https://github.com/jacksonkasi1/tnks-data-table/discussions)

---

## ❤️ Support This Project

If you find this project helpful, consider supporting its development!

[![GitHub Sponsors](https://img.shields.io/badge/sponsor-jacksonkasi1-blue?style=flat-square&logo=github)](https://github.com/sponsors/jacksonkasi1)

Your support helps maintain and improve this component. Every contribution matters! 🚀

---

## Quick Start

Install the data table component with a single command using Shadcn CLI:

```bash
# Install required Shadcn UI components first
npx shadcn@latest init
npx shadcn@latest add button checkbox input select popover calendar dropdown-menu separator table command

# Install the data-table component
npx shadcn@latest add https://tnks-data-table.vercel.app/r/data-table.json

# Install the calendar-date-picker (required dependency)
npx shadcn@latest add https://tnks-data-table.vercel.app/r/calendar-date-picker.json
```

**Important:** You must add the table styles to your `globals.css` for proper functionality. [Get the styles here](#2-configure-styles).

That's it! See [Installation & Setup](#installation--setup) for detailed installation options.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features Overview](#features-overview)
3. [File Structure](#file-structure)
4. [Installation & Setup](#installation--setup)
5. [Basic Usage](#basic-usage)
6. [Core Components](#core-components)
7. [API Integration](#api-integration)
8. [Advanced Configuration](#advanced-configuration)
   - [Column Configuration](#column-configuration)
   - [Default Sort Configuration](#default-sort-configuration)
   - [Row Actions](#row-actions)
   - [Filtering & Sorting](#filtering--sorting)
   - [Pagination](#pagination)
   - [Date Range Filtering](#date-range-filtering)
   - [Row Selection](#row-selection)
   - [Row Click Handling](#row-click-handling)
   - [Toolbar Customization](#toolbar-customization)
   - [Export Options](#export-options)
   - [Case Format Support](#case-format-support)
   - [Export Data Transformation](#export-data-transformation)
   - [Subrows Feature (Hierarchical Data)](#subrows-feature-hierarchical-data)
9. [Server Implementation](#server-implementation)
   - [API Endpoints](#api-endpoints)
   - [Request & Response Formats](#request--response-formats)
   - [Error Handling](#error-handling)
10. [Popups & Modals](#popups--modals)
11. [Customization](#customization)
12. [Performance Optimization](#performance-optimization)
13. [Best Practices](#best-practices)
14. [Troubleshooting](#troubleshooting)
15. [Complete API Reference](#complete-api-reference)
16. [Example Implementations](#example-implementations)

---

## Introduction

The

[...截断...]

 Advanced Data Table component is a highly configurable and feature-rich table implementation built on top of Shadcn UI components and TanStack Table (React Table v8). It is fully compatible with all modern React frameworks including **Next.js**, **Vite**, **Remix**, **TanStack Start**, and others. It's designed to handle enterprise-level requirements including complex data operations, server-side processing, and customizable UI elements.

This documentation provides comprehensive guidance on how to implement, configure, and extend the data table for your specific needs regardless of your chosen framework.

## Server

Check out the [API development document](./src/SERVER.md) to understand the default configuration for this table.

### Key Benefits

- **Framework Agnostic**: Works seamlessly with Next.js, Vite, Remix, TanStack Start, etc.
- **TypeScript Support**: Fully typed components for better developer experience
- **Modular Architecture**: Easily extendable and customizable
- **Server Integration**: Built-in support for server-side operations
- **Accessibility**: Follows WCAG guidelines for accessible tables
- **Performance Optimized**: Efficient rendering even with large datasets
- **Responsive Design**: Works across various screen sizes
- **Theming Support**: Customizable appearance with Tailwind CSS

---

## Features Overview

The Data Table includes the following features:

### Data Management

- ✅ Server-side pagination
- ✅ Server-side sorting
- ✅ Server-side filtering
- ✅ Single & multi-row selection
- ✅ Row click callbacks for navigation
- ✅ Optimistic UI updates
- ✅ **Hierarchical data with subrows** (expandable nested rows)
- ✅ **Cross-page subrow selection** and export

### UI Features

- ✅ Responsive layout
- ✅ Column resizing
- ✅ Column visibility toggle
- ✅ Date range filtering
- ✅ Search functionality
- ✅ Customizable toolbar
- ✅ Row actions menu
- ✅ Bulk action support
- ✅ **Expand/collapse rows** with smooth animations
- ✅ **Three subrow rendering modes** (same-columns, custom-columns, custom-component)

### Operations

- ✅ Add new records
- ✅ Edit existing records
- ✅ Delete single records
- ✅ Bulk delete operations
- ✅ Data export (CSV/Excel) with custom formatting
- ✅ Export data transformation and new calculated columns

### Integration

- ✅ React Query data fetching
- ✅ Zod validation
- ✅ Form handling with React Hook Form
- ✅ Toast notifications
- ✅ URL state persistence
- ✅ Case format conversion (snake_case ↔ camelCase)
- ✅ Flexible API parameter mapping

---

## File Structure

The data table implementation follows a modular structure to separate concerns and improve maintainability. Below is the recommended file structure for implementing the data table in your project:

```sh
src/
├── api/                       # API integration layer
│   └── entity/                # Entity-specific API functions
│       ├── add-entity.ts      # Create operation
│       ├── delete-entity.ts   # Delete operation
│       ├── fetch-entities.ts  # List operation with filters
│       └── fetch-entity-by-ids.ts # Fetch specific entities
│
├── components/                # Shared UI components
└── 📁data-table               # Core data table components
    └── 📁hooks                # Custom React hooks for data-table
        └── use-table-column-resize.ts  # Hook for managing column resize state and persistence
    └── 📁utils                # Utility functions and helpers
        └── column-sizing.ts   # Functions for calculating and managing column widths
        └── conditional-state.ts # Logic for conditional rendering and state transitions
        └── date-format.ts     # Date formatting and manipulation utilities
        └── deep-utils.ts      # Deep object comparison and manipulation
        └── export-utils.ts    # Utilities for data export (CSV/Excel)
        └── index.ts           # Export barrel file for utilities
        └── keyboard-navigation.ts # Keyboard navigation and accessibility
        └── search.ts  