# Prompt for GPT-4o

**Goal:** Interactively cherry-pick all changes in code in `.vscode/tasks.json` `greenova/users/templates/users/partials/profile_detail.html` and `greenova/users/views.py` from [PR97](https://github.com/enveng-group/dev_greenova/pull/97) that resolves [Issue88](https://github.com/enveng-group/dev_greenova/issues/88).

**Context:** The Greenova project aims to enhance the user profile functionality by establishing a relationship between the user profile's role and the responsibility table, and by adding an overdue actions display. This involves backend, profile view, and frontend enhancements, as well as real-time updates and thorough testing to ensure compliance with project standards and accessibility guidelines.

**Output:**

```diff
diff --git a/.vscode/tasks.json b/.vscode/tasks.json
old mode 100755
new mode 100644
index c41da99..5948945
--- a/.vscode/tasks.json
+++ b/.vscode/tasks.json
@@ -1,4 +1,818 @@
 {
-  "tasks": [],
+  "tasks": [
+    {
+      "args": [
+        "-c",
+        "autopep8 --in-place --aggressive --aggressive \"${file}\""
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Format with autopep8",
+      "presentation": {
+        "clear": true,
+        "panel": "shared",
+        "reveal": "silent"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "isort \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Sort imports with isort",
+      "presentation": {
+        "clear": true,
+        "panel": "shared",
+        "reveal": "silent"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "pylint \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Lint with pylint",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "python",
+        "pattern": {
+          "column": 3,
+          "file": 1,
+          "line": 2,
+          "message": 5,
+          "regexp": "^(.+):(\\d+):(\\d+):\\s+(warning|error|fatal):\\s+(.*)$",
+          "severity": 4
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "mypy \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Type check with mypy",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "python",
+        "pattern": {
+          "file": 1,
+          "line": 2,
+          "message": 4,
+          "regexp": "^(.+):(\\d+):\\s+(error|note):\\s+(.*)$",
+          "severity": 3
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "mypy --ignore-missing-imports --disallow-untyped-defs --no-implicit-optional \"${file}\""
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Type check with mypy (standard)",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "python",
+        "pattern": {
+          "file": 1,
+          "line": 2,
+          "message": 4,
+          "regexp": "^(.+):(\\d+):\\s+(error|note):\\s+(.*)$",
+          "severity": 3
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "mypy --config-file \"${workspaceFolder}/mypy.ini\" \"${file}\""
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Type check with mypy (Django)",
+      "options": {
+        "env": {
+          "PYTHONPATH": "/workspaces/greenova"
+        }
+      },
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "python",
+        "pattern": {
+          "file": 1,
+          "line": 2,
+          "message": 4,
+          "regexp": "^(.+):(\\d+):\\s+(error|note):\\s+(.*)$",
+          "severity": 3
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "bandit -r \"${file}\" --skip B101"],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Security check with bandit",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "dependsOn": [
+        "Python: Sort imports with isort",
+        "Python: Format with autopep8",
+        "Python: Lint with pylint",
+        "Python: Type check with mypy (standard)",
+        "Python: Security check with bandit"
+      ],
+      "dependsOrder": "sequence",
+      "group": "none",
+      "label": "Python: Fix all",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": []
+    },
+    {
+      "args": [
+        "-c",
+        "pylint --rcfile=\"${workspaceFolder}/.pylintrc\" \"${file}\""
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Lint with pylint (standard)",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "python",
+        "pattern": {
+          "column": 3,
+          "file": 1,
+          "line": 2,
+          "message": 5,
+          "regexp": "^(.+):(\\d+):(\\d+):\\s+(warning|error|fatal):\\s+(.*)$",
+          "severity": 4
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "pylint --rcfile=\"${workspaceFolder}/.pylintrc-django\" --load-plugins=pylint_django \"${file}\""
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Lint with pylint (Django)",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "python",
+        "pattern": {
+          "column": 3,
+          "file": 1,
+          "line": 2,
+          "message": 5,
+          "regexp": "^(.+):(\\d+):(\\d+):\\s+(warning|error|fatal):\\s+(.*)$",
+          "severity": 4
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "dependsOn": [
+        "Python: Sort imports with isort",
+        "Python: Format with autopep8",
+        "Python: Lint with pylint (standard)",
+        "Python: Type check with mypy (standard)"
+      ],
+      "dependsOrder": "sequence",
+      "group": "none",
+      "label": "Python: Fix all (standard)",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": []
+    },
+    {
+      "dependsOn": [
+        "Python: Sort imports with isort",
+        "Python: Format with autopep8",
+        "Python: Lint with pylint (Django)",
+        "Python: Type check with mypy (Django)",
+        "Python: Security check with bandit"
+      ],
+      "dependsOrder": "sequence",
+      "group": "none",
+      "label": "Python: Fix all (Django)",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": []
+    },
+    {
+      "args": [
+        "-c",
+        "mypy --no-config --ignore-missing-imports --disallow-untyped-defs --no-implicit-optional \"${file}\""
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Type check with mypy (config files)",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "python",
+        "pattern": {
+          "file": 1,
+          "line": 2,
+          "message": 4,
+          "regexp": "^(.+):(\\d+):\\s+(error|note):\\s+(.*)$",
+          "severity": 3
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "djlint \"${file}\" --reformat"],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "HTML: Format with djlint",
+      "presentation": {
+        "clear": true,
+        "panel": "shared",
+        "reveal": "silent"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "djlint \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "HTML: Lint with djlint",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "djlint",
+        "pattern": {
+          "column": 3,
+          "file": 1,
+          "line": 2,
+          "message": 5,
+          "regexp": "^(.+):(\\d+):(\\d+):\\s+(\\w+)\\s+(.+)$",
+          "severity": 4
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "npx prettier --write \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "JavaScript: Format with prettier",
+      "presentation": {
+        "clear": true,
+        "panel": "shared",
+        "reveal": "silent"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "npx eslint \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "JavaScript: Lint with eslint",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": ["$eslint-stylish"],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "npx eslint --fix \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "JavaScript: Fix eslint issues",
+      "presentation": {
+        "clear": true,
+        "panel": "shared",
+        "reveal": "silent"
+      },
+      "problemMatcher": ["$eslint-stylish"],
+      "type": "shell"
+    },
+    {
+      "dependsOn": [
+        "JavaScript: Format with prettier",
+        "JavaScript: Fix eslint issues"
+      ],
+      "dependsOrder": "sequence",
+      "group": "none",
+      "label": "JavaScript: Fix all",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": []
+    },
+    {
+      "args": ["-c", "npx prettier --write \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "CSS: Format with prettier",
+      "presentation": {
+        "clear": true,
+        "panel": "shared",
+        "reveal": "silent"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "npx stylelint \"${file}\" --config \"${workspaceFolder}/stylelint.config.js\""
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "CSS: Lint with stylelint",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "stylelint",
+        "pattern": {
+          "column": 3,
+          "file": 1,
+          "line": 2,
+          "message": 5,
+          "regexp": "^([^:]+):(\\d+):(\\d+):\\s+(.+)\\s+(.+)$",
+          "severity": 4
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "npx stylelint \"${file}\" --config \"${workspaceFolder}/stylelint.config.js\" --fix"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "CSS: Fix stylelint issues",
+      "presentation": {
+        "clear": true,
+        "panel": "shared",
+        "reveal": "silent"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "dependsOn": ["CSS: Format with prettier", "CSS: Fix stylelint issues"],
+      "dependsOrder": "sequence",
+      "group": "none",
+      "label": "CSS: Fix all",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": []
+    },
+    {
+      "args": ["-c", "npx prettier --write \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "JSON: Format with prettier",
+      "presentation": {
+        "clear": true,
+        "panel": "shared",
+        "reveal": "silent"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "npx prettier --config \"${workspaceFolder}/.prettierrc\" --write \"${file}\""
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "YAML: Format with prettier",
+      "presentation": {
+        "clear": true,
+        "panel": "shared",
+        "reveal": "silent"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "npx prettier --write \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Markdown: Format with prettier",
+      "presentation": {
+        "clear": true,
+        "panel": "shared",
+        "reveal": "silent"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "/usr/local/share/nvm/current/bin/markdownlint-cli2 --fix \"${file}\""
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Markdown: Lint with markdownlint",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "markdownlint",
+        "pattern": {
+          "column": 3,
+          "file": 1,
+          "line": 2,
+          "message": 4,
+          "regexp": "^(.+?):(\\d+)(?::(\\d+))? (.+)$"
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "dependsOn": [
+        "Markdown: Format with prettier",
+        "Markdown: Lint with markdownlint"
+      ],
+      "dependsOrder": "sequence",
+      "group": "none",
+      "label": "Markdown: Fix all",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": []
+    },
+    {
+      "args": ["-c", "shellcheck \"${file}\""],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Shell: Check with shellcheck",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": {
+        "fileLocation": ["relative", "${workspaceFolder}"],
+        "owner": "shellcheck",
+        "pattern": {
+          "column": 3,
+          "file": 1,
+          "line": 2,
+          "message": 5,
+          "regexp": "^(.+):(\\d+):(\\d+):\\s+(note|warning|error|style):\\s+(.*)$",
+          "severity": 4
+        }
+      },
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "${command:workbench.action.terminal.clear}"],
+      "command": "/bin/sh",
+      "group": {
+        "isDefault": true,
+        "kind": "build"
+      },
+      "label": "Format current file",
+      "linux": {
+        "args": ["-c", "clear"],
+        "command": "/bin/sh"
+      },
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell",
+      "windows": {
+        "args": ["/c", "cls"],
+        "command": "cmd.exe"
+      }
+    },
+    {
+      "args": [
+        "-c",
+        "if [ -n \"$(echo \"${file}\" | grep '\\\\.py$')\" ]; then autopep8 --in-place \"${file}\" && isort \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\\\.html$')\" ]; then djlint \"${file}\" --reformat; elif [ -n \"$(echo \"${file}\" | grep '\\\\.(js\\\\|css\\\\|json\\\\|md\\\\|yaml\\\\|yml\\\\|toml)$')\" ]; then npx prettier --write \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\\\.sh$')\" ]; then echo \"Shell files can't be formatted automatically, running shellcheck...\"; shellcheck \"${file}\"; fi"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Auto-detect and format file",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "if [ -n \"$(echo \"${file}\" | grep '/greenova/.*\\.py$')\" ]; then pylint --rcfile=${workspaceFolder}/.pylintrc-django --load-plugins=tools.pylint.fix_good_names,pylint_django,tools.pylint.gevent_checker \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.py$')\" ]; then pylint --rcfile=${workspaceFolder}/.pylintrc \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.html$')\" ]; then djlint \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.js$')\" ]; then npx eslint \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.md$')\" ]; then /usr/local/share/nvm/current/bin/markdownlint-cli2 \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.sh$')\" ]; then shellcheck \"${file}\"; fi"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Auto-detect and lint file",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "if [ -n \"$(echo \"${file}\" | grep '/greenova/.*\\.py$')\" ]; then isort \"${file}\" && autopep8 --in-place \"${file}\" && pylint --rcfile=${workspaceFolder}/.pylintrc-django --load-plugins=pylint_django \"${file}\" && mypy --config-file ${workspaceFolder}/mypy.ini \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\(setup\\.py\\|pyproject\\.toml\\|\\.pylintrc\\)')\" ]; then isort \"${file}\" && autopep8 --in-place \"${file}\" && pylint --rcfile=${workspaceFolder}/.pylintrc \"${file}\" && mypy --no-config --ignore-missing-imports \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.py$')\" ]; then isort \"${file}\" && autopep8 --in-place \"${file}\" && pylint --rcfile=${workspaceFolder}/.pylintrc \"${file}\" && mypy --ignore-missing-imports --disallow-untyped-defs \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.html$')\" ]; then djlint \"${file}\" --reformat; elif [ -n \"$(echo \"${file}\" | grep '\\.js$')\" ]; then npx prettier --write \"${file}\" && npx eslint --fix \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.md$')\" ]; then npx prettier --write \"${file}\" && /usr/local/share/nvm/current/bin/markdownlint-cli2 \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.(css\\|json\\|yaml\\|yml\\|toml)$')\" ]; then npx prettier --write \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.css$')\" ]; then npx stylelint --config \"${workspaceFolder}/stylelint.config.js\" --fix \"${file}\"; elif [ -n \"$(echo \"${file}\" | grep '\\.sh$')\" ]; then shellcheck \"${file}\"; fi"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Auto-detect and fix all issues",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "find . -type d -name \"__pycache__\" -exec rm -rf {} \\; 2>/dev/null || true && find . -name \"*.pyc\" -delete"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Python: Clean cache files",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+
+    {
+      "args": [
+        "-c",
+        "cd greenova && python3 manage.py collectstatic --clear --noinput"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Collect static files",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+
+    {
+      "args": [
+        "-c",
+        "cd greenova && python3 manage.py import_obligations dummy_data.csv"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Import obligations",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "cd greenova && python3 manage.py sync_mechanisms"],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Sync mechanisms",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "cd greenova && python3 manage.py createsuperuser"],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Create superuser",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "dependsOn": ["Django: Run Tailwind", "Django: Run server"],
+      "dependsOrder": "parallel",
+      "group": "none",
+      "label": "Django: Development environment",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "cd greenova/theme/static_src/src && npm install && cd ../../.. && python3 manage.py tailwind check-updates && python3 manage.py tailwind update && python3 manage.py tailwind install && python3 manage.py tailwind build"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Build and install Tailwind",
+      "presentation": {
+        "panel": "dedicated",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "cd greenova && python3 manage.py runserver"],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Run server",
+      "presentation": {
+        "panel": "dedicated",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "cd greenova && python manage.py create_missing_profiles"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Create Missing Profiles",
+      "presentation": {
+        "panel": "dedicated",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "cd greenova && python3 manage.py check"],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Check",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "cd greenova && python3 manage.py compile_protos"],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Compile Proto",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "npx protolint lint --fix ."],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Protolint: Lint with protolint",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    }
+    {
+      "args": [
+        "-c",
+        "cd greenova && python3 manage.py makemigrations chatbot company users mechanisms obligations projects responsibility procedures feedback"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Create migrations",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": ["-c", "cd greenova && python3 manage.py migrate"],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Apply migrations",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "args": [
+        "-c",
+        "find . -path \"*/migrations/*.py\" -not -name \"__init__.py\" -delete"
+      ],
+      "command": "/bin/sh",
+      "group": "none",
+      "label": "Django: Delete Migrations",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": [],
+      "type": "shell"
+    },
+    {
+      "label": "Django: Refresh migrations",
+      "dependsOn": [
+        "Django: Delete Migrations",
+        "Django: Create migrations",
+        "Django: Apply migrations"
+      ],
+      "dependsOrder": "sequence",
+      "type": "shell",
+      "group": "none",
+      "presentation": {
+        "panel": "shared",
+        "reveal": "always"
+      },
+      "problemMatcher": []
+    }
+  ],
   "version": "2.0.0"
 }
diff --git a/greenova/users/templates/users/partials/profile_detail.html b/greenova/users/templates/users/partials/profile_detail.html
old mode 100755
new mode 100644
index c698aef..3f73b67
--- a/greenova/users/templates/users/partials/profile_detail.html
+++ b/greenova/users/templates/users/partials/profile_detail.html
@@ -8,9 +8,7 @@
         {% if profile.profile_image %}
           <img src="{{ profile.profile_image.url }}"
                alt="Profile picture"
-               class="profile-image"
-               height="150"
-               width="150" />
+               class="profile-image" />
         {% else %}
           <div class="profile-initial">
 {{ profile.user.username|first|upper }}
diff --git a/greenova/users/views.py b/greenova/users/views.py
old mode 100755
new mode 100644
index 7b2a72c..b467fb5
--- a/greenova/users/views.py
+++ b/greenova/users/views.py
@@ -1,23 +1,22 @@
-from typing import Any
+from datetime import timedelta
+from typing import Any, Dict

 from company.models import CompanyMembership
 from django.contrib import messages
-from django.contrib.auth import get_user_model, update_session_auth_hash
+from django.contrib.auth import get_user_model  # Updated import for User model
+from django.contrib.auth import update_session_auth_hash
 from django.contrib.auth.decorators import login_required, user_passes_test
 from django.contrib.auth.forms import PasswordChangeForm
 from django.http import HttpRequest, HttpResponse, JsonResponse
 from django.shortcuts import get_object_or_404, redirect, render
-from django.template.loader import render_to_string
-from django.urls import reverse
-from django.views.decorators.http import require_http_methods
-from django_htmx.http import trigger_client_event
+from django.utils import timezone
 from obligations.models import Obligation
 from projects.models import Project

 from .forms import AdminUserForm, ProfileImageForm, UserProfileForm
 from .models import Profile

-User = get_user_model()
+User = get_user_model()  # Use the recommended method to get the User model


 def is_admin(user: User) -> bool:
@@ -31,221 +30,190 @@ def profile_view(request: HttpRequest) -> HttpResponse:
     profile: Profile = request.user.profile

     company_memberships = CompanyMembership.objects.filter(user_id=request.user.id)
-
+
     if not company_memberships:
-        context: dict[str, Any] = {"profile": profile, "overdue_count": 0}
+        # No company memberships found for user
+
+        context: Dict[str, Any] = {
+        'profile': profile,
+        'overdue_count': 0
+    }
     else:
         # Get all the roles this user has across companies
-        user_roles = company_memberships.values_list("role", flat=True).distinct()
-
+        user_roles = company_memberships.values_list('role', flat=True).distinct()
+
         # Find obligations that match any of the user's roles
-        project_ids = Project.objects.filter(members=request.user.id).values_list(
-            "id", flat=True
-        )
-
+        project_ids = Project.objects.filter(members=request.user.id).values_list('id', flat=True)
+
         # Find obligations that match any of the user's roles and are in their projects
-        obligations = (
-            Obligation.objects.filter(
-                responsibility__in=user_roles, project_id__in=project_ids
-            )
-            .select_related("project")
-            .distinct()
-        )
-
-        # Get obligations that are overdue
-        overdue_obligations = [
-            obligation for obligation in obligations if obligation.is_overdue
-        ]
-
-        context: dict[str, Any] = {
-            "profile": profile,
-            "overdue_count": len(overdue_obligations),
+        obligations = Obligation.objects.filter(
+            responsibility__in=user_roles,
+            project_id__in=project_ids
+        ).select_related('project').distinct()
+
+        # Get obligations that are overdue (due_date is in the past)
+        overdue_obligations = [obligation for obligation in obligations if obligation.is_overdue]
+
+        context: Dict[str, Any] = {
+        'profile': profile,
+        'overdue_count': len(overdue_obligations),
         }
+

     if request.htmx:
-        return render(request, "users/partials/profile_detail.html", context)
-    return render(request, "users/profile_detail.html", context)
+        return render(request, 'users/partials/profile_detail.html', context)
+    return render(request, 'users/profile_detail.html', context)


 @login_required
-def profile_edit(request):
+def profile_edit(request: HttpRequest) -> HttpResponse:
     """View for editing user's profile."""
-    profile = request.user.profile
+    profile: Profile = request.user.profile

-    if request.method == "POST":
-        form = UserProfileForm(request.POST, instance=profile)
+    if request.method == 'POST':
+        form = UserProfileForm(request.POST, request.FILES, instance=profile)
         if form.is_valid():
             form.save()
-            messages.success(request, "Profile updated successfully.")
-
-            if request.htmx:
-                response = render(
-                    request, "users/partials/profile_detail.html", {"profile": profile}
-                )
-                return trigger_client_event(response, "profileUpdated", {})
-            return redirect("users:profile")
-
-        messages.error(request, "Please correct the errors below.")
+            messages.success(request, 'Profile updated successfully.')
+            return redirect('users:profile')
     else:
-        # Initialize form with current user data
-        form = UserProfileForm(
-            instance=profile,
-            initial={
-                "first_name": request.user.first_name,
-                "last_name": request.user.last_name,
-                "email": request.user.email,
-            },
-        )
+        form = UserProfileForm(instance=profile)

-    context = {
-        "form": form,
-        "profile": profile,
+    context: Dict[str, Any] = {
+        'form': form,
+        'profile': profile,
     }

     if request.htmx:
-        return render(request, "users/partials/profile_edit_form.html", context)
-    return render(request, "users/profile_edit.html", context)
+        return render(request, 'users/partials/profile_edit.html', context)
+    return render(request, 'users/profile_edit.html', context)


 @login_required
-def change_password(request):
-    """View for changing password."""
-    if request.method == "POST":
+def change_password(request: HttpRequest) -> HttpResponse:
+    """View for changing user password."""
+    if request.method == 'POST':
         form = PasswordChangeForm(request.user, request.POST)
         if form.is_valid():
             user = form.save()
+            # Update session to prevent logout
             update_session_auth_hash(request, user)
-            messages.success(request, "Your password was successfully updated!")
-
-            if request.htmx:
-                return HttpResponse(
-                    '<div class="alert success">Password changed successfully.</div>',
-                    headers={"HX-Trigger": "passwordChanged"},
-                )
-            return redirect("users:profile")
+            messages.success(request, 'Your password was successfully updated!')
+            return redirect('users:profile')
     else:
         form = PasswordChangeForm(request.user)

-    context = {"form": form}
+    context: Dict[str, Any] = {'form': form}

     if request.htmx:
-        return render(request, "users/partials/password_change_form.html", context)
-    return render(request, "users/password_change.html", context)
+        return render(request, 'users/partials/change_password.html', context)
+    return render(request, 'users/change_password.html', context)


 @login_required
-@require_http_methods(["POST"])
-def upload_profile_image(request):
-    """AJAX view for uploading profile image."""
-    form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
-    if form.is_valid():
-        form.save()
-        return JsonResponse(
-            {"status": "success", "image_url": request.user.profile.profile_image.url}
+def upload_profile_image(request: HttpRequest) -> HttpResponse:
+    """View for uploading a profile image."""
+    if request.method == 'POST':
+        form = ProfileImageForm(
+            request.POST, request.FILES, instance=request.user.profile
         )
-    return JsonResponse({"status": "error", "errors": form.errors})
+        if form.is_valid():
+            form.save()
+            messages.success(request, 'Profile image updated successfully.')
+
+            if request.htmx:
+                return JsonResponse(
+                    {
+                        'success': True,
+                        'image_url': request.user.profile.profile_image.url,
+                    }
+                )
+            return redirect('users:profile')
+    else:
+        form = ProfileImageForm(instance=request.user.profile)
+
+    context = {
+        'form': form,
+    }
+
+    return render(request, 'users/partials/profile_image_form.html', context)


 @user_passes_test(is_admin)
-def admin_user_list(request):
-    """Admin view for listing all users."""
-    users = User.objects.all().order_by("-date_joined")
+def admin_user_list(request: HttpRequest) -> HttpResponse:
+    """View for displaying all users to an admin."""
+    users = User.objects.all().select_related('profile').order_by('-is_staff', 'username')

-    context = {"users": users}
+    context = {
+        'users': users,
+    }

-    if request.htmx:
-        return render(request, "users/partials/admin_user_list.html", context)
-    return render(request, "users/admin_user_list.html", context)
+    return render(request, 'users/admin_user_list.html', context)


 @user_passes_test(is_admin)
-def admin_user_create(request):
-    """Admin view for creating a new user."""
-    if request.method == "POST":
+def admin_user_create(request: HttpRequest) -> HttpResponse:
+    """Admin view for creating new users."""
+    if request.method == 'POST':
         form = AdminUserForm(request.POST)
         if form.is_valid():
             user = form.save()
-            messages.success(request, f"User {user.username} created successfully!")
-
-            if request.htmx:
-                return HttpResponse(
-                    '<div class="alert success">User created successfully.</div>',
-                    headers={"HX-Redirect": reverse("users:admin_user_list")},
-                )
-            return redirect("users:admin_user_list")
+            messages.success(request, f'User {user.username} created successfully.')
+            return redirect('users:admin_user_list')
     else:
         form = AdminUserForm()

-    context = {"form": form, "action": "Create"}
+    context = {
+        'form': form,
+        'action': 'Create',
+    }

-    if request.htmx:
-        return render(request, "users/partials/admin_user_form.html", context)
-    return render(request, "users/admin_user_form.html", context)
+    return render(request, 'users/admin_user_form.html', context)


 @user_passes_test(is_admin)
-def admin_user_edit(request, user_id):
-    """Admin view for editing a user."""
+def admin_user_edit(request: HttpRequest, user_id: int) -> HttpResponse:
+    """Admin view for editing users."""
     user_obj = get_object_or_404(User, id=user_id)

-    if request.method == "POST":
+    if request.method == 'POST':
         form = AdminUserForm(request.POST, instance=user_obj)
-        profile_form = UserProfileForm(
-            request.POST, request.FILES, instance=user_obj.profile
-        )
+        profile_form = UserProfileForm(request.POST, instance=user_obj.profile)

         if form.is_valid() and profile_form.is_valid():
             form.save()
             profile_form.save()
-            messages.success(request, f"User {user_obj.username} updated successfully!")
-
-            if request.htmx:
-                return HttpResponse(
-                    '<div class="alert success">User updated successfully.</div>',
-                    headers={"HX-Redirect": reverse("users:admin_user_list")},
-                )
-            return redirect("users:admin_user_list")
+            messages.success(request, f'User {user_obj.username} updated successfully.')
+            return redirect('users:admin_user_list')
     else:
         form = AdminUserForm(instance=user_obj)
         profile_form = UserProfileForm(instance=user_obj.profile)

     context = {
-        "form": form,
-        "profile_form": profile_form,
-        "user_obj": user_obj,
-        "action": "Update",
+        'form': form,
+        'profile_form': profile_form,
+        'user_obj': user_obj,
+        'action': 'Edit',
     }

-    if request.htmx:
-        return render(request, "users/partials/admin_user_form.html", context)
-    return render(request, "users/admin_user_form.html", context)
+    return render(request, 'users/admin_user_form.html', context)


 @user_passes_test(is_admin)
-def admin_user_delete(request, user_id):
-    """Admin view for deleting a user."""
+def admin_user_delete(request: HttpRequest, user_id: int) -> HttpResponse:
+    """Admin view for deleting users."""
     user_obj = get_object_or_404(User, id=user_id)

-    # Prevent admins from deleting themselves
-    if user_obj == request.user:
-        messages.error(request, "You cannot delete your own account!")
-        return redirect("users:admin_user_list")
-
-    if request.method == "POST":
+    if request.method == 'POST':
         username = user_obj.username
         user_obj.delete()
-        messages.success(request, f"User {username} deleted successfully!")
-
-        if request.htmx:
-            users = User.objects.all().order_by("-date_joined")
-            html = render_to_string(
-                "users/partials/admin_user_list.html", {"users": users}
-            )
-            return HttpResponse(html)
-        return redirect("users:admin_user_list")
+        messages.success(request, f'User {username} deleted successfully.')
+        return redirect('users:admin_user_list')

-    context = {"user_obj": user_obj}
+    context = {
+        'user_obj': user_obj,
+    }

     if request.htmx:
-        return render(request, "users/partials/admin_user_delete_confirm.html", context)
-    return render(request, "users/admin_user_delete.html", context)
+        return render(request, 'users/partials/admin_user_delete_confirm.html', context)
+    return render(request, 'users/admin_user_delete.html', context)

```

**Objective:** Ensure the user profile model has a proper relationship with the responsibility table, the profile view retrieves and provides overdue records in context, the overdue_count action table is properly positioned in the profile view, the table shows relevant information about overdue items, the table UI follows project design standards and is responsive, and the implementation maintains WCAG 2.1 AA compliance. All changes must be properly tested.

**Source:**

- <https://github.com/enveng-group/dev_greenova/issues/88>
- <https://github.com/enveng-group/dev_greenova/pull/97>
- `.vscode/tasks.json`
- `greenova/users/templates/users/partials/profile_detail.html`
- `greenova/users/views.py`
- `logs/changed_files.log`
- `logs/conflict_analysis.log`
- `logs/diff_stats.log`
- `logs/repo_status.log`
- `logs/commit_history.log`
- `logs/diff.log`
- `logs/pre_merge_analysis.log`
- `logs/pre_merge/integration_v0.0.6.log`
- `greenova/tests/pre_merge.py`

**Expectations**: GitHub Copilot can delete and consolidate files where
multiple implementations are found and can be merged into a single file
globally. Always use `use context7` to lookup documentation from the context7
MCP server, which provides access to all project-specific configuration files
and standards. Additional resources such as the github, filesystem, JSON,
context7, sqlite, git, fetch, sequential-thinking, and docker MCP servers have
been activated and are available for use by GitHub Copilot.

**Instructions**:

1. Identify and remove unnecessary or outdated files, code, or documentation
   that no longer serves the project's objectives. Clearly define the task's
   scope to focus only on relevant elements flagged in pre-commit checks.
2. Organize project resources, including tools, code, and documentation, into a
   logical structure. Ensure naming conventions and folder hierarchies are
   consistent, making it easier to locate and work with files.
3. Create stub files (.pyi files) for internal modules that don't have proper
   type information.
4. Add a py.typed marker file to indicate these modules have type information
5. Refactor the code to address issues such as readability, maintainability,
   and technical debt. Implement clean coding practices and resolve any flagged
   issues in the pre-commit output, such as formatting or style violations.
6. Use automated tools like bandit, autopep8, mypy, eslint, djlint,
   markdownlint, ShellCheck, and pylint to enforce coding standards. Validate
   compliance with the project's guidelines and ensure all pre-commit checks
   pass without errors. Iterate running `pre-commit` to check for any remaining
   issues after each change. Do not use the command
   `pre-commit run --all-files`.
7. Ensure that the code is well-documented, with clear explanations of
   functions, classes, and modules. Use docstrings and comments to clarify
   complex logic or important decisions made during development.
8. Test the code thoroughly to ensure it works as intended and meets the
   project's requirements. Write unit tests and integration tests as needed in
   `greenova/tests/pre_merge.py` to cover the new functionality and any
   changes made. Run the tests using `pytest` or the appropriate testing
   framework for the project. Use `pytest --disable-warnings` to suppress
   warnings during testing. Ensure that the tests are comprehensive and cover
   all edge cases. Use `pytest --cov` to check code coverage and ensure that
   all critical paths are tested. Use `pytest --maxfail=1` to stop testing
   after the first failure, allowing for easier debugging. Use `pytest --tb=short`
   to get a shorter traceback output for easier reading. Use `pytest --pdb` to
   drop into the debugger on test failures, allowing for interactive debugging.
9. Review the code for any potential security vulnerabilities or performance
   issues. Use tools like bandit to scan for security vulnerabilities and
   address any findings. Optimize the code for performance where necessary,
   ensuring that it runs efficiently and does not introduce unnecessary
   overhead.
10. Iterate until resolved.
