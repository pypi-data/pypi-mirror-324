# VGLS/Vigilant Scanner

**vgls** is a Python-based CLI tool for monitoring file integrity, detecting changes, analyzing logs and identifying 
potential security threats. 

---

## 🚀 Features

- **System Integrity Monitoring**: Detect changes in file content, metadata, and structure. Monitor 
directories for unauthorized or suspicious changes (permissions, owner, etc).
- **Log Analysis** *(In Progress)*: Analyze logs for security threats and anomalies.

---

## 🛠 Installation

```bash
pip install vigilant-scanner
```

---

## 📋 Usage

1. **Initialize Snapshot**
   Create a snapshot of the current directory state and store metadata in the database:
   ```bash
   vgls integrity-init <directory>
   ```
   ![Alt Text](docs/media/init.gif)

2. **Scan and Compare**
   Scan the directory and compare results with the last snapshot:
   ```bash
   vgls integrity-scan <directory>
   ```
   ![Alt Text](docs/media/scan.gif)

3. **Update the Database**
   Update the database with the current state of the directory:
   ```bash
   vgls update <directory>
   ```
![Alt Text](docs/media/update.gif)

4. **Log analysis**
   Analyse all logs (all files with .log extension) in provided directory on matching with malicious patterns.
   ```shell
   vgls log-scan <directory>
   ```
   **Work is still in progress.** Mostly working on malicious signature collection that will be used here.
![Alt Text](docs/media/logger.png)
   

---

## ⚙️ How It Works

```bash
# Create database with the current state of a target directory
vgls integrity-init /var/www

# Perform a scan to detect changes
vgls integrity-scan /var/www

# Update the database after legitimate changes are made (deploy was conducted etc.)
vgls integrity-update /var/www
```

1. **Initialization (`init`)**
   - Scans a directory and stores metadata (file path, hash, size, permissions, etc.) in a SQLite database.

2. **Scanning and Comparison (`scan`)**
   - Scans the directory again and compares the current state with the stored metadata.
   - Outputs new, modified, and deleted files.

3. **Updating the Database (`update`)**
   - Updates the database to reflect the latest directory state.
   - Inserts new files, updates modified files, and removes deleted files.

---

## 📋 Requirements

- Python 3.10+

---

## 🛠 Development

To contribute or run the tool locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/ivpel/vigilant-scanner.git
   ```

2. Navigate to the project directory:
   ```bash
   cd vigilant-scanner
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests:
   ```bash
   pytest
   ```

---

## 📜 License

This project is licensed under the GNU General Public License v3 or later (GPLv3+). See the [LICENSE](LICENSE) file for details.

---

## 💬 Support

If you encounter any issues, feel free to open a ticket on the [GitHub Bug Tracker](https://github.com/ivpel/vigilant-scanner/issues).

---

## 🔗 Links

- **Homepage**: [Vigilant Scanner on GitHub](https://github.com/ivpel/vigilant-scanner)
- **Bug Tracker**: [Report Issues](https://github.com/ivpel/vigilant-scanner/issues)

