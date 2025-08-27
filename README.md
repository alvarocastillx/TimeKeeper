# ⏳ Timekeeper

          
          

          
          

A **lightweight version control system** designed to help you track your project files.  
Think of it as a mini-Git: simple, visual, and educational — perfect for understanding the core of version control.

---

## 🎯 Features

- ✅ Initialize a repository: `timekeeper init`  
- ✅ Stage all files: `timekeeper add_all`  
- ✅ Interactive CLI with colors and ASCII banners  
- ✅ Handles **Unicode files** flawlessly  
- ✅ Lightweight, simple, and fully understandable  
- ⚡ **Future:** commit history, revert, checkout  

---

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/timekeeper.gitc
cd timekeeper

# (Optional) Add to PATH for CLI usage
# Windows PowerShell:
setx PATH "$env:PATH;C:\path\to\timekeeper"
```

## 🔧 How it works
| Component  | Purpose |
|------------|---------|
| **Staging** | `add_all` indexes your files and creates **hashed blobs** in `.tkp/objects/`. |
| **Objects** | Stores the **content of each file** exactly once, identified by SHA-256 hash. |
| **Index** | Maps file paths to object hashes for reconstruction. |
| **Commit** | Records a snapshot of the project, referencing the staged objects (future feature). |

## 💡 Usage
| Command  | Function |
|------------|---------|
| **timekeeper init** | Initialize timekeeper repository |
| **timekeeper add_all** | Stage all changes |
| **timekeeper commit** | Commit last uncomitted stage |
| **timekeeper help** | Displays help menu |
| **(Developing...) timekeeper revert** | Revert files to last commit |

