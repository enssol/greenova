import { exec } from 'child_process';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import path from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Copy WASM files to the static directory
function copyWasmFiles() {
  const sourceDir = path.resolve(__dirname, '../greenova/static/as/build');
  const destDir = path.resolve(__dirname, '../greenova/static/dist/wasm');

  // Ensure destination directory exists
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }

  // Copy optimized and debug WASM files
  ['optimized.wasm', 'debug.wasm'].forEach((file) => {
    const sourcePath = path.join(sourceDir, file);
    const destPath = path.join(destDir, file);
    if (fs.existsSync(sourcePath)) {
      fs.copyFileSync(sourcePath, destPath);
      console.log(`Copied ${file} to ${destDir}`);
    }
  });
}

// Run TypeScript compilation
exec(
  'npx tsc --project ../greenova/static/ts/tsconfig.json',
  {
    cwd: __dirname,
  },
  (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      process.exit(1);
    }
    if (stderr) {
      console.error(`Stderr: ${stderr}`);
      process.exit(1);
    }
    console.log(`Stdout: ${stdout}`);

    // After successful TypeScript compilation, copy WASM files
    copyWasmFiles();
  }
);
