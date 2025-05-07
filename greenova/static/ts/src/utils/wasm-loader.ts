/**
 * WebAssembly Module Loader
 *
 * This utility handles loading and initializing the AssemblyScript WASM module
 * and provides a typed interface for interacting with it.
 */

// Interface for the WASM module exports
export interface GreenovaWasmModule {
  // Memory management
  memory: WebAssembly.Memory;

  // Theme functions
  getTheme: () => number;
  setTheme: (theme: number) => void;
  resolveTheme: (systemPrefersDark: number) => number;

  // Constants
  THEME_LIGHT: number;
  THEME_DARK: number;
  THEME_AUTO: number;

  // Error handling
  getLastErrorCode: () => number;
  getLastErrorDetails: () => number;
  recordError: (code: number, details: number) => void;
  clearError: () => void;
  ERROR_NONE: number;
  ERROR_GENERAL: number;
  ERROR_THEME: number;
  ERROR_ANIMATION: number;

  // Animation functions
  linearEasing: (current: number, duration: number) => number;
  easeInOutEasing: (current: number, duration: number) => number;
  calculateAnimationHeight: (
    isExpanding: boolean,
    progress: number,
    startHeight: number,
    endHeight: number
  ) => number;
}

/**
 * Initialize the WebAssembly module
 * @returns Promise resolving to the initialized WASM module
 */
export async function initializeWasmModule(): Promise<GreenovaWasmModule> {
  try {
    // Path to the WASM file
    const wasmPath = '/static/as/build/optimized.wasm';

    // Fetch the WASM module
    const response = await fetch(wasmPath);
    const buffer = await response.arrayBuffer();

    // Instantiate the WASM module
    const { instance } = await WebAssembly.instantiate(buffer, {
      env: {
        memory: new WebAssembly.Memory({ initial: 1 }),
        abort: (message: number, fileName: number, lineNumber: number, columnNumber: number) => {
          console.error(
            'WASM module aborted:',
            { message, fileName, lineNumber, columnNumber }
          );
        }
      }
    });

    // Return the exports as a typed module
    return instance.exports as unknown as GreenovaWasmModule;
  } catch (error) {
    console.error('Failed to initialize WASM module:', error);
    throw new Error('WASM module initialization failed');
  }
}

/**
 * Check if WebAssembly is supported in the current browser
 * @returns True if WebAssembly is supported
 */
export function isWasmSupported(): boolean {
  return typeof WebAssembly === 'object'
    && typeof WebAssembly.instantiate === 'function'
    && typeof WebAssembly.Memory === 'function';
}
