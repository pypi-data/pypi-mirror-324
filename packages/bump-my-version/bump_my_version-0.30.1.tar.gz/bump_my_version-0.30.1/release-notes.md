[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.30.0...0.30.1)

### Fixes

- Fixing issues with 3.9 compatibility. [cd2b193](https://github.com/callowayproject/bump-my-version/commit/cd2b193412b87ef47c3b9129b527eaa826429270)
    
- Fixes #284. Add UTF-8 encoding to subprocess.run in run_command. [6c856b6](https://github.com/callowayproject/bump-my-version/commit/6c856b6db40300de2ba0583bbd092b25d01b0004)
    
  Explicitly set the encoding to "utf-8" in the subprocess.run call to ensure consistent handling of command output. This prevents potential encoding-related issues when processing command results.
