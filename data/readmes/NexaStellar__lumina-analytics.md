# Lumina Analytics

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Stellar](https://img.shields.io/badge/Stellar-Analytics-purple)](https://stellar.org)

Real-time analytics and monitoring dashboard for the Stellar network. Track transactions, accounts, assets, DEX activity, and Soroban contract interactions with beautiful visualizations and powerful insights.

## 🌟 Features

- **📊 Real-Time Dashboard**: Live metrics and transaction monitoring
- **🔍 Transaction Explorer**: Deep dive into any Stellar transaction
- **💰 Asset Analytics**: Track asset issuance, distribution, and trading
- **📈 DEX Monitoring**: Real-time orderbook and trade analytics
- **🤖 Soroban Insights**: Smart contract activity and gas usage
- **⚡ Network Health**: Node status, ledger metrics, and performance
- **📱 Responsive Design**: Works beautifully on desktop, tablet, and mobile
- **🔔 Alerts**: Custom alerts for specific events or thresholds
- **📥 Data Export**: Export analytics data to CSV/JSON
- **🎨 Customizable**: Create custom dashboards and widgets

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Lumina Analytics                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  Frontend (React + TypeScript)                  │
│  ├── Dashboard                                  │
│  ├── Transaction Explorer                       │
│  ├── Asset Analytics                            │
│  └── Network Monitor                            │
│                                                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  Backend (Node.js + PostgreSQL)                 │
│  ├── Horizon API Integration                    │
│  ├── Soroban RPC Integration                    │
│  ├── Data Aggregation Engine                    │
│  ├── WebSocket Server (Real-time)              │
│  └── REST API                                   │
│                                                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  Database Layer                                  │
│  ├── TimescaleDB (Time-series data)            │
│  ├── Redis (Caching & Real-time)               │
│  └── PostgreSQL (Relational data)              │
│                                                  │
└─────────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│  Horizon API    │  │  Soroban RPC    │
│  (Stellar)      │  │  (Contracts)    │
└─────────────────┘  └─────────────────┘
```

## 📋 Prerequisites

- [Node.js](https://nodejs.org/) v18 or higher
- [Docker](https://www.docker.com/) & Docker Compose (recommended)
- [PostgreSQL](https://www.postgresql.org/) 14+ (if not using Docker)
- [Redis](https://redis.io/) 7+ (if not using Docker)

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/NexaStellar/lumina-analytics.git
cd lumina-analytics

# Start all services
docker-compose up -d

# Access the dashboard
open http://localhost:3000
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/NexaStellar/lumina-analytics.git
cd lumina-analytics

# Install backend dependencies
cd backend
npm install

# Setup database
npm run db:migrate
npm run db:seed

# Start backend
npm run dev

# In a new terminal, install frontend dependencies
cd ../frontend
npm install

# Start frontend
npm run dev
```

## 🎯 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/lumina
REDIS_URL=redis://localhost:6379

# Stellar Network
HORIZON_URL=https://horizon-testnet.stellar.org
SOROBAN_RPC_URL=https://soroban-testnet.stellar.org
NETWORK=testnet

# API
API_PORT=4000
API_HOST=0.0.0.0

# WebSocket
WS_PORT=4001

# Features
ENABLE_ALERTS=true
ENABLE_DATA_EXPORT=true
```

Frontend `.env`:

```bash
VITE_API_URL=http://localhost:4000
VITE_WS_URL=ws://localhost:4001
VITE_NETWORK=testnet
```

## 📖 Usage

### Dashboard

The main dashboard provides an overview of:
- Transaction volume (24h, 7d, 30d)
- Active accounts
- Top assets by volume
- Recent transactions
- Network health metrics

### Transaction Explorer

Search and analyze any transaction:
```
https://lumina.nexastellar.dev/tx/TRANSACTION_HASH
```

Features:
- Transaction details and metadata
- Operation breakdown
- Fee analysis
- Related transactions

### Asset Analytics

Track any Stellar asset:
```
https://lumina.nexastellar.dev/asset/ASSET_CODE:ISSUER
```

View:
- Supply and distribution
- Holder statistics
- Trading volume
- Price history (if available)
- Trustline growth

### DEX Monitor

Monitor decentralized exchange activity:
- Order book depth
- Recent trades
- Volume by asset pair
- Spread analysis
- Liquidity pools

### Soroban Analytics

Contract interaction metrics:
- Contract invocations
- Gas usage patterns
- Most active contracts
- Event logs
- Storage analysis

## 🔌 API

### REST Endpoints

```typescript
// Get network statistics
GET /api/v1/stats

// Get transaction by hash
GET /api/v1/transactions/:hash

// Get account details
GET /api/v1/accounts/:publicKey

// Get asset information
GET /api/v1/assets/:code/:issuer

// Get contract activity
GET /api/v1/contracts/:contractId

// Search
GET /api/v1/search?q=:query
```

### WebSocket Events

```typescript
// Subscribe to real-time transactions
ws://localhost:4001/stream/transactions

// Subscribe to ledger closes
ws://localhost:4001/stream/ledgers

// Subscribe to specific account
ws://localhost:4001/stream/accounts/:publicKey

// Subscribe to contract events
ws://localhost:4001/stream/contracts/:contractId
```

## 📁 Project Structure

```
lumina-analytics/
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── hooks/           # Custom hooks
│   │   ├── services/        # API services
│   │   ├── utils/           # Utilities
│   │   └── types/           # TypeScript types
│   ├── public/
│   └── package.json
├── backend/
│   ├── src/
│   │   ├── api/             # REST API routes
│   │   ├── services/        # Business logic
│   │   │   ├── horizon.ts   # Horizon integration
│   │   │   ├── soroban.ts   # Soroban RPC
│   │   │   ├── indexer.ts   # Data indexing
│   │   │   └── analytics.ts # Analytics engine
│   │   ├── db/              # Database models
│   │   ├── ws/              # WebSocket server
│   │   └── utils/           # Utilities
│   ├── migrations/          # DB migrations
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🧪 Testing

```bash
# Backend tests
cd backend
npm test

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e

# Load testing
npm run test:load
```

## 📊 Metrics Collected

### Transaction Metrics
- Transaction count and volume
- Operation distribution
- Fee statistics
- Success/failure rates

### Account Metrics
- New account creation rate
- Account balance distribution
- Active account trends
- Trust line statistics

### Asset Metrics
- Asset creation and issuance
- Trading volume
- Holder count
- Distribution patterns

### Network Metrics
- Ledger close time
- Transaction throughput
- Operation counts
- Fee pool statistics

### Soroban Metrics
- Contract deployments
- Invocation counts
- Gas consumption
- Event emission rates

## 🎨 Customization

### Custom Dashboard Widgets

```typescript
// Create custom widget
import { Widget } from '@lumina/dashboard';

export const MyCustomWidget: Widget = {
  id: 'custom-widget',
  title: 'My Custom Metric',
  fetch: async () => {
    // Fetch your data
  },
  render: (data) => {
    // Render your visualization
  },
};
```

### Custom Alerts

```typescript
// Define custom alert
{
  name: 'High Transaction Volume',
  condition: {
    metric: 'transactions.count',
    operator: '>',
    threshold: 1000,
    window: '1h',
  },
  actions: [
    { type: 'email', to: 'alerts@example.com' },
    { type: 'webhook', url: 'https://...' },
  ],
}
```

## 🔒 Security

- API rate limiting
- CORS configuration
- Input validation
- SQL injection prevention
- XSS protection
- Authentication (optional)

## 🚢 Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment

```bash
# Build frontend
cd frontend
npm run build

# Serve with nginx or similar
# Configure reverse proxy to backend

# Start backend in production
cd backend
npm run build
NODE_ENV=production npm start
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

### Development Workflow

1. Fork the repository
2. Create feature branch
3. Make changes and write tests
4. Run linters and tests
5. Submit pull request

## 🗺️ Roadmap

- [x] Real-time transaction monitoring
- [x] Asset analytics
- [x] DEX monitoring
- [x] Basic Soroban integration
- [ ] Advanced contract analytics
- [ ] Machine learning insights
- [ ] Mobile app (React Native)
- [ ] Public API with authentication
- [ ] Embeddable widgets
- [ ] Historical data analysis tools

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🔗 Links

- [Live Demo](https://demo.lumina.nexastellar.dev)
- [Developer documentation](https://nexastellar.github.io/lumina-analytics/)
- [API Docs](https://api.lumina.nexastellar.dev/docs)
- [Report Issues](https://github.com/NexaStellar/lumina-analytics/issues)

The documentation site is maintained in [`docs/`](docs/). GitHub Pages must be enabled with **GitHub Actions** as the build and deployment source.

## 💬 Community

- [Discord](https://discord.gg/nexastellar)
- [Twitter](https://twitter.com/nexastellar)
- [Telegram](https://t.me/nexastellar)

## 🙏 Acknowledgments

Built for the Stellar ecosystem. NexaStellar intends to apply this repository to the Drips Wave program; approval is pending.

Special thanks to:
- Stellar Development Foundation
- The Horizon and Soroban teams
- All our contributors

---

**Maintained by NexaStellar** | [Website](https://nexastellar.dev) | [GitHub](https://github.com/NexaStellar)
