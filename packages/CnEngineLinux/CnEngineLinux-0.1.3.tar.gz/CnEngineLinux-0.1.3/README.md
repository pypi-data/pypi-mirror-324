# cn-engine v0.1.3

**Simple console-based protocol similar to HTTP**

cn-engine is a lightweight and easy-to-use protocol for console communication. It is mainly designed for simple communication between programs and includes three main protocols.

Created by **Rasmnout** (Member: David Machek)

---

## Programs in cn-engine

### 1. cn-server
Starts a server for one of the available protocols.

#### Usage:
```
cn-server <LISTEN IP>
```
- Starts the server on the specified IP address.

```
cn-server version
```
- Displays the program version.

### 2. cn-view
Used to display file content via the CN FILES protocol.

#### Usage:
```
cn-view <FILE>
```
- Displays the content of a file.

```
cn-view version
```
- Displays the program version.

### 3. cn-search
Searches for information in files or data (more details to be added later).

---

## Supported protocols

### 1. CN (basic and unencrypted)
- The first and main version of the protocol.
- Used for simple connections and text display.
- Runs on port **60000**.

### 2. CNSS (CN SSL SECURITY)
- An extended version of the CN protocol with SSL encryption support.
- Supports input data and secure communication.
- Runs on port **61000**.

### 3. CNF (CN FILES)
- Used to display file content.
- Runs on port **62000**.

---

## CN Programming Language

CN is a programming language for creating pages with CN.

### Elements:
- **BUTTON** - Creates a button
- **INPUT** - Creates an input field
- **TEXT** - Creates a text element
- **TEXTAREA** - Creates a larger text area for multi-line input
- **BACKGROUND** - Sets the background color
- **TITLE** - Sets the page title

### Attributes:
- **placex** - Horizontal placement
- **placey** - Vertical placement
- **backcolor** - Background color
- **fontcolor** - Font color
- **border** - Border around the element
- **tawidth** - Text area width
- **taheight** - Text area height

### Example:

#### Text with red font color, white background, centered with a border:
```
TEXT."Hello, Client!"<backcolor:WHITE fontcolor:RED placex:CENTER placey:CENTER border:TRUE>
```

#### Button with white font color, black background at x:60, y:30 without a border:
```
BUTTON."This is a Button!"<backcolor:BLACK fontcolor:#FFFFFF placex:60 placey:30 border:FALSE>
```

#### Input field with red font color, white background, centered with a border:
```
INPUT<backcolor:WHITE fontcolor:RED placex:CENTER placey:CENTER border:TRUE>
```

#### Textarea with red font color, white background, centered, without a border, width 50, height 50:
```
TEXTAREA<backcolor:WHITE fontcolor:RED placex:CENTER placey:CENTER tawidth:50 taheight:50>
```

#### Background color set to red:
```
BACKGROUND<backcolor:RED>
```

#### Title set to "CN Example" with red font color:
```
TITLE."CN Example"<fontcolor:RED>
```

---

## Installation

To install cn-engine using pip, run:
```
pip install cn-engine
```

1. Download the binary files or source code.
2. Run the corresponding programs as needed.
3. Use the appropriate protocol for communication.

---

## Example usage

Starting the server on IP **192.168.1.100**:
```
cn-server 192.168.1.100
```

Displaying file content:
```
cn-view data.txt
```

---

**Rasmnout | David Machek**

