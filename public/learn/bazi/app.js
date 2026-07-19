(() => {
  'use strict';

  const buildId = 'BZG-35-draft-2026-07-19';
  window.dataLayer = window.dataLayer || [];

  const emit = (eventName, detail = {}) => {
    const payload = {
      event: eventName,
      page_type: 'foundation_cornerstone',
      page_topic: 'bazi',
      build_id: buildId,
      ...detail
    };
    window.dataLayer.push(payload);
    window.dispatchEvent(new CustomEvent('sizhu:analytics', { detail: payload }));
  };

  document.querySelectorAll('[data-event]').forEach((element) => {
    element.addEventListener('click', () => {
      emit(element.dataset.event, {
        destination: element.dataset.destination || '',
        link_url: element.href || ''
      });
    });
  });

  const pillarContent = {
    year: {
      label: 'Year Pillar · 年柱 · niánzhù',
      text: 'The stem-branch pair assigned to the chart’s year under the selected year-boundary convention. Traditional readings often connect it with broader background or inherited and social context.'
    },
    month: {
      label: 'Month Pillar · 月柱 · yuèzhù',
      text: 'The pair assigned through the selected solar-term and month method. In many Zi Ping approaches, the Month Branch and seasonal context carry substantial structural weight.'
    },
    day: {
      label: 'Day Pillar · 日柱 · rìzhù',
      text: 'The pair assigned to the day. Its Heavenly Stem is the Day Master — the main relational reference point in many traditional readings, not a complete personality label.'
    },
    hour: {
      label: 'Hour Pillar · 时柱 · shízhù',
      text: 'The pair assigned to a traditional two-hour period under the selected time convention. If birth time is unknown or close to a boundary, the Hour Pillar should be marked uncertain.'
    }
  };

  const pillarTabs = Array.from(document.querySelectorAll('[data-pillar]'));
  const pillarPanel = document.getElementById('pillar-explanation');

  const activatePillar = (button) => {
    const key = button.dataset.pillar;
    const content = pillarContent[key];
    if (!content || !pillarPanel) return;

    pillarTabs.forEach((tab) => {
      const active = tab === button;
      tab.classList.toggle('is-active', active);
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
    });

    pillarPanel.innerHTML = `
      <p class="pillar-explanation-label">${content.label}</p>
      <p>${content.text}</p>
    `;

    emit('diagram_interaction', { diagram: 'four-pillars', item: key });
  };

  pillarTabs.forEach((button, index) => {
    button.addEventListener('click', () => activatePillar(button));
    button.addEventListener('keydown', (event) => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      let nextIndex = index;
      if (event.key === 'ArrowLeft') nextIndex = (index - 1 + pillarTabs.length) % pillarTabs.length;
      if (event.key === 'ArrowRight') nextIndex = (index + 1) % pillarTabs.length;
      if (event.key === 'Home') nextIndex = 0;
      if (event.key === 'End') nextIndex = pillarTabs.length - 1;
      pillarTabs[nextIndex].focus();
      activatePillar(pillarTabs[nextIndex]);
    });
  });

  document.querySelectorAll('.phase-node').forEach((node) => {
    const interact = () => emit('diagram_interaction', {
      diagram: 'wu-xing',
      item: node.getAttribute('aria-label') || ''
    });
    node.addEventListener('click', interact);
    node.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        interact();
      }
    });
  });

  document.querySelectorAll('details').forEach((detail, index) => {
    detail.addEventListener('toggle', () => {
      if (detail.open) emit('diagram_interaction', { diagram: 'misconception-accordion', item: index + 1 });
    });
  });

  const sectionLinks = new Map();
  document.querySelectorAll('.contents-panel a[href^="#"]').forEach((link) => {
    sectionLinks.set(link.getAttribute('href').slice(1), link);
  });

  const seenSections = new Set();
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const id = entry.target.id || entry.target.dataset.trackSection;
        if (entry.isIntersecting && id) {
          sectionLinks.forEach((link, key) => link.classList.toggle('is-current', key === id));
          if (!seenSections.has(id)) {
            seenSections.add(id);
            emit('section_view', { section_id: id });
          }
        }
      });
    }, { rootMargin: '-20% 0px -65% 0px', threshold: 0.01 });

    document.querySelectorAll('[data-track-section], .reading-column section[id]').forEach((section) => observer.observe(section));
  }

  const scrollDepthEvents = {
    25: 'scroll_depth_25',
    50: 'scroll_depth_50',
    75: 'scroll_depth_75',
    100: 'scroll_depth_100'
  };
  const depths = Object.keys(scrollDepthEvents).map(Number);
  const sentDepths = new Set();
  const trackScrollDepth = () => {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    if (scrollable <= 0) return;
    const percent = Math.min(100, Math.round((window.scrollY / scrollable) * 100));
    depths.forEach((depth) => {
      if (percent >= depth && !sentDepths.has(depth)) {
        sentDepths.add(depth);
        emit(scrollDepthEvents[depth], { percent_scrolled: depth });
      }
    });
  };
  window.addEventListener('scroll', trackScrollDepth, { passive: true });
  trackScrollDepth();

  emit('learn_hub_click', { destination: 'page_loaded', interaction_type: 'page_view' });
})();
