(() => {
  const tabs = [...document.querySelectorAll('[data-tab]')];
  const panels = [...document.querySelectorAll('[data-purpose]')];
  const tablist = document.querySelector('.purpose-tabs');
  if (!tablist || tabs.length !== panels.length) return;

  function hashTarget() {
    try {
      return document.getElementById(decodeURIComponent(location.hash.slice(1)));
    } catch {
      return null;
    }
  }

  function select(purpose, {write = false, focus = false} = {}) {
    const active = tabs.find(tab => tab.dataset.tab === purpose) || tabs[0];
    for (const tab of tabs) {
      const selected = tab === active;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
    }
    for (const panel of panels) panel.hidden = panel.dataset.purpose !== active.dataset.tab;
    if (write) {
      const url = new URL(location.href);
      url.searchParams.set('purpose', active.dataset.tab);
      url.hash = '';
      history.pushState(null, '', url);
    }
    if (focus) active.focus();
  }

  function restore() {
    const target = hashTarget();
    const purpose = target?.closest('[data-purpose]')?.dataset.purpose
      || new URL(location.href).searchParams.get('purpose') || 'mac';
    select(purpose);
    if (target) requestAnimationFrame(() => target.scrollIntoView());
  }

  tablist.setAttribute('role', 'tablist');
  for (const panel of panels) panel.setAttribute('role', 'tabpanel');
  for (const tab of tabs) {
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', `purpose-${tab.dataset.tab}`);
    tab.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
      event.preventDefault();
      select(tab.dataset.tab, {write: true, focus: true});
    });
    tab.addEventListener('keydown', event => {
      const index = tabs.indexOf(tab);
      let next;
      if (event.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
      if (event.key === 'ArrowLeft') next = tabs[(index + tabs.length - 1) % tabs.length];
      if (event.key === 'Home') next = tabs[0];
      if (event.key === 'End') next = tabs[tabs.length - 1];
      if (!next) return;
      event.preventDefault();
      select(next.dataset.tab, {write: true, focus: true});
    });
  }
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href^="#"]');
    if (!anchor || anchor.dataset.tab || event.defaultPrevented || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
    let target;
    try { target = document.getElementById(decodeURIComponent(anchor.hash.slice(1))); } catch { return; }
    const panel = target?.closest('[data-purpose]');
    if (panel) select(panel.dataset.purpose);
  });
  addEventListener('popstate', restore);
  addEventListener('hashchange', restore);
  restore();
})();
