# Smart TV Live Player

## Android TV 直播定制版

新增基于用户提供的影视仓 APK 定制的 **影视仓·直播**：启动直达直播、内置完整地区直播源、遥控器长按确认收藏、大字深色菜单，并移除原有人像壁纸。

- [定制代码与构建说明](live-customization/README.md)
- [下载安装包](https://github.com/loru12321/smart-tv-live-player/releases/tag/ysc-live-2026.10.1)
- [遥控器使用说明](发布/影视仓直播版/使用说明.md)

这是基于原 APK 的直播定制版，保留原播放内核；以下为仓库原有 Web 播放器说明。

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
