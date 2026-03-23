# 🚀 Frontend II Project - Environment Setup

This repository contains the initial configuration required for our projects. We will use a professional workflow that includes static code analysis, automatic formatting, and mandatory unit testing.

## 🛠️ Tools Used

- **ESLint:** Linter to find and fix problems in your JavaScript code.
- **Prettier:** Code formatter to maintain a consistent style.
- **Vitest:** Unit testing framework (similar to Jest but faster).
- **Husky & Lint-staged (Local Pre-commit):** Tools to _automatically_ validate code on your local machine before allowing a commit to be saved.
- **GitHub Actions:** Continuous Integration (CI) that automatically grades your Pull Requests.

## 📦 Installation Instructions
1. **Use this repository as a template** to create your project repo clicking in the **use this template** button.
2. Select **Create a new repository**.
3. As repository name use the following naming convention frontend2-projet-**project_name**, e.g. **frontend2-project-CESUN-page**.
4. **Clone the repository** to your local machine:

   ```bash
   git clone <REPOSITORY_URL>
   cd <REPOSITORY_NAME>
   ```

5. **Install Node.js dependencies**:

   ```bash
   npm install
   ```

6. **Activate local Pre-commit**:
   To ensure code validations run on your computer before pushing any changes, initialize Husky by running:
   ```bash
   git config core.hooksPath .husky
   npm run prepare
   ```
   _Note: This will create a hidden `.husky` folder that intercepts your git commands to review the code._

## 🚦 Mandatory Workflow

The `main` branch is protected by repository rules. **You cannot push directly to main.** You must follow this workflow for each task:

1. **Create a new branch** for your task or feature:

   ```bash
   git checkout -b feature/your-task-name
   ```

2. **Write your code and unit tests**.

3. **Manual Verification (Optional but recommended)**:
   Before committing, you can verify that everything is in order by running:
   - `npm run format` (To format your files)
   - `npm run lint` (To check for errors in your code)
   - `npm run test` (To run unit tests)

4. **Make your commit (Pre-commit intervention)**:

   ```bash
   git add .
   git commit -m "feat: add feature X"
   ```

   _🛑 Important! At this moment, Husky will pause the commit and run ESLint and Prettier locally only on the files you modified. If the code has syntax errors or bad formatting, the commit will be **rejected**. You must fix the errors and try committing again._

5. **Push your changes**:

   ```bash
   git push origin feature/your-task-name
   ```

6. **Open a Pull Request (PR)** on GitHub towards the `main` branch. The "Grader" (GitHub Actions) will run all tests again in the cloud. If everything is green, you will be ready to Merge your work.

---

## 🔒 Administrator Guide: Protecting the `main` Branch

To enforce the professional workflow described above, the repository administrator must configure the following Branch Protection Rules in GitHub. This ensures no one (not even the administrator) can bypass the quality checks.

1. Go to your repository on GitHub.
2. Click on **Settings** (the gear icon at the top).
3. On the left sidebar, click on **Branches**.
4. Click the **Add branch protection rule** button.
5. In the **Branch name pattern** field, type exactly: `main`.
6. Enable the following critical settings:
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
      - ✅ *Inside this option, also check:* **Require branches to be up to date before merging**
      - 🔍 *In the search bar for status checks, type and select:* **`evaluacion`** (This matches the exact name of the job in your GitHub Actions YAML file).
   - ✅ **Do not allow bypassing the above settings** (This locks the repository down completely, enforcing the rules for all users, including admins).
7. Scroll to the bottom and click **Create** (or **Save changes**).

Your repository is now secured! All code must pass the `evaluacion` CI pipeline via a Pull Request before being integrated into `main`.

---
## 🚑 Troubleshooting

**1. "My commit was rejected by Husky/Lint-staged. What do I do?"**
Read the error output in your terminal. Usually, it's a formatting issue or an unused variable.
*Fix:* Run `npm run format` and `npm run lint --fix` (or your configured script) to let the tools attempt to fix the issues automatically. Then, run `git add .` and try your commit again.

**2. "The tests passed on my computer, but the GitHub Action (evaluacion) failed."**
Husky only checks the files you *staged* for that specific commit. GitHub Actions evaluates the *entire* project from scratch in an isolated environment.
*Fix:* Always run `npm run test` locally before pushing to ensure no other parts of the application were broken by your changes.

**3. "I am getting a 'node_modules' or caching error in GitHub Actions."**
Sometimes CI runners get stuck with outdated packages. If you recently added a new dependency, ensure your `package-lock.json` was committed and pushed alongside your `package.json`.

**4. "Husky not working"**
Make sure you have run `npm install` after cloning the repository. Husky hooks are installed during the `postinstall` script.

You can also manually install Husky by running `npx husky install` in the project root and verify with `ls -la .husky`., it should show the `pre-commit` file.

**5. "Cannot find module '@rollup/rollup-linux-x64-gnu'"**
This error usually occurs when there's a mismatch between the Node.js version used locally and the one used by the CI runner. Make sure you have the correct Node.js version installed locally and that your `package-lock.json` is up to date. You can try `rm -rf node_modules package-lock.json` and then `npm install` to regenerate it.

## Prueba de versionamiento automatico con release.
