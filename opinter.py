import random
import re
import os
import sys
import time

class OpScriptInterpreter:
    def __init__(self, code):
        self.raw_code = code
        self.lines = []
        self.variables = {}
        self.labels = {}
        self.pc = 0  # Program counter

    def preprocess(self):
        """Cleans source blocks and maps line numbers to labels."""
        # Strip out the file header/source block markers if included in the string
        cleaned_text = re.sub(r'\', '', self.raw_code)
        
        # Split into lines and strip whitespace
        raw_lines = cleaned_text.splitlines()
        
        for line in raw_lines:
            line = line.strip()
            # Ignore empty lines and single-line comments
            if not line or line.startswith("//"):
                continue
            # Handle inline comments
            if "//" in line:
                line = line.split("//")[0].strip()
            self.lines.append(line)

        # Pre-pass to scan labels for jmp targets
        for idx, line in enumerate(self.lines):
            if line.startswith("lbl"):
                match = re.search(r'lbl\s*\((.*?)\)', line)
                if match:
                    label_name = match.group(1).strip()
                    self.labels[label_name] = idx

    def evaluate_vars(self, text):
        """Replaces %var% placeholders with their stored values."""
        def replace(match):
            var_name = match.group(1)
            return str(self.variables.get(var_name, f"%{var_name}%"))
        return re.sub(r'%([^%]+)%', replace, text)

    def eval_condition(self, condition_str):
        """Evaluates basic OpScript comparison logic."""
        condition_str = self.evaluate_vars(condition_str)
        
        # Parse comparison operators
        for op in ['==', '!=', '>=', '<=', '>', '<']:
            if op in condition_str:
                left, right = condition_str.split(op, 1)
                left, right = left.strip(), right.strip()
                
                # Attempt numeric evaluation if possible
                try:
                    left_val = float(left)
                    right_val = float(right)
                except ValueError:
                    left_val, right_val = left, right
                
                if op == '==': return left_val == right_val
                if op == '!=': return left_val != right_val
                if op == '>':  return left_val > right_val
                if op == '<':  return left_val < right_val
                if op == '>=': return left_val >= right_val
                if op == '<=': return left_val <= right_val
        return False

    def execute_line(self, line):
        """Executes a single line of OpScript."""
        line = line.strip()
        
        # --- DISP ---
        if line.startswith("disp"):
            match = re.search(r'disp\s*\((.*)\)', line)
            if match:
                content = match.group(1).strip().strip('"')
                print(self.evaluate_vars(content))

        # --- USERIN ---
        elif line.startswith("userin"):
            match = re.search(r'userin\s*%([^%]+)%\s*=\s*"(.*)"', line)
            if match:
                var_name, prompt = match.groups()
                user_val = input(self.evaluate_vars(prompt) + " ")
                self.variables[var_name] = user_val

        # --- RAN ---
        elif line.startswith("ran"):
            match = re.search(r'ran\s*\((\d+)\)\s*-\s*\((\d+)\)\s*%([^%]+)%', line)
            if match:
                low, high, var_name = match.groups()
                self.variables[var_name] = str(random.randint(int(low), int(high)))

        # --- SH (Shell command) ---
        elif line.startswith("sh"):
            # Syntax: sh -flags (command) iferr (fallback)
            args = re.findall(r'\((.*?)\)', line)
            for cmd in args:
                cmd_eval = self.evaluate_vars(cmd)
                ret = os.system(cmd_eval)
                if ret == 0:
                    break  # Command succeeded, don't execute 'iferr' fallbacks

        # --- CLOR ---
        elif line.startswith("clor"):
            color = line.split()[1].upper()
            colors = {
                "RED": "\033[91m",
                "BLUE": "\033[94m",
                "YELLOW": "\033[93m",
                "PINK": "\033[95m",
                "ORANGE": "\033[33m",
                "DEFAULT": "\033[0m"
            }
            sys.stdout.write(colors.get(color, "\033[0m"))

        # --- SLEEP ---
        elif line.startswith("sleep"):
            secs = float(self.evaluate_vars(line.split()[1]))
            time.sleep(secs)

        # --- EXEC ---
        elif line.startswith("exec"):
            sub_cmds = re.findall(r'\((.*?)\)', line)
            for sub in sub_cmds:
                self.execute_line(sub)

        # --- MAP ---
        elif line.startswith("map"):
            match = re.search(r'map\s+(\d+)\s*\[(.*?)\]', line)
            if match:
                map_id, content = match.groups()
                # Generate random numbers 1-9 replacing whitespace inside brackets
                random_string = "".join(str(random.randint(1, 9)) for _ in content)
                self.variables[f"__map_{map_id}"] = random_string
                print(f"[{random_string}]")

        # --- READMAP ---
        elif line.startswith("readmap"):
            match = re.search(r'readmap\s*\{(\d+)\}\s*%([^%]+)%', line)
            if match:
                map_id, var_name = match.groups()
                map_str = self.variables.get(f"__map_{map_id}", "0")
                # Add up map characters as integers
                total = sum(int(ch) for ch in map_str if ch.isdigit())
                self.variables[var_name] = str(total)

    def run(self):
        """Main execution loop handling jumps and logic flow."""
        self.preprocess()

        while self.pc < len(self.lines):
            line = self.lines[self.pc]

            # JMP handling
            if line.startswith("jmp"):
                match = re.search(r'jmp\s*\((.*?)\)', line)
                if match:
                    target_label = match.group(1).strip()
                    if target_label in self.labels:
                        self.pc = self.labels[target_label]
                        continue

            # ILIT (IF condition) handling
            elif line.startswith("ilit"):
                condition_str = line[4:].strip()
                condition_passed = self.eval_condition(condition_str)

                if not condition_passed:
                    # Skip forward to matching 'else' or 'endil'
                    depth = 1
                    while self.pc + 1 < len(self.lines) and depth > 0:
                        self.pc += 1
                        nxt = self.lines[self.pc]
                        if nxt.startswith("ilit"):
                            depth += 1
                        elif nxt == "endil":
                            depth -= 1
                        elif nxt == "else" and depth == 1:
                            break
                    self.pc += 1
                    continue

            # Skip 'else' blocks if execution hit them normally from a successful 'ilit'
            elif line == "else":
                depth = 1
                while self.pc + 1 < len(self.lines) and depth > 0:
                    self.pc += 1
                    nxt = self.lines[self.pc]
                    if nxt.startswith("ilit"):
                        depth += 1
                    elif nxt == "endil":
                        depth -= 1
                self.pc += 1
                continue

            elif line == "endil" or line.startswith("lbl"):
                self.pc += 1
                continue

            # Execute normal command
            self.execute_line(line)
            self.pc += 1


# Example Usage:
if __name__ == "__main__":
    opscript_code = """
    disp ("hello world in opscript!")
    userin %variable1%="what is your name?"

    ilit %variable1% == jeff
        disp ("Hello jeff!")
    else 
        disp ("hello %variable1%!")
    endil

    ran (1)-(100) %var2%

    lbl (start_guess)

    disp ("GUESS GAME: GUESS THE NUMBER FROM 1-100")
    userin %answer%="NUMBER:"

    ilit %answer% > %var2%
        disp ("too big!")
        jmp (start_guess)
    endil

    ilit %answer% < %var2%
        disp ("too low")
        jmp (start_guess)
    endil

    ilit %answer% == %var2%
        disp ("correct!")
        jmp (next)
    endil

    lbl (next)
    sh -a (clear) iferr (cls) iferr (echo "sorry, your shell is not supported")
    clor BLUE
    exec (disp ("hello again")) (ran (1)-(29) %var3%) 

    map 1 [                                                          ]
    sleep 1
    map 2 [                                                                     ]

    readmap {1} %var4%
    readmap {2} %var5%

    disp (%var4%-%var5%)
    """

    interpreter = OpScriptInterpreter(opscript_code)
    interpreter.run()
