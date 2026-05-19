(function () {
  const GA_MEASUREMENT_ID = "G-ZTLGY2QWVR";
  const UTM_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"];
  const CLICK_ID_KEYS = ["gclid", "gbraid", "wbraid", "fbclid", "msclkid"];
  const ATTRIBUTION_KEYS = [...UTM_KEYS, ...CLICK_ID_KEYS];
  const STORAGE_KEY = "rito_attribution";

  window.dataLayer = window.dataLayer || [];

  function installGoogleAnalytics() {
    if (!GA_MEASUREMENT_ID) {
      return;
    }

    window.gtag =
      window.gtag ||
      function () {
        window.dataLayer.push(arguments);
      };

    window.gtag("js", new Date());
    window.gtag("config", GA_MEASUREMENT_ID, {
      send_page_view: false,
    });

    if (document.querySelector(`script[data-rito-ga4="${GA_MEASUREMENT_ID}"]`)) {
      return;
    }

    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(
      GA_MEASUREMENT_ID
    )}`;
    script.dataset.ritoGa4 = GA_MEASUREMENT_ID;
    document.head.appendChild(script);
  }

  function readStoredAttribution() {
    try {
      return JSON.parse(window.sessionStorage.getItem(STORAGE_KEY) || "{}") || {};
    } catch (error) {
      return {};
    }
  }

  function writeStoredAttribution(attribution) {
    try {
      window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(attribution));
    } catch (error) {
      // Some browsers block sessionStorage; tracking should never break the page.
    }
  }

  function cleanValue(value, limit) {
    return String(value || "").trim().slice(0, limit);
  }

  function currentAttribution() {
    const params = new URLSearchParams(window.location.search);
    const stored = readStoredAttribution();
    const current = {};
    const hasCampaignParams = ATTRIBUTION_KEYS.some((key) => params.has(key));

    ATTRIBUTION_KEYS.forEach((key) => {
      const value = params.get(key);

      if (value) {
        current[key] = cleanValue(value, 180);
      }
    });

    if (document.referrer) {
      current.referrer = cleanValue(document.referrer, 400);
    }

    current.landing_page = cleanValue(
      `${window.location.pathname}${window.location.search}`,
      400
    );

    const attribution =
      hasCampaignParams || !stored.landing_page
        ? { ...stored, ...current }
        : { ...current, ...stored };

    writeStoredAttribution(attribution);
    return attribution;
  }

  const attribution = currentAttribution();

  installGoogleAnalytics();

  function gaEventName(eventName) {
    if (eventName === "rito_page_view") {
      return "page_view";
    }

    return eventName;
  }

  function sendToGoogleAnalytics(eventName, eventPayload) {
    if (typeof window.gtag !== "function") {
      return;
    }

    const { event, ...params } = eventPayload;

    window.gtag("event", gaEventName(eventName), {
      event_category: "rito_site",
      page_location: window.location.href,
      ...params,
    });
  }

  function pushEvent(eventName, payload) {
    const eventPayload = {
      event: eventName,
      page_path: window.location.pathname,
      page_title: document.title,
      ...attribution,
      ...(payload || {}),
    };

    window.dataLayer.push(eventPayload);
    sendToGoogleAnalytics(eventName, eventPayload);
    return eventPayload;
  }

  function setHiddenValue(form, name, value) {
    if (!form || value === undefined || value === null || value === "") {
      return;
    }

    let field = form.querySelector(`input[name="${name}"]`);

    if (!field) {
      field = document.createElement("input");
      field.type = "hidden";
      field.name = name;
      form.appendChild(field);
    }

    if (!field.value) {
      field.value = value;
    }
  }

  function enrichForms() {
    document.querySelectorAll('form[method="post"], form:not([method])').forEach((form) => {
      ATTRIBUTION_KEYS.forEach((key) => {
        setHiddenValue(form, key, attribution[key]);
      });

      setHiddenValue(form, "landing_page", attribution.landing_page);
      setHiddenValue(form, "referrer", attribution.referrer);
    });
  }

  function linkLabel(link) {
    return cleanValue(link.textContent || link.getAttribute("aria-label") || "", 120);
  }

  window.ritoTrack = pushEvent;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enrichForms);
  } else {
    enrichForms();
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest ? event.target.closest("a[href]") : null;

    if (!link) {
      return;
    }

    const href = link.getAttribute("href") || "";
    const trackingPayload = {
      link_url: href,
      link_text: linkLabel(link),
    };

    if (href.includes("wa.me/") || href.includes("api.whatsapp.com")) {
      pushEvent("click_whatsapp", trackingPayload);
    } else if (href.startsWith("mailto:")) {
      pushEvent("click_email", trackingPayload);
    } else if (href.includes("instagram.com")) {
      pushEvent("click_instagram", trackingPayload);
    } else if (href.includes("projeto-piloto.html")) {
      pushEvent("click_pilot_landing", trackingPayload);
    }
  });

  pushEvent("rito_page_view");
})();
