# ⏳ Timekeeper

A **lightweight version control system**  that tracks your project through stages and commits. Designed to provide clear checkpoints during development and snapshots of stable versions, making it easy to manage and revert your work.

---

## 🎯 Features

- ✅ Initialize a repository: `timekeeper init`  
- ✅ Stage all files: `timekeeper add_all`
- ✅ Commit your tested checkpoint: `timekeeper commit`
- ✅ Recover old states of your project
- ✅ Interactive CLI with colors and ASCII banners  
- ✅ Handles **Unicode files** flawlessly  
- ✅ Lightweight, simple, and fully understandable  
- ⚡ **Future features:** blockchain to track commits 🔧 
- 🆘 Feedback is the most important thing! Feel free to help make TimeKeeper something useful!

---

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/alvarocastillx/timekeeper.git
cd timekeeper

# (Optional) Add to PATH for CLI usage
# Windows PowerShell:
setx PATH "$env:PATH;C:\path\to\timekeeper"
```

## 🔧 How it works
| Component  | Purpose |
|------------|---------|
| **Staging** | Indexes your files and stores them as hashed blobs in `.tkp/objects/`. Stages act as checkpoints during build stabilization, allowing you to revert your project to the last stage at any time. |
| **Objects** | Stores the **content of each file**, identified by SHA-256 hash. |
| **Index** | Maps file paths to object hashes for reconstruction. |
| **Commit** | Commit finalized stage — removes all stages and creates a clean project snapshot.  |
| **Reverts** | TimeKeeper lets you revert your project to last stage  (checkpoint) or commit whenever you want! PD: In the future it will let you decide a specific stage or commit 👁|


## 💡 Usage
| Command  | Purpose |
|------------|---------|
| **timekeeper init** | Initialize timekeeper repository |
| **timekeeper add_all** | Stage all changes |
| **timekeeper commit** | Commit last uncomitted stage |
| **timekeeper help** | Displays help menu |
| **timekeeper revert_stage** | Revert project to last stage |
| **timekeeper revert_commit** | Revert project to last commit |
| **timekeeper uninstall** | Removes Timekeeper from your project |



