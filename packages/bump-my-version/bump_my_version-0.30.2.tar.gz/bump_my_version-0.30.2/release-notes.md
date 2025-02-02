[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.30.1...0.30.2)

### Fixes

- Fix #388 - `python3.8` type hint compatibility. [5744f86](https://github.com/callowayproject/bump-my-version/commit/5744f86e8d5ff21e39d6e307b6bb26c70591c5e0)
    
  This should address the following error when running `bump-my-version`
  in a `python3.8` environment:

  ```
      def is_subpath(parent: Path | str, path: Path | str) -> bool:
  **typeerror:** unsupported operand type(s) for |: 'type' and 'type'

### Other

- [pre-commit.ci] pre-commit autoupdate. [ea3267a](https://github.com/callowayproject/bump-my-version/commit/ea3267a9114182f1ea9299ac468fc65a379005f1)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.9.2 → v0.9.3](https://github.com/astral-sh/ruff-pre-commit/compare/v0.9.2...v0.9.3)
