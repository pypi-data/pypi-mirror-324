# Orca Venus Driver

The **Orca Venus Driver** is used by **Orca** to run **Hamilton Venus** methods. This driver allows **Orca** to execute **Venus** methods and pass variables to them. If users want to pass variables from Orca to a Venus method, the method must use the **submethod library** provided in the `venus_submethod` folder.

## 📂 Submethod Library

The `venus_submethod` folder contains a **Hamilton submethod library** that enables Venus methods to retrieve variables from **Orca**.  Add/Remove this library into your method using Venus.

### 📌 Methods in the Submethod Library

#### `ORCA::Initialize(useDefaultValues)`
- **Purpose**: Initializes the variable retrieval system.
- **Parameters**:
  - `useDefaultValues` (Integer)
    - `0` → Retrieve values from Orca.
    - `1` → Use default values within the Venus method (allows methods to run locally without Orca).
- **Usage**:
  - If `useDefaultValues = 0`, variables will be injected by **Orca**.
  - If `useDefaultValues = 1`, `defaultValue` will be set to each variable instead.  Set this if you're running Venus locally and not using Orca at the moment.

#### `GetConfigProperty_Float(propertyName, defaultValue, value)`
#### `GetConfigProperty_String(propertyName, defaultValue, value)`
#### `GetConfigProperty_Integer(propertyName, defaultValue, value)`
- **Purpose**: Retrieve a value from Orca and assign it to a Venus variable.
- **Parameters**:
  - `propertyName` → The name of the property as set in the `params` key of the **Orca action**.
  - `defaultValue` → Used if `ORCA::Initialize(1)` was called.
  - `value` → The **Venus variable** that will receive the value (either injected by **Orca** or assigned the `defaultValue` if `useDefaultValues = 1`).

## 🔧 Installation

The **Orca Venus Driver** can be installed via **Orca’s driver installation command** or manually via **pip**:

```sh
pip install orca-driver-venus
```

## 🛠 Usage
To use the driver with Venus methods, make sure your venus method calls submethod function `ORCA::Initialize(0)` at the beginning and uses the `GetConfigProperty_*` methods to retrieve values dynamically from Orca.