/**
 * 高达信息展示平台 - 登录页面脚本
 * 实现背景视差效果、加载动画等
 */

// 背景视差效果
var back = document.querySelector('main');
window.onmousemove = function(event) {
    var x = -event.clientX/10;
    var y = -event.clientY/15;
    back.style.backgroundPositionX = x + "px";
    back.style.backgroundPositionY = y + "px";
}

// 创建加载动画
function createLoadingAnimation() {
    // 创建加载容器
    const loadingContainer = document.createElement('div');
    loadingContainer.className = 'loading-container';
    loadingContainer.style.display = 'none';
    loadingContainer.style.position = 'fixed';
    loadingContainer.style.top = '0';
    loadingContainer.style.left = '0';
    loadingContainer.style.width = '100%';
    loadingContainer.style.height = '100%';
    loadingContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    loadingContainer.style.zIndex = '9999';
    loadingContainer.style.display = 'flex';
    loadingContainer.style.justifyContent = 'center';
    loadingContainer.style.alignItems = 'center';
    
    // 创建加载动画
    const loadingDots = document.createElement('div');
    loadingDots.className = 'loading-dots';
    loadingDots.style.display = 'flex';
    
    // 添加7个点
    for (let i = 0; i < 7; i++) {
        const dot = document.createElement('div');
        dot.className = 'dot';
        dot.style.width = '20px';
        dot.style.height = '20px';
        dot.style.margin = '0 5px';
        dot.style.borderRadius = '50%';
        dot.style.backgroundColor = 'white';
        dot.style.animation = 'loadingAnimation 1.4s ease-in-out infinite';
        dot.style.animationDelay = `${i * 0.2}s`;
        loadingDots.appendChild(dot);
    }
    
    // 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes loadingAnimation {
            0%, 100% {
                transform: scale(0.2);
                background-color: rgba(255, 255, 255, 0.2);
            }
            50% {
                transform: scale(1);
                background-color: rgba(255, 255, 255, 1);
            }
        }
    `;
    
    document.head.appendChild(style);
    loadingContainer.appendChild(loadingDots);
    document.body.appendChild(loadingContainer);
    
    return loadingContainer;
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 隐藏导航栏和页脚
    document.body.style.paddingTop = '0';
    
    // 创建并显示加载动画
    const loadingAnimation = createLoadingAnimation();
    
    // 延迟3秒后隐藏加载动画
    setTimeout(function() {
        loadingAnimation.style.display = 'none';
    }, 2000);
    
    // 登录表单提交前显示加载动画
    const loginForm = document.querySelector('form');
    if (loginForm) {
        loginForm.addEventListener('submit', function() {
            loadingAnimation.style.display = 'flex';
        });
    }
}); 