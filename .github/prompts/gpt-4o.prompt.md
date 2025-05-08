---
description:
  Automated issue resolution for logout, landing page, and JS errors in
  Greenova.
mode: agent

tools:
  - filesystem
  - sequential-thinking
  - json
---

# GitHub Copilot Prompt Template for Automated Issue Resolution

## Goal

Fix the following issues:

1. Logging out from the `/dashboard/` redirects to `/landing/` but displays a
   blank page until the user refreshes the page.
2. Reloading the `/landing/` page causes it to flash briefly before
   disappearing.
3. New JavaScript errors:
   - `Uncaught SyntaxError: Unexpected token ')'` in `theme-manager.js` and
     `wasm-loader.js`
   - `Uncaught SyntaxError: Unexpected token '{'` in `theme-manager.js`
   - `Uncaught SyntaxError: Failed to execute 'insertBefore' on 'Node': Identifier 'logo' has already been declared`
     in `htmx.min.js`
   - `Uncaught (in promise) TypeError: Failed to fetch` in `toolbar.js`

## Context

- **Environment**:
  - Django Version: 5.2.1
  - Python Version: 3.12.9
  - Database: SQLite3
- **Issue Details**:
  - The `/landing/` page should load automatically and display its content
    immediately after the logout action, and it should remain stable upon
    reload.
  - JavaScript errors are preventing proper functionality and need to be
    resolved.
- **Additional Files**:
  - The following files were added to the `landing` app and may assist with
    solving the logic problem:
    - `commons.py`
    - `constants.py`
    - `context_processors.py`
    - `middleware.py`
    - `mixins.py`
    - `permissions.py`
    - `serializers.py`
    - `signals.py`
    - `tasks.py`
    - `validators.py`
    - `templatetags/landing_tags.py`

## Objectives

1. Investigate the logout functionality in the `dashboard` app to identify the
   cause of the blank page and flashing issues.
2. Check the templates for the `/landing/` page to ensure they are correctly
   structured.
3. Analyze the newly added files in the `landing` app for potential logic
   issues or missing configurations.
4. Debug and fix the JavaScript errors in `theme-manager.js`, `wasm-loader.js`,
   `htmx.min.js`, and `toolbar.js`.
5. Refactor the code, templates, or newly added files as needed to resolve the
   issues.
6. Test the logout process and `/landing/` page to ensure they work correctly
   and remain stable upon reload.

## Sources

- Relevant files in the workspace:
  - `greenova/dashboard/views.py`
  - `greenova/dashboard/templates/dashboard/`
  - `greenova/landing/templates/landing/`
  - `greenova/urls.py`
  - `greenova/landing/commons.py`
  - `greenova/landing/constants.py`
  - `greenova/landing/context_processors.py`
  - `greenova/landing/middleware.py`
  - `greenova/landing/mixins.py`
  - `greenova/landing/permissions.py`
  - `greenova/landing/serializers.py`
  - `greenova/landing/signals.py`
  - `greenova/landing/tasks.py`
  - `greenova/landing/validators.py`
  - `greenova/landing/templatetags/landing_tags.py`
- Relevant commands:
  - `python manage.py runserver`
  - `python manage.py test`

## Expectations

1. Use the filesystem MCP server to read the `views.py` file in the `dashboard`
   app to analyze the logout functionality.
2. Use the filesystem MCP server to check the templates for the `/landing/`
   page to ensure they are correctly structured.
3. Use the filesystem MCP server to analyze the newly added files in the
   `landing` app for potential logic issues or missing configurations.
4. Use the sequential-thinking MCP server to identify the root cause of the
   blank page, flashing issues, and JavaScript errors.
5. Refactor the logout functionality, templates, or newly added files as needed
   to resolve the issues.
6. Debug and fix the JavaScript errors in `theme-manager.js`, `wasm-loader.js`,
   `htmx.min.js`, and `toolbar.js`.
7. Test the logout process and `/landing/` page to ensure they work correctly
   and remain stable upon reload.

## Acceptance Criteria
