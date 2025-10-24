# Library Structure Documentation

This document describes the refactored library structure for the MockupKost application.

## Library Files Created

### 1. `search_utils.py` - Search Functionality Library
**Purpose**: Handles all search-related functionality for kosan search and highlighting.

**Key Classes**:
- `SearchManager`: Manages search operations and kosan highlighting

**Key Methods**:
- `search_kosan(search_input)`: Search for kosan based on input and highlight on map
- `clear_search(search_input)`: Clear search and show all kosans
- `highlight_searched_kosan(kosan_name)`: Highlight specific kosan path on the map

### 2. `ui_components.py` - UI Components Library
**Purpose**: Manages all UI components including kosan cards and scroll container management.

**Key Classes**:
- `UIComponents`: Handles UI component creation and management

**Key Methods**:
- `create_search_ui(search_kosan_func, clear_search_func)`: Create search input and buttons UI
- `update_kosan_cards_filtered(graph, search_term)`: Update kosan cards showing only filtered results
- `update_kosan_cards(graph)`: Update kosan cards with all kosans
- `create_navigation_ui(...)`: Create navigation controls UI

### 3. `map_navigation.py` - Map Navigation Library
**Purpose**: Handles map navigation including zoom, move, and reset view functions.

**Key Classes**:
- `MapNavigation`: Manages map navigation operations

**Key Methods**:
- `reset_view()`: Reset the map view to initial state
- `zoom_view(factor)`: Zoom the map view by the given factor
- `move_view(dx, dy)`: Move the map view by the given delta values
- `set_initial_view_limits()`: Set the initial view limits for reset functionality

### 4. `area_management.py` - Area Management Library
**Purpose**: Manages loading different area graphs and area data.

**Key Classes**:
- `AreaManager`: Handles area loading and management

**Key Methods**:
- `load_area_graph(area_name)`: Load graph for the specified area
- `get_area_data()`: Get all area configuration data
- `get_current_area()`: Get current area information

## Refactored Main File

### `frontshots_refactored.py`
The main application file has been refactored to use the new library structure:

- **Imports**: All necessary libraries are imported at the top
- **State Management**: Global variables for current_graph and view_state
- **Component Initialization**: Each library component is initialized with proper dependencies
- **Function Wiring**: All functions are properly wired together to maintain functionality

## Benefits of This Structure

1. **Separation of Concerns**: Each library handles a specific aspect of the application
2. **Maintainability**: Code is organized into logical modules
3. **Reusability**: Library components can be reused in other projects
4. **Testability**: Each library can be tested independently
5. **Readability**: The main file is cleaner and easier to understand

## Usage

To use the refactored version:

1. Ensure all library files are in the same directory as the main file
2. Run `frontshots_refactored.py` instead of the original `frontshots.py`
3. The application will function identically to the original version

## Dependencies

- `nicegui`: UI framework
- `networkx`: Graph operations
- `matplotlib`: Plotting
- `backshots`: Custom graph operations (existing file)

All dependencies remain the same as the original application.
