/* Poem Detail Page JavaScript */

// Copy poem text to clipboard
function copyToClipboard() {
    const poemText = document.querySelector('.poem-text').innerText;
    const poemData = window.poemData || {};
    const title = poemData.title || '';
    const poet = poemData.poet || '';
    const textToCopy = `${title}\n\nСуруда: ${poet}\n\n${poemText}`;
    
    navigator.clipboard.writeText(textToCopy).then(function() {
        const btn = event.target.closest('.copy-text');
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<span class="btn-icon">✅</span>Нусха бардошта шуд!';
        btn.classList.remove('btn-outline-secondary');
        btn.classList.add('btn-success');
        
        setTimeout(function() {
            btn.innerHTML = originalHTML;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-outline-secondary');
        }, 2000);
    }).catch(function(err) {
        console.error('Хатогӣ дар нусха бардоштан: ', err);
        alert('Хатогӣ дар нусха бардоштан');
    });
}

// Share functions
function sharePoem() {
    const poemData = window.poemData || {};
    const url = poemData.url || window.location.href;
    const title = `${poemData.title || ''} - ${poemData.poet || ''}`;
    
    if (navigator.share) {
        navigator.share({
            title: title,
            url: url,
        }).catch(console.error);
    } else {
        // Fallback: copy URL to clipboard
        navigator.clipboard.writeText(url).then(() => {
            alert('Пайванд нусхабардорӣ шуд!');
        });
    }
}

function shareOnFacebook() {
    const poemData = window.poemData || {};
    const url = encodeURIComponent(poemData.url || window.location.href);
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank');
}

function shareOnTwitter() {
    const poemData = window.poemData || {};
    const url = encodeURIComponent(poemData.url || window.location.href);
    const text = encodeURIComponent(`${poemData.title || ''} - ${poemData.poet || ''}`);
    window.open(`https://twitter.com/intent/tweet?url=${url}&text=${text}`, '_blank');
}

function shareOnTelegram() {
    const poemData = window.poemData || {};
    const url = encodeURIComponent(poemData.url || window.location.href);
    const text = encodeURIComponent(`${poemData.title || ''} - ${poemData.poet || ''}`);
    window.open(`https://t.me/share/url?url=${url}&text=${text}`, '_blank');
}

function shareOnWhatsApp() {
    const poemData = window.poemData || {};
    const url = encodeURIComponent(poemData.url || window.location.href);
    const text = encodeURIComponent(`${poemData.title || ''} - ${poemData.poet || ''}`);
    window.open(`https://wa.me/?text=${text} ${url}`, '_blank');
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const copyBtn = document.querySelector('.copy-text');
    if (copyBtn) {
        copyBtn.addEventListener('click', copyToClipboard);
    }
});