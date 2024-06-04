import re

def tokenize_basic(code):
    patterns = [
        ('COMMENT', r'(\'.*|\bREM\s.*)'),
        ('KEYWORD', r'\b(AND|OR|NOT|REM|LET|IF|THEN|ELSE|ELSEIF|ENDIF|GOTO|GOSUB|RETURN|FOR|TO|STEP|NEXT|WHILE|WEND|DO|LOOP|EXIT|SELECT|CASE|ENDSELECT|ENDCASE|DIM|AS|FUNCTION|ENDFUNCTION|SUB|ENDSUB|PRINT|INPUT|READ|DATA|RESTORE|GOTO|ON|ERROR|RESUME|RESUME_NEXT|STOP|END|CONST|INCLUDE)\b'),
        ('LITERAL', r'("[^"]*"|\b\d+(\.\d+)?\b)'),
        ('OPERATOR', r'(\+|-|\*|/|\^|=|<|>|<=|>=|<>|MOD|AND|OR|NOT)'),
        ('SEPARATOR', r'[\(\)\[\]{},:;\.]'),
        ('IDENTIFIER', r'[a-zA-Z_]\w*'),
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

def generate_html(tokens):
    color_map = {
        'KEYWORD': '#56E1FF',      # Azul
        'IDENTIFIER': '#ffffff',   # Blanco
        'OPERATOR': '#FFA800',     # Naranja
        'LITERAL': '#23FF55',      # Verde
        'SEPARATOR': '#FF295D',    # Rojo
        'COMMENT': '#9256FF',      # Morado
        'OTHER': '#212529',        # Negro
    }

    html = '''<!DOCTYPE html>
<html>
<head>
    <title>Resaltador de sintaxis</title>
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
    <h1>Resaltador de sintaxis</h1>
    <h2>Codigo de colores</h2>
    <div class="color-guide">'''

    for token_type, _ in color_map.items():
        if token_type != 'OTHER':
            html += f'        <div class="color-item guide-{token_type.lower()}">{token_type.capitalize()}</div>\n'

    html += '''    </div>
    <h2>Codigo resaltado</h2>
    <pre><code>'''

    for token_type, value in tokens:
        escaped_value = value.replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')
        html += f'<span class="token {token_type.lower()}">{escaped_value}</span>'

    html += '''    </code></pre>
</body>
</html>'''
    return html

# Ejemplo de uso
file_path = input("Introduce la ruta del archivo BASIC: ")
with open(file_path, 'r') as file:
    code = file.read()

tokens = tokenize_basic(code)  

html_output = generate_html(tokens)

output_path = "BASIC_Resaltado.html"
with open(output_path, 'w') as file:
    file.write(html_output)

print(f"El codigo resaltado se ha guardado en {output_path}")
