# 🏈 Fantasy Football Standings - Tidbyt App

A dynamic, rotating display app for ESPN Fantasy Football league standings, designed for the Tidbyt smart display. Shows real-time team rankings, records, and rotates through all teams in your league.

## 🎯 **Project Overview**

This project demonstrates:
- **Tidbyt App Development** using Starlark
- **ESPN API Integration** with Python authentication
- **Data Processing** and JSON manipulation
- **UI/UX Design** for small displays (64x32 pixels)
- **Animation & Rotation** systems
- **Cross-platform Development** (Python + Starlark)

## ✨ **Features**

- **Real-time Standings**: Displays current league rankings and records
- **Smart Rotation**: Automatically rotates through teams every 3 seconds
- **Responsive Design**: Adapts to leagues with 4-16 teams
- **High Contrast UI**: Optimized for readability on Tidbyt displays
- **Customizable**: User-configurable league ID and season ID
- **Offline Capable**: Works without internet connection once deployed

## 🛠 **Technical Stack**

- **Frontend**: Starlark (Tidbyt's programming language)
- **Backend**: Python 3.9+
- **API**: ESPN Fantasy Football API
- **Data Format**: JSON
- **Authentication**: ESPN cookies (espn_s2, SWID)
- **Deployment**: Pixlet CLI

## 📱 **Screenshots**

The app displays:
- Header: "FF Standings"
- Team rows: Rank, Team Name, Win-Loss Record
- Background colors: High contrast dark themes
- Rotation: 3 teams per screen, 3-second intervals

## 🚀 **Quick Start**

### Prerequisites
- Python 3.9+
- Pixlet CLI
- ESPN Fantasy Football account
- Tidbyt device

### Installation

1. **Clone the repository**
   ```bash
   git clone [your-repo-url]
   cd fantasy-football-standings
   ```

2. **Install dependencies**
   ```bash
   pip3 install espn-api
   ```

3. **Get ESPN cookies** (see `get_cookies.py` for instructions)

4. **Fetch your league data**
   ```bash
   python3 fetch_league_data.py [LEAGUE_ID] [SEASON_ID] [espn_s2] [swid]
   ```

5. **Load data into app**
   ```bash
   python3 load_data.py
   ```

6. **Deploy to Tidbyt**
   ```bash
   pixlet render fantasy_football_standings.star
   pixlet push [DEVICE_ID] fantasy_football_standings.webp -i fantasyfootballstandings
   ```

## 🔧 **Configuration**

### App Settings (in manifest.yaml)
- **League ID**: Your ESPN Fantasy Football league ID
- **Season ID**: Current season year (e.g., 2025)
- **Rotation Speed**: Seconds between rotations (default: 3)
- **Teams per Screen**: Number of teams shown per frame (default: 3)

### Customization Options
- **Team Colors**: 16 high-contrast background colors
- **Font**: CG-pixel-3x5-mono (optimized for small displays)
- **Layout**: Responsive design for different team counts

## 📊 **Data Structure**

The app processes team data with this structure:
```json
{
  "name": "Team Name",
  "record": {
    "overall": {
      "wins": 0,
      "losses": 0,
      "ties": 0
    }
  },
  "points_for": 0.0,
  "points_against": 0.0,
  "rank": 1
}
```

## 🔐 **Authentication**

ESPN requires authentication cookies:
- **espn_s2**: Session cookie from ESPN website
- **SWID**: User identification cookie
- **Instructions**: See `get_cookies.py` for detailed steps

## 🎨 **UI Components**

### Layout Structure
- **Header**: 6px height, centered title
- **Team Rows**: 8px height each, left-aligned content
- **Rank**: Fixed width, right-aligned numbers
- **Team Name**: Truncated to 10 characters for readability
- **Record**: Fixed width, "W-L" format

### Color Scheme
- **Background**: Dark high-contrast colors
- **Text**: White (#FFFFFF)
- **Header**: Dark gray (#1a1a1a)

## 🚧 **Limitations & Considerations**

### ESPN API Limitations
- **No Public API**: Requires personal authentication
- **Cookie Expiration**: Tokens expire and need refresh
- **Rate Limiting**: API has usage restrictions

### Community Deployment
- **Manual Setup**: Users must follow authentication process
- **Data Updates**: Requires manual refresh for new data
- **No Real-time**: Data is static once deployed

## 🤝 **Contributing**

This project is open for contributions:
- UI/UX improvements
- Additional data sources
- Performance optimizations
- Documentation enhancements

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 **Author**

**Joseph Scharnweber**
- GitHub: [@JosephScharnweber](https://github.com/JosephScharnweber)
- Portfolio: [Your Portfolio URL]

## 🙏 **Acknowledgments**

- ESPN Fantasy Football API
- Tidbyt development team
- Pixlet CLI creators
- Fantasy football community

---

**Note**: This app requires ESPN Fantasy Football league access and authentication. It's designed for personal use and community sharing with manual setup requirements.
