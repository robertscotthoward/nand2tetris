"""
For each *.asm file in the code folder, assemble it into a *.hack file in the parent 08-Project6 folder.
"""
import re
import os


# Define the C-instruction patterns.
DATA = """
0    101010
1    111111
-1   111010
D    001100
A    110000
!D   001101
!A   110001
-D   001111
-A   110011
D+1  011111
A+1  110111
D-1  001110
A-1  110010
D+A  000010
D-A  010011
A-D  000111
D&A  000000
D|A  010101
""".strip()
DATA = [line.strip().split() for line in DATA.split("\n")]
DEST = ["", "M", "D", "MD", "A", "AM", "AD", "AMD"]
JUMP = ["", "JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP"]

# Predefined symbols of the Hack computer. We'll add more as we assemble the code.
SYMBOLS = """
R0,0
R1,1
R2,2
R3,3
R4,4
R5,5
R6,6
R7,7
R8,8
R9,9
R10,10
R11,11
R12,12
R13,13
R14,14
R15,15
SCREEN,16384
KBD,24576
SP,0
LCL,1
ARG,2
THIS,3
THAT,4
""".strip()

SYMBOLS = [line.strip().split(",") for line in SYMBOLS.split("\n")]




def readText(file):
    with open(file, "r") as f:
        return f.read()

def writeText(file, text):
    with open(file, "w") as f:
        f.write(text)




def assembleText(text):
    symbolTable = {}
    for symbol, address in SYMBOLS:
        symbolTable[symbol] = int(address)

    machineCode = []
    for line in text.split("\n"):
        line = line.strip()
        # Remove comments
        line = line.split("//")[0].strip()

        if not line:
            continue

        line = line.strip()


        # Each line will match some type of assembly pattern.
        # PATTERN: (label)
        if line.startswith("("):
            label = line[1:-1]
            address = symbolTable.get(label, None)
            if address is None:
                symbolTable[label] = len(machineCode)
            else:
                symbolTable[label] = address
            continue

        # PATTERN: @address
        if line.startswith("@"):
            address = line[1:]

            if address.isdigit():
                # @123
                address = int(address)
                machineCode.append(f"{address:016b}")
            else:
                # @label
                a = symbolTable.get(address, None)
                if a is None:
                    # The label was not defined yet, so we need to add it to the symbol table as a forward reference.
                    symbolTable[f'FORWARD_{len(machineCode)}'] = address
                    machineCode.append("") # And create a placeholder for the forward reference.
                else:
                    machineCode.append(f"{a:016b}")
            
            continue

        # PATTERN: dest=comp;jump
        match = re.match(r"^((?P<dest>\w+)=)?\s*((?P<comp>[^;]+))?\s*(;\s*(?P<jump>\w+))?$", line)  
        if match:
            dest, comp, jump = match.group('dest'), match.group('comp'), match.group('jump')
            comp = comp or ""
            jump = jump or ""

            A = 1 if "M" in comp else 0
            comp = comp.replace("M", "A")
            if comp:
                # Find index i in data where data[i][0] matches comp
                CCCCCC = None
                for (pattern, bits) in DATA:
                    if pattern == comp:
                        CCCCCC = bits
                        break
                if CCCCCC is None:
                    raise Exception(f"Unknown computation: {comp}")
            else:
                CCCCCC = "0000000"
            
            DDD = f"{DEST.index(dest) if dest else 0:03b}"
            JJJ = f"{JUMP.index(jump) if jump else 0:03b}"

            machineCode.append(f"111{A}{CCCCCC}{DDD}{JJJ}")
            continue

        raise Exception(f"Unknown instruction: {line}")

    # Undefined labels become instance variables and are defined in order as they appear from MEM[16].
    var = 16
    for k,v in symbolTable.copy().items():
        if k.startswith('FORWARD_'):
            x = symbolTable.get(v, None)
            if x is None:
                symbolTable[v] = var
                var += 1

    # Resolve forward references with their actual values.
    for k,v in symbolTable.items():
        if k.startswith('FORWARD_'):
            v = symbolTable.get(v, None)
            i = int(k.split('_')[1])
            machineCode[i] = f"{v:016b}"

    return machineCode




def assembleFile(asmFile, hackFile):
    text = readText(asmFile)
    machineCode = assembleText(text)
    writeText(hackFile, "\n".join(machineCode))
    return machineCode




def assembleAllFiles(asmFolder, hackFolder):
    # Get all files in the directory
    files = os.listdir(asmFolder)
    
    # Assemble each file
    for file in files:
        if file.endswith('.asm'):
            print("\n" + "="*50)
            print(f"Assembling {file}")
            asmFile = os.path.join(asmFolder, file)
            hackFile = os.path.join(hackFolder, file.replace('.asm', '.hack'))
            parsed = assembleFile(asmFile, hackFile)




if __name__ == "__main__":
    assembleAllFiles(r"code", r"..\08-Project6")
    