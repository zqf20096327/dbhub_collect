# Gacha Dev

**Gacha Dev** is a gamified knowledge-sharing application that turns learning software engineering into a fun, collectible experience.

Users spin a virtual "Gachapon" machine to receive random "knowledge capsules" (tidbits). Each capsule contains a bite-sized explanation of a concept, code snippet, or best practice, powered by Google's Gemini AI.

## Features

-   **Interactive Gachapon Machine**: A playful, animated interface to "spin" for new knowledge.
-   **AI-Powered Content**: Generates unique, high-quality engineering tips on-the-fly using **Google Gemini 2.5 Flash**.
-   **Categories**: Filter tidbits by domain:
    -   Frontend
    -   Backend
    -   DevOps
    -   Mobile
    -   Security
    -   Soft Skills
-   **Collection System**: Automatically saves your unlocked tidbits to a local history for future reference.
-   **Visual Stats**: Track your learning progress across different categories.

## Tech Stack

-   **Framework**: [React](https://react.dev/) (v19) + [Vite](https://vitejs.dev/)
-   **Styling**: [Tailwind CSS](https://tailwindcss.com/)
-   **AI Integration**: [Google GenAI SDK](https://www.npmjs.com/package/@google/genai)
-   **Icons**: [Lucide React](https://lucide.dev/)
-   **Charts**: [Recharts](https://recharts.org/)

## Getting Started

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Set up Environment Variables (Optional)**:
    Create a `.env.local` file and add your Gemini API key:
    ```env
    VITE_GEMINI_API_KEY=your_api_key_here
    ```
    *Alternatively, you can configure the API key directly in the application UI.*

4.  **Run the development server**:
    ```bash
    npm run dev
    ```

## API Key Configuration

You can configure your Google Gemini API key in two ways:

1.  **Environment Variable**: Set `VITE_GEMINI_API_KEY` in your `.env.local` file. This is recommended for local development.
2.  **UI Configuration**: Click the **Settings** (gear icon) in the top-right corner of the application to enter your API key manually. The key is stored securely in your browser's LocalStorage. This is useful for deployed versions where you cannot set environment variables.
