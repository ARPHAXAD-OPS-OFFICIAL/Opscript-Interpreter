# OpScript

**OpScript** is a lightweight interpreted scripting language and execution environment developed under **ARPHA11 OPS**.

The project is designed around a simple, command-oriented syntax that provides basic programming constructs such as variables, user input, conditional logic, labels, jumps, shell commands, terminal colors, delays, random number generation, and simple data mapping.

OpScript is implemented in Python and is intended to provide a straightforward scripting environment without requiring a large runtime or external framework.

---

## Features

OpScript currently provides:

* **Text output** with `disp`
* **User input** with `userin`
* **Variables** using `%variable%` syntax
* **Conditional statements** with `ilit`
* **`else` / `endil` conditional blocks**
* **Labels** with `lbl`
* **Program jumps** with `jmp`
* **Random number generation** with `ran`
* **Shell command execution** with `sh`
* **Terminal color control** with `clor`
* **Execution delays** with `sleep`
* **Nested command execution** with `exec`
* **Randomized map generation** with `map`
* **Map value extraction** with `readmap`
* **Inline and single-line comments**
* Basic numeric and string comparisons

The interpreter preprocesses source code, removes comments and empty lines, indexes labels, and then executes the resulting instruction stream.

---

## Example

A basic OpScript program:

```opscript
disp ("Hello, world!")

userin %name%="What is your name?"

disp ("Hello %name%!")
```

Conditional logic can be written using `ilit`:

```opscript
userin %name%="What is your name?"

ilit %name% == jeff
    disp ("Hello jeff!")
else
    disp ("Hello %name%!")
endil
```

Variables are substituted using `%variable%` placeholders.

---

## Commands

### `disp`

Displays text to the terminal.

```opscript
disp ("Hello world!")
```

Variables can be embedded directly into the output:

```opscript
disp ("Hello %name%!")
```

---

### `userin`

Requests input from the user and stores the result in a variable.

```opscript
userin %name%="What is your name?"
```

The entered value is stored in `%name%`.

---

### `ran`

Generates a random integer within a specified range.

```opscript
ran (1)-(100) %number%
```

The generated value is stored in `%number%`.

---

### `ilit`

Performs a conditional comparison.

```opscript
ilit %number% > 50
    disp ("The number is greater than 50.")
endil
```

Supported comparison operators include:

```text
==
!=
>
<
>=
<=
```

The interpreter attempts numeric comparisons when both operands can be interpreted as numbers.

---

### `else`

Provides an alternative branch for an `ilit` block.

```opscript
ilit %name% == jeff
    disp ("Hello jeff!")
else
    disp ("You are not jeff.")
endil
```

---

### `lbl`

Creates a label that can be targeted by `jmp`.

```opscript
lbl (start)
```

Labels are indexed during preprocessing so that jump instructions can locate their destinations.

---

### `jmp`

Jumps execution to a previously defined label.

```opscript
jmp (start)
```

Example:

```opscript
lbl (loop)

disp ("Running...")

jmp (loop)
```

---

### `sh`

Executes shell commands through the host operating system.

```opscript
sh -a (clear) iferr (cls)
```

Multiple parenthesized commands can be supplied. The interpreter evaluates them and stops trying alternatives when a command succeeds.

> **Security notice:** `sh` executes commands on the host system. Do not execute untrusted OpScript source.

---

### `clor`

Changes the terminal's output color.

Supported colors currently include:

```text
RED
BLUE
YELLOW
PINK
ORANGE
DEFAULT
```

Example:

```opscript
clor BLUE
disp ("Blue text")
clor DEFAULT
```

The implementation uses ANSI terminal escape sequences for color output.

---

### `sleep`

Pauses execution for a specified number of seconds.

```opscript
sleep 1
```

Variables can also be evaluated as part of the delay value.

---

### `exec`

Executes multiple OpScript commands from a single line.

```opscript
exec (disp ("Hello")) (ran (1)-(10) %number%)
```

Each contained command is passed back through the interpreter for execution.

---

### `map`

Creates a randomized numeric map based on the supplied map contents.

```opscript
map 1 [          ]
```

The current implementation generates a string of random digits from `1` through `9` corresponding to the characters contained within the map.

---

### `readmap`

Reads a previously generated map and stores the sum of its numeric characters in a variable.

```opscript
readmap {1} %total%
```

The resulting value can then be accessed through `%total%`.

---

## Control Flow

OpScript programs are executed sequentially by the interpreter.

The interpreter maintains a program counter and uses labels and jumps to alter execution flow. Conditional blocks can skip forward to their corresponding `else` or `endil` statements when a condition fails.

A simple loop can therefore be constructed using `lbl` and `jmp`:

```opscript
lbl (loop)

disp ("This is a loop.")

jmp (loop)
```

---

## Example Program

The repository's interpreter includes an example demonstrating several features together, including:

* User input
* Variables
* Conditional statements
* Random number generation
* Labels
* Jumps
* Shell commands
* Terminal colors
* Nested execution
* Maps
* Delays

The included example implements a simple number-guessing game in which a random number between `1` and `100` is generated and the user receives "too high", "too low", or "correct" responses.

---

## Running

OpScript is currently implemented as a Python interpreter.

Run the interpreter with:

```bash
python3 oppy.py
```

The interpreter's example program is executed when the file is run directly.

---

## Project Structure

A minimal installation may consist of:

```text
.
├── oppy.py
└── README.md
```

`oppy.py` contains the `OpScriptInterpreter` implementation and example program.

---

## Project Status

OpScript is an actively developed project under **ARPHA11 OPS**.

The language and interpreter may change as development continues. Syntax, commands, behavior, and implementation details should therefore be considered subject to change.

---

## Philosophy

OpScript is built around a simple idea:

> **Make scripting feel direct, readable, and easy to experiment with.**

Rather than attempting to replace established programming languages, OpScript provides its own compact scripting model focused on straightforward commands and control flow.

---

## License

Copyright © 2026 **ARPHA11 OPS**

This project is licensed under the **BSD 2-Clause License**.

You may use, modify, and redistribute the software in accordance with the terms of the license.

### BSD 2-Clause License

```text
Copyright (c) 2026, ARPHA11 OPS
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```

---

## Copyright

**ARPHA11 OPS**
Copyright © 2026

Part of the **ARPHA11** software ecosystem.

---

## Author

Developed and maintained by **ARPHA11 OPS**.
