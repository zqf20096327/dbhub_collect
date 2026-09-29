# Vue 3 SQLite Playground

![Vue SQLite Playground](./public/vue-3-playground.png)

A modern Vue.js application demonstrating how to use SQLite in the browser through WebAssembly. This project showcases building offline-capable applications with a real SQL database running entirely in the browser.

## Features

- 🗄️ Full SQLite database in the browser via WebAssembly
- 📁 **CSV Import** - Import CSV files directly into SQLite tables
- 🚀 [Vue 3.5](https://vuejs.org/) with Composition API
- ⚡️ [Vite 5](https://vitejs.dev/) for development
- 🎯 [TypeScript 5.6](https://www.typescriptlang.org/) for type safety
- 💾 Persistent storage using Origin Private File System (OPFS)
- 🧵 Background processing with Web Workers
- 🎨 [TailwindCSS 3](https://tailwindcss.com/) for styling

## Key Technologies

- **SQLite Wasm**: SQLite compiled to WebAssembly for browser execution
- **Web Workers**: Background thread for database operations
- **OPFS**: Persistent storage for database files
- **@sqlite.org/sqlite-wasm**: Official SQLite WebAssembly package

## Prerequisites

- Node.js (version 20.x or higher)
- Modern browser with WebAssembly and OPFS support
- npm (comes with Node.js)

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/vue-sqlite-playground.git
   cd vue-sqlite-playground
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

4. Open your browser and visit `http://localhost:5173`

## Features Demo

- Create and manage SQLite databases in the browser
- **Import CSV files** into SQLite tables with transaction support
- Execute SQL queries directly in the UI
- View query results in real-time
- Persistent storage across browser sessions
- Example CRUD operations

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint and fix files
- `npm run type-check` - Check TypeScript types

## Browser Support

This application requires a modern browser with support for:

- WebAssembly
- Web Workers
- Origin Private File System (OPFS)
- SharedArrayBuffer

## Technical Details

### Database Configuration

The SQLite database is configured with a sample table structure:

```sql
CREATE TABLE IF NOT EXISTS test_table (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### CSV Import

The application includes a powerful CSV import feature that allows you to import data from CSV files directly into SQLite tables:

**Features:**
- Browser-based CSV parsing (no server required)
- Transaction-wrapped imports for data integrity
- Automatic rollback on errors
- Real-time progress and error reporting
- Support for custom table names and column mappings

**How it works:**
1. Navigate to the **CSV Import** page
2. Specify your table name and column names (comma-separated)
3. Select a CSV file from your computer
4. The file is parsed in JavaScript and inserted using parameterized SQL queries
5. All inserts are wrapped in a transaction for performance and consistency
6. View imported data immediately in the table preview

**Example CSV format:**
```csv
id,name
1,Alice Johnson
2,Bob Smith
3,Charlie Davis
```

**Important Notes:**
- CSV files must have a header row
- Column names must match the order in your CSV file
- SQLite CLI dot commands (`.import`, `.mode csv`) don't work in the browser - this JavaScript-based approach provides equivalent functionality
- For complex CSVs with quoted fields or special characters, consider using a library like [Papa Parse](https://www.papaparse.com/)

**Download Sample CSV:**
A sample `users.csv` file is included in the `public/` directory for testing.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

[MIT](./LICENSE)

## Learn More

For a detailed explanation of how this works, check out our [blog post](https://your-blog-post-url) about implementing SQLite in Vue 3 applications.
