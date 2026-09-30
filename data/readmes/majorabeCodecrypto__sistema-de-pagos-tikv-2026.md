# Uniswap Token Swapper dApp

A web application for swapping tokens (DAI ↔ WETH) using Uniswap V2 on a local Ethereum fork (Anvil).

## Prerequisites

- Node.js 18+
- MetaMask or compatible Web3 wallet installed in your browser
- Anvil (from Foundry) for local Ethereum fork

## Setup

### 1. Start Anvil Fork

```bash
anvil --fork-url https://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
```

This creates a local fork of Ethereum mainnet on `http://localhost:8545` with chainId `31337`.

### 2. Install Dependencies

```bash
npm install
```

### 3. Setup Environment Variables

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

The defaults in `.env.local` should work for local development with Anvil.

### 4. Start Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Funding Test Accounts with Tokens

### Deposit ETH → WETH

Before you can swap, you need WETH. Use these commands to deposit ETH into the WETH contract:

#### Option 1: Direct Deposit (Recommended for first time)

```bash
# Impersonate account 0 to deposit 100 ETH worth of WETH
cast rpc anvil_impersonateAccount 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266

# Send ETH to account 0 to pay for gas
cast send 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 --value 1000ether --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb476cadcccea5967f6456925f9a6

# Call deposit() on WETH contract with 100 ETH
cast send 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 "deposit()" --value 100ether --from 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 --rpc-url http://localhost:8545

# Stop impersonation
cast rpc anvil_stopImpersonatingAccount 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
```

#### Option 2: Using Private Key

If you prefer to use a specific test account:

```bash
# Deposit 100 ETH as WETH from test account
cast send 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 "deposit()" \
  --value 100ether \
  --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb476cadcccea5967f6456925f9a6 \
  --rpc-url http://localhost:8545
```

### Verify Token Balances

Check your WETH balance:

```bash
# Check WETH balance (18 decimals)
cast call 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 "balanceOf(address)(uint256)" 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 --rpc-url http://localhost:8545
```

Check DAI balance:

```bash
# Check DAI balance (18 decimals)
cast call 0x6B175474E89094C44Da98b954EedeAC495271d0F "balanceOf(address)(uint256)" 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 --rpc-url http://localhost:8545
```

## Token Addresses (Mainnet fork)

- **WETH**: `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`
- **DAI**: `0x6B175474E89094C44Da98b954EedeAC495271d0F`
- **USDC**: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`

## Uniswap Smart Contracts (Mainnet fork)

- **V2 Router**: `0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D`
- **V2 Factory**: `0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f`
- **V3 Router**: `0xE592427A0AEce92De3Edee1F18E0157C05861564` (not available on all forks)

## Using the dApp

1. **Connect Wallet**: Click "Connect Wallet" button in header to connect MetaMask
2. **Select Tokens**: Choose "From" and "To" tokens (default: DAI → WETH)
3. **Enter Amount**: Type the amount you want to swap
4. **Review Price**: Check the estimated output and slippage tolerance
5. **Confirm**: Click "Swap" and approve the transaction in MetaMask
6. **Wait**: Transaction will be confirmed on-chain

## Useful Cast Commands

### General Network Info

```bash
# Get current block number
cast block-number --rpc-url http://localhost:8545

# Get chain ID
cast chain-id --rpc-url http://localhost:8545

# Get gas price
cast gas-price --rpc-url http://localhost:8545
```

### ERC20 Token Operations

```bash
# Get token balance (replace ADDRESS with your address)
cast call TOKEN_ADDRESS "balanceOf(address)(uint256)" ADDRESS --rpc-url http://localhost:8545

# Get token allowance
cast call TOKEN_ADDRESS "allowance(address,address)(uint256)" OWNER_ADDRESS SPENDER_ADDRESS --rpc-url http://localhost:8545

# Approve tokens for spending
cast send TOKEN_ADDRESS "approve(address,uint256)" SPENDER_ADDRESS AMOUNT --private-key YOUR_KEY --rpc-url http://localhost:8545

# Transfer tokens
cast send TOKEN_ADDRESS "transfer(address,uint256)" RECIPIENT_ADDRESS AMOUNT --private-key YOUR_KEY --rpc-url http://localhost:8545
```

### Query Uniswap V2

```bash
# Get reserves from a pair (DAI/WETH example)
cast call 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f "getPair(address,address)(address)" \
  0x6B175474E89094C44Da98b954EedeAC495271d0F \
  0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 \
  --rpc-url http://localhost:8545
```

## Building for Production

```bash
npm run build
```

The build must pass with no TypeScript errors. All code must compile successfully.

## Project Structure

```
web/
├── app/
│   ├── page.tsx              # Main swap interface
│   ├── layout.tsx            # Root layout with providers
│   ├── globals.css           # Global styles
│   └── providers.tsx         # Wagmi configuration
├── components/
│   ├── SwapForm.tsx          # Swap input form
│   ├── TokenSelector.tsx     # Token selection dropdown
│   ├── TransactionStatus.tsx # Transaction status display
│   ├── PriceDisplay.tsx      # Price and slippage info
│   └── WalletButton.tsx      # Wallet connection button
├── lib/
│   ├── uniswap.ts           # Uniswap V2 integration
│   ├── tokens.ts            # Token definitions
│   └── utils.ts             # Utility functions
├── types/
│   └── index.ts             # TypeScript types
└── .env.example             # Environment variables template
```

## Technology Stack

- **Frontend**: Next.js 16 with React 19
- **Web3**: viem v2 + wagmi v3
- **Styling**: Tailwind CSS + shadcn/ui
- **DEX**: Uniswap V2 Router
- **Local Fork**: Anvil (Foundry)

## Troubleshooting

### "Wallet not connected" Error

- Make sure MetaMask is installed and connected
- Verify MetaMask is connected to chainId 31337
- Check that Anvil is running on `http://localhost:8545`

### "Swap failed" Error

- Ensure you have sufficient WETH balance
- Check that slippage tolerance is reasonable
- Verify token pair has liquidity in Uniswap V2

### Balance Not Updating

- Wait a few seconds for the balance to refresh (5-second polling)
- Try refreshing the page
- Check balance directly with cast command (see above)

### No Liquidity Error

- Confirm you're using the correct token addresses
- Check Uniswap V2 has the trading pair available
- Try a different token pair if available

## Development Notes

- ChainId: `31337` (Anvil local fork)
- RPC URL: `http://localhost:8545`
- Wallet client uses viem's injected provider (window.ethereum)
- All transactions require MetaMask signature confirmation
- Supports dark/light mode

## License

MIT
