const yearNode = document.getElementById("year");
const topbar = document.querySelector(".topbar");
const navToggle = document.querySelector(".nav-toggle");
const navigation = document.getElementById("site-nav");
const mobileNavigationQuery = window.matchMedia("(max-width: 900px)");

if (yearNode) {
  yearNode.textContent = new Date().getFullYear();
}

function closeMobileNavigation() {
  if (!topbar || !navToggle) {
    return;
  }

  topbar.classList.remove("is-menu-open");
  navToggle.setAttribute("aria-expanded", "false");
  navToggle.setAttribute("aria-label", "Abrir navegação principal");
}

function openMobileNavigation() {
  if (!topbar || !navToggle) {
    return;
  }

  topbar.classList.add("is-menu-open");
  navToggle.setAttribute("aria-expanded", "true");
  navToggle.setAttribute("aria-label", "Fechar navegação principal");
}

if (topbar && navToggle && navigation) {
  navToggle.addEventListener("click", () => {
    const isOpen = topbar.classList.contains("is-menu-open");

    if (isOpen) {
      closeMobileNavigation();
      return;
    }

    openMobileNavigation();
  });

  navigation.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      if (mobileNavigationQuery.matches) {
        closeMobileNavigation();
      }
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeMobileNavigation();
    }
  });

  const syncNavigationLayout = (event) => {
    if (!event.matches) {
      closeMobileNavigation();
    }
  };

  syncNavigationLayout(mobileNavigationQuery);

  if (typeof mobileNavigationQuery.addEventListener === "function") {
    mobileNavigationQuery.addEventListener("change", syncNavigationLayout);
  } else if (typeof mobileNavigationQuery.addListener === "function") {
    mobileNavigationQuery.addListener(syncNavigationLayout);
  }
}

const contactForm = document.getElementById("quote-form");
const contactStatus = document.getElementById("contact-status");
const phoneField = contactForm ? contactForm.querySelector('input[name="whatsapp"]') : null;
const emailField = contactForm ? contactForm.querySelector('input[name="email"]') : null;
const solutionTypeField = contactForm ? contactForm.querySelector('select[name="solution_type"]') : null;
const casePermissionField = contactForm ? contactForm.querySelector('input[name="case_permission"]') : null;
const preferredContactFields = contactForm
  ? Array.from(contactForm.querySelectorAll('input[name="preferred_contact"]'))
  : [];

function setContactStatus(type, message) {
  if (!contactStatus) {
    return;
  }

  contactStatus.textContent = message;
  contactStatus.className = `form-status is-visible is-${type}`;
}

function clearContactStatus() {
  if (!contactStatus) {
    return;
  }

  contactStatus.textContent = "";
  contactStatus.className = "form-status";
}

function digitsOnly(value) {
  return value.replace(/\D/g, "").slice(0, 11);
}

function formatPhoneNumber(value) {
  const digits = digitsOnly(value);

  if (digits.length <= 2) {
    return digits;
  }

  if (digits.length <= 6) {
    return `${digits.slice(0, 2)} ${digits.slice(2)}`;
  }

  if (digits.length <= 10) {
    return `${digits.slice(0, 2)} ${digits.slice(2, 6)} ${digits.slice(6)}`;
  }

  return `${digits.slice(0, 2)} ${digits.slice(2, 7)} ${digits.slice(7)}`;
}

function selectedPreferredContact() {
  const checkedField = preferredContactFields.find((field) => field.checked);
  return checkedField ? checkedField.value : "whatsapp";
}

function setFieldError(field, message) {
  const fieldGroup = field.closest(".field-group");
  const errorNode = fieldGroup ? fieldGroup.querySelector(".field-error") : null;

  field.setCustomValidity(message);

  if (fieldGroup) {
    fieldGroup.classList.toggle("is-invalid", Boolean(message));
  }

  if (errorNode) {
    errorNode.textContent = message;
  }
}

function validateField(field) {
  const value = field.value.trim();
  const name = field.name;
  let errorMessage = "";

  if (name === "name" && value === "") {
    errorMessage = "Informe seu nome para continuarmos.";
  }

  if (name === "business" && value === "") {
    errorMessage = "Informe o nome da empresa ou atividade.";
  }

  if (name === "message" && value === "") {
    errorMessage = "Descreva o problema ou a necessidade que você quer resolver.";
  }

  if (name === "whatsapp") {
    const digits = digitsOnly(value);

    if (digits.length === 0) {
      errorMessage = "Informe um telefone ou WhatsApp para retorno.";
    } else if (digits.length < 10) {
      errorMessage = "Informe o telefone completo com DDD.";
    }
  }

  if (name === "email") {
    if (value !== "" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      errorMessage = "Informe um e-mail válido ou deixe este campo em branco.";
    } else if (selectedPreferredContact() === "email" && value === "") {
      errorMessage = "Se preferir retorno por e-mail, preencha um e-mail válido.";
    }
  }

  if (name === "solution_type" && field.hasAttribute("required") && value === "") {
    errorMessage = "Selecione o tipo de solução que parece fazer mais sentido.";
  }

  if (name === "case_permission" && field.hasAttribute("required") && !field.checked) {
    errorMessage = "Confirme a condição do projeto piloto para continuar.";
  }

  setFieldError(field, errorMessage);
  return errorMessage === "";
}

function validateContactForm() {
  if (!contactForm) {
    return true;
  }

  const fieldsToValidate = Array.from(
    contactForm.querySelectorAll('input[name="name"], input[name="business"], input[name="email"], input[name="whatsapp"], select[name="solution_type"], input[name="case_permission"], textarea[name="message"]')
  );

  const results = fieldsToValidate.map(validateField);
  return results.every(Boolean);
}

if (contactStatus) {
  const params = new URLSearchParams(window.location.search);
  const status = params.get("status");

  if (status === "success") {
    setContactStatus("success", "Recebemos a sua solicitação. A RITO entrará em contato em breve.");
  }

  if (status === "error") {
    setContactStatus(
      "error",
      "Não conseguimos enviar sua solicitação agora. Tente novamente em instantes ou use o envio por e-mail."
    );
  }

  if (status) {
    params.delete("status");
    const query = params.toString();
    const nextUrl = `${window.location.pathname}${query ? `?${query}` : ""}${window.location.hash}`;
    window.history.replaceState({}, "", nextUrl);
  }
}

if (contactForm) {
  const submitButton = contactForm.querySelector('button[type="submit"]');
  const defaultButtonLabel = submitButton ? submitButton.textContent : "";
  const fields = Array.from(
    contactForm.querySelectorAll('input[name="name"], input[name="business"], input[name="email"], input[name="whatsapp"], select[name="solution_type"], input[name="case_permission"], textarea[name="message"]')
  );

  if (phoneField) {
    phoneField.addEventListener("input", () => {
      phoneField.value = formatPhoneNumber(phoneField.value);
      validateField(phoneField);
    });
  }

  fields.forEach((field) => {
    field.addEventListener("input", () => {
      validateField(field);
    });

    field.addEventListener("blur", () => {
      validateField(field);
    });
  });

  preferredContactFields.forEach((field) => {
    field.addEventListener("change", () => {
      if (emailField) {
        validateField(emailField);
      }
    });
  });

  if (solutionTypeField) {
    solutionTypeField.addEventListener("change", () => {
      validateField(solutionTypeField);
    });
  }

  if (casePermissionField) {
    casePermissionField.addEventListener("change", () => {
      validateField(casePermissionField);
    });
  }

  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearContactStatus();

    if (!validateContactForm()) {
      const firstInvalidField = contactForm.querySelector(
        ".field-group.is-invalid input, .field-group.is-invalid select, .field-group.is-invalid textarea"
      );

      if (firstInvalidField) {
        firstInvalidField.focus();
      }

      return;
    }

    if (!window.fetch) {
      contactForm.submit();
      return;
    }

    const formData = new FormData(contactForm);

    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Enviando...";
    }

    try {
      const response = await fetch(contactForm.action, {
        method: "POST",
        body: formData,
        headers: {
          Accept: "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      const result = await response.json().catch(() => ({}));

      if (!response.ok || !result.ok) {
        throw new Error(
          result.message ||
            "Não conseguimos enviar sua solicitação agora. Tente novamente em instantes."
        );
      }

      if (typeof window.ritoTrack === "function") {
        window.ritoTrack("generate_lead_form", {
          form_id: contactForm.id || "",
          campaign: formData.get("campaign") || formData.get("utm_campaign") || "",
          lead_source: formData.get("lead_source") || "",
          preferred_contact: formData.get("preferred_contact") || "",
          solution_type: formData.get("solution_type") || "",
        });
      }

      contactForm.reset();
      fields.forEach((field) => setFieldError(field, ""));
      setContactStatus(
        "success",
        result.message || "Recebemos a sua solicitação. A RITO entrará em contato em breve."
      );
    } catch (error) {
      setContactStatus(
        "error",
        error instanceof Error
          ? error.message
          : "Não conseguimos enviar sua solicitação agora. Tente novamente em instantes."
      );
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = defaultButtonLabel;
      }
    }
  });
}
