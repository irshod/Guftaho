/* Guftaho - Tajik Poetry Library JavaScript */

// Dark mode functionality
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    
    // Update toggle button icon
    const toggle = document.querySelector('.dark-mode-toggle');
    if (toggle) {
        toggle.textContent = isDark ? '☀️' : '🌙';
    }
}

// Load dark mode preference
document.addEventListener('DOMContentLoaded', function() {
    const isDark = localStorage.getItem('darkMode') === 'true';
    if (isDark) {
        document.body.classList.add('dark-mode');
        const toggle = document.querySelector('.dark-mode-toggle');
        if (toggle) {
            toggle.textContent = '☀️';
        }
    }
    
    // Page transition
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
        setTimeout(() => {
            mainContent.classList.add('loaded');
        }, 100);
    }
    
    // Scroll reveal animation
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.scroll-reveal').forEach(el => {
        observer.observe(el);
    });
    
    // Add scroll reveal to cards
    document.querySelectorAll('.card').forEach((card, index) => {
        card.classList.add('scroll-reveal');
        card.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Copy text functionality for poems
    const copyBtns = document.querySelectorAll('.copy-text');
    copyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const poemContent = document.querySelector('.poem-content');
            if (poemContent) {
                navigator.clipboard.writeText(poemContent.textContent).then(() => {
                    btn.textContent = 'Нусхабардорӣ шуд!';
                    btn.style.background = '#10b981';
                    setTimeout(() => {
                        btn.textContent = 'Нусхабардории матн';
                        btn.style.background = '';
                    }, 2000);
                });
            }
        });
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'd') {
            e.preventDefault();
            toggleDarkMode();
        }
    });
    
    // Loading state for navigation
    const navLinks = document.querySelectorAll('.nav-link, .navbar-brand');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.href && !this.href.includes('#')) {
                const mainContent = document.getElementById('main-content');
                if (mainContent) {
                    mainContent.classList.add('loading');
                }
            }
        });
    });
    
    // Smooth scrolling for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Share functionality
function sharePoem(title, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            url: url
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(url).then(() => {
            alert('Пайванд нусхабардорӣ шуд!');
        });
    }
}

// Social sharing functions
function shareOnFacebook(url, title) {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`, '_blank');
}

function shareOnTwitter(url, title) {
    window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`, '_blank');
}

function shareOnTelegram(url, title) {
    window.open(`https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`, '_blank');
}

function shareOnWhatsApp(url, title) {
    window.open(`https://wa.me/?text=${encodeURIComponent(title + ' ' + url)}`, '_blank');
}