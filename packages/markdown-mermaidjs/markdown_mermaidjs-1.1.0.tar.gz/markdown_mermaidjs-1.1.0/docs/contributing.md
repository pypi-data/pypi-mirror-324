### Step 1. Fork this repository to your GitHub

### Step 2. Clone the repository from your GitHub

```sh
git clone https://github.com/[YOUR GITHUB ACCOUNT]/markdown-mermaidjs.git
```

### Step 3. Add this repository to the remote in your local repository

```sh
git remote add upstream "https://github.com/Lee-W/markdown-mermaidjs"
```

You can pull the latest code in main branch through `git pull upstream main` afterward.

### Step 4. Check out a branch for your new feature

```sh
git checkout -b [YOUR FEATURE]
```

### Step 5. Install prerequisite

```sh
python -m pip install pipx
python -m pipx install uv invoke
python -m pipx ensurepath
```

* [pipx](https://github.com/pipxproject/pipx): for python tool management
* [uv](https://github.com/astral-sh/uv/): for dependency management
* [invoke](https://github.com/pyinvoke/invoke): for task management

#### Notes for Windows Developers

By default, the tasks leverage [pty](https://docs.python.org/3/library/pty.html) under the covers, which
does not support Windows. Either run this via WSL or pass --no-pty to commands that demand it.

### Step 6. Create your local Python virtual environment and install dependencies

```sh
inv env.init-dev
```

### Step 7. Work on your new feature
Note that this project follows [conventional-commit](https://www.conventionalcommits.org/en/v1.0.0/) and bumps version based on it. Use the following command to commit your changes.

```sh
inv git.commit
```

or on Windows (currently throws an error when run outside of cmd.exe):

```sh
inv git.commit --no-pty
```

### Step 8. Run test cases
Make sure all test cases pass.

```sh
inv test
```

or on Windows:

```sh
inv test --no-pty
```

### Step 9. Run test coverage
Check the test coverage and see where you can add test cases.

```sh
inv test.cov
```

### Step 10. Reformat source code

Format your code through `ruff`.

```sh
inv style.format
```

### Step 11. Run style check
Make sure your coding style passes all enforced linters.

```sh
inv style
```

### Step 12. Run security check

Ensure the packages installed are secure, and no server vulnerability is introduced

```sh
inv secure
```

or on Windows:

```sh
inv secure --no-pty
```

### Step 13. Create a Pull Request and celebrate 🎉
