// ================================================================
// navbar.js — Injects consistent topbar into every page
// Call buildNavbar("pageName") in each page's init()
// ================================================================

function buildNavbar(activePage) {
    const isRoot  = !window.location.pathname.includes('/pages/');
    const prefix  = isRoot ? 'pages/' : '';
    const rootPfx = isRoot ? '' : '../';

    const links = [
        { id:'orders',    label:'Orders',    href:`${prefix}orders.html`    },
        { id:'inventory', label:'Inventory', href:`${prefix}inventory.html` },
        { id:'payments',  label:'Payments',  href:`${prefix}payments.html`  },
        { id:'products',  label:'Products',  href:`${prefix}products.html`  },
        { id:'customers', label:'Customers', href:`${prefix}customers.html` },
        { id:'suppliers', label:'Suppliers', href:`${prefix}suppliers.html` },
        { id:'uom',       label:'UOM',       href:`${prefix}uom.html`       },
    ];

    const navLinks = links.map(l => `
        <a href="${l.href}" class="${activePage === l.id ? 'active' : ''}">${l.label}</a>
    `).join('');

    const html = `
    <div class="bg-mesh"></div>
    <div class="bg-grid"></div>
    <header class="gms-topbar">
        <a href="${rootPfx}index.html" class="brand">
            <div class="brand-icon"><i class="bi bi-cart3"></i></div>
            <span class="brand-name">Grocery MS</span>
        </a>
        <nav>${navLinks}</nav>
        <div class="topbar-right">
            <div class="theme-toggle" id="themeToggleBtn" onclick="cycleTheme()" title="Switch theme">
                <i class="bi bi-moon-stars"></i>
            </div>
            <div class="user-pill-sm d-none" id="navUserPill">
                <div class="user-avatar-sm" id="navUserAvatar">A</div>
                <span class="user-name-sm" id="navUserName"></span>
            </div>
            <button class="btn-signout" onclick="signOut()">
                <i class="bi bi-box-arrow-right"></i> Sign Out
            </button>
        </div>
    </header>`;

    const target = document.getElementById('gms-navbar');
    if (target) target.innerHTML = html;

    updateThemeBtn(getSavedTheme());
    loadNavbarUser();
}

async function loadNavbarUser() {
    try {
        const { data: { session } } = await supabaseClient.auth.getSession();
        if (!session) return;

        const user     = session.user;
        const name     = user.user_metadata?.full_name || user.email || 'Admin';
        const avatar   = user.user_metadata?.avatar_url;
        const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0,2);
        const pill     = document.getElementById('navUserPill');
        const av       = document.getElementById('navUserAvatar');
        const nm       = document.getElementById('navUserName');

        if (pill) pill.classList.remove('d-none');
        if (nm)   nm.textContent = name.split(' ')[0];
        if (av) {
            av.innerHTML = avatar
                ? `<img src="${avatar}" style="width:26px;height:26px;border-radius:50%;object-fit:cover">`
                : initials;
        }
    } catch(e) { /* silent */ }
}

function updateThemeBtn(t) {
    const btn = document.getElementById('themeToggleBtn');
    if (!btn) return;
    const icons = { dark:'bi-moon-stars', light:'bi-sun', bw:'bi-circle-half' };
    btn.innerHTML = `<i class="bi ${icons[t] || 'bi-moon-stars'}"></i>`;
}