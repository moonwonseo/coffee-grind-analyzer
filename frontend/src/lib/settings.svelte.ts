/**
 * settings.ts — Shared app settings store with localStorage persistence.
 *
 * Unit preferences:
 *   - Temperature: °C or °F
 *   - Weight: g (grams) or mL (milliliters)
 *   - Particle size: always µm (not user-configurable)
 */

// ── Types ──────────────────────────────────────────────

export type TempUnit = 'C' | 'F';
export type WeightUnit = 'g' | 'mL';

export interface AppSettings {
  grinder: string;
  tempUnit: TempUnit;
  weightUnit: WeightUnit;
  notifications: boolean;
  publicProfile: boolean;
}

const STORAGE_KEY = 'truegrind_settings';

const DEFAULTS: AppSettings = {
  grinder: 'fellow-ode',
  tempUnit: 'C',
  weightUnit: 'g',
  notifications: true,
  publicProfile: false,
};

// ── State ──────────────────────────────────────────────

function loadSettings(): AppSettings {
  if (typeof localStorage === 'undefined') return { ...DEFAULTS };
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return { ...DEFAULTS, ...JSON.parse(raw) };
  } catch {}
  return { ...DEFAULTS };
}

let _settings = $state<AppSettings>(loadSettings());

function save() {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(_settings));
  }
}

// ── Public API ─────────────────────────────────────────

export function getSettings(): AppSettings {
  return _settings;
}

export function updateSettings(partial: Partial<AppSettings>) {
  Object.assign(_settings, partial);
  save();
}

// ── Conversion helpers ─────────────────────────────────

export function displayTemp(celsiusValue: number | undefined | null): string {
  if (celsiusValue == null) return '—';
  if (_settings.tempUnit === 'F') {
    return `${Math.round(celsiusValue * 9 / 5 + 32)}°F`;
  }
  return `${Math.round(celsiusValue)}°C`;
}

export function displayTempUnit(): string {
  return _settings.tempUnit === 'F' ? '°F' : '°C';
}

export function inputTempToCelsius(inputValue: number): number {
  if (_settings.tempUnit === 'F') {
    return (inputValue - 32) * 5 / 9;
  }
  return inputValue;
}

export function celsiusToDisplay(celsius: number): number {
  if (_settings.tempUnit === 'F') {
    return Math.round(celsius * 9 / 5 + 32);
  }
  return celsius;
}

export function displayWeight(grams: number | undefined | null): string {
  if (grams == null) return '—';
  if (_settings.weightUnit === 'mL') {
    return `${Math.round(grams)} mL`;
  }
  return `${Math.round(grams)} g`;
}

export function displayWeightUnit(): string {
  return _settings.weightUnit;
}

/**
 * Convert user input weight to grams for the API.
 * If using mL, we treat 1mL ≈ 1g (water density at brewing temp).
 */
export function inputWeightToGrams(inputValue: number): number {
  // For coffee brewing, 1 mL water ≈ 1 g, so no conversion needed
  return inputValue;
}

export function tempPlaceholder(): string {
  return _settings.tempUnit === 'F' ? '200' : '94';
}
