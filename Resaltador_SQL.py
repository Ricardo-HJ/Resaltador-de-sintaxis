import re

def tokenize_sql(code):
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
            regex = re.compile(pattern)
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
    # Definir colores constantes para cada tipo de token
    color_map = {
        'KEYWORD': '#56E1FF',      # Azul
        'IDENTIFIER': '#ffffff',   # Blanco
        'OPERATOR': '#FFA800',     # Naranja
        'LITERAL': '#23FF55',      # Verde
        'SEPARATOR': '#FF295D',    # Rojo
        'COMMENT': '#9256FF',      # Morado
        'OTHER': '#212529',       # Negro
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
    
    # Generar estilos CSS y guía de colores
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

    # Agregar elementos de la guía de colores (excluyendo 'OTHER')
    for token_type, _ in color_map.items():
        if token_type != 'OTHER':
            html += f'        <div class="color-item guide-{token_type.lower()}">{token_type.capitalize()}</div>\n'

    html += '''    </div>
    <h2>Codigo resaltado</h2>
    <pre><code>'''

    # Resaltar el código
    for token_type, value in tokens:
        escaped_value = value.replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')
        html += f'<span class="token {token_type.lower()}">{escaped_value}</span>'

    html += '''    </code></pre>
</body>
</html>'''
    return html

# Ejemplo de uso
file_path = input("Introduce la ruta del archivo SQL: ")
with open(file_path, 'r') as file:
    code = file.read()

tokens = tokenize_sql(code)
html_output = generate_html(tokens)

output_path = "SQL_Resaltado.html"
with open(output_path, 'w') as file:
    file.write(html_output)

print(f"El código resaltado se ha guardado en {output_path}")
