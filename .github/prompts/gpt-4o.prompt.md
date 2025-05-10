---
description: Diagnose and resolve static asset MIME type and 404 errors for WASM, CSS, JS, SVG, and favicon resources in the Greenova Django app.
mode: agent

tools:
  - github
  - file_search
  - read_file
  - insert_edit_into_file
  - semantic_search
  - get_errors
  - sequential-thinking
  - Context7
  - filesystem
---

# GitHub Copilot Prompt Template for Static Asset MIME Type and 404 Errors

## Goal

Resolve issues where static WASM, CSS, JS, SVG, and favicon resources are not loading due to 404 errors or incorrect MIME types, resulting in browser errors such as:

- "Refused to apply style from '<URL>' because its MIME type ('text/html') is not a supported stylesheet MIME type, and strict MIME checking is enabled."
- "Failed to load resource: the server responded with a status of 404 ()"
- "Refused to execute script from '<URL>' because its MIME type ('text/html') is not executable, and strict MIME type checking is enabled."

## Context

- The Greenova Django app is serving static assets (WASM, CSS, JS, SVG, favicon) from `/static/` and `/img/` URLs.
- Browsers are refusing to load these assets due to 404 errors or because the server is returning `text/html` instead of the correct MIME type.
- This breaks site styling, interactivity, and icons.
- The project uses Django 5.2.1, Node.js 20.19.1, npm 11.3.0, and a modular app structure.
- Static files are managed via Django's staticfiles system and may be built with tools like Tailwind, PostCSS, or Webpack.

## Objectives

- Diagnose why static assets are returning 404 or incorrect MIME types.
- Ensure all static files (WASM, CSS, JS, SVG, favicon, etc.) are present in the correct locations and collected for deployment.
- Confirm Django's staticfiles settings, storage, and middleware are correctly configured for both development and production.
- Ensure the web server (if used in production) is configured to serve static files with correct MIME types.
- Update documentation and tests as needed.

## Sources

- `greenova/settings.py` (Django staticfiles and storage configuration)
- `static/` and `staticfiles/` directories (asset locations)
- `templates/` (static asset references in HTML)
- Build scripts (e.g., Tailwind, PostCSS, Webpack configs)
- Deployment and server configuration (Django's `runserver 0.0.0.0:80`, systemd config `greenova.service`, Cloudflare's reverse proxy managing SSL from Cloudlfare's Dashboard web UI service because of the `greenova` domain)
- Project static, staticfiles and deployment documentation (see context7)

## Expectations

- Copilot should inspect staticfiles settings, asset build output, and deployment configuration.
- All static assets should load with correct MIME types and no 404 errors.
- The solution should work for both development (`runserver`) and production deployments.
- All code and configuration should follow project and Django best practices.
- Documentation and tests should be updated as needed.

## Acceptance Criteria

- All WASM, CSS, JS, SVG, and favicon resources load without 404 or MIME type errors.
- Browser console is free of static asset loading errors.
- Static assets are served with correct MIME types.
- The solution works in both development and production environments.
- All pre-commit checks and tests pass.
- The solution is documented and does not break other workflows.

## Instructions

- Use `sequential-thinking` to break down the problem into smaller tasks.
- Use `Context7` to gather information about the project structure and configuration.
- Use `file_search` to locate relevant files and settings.
- Use `read_file` to inspect the contents of files related to staticfiles configuration, asset build output, and deployment setup.
- Investigate staticfiles configuration, asset build output, and deployment setup.
- Fix any issues with asset paths, collection, or MIME types.
- Test in both development and production environments.
- Update documentation and tests as needed.
- Iterate until all acceptance criteria are met.
