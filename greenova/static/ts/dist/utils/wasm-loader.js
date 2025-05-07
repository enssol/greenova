/**
 * WebAssembly Module Loader
 *
 * This utility handles loading and initializing the AssemblyScript WASM module
 * and provides a typed interface for interacting with it.
 */
var __awaiter =
  (this && this.__awaiter) ||
  function (thisArg, _arguments, P, generator) {
  function adopt(value) {
      return value instanceof P
        ? value
        : new P(function (resolve) {
            resolve(value);
          });
    }
  return new (P || (P = Promise))(function (resolve, reject) {
    function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
    function rejected(value) { try { step(generator['throw'](value)); } catch (e) { reject(e); } }
    function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
    step((generator = generator.apply(thisArg, _arguments || [])).next());
  });
  };
/**
 * Initialize the WebAssembly module
 * @returns Promise resolving to the initialized WASM module
 */
export function initializeWasmModule() {
  return __awaiter(this, void 0, void 0, function* () {
    try {
      // Path to the WASM file
      const wasmPath = '/static/as/build/optimized.wasm';
      // Fetch the WASM module
      const response = yield fetch(wasmPath);
      const buffer = yield response.arrayBuffer();
      // Instantiate the WASM module
      const { instance } = yield WebAssembly.instantiate(buffer, {
        env: {
          memory: new WebAssembly.Memory({ initial: 1 }),
          abort: (message, fileName, lineNumber, columnNumber) => {
            console.error('WASM module aborted:', { message, fileName, lineNumber, columnNumber });
          }
        }
      });
      // Return the exports as a typed module
      return instance.exports;
    }
    catch (error) {
      console.error('Failed to initialize WASM module:', error);
      throw new Error('WASM module initialization failed');
    }
  });
}
/**
 * Check if WebAssembly is supported in the current browser
 * @returns True if WebAssembly is supported
 */
export function isWasmSupported() {
  return typeof WebAssembly === 'object'
        && typeof WebAssembly.instantiate === 'function'
    typeof WebAssembly.Memory === 'function'
  );
}
//# sourceMappingURL=wasm-loader.js.map
