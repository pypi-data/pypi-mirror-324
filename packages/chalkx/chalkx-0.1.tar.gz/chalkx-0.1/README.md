# Chalk

**Chalk** is a simple Python package that allows you to change the color of your text in the terminal using ANSI escape codes. With this package, you can easily print colorful text to the command line, perfect for making your console outputs more vibrant.

## Installation

You can install Chalk from PyPI using `pip`:

```bash
pip install chalk
```

## Usage

### Basic Example

Use the `chalk` function to color your text. The `color` parameter accepts standard color names as strings, or you can use the `COLORS` dictionary.

```python
from chalk import chalk, COLORS

# Simple usage with color name
print(chalk("This is red text", color="red"))
print(chalk("This is blue text", color="blue"))

# Using the COLORS dictionary
print(chalk("This is green text", color=COLORS.green))
print(chalk("This is yellow text", color=COLORS.yellow))
```

### Erasing Colors

You can also remove the color formatting from text by using the `erase=True` option. This strips any previous color codes from the text and shows the raw output.

```python
from chalk import chalk, COLORS

# Using erase to clean up the colors
colored_text = chalk("This is red text", color=COLORS.red)
print(colored_text)  # Shows red text
print(chalk(colored_text, erase=True))  # Erases the color, showing plain text
```

### Available Colors

Chalk supports the following colors:

- `"black"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, `"white"`
- Bright variations: `"bred"`, `"bgreen"`, `"byellow"`, `"bblue"`, `"bmagenta"`, `"bcyan"`, `"bwhite"`
- Grayscale: `"grey"`, `"gray"`

These colors can be passed as strings or accessed via the `COLORS` dictionary.

```python
# Using colors as strings
print(chalk("This is black text", color="black"))

# Using colors from the COLORS dictionary
print(chalk("This is cyan text", color=COLORS.cyan))
```

## Contributing

Feel free to open issues or submit pull requests. All contributions are welcome!

## License

MIT License. See LICENSE file for details.