#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import readline from "node:readline/promises";
import { stdin as input, stdout as output, exit } from "node:process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DEFAULT_PROFILE_DIR = path.join(__dirname, ".auth", "rito-meta-profile");
const DEFAULT_SLOW_MO_MS = 120;
const DEFAULT_TIMEOUT_MS = 30000;
const DEFAULT_PACING = {
  afterComposerLoadMs: 1200,
  afterMediaClearMs: 500,
  afterMediaUploadMs: 1500,
  afterScheduleToggleMs: 400,
  afterDateSetMs: 400,
  afterTimeSetMs: 400,
  beforeScheduleClickMs: 1200,
  afterScheduleSuccessMs: 1000,
  betweenStoriesMs: 2000,
  stepPauseMs: 180,
};
const DATE_DISPLAY_FORMATTER = new Intl.DateTimeFormat("en-US", {
  month: "long",
  day: "numeric",
  year: "numeric",
  timeZone: "UTC",
});

const HELP_TEXT = `
Uso:
  node schedule_instagram_stories.mjs auth --config <arquivo.json>
  node schedule_instagram_stories.mjs validate --config <arquivo.json>
  node schedule_instagram_stories.mjs schedule --config <arquivo.json> [--limit N] [--dry-run] [--continue-on-error] [--headless true|false]

Comandos:
  auth       Abre o Meta com perfil persistente para login inicial.
  validate   Valida o plano e os caminhos das imagens sem abrir o navegador.
  schedule   Agenda os stories descritos no plano.

Flags:
  --config <path>             Caminho do plano JSON.
  --limit <n>                 Agenda apenas os primeiros N stories.
  --dry-run                   Mostra o plano resolvido e encerra.
  --continue-on-error         Continua para o proximo story em caso de falha.
  --headless true|false       Sobrescreve o modo headless do arquivo JSON.
  --help                      Mostra esta ajuda.
`.trim();

async function main() {
  const { command, options } = parseCli(process.argv.slice(2));

  if (!command || options.help) {
    console.log(HELP_TEXT);
    return;
  }

  if (!["auth", "validate", "schedule"].includes(command)) {
    throw new Error(`Comando invalido: ${command}`);
  }

  if (!options.config) {
    throw new Error("Use --config <arquivo.json>.");
  }

  const config = await loadPlanConfig(options.config);
  const selectedStories = applyStorySelection(config.stories, options.limit);
  validateDuplicateSlots(selectedStories);

  if (command === "validate" || options.dryRun) {
    await ensureStoryFilesExist(selectedStories);
    printResolvedPlan(config, selectedStories);
    return;
  }

  const playwright = await loadPlaywright();

  if (command === "auth") {
    await runAuthFlow(playwright, config, options);
    return;
  }

  await runScheduleFlow(playwright, config, selectedStories, options);
}

function parseCli(argv) {
  const options = {};
  const [command, ...rest] = argv;

  for (let index = 0; index < rest.length; index += 1) {
    const token = rest[index];

    if (token === "--help") {
      options.help = true;
      continue;
    }

    if (token === "--dry-run") {
      options.dryRun = true;
      continue;
    }

    if (token === "--continue-on-error") {
      options.continueOnError = true;
      continue;
    }

    if (token.startsWith("--")) {
      const next = rest[index + 1];
      if (next == null) {
        throw new Error(`Flag sem valor: ${token}`);
      }

      switch (token) {
        case "--config":
          options.config = next;
          break;
        case "--limit":
          options.limit = Number.parseInt(next, 10);
          if (!Number.isInteger(options.limit) || options.limit <= 0) {
            throw new Error("--limit precisa ser um inteiro maior que zero.");
          }
          break;
        case "--headless":
          options.headless = parseBoolean(next, "--headless");
          break;
        default:
          throw new Error(`Flag desconhecida: ${token}`);
      }

      index += 1;
      continue;
    }

    throw new Error(`Argumento inesperado: ${token}`);
  }

  return { command, options };
}

function parseBoolean(value, flagName) {
  if (value === "true") return true;
  if (value === "false") return false;
  throw new Error(`${flagName} aceita apenas true ou false.`);
}

async function loadPlanConfig(configPathInput) {
  const absoluteConfigPath = path.resolve(configPathInput);
  const raw = JSON.parse(await fs.readFile(absoluteConfigPath, "utf8"));
  const configDir = path.dirname(absoluteConfigPath);

  if (!raw.businessId || !raw.assetId) {
    throw new Error("O plano precisa conter businessId e assetId.");
  }

  if (!Array.isArray(raw.stories) || raw.stories.length === 0) {
    throw new Error("O plano precisa conter ao menos um item em stories.");
  }

  const profileDir = resolveFromConfig(
    raw.profileDir || DEFAULT_PROFILE_DIR,
    configDir,
  );

  const stories = raw.stories.map((story, index) =>
    normalizeStoryItem(story, index, configDir),
  );

  return {
    configPath: absoluteConfigPath,
    businessId: String(raw.businessId),
    assetId: String(raw.assetId),
    shareToAccount: raw.shareToAccount || "ritosistemas",
    timezoneId: raw.timezoneId || "America/Sao_Paulo",
    baseUrl: raw.baseUrl || "https://business.facebook.com",
    profileDir,
    headless: raw.headless ?? false,
    slowMoMs: Number.isFinite(raw.slowMoMs) ? raw.slowMoMs : DEFAULT_SLOW_MO_MS,
    pacing: normalizePacingConfig(raw.pacing),
    stories,
  };
}

function normalizeStoryItem(story, index, configDir) {
  if (!story || typeof story !== "object") {
    throw new Error(`Story ${index + 1} invalido.`);
  }

  const label = story.label || `story-${index + 1}`;
  const date = String(story.date || "");
  const time = String(story.time || "");
  const imagePath = resolveFromConfig(String(story.imagePath || ""), configDir);

  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
    throw new Error(`Story "${label}" precisa usar date em formato YYYY-MM-DD.`);
  }

  if (!/^\d{2}:\d{2}$/.test(time)) {
    throw new Error(`Story "${label}" precisa usar time em formato HH:MM.`);
  }

  const [hourRaw, minuteRaw] = time.split(":").map((part) => Number.parseInt(part, 10));
  if (hourRaw < 0 || hourRaw > 23 || minuteRaw < 0 || minuteRaw > 59) {
    throw new Error(`Story "${label}" usa horario invalido: ${time}.`);
  }

  if (!path.isAbsolute(imagePath)) {
    throw new Error(`Story "${label}" precisa resolver para um caminho absoluto.`);
  }

  return {
    label,
    date,
    time,
    imagePath,
    slotKey: `${date} ${time}`,
  };
}

function resolveFromConfig(value, configDir) {
  if (!value) {
    return value;
  }

  if (path.isAbsolute(value)) {
    return value;
  }

  return path.resolve(configDir, value);
}

function applyStorySelection(stories, limit) {
  if (!limit) {
    return stories;
  }

  return stories.slice(0, limit);
}

function validateDuplicateSlots(stories) {
  const seen = new Map();

  for (const story of stories) {
    if (seen.has(story.slotKey)) {
      throw new Error(
        `Horario duplicado no plano: ${story.slotKey} em "${seen.get(story.slotKey)}" e "${story.label}".`,
      );
    }
    seen.set(story.slotKey, story.label);
  }
}

async function ensureStoryFilesExist(stories) {
  for (const story of stories) {
    try {
      const stats = await fs.stat(story.imagePath);
      if (!stats.isFile()) {
        throw new Error();
      }
    } catch {
      throw new Error(`Arquivo nao encontrado para "${story.label}": ${story.imagePath}`);
    }
  }
}

function normalizePacingConfig(rawPacing) {
  const config = {};

  for (const [key, defaultValue] of Object.entries(DEFAULT_PACING)) {
    const candidate = rawPacing?.[key];
    if (candidate == null) {
      config[key] = defaultValue;
      continue;
    }

    const numeric = Number(candidate);
    if (!Number.isFinite(numeric) || numeric < 0) {
      throw new Error(`Pacing invalido para "${key}". Use um numero maior ou igual a zero.`);
    }

    config[key] = Math.round(numeric);
  }

  return config;
}

function printResolvedPlan(config, stories) {
  console.log(`Plano: ${config.configPath}`);
  console.log(`Perfil do navegador: ${config.profileDir}`);
  console.log(`Business ID: ${config.businessId}`);
  console.log(`Asset ID: ${config.assetId}`);
  console.log(`Stories selecionados: ${stories.length}`);
  console.log(`Pacing entre stories: ${config.pacing.betweenStoriesMs}ms`);
  console.log("");

  for (const story of stories) {
    console.log(`- ${story.date} ${story.time} | ${story.label}`);
    console.log(`  ${story.imagePath}`);
  }
}

async function loadPlaywright() {
  try {
    return await import("playwright");
  } catch (error) {
    throw new Error(
      "Playwright nao encontrado. Rode `npm install` em scripts/meta-story-scheduler/ antes de usar o agendador.",
      { cause: error },
    );
  }
}

async function runAuthFlow(playwright, config, options) {
  const context = await launchPersistentContext(playwright, config, options);

  try {
    const page = context.pages()[0] || (await context.newPage());
    await page.goto(buildPlannerUrl(config), { waitUntil: "domcontentloaded" });

    console.log("");
    console.log("Janela aberta para autenticacao.");
    console.log("1. Faça login no Meta Business Suite, se necessario.");
    console.log("2. Confirme que a conta do Instagram correta esta selecionada.");
    console.log("3. Quando terminar, volte ao terminal e pressione Enter.");
    console.log("");

    const rl = readline.createInterface({ input, output });
    await rl.question("");
    rl.close();

    await page.goto(buildStoryComposerUrl(config), { waitUntil: "domcontentloaded" });
    await waitForStoryComposer(page, config.shareToAccount);

    console.log("");
    console.log(`Perfil autenticado salvo em: ${config.profileDir}`);
  } finally {
    await context.close();
  }
}

async function runScheduleFlow(playwright, config, stories, options) {
  await ensureStoryFilesExist(stories);
  const context = await launchPersistentContext(playwright, config, options);
  const page = context.pages()[0] || (await context.newPage());
  const results = [];

  try {
    for (let index = 0; index < stories.length; index += 1) {
      const story = stories[index];
      console.log(`[${index + 1}/${stories.length}] Agendando ${story.label} em ${story.date} ${story.time}...`);

      try {
        await scheduleSingleStory(page, config, story);
        results.push({ status: "scheduled", story });
        console.log(`  OK: ${story.label}`);

        if (index < stories.length - 1) {
          await pause(config.pacing.betweenStoriesMs);
        }
      } catch (error) {
        const screenshotPath = await captureDebugScreenshot(page, story.label);
        results.push({
          status: "failed",
          story,
          error: error instanceof Error ? error.message : String(error),
          screenshotPath,
        });
        console.error(`  FALHA: ${story.label}`);
        console.error(`  ${results.at(-1).error}`);
        console.error(`  Screenshot: ${screenshotPath}`);

        if (!options.continueOnError) {
          break;
        }
      }
    }
  } finally {
    await context.close();
  }

  console.log("");
  console.log("Resumo:");
  for (const result of results) {
    console.log(`- ${result.status.toUpperCase()} | ${result.story.date} ${result.story.time} | ${result.story.label}`);
  }

  if (results.some((result) => result.status === "failed")) {
    exit(1);
  }
}

async function launchPersistentContext(playwright, config, options) {
  const { chromium } = playwright;

  await fs.mkdir(config.profileDir, { recursive: true });

  return chromium.launchPersistentContext(config.profileDir, {
    channel: "chrome",
    headless: options.headless ?? config.headless,
    locale: "en-US",
    timezoneId: config.timezoneId,
    slowMo: config.slowMoMs,
    viewport: { width: 1440, height: 1200 },
    args: ["--window-size=1440,1200"],
  });
}

function buildPlannerUrl(config) {
  return `${config.baseUrl}/latest/content_calendar?business_id=${config.businessId}&asset_id=${config.assetId}`;
}

function buildStoryComposerUrl(config) {
  return `${config.baseUrl}/latest/story_composer/?asset_id=${config.assetId}&business_id=${config.businessId}&ir_qe_exposed=1&ref=biz_web_content_manager_calendar_tab_stories&context_ref=CONTENT_CALENDAR`;
}

async function scheduleSingleStory(page, config, story) {
  await page.goto(buildStoryComposerUrl(config), { waitUntil: "domcontentloaded" });
  await pause(config.pacing.afterComposerLoadMs);
  await waitForStoryComposer(page, config.shareToAccount);
  await clearComposerMediaIfNeeded(page, config.pacing);
  await uploadStoryImage(page, story.imagePath, config.pacing);
  await enableScheduling(page, config.pacing);
  await setStoryDate(page, story.date, config.pacing);
  await setStoryTime(page, story.time, config.pacing);
  await pause(config.pacing.beforeScheduleClickMs);
  await page.getByRole("button", { name: /^Schedule$/ }).click();
  await page.waitForURL(/content_calendar/, { timeout: DEFAULT_TIMEOUT_MS });
  await page.getByText(/successfully scheduled/i).waitFor({ timeout: DEFAULT_TIMEOUT_MS });
  await pause(config.pacing.afterScheduleSuccessMs);
}

async function waitForStoryComposer(page, expectedAccount) {
  await page.getByRole("heading", { name: "Create story", exact: true }).waitFor({
    timeout: DEFAULT_TIMEOUT_MS,
  });

  if (expectedAccount) {
    await page.getByRole("combobox", {
      name: new RegExp(`Share to ${escapeRegExp(expectedAccount)}`, "i"),
    }).waitFor({ timeout: DEFAULT_TIMEOUT_MS });
  }
}

async function clearComposerMediaIfNeeded(page, pacing) {
  const removeButton = page.getByRole("button", { name: /^Remove$/ });
  if (await removeButton.isVisible().catch(() => false)) {
    await removeButton.click();
    await page.getByRole("button", { name: "Add photo/video", exact: true }).waitFor({
      timeout: DEFAULT_TIMEOUT_MS,
    });
    await pause(pacing.afterMediaClearMs);
  }
}

async function uploadStoryImage(page, imagePath, pacing) {
  const chooserPromise = page.waitForEvent("filechooser", { timeout: DEFAULT_TIMEOUT_MS });
  await page.getByRole("button", { name: "Add photo/video", exact: true }).click({
    timeout: DEFAULT_TIMEOUT_MS,
  });
  const chooser = await chooserPromise;
  await chooser.setFiles([imagePath]);
  await page.getByRole("button", { name: /^Remove$/ }).waitFor({
    timeout: DEFAULT_TIMEOUT_MS,
  });
  await pause(pacing.afterMediaUploadMs);
}

async function enableScheduling(page, pacing) {
  const dateBox = page.getByRole("textbox", { name: "Date picker", exact: true });
  if (await dateBox.isVisible().catch(() => false)) {
    return;
  }

  await page.getByRole("switch", { name: "Set date and time", exact: true }).click({
    timeout: DEFAULT_TIMEOUT_MS,
  });

  await dateBox.waitFor({ timeout: DEFAULT_TIMEOUT_MS });
  await pause(pacing.afterScheduleToggleMs);
}

async function setStoryDate(page, isoDate, pacing) {
  const dateBox = page.getByRole("textbox", { name: "Date picker", exact: true });
  const dateInputText = formatDateForInput(isoDate);
  const expectedValue = formatDateForMetaUi(isoDate);

  await dateBox.click({ timeout: DEFAULT_TIMEOUT_MS });
  await dateBox.press(selectAllShortcut());
  await dateBox.type(dateInputText, { delay: 20 });
  await dateBox.press("Tab");
  await pause(pacing.afterDateSetMs);

  await waitFor(async () => {
    const currentValue = await dateBox.getAttribute("value");
    return currentValue === expectedValue;
  }, `Data nao aplicada corretamente: ${expectedValue}`);
}

async function setStoryTime(page, time24, pacing) {
  const { hours12, minutes, meridiem } = parseTime24(time24);
  const hourSpin = page.getByRole("spinbutton", { name: "hours", exact: true });
  const minuteSpin = page.getByRole("spinbutton", { name: "minutes", exact: true });
  const meridiemSpin = page.getByRole("spinbutton", { name: "meridiem", exact: true });

  await setSpinbuttonNumber(hourSpin, hours12, { min: 1, max: 12 }, pacing);
  await setSpinbuttonNumber(minuteSpin, minutes, { min: 0, max: 59 }, pacing);
  await setMeridiem(meridiemSpin, meridiem, pacing);
  await pause(pacing.afterTimeSetMs);
}

async function setSpinbuttonNumber(locator, target, bounds, pacing) {
  let current = await readSpinbuttonNumber(locator);
  if (current === target) {
    return;
  }

  const direction = computeShortestSpinDirection(current, target, bounds);
  const key = direction > 0 ? "ArrowUp" : "ArrowDown";

  await locator.click({ timeout: DEFAULT_TIMEOUT_MS });
  for (let index = 0; index < Math.abs(direction); index += 1) {
    await locator.press(key, { timeout: DEFAULT_TIMEOUT_MS });
    await pause(pacing.stepPauseMs);
  }

  current = await readSpinbuttonNumber(locator);
  if (current !== target) {
    throw new Error(`Spinbutton nao chegou no valor esperado. Atual: ${current}, esperado: ${target}.`);
  }
}

async function setMeridiem(locator, target, pacing) {
  const current = await readMeridiem(locator);
  if (current === target) {
    return;
  }

  await locator.click({ timeout: DEFAULT_TIMEOUT_MS });
  await locator.press(target === "PM" ? "p" : "a", { timeout: DEFAULT_TIMEOUT_MS });
  await pause(pacing.stepPauseMs);

  let updated = await readMeridiem(locator);
  if (updated === target) {
    return;
  }

  await locator.press("ArrowDown", { timeout: DEFAULT_TIMEOUT_MS });
  await pause(pacing.stepPauseMs);
  updated = await readMeridiem(locator);

  if (updated !== target) {
    throw new Error(`Meridiem nao chegou em ${target}. Atual: ${updated}.`);
  }
}

async function readSpinbuttonNumber(locator) {
  const value = await locator.getAttribute("aria-valuenow");
  const parsed = Number.parseInt(value || "", 10);

  if (!Number.isInteger(parsed)) {
    throw new Error("Nao foi possivel ler o valor numerico do spinbutton.");
  }

  return parsed;
}

async function readMeridiem(locator) {
  const value = (await locator.getAttribute("aria-valuetext")) || "";
  return value.toUpperCase();
}

function computeShortestSpinDirection(current, target, bounds) {
  const size = bounds.max - bounds.min + 1;
  const upward = ((target - current) % size + size) % size;
  const downward = ((current - target) % size + size) % size;

  return upward <= downward ? upward : -downward;
}

function parseTime24(time24) {
  const [hoursRaw, minutesRaw] = time24.split(":").map((part) => Number.parseInt(part, 10));
  const meridiem = hoursRaw >= 12 ? "PM" : "AM";
  const hours12 = hoursRaw % 12 === 0 ? 12 : hoursRaw % 12;

  return {
    hours12,
    minutes: minutesRaw,
    meridiem,
  };
}

function formatDateForInput(isoDate) {
  const [year, month, day] = isoDate.split("-");
  return `${month}/${day}/${year}`;
}

function formatDateForMetaUi(isoDate) {
  const [year, month, day] = isoDate.split("-").map((part) => Number.parseInt(part, 10));
  return DATE_DISPLAY_FORMATTER.format(new Date(Date.UTC(year, month - 1, day)));
}

function selectAllShortcut() {
  return process.platform === "darwin" ? "Meta+A" : "Control+A";
}

async function pause(durationMs) {
  if (!durationMs || durationMs <= 0) {
    return;
  }

  await new Promise((resolve) => setTimeout(resolve, durationMs));
}

async function waitFor(predicate, message, attempts = 20, delayMs = 250) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    if (await predicate()) {
      return;
    }

    await new Promise((resolve) => setTimeout(resolve, delayMs));
  }

  throw new Error(message);
}

async function captureDebugScreenshot(page, label) {
  const safeLabel = label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const filePath = path.join(
    os.tmpdir(),
    `rito-meta-story-scheduler-${safeLabel || "story"}-${Date.now()}.png`,
  );

  await page.screenshot({ path: filePath, fullPage: false }).catch(() => {});
  return filePath;
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

main().catch((error) => {
  console.error("");
  console.error("Erro no agendador de stories:");
  console.error(error instanceof Error ? error.message : String(error));
  exit(1);
});
