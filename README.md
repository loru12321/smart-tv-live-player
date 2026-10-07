# Smart TV Live Player

A modern web-based IPTV player with remote control support and elegant UI design.

## Features

- 📺 Support for M3U/M3U8 live stream sources
- 🎮 Full keyboard/remote control navigation
- 🎨 Modern dark theme interface
- 📱 Responsive layout optimized for TV screens
- ⚡ Fast channel switching
- 🔄 Auto-reload channel list

## Keyboard Controls

- **Arrow Up/Down**: Navigate through channel list
- **Enter**: Play selected channel
- **Arrow Left/Right**: Previous/Next channel
- **Space**: Play/Pause
- **Escape**: Exit fullscreen

## Live Stream Source

Default source: `https://gh-proxy.org/https://raw.githubusercontent.com/jn950/live/main/tv/pllive.txt`

## Quick Start

1. Clone this repository
2. Serve the files with any HTTP server:
   ```bash
   python -m http.server 8000
   ```
3. Open `http://localhost:8000` in your browser
4. Navigate with keyboard or remote control

## Project Structure

```
.
├── index.html          # Main HTML structure
├── style.css           # UI styling
├── app.js              # Application logic
└── README.md           # Documentation
```

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Smart TV browsers with modern JavaScript support

## License

MIT License

## Credits

Built with modern web technologies for optimal TV viewing experience.
