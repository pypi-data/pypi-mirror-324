[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.31.0...0.31.1)

### Fixes

- Fix type hinting incompatibility in Python 3.9. [96b29f5](https://github.com/callowayproject/bump-my-version/commit/96b29f5ff561586e5dfb2da6e51172930bb717bc)
    
  Refactor to use Pathlike type alias for path representation

  Unified path type handling across the codebase by introducing the `Pathlike` type alias (`Union[str, Path]`). This improves readability and consistency in path-related functions and methods, reducing redundancy. Updated corresponding type annotations, imports, and tests accordingly.
