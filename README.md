# Fuda Terminal

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)](https://github.com)
[![Language](https://img.shields.io/badge/language-EN%20%7C%20PT--BR-orange)](README.md)

**A terminal-based Planning Poker implementation for agile teams**

[🇧🇷 Versão em Português](README.md) | **🇺🇸 English**

<img src="https://img.shields.io/badge/status-active-success.svg" alt="Status">
<img src="https://img.shields.io/badge/maintainer-yes-green.svg" alt="Maintainer">

</div>

## 📖 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [How to Play](#-how-to-play)
- [Cards and Meanings](#-cards-and-meanings)
- [Network Play](#-network-play)
- [Project Structure](#-project-structure)
- [Configuration](#️-configuration)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## 💡 About

Fuda Terminal is a command-line implementation of the popular agile estimation technique. Built with Python, it allows distributed teams to conduct estimation sessions directly from their terminals, without the need for web browsers or complex setups.

Perfect for:
- 🏢 Remote teams who love the terminal
- 💻 Developers who prefer CLI tools
- 🎮 Teams looking for a fun, lightweight estimation tool
- 📊 Scrum Masters who want quick setup for planning sessions

### Why Terminal?

- **Fast**: No browser overhead, instant startup
- **Lightweight**: Minimal resource usage
- **Accessible**: Works over SSH, perfect for remote servers
- **Fun**: Brings gamification to your terminal workflow
- **Cross-platform**: Works on any system with Python

## ✨ Features

### Core Features
- 🎮 **Real-time Multiplayer** - Connect multiple players on the same network
- 🔒 **Secret Voting** - Votes are hidden until everyone has voted
- 📊 **Automatic Statistics** - Instant calculation of average, consensus, and divergence
- 🌍 **Multi-language Support** - Available in English and Portuguese (switch anytime)
- 🎨 **Colorful Interface** - Beautiful terminal UI with color-coded cards
- 👑 **Host Controls** - Room creator has special permissions
- 🔄 **Multiple Rounds** - Start new votes without creating new rooms
- 💾 **Session Persistence** - Language preference saved between sessions

### Technical Features
- **TCP/IP Socket Communication** - Reliable client-server architecture
- **Thread-based Concurrency** - Handle multiple players simultaneously
- **JSON Message Protocol** - Clean, extensible communication format
- **Cross-platform Compatibility** - Works on Linux, Windows, and macOS
- **UTF-8 Support** - Emoji and special characters display correctly

## 🎬 Demo

```
╔════════════════════════════════════════════════╗
║ Room:                 SPRINT1                  ║
╚════════════════════════════════════════════════╝
📋 Story: Implement user authentication
📊 Status: Voting in Progress

Players:
──────────────────────
  ● John 👑
  ○ Maria
  ○ Pedro
  ● Ana

Available cards:
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│  0 │  1 │  2 │  3 │  5 │  8 │ 13 │ 21 │  ? │ ☕ │
└────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
```

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)
- Terminal with UTF-8 support

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/fuda-terminal.git
cd fuda-terminal
```

### Step 2: Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import colorama; print('✅ Installation successful!')"
```

## 🎮 Usage

### Starting the Server

The server must be running before clients can connect:

```bash
python run_server.py
```

Optional: Specify a custom port:
```bash
python run_server.py 8080
```

You'll see:
```
==================================================
         PLANNING POKER - SERVER
==================================================
✓ Server running on 0.0.0.0:5555
ℹ Press Ctrl+C to stop the server
```

### Connecting as a Client

In a new terminal:

```bash
python run_client.py
```

You'll be prompted for:
1. **Language selection** (first time only)
2. **Server address** (press Enter for localhost)
3. **Port** (press Enter for default 5555)

### Main Menu Options

```
1. Create room      - Start a new planning session
2. Join room        - Enter an existing room
3. Change language  - Switch between English/Portuguese
0. Exit            - Close the application
```

## 🎯 How to Play

### 1. Creating a Session

**As the Scrum Master:**
1. Start the server on your machine
2. Connect a client to your own server
3. Select "Create room"
4. Enter your name
5. Share the 6-character room code with your team

### 2. Joining a Session

**As a Team Member:**
1. Run the client
2. Enter the server's IP address
3. Select "Join room"
4. Enter the room code provided by the Scrum Master
5. Enter your name

### 3. Voting Process

**Round Flow:**
1. **Host describes the story** - Brief explanation of the task
2. **Host starts voting** - Press 1 to begin
3. **Everyone votes secretly** - Press 2 and select a card
4. **Votes are revealed** - Automatically when all voted, or host can force reveal
5. **Discussion** - Team discusses any large divergences
6. **New round** - Host can start another vote for the same or different story

### 4. Room Interface

**Status Indicators:**
- 👑 = Room host (creator)
- ● = Player has voted
- ○ = Player hasn't voted yet

**Menu Options (vary by role and state):**
- `1. Start voting` - Host only, when not voting
- `2. Vote` - All players, during voting
- `3. Reveal votes` - Host only, during voting
- `4. New round` - Host only, after revealing
- `9. Leave room` - Exit to main menu
- `Press ENTER` - Refresh the screen

## 🃏 Cards and Meanings

| Card | Story Points | Typical Meaning |
|------|--------------|-----------------|
| 0 | Zero | Already done or trivial (minutes) |
| 1 | One | Very small task (< 1 hour) |
| 2 | Two | Small task (few hours) |
| 3 | Three | Easy task (half day) |
| 5 | Five | Medium task (1 day) |
| 8 | Eight | Complex task (2-3 days) |
| 13 | Thirteen | Large task (1 week) |
| 21 | Twenty-one | Very large task (2+ weeks) |
| ? | Unknown | Need more information |
| ☕ | Coffee | Break needed! |

### Fibonacci Sequence

The cards follow a modified Fibonacci sequence (0, 1, 2, 3, 5, 8, 13, 21), which naturally accounts for greater uncertainty in larger estimates.

## 🌐 Network Play

### Local Network (Office/Home)

**On the server machine:**
1. Find your IP address:
   ```bash
   # Linux/macOS
   ip addr show | grep inet
   hostname -I
   
   # Windows
   ipconfig
   ```
2. Look for addresses like `192.168.x.x` or `10.x.x.x`
3. Share this IP with your team

**On client machines:**
1. Run the client
2. Enter the server's IP when prompted
3. Join using the room code

### Internet Play

**Option 1: Using ngrok (Easiest)**
```bash
# Install ngrok from https://ngrok.com
ngrok tcp 5555

# Share the generated address (e.g., 4.tcp.ngrok.io:12345)
```

**Option 2: Port Forwarding**
1. Configure your router to forward port 5555
2. Find your public IP: `curl ifconfig.me`
3. Share your public IP with the team

**Option 3: VPN**
Use tools like Hamachi, ZeroTier, or Tailscale to create a virtual LAN

### Firewall Configuration

**Linux (Ubuntu/Debian):**
```bash
sudo ufw allow 5555/tcp
sudo ufw reload
```

**Linux (Fedora/RHEL):**
```bash
sudo firewall-cmd --add-port=5555/tcp --permanent
sudo firewall-cmd --reload
```

**Windows:**
- Windows Defender will prompt automatically
- Or add manual exception in Windows Firewall settings

## 📁 Project Structure

```
Fuda - Terminal/
├── src/                    # Source code
│   ├── __init__.py
│   ├── server.py          # Server implementation
│   ├── client.py          # Client implementation
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   ├── player.py      # Player class
│   │   └── room.py        # Room class
│   └── utils/             # Utilities
│       ├── __init__.py
│       ├── display.py     # Terminal UI functions
│       ├── network.py     # Network protocol
│       └── i18n.py        # Internationalization
├── docs/                  # Documentation
│   ├── MANUAL.md         # User manual
│   ├── MANUAL_EN.md      # English manual
│   └── API.md            # API documentation
├── run_server.py         # Server entry point
├── run_client.py         # Client entry point
├── requirements.txt      # Python dependencies
├── LICENSE              # MIT License
├── README.md            # Portuguese readme
└── README_EN.md         # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (optional):
```bash
DEFAULT_PORT=5555
DEFAULT_HOST=0.0.0.0
LANGUAGE=en-US
```

### Custom Cards

Edit `src/models/room.py`:
```python
VALID_CARDS = ['0', '1', '2', '3', '5', '8', '13', '21', '34', '55', '?', '☕']
```

### Color Schemes

Modify colors in `src/utils/display.py`:
- Green: Low estimates (0-3)
- Yellow: Medium estimates (5-8)
- Red: High estimates (13-21)
- Magenta: Uncertainty (?)
- Cyan: Break (☕)

## 📚 API Documentation

### Message Protocol

The system uses JSON messages over TCP sockets.

**Client → Server Messages:**
- `CREATE_ROOM` - Create a new room
- `JOIN_ROOM` - Join existing room
- `START_VOTING` - Begin voting round
- `SUBMIT_VOTE` - Submit a vote
- `REVEAL_VOTES` - Reveal all votes
- `RESET_ROUND` - Start new round

**Server → Client Messages:**
- `ROOM_STATUS` - Room state update (broadcast)
- `SUCCESS` - Operation successful
- `ERROR` - Operation failed

See [docs/API.md](docs/API.md) for complete protocol documentation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and descriptive
- Ensure cross-platform compatibility

### Ideas for Contributions

- [ ] Vote history and export to CSV
- [ ] Time limits for voting
- [ ] Sound notifications
- [ ] Vote templates for common scales
- [ ] Web dashboard for statistics
- [ ] Mobile client (using Termux/Pythonista)
- [ ] Docker container
- [ ] Kubernetes deployment
- [ ] Integration with Jira/Trello

## 🐛 Troubleshooting

### Common Issues

**"Connection refused" error:**
- Ensure server is running
- Check firewall settings
- Verify correct IP and port

**"Address already in use" error:**
```bash
# Find process using the port
lsof -i :5555  # Linux/macOS
netstat -ano | findstr :5555  # Windows

# Kill the process
kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows
```

**Characters display incorrectly:**
- Ensure terminal supports UTF-8
- On Windows: `chcp 65001`

**Screen doesn't update:**
- Press ENTER to refresh
- Check network connectivity

### Debug Mode

Enable debug output:
```python
# In src/server.py or src/client.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Planning Poker®](https://www.planningpoker.com/) by Mountain Goat Software
- Built with [Colorama](https://github.com/tartley/colorama) for cross-platform terminal colors
- Agile community for methodology and best practices
- All contributors and testers

## 📞 Support

- 📧 Email: devguilhermedarochasalvador@outlook.com

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/your-username/fuda-terminal?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/your-username/fuda-terminal?style=social)
![GitHub forks](https://img.shields.io/github/forks/your-username/fuda-terminal?style=social)

---

<div align="center">

**Made with ❤️ and ☕ for agile teams everywhere**

⭐ Star this repo if you find it useful!

</div>
