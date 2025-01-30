# KeepYourNetwork 🌐

A powerful network monitoring and analysis tool that provides real-time insights into your network traffic, bandwidth usage, and system statistics. Built with Python and featuring a beautiful terminal UI.

![KeepYourNetwork Demo](screenshots/demo.png)

## ✨ Features

- **Real-time Network Monitoring**
  - Upload/Download speeds with live updates
  - Maximum speed tracking
  - Total data transfer statistics
  - Packet analysis and error tracking
  
- **Beautiful Interface**
  - Color-coded statistics
  - Clean and intuitive layout
  - Auto-updating display
  - Comprehensive session information
  
- **Detailed Analytics**
  - Packet statistics
  - Error tracking
  - Network session analysis
  - Bandwidth usage patterns

- **User Experience**
  - Easy to use command-line interface
  - Summary report on exit
  - Multiple display options
  - Cross-platform support

## 🚀 Installation

```bash
pip install keepyournetwork
```

## 📊 Usage

Start monitoring with the full command:
```bash
keepyournetwork
```

Or use the shorter alias:
```bash
kyn
```

### Controls
- `Ctrl+C` - Exit and view session summary

## 🛠 Development Setup

1. Clone the repository:
```bash
git clone https://github.com/HFerrahoglu/KeepYourNetwork.git
cd KeepYourNetwork
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run for development:
```bash
python -m network_monitor
```

## 📋 Requirements

- Python 3.7+
- Dependencies:
  - rich >= 13.7.0
  - psutil >= 5.9.8
  - colorama >= 0.4.6

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Hamza Ferrahoğlu**
- GitHub: [@HFerrahoglu](https://github.com/HFerrahoglu)

## 🙏 Acknowledgments

- [rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [psutil](https://github.com/giampaolo/psutil) - System and process utilities
- [colorama](https://github.com/tartley/colorama) - Cross-platform colored terminal text 