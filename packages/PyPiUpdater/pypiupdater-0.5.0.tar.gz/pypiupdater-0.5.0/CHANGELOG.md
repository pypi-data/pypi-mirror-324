# Changelog

## 0.5.0: Rework (BREAKING CHANGE)
- Improved code consistency: return values are now always **lists** when containing multiple objects.
- **Simplified the package**: Removed the default waiting period for update checks.
  - It is now the **developer's responsibility** to decide when to check for updates. A separate independent function may be introduced later.
  - The last update check is still saved in the config and returned as a `time.time()` object.

---

## 0.4.0: Rework (BREAKING CHANGE)
- The log file is now a JSON file, allowing it to store multiple package names, versions, and last update timestamps.
- Some return values are now lists.

---

## 0.3.0: Rework (BREAKING CHANGE)
- Changed how program behaves

---

## 0.2.1: CI/CD pipeline
- Added auto tagging and publishing

---

## 0.0.1: Project Initiation
- First working version
- ATM terminal promt to accept or deny update
- More to come soon
