---

description: Add a card to the left of Active Obligations on the dashboard that displays the count of overdue obligations in the Greenova Django app.
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

# GitHub Copilot Prompt Template for Overdue Obligations Card Feature

## Goal

Add a new card to the dashboard, positioned to the left of the "Active Obligations" card, that displays the count of overdue obligations for the selected project.

## Context

- The dashboard currently displays summary cards for Active Obligations, Upcoming Deadlines, Projects Overview, and Mechanisms Overview.
- There is no card showing the count of overdue obligations, which is a key compliance metric.
- The new card should match the style and structure of existing metric cards and be placed to the left of the "Active Obligations" card.
- The count should be dynamically calculated based on the selected project (if any) and update via HTMX as needed.
- The project uses Django 5.2.1, SQLite3, and follows a modular app structure.

## Objectives

- Add a new dashboard card for overdue obligations, styled consistently with existing cards.
- Calculate the overdue obligations count in the dashboard view logic.
- Ensure the card updates correctly when the project selection changes (HTMX support).
- Update tests and documentation as needed.

## Sources

- `greenova/dashboard/templates/dashboard/partials/dashboard_content.html` (dashboard cards markup)
- `greenova/dashboard/views.py` (dashboard context and logic)
- `obligations/models.py` (Obligation model definition)
- `dashboard/tests/` (dashboard tests)
- Project style and UI documentation (see context7)

## Expectations

- Copilot should update the dashboard template and view logic to include the overdue obligations card.
- The card should appear to the left of "Active Obligations" and update dynamically.
- All code should follow project coding and style guidelines.
- Tests and documentation should be updated as needed.

## Acceptance Criteria

- The dashboard displays a new card to the left of "Active Obligations" showing the overdue obligations count.
- The count is accurate and updates with project selection.
- All tests and pre-commit checks pass.
- The solution is documented and does not break other dashboard features.

## Instructions

- Update the dashboard template and view logic to add the overdue obligations card.
- Ensure dynamic updates and correct placement.
- Update or add tests and documentation.
- Iterate until all acceptance criteria are met.

---

description: Fix OperationalError 'no such column:
responsibility_responsibility.company_id' when accessing /obligations/create/
in Greenova Django app. mode: agent

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

# GitHub Copilot Prompt Template for Responsibility Model Migration Issue

## Goal

Resolve the database error 'no such column:
responsibility_responsibility.company_id' when accessing the obligations
creation form at `/obligations/create/` in the Greenova Django application.

## Context

- The error occurs when rendering the obligations creation form, specifically
  when displaying the responsibilities field in the template
  `obligations/form/new_obligation.html`.
- The stack trace indicates that the `Responsibility` model references a
  `company_id` column that does not exist in the database.
- This is likely due to a missing or unapplied database migration after adding
  or modifying a ForeignKey or field in the `Responsibility` model.
- The error prevents users from creating new obligations and breaks the
  obligations workflow.
- The project uses Django 5.2.1 and SQLite3.

## Objectives

- Diagnose why the `company_id` column is missing from the
  `responsibility_responsibility` table.
- Ensure all model changes for the `Responsibility` model are reflected in the
  database schema.
- Apply or generate the necessary migrations to add the `company_id` column if
  required.
- Confirm that the obligations creation form renders without error and the
  responsibilities field works as intended.
- Document the changes and rationale for the solution.

## Sources

- `greenova/responsibility/models.py` (Responsibility model definition)
- `greenova/obligations/forms.py` (Obligation form logic)
- `greenova/obligations/views.py` (Obligation creation view)
- `greenova/obligations/templates/obligations/form/new_obligation.html`
  (Obligation form template)
- `db.sqlite3` (database schema)
- Django migration files in `greenova/responsibility/migrations/`
- Project migration and database documentation (see context7)

## Expectations

- Copilot should use all available MCP servers to inspect model definitions,
  migrations, and database schema.
- Generate and apply missing migrations as needed.
- Refactor code or templates if model relationships have changed.
- Run pre-commit checks and tests to ensure the fix is robust.
- Document all changes and the reasoning behind them.

## Acceptance Criteria

- The obligations creation form at `/obligations/create/` renders without
  error.
- The responsibilities field displays and functions correctly.
- The `company_id` column exists in the `responsibility_responsibility` table
  if required by the model.
- All migrations are up to date and applied.
- All pre-commit checks and tests pass.
- The solution is documented and does not break other workflows.

## Instructions

- Investigate the `Responsibility` model and its migrations.
- Generate and apply any missing migrations.
- Test the obligations creation form after the fix.
- Document your changes and rationale.
- Iterate until all acceptance criteria are met.
