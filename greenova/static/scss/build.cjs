/**
 * SCSS Build Script
 *
 * This script compiles SCSS files to CSS and applies necessary transformations
 * like autoprefixing and minification.
 */

const fs = require('fs');
const path = require('path');
const postcss = require('postcss');
const sass = require('sass');

const inputDir = path.join(__dirname, './');
const outputDir = path.join(__dirname, '../css/dist/');

// Compile SCSS to CSS
function compileSCSS(file) {
  const result = sass.renderSync({
    file: path.join(inputDir, file),
  });
  return result.css.toString();
}

// Process CSS with PostCSS
async function processCSS(css, outputFile) {
  const result = await postcss([
    require('postcss-import'),
    require('tailwindcss'),
    require('autoprefixer'),
    require('cssnano')({ preset: 'default' }),
  ]).process(css, { from: undefined });

  fs.writeFileSync(path.join(outputDir, outputFile), result.css);
  console.log(`Generated: ${outputFile}`);
}

// Main build function
async function build() {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const scssFiles = fs
    .readdirSync(inputDir)
    .filter((file) => file.endsWith('.scss'));

  for (const file of scssFiles) {
    const css = compileSCSS(file);
    const outputFile = file.replace('.scss', '.css');
    await processCSS(css, outputFile);
  }

  console.log('Build complete.');
}

build().catch((err) => console.error(err));
