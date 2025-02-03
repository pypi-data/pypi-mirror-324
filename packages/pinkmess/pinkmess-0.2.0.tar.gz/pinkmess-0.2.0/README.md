# Pinkmess 🌸

Pinkmess is a note-taking CLI tool that allows you to manage collections of markdown notes with AI-powered metadata generation capabilities.

It is a completely opinionated PKMS terminal manager for lazy people just like me.

> [!WARNING]
>
> This is a personal tool that I built for my own note-taking workflow and experimentation with AI-powered note organization. It is **NOT** intended for production use and comes with several important caveats:
>
> - **No Stability Guarantees**: The API and CLI interface may change at any time without warning
> - **Limited Testing**: The code has not been extensively tested beyond my personal use cases
> - **Security Considerations**: The tool hasn't undergone security auditing
> - **Dependencies**: Relies on specific versions of external libraries that may become outdated
> - **Performance**: Not optimized for large-scale note collections
> - **Documentation**: May be incomplete or outdated
>

## 📥 Installation

```bash
pip install pinkmess
```

Or install the latest version from the repository:

```bash
$ pip install git+https://github.com/leodiegues/pinkmess.git
```

## 🚀 Quick Start

Requirements:

- Python 3.10+
- OpenAI API key
- Text editor (defaults to nvim)

1. Set your OpenAI API key:

![Set your OpenAI API key](./docs/assets/gifs/quickstart/01-set-openai-api-key.gif)

2. Create and set a collection:

![Create and set a collection](./docs/assets/gifs/quickstart/02-create-and-set-collection.gif)

3. Create and edit a note:

![Create and edit a note](./docs/assets/gifs/quickstart/03-create-and-edit-note.gif)

4. Generate metadata:

![Generate metadata](./docs/assets/gifs/quickstart/04-generate-metadata.gif)

## 🏗️ Basic Structure

The CLI is organized into three main command groups:

- `collection`: Manages note collections
- `note`: Handles individual notes
- `config`: Manages application configuration

## 📁 Collection Commands

### Create a Collection
```bash
pinkmess collection create PATH [--name NAME] [--llm-model MODEL] [--llm-settings SETTINGS]
```
Creates a new collection at the specified path.

Example:
```bash
pinkmess collection create ~/notes --name personal
```

### Set Current Collection
```bash
pinkmess collection set NAME
```
Sets the active collection by its name.

Example:
```bash
pinkmess collection set personal
```

### List Collections
```bash
pinkmess collection list
# or
pinkmess collection ls
```
Shows all registered collections.

### Show Current Collection
```bash
pinkmess collection current
```
Displays the currently active collection.

### Remove Collection
```bash
pinkmess collection remove NAME
# or
pinkmess collection rm NAME
```
Removes a collection from the registry.

Example:
```bash
pinkmess collection remove personal
```

### Open Collection
```bash
pinkmess collection open [--name NAME]
```
Opens the specified collection (or current collection if no name provided) in your configured editor.

Example:
```bash
# Open current collection
pinkmess collection open

# Open a specific collection
pinkmess collection open --name personal
```

### Show Collection Stats
```bash
pinkmess collection stats
```
Displays statistics about the current collection (number of notes, creation date, last modification).

## 📝 Note Commands

### Create Note
```bash
pinkmess note create
```
Creates a new empty note in the current collection with a timestamp-based filename.

### Edit Note
```bash
pinkmess note edit [--path PATH]
```
Opens the specified note (or last created note) in your configured editor.

### Generate Metadata
```bash
pinkmess note generate-metadata [--path PATH] [--key {summary|tags}]
```
Generates AI-powered metadata for a note.

Examples:
```bash
# Generate summary for the last created note
pinkmess note generate-metadata --key summary

# Generate tags for a specific note
pinkmess note generate-metadata --path ~/notes/20230815123456.md --key tags
```

### Duplicate Note
```bash
pinkmess note duplicate [--path PATH]
```
Creates a copy of the specified note (or last created note) with a new timestamp-based filename in the current collection.

Example:
```bash
# Duplicate the last created note
pinkmess note duplicate

# Duplicate a specific note
pinkmess note duplicate --path ~/notes/20230815123456.md
```

### Show Last Created Note
```bash
pinkmess note last
```
Shows the path of the most recently created note.

## ⚙️ Config Commands

### Edit Configuration
```bash
pinkmess config edit
```
Opens the configuration file in your default editor.

### Show Configuration
```bash
pinkmess config show
```
Displays the current configuration in JSON format.

### Set Environment Variable
```bash
pinkmess config set-env KEY VALUE
```
Sets an environment variable in the .env file.

Example:
```bash
pinkmess config set-env OPENAI_API_KEY your_api_key_here
```

## 🛠️ Configuration Details

The configuration is stored in TOML format at the user config directory:
- Linux: `~/.config/pinkmess/config.toml`
- macOS: `~/Library/Application Support/pinkmess/config.toml`
- Windows: `%LOCALAPPDATA%\pinkmess\config.toml`

Key configuration options include:
- Collections list
- Current collection index
- Default LLM model
- LLM settings
- Editor preference

Environment variables are stored in a `.env` file in the same directory.

## 🔄 Typical Workflow

1. Create a new collection:
```bash
pinkmess collection create ~/notes/work --name work
```

2. Set it as current:
```bash
pinkmess collection set work
```

3. Create a new note:
```bash
pinkmess note create
```

4. Edit the note:
```bash
pinkmess note edit
```

5. Generate metadata:
```bash
pinkmess note generate-metadata --key summary
pinkmess note generate-metadata --key tags
```

## 📜 License

The project is licensed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) license.

---

Happy note-taking! 🌸
