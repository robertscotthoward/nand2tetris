import re
import os
from tools import *



from pyparsing import (
    Word, alphas, alphanums, nums, 
    Literal, Group, Optional, 
    LineEnd, SkipTo, OneOrMore,
    ParseException
)




def getParser():
    """
    Create a parser for Hack assembly language patterns:
    - LABEL: '(' + NAME + ')'
    - ADDRESS: '@' (NAME | INTEGER)
    """
    # Define comment pattern to skip
    COMMENT = Literal("//") + SkipTo(LineEnd())
    # Define basic elements
    NAME = Word(alphas + '_', alphas + alphanums + '_').setParseAction(lambda t: t[0])
    INTEGER = Word(nums).setParseAction(lambda t: t[0])
    # Skip comments
    NAME.ignore(COMMENT)
    INTEGER.ignore(COMMENT)
    
    # Define patterns
    LABEL = Group(Literal('(') + NAME + Literal(')'))
    ADDRESS = Group(Literal('@') + (NAME | INTEGER))
    
    # Define a line as either a LABEL or ADDRESS, followed by optional whitespace and end of line
    LINE = (LABEL | ADDRESS) + Optional(SkipTo(LineEnd()))
    
    # Create parser for multiple lines
    PARSER = OneOrMore(LINE)
    
    return PARSER




def parse_assembly_file(file_path):
    parser = getParser()
    results = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Parse the entire content
        parsed = parser.parseString(content)
        
        # Process results
        line_number = 1
        for item in parsed:
            if len(item) == 3 and item[0] == '(' and item[2] == ')':
                # This is a LABEL
                results.append({
                    'type': 'LABEL',
                    'value': item[1],
                    'line_number': line_number
                })
            elif len(item) == 2 and item[0] == '@':
                # This is an ADDRESS
                results.append({
                    'type': 'ADDRESS',
                    'value': item[1],
                    'line_number': line_number
                })
            line_number += 1
            
    except ParseException as e:
        print(f"Parse error at line {e.lineno}, col {e.col}: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error parsing file: {e}")
    
    return results





def parse_assembly_text(text):
    """
    Parse assembly text and return structured data.
    
    Args:
        text (str): Assembly code as string
        
    Returns:
        list: List of parsed elements
    """
    parser = getParser()
    results = []
    
    try:
        parsed = parser.parseString(text)
        
        line_number = 1
        for item in parsed:
            if len(item) == 3 and item[0] == '(' and item[2] == ')':
                # This is a LABEL
                results.append({
                    'type': 'LABEL',
                    'value': item[1],
                    'line_number': line_number
                })
            elif len(item) == 2 and item[0] == '@':
                # This is an ADDRESS
                results.append({
                    'type': 'ADDRESS',
                    'value': item[1],
                    'line_number': line_number
                })
            line_number += 1
            
    except ParseException as e:
        print(f"Parse error at line {e.lineno}, col {e.col}: {e}")
    except Exception as e:
        print(f"Error parsing text: {e}")
    
    return results




def assembleAllFiles(folder):
    """
    Assemble all files in the given directory.
    
    Args:
        file_path (str): Path to the directory containing assembly files
    """
    # Get all files in the directory
    files = os.listdir(folder)
    
    # Assemble each file
    for file in files:
        if file.endswith('.asm'):
            print("\n" + "="*50 + "\n")
            print(f"Assembling {file}")
            parsed = parse_assembly_file(os.path.join(folder, file))
            print(parsed)




# Example usage and testing
if __name__ == "__main__":
    assembleAllFiles(r"D:\github\nand2tetris\08-assembler\code")
    