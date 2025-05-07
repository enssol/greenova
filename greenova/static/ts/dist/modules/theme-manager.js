/**
 * Greenova TypeScript Theme Manager
 *
 * This module manages theme application and system preference detection,
 * leveraging the AssemblyScript WASM module for performance-critical operations.
 */
/**
 * Theme manager class
 */
export class ThemeManager {
  constructor(wasmModule) {
    this.wasmModule = wasmModule;
    // Theme configuration
    this.config = {
      rootAttribute: 'data-theme',
      localStorageKey: 'picoPreferredColorScheme',
      defaultScheme: 'auto'
    };
    // System preference media query
    this.mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  }
  /**
   * Initialize the theme manager
   * Important: This should be called as early as possible in the page load
   */
  init() {
    // Get stored theme preference
    const savedTheme = this.getStoredTheme();
    // Set theme preference in WASM
    this.setThemeInWasm(savedTheme);
    // Apply theme to document
    this.applyTheme(savedTheme);
    // Set up listener for system preference changes
    this.setupSystemPreferenceListener();
    // Set up theme toggle listeners
    this.setupThemeToggleListeners();
  }
  /**
   * Get theme from local storage or use default
   * @returns The stored theme or default
   */
  getStoredTheme() {
    var _a;
    const storedTheme = (_a = window.localStorage) === null || _a === void 0 ? void 0 : _a.getItem(this.config.localStorageKey);
    return storedTheme || this.config.defaultScheme;
  }
  /**
   * Set theme preference in WASM module
   * @param theme The theme to set ('light', 'dark', or 'auto')
   */
  setThemeInWasm(theme) {
    let themeValue;
    switch (theme) {
      case 'light':
        themeValue = this.wasmModule.THEME_LIGHT;
      break;
      case 'dark':
        themeValue = this.wasmModule.THEME_DARK;
      break;
      case 'auto':
      default:
        themeValue = this.wasmModule.THEME_AUTO;
      break;
    }
    this.wasmModule.setTheme(themeValue);
  }
  /**
   * Get system preference for dark mode
   * @returns True if system prefers dark mode
   */
  getSystemPreference() {
    return this.mediaQuery.matches;
  }
  /**
   * Apply theme to document
   * @param theme The theme to apply ('light', 'dark', or 'auto')
   */
  applyTheme(theme) {
    const rootElement = document.documentElement;
    if (!rootElement)
      return;
    if (theme === 'auto') {
      // Use WASM module to resolve theme based on system preference
      const systemPrefersDark = this.getSystemPreference() ? 1 : 0;
      const resolvedTheme = this.wasmModule.resolveTheme(systemPrefersDark);
      // Apply resolved theme
      rootElement.setAttribute(this.config.rootAttribute, resolvedTheme === this.wasmModule.THEME_DARK ? 'dark' : 'light');
    }
    } else {
      // Apply explicit theme
      rootElement.setAttribute(this.config.rootAttribute, theme);
    }
    // Dispatch theme changed event
    this.dispatchThemeChangedEvent(theme);
  }
  /**
   * Set up listener for system preference changes
   */
  setupSystemPreferenceListener() {
    // Check if matchMedia is supported
    if (!this.mediaQuery || !this.mediaQuery.addEventListener)
      return;
    // Use the modern event listener approach
    this.mediaQuery.addEventListener('change', () => {
      const storedTheme = this.getStoredTheme();
      if (storedTheme === 'auto') {
        this.applyTheme('auto');
      }
    });
  }
  /**
   * Set up listeners for theme toggle elements
   */
  setupThemeToggleListeners() {
    // Find all theme toggles
    const themeToggles = document.querySelectorAll('[data-theme-toggle]');
    themeToggles.forEach(toggle => {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const targetTheme = toggle.getAttribute('data-theme-value') || 'auto';
        this.setTheme(targetTheme);
      });
    });
  }
  /**
   * Set and save theme preference
   * @param theme The theme to set ('light', 'dark', or 'auto')
   */
  setTheme(theme) {
    // Validate theme
    if (!['light', 'dark', 'auto'].includes(theme)) {
      theme = this.config.defaultScheme;
    }
    // Save to local storage
    try {
      window.localStorage.setItem(this.config.localStorageKey, theme);
    }
    catch (error) {
      console.error('Failed to save theme preference to localStorage:', error);
    }
    // Update WASM module
    this.setThemeInWasm(theme);
    // Apply theme
    this.applyTheme(theme);
  }
  /**
   * Dispatch custom event when theme changes
   * @param theme The current theme
   */
  dispatchThemeChangedEvent(theme) {
    window.dispatchEvent(new CustomEvent('themeChanged', {
      detail: { theme }
    }));
  }
  /**
   * Get the current theme
   * @returns The current theme ('light', 'dark', or 'auto')
   */
  getCurrentTheme() {
    const storedTheme = this.getStoredTheme();
    if (storedTheme === 'auto') {
      const systemPrefersDark = this.getSystemPreference() ? 1 : 0;
      const resolvedTheme = this.wasmModule.resolveTheme(systemPrefersDark);
      return resolvedTheme === this.wasmModule.THEME_DARK ? 'dark' : 'light';
    }
    return storedTheme;
  }
  /**
   * Toggle between light and dark themes
   * If current theme is auto, sets to light or dark based on current appearance
   */
  toggleTheme() {
    const currentTheme = this.getCurrentTheme();
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    this.setTheme(newTheme);
  }
}
//# sourceMappingURL=theme-manager.js.map
