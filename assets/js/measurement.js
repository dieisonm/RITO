(function () {
  const UTM_KEYS = [
    "utm_id",
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_source_platform",
    "utm_content",
    "utm_term",
    "utm_creative_format",
    "utm_marketing_tactic",
  ];
  const CLICK_ID_KEYS = ["gclid", "gbraid", "wbraid", "fbclid", "msclkid", "li_fat_id", "ttclid"];
  const ATTRIBUTION_KEYS = [...UTM_KEYS, ...CLICK_ID_KEYS];
  const STORAGE_KEY = "rito_attribution";
  const STORAGE_TTL_MS = 90 * 24 * 60 * 60 * 1000;
  const DEFAULT_CONFIG = {
    gaMeasurementId: "G-ZTLGY2QWVR",
    metaPixelId: "",
  };

  window.dataLayer = window.dataLayer || [];

  function cleanValue(value, limit) {
    return String(value || "").trim().slice(0, limit);
  }

  function readRuntimeConfig() {
    const rawConfig =
      window.RITO_MEASUREMENT_CONFIG && typeof window.RITO_MEASUREMENT_CONFIG === "object"
        ? window.RITO_MEASUREMENT_CONFIG
        : {};

    return {
      gaMeasurementId: cleanValue(
        rawConfig.gaMeasurementId || DEFAULT_CONFIG.gaMeasurementId,
        40
      ),
      metaPixelId: cleanValue(rawConfig.metaPixelId || DEFAULT_CONFIG.metaPixelId, 40),
    };
  }

  const runtimeConfig = readRuntimeConfig();
  const GA_MEASUREMENT_ID = runtimeConfig.gaMeasurementId;
  const META_PIXEL_ID = runtimeConfig.metaPixelId;

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

  function installMetaPixel() {
    if (!META_PIXEL_ID) {
      return;
    }

    if (!window.fbq) {
      const fbq = function () {
        if (fbq.callMethod) {
          fbq.callMethod.apply(fbq, arguments);
        } else {
          fbq.queue.push(arguments);
        }
      };

      fbq.queue = [];
      fbq.loaded = true;
      fbq.version = "2.0";
      window.fbq = fbq;

      if (!window._fbq) {
        window._fbq = fbq;
      }
    }

    if (!document.querySelector(`script[data-rito-meta-pixel="${META_PIXEL_ID}"]`)) {
      const script = document.createElement("script");
      script.async = true;
      script.src = "https://connect.facebook.net/en_US/fbevents.js";
      script.dataset.ritoMetaPixel = META_PIXEL_ID;
      document.head.appendChild(script);
    }

    if (window.fbq.__ritoPixelId !== META_PIXEL_ID) {
      window.fbq("init", META_PIXEL_ID);
      window.fbq.__ritoPixelId = META_PIXEL_ID;
    }
  }

  function readStoredAttribution() {
    const now = Date.now();

    try {
      const stored = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "{}") || {};

      if (stored.expires_at && stored.expires_at < now) {
        window.localStorage.removeItem(STORAGE_KEY);
      } else if (stored.values) {
        return stored.values || {};
      } else if (Object.keys(stored).length > 0) {
        return stored;
      }
    } catch (error) {
      // localStorage can be blocked; fall back to sessionStorage below.
    }

    try {
      return JSON.parse(window.sessionStorage.getItem(STORAGE_KEY) || "{}") || {};
    } catch (error) {
      return {};
    }
  }

  function writeStoredAttribution(attribution) {
    const stored = {
      values: attribution,
      updated_at: Date.now(),
      expires_at: Date.now() + STORAGE_TTL_MS,
    };

    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(stored));
    } catch (error) {
      // Some browsers block localStorage; tracking should never break the page.
    }

    try {
      window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(attribution));
    } catch (error) {
      // Some browsers block sessionStorage; tracking should never break the page.
    }
  }

  function readCookie(name) {
    const escapedName = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const match = document.cookie.match(new RegExp(`(?:^|; )${escapedName}=([^;]*)`));
    return match ? decodeURIComponent(match[1]) : "";
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

    if (!attribution.first_landing_page) {
      attribution.first_landing_page = stored.first_landing_page || stored.landing_page || current.landing_page;
    }

    if (!attribution.first_referrer && (stored.first_referrer || stored.referrer || current.referrer)) {
      attribution.first_referrer = stored.first_referrer || stored.referrer || current.referrer;
    }

    ATTRIBUTION_KEYS.forEach((key) => {
      const firstKey = `first_${key}`;

      if (!attribution[firstKey] && (stored[firstKey] || stored[key] || current[key])) {
        attribution[firstKey] = stored[firstKey] || stored[key] || current[key];
      }
    });

    writeStoredAttribution(attribution);
    return attribution;
  }

  const attribution = currentAttribution();

  installGoogleAnalytics();
  installMetaPixel();

  function gaEventName(eventName) {
    if (eventName === "rito_page_view") {
      return "page_view";
    }

    if (eventName === "generate_lead_form") {
      return "generate_lead";
    }

    return eventName;
  }

  function metaEventName(eventName) {
    if (eventName === "rito_page_view") {
      return "PageView";
    }

    if (eventName === "generate_lead_form") {
      return "Lead";
    }

    return "";
  }

  function metaCustomEventName(eventName) {
    if (eventName === "click_whatsapp") {
      return "RitoClickWhatsApp";
    }

    if (eventName === "click_email") {
      return "RitoClickEmail";
    }

    if (eventName === "click_instagram") {
      return "RitoClickInstagram";
    }

    if (eventName === "click_pilot_landing") {
      return "RitoClickPilotLanding";
    }

    return `Rito${eventName
      .split("_")
      .filter(Boolean)
      .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
      .join("")}`;
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

  function sendToMetaPixel(eventName, eventPayload) {
    if (typeof window.fbq !== "function" || !META_PIXEL_ID) {
      return;
    }

    const { event, event_id, ...params } = eventPayload;
    const metaParams = {
      page_path: window.location.pathname,
      page_title: document.title,
      page_location: window.location.href,
      ...params,
    };

    const mappedEventName = metaEventName(eventName);

    if (mappedEventName) {
      window.fbq("track", mappedEventName, metaParams, {
        eventID: event_id,
      });
      return;
    }

    window.fbq("trackCustom", metaCustomEventName(eventName), metaParams, {
      eventID: event_id,
    });
  }

  function createEventId(eventName) {
    return `${eventName}_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
  }

  function currentMetaClickId() {
    const existingFbc = cleanValue(readCookie("_fbc"), 240);

    if (existingFbc) {
      return existingFbc;
    }

    const fbclid = cleanValue(attribution.fbclid || attribution.first_fbclid || "", 200);

    if (!fbclid) {
      return "";
    }

    return `fb.1.${Date.now()}.${fbclid}`;
  }

  function pushEvent(eventName, payload) {
    const eventPayload = {
      event: eventName,
      event_id: createEventId(eventName),
      page_path: window.location.pathname,
      page_title: document.title,
      ...attribution,
      ...(payload || {}),
    };

    window.dataLayer.push(eventPayload);
    sendToGoogleAnalytics(eventName, eventPayload);
    sendToMetaPixel(eventName, eventPayload);
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
      setHiddenValue(form, "first_landing_page", attribution.first_landing_page);
      setHiddenValue(form, "first_referrer", attribution.first_referrer);
      setHiddenValue(form, "meta_fbp", cleanValue(readCookie("_fbp"), 240));
      setHiddenValue(form, "meta_fbc", currentMetaClickId());

      ATTRIBUTION_KEYS.forEach((key) => {
        setHiddenValue(form, `first_${key}`, attribution[`first_${key}`]);
      });
    });
  }

  function linkLabel(link) {
    return cleanValue(link.textContent || link.getAttribute("aria-label") || "", 120);
  }

  window.ritoTrack = pushEvent;
  window.ritoRefreshTrackingFields = enrichForms;

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
