import re
import os
import time
import cProfile
import pstats
from concurrent.futures import ThreadPoolExecutor

def tokenize(code, language):
    patterns = []
    if language.lower() == 'basic':
        patterns = [
            ('COMMENT', r'(\'.*|\bREM\s.*)'),
            ('KEYWORD', r'\b(AND|OR|NOT|REM|LET|IF|THEN|ELSE|ELSEIF|ENDIF|GOTO|GOSUB|RETURN|FOR|TO|STEP|NEXT|WHILE|WEND|DO|LOOP|EXIT|SELECT|CASE|ENDSELECT|ENDCASE|DIM|AS|FUNCTION|ENDFUNCTION|SUB|ENDSUB|PRINT|INPUT|READ|DATA|RESTORE|GOTO|ON|ERROR|RESUME|RESUME_NEXT|STOP|END|CONST|INCLUDE)\b'),
            ('LITERAL', r'("[^"]*"|\b\d+(\.\d+)?\b)'),
            ('OPERATOR', r'(\+|-|\*|/|\^|=|<|>|<=|>=|<>|MOD|AND|OR|NOT)'),
            ('SEPARATOR', r'[\(\)\[\]{},:;\.]'),
            ('IDENTIFIER', r'[a-zA-Z_]\w*'),
        ]
    elif language.lower() == 'python':
        patterns = [
            ('KEYWORD', r'\b(and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b'),
            ('LITERAL', r'(".*?"|\'.*?\'|""".*?"""|\'\'\'.*?\'\'\'|r".*?"|r\'.*?\'|\b\d+(\.\d+)?([eE][+-]?\d+)?\b|\b0[xX][0-9a-fA-F]+\b|\b0[oO][0-7]+\b|\b0[bB][01]+\b)'),
            ('OPERATOR', r'(\+|-|\*|/|//|%|\*\*|&|\||\^|~|<<|>>|<|>|<=|>=|==|!=|=|\+=|-=|\*=|/=|//=|%=|\*\*=|&=|\|=|\^=|<<=|>>=)'),
            ('SEPARATOR', r'[\(\)\[\]{},:;.]'),
            ('COMMENT', r'#.*'),
            ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
        ]
    elif language.lower() == 'sql':
        patterns = [
            ('COMMENT', r'--.*'),
            ('KEYWORD', r'\b(SELECT|FROM|WHERE|AND|OR|NOT|INSERT|INTO|VALUES|UPDATE|SET|DELETE|CREATE|TABLE|DROP|ALTER|ADD|PRIMARY|KEY|FOREIGN|REFERENCES|INDEX|ASC|DESC)\b'),
            ('LITERAL', r'(".*?"|\'.*?\')'),
            ('OPERATOR', r'(\+|-|\*|/|%|=|!=|<|>|<=|>=|AND|OR)'),
            ('SEPARATOR', r'[\(\)\[\]{},:;.]'),
            ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
        ]

    tokens = []
    position = 0
    while position < len(code):
        match = None
        for token_type, pattern in patterns:
            regex = re.compile(pattern, re.IGNORECASE)
            match = regex.match(code, position)
            if match:
                value = match.group(0)
                tokens.append((token_type, value))
                position = match.end()
                break
        if not match:
            tokens.append(('OTHER', code[position]))
            position += 1
    return tokens

def generate_html(tokens, language):
    color_map = {
        'KEYWORD': '#56E1FF',      # Blue
        'IDENTIFIER': '#ffffff',   # White
        'OPERATOR': '#FFA800',     # Orange
        'LITERAL': '#23FF55',      # Green
        'SEPARATOR': '#FF295D',    # Red
        'COMMENT': '#9256FF',      # Purple
        'OTHER': '#212529',        # Black
    }

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Syntax Highlighter</title>
    <style>
        body { font-family: 'Inter', monospace; background-color: #3c3c3c; }
        h1, h2 { text-align: center; color: #ffffff; }
        pre { margin: auto; width: 75%; padding: 20px; border-radius: 1.125rem; background: linear-gradient(68deg, #010101 0%, #232323 100%); box-shadow: 0px 0px 0px 1px rgba(165, 165, 165, 0.04), -9px 9px 9px -0.5px rgba(0, 0, 0, 0.04), -18px -18px 18px -1.5px rgba(0, 0, 0, 0.08), -37px 37px 37px -3px rgba(0, 0, 0, 0.16), -75px 75px 75px -6px rgba(0, 0, 0, 0.24), -150px 150px 150px -12px rgba(0, 0, 0, 0.48);}
        .color-guide { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; padding: 20px; background-color: #010101; margin: 20px auto; max-width: 800px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .color-item { padding: 15px; border-radius: 5px; color: black; font-weight: bold; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        .token { display: inline; }
'''

    for token_type, color in color_map.items():
        html += f'''        .{token_type.lower()} {{
            color: {color};
        }}
        .guide-{token_type.lower()} {{
            background-color: {color};
        }}
'''

    html += '''    </style>
</head>
<body>
    <h1>Syntax Highlighter</h1>
    <h2>Color Guide</h2>
    <div class="color-guide">'''

    for token_type, _ in color_map.items():
        if token_type != 'OTHER':
            html += f'        <div class="color-item guide-{token_type.lower()}">{token_type.capitalize()}</div>\n'

    html += f'''    </div>
    <h2>Highlighted {language.upper()} Code</h2>
    <pre><code>'''

    for token_type, value in tokens:
        escaped_value = value.replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')
        html += f'<span class="token {token_type.lower()}">{escaped_value}</span>'

    html += '''    </code></pre>
</body>
</html>'''
    return html

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        file_name, file_ext = os.path.splitext(os.path.basename(file_path))
        language = file_ext[1:].upper()  # Extract language from file extension

        if language == "PY":
            language = "python"
        elif language == "SQL":
            language = "sql"
        elif language == "VBS":
            language = "basic"

        tokens = tokenize(code, language)
        html_output = generate_html(tokens, language)

        output_path = f"{file_name}_{language.lower()}_resaltado.html"
        with open(output_path, 'w') as file:
            file.write(html_output)

        print(f"El código resaltado para {file_path} se ha guardado en {output_path}")
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {str(e)}")

def main():
    file_paths = []
    print("Introduce la ruta de los archivos (deja en blanco para terminar):")

    while True:
        file_path = input("> ")
        if not file_path:
            break
        file_paths.append(file_path)

    # Running each file individually
    start_time_individual = time.time()
    for file_path in file_paths:
        process_file(file_path)
    end_time_individual = time.time()
    individual_time = end_time_individual - start_time_individual
    print(f"Time taken to process files individually: {individual_time:.2f} seconds")

    # Running files in parallel using ThreadPoolExecutor
    start_time_thread_pool = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(process_file, file_paths)
    end_time_thread_pool = time.time()
    thread_pool_time = end_time_thread_pool - start_time_thread_pool
    print(f"Time taken to process files with ThreadPoolExecutor: {thread_pool_time:.2f} seconds")

if __name__ == "__main__":
    main()
