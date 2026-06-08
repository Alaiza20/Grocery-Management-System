// ================================================================
// theme.js — Central theme management
// Uses same key and themes as index.html: 'gms-theme'
// Themes: dark (default), light, bw
// ================================================================

const THEMES = ['dark', 'light', 'bw'];

const THEME_META = {
    dark:  { icon: 'bi-moon-stars', label: 'Dark'  },
    light: { icon: 'bi-sun',        label: 'Light' },
    bw:    { icon: 'bi-circle-half', label: 'B&W'  }
};

function applyTheme(t) {
    if (!THEMES.includes(t)) t = 'dark';
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('gms-theme', t);
    updateThemeBtn(t);
}

function getSavedTheme() {
    return localStorage.getItem('gms-theme') || 'dark';
}

function cycleTheme() {
    const current = getSavedTheme();
    const next    = THEMES[(THEMES.indexOf(current) + 1) % THEMES.length];
    applyTheme(next);
}

function updateThemeBtn(t) {
    const btn = document.getElementById('themeToggleBtn');
    if (!btn) return;
    const meta = THEME_META[t];
    btn.innerHTML = `<i class="bi ${meta.icon}"></i> ${meta.label}`;
}

// Apply immediately on script load — no flash
applyTheme(getSavedTheme());

document.addEventListener('DOMContentLoaded', () => {
    updateThemeBtn(getSavedTheme());
});