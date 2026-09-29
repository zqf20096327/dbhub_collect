# TidBit: Short-Form Gamified Education

## Inspiration
Kids spend hours scrolling, eagerly going through TikTok, Instagram Reels, and YouTube Shorts. These platforms capture their attention with bite-sized content, but rarely do they ever offer meaningful learning. With attention spans getting shorter and shorter, we saw an opportunity: what if kids could scroll more--but on something educational, engaging, and fun? TidBit was born from that vision.
## What it does
TidBit provides short-form, reward-based educational content tailored to each child's interests. It uses AI-powered exploration to suggest new topics, while an integrated video game layer makes learning rewarding. Our goal is to bring together the best parts of social media and gaming with the power of adaptive learning, transforming scrolling into a tool for curiosity and growth. For kids, TidBit reminds them of TikTok, fun and rewarding. For parents, it's a safe space for their kids to learn.
## How we built it
We built TidBit using React Native and Expo for an easy cross-platform mobile app experience. We then utilized Google Gemini API to generate the adaptive, personalized educational content. Finally, we utilized the OpenAI API to implement a text-to-speech feature.
## Challenges we ran into
Designing an experience that is engaging but not too overwhelming. Creating a reward system that simultaneously motivates kids without making their learning feel like a transaction. Developing the system that seamlessly transitions between pre-created material and the personalized adaptive learning.
## Accomplishments that we're proud of
Developing a working prototype that combines scrollable short-form content with adaptive AI learning that expands upon topics that the user is interested in. Implementing the game system where users can learn while also having fun.
## What we learned
The importance of integrating AI in a way that makes it feel natural/adaptive instead of forced. Short-form learning does not need to be shallow, the learning can be split into smaller, easily understandable sections.
## What's next for TidBit
Make the AI more efficient to allow for faster loading. Expand the AI's ability to adapt the learning paths based on the user's progress and interests. Potentially add a social aspect to the platform. Partner with educators to create more base content. TidBit becoming the go-to platform for education and fun.

---

## Codebase Analysis & Technical Overview

### 1. Project Architecture
TidBit is a modern mobile application built with **React Native** and **Expo**, leveraging a cloud-native architecture for backend services and AI integration.

*   **Frontend Framework**: React Native (v0.81.4) with Expo SDK 54.
*   **Navigation**: Expo Router (v6) using file-based routing in the `app/` directory.
*   **Language**: TypeScript for type safety across the entire codebase.
*   **State Management**: React Context (`GameDataContext`) combined with real-time Firestore listeners.

### 2. Key Features & Implementation

#### A. AI-Powered Content Generation
The core educational value is driven by Generative AI, implemented in `src/lib/`.
*   **Learning Modules (`gemini.ts`)**: Uses **Google Gemini 2.5 Flash** to dynamically generate educational content. The system prompts the AI to break down complex topics into 5-6 digestible sections suitable for an 8-year-old, returning structured JSON data.
*   **Dynamic Quizzes (`quizgen.ts`)**: Generates multiple-choice questions on-the-fly using Gemini. It tailors questions to a 6th-grade level and ensures they are relevant to the current game context or specific topics.
*   **Text-to-Speech (`tts.ts`)**: Integrates **OpenAI's Audio API** (`gpt-4o-mini-tts`) to convert educational text into speech, enhancing accessibility and engagement. Audio files are cached locally using `expo-file-system`.

#### B. Gamification Layer (Idle RPG)
The app features a fully integrated idle RPG game (`app/game.tsx`) that incentivizes learning.
*   **Game Loop**: Managed via `GameDataContext`, handling real-time updates for enemy health, player DPS (Damage Per Second), and currency.
*   **Progression System**:
    *   **Idle Damage**: Characters in the player's party deal automatic damage over time.
    *   **Active Damage**: Answering quizzes correctly deals massive "burst" damage (30,000 points), directly linking knowledge to game progress.
    *   **Scaling**: Enemy health scales exponentially (`BASE_ENEMY_HEALTH * 1.2^(level-1)`), requiring players to upgrade their party and answer more quizzes to advance.
*   **Boss Mechanics**: Every 10th level features a boss with significantly higher health (2.5x multiplier).

#### C. Backend & Data Persistence
*   **Authentication**: Firebase Auth handles user sign-up and sign-in (`app/signin`, `app/signup`).
*   **Database**: Cloud Firestore stores user profiles, game progress (level, coins, party), and character collection.
*   **Real-time Sync**: The app uses `onSnapshot` listeners to ensure the game state is instantly synchronized across devices and sessions.

### 3. Technology Stack Summary

| Category | Technology | Purpose |
|----------|------------|---------|
| **Core** | React Native, Expo | Cross-platform mobile development |
| **AI** | Google Gemini (via `@google/generative-ai`) | Content & Quiz Generation |
| **AI** | OpenAI API | Text-to-Speech (TTS) |
| **Backend** | Firebase (Auth, Firestore) | User management & Real-time DB |
| **UI/UX** | React Native Reanimated | Complex animations |
| **UI/UX** | Expo Linear Gradient, Expo Image | Visual styling & Asset management |
| **Storage** | Async Storage | Local data persistence |

### 4. Directory Structure Highlights
*   `app/`: Contains the Expo Router screens (pages). `_layout.tsx` defines the navigation structure.
*   `components/`: Reusable UI components. `ContentCard.tsx` is the core component for displaying learning cards and quizzes.
*   `context/`: Global state management. `GameDataContext.tsx` is the "brain" of the game logic.
*   `src/lib/`: Service layer for external APIs (Gemini, OpenAI, TTS).
*   `assets/`: Static assets including character JSON definitions and images.
