/* Pamplin AI Agent Recipes — clipboard + analytics
 *
 * Inherits the workshop platform's submitToGoogleForm pattern.
 * No localStorage; sessionStorage only for the per-tab session ID.
 * No external dependencies.
 */
(function () {
  'use strict';

  var CONFIG = window.__SITE_CONFIG__ || {};
  var SESSION_KEY = 'pamplin_recipes_session_id';

  // ---------- session id ----------
  function uuidV4() {
    if (window.crypto && typeof window.crypto.randomUUID === 'function') {
      return window.crypto.randomUUID();
    }
    // RFC 4122 v4 fallback
    var bytes = new Uint8Array(16);
    if (window.crypto && window.crypto.getRandomValues) {
      window.crypto.getRandomValues(bytes);
    } else {
      for (var i = 0; i < 16; i++) bytes[i] = Math.floor(Math.random() * 256);
    }
    bytes[6] = (bytes[6] & 0x0f) | 0x40;
    bytes[8] = (bytes[8] & 0x3f) | 0x80;
    var hex = [];
    for (var j = 0; j < bytes.length; j++) {
      hex.push(('00' + bytes[j].toString(16)).slice(-2));
    }
    return hex.slice(0, 4).join('') + '-' +
           hex.slice(4, 6).join('') + '-' +
           hex.slice(6, 8).join('') + '-' +
           hex.slice(8, 10).join('') + '-' +
           hex.slice(10, 16).join('');
  }

  function getSessionId() {
    try {
      var existing = sessionStorage.getItem(SESSION_KEY);
      if (existing) return existing;
      var fresh = uuidV4();
      sessionStorage.setItem(SESSION_KEY, fresh);
      return fresh;
    } catch (e) {
      // sessionStorage blocked (e.g., private mode in some browsers); fall back to in-memory
      return uuidV4();
    }
  }

  // ---------- analytics ----------
  function submitToGoogleForm(eventType, payload) {
    if (!CONFIG.formSubmissionUrl) return;
    var url = CONFIG.formSubmissionUrl;
    var formData = new FormData();
    formData.append(CONFIG.entryEventType, eventType);
    formData.append(CONFIG.entrySessionId, getSessionId());
    formData.append(CONFIG.entryTimestamp, new Date().toISOString());
    formData.append(CONFIG.entryPayload, JSON.stringify(payload || {}));

    // no-cors fire-and-forget
    fetch(url, { method: 'POST', mode: 'no-cors', body: formData })
      .catch(function (err) {
        // Analytics failures must not surface to user; log only.
        if (window.console && console.log) {
          console.log('analytics submit failed:', err && err.message);
        }
      });
  }

  function firePageView() {
    var pageType = CONFIG.pageType || 'unknown';
    submitToGoogleForm('page_view', {
      page_type: pageType,
      recipe_id: CONFIG.recipeId || null
    });
  }

  // ---------- clipboard ----------
  function fallbackCopyText(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'absolute';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }

  function copyText(text) {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      return navigator.clipboard.writeText(text).then(
        function () { return true; },
        function () { return fallbackCopyText(text); }
      );
    }
    return Promise.resolve(fallbackCopyText(text));
  }

  function announce(message) {
    var el = document.getElementById('copy-announcement');
    if (!el) return;
    // Reset to retrigger the live region.
    el.textContent = '';
    setTimeout(function () { el.textContent = message; }, 30);
  }

  function setSuccessState(button) {
    var original = button.dataset.originalLabel;
    if (!original) {
      original = button.textContent;
      button.dataset.originalLabel = original;
    }
    button.dataset.state = 'success';
    button.textContent = 'Copied';
    setTimeout(function () {
      if (button.dataset.state === 'success') {
        button.dataset.state = '';
        button.textContent = original;
      }
    }, 2000);
  }

  function bindCopyButtons() {
    var buttons = document.querySelectorAll('.plib-copy-btn[data-copy-target]');
    for (var i = 0; i < buttons.length; i++) {
      (function (btn) {
        btn.addEventListener('click', function () {
          var target = document.querySelector(btn.dataset.copyTarget);
          if (!target) return;
          var text = target.textContent;
          Promise.resolve(copyText(text)).then(function (ok) {
            if (ok !== false) {
              setSuccessState(btn);
              announce('Copied');
              submitToGoogleForm('field_copied', {
                recipe_id: btn.dataset.recipeId || null,
                field_name: btn.dataset.fieldName || null
              });
            } else {
              announce('Copy failed');
              if (window.console && console.log) {
                console.log('copy failed; clipboard unavailable');
              }
            }
          });
        });
      })(buttons[i]);
    }
  }

  // ---------- boot ----------
  function ready(fn) {
    if (document.readyState !== 'loading') { fn(); return; }
    document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    bindCopyButtons();
    firePageView();
  });
})();
