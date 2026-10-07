class TVPlayer {
    constructor() {
        this.sourceUrl = 'https://gh-proxy.org/https://raw.githubusercontent.com/jn950/live/main/tv/pllive.txt';
        this.channels = [];
        this.currentIndex = -1;
        this.focusedIndex = 0;

        this.videoPlayer = document.getElementById('videoPlayer');
        this.channelList = document.getElementById('channelList');
        this.currentChannelEl = document.getElementById('currentChannel');
        this.channelUrlEl = document.getElementById('channelUrl');

        this.init();
    }

    async init() {
        await this.loadChannels();
        this.setupControls();
        this.setupKeyboard();
        this.renderChannels();
    }

    async loadChannels() {
        try {
            const response = await fetch(this.sourceUrl);
            const text = await response.text();
            this.parseM3U(text);
        } catch (error) {
            console.error('加载频道失败:', error);
            this.channelList.innerHTML = '<div class="loading">❌ 加载失败，请刷新重试</div>';
        }
    }

    parseM3U(text) {
        const lines = text.split('\n');
        this.channels = [];
        let currentGroup = '未分类';

        for (let line of lines) {
            line = line.trim();

            // 跳过空行和注释（除了分组标记）
            if (!line || line.startsWith('//')) {
                continue;
            }

            // 检测分组标记（格式：分组名,#genre#）
            if (line.includes(',#genre#')) {
                currentGroup = line.replace(',#genre#', '').trim();
                continue;
            }

            // 检测标准 M3U 格式
            if (line.startsWith('#EXTINF:')) {
                const match = line.match(/,(.+)/);
                if (match) {
                    const name = match[1].trim();
                    const groupMatch = line.match(/group-title="([^"]+)"/);
                    const group = groupMatch ? groupMatch[1] : currentGroup;

                    this.channels.push({
                        name: name,
                        group: group,
                        url: '', // 下一行是URL
                        _pendingUrl: true
                    });
                }
                continue;
            }

            // 检测简化格式（频道名,URL）
            if (line.includes(',http')) {
                const parts = line.split(',');
                if (parts.length >= 2) {
                    const name = parts[0].trim();
                    const url = parts.slice(1).join(',').trim();

                    this.channels.push({
                        name: name,
                        group: currentGroup,
                        url: url
                    });
                }
                continue;
            }

            // 处理URL行（跟在 #EXTINF 后面）
            if (line.startsWith('http') && this.channels.length > 0) {
                const lastChannel = this.channels[this.channels.length - 1];
                if (lastChannel._pendingUrl) {
                    lastChannel.url = line;
                    delete lastChannel._pendingUrl;
                }
            }
        }

        // 过滤掉没有URL的频道
        this.channels = this.channels.filter(ch => ch.url && !ch._pendingUrl);

        console.log(`已加载 ${this.channels.length} 个频道`);
    }

    renderChannels() {
        if (this.channels.length === 0) {
            this.channelList.innerHTML = '<div class="loading">暂无频道</div>';
            return;
        }

        this.channelList.innerHTML = '';

        this.channels.forEach((channel, index) => {
            const item = document.createElement('div');
            item.className = 'channel-item';
            item.dataset.index = index;

            item.innerHTML = `
                <div class="channel-name">${channel.name}</div>
                <div class="channel-group">${channel.group}</div>
            `;

            item.addEventListener('click', () => this.playChannel(index));

            this.channelList.appendChild(item);
        });

        // 默认选中第一个频道
        if (this.channels.length > 0) {
            this.updateFocus(0);
        }
    }

    playChannel(index) {
        if (index < 0 || index >= this.channels.length) return;

        this.currentIndex = index;
        const channel = this.channels[index];

        // 更新UI
        document.querySelectorAll('.channel-item').forEach((item, i) => {
            item.classList.toggle('active', i === index);
        });

        this.currentChannelEl.textContent = channel.name;
        this.channelUrlEl.textContent = channel.url;

        // 播放视频
        this.videoPlayer.src = channel.url;
        this.videoPlayer.play().catch(err => {
            console.error('播放失败:', err);
            alert(`播放失败: ${channel.name}\n${err.message}`);
        });

        // 滚动到当前频道
        const item = this.channelList.querySelector(`[data-index="${index}"]`);
        if (item) {
            item.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    updateFocus(index) {
        if (index < 0 || index >= this.channels.length) return;

        this.focusedIndex = index;

        document.querySelectorAll('.channel-item').forEach((item, i) => {
            item.classList.toggle('focused', i === index);
        });

        // 滚动到焦点位置
        const item = this.channelList.querySelector(`[data-index="${index}"]`);
        if (item) {
            item.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    playNext() {
        if (this.currentIndex < this.channels.length - 1) {
            this.playChannel(this.currentIndex + 1);
            this.updateFocus(this.currentIndex);
        }
    }

    playPrev() {
        if (this.currentIndex > 0) {
            this.playChannel(this.currentIndex - 1);
            this.updateFocus(this.currentIndex);
        }
    }

    togglePlayPause() {
        if (this.videoPlayer.paused) {
            this.videoPlayer.play();
        } else {
            this.videoPlayer.pause();
        }
    }

    setupControls() {
        document.getElementById('prevBtn').addEventListener('click', () => this.playPrev());
        document.getElementById('nextBtn').addEventListener('click', () => this.playNext());
        document.getElementById('playPauseBtn').addEventListener('click', () => this.togglePlayPause());
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadChannels().then(() => this.renderChannels());
        });
    }

    setupKeyboard() {
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowUp':
                    e.preventDefault();
                    this.focusedIndex = Math.max(0, this.focusedIndex - 1);
                    this.updateFocus(this.focusedIndex);
                    break;

                case 'ArrowDown':
                    e.preventDefault();
                    this.focusedIndex = Math.min(this.channels.length - 1, this.focusedIndex + 1);
                    this.updateFocus(this.focusedIndex);
                    break;

                case 'ArrowLeft':
                    e.preventDefault();
                    this.playPrev();
                    break;

                case 'ArrowRight':
                    e.preventDefault();
                    this.playNext();
                    break;

                case 'Enter':
                    e.preventDefault();
                    this.playChannel(this.focusedIndex);
                    break;

                case ' ':
                    e.preventDefault();
                    this.togglePlayPause();
                    break;

                case 'Escape':
                    e.preventDefault();
                    if (document.fullscreenElement) {
                        document.exitFullscreen();
                    }
                    break;
            }
        });
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    const player = new TVPlayer();
});
