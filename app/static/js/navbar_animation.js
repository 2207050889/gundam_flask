document.addEventListener('DOMContentLoaded', function () {
    const navLinksContainer = document.querySelector('.navbar-nav.me-auto');
    const navLinks = document.querySelectorAll('.navbar-nav.me-auto .nav-link:not(.series-dropdown)');
    const follower = document.querySelector('.navbar-nav.me-auto .nav-item-follower');
    let activeLink = document.querySelector('.navbar-nav.me-auto .nav-link.active');

    function positionFollower(element) {
        if (element && follower) {
            // Use element's (<a> tag) offsetLeft relative to its offsetParent (the <ul>)
            // and element's offsetWidth for the width of the follower.
            follower.style.left = `${element.offsetLeft}px`;
            follower.style.width = `${element.offsetWidth}px`;
            
            // CSS will control height and vertical alignment (e.g., bottom: 4px)
            // follower.style.height = `${element.offsetHeight}px`; 
            
            follower.style.opacity = '1';
        } else if (follower) {
            follower.style.opacity = '0';
        }
    }

    // Initial position for active link with responsive check
    function initializeFollower() {
        const isMobileTablet = window.innerWidth < 992;
        
        if (follower) {
            if (isMobileTablet) {
                // Hide follower on mobile/tablet
                follower.style.opacity = '0';
                follower.style.display = 'none';
            } else {
                // Show follower on desktop
                follower.style.display = 'block';
    if (activeLink) {
        // Timeout to allow layout to settle, especially if fonts affect dimensions
        setTimeout(() => positionFollower(activeLink), 100);
                } else if (navLinks.length > 0) {
                    // If no active link, hide the follower
        follower.style.opacity = '0';
                }
            }
        }
    }
    
    // Initialize on load
    initializeFollower();
    
    // 初始时更新导航栏活动状态
    updateActiveNavLink();

    // 更新导航栏高亮状态
    function updateActiveNavLink() {
        // 获取当前路径
        const currentPath = window.location.pathname;
        console.log('🔄 导航栏: 更新高亮状态，当前路径:', currentPath);
        
        // 清除所有导航链接的活动状态
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        // 根据当前路径设置活动链接
        let newActiveLink = null;
        
        // 精确匹配首页
        if (currentPath === '/' || currentPath.includes('/index')) {
            newActiveLink = document.querySelector('.navbar-nav.me-auto .nav-link[href="/"]');
            console.log('🔄 导航栏: 匹配到首页');
        } 
        // 匹配其他页面
        else {
            for (const link of navLinks) {
                const href = link.getAttribute('href');
                if (href && href !== '/' && currentPath.includes(href)) {
                    newActiveLink = link;
                    console.log('🔄 导航栏: 匹配到页面:', href);
                    break;
                }
            }
        }
        
        // 设置新的活动链接
        if (newActiveLink) {
            newActiveLink.classList.add('active');
            activeLink = newActiveLink;
            console.log('🔄 导航栏: 设置活动链接:', newActiveLink.getAttribute('href'));
            setTimeout(() => positionFollower(activeLink), 10);
        } else {
            // 如果没有匹配的链接，隐藏follower
            console.log('🔄 导航栏: 未找到匹配链接');
            if (follower) follower.style.opacity = '0';
        }
    }

    // 为导航链接添加悬停效果，但不改变活动状态
    navLinks.forEach(link => {
        // 悬停效果 - 仅视觉效果，不更改活动状态
        link.addEventListener('mouseenter', () => {
            // 临时显示follower在悬停的链接上，但不改变activeLink
            if (follower) {
                follower.style.transition = 'left 0.3s ease, width 0.3s ease';
                positionFollower(link);
            }
        });

        // 点击事件 - 由服务器处理实际页面导航
        link.addEventListener('click', () => {
            // 点击时设置活动状态，提供即时视觉反馈
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            activeLink = link;
        });
    });

    // 鼠标离开导航栏时恢复到当前活动链接
    if (navLinksContainer) {
        navLinksContainer.addEventListener('mouseleave', () => {
            if (follower) {
                follower.style.transition = 'left 0.3s ease, width 0.3s ease, opacity 0.3s ease';
                if (activeLink) {
                    positionFollower(activeLink);
                } else {
                    follower.style.opacity = '0';
                }
            }
        });
    }

    // 添加pageshow事件监听，处理浏览器后退/前进操作
    window.addEventListener('pageshow', (event) => {
        console.log('🔄 导航栏: 页面显示事件触发，是否从缓存:', event.persisted);
        
        // 无论是否从缓存恢复，都重新更新导航栏状态
        // 短暂延迟确保DOM已完全恢复
        setTimeout(() => {
            updateActiveNavLink();
        }, 100);
    });

    // 添加popstate事件监听，专门处理浏览器前进/后退按钮操作
    window.addEventListener('popstate', (event) => {
        console.log('🔄 导航栏: popstate事件触发');
        setTimeout(() => {
            updateActiveNavLink();
        }, 100);
    });

    // Enhanced responsive handling on window resize
    window.addEventListener('resize', () => {
        const currentActiveLink = document.querySelector('.navbar-nav.me-auto .nav-link.active');
        
        // Check if we're in mobile/tablet mode where follower should be hidden
        const isMobileTablet = window.innerWidth < 992;
        
        if (follower) {
            if (isMobileTablet) {
                // Hide follower on mobile/tablet
                follower.style.opacity = '0';
                follower.style.display = 'none';
            } else {
                // Show and position follower on desktop
                follower.style.display = 'block';
        if (currentActiveLink) {
                    // Add small delay to ensure layout has settled after resize
                    setTimeout(() => {
            positionFollower(currentActiveLink);
                    }, 100);
        } else {
                    follower.style.opacity = '0';
                }
            }
        }
    });

    // Enhanced navbar with scroll direction detection and hide/show functionality
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    let isScrollingDown = false;
    let scrollThreshold = 10; // Minimum scroll distance to trigger hide/show
    
    window.addEventListener('scroll', () => {
        const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add background blur when scrolled
        if (currentScrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Detect scroll direction and hide/show navbar
        if (Math.abs(currentScrollTop - lastScrollTop) > scrollThreshold) {
            if (currentScrollTop > lastScrollTop && currentScrollTop > 80) {
                // Scrolling down & past initial threshold - hide navbar
                if (!isScrollingDown) {
                    navbar.classList.add('navbar-hidden');
                    navbar.classList.remove('navbar-visible');
                    isScrollingDown = true;
                }
            } else if (currentScrollTop < lastScrollTop) {
                // Scrolling up - show navbar
                if (isScrollingDown) {
                    navbar.classList.remove('navbar-hidden');
                    navbar.classList.add('navbar-visible');
                    isScrollingDown = false;
                }
            }
            lastScrollTop = currentScrollTop;
        }
        
        // Always show navbar when at top
        if (currentScrollTop <= 0) {
            navbar.classList.remove('navbar-hidden');
            navbar.classList.add('navbar-visible');
            isScrollingDown = false;
        }
    });

    // Enhanced mobile menu animations
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Add animation classes for mobile menu
        navbarToggler.addEventListener('click', () => {
            // Add a small delay to ensure Bootstrap has processed the toggle
            setTimeout(() => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.style.animation = 'slideDown 0.3s ease-out forwards';
                } else {
                    navbarCollapse.style.animation = 'slideUp 0.3s ease-out forwards';
                }
            }, 10);
        });
        
        // Auto-close mobile menu when clicking on nav links (except dropdowns)
        const mobileNavLinks = navbarCollapse.querySelectorAll('.nav-link:not(.dropdown-toggle)');
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                    navbarToggler.click(); // Trigger the toggle to close menu
                }
            });
        });
    }

    // Also listen for Bootstrap's 'shown.bs.dropdown' or similar events if your active link might change
    // due to dropdowns or other Bootstrap components dynamically altering active states.
    // For now, this covers basic hover and active link on load.
}); 