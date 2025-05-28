/**
 * 高达信息展示平台 - 统一音频管理系统
 * 管理所有音效和背景音乐
 */

class AudioManager {
    constructor() {
        this.audioContext = null;
        this.sounds = {};
        this.loadingStates = {};
        this.failedSounds = new Set();
        this.isEnabled = true;
        this.masterVolume = 0.5;
        this.hasAudioFiles = false;
        
        // 背景音乐相关
        this.currentBGM = null;
        this.isMusicPlaying = false;
        this.musicController = null;
        
        this.init();
    }

    async init() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.bindGlobalEvents();
            this.createMusicController();
            console.log('🎵 Unified Audio Manager initialized');
        } catch (error) {
            console.log('🔇 Audio Manager: Running in silent mode');
            this.isEnabled = false;
        }
    }

    // 创建音乐控制器UI
    createMusicController() {

        if (document.getElementById('music-controller')) {
            console.log('🎵 音乐控制器已存在，跳过创建');
            this.musicController = document.getElementById('music-controller');
            return;
        }

        const path = window.location.pathname;
        
        // 检查是否是演播厅页面，演播厅可能有自己的音频控制器
        const showroomPages = ['/uc_showroom', '/seed_showroom', '/ibo_showroom', '/oo_showroom', '/w_showroom'];
        const isShowroomPage = showroomPages.some(page => path.includes(page));
        
        if (isShowroomPage) {
            console.log('🎵 演播厅页面，检查是否已有音频控制器');
            // 演播厅页面可能有自己的音频控制器，延迟检查避免冲突
            setTimeout(() => {
                if (!document.getElementById('music-controller')) {
                    console.log('🎵 演播厅页面未发现现有控制器，创建通用控制器');
                    this.createControllerForShowroom(path);
                }
            }, 200);
            return;
        }
        
        // 排除不需要音乐的页面
        const excludedPages = ['/series/', '/detail/', '/gundam/', '/search'];
        const isExcluded = excludedPages.some(page => path.includes(page));
        
        if (isExcluded) {
            console.log('🎵 Page excluded from music controller:', path);
            return;
        }
        
        // 只在特定页面显示音乐控制器和播放音乐
        const musicPages = ['/', '/index', '/jingxuanxilie', '/album'];
        const shouldHaveMusic = musicPages.some(page => 
            path === page || (page !== '/' && path.includes(page))
        );
        
        if (!shouldHaveMusic) {
            console.log('🎵 Page does not need music controller:', path);
            return;
        }

        this.createStandardController();
    }

    // 为演播厅创建控制器
    createControllerForShowroom(path) {
        this.createStandardController();
    }

    // 创建标准音乐控制器
    createStandardController() {
        const controllerHTML = `
            <div id="music-controller" class="music-controller">
                <div class="music-controller-content">
                    <div class="music-icon">
                        <i class="fas fa-music"></i>
                    </div>
                    <div class="music-info">
                        <div class="music-title">背景音乐</div>
                        <div class="music-status">点击播放</div>
                    </div>
                    <div class="music-toggle">
                        <i class="fas fa-play"></i>
                    </div>
                </div>
                <div class="music-wave">
                    <span></span>
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', controllerHTML);
        this.musicController = document.getElementById('music-controller');
        
        // 绑定点击事件
        this.musicController.addEventListener('click', () => {
            this.toggleBackgroundMusic();
        });

        // 设置滚动行为
        this.setupScrollBehavior();

        // 延迟自动播放
        setTimeout(() => {
            this.autoStartBackgroundMusic();
        }, 1000);
    }

    // 滚动行为
    setupScrollBehavior() {
        window.addEventListener('scroll', () => {
            const currentScrollY = window.scrollY;
            const navbar = document.querySelector('.navbar');
            const navbarHeight = navbar ? navbar.offsetHeight : 60;

            if (currentScrollY > navbarHeight + 20) {
                this.musicController.classList.add('hidden');
            } else {
                this.musicController.classList.remove('hidden');
            }
        });
    }

    // 自动开始背景音乐
    async autoStartBackgroundMusic() {
        try {
            await this.startBackgroundMusic();
            this.showNotification('背景音乐已启动');
        } catch (error) {
            console.log('🎵 Auto-play blocked, waiting for user interaction');
            this.waitForUserInteraction();
        }
    }

    // 等待用户交互
    waitForUserInteraction() {
        const startOnInteraction = async () => {
            try {
                await this.startBackgroundMusic();
                this.showNotification('背景音乐已启动');
                
                document.removeEventListener('click', startOnInteraction);
                document.removeEventListener('keydown', startOnInteraction);
                document.removeEventListener('scroll', startOnInteraction);
            } catch (error) {
                console.log('❌ Still failed to start music');
            }
        };

        document.addEventListener('click', startOnInteraction);
        document.addEventListener('keydown', startOnInteraction);
        document.addEventListener('scroll', startOnInteraction);
    }

    // 切换背景音乐
    async toggleBackgroundMusic() {
        if (this.isMusicPlaying) {
            this.stopBackgroundMusic();
        } else {
            await this.startBackgroundMusic();
        }
    }

    // 开始背景音乐
    async startBackgroundMusic() {
        try {
            // 停止当前音乐
            this.stopBackgroundMusic();

            const path = window.location.pathname;
            
            // 排除不需要音乐的页面
            const excludedPages = ['/series/', '/detail/', '/gundam/', '/search'];
            const isExcluded = excludedPages.some(page => path.includes(page));
            
            if (isExcluded) {
                console.log('🎵 Page excluded from background music:', path);
                return;
            }
            
            // 检查是否是允许播放音乐的页面
            const musicPages = ['/', '/index', '/jingxuanxilie', '/album', '/uc_showroom', '/seed_showroom', '/ibo_showroom', '/oo_showroom', '/w_showroom'];
            const shouldHaveMusic = musicPages.some(page => 
                path === page || (page !== '/' && path.includes(page))
            );
            
            if (!shouldHaveMusic) {
                console.log('🎵 Page does not support background music:', path);
                return;
            }
            
            let musicFile = '';
            let volume = 0.3;

            if (path === '/' || path.includes('index')) {
                musicFile = '/static/audio/伊藤由奈 - trust you.ogg';
                volume = 0.3;
            } else if (path.includes('jingxuanxilie')) {
                musicFile = '/static/audio/有馬孝哲 - 颯爽たるシャア.ogg';
                volume = 0.25;
            } else if (path.includes('album')) {
                musicFile = '/static/audio/anime theme.mp3';
                volume = 0.2;
            } else if (path.includes('uc_showroom')) {
                musicFile = '/static/audio/鮎川麻弥 - Z・刻をこえて(ワンコーラス).ogg';
                volume = 0.25;
            } else if (path.includes('seed_showroom')) {
                musicFile = '/static/audio/See-Saw - 君は僕に似ている (你与我相似).ogg';
                volume = 0.25;
            } else if (path.includes('ibo_showroom')) {
                musicFile = '/static/audio/Uru - フリージア (TV size).ogg';
                volume = 0.25;
            } else if (path.includes('oo_showroom')) {
                musicFile = '/static/audio/伊藤由奈 - trust you.ogg';
                volume = 0.25;
            } else if (path.includes('w_showroom')) {
                musicFile = '/static/audio/TWO-MIX - JUST COMMUNICATION NEXTII (TYPEII).ogg';
                volume = 0.25;
            }

            this.currentBGM = new Audio(musicFile);
            this.currentBGM.loop = true;
            this.currentBGM.volume = volume;

            await this.currentBGM.play();

            this.isMusicPlaying = true;
            this.updateMusicUI();
            console.log('🎵 Background music started:', musicFile);
        } catch (error) {
            console.log('❌ Failed to start background music:', error);
            this.isMusicPlaying = false;
            this.updateMusicUI();
            throw error;
        }
    }

    // 停止背景音乐
    stopBackgroundMusic() {
        if (this.currentBGM) {
            this.currentBGM.pause();
            this.currentBGM = null;
        }
        this.isMusicPlaying = false;
        this.updateMusicUI();
        console.log('⏸ Background music stopped');
    }

    // 更新音乐控制器UI
    updateMusicUI() {
        if (!this.musicController) return;

        const toggleIcon = this.musicController.querySelector('.music-toggle i');
        const statusText = this.musicController.querySelector('.music-status');
        const waveElement = this.musicController.querySelector('.music-wave');

        if (this.isMusicPlaying) {
            toggleIcon.className = 'fas fa-pause';
            statusText.textContent = '正在播放';
            this.musicController.classList.add('playing');
            waveElement.classList.add('active');
        } else {
            toggleIcon.className = 'fas fa-play';
            statusText.textContent = '点击播放';
            this.musicController.classList.remove('playing');
            waveElement.classList.remove('active');
        }
    }

    // 显示通知
    showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'music-notification';
        notification.innerHTML = `
            <i class="fas fa-music"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    // 懒加载音效文件
    async loadSoundLazy(soundName) {
        if (this.sounds[soundName] || this.loadingStates[soundName] || this.failedSounds.has(soundName)) {
            return this.sounds[soundName] || null;
        }

        const soundFiles = {
            hover: 'uiHover',
            click: 'mechanical click',
            pageTransition: 'sci-fi transition',
            mechanicalMove: 'mechanical click',
            systemStart: 'start',
            cardFlip: 'paper flip'
        };

        const filename = soundFiles[soundName];
        if (!filename) {
            console.warn(`🚫 Unknown sound: ${soundName}`);
            return null;
        }

        this.loadingStates[soundName] = true;
        const supportedFormats = ['.wav', '.mp3', '.ogg', '.m4a', '.aac'];

        for (const format of supportedFormats) {
            try {
                const url = `/static/audio/${filename}${format}`;
                const audioBuffer = await this.loadSound(url);
                
                this.sounds[soundName] = audioBuffer;
                this.hasAudioFiles = true;
                delete this.loadingStates[soundName];
                
                console.log(`✅ Lazy loaded: ${soundName} as ${filename}${format}`);
                return audioBuffer;
            } catch (error) {
                continue;
            }
        }

        this.failedSounds.add(soundName);
        delete this.loadingStates[soundName];
        console.log(`❌ Failed to lazy load: ${soundName} (${filename})`);
        return null;
    }

    async loadSound(url) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 3000);

        try {
            const response = await fetch(url, { 
                signal: controller.signal,
                cache: 'force-cache'
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const arrayBuffer = await response.arrayBuffer();
            const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
            return audioBuffer;
        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }

    // 播放音效
    async playSound(soundName, volume = 1, loop = false) {
        if (!this.isEnabled || !this.audioContext) {
            return null;
        }

        try {
            let audioBuffer = this.sounds[soundName];
            if (!audioBuffer && !this.failedSounds.has(soundName)) {
                audioBuffer = await this.loadSoundLazy(soundName);
            }

            if (!audioBuffer) {
                return null;
            }

            const source = this.audioContext.createBufferSource();
            const gainNode = this.audioContext.createGain();
            
            source.buffer = audioBuffer;
            source.loop = loop;
            
            gainNode.gain.value = this.masterVolume * volume;
            
            source.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            source.start();
            return source;
        } catch (error) {
            return null;
        }
    }

    // 绑定全局事件
    bindGlobalEvents() {
        let hoverTimeout;
        document.addEventListener('mouseover', (e) => {
            if (e.target.matches('.nav-link, .btn, .card-link-btn, .community-tag')) {
                if (hoverTimeout) return;
                
                hoverTimeout = setTimeout(() => {
                    this.playSound('hover', 0.3);
                    hoverTimeout = null;
                }, 50);
            }
        });

        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn, .card-link-btn, .nav-link')) {
                this.playSound('click', 0.4);
            }
        });
    }

    // 页面特定音效方法
    playPageEnterSound(pageName) {
        console.log(`🔊 Page ${pageName} loaded`);
    }

    playStartButtonSound() {
        this.playSound('systemStart', 0.5);
    }

    setMasterVolume(volume) {
        this.masterVolume = Math.max(0, Math.min(1, volume));
    }

    toggle() {
        this.isEnabled = !this.isEnabled;
        if (!this.isEnabled) {
            this.stopBackgroundMusic();
        }
        return this.isEnabled;
    }
}

// 全局音频管理器实例
window.audioManager = new AudioManager();

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔊 Unified Audio Manager ready');
});

// 页面卸载时清理
window.addEventListener('beforeunload', () => {
    if (window.audioManager && window.audioManager.currentBGM) {
        window.audioManager.currentBGM.pause();
        window.audioManager.currentBGM = null;
    }
});

// 添加页面显示事件监听（处理浏览器前进后退）
window.addEventListener('pageshow', (event) => {
    console.log('🔄 页面显示事件触发，是否从缓存:', event.persisted);
    
    // 如果页面从缓存恢复，重新初始化音频系统
    if (event.persisted && window.audioManager) {
        console.log('🎵 从缓存恢复页面，重新初始化音频系统');
        
        // 重置音频管理器状态
        window.audioManager.isMusicPlaying = false;
        if (window.audioManager.currentBGM) {
            window.audioManager.currentBGM.pause();
            window.audioManager.currentBGM = null;
        }
        
        // 清除现有的音乐控制器
        const existingController = document.getElementById('music-controller');
        if (existingController) {
            existingController.remove();
            window.audioManager.musicController = null;
        }
        
        // 等待短暂延迟以确保DOM完全恢复
        setTimeout(() => {
            // 重新创建音乐控制器，适用于所有页面
            window.audioManager.createMusicController();
            
            // 再次延迟以确保控制器创建完成后尝试播放音乐
            setTimeout(() => {
                window.audioManager.startBackgroundMusic();
            }, 300);
        }, 200);
    }
});

// 添加页面可见性变化监听
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.audioManager) {
        console.log('🎵 页面变为可见，检查音频状态');
        
        // 如果页面变为可见且应该有背景音乐但没有播放，则重新启动
        const path = window.location.pathname;
        const musicPages = ['/', '/index', '/jingxuanxilie', '/album', '/uc_showroom', '/seed_showroom', '/ibo_showroom', '/oo_showroom', '/w_showroom'];
        const shouldHaveMusic = musicPages.some(page => 
            path === page || (page !== '/' && path.includes(page))
        );
        
        if (shouldHaveMusic && window.audioManager.musicController) {
            // 如果音乐应该播放但不在播放，则重新启动
            if (!window.audioManager.isMusicPlaying || !window.audioManager.currentBGM) {
                console.log('🎵 检测到音乐应该播放但未播放，重新启动背景音乐');
                setTimeout(() => {
                    window.audioManager.startBackgroundMusic();
                }, 300);
            }
        }
    }
});