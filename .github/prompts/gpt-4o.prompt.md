# Prompt for GPT-4o

**Goal:**

- Using Github's MCP server fetch [PR102](https://github.com/enveng-group/dev_greenova/pull/102).
- Using Github's MCP server fetch [Issue87](https://github.com/enveng-group/dev_greenova/issues/87).
- Using git MCP server, read the diff in the Context section
  comparing this current branch integration/v0.0.6 and [mhahmad0:mhahmad0/issue87](https://github.com/mhahmad0/dev_greenova/tree/mhahmad0/issue87).
- Using sequential-thinking MCP server, analyse the incoming file changes in the
  sources section.
- Using sequential-thinking MCP server, systematically identify and
  using the filesystem mcp server cherry-pick and apply the changes from the
  incoming branch (mhahmad0:mhahmad0/issue87) to the current branch
  (integration/v0.0.6) that meet the objectives listed in the objective section.
- Using Context7 MCP server, ensure that the changes are consistent with
  Django's and all other modules' best practices available in the context7 MCP
  server.
- Using sqlite MCP server or the DBCode server, ensure that the changes made
  to the database schema are consistent with the project's **/models.py** files'.

**Context:**

- `logs/git_diff.diff`

**Objective:**

- Implement a company management feature to associate users with one or more companies.
- Ensure company data is unique, stored separately from obligation data, and used for metadata tracking and internal purposes.
- Create a new Django app named `company` with the following functionalities:
  - Define a `Company` model with appropriate fields.
  - Establish a many-to-many relationship between `User` and `Company` models.
  - Implement CRUD operations for managing companies through views and templates.
  - Add functionality for users to switch between companies they are associated with.
- Enforce proper access controls to ensure users can only view or manage companies they have access to.
- Maintain separation between company data and obligation data tables.
- Test and validate the company management interface to ensure all features work as intended.
- Optimize the implementation for security, performance, and maintainability.
- Document the functionality and provide clear instructions for usage.

**Source:**

- `greenova/company/admin.py`
- `greenova/company/middleware.py`
- `greenova/company/mixins.py`
- `greenova/company/models.py`
- `greenova/company/signals.py`
- `greenova/company/templates/company/company_delete.html`
- `greenova/company/templates/company/company_form.html`
- `greenova/company/templates/company/company_form_base.html`
- `greenova/company/templates/company/company_list.html`
- `greenova/company/templates/company/company_update.html`
- `greenova/company/templates/company/company_view.html`
- `greenova/company/urls.py`
- `greenova/company/views.py`

**Expectations**:

- Delete and consolidate files where multiple implementations exist, merging them into a single file globally.
- Use `use context7` to look up documentation from the context7 MCP server for project-specific configuration files and standards.
- Leverage additional MCP servers such as github, filesystem, JSON, context7, sqlite, git, fetch, sequential-thinking, and docker for assistance.

**Instructions**:

1. Remove outdated or unnecessary files, code, or documentation. Focus only on elements that no longer serve the project's objectives.

2. Organize project resources into a logical structure. Ensure consistent naming conventions and folder hierarchies for easier navigation.

3. Refactor code to improve readability, maintainability, and reduce technical debt. Address formatting or style violations flagged in pre-commit checks. Follow the preferred order of technologies for implementation:

4. **Restructured Text (RST)**: Use as the foundational layer for structure and content.
5. **HTML**: Utilize for semantic structure and markup.
6. **Protobuf3**: Utilize for data formats where applicable.
7. **Classless-CSS**: Apply minimal styling using Classless-PicoCSS.
8. **hyperscript**: Implement simple client-side interactions.
9. **htmx**: Leverage for more complex AJAX-based interactions.
10. **SASS/PostCSS**: Use for advanced styling needs when required.
11. **TypeScript**: Introduce only when absolutely necessary for type safety.
12. **AssemblyScript**: Reserve for WASM implementations as a last resort.

    Ensure that the refactored code adheres to these priorities and aligns with the project's coding standards and objectives.

13. Use automated tools like `bandit`, `autopep8`, `mypy`, `eslint`, `djlint`, `markdownlint`, `ShellCheck`, and `pylint` to enforce coding standards. Ensure all pre-commit checks pass without errors.

14. Add clear documentation for functions, classes, and modules. Use docstrings and comments to explain complex logic or important decisions.

15. Write unit and integration tests for new functionality and changes in `greenova/tests/test_pre_merge.py`. Use `pytest` with options like `--disable-warnings`, `--cov`, `--maxfail=1`, `--tb=short`, and `--pdb` to ensure comprehensive testing and debugging.

16. Review the code for security vulnerabilities using tools like `bandit`. Address any findings and optimize the code for performance and efficiency.

17. Iterate on the above steps until all issues are resolved and the code meets the project's requirements.
