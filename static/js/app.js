/**
 * FacultyFlow - Frontend Application Controller
 * Handles real authentication, role-based landing pages, and multi-screen navigation
 */

const AppState = {
  currentUser: null,
  currentView: 'view-login',
  users: [],
  adminUsers: [],
  timetableDay: 'Mon'
};

document.addEventListener('DOMContentLoaded', async () => {
  await loadUsers();
  checkAuthSession();
});

async function apiCall(endpoint, method = 'GET', body = null) {
  const options = { method, headers: {} };
  if (body && !(body instanceof FormData)) {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(body);
  } else if (body instanceof FormData) {
    options.body = body;
  }
  try {
    const res = await fetch(endpoint, options);
    return await res.json();
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    return null;
  }
}

async function loadUsers() {
  AppState.users = await apiCall('/api/auth/users') || [];
}

const ROLE_PERMISSIONS = {
  student: ['view-student-dashboard', 'view-timetable', 'view-calendar', 'view-notifications'],
  faculty: ['view-faculty-dashboard', 'view-apply-leave', 'view-my-leaves', 'view-timetable', 'view-notifications', 'view-leave-history', 'view-leave-balance'],
  hod: ['view-leave-slot-queue', 'view-hod-approvals', 'view-substitutes', 'view-timetable', 'view-calendar', 'view-notifications'],
  dean: ['view-dean-queue', 'view-timetable', 'view-calendar', 'view-notifications'],
  principal: ['view-principal-dashboard', 'view-calendar', 'view-admin-panel', 'view-timetable', 'view-notifications'],
  admin: ['*']
};

/**
 * Check if a session already exists; if not, display Login Page (Screen 1)
 */
function checkAuthSession() {
  const savedUser = sessionStorage.getItem('facultyflow_user');
  if (savedUser) {
    try {
      AppState.currentUser = JSON.parse(savedUser);
      updateUserUI();
      const defaultView = getDefaultViewForRole(AppState.currentUser.role);
      switchView(defaultView);
      return;
    } catch (e) {
      sessionStorage.removeItem('facultyflow_user');
    }
  }

  // Not logged in -> Show Screen 1 Login
  showLoginPage();
}

function getDefaultViewForRole(role) {
  switch (role) {
    case 'student':
      return 'view-student-dashboard';
    case 'faculty':
      return 'view-faculty-dashboard';
    case 'hod':
      return 'view-hod-approvals';
    case 'dean':
      return 'view-dean-queue';
    case 'principal':
      return 'view-principal-dashboard';
    case 'admin':
      return 'view-admin-panel';
    default:
      return 'view-faculty-dashboard';
  }
}

function showLoginPage() {
  const loginEl = document.getElementById('view-login');
  const appRoot = document.getElementById('app-root');
  const emailInput = document.getElementById('login-email');
  const passInput = document.getElementById('login-password');
  const errorEl = document.getElementById('login-error-msg');

  // Ensure fields are completely empty with clean placeholders
  if (emailInput) emailInput.value = '';
  if (passInput) passInput.value = '';
  if (errorEl) {
    errorEl.textContent = '';
    errorEl.style.display = 'none';
  }

  if (loginEl) loginEl.style.display = 'block';
  if (appRoot) appRoot.style.display = 'none';
  AppState.currentView = 'view-login';
}

/**
 * Real Login Handler: verifies email/username and loads that user's role and dashboard
 */
async function handleLoginSubmit(event) {
  if (event) event.preventDefault();
  const emailInput = document.getElementById('login-email');
  const passwordInput = document.getElementById('login-password');
  const errorEl = document.getElementById('login-error-msg');
  const submitBtn = document.getElementById('login-submit-btn');

  const emailVal = emailInput ? emailInput.value.trim() : '';
  const passwordVal = passwordInput ? passwordInput.value : '';

  if (!emailVal || !passwordVal) {
    if (errorEl) {
      errorEl.textContent = 'Please enter both your email/username and password.';
      errorEl.style.display = 'block';
    }
    return;
  }

  if (errorEl) errorEl.style.display = 'none';
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Logging in...';
  }

  const res = await apiCall('/api/auth/login', 'POST', {
    email: emailVal,
    password: passwordVal
  });

  if (submitBtn) {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Login';
  }

  if (res && res.success && res.user) {
    AppState.currentUser = res.user;
    sessionStorage.setItem('facultyflow_user', JSON.stringify(res.user));

    const loginEl = document.getElementById('view-login');
    const appRoot = document.getElementById('app-root');
    if (loginEl) loginEl.style.display = 'none';
    if (appRoot) appRoot.style.display = 'flex';

    updateUserUI();

    // Automatically navigate to that user's specific landing dashboard
    const landingView = getDefaultViewForRole(res.user.role);
    switchView(landingView);
  } else {
    if (errorEl) {
      const msg = (res && res.message) || (res && res.detail) || 'Invalid credentials or server error. Please try again.';
      errorEl.textContent = msg;
      errorEl.style.display = 'block';
    }
  }
}

/**
 * Logout Handler: clears session and redirects to Screen 1 Login
 */
function handleLogout() {
  sessionStorage.removeItem('facultyflow_user');
  AppState.currentUser = null;
  showLoginPage();
}

/**
 * Update Sidebar Avatar, Name, Designation, and Dynamic Navigation Links
 */
function updateUserUI() {
  const u = AppState.currentUser;
  if (!u) return;

  const avatarEl = document.getElementById('sidebar-user-avatar');
  const mobileAvatarEl = document.getElementById('mobile-topbar-avatar');
  const nameEl = document.getElementById('sidebar-user-name');
  const roleEl = document.getElementById('sidebar-user-role');

  const avatarSrc = u.avatar || DEFAULT_AVATAR;
  if (avatarEl) avatarEl.src = avatarSrc;
  if (mobileAvatarEl) mobileAvatarEl.src = avatarSrc;
  if (nameEl) nameEl.textContent = u.name;
  if (roleEl) {
    if (u.role === 'student') roleEl.textContent = 'Student - 5th Sem A';
    else if (u.role === 'faculty') roleEl.textContent = 'Faculty - CSE(AIML)';
    else if (u.role === 'hod') roleEl.textContent = 'HOD - CSE(AIML)';
    else if (u.role === 'dean') roleEl.textContent = 'Dean - Academic';
    else if (u.role === 'principal') roleEl.textContent = 'Principal';
    else if (u.role === 'admin') roleEl.textContent = 'Administrator';
    else roleEl.textContent = `${u.designation || 'User'} - ${u.department}`;
  }

  renderSidebarNav(u.role);
}

function renderSidebarNav(role) {
  const navContainer = document.getElementById('sidebar-nav-container');
  if (!navContainer) return;

  let links = [];

  if (role === 'student') {
    links = [
      { id: 'view-student-dashboard', label: 'Dashboard', icon: '<path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>' },
      { id: 'view-timetable', label: 'Class Timetable', icon: '<path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>' },
      { id: 'view-calendar', label: 'College Calendar', icon: '<path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>' },
      { id: 'view-notifications', label: 'Notifications', badge: '1', icon: '<path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>' }
    ];
  } else if (role === 'faculty') {
    links = [
      { id: 'view-faculty-dashboard', label: 'Dashboard', icon: '<path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>' },
      { id: 'view-apply-leave', label: 'Apply Leave', icon: '<path d="M12 4v16m8-8H4"/>' },
      { id: 'view-my-leaves', label: 'My Leaves', icon: '<path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>' },
      { id: 'view-timetable', label: 'Timetable', icon: '<path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>' },
      { id: 'view-notifications', label: 'Notifications', badge: '4', icon: '<path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>' },
      { id: 'view-leave-history', label: 'Leave History', icon: '<path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>' },
      { id: 'view-leave-balance', label: 'Leave Balance', icon: '<path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>' }
    ];
  } else if (role === 'hod') {
    links = [
      { id: 'view-leave-slot-queue', label: 'Slot Queue', icon: '<path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>' },
      { id: 'view-hod-approvals', label: 'Pending Approvals', icon: '<path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>' },
      { id: 'view-substitutes', label: 'Substitute Mgmt', icon: '<path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>' },
      { id: 'view-timetable', label: 'Timetable', icon: '<path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>' },
      { id: 'view-notifications', label: 'Notifications', badge: '2', icon: '<path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>' }
    ];
  } else if (role === 'dean') {
    links = [
      { id: 'view-dean-queue', label: 'Approval Queue', icon: '<path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>' },
      { id: 'view-timetable', label: 'Timetable', icon: '<path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>' },
      { id: 'view-notifications', label: 'Notifications', icon: '<path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>' }
    ];
  } else if (role === 'principal') {
    links = [
      { id: 'view-principal-dashboard', label: 'Dashboard', icon: '<path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>' },
      { id: 'view-calendar', label: 'College Calendar', icon: '<path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>' },
      { id: 'view-admin-panel', label: 'Faculty Directory', icon: '<path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>' },
      { id: 'view-timetable', label: 'Timetable', icon: '<path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>' }
    ];
  } else {
    // Admin (Full System Access)
    links = [
      { id: 'view-admin-panel', label: 'User & Credentials', icon: '<path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>' },
      { id: 'view-principal-dashboard', label: 'Institutional Overview', icon: '<path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>' },
      { id: 'view-hod-approvals', label: 'Leave Approvals', icon: '<path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>' },
      { id: 'view-leave-slot-queue', label: 'Slot Quota & Queue', icon: '<path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>' },
      { id: 'view-timetable', label: 'Academic Timetable', icon: '<path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>' },
      { id: 'view-substitutes', label: 'Substitutions', icon: '<path d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/>' },
      { id: 'view-calendar', label: 'College Calendar', icon: '<path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>' },
      { id: 'view-notifications', label: 'Notifications', icon: '<path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>' }
    ];
  }

  navContainer.innerHTML = links.map(l => `
    <a class="nav-link ${l.id === AppState.currentView ? 'active' : ''}" data-view="${l.id}" onclick="switchView('${l.id}')">
      <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">${l.icon}</svg>
      <span>${l.label}</span>
      ${l.badge ? `<span class="nav-badge">${l.badge}</span>` : ''}
    </a>
  `).join('');
}

function switchView(viewId) {
  if (viewId === 'view-login') {
    showLoginPage();
    return;
  }

  // Access Control: check if current role has permission to view this screen
  if (AppState.currentUser && AppState.currentUser.role !== 'admin') {
    const allowed = ROLE_PERMISSIONS[AppState.currentUser.role] || [];
    if (!allowed.includes(viewId)) {
      console.warn(`Access restricted: ${AppState.currentUser.role} cannot access ${viewId}`);
      viewId = getDefaultViewForRole(AppState.currentUser.role);
    }
  }

  const loginEl = document.getElementById('view-login');
  const appRoot = document.getElementById('app-root');
  if (loginEl) loginEl.style.display = 'none';
  if (appRoot) appRoot.style.display = 'flex';

  AppState.currentView = viewId;

  // Deactivate all sections, activate current
  document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
  const target = document.getElementById(viewId);
  if (target) {
    target.classList.add('active');
  }

  // Update active state in sidebar nav
  document.querySelectorAll('.sidebar-nav .nav-link').forEach(link => {
    link.classList.toggle('active', link.dataset.view === viewId);
  });

  // Load screen data
  refreshViewData(viewId);

  // Close mobile sidebar on navigation
  closeMobileSidebar();
}

function toggleMobileSidebar() {
  const sidebar = document.getElementById('app-sidebar');
  const backdrop = document.getElementById('sidebar-backdrop');
  if (!sidebar) return;
  const isOpen = sidebar.classList.contains('mobile-open');
  if (isOpen) {
    closeMobileSidebar();
  } else {
    sidebar.classList.add('mobile-open');
    if (backdrop) backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeMobileSidebar() {
  const sidebar = document.getElementById('app-sidebar');
  const backdrop = document.getElementById('sidebar-backdrop');
  if (sidebar) sidebar.classList.remove('mobile-open');
  if (backdrop) backdrop.classList.remove('active');
  document.body.style.overflow = '';
}

function refreshViewData(viewId) {
  switch (viewId) {
    case 'view-faculty-dashboard':
      loadFacultyDashboard();
      break;
    case 'view-apply-leave':
      loadApplyLeave();
      break;
    case 'view-my-leaves':
      loadMyLeaves('all');
      break;
    case 'view-timetable':
      loadTimetable(AppState.timetableDay);
      break;
    case 'view-leave-slot-queue':
      loadSlotQueue();
      break;
    case 'view-hod-approvals':
      loadHODApprovals();
      break;
    case 'view-dean-queue':
      loadDeanQueue();
      break;
    case 'view-calendar':
      initCalendarGrid();
      break;
    case 'view-substitutes':
      loadSubstitutes();
      break;
    case 'view-leave-history':
      loadLeaveHistory();
      break;
    case 'view-admin-panel':
      loadAdminPanel();
      break;
  }
}

// --- Screen 2: Faculty Dashboard ---
async function loadFacultyDashboard() {
  document.getElementById('dash-pending-count').textContent = '2';
  document.getElementById('dash-approved-count').textContent = '5';
  document.getElementById('dash-rejected-count').textContent = '1';
  document.getElementById('dash-affected-count').textContent = '3';

  updateCircleSvg('dash-slot-svg', 1, 3);
  document.getElementById('dash-slot-text').textContent = '1/3';
}

function updateCircleSvg(svgId, val, total) {
  const svg = document.getElementById(svgId);
  if (!svg) return;
  const circle = svg.querySelector('.gauge-circle-fill');
  if (!circle) return;
  const radius = circle.r.baseVal.value;
  const circumference = 2 * Math.PI * radius;
  circle.style.strokeDasharray = `${circumference} ${circumference}`;
  const ratio = total > 0 ? (val / total) : 0;
  circle.style.strokeDashoffset = circumference - (ratio * circumference);
}

// --- Screen 3: Apply Leave ---
function loadApplyLeave() {
  updateCircleSvg('apply-slot-svg', 1, 3);
  const textEl = document.getElementById('apply-slot-text');
  if (textEl) textEl.textContent = '1/3';
}

async function handleApplyLeaveSubmit(e) {
  e.preventDefault();
  alert('Leave application submitted successfully! Assigned Queue Position: #2');
  switchView('view-slot-status');
}

// --- Screen 5: Notifications ---
function filterNotificationsTab(btn, tab) {
  document.querySelectorAll('#view-notifications .tab-pill').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

// --- Screen 6: My Leave Requests ---
const myLeavesData = [
  { id: 'LV1026', date: '21 Sep 2026', type: 'CL', status: 'Waiting for Slot', badge: 'badge-queue' },
  { id: 'LV1018', date: '12 Sep 2026', type: 'CL', status: 'Pending', badge: 'badge-pending' },
  { id: 'LV1007', date: '05 Sep 2026', type: 'ML', status: 'Rejected', badge: 'badge-rejected' },
  { id: 'LV1013', date: '28 Aug 2026', type: 'OD', status: 'Approved', badge: 'badge-approved' },
  { id: 'LV1009', date: '20 Aug 2026', type: 'CL', status: 'Approved', badge: 'badge-approved' }
];

function loadMyLeaves(filter = 'all') {
  const tbody = document.getElementById('my-leaves-tbody');
  if (!tbody) return;

  const filtered = myLeavesData.filter(d => {
    if (filter === 'all') return true;
    if (filter === 'pending') return d.status === 'Pending' || d.status === 'Waiting for Slot';
    if (filter === 'approved') return d.status === 'Approved';
    if (filter === 'rejected') return d.status === 'Rejected';
    if (filter === 'canceled') return d.status === 'Canceled';
    return true;
  });

  tbody.innerHTML = filtered.map(row => `
    <tr>
      <td style="font-weight:700;">${row.id}</td>
      <td style="color:var(--text-muted);">${row.date}</td>
      <td><strong>${row.type}</strong></td>
      <td><span class="badge ${row.badge}">${row.status}</span></td>
      <td><button class="btn-table-view" onclick="openLeaveModal('${row.id}')">View</button></td>
    </tr>
  `).join('');
}

function filterMyLeavesTab(btn, tab) {
  document.querySelectorAll('#view-my-leaves .tab-pill').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  loadMyLeaves(tab);
}

// --- Screen 7: Timetable ---
const timetableSchedule = [
  { time: '09:00 - 10:00', subject: 'CN', class: '5th Sem A', room: '204' },
  { time: '10:00 - 11:00', subject: 'TOC', class: '5th Sem A', room: '204' },
  { time: '11:00 - 12:00', subject: 'UNIX', class: '5th Sem B', room: '301' },
  { time: '12:00 - 01:00', subject: 'LB', class: '5th Sem A', room: '204' },
  { time: '02:00 - 03:00', subject: 'RMYK', class: '5th Sem A', room: '302' },
  { time: '03:00 - 04:00', subject: 'SOFTWARE ENG', class: '5th Sem A', room: '204' }
];

function loadTimetable(day) {
  AppState.timetableDay = day;
  document.querySelectorAll('.tt-day-tab').forEach(t => {
    t.classList.toggle('active', t.dataset.day === day);
  });
  const tbody = document.getElementById('timetable-tbody');
  if (!tbody) return;

  tbody.innerHTML = timetableSchedule.map(row => `
    <tr>
      <td style="font-weight:600; color:var(--text-muted);">${row.time}</td>
      <td><strong style="color:var(--text-dark);">${row.subject}</strong></td>
      <td>${row.class}</td>
      <td><span style="background:#f1f5f9; padding:2px 7px; border-radius:4px; font-weight:700;">${row.room}</span></td>
    </tr>
  `).join('');
}

// --- Screen 8: Slot Queue (HOD) ---
const slotQueueData = [
  { num: 1, name: 'Dr. B', date: '21 Sep 2026', status: 'On Approval', badge: 'badge-pending' },
  { num: 2, name: 'Dr. C', date: '22 Sep 2026', status: 'Waiting', badge: 'badge-queue' },
  { num: 3, name: 'Dr. D', date: '23 Sep 2026', status: 'Waiting', badge: 'badge-queue' },
  { num: 4, name: 'Dr. E', date: '25 Sep 2026', status: 'Waiting', badge: 'badge-queue' }
];

function loadSlotQueue() {
  const tbody = document.getElementById('slot-queue-tbody');
  if (!tbody) return;
  tbody.innerHTML = slotQueueData.map(r => `
    <tr>
      <td style="font-weight:700;">${r.num}</td>
      <td><strong>${r.name}</strong></td>
      <td style="color:var(--text-muted);">${r.date}</td>
      <td><span class="badge ${r.badge}">${r.status}</span></td>
    </tr>
  `).join('');
}

// --- Screen 9: HOD Pending Approvals ---
const hodApprovalsData = [
  { name: 'Dr. B', date: '21 Sep 2026', type: 'CL', reason: 'Personal' },
  { name: 'Dr. C', date: '22 Sep 2026', type: 'ML', reason: 'Medical' },
  { name: 'Dr. D', date: '25 Sep 2026', type: 'CL', reason: 'Family function' }
];

function loadHODApprovals() {
  const tbody = document.getElementById('hod-approvals-tbody');
  if (!tbody) return;
  tbody.innerHTML = hodApprovalsData.map(r => `
    <tr>
      <td><strong>${r.name}</strong></td>
      <td style="color:var(--text-muted);">${r.date}</td>
      <td><strong>${r.type}</strong></td>
      <td>${r.reason}</td>
      <td>
        <div style="display:flex; gap:6px;">
          <button class="btn-table-view" onclick="alert('Viewing application details')">View</button>
          <button class="btn-success-sm" onclick="alert('Approved application for ${r.name}')">Approve</button>
          <button class="btn-danger-sm" onclick="alert('Rejected application')">Reject</button>
        </div>
      </td>
    </tr>
  `).join('');
}

// --- Screen 10: Dean Approval Queue ---
const deanQueueData = [
  { name: 'Dr. A', dept: 'CSE(AIML)', date: '21 Sep 2026', status: 'HOD ✓  Dean Pending' },
  { name: 'Dr. E', dept: 'ECE', date: '22 Sep 2026', status: 'HOD ✓  Dean Pending' },
  { name: 'Dr. F', dept: 'ME', date: '25 Sep 2026', status: 'HOD ✓  Dean Pending' }
];

function loadDeanQueue() {
  const tbody = document.getElementById('dean-queue-tbody');
  if (!tbody) return;
  tbody.innerHTML = deanQueueData.map(r => `
    <tr>
      <td><strong>${r.name}</strong></td>
      <td>${r.dept}</td>
      <td style="color:var(--text-muted);">${r.date}</td>
      <td>
        <span class="badge badge-approved" style="margin-right:4px;">HOD ✓</span>
        <span class="badge badge-queue">Dean Pending</span>
      </td>
      <td><button class="btn-table-view" onclick="alert('Viewing application')">View</button></td>
    </tr>
  `).join('');
}

// --- Screen 12: Calendar Grid ---
function initCalendarGrid() {
  const container = document.getElementById('calendar-grid-cells');
  if (!container) return;

  // September 2026 starts on Tuesday (Su, Mo, Tu -> 2 empty offsets)
  let html = `
    <div class="cal-cell" style="opacity:0.3;"><span class="cal-date-num">30</span></div>
    <div class="cal-cell" style="opacity:0.3;"><span class="cal-date-num">31</span></div>
  `;

  for (let day = 1; day <= 30; day++) {
    const isSelected = day === 21;
    let dotHtml = '<span class="cal-density-dot" style="background:#cbd5e1;"></span>';
    if (day === 5 || day === 12 || day === 15) {
      dotHtml = '<span class="cal-density-dot" style="background:#f59e0b;"></span>';
    } else if (day === 21 || day === 22 || day === 25) {
      dotHtml = '<span class="cal-density-dot" style="background:#2563eb;"></span>';
    }

    html += `
      <div class="cal-cell ${isSelected ? 'selected' : ''}" onclick="selectCalendarDay(${day}, this)">
        <span class="cal-date-num">${day}</span>
        ${dotHtml}
      </div>
    `;
  }
  container.innerHTML = html;
}

function selectCalendarDay(day, el) {
  document.querySelectorAll('.cal-cell').forEach(c => c.classList.remove('selected'));
  el.classList.add('selected');
}

// --- Screen 13: Substitute Management ---
const substitutesData = [
  { faculty: 'Dr. A', subject: 'CN', class: '5A', time: '9:00 - 10:00', status: 'Pending', assigned: false },
  { faculty: 'Dr. B', subject: 'TOC', class: '5B', time: '11:00 - 12:00', status: 'Assigned', assigned: true },
  { faculty: 'Dr. C', subject: 'UNIX', class: '5A', time: '2:00 - 3:00', status: 'Pending', assigned: false }
];

function loadSubstitutes() {
  const tbody = document.getElementById('substitutes-tbody');
  if (!tbody) return;
  tbody.innerHTML = substitutesData.map(r => `
    <tr>
      <td><strong>${r.faculty}</strong></td>
      <td><span class="class-sub-badge">${r.subject}</span></td>
      <td>${r.class}</td>
      <td style="color:var(--text-muted);">${r.time}</td>
      <td><span class="badge ${r.assigned ? 'badge-approved' : 'badge-pending'}">${r.status}</span></td>
      <td>
        ${r.assigned
          ? `<button class="btn-outline-sm" onclick="alert('View assigned substitute')">View</button>`
          : `<button class="btn btn-primary btn-xs" onclick="alert('Allocating substitute for ${r.faculty}')">Assign</button>`
        }
      </td>
    </tr>
  `).join('');
}

// --- Screen 14: Leave History ---
const historyData = [
  { id: 'LV1006', date: '21 Sep 2026', type: 'CL', status: 'Pending', badge: 'badge-pending' },
  { id: 'LV1018', date: '12 Sep 2026', type: 'CL', status: 'Approved', badge: 'badge-approved' },
  { id: 'LV1007', date: '05 Sep 2026', type: 'ML', status: 'Rejected', badge: 'badge-rejected' },
  { id: 'LV1013', date: '28 Aug 2026', type: 'OD', status: 'Approved', badge: 'badge-approved' },
  { id: 'LV1009', date: '20 Aug 2026', type: 'CL', status: 'Approved', badge: 'badge-approved' }
];

function loadLeaveHistory() {
  const tbody = document.getElementById('history-tbody');
  if (!tbody) return;
  tbody.innerHTML = historyData.map(r => `
    <tr>
      <td style="font-weight:700;">${r.id}</td>
      <td style="color:var(--text-muted);">${r.date}</td>
      <td><strong>${r.type}</strong></td>
      <td><span class="badge ${r.badge}">${r.status}</span></td>
    </tr>
  `).join('');
}

// --- Screen 16: Admin User & Credential Management (MongoDB Atlas) ---

const DEFAULT_AVATAR = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 128 128'%3E%3Ccircle cx='64' cy='64' r='64' fill='%23e2e8f0'/%3E%3Cpath d='M64 68a24 24 0 100-48 24 24 0 000 48zm0 12c-26.7 0-48 16-48 36v12h96v-12c0-20-21.3-36-48-36z' fill='%2394a3b8'/%3E%3C/svg%3E";

let selectedDeleteUserId = null;

async function loadAdminPanel() {
  const tbody = document.getElementById('admin-users-tbody') || document.getElementById('admin-faculty-tbody');
  if (!tbody) return;

  tbody.innerHTML = `
    <tr>
      <td colspan="6" style="text-align:center; padding:32px; color:var(--text-muted);">
        <div style="display:inline-flex; align-items:center; gap:8px;">
          Loading user accounts...
        </div>
      </td>
    </tr>
  `;

  const users = await apiCall('/api/admin/users');
  AppState.adminUsers = Array.isArray(users) ? users : (AppState.users || []);

  // Calculate & update KPI statistics
  const total = AppState.adminUsers.length;
  const facultyCount = AppState.adminUsers.filter(u => (u.role || '').toLowerCase() === 'faculty').length;
  const leadershipCount = AppState.adminUsers.filter(u => ['hod', 'dean', 'principal'].includes((u.role || '').toLowerCase())).length;
  const adminCount = AppState.adminUsers.filter(u => (u.role || '').toLowerCase() === 'admin').length;

  const totalEl = document.getElementById('admin-stat-total');
  const facEl = document.getElementById('admin-stat-faculty');
  const leadEl = document.getElementById('admin-stat-leadership');
  const admEl = document.getElementById('admin-stat-admin');

  if (totalEl) totalEl.textContent = total;
  if (facEl) facEl.textContent = facultyCount;
  if (leadEl) leadEl.textContent = leadershipCount;
  if (admEl) admEl.textContent = adminCount;

  filterAdminUsers();
}

function renderAdminTable(userList) {
  const tbody = document.getElementById('admin-users-tbody') || document.getElementById('admin-faculty-tbody');
  if (!tbody) return;

  if (!userList || userList.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" style="text-align:center; padding:36px; color:var(--text-muted);">
          No users match the selected search or filter criteria.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = userList.map(u => {
    const roleLower = (u.role || 'faculty').toLowerCase();
    const initials = (u.name || 'U').split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();
    const avatarImg = u.avatar
      ? `<img src="${u.avatar}" class="avatar-img-sm" alt="${u.name}" onerror="this.outerHTML='<div class=\\'avatar-initials-sm\\'>${initials}</div>'">`
      : `<div class="avatar-initials-sm">${initials}</div>`;

    const roleBadgeClass = `role-${roleLower}`;
    const cleanPassword = u.password || 'password123';
    const rowPwdId = `pwd-row-${u.id}`;

    return `
      <tr>
        <td>
          <div class="user-avatar-cell">
            ${avatarImg}
            <div>
              <div style="font-weight:700; color:var(--text-dark);">${escapeHtml(u.name || 'User')}</div>
              <div style="font-size:11px; color:var(--text-muted);">${escapeHtml(u.designation || 'Academic Staff')}</div>
            </div>
          </div>
        </td>
        <td>
          <span style="font-family:monospace; font-size:12px; font-weight:600; color:var(--text-body);">${escapeHtml(u.email || '-')}</span>
        </td>
        <td>
          <span class="role-badge ${roleBadgeClass}">${roleLower}</span>
        </td>
        <td>
          <div style="font-weight:600;">${escapeHtml(u.department || 'General')}</div>
          <div style="font-size:11px; color:var(--text-muted);">${escapeHtml(u.phone || '-')}</div>
        </td>
        <td>
          <div class="pwd-masked-pill">
            <span id="${rowPwdId}">••••••••</span>
            <button type="button" class="pwd-peek-btn" title="Show / Hide Password" onclick="togglePasswordPeek('${rowPwdId}', '${escapeHtml(cleanPassword)}')">
              <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
            </button>
          </div>
        </td>
        <td style="text-align:right;">
          <div class="btn-action-group" style="justify-content:flex-end;">
            <button class="btn-icon-sm btn-edit" onclick="openEditUserModal('${u.id}')" title="Edit Credentials & Profile">
              <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              Edit
            </button>
            <button class="btn-icon-sm btn-delete" onclick="openDeleteUserModal('${u.id}')" title="Delete User">
              <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

function filterAdminUsers() {
  const query = (document.getElementById('admin-user-search')?.value || '').toLowerCase().trim();
  const roleFilter = document.getElementById('admin-role-filter')?.value || 'All';
  const deptFilter = document.getElementById('admin-dept-filter')?.value || 'All';

  const all = AppState.adminUsers || [];
  const filtered = all.filter(u => {
    // Role filter
    if (roleFilter !== 'All' && (u.role || '').toLowerCase() !== roleFilter.toLowerCase()) {
      return false;
    }
    // Department filter
    if (deptFilter !== 'All' && (u.department || '').toLowerCase() !== deptFilter.toLowerCase()) {
      return false;
    }
    // Query search
    if (query) {
      const matchName = (u.name || '').toLowerCase().includes(query);
      const matchEmail = (u.email || '').toLowerCase().includes(query);
      const matchDept = (u.department || '').toLowerCase().includes(query);
      const matchRole = (u.role || '').toLowerCase().includes(query);
      const matchDesig = (u.designation || '').toLowerCase().includes(query);
      return matchName || matchEmail || matchDept || matchRole || matchDesig;
    }
    return true;
  });

  const countEl = document.getElementById('admin-filtered-count');
  if (countEl) {
    countEl.textContent = `Showing ${filtered.length} of ${all.length} accounts`;
  }

  renderAdminTable(filtered);
}

/**
 * Handle direct device image upload (Max 100MB)
 * Validates file size, extracts image, and downscales to high-res square avatar via Canvas
 */
function handleAvatarDeviceUpload(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;

  const statusEl = document.getElementById('user-form-avatar-status');
  const previewImg = document.getElementById('user-form-avatar-preview');
  const dataInput = document.getElementById('user-form-avatar-data');
  const resetBtn = document.getElementById('user-form-avatar-reset-btn');

  // Validate image MIME type
  if (!file.type.startsWith('image/')) {
    if (statusEl) {
      statusEl.textContent = 'Please select a valid image file (JPG, PNG, WebP, GIF).';
      statusEl.className = 'avatar-upload-status error';
      statusEl.style.display = 'block';
    }
    event.target.value = '';
    return;
  }

  // Strict 100MB max limit
  const MAX_SIZE_MB = 100;
  const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;
  if (file.size > MAX_SIZE_BYTES) {
    const sizeInMB = (file.size / (1024 * 1024)).toFixed(1);
    if (statusEl) {
      statusEl.textContent = `File size (${sizeInMB}MB) exceeds the maximum allowed limit of 100MB.`;
      statusEl.className = 'avatar-upload-status error';
      statusEl.style.display = 'block';
    }
    alert(`File is too large (${sizeInMB}MB)! Maximum allowed image size is 100MB.`);
    event.target.value = '';
    return;
  }

  const sizeStr = file.size > 1024 * 1024
    ? `${(file.size / (1024 * 1024)).toFixed(1)}MB`
    : `${Math.round(file.size / 1024)}KB`;

  if (statusEl) {
    statusEl.textContent = `Processing image (${sizeStr})...`;
    statusEl.className = 'avatar-upload-status';
    statusEl.style.display = 'block';
  }

  const reader = new FileReader();
  reader.onload = function(e) {
    const img = new Image();
    img.onload = function() {
      try {
        const canvas = document.createElement('canvas');
        const MAX_DIM = 400; // 400x400 max gives crystal-clear resolution on all screen densities
        const width = img.width;
        const height = img.height;

        // Crop to center square
        const minDim = Math.min(width, height);
        const sx = (width - minDim) / 2;
        const sy = (height - minDim) / 2;

        canvas.width = Math.min(minDim, MAX_DIM);
        canvas.height = canvas.width;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, sx, sy, minDim, minDim, 0, 0, canvas.width, canvas.height);

        const optimizedDataUrl = canvas.toDataURL('image/jpeg', 0.88);

        if (previewImg) previewImg.src = optimizedDataUrl;
        if (dataInput) dataInput.value = optimizedDataUrl;
        if (resetBtn) resetBtn.style.display = 'inline-block';

        if (statusEl) {
          statusEl.textContent = `✓ Uploaded: ${file.name} (${sizeStr})`;
          statusEl.className = 'avatar-upload-status success';
          statusEl.style.display = 'block';
        }
      } catch (err) {
        console.error('Canvas error:', err);
        if (previewImg) previewImg.src = e.target.result;
        if (dataInput) dataInput.value = e.target.result;
        if (resetBtn) resetBtn.style.display = 'inline-block';
      }
    };
    img.onerror = function() {
      if (statusEl) {
        statusEl.textContent = 'Could not process image file. Please choose another image.';
        statusEl.className = 'avatar-upload-status error';
        statusEl.style.display = 'block';
      }
    };
    img.src = e.target.result;
  };
  reader.onerror = function() {
    if (statusEl) {
      statusEl.textContent = 'Error reading file from device.';
      statusEl.className = 'avatar-upload-status error';
      statusEl.style.display = 'block';
    }
  };
  reader.readAsDataURL(file);
}

function resetUploadedAvatar() {
  const fileInput = document.getElementById('user-form-avatar-file');
  const previewImg = document.getElementById('user-form-avatar-preview');
  const dataInput = document.getElementById('user-form-avatar-data');
  const statusEl = document.getElementById('user-form-avatar-status');
  const resetBtn = document.getElementById('user-form-avatar-reset-btn');

  if (fileInput) fileInput.value = '';
  if (dataInput) dataInput.value = DEFAULT_AVATAR;
  if (previewImg) previewImg.src = DEFAULT_AVATAR;
  if (statusEl) {
    statusEl.textContent = 'Avatar reset to default.';
    statusEl.className = 'avatar-upload-status';
    statusEl.style.display = 'block';
  }
  if (resetBtn) resetBtn.style.display = 'none';
}

function handleRoleChange(role) {
  const desigInput = document.getElementById('user-form-designation');
  const deptSelect = document.getElementById('user-form-department');
  if (!desigInput) return;

  const defaults = {
    faculty: { desig: 'Assistant Professor', dept: 'CSE(AIML)' },
    hod: { desig: 'Professor & HOD', dept: 'CSE(AIML)' },
    dean: { desig: 'Dean Academic', dept: 'Administration' },
    principal: { desig: 'Principal', dept: 'Administration' },
    admin: { desig: 'System Administrator', dept: 'Administration' },
    student: { desig: 'Student - 5th Sem', dept: 'CSE(AIML)' }
  };

  if (defaults[role]) {
    desigInput.value = defaults[role].desig;
    if (deptSelect && ['dean', 'principal', 'admin'].includes(role)) {
      deptSelect.value = 'Administration';
    }
  }
}

function openAddUserModal() {
  document.getElementById('user-modal-title').textContent = 'Add New User & Account';
  document.getElementById('user-form-mode').value = 'add';
  document.getElementById('user-form-id').value = '';

  document.getElementById('user-form-name').value = '';
  document.getElementById('user-form-email').value = '';
  document.getElementById('user-form-password').value = 'password123';
  document.getElementById('user-form-role').value = 'faculty';
  document.getElementById('user-form-department').value = 'CSE(AIML)';
  document.getElementById('user-form-designation').value = 'Assistant Professor';
  document.getElementById('user-form-phone').value = '';

  const defaultAvatar = DEFAULT_AVATAR;
  document.getElementById('user-form-avatar-data').value = defaultAvatar;
  document.getElementById('user-form-avatar-preview').src = defaultAvatar;

  const fileInput = document.getElementById('user-form-avatar-file');
  if (fileInput) fileInput.value = '';
  const statusEl = document.getElementById('user-form-avatar-status');
  if (statusEl) statusEl.style.display = 'none';
  const resetBtn = document.getElementById('user-form-avatar-reset-btn');
  if (resetBtn) resetBtn.style.display = 'none';

  document.getElementById('user-modal-backdrop').classList.add('active');
}

function openEditUserModal(userId) {
  const user = (AppState.adminUsers || []).find(u => u.id === userId);
  if (!user) {
    alert('User not found.');
    return;
  }

  document.getElementById('user-modal-title').textContent = `Edit Credentials: ${user.name}`;
  document.getElementById('user-form-mode').value = 'edit';
  document.getElementById('user-form-id').value = user.id;

  document.getElementById('user-form-name').value = user.name || '';
  document.getElementById('user-form-email').value = user.email || '';
  document.getElementById('user-form-password').value = user.password || 'password123';
  document.getElementById('user-form-role').value = user.role || 'faculty';
  document.getElementById('user-form-department').value = user.department || 'CSE(AIML)';
  document.getElementById('user-form-designation').value = user.designation || '';
  document.getElementById('user-form-phone').value = user.phone || '';

  const avatar = user.avatar || DEFAULT_AVATAR;
  document.getElementById('user-form-avatar-data').value = avatar;
  document.getElementById('user-form-avatar-preview').src = avatar;

  const fileInput = document.getElementById('user-form-avatar-file');
  if (fileInput) fileInput.value = '';

  const statusEl = document.getElementById('user-form-avatar-status');
  const resetBtn = document.getElementById('user-form-avatar-reset-btn');

  const hasCustomAvatar = avatar && avatar !== DEFAULT_AVATAR;
  if (statusEl) {
    statusEl.textContent = hasCustomAvatar ? 'Photo attached' : '';
    statusEl.className = 'avatar-upload-status';
    statusEl.style.display = hasCustomAvatar ? 'block' : 'none';
  }
  if (resetBtn) resetBtn.style.display = hasCustomAvatar ? 'inline-block' : 'none';

  document.getElementById('user-modal-backdrop').classList.add('active');
}

async function handleSaveUserSubmit(e) {
  e.preventDefault();
  const mode = document.getElementById('user-form-mode').value;
  const userId = document.getElementById('user-form-id').value;
  const submitBtn = document.getElementById('user-modal-submit-btn');

  const payload = {
    name: document.getElementById('user-form-name').value.trim(),
    email: document.getElementById('user-form-email').value.trim().toLowerCase(),
    password: document.getElementById('user-form-password').value.trim() || 'password123',
    role: document.getElementById('user-form-role').value,
    department: document.getElementById('user-form-department').value,
    designation: document.getElementById('user-form-designation').value.trim(),
    phone: document.getElementById('user-form-phone').value.trim(),
    avatar: document.getElementById('user-form-avatar-data').value.trim() || DEFAULT_AVATAR
  };

  if (!payload.name || !payload.email) {
    alert('Name and Email are required.');
    return;
  }

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Saving...';
  }

  try {
    let res;
    if (mode === 'add') {
      res = await apiCall('/api/admin/users', 'POST', payload);
    } else {
      res = await apiCall(`/api/admin/users/${userId}`, 'PUT', payload);
    }

    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Save Changes';
    }

    if (res && res.success) {
      closeModal('user-modal-backdrop');
      showAdminToast(mode === 'add' ? `User '${payload.name}' created successfully!` : `Credentials for '${payload.name}' updated!`, 'success');

      // If active logged-in user edited their own credentials, update current session state
      if (AppState.currentUser && (AppState.currentUser.id === userId || AppState.currentUser.email === payload.email)) {
        Object.assign(AppState.currentUser, payload);
        sessionStorage.setItem('facultyflow_user', JSON.stringify(AppState.currentUser));
        updateUserUI();
      }

      await loadAdminPanel();
      await loadUsers();
    } else {
      alert((res && res.detail) ? res.detail : ((res && res.message) ? res.message : 'Error saving user.'));
    }
  } catch (err) {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Save to MongoDB';
    }
    alert(`Server Error: ${err}`);
  }
}

function openDeleteUserModal(userId) {
  const user = (AppState.adminUsers || []).find(u => u.id === userId);
  if (!user) return;

  if (AppState.currentUser && AppState.currentUser.id === userId) {
    alert('Security Notice: You cannot delete the account of the currently logged-in administrator.');
    return;
  }

  selectedDeleteUserId = userId;
  document.getElementById('delete-user-name-text').textContent = user.name;
  document.getElementById('delete-user-role-text').textContent = (user.role || 'User').toUpperCase();
  document.getElementById('delete-user-modal-backdrop').classList.add('active');
}

async function confirmDeleteUserAction() {
  if (!selectedDeleteUserId) return;
  const btn = document.getElementById('confirm-delete-user-btn');
  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Deleting...';
  }

  try {
    const res = await apiCall(`/api/admin/users/${selectedDeleteUserId}`, 'DELETE');
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Delete User';
    }

    if (res && res.success) {
      closeModal('delete-user-modal-backdrop');
      showAdminToast('User deleted successfully.', 'success');
      selectedDeleteUserId = null;
      await loadAdminPanel();
      await loadUsers();
    } else {
      alert((res && res.detail) ? res.detail : 'Failed to delete user.');
    }
  } catch (err) {
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Delete User';
    }
    alert(`Error: ${err}`);
  }
}

function togglePasswordPeek(spanId, actualPassword) {
  const el = document.getElementById(spanId);
  if (!el) return;
  if (el.textContent === '••••••••') {
    el.textContent = actualPassword;
    el.style.color = '#2563eb';
    el.style.fontWeight = '700';
  } else {
    el.textContent = '••••••••';
    el.style.color = 'var(--text-muted)';
    el.style.fontWeight = 'normal';
  }
}

function showAdminToast(message, type = 'success') {
  const existing = document.getElementById('admin-toast-el');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.id = 'admin-toast-el';
  toast.className = `admin-toast ${type === 'error' ? 'toast-error' : 'toast-success'}`;
  toast.innerHTML = `
    <svg width="18" height="18" fill="none" stroke="${type === 'error' ? '#ef4444' : '#10b981'}" stroke-width="2.5" viewBox="0 0 24 24">
      ${type === 'error' ? '<path d="M6 18L18 6M6 6l12 12"/>' : '<path d="M5 13l4 4L19 7"/>'}
    </svg>
    <span>${escapeHtml(message)}</span>
  `;
  document.body.appendChild(toast);
  setTimeout(() => {
    if (toast && toast.parentNode) toast.remove();
  }, 3800);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// --- Modals & Utilities ---
function openLeaveModal(id) {
  const modal = document.getElementById('leave-details-modal-backdrop');
  const content = document.getElementById('leave-modal-content');
  if (!modal || !content) return;

  content.innerHTML = `
    <h3 style="font-size:17px; font-weight:800; margin-bottom:12px;">Leave Details #${id}</h3>
    <div style="font-size:13px; color:var(--text-body); line-height:1.6;">
      <p><strong>Faculty:</strong> Dr. Ananya (CSE-AIML)</p>
      <p><strong>Leave Type:</strong> Casual Leave (CL)</p>
      <p><strong>Dates:</strong> 21 Sep 2026 - 21 Sep 2026</p>
      <p><strong>Status:</strong> Waiting for Slot (#2 in queue)</p>
      <p><strong>Reason:</strong> Personal work</p>
    </div>
    <div style="margin-top:18px; text-align:right;">
      <button class="btn btn-primary" onclick="closeModal('leave-details-modal-backdrop')">Close</button>
    </div>
  `;
  modal.classList.add('active');
}

function closeModal(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.remove('active');
}

function togglePasswordVisibility(inputId) {
  const input = document.getElementById(inputId);
  if (input) {
    input.type = input.type === 'password' ? 'text' : 'password';
  }
}

function handleUserCardClick() {
  switchView('view-leave-balance');
}

function handleAddFacultySubmit(e) {
  e.preventDefault();
  handleSaveUserSubmit(e);
}
