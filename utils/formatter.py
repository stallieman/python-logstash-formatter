import re

def format_logstash_pipeline(file_content):
    """
    Processes a Logstash pipeline configuration string.
    
    • Re-indents the configuration using brace scopes.
    • Inserts a space before an opening brace if missing.
    • Checks for extra or missing closing braces, reporting errors with line numbers.
    • Automatically fixes common syntax errors where possible.
    
    Returns:
        formatted (str): The re-indented configuration (without injected line numbers).
        errors (list): List of error messages with line numbers.
        fixes_applied (list): List of automatic fixes that were applied.
    """
    lines = file_content.splitlines()
    formatted_lines = []
    errors = []
    fixes_applied = []
    indent_level = 0
    brace_stack = []  # stack holds the line numbers of unmatched '{'
    quote_state = False
    quote_start_line = None

    for line_number, line in enumerate(lines, start=1):
        original_line = line
        # Strip spaces and insert a space before '{' if missing, but preserve template variables like %{...}
        trimmed = line.strip()
        
        # Clean up excessive whitespace before opening braces (but not in template variables)
        if not '%{' in trimmed:
            # Replace multiple spaces before { with single space
            trimmed = re.sub(r'\s+\{', r' {', trimmed)
            # Ensure there's exactly one space before { for block definitions
            trimmed = re.sub(r'(\w)\{', r'\1 {', trimmed)
        
        # Clean up excessive whitespace around => operators
        if '=>' in trimmed:
            # Normalize spaces around => operator
            trimmed = re.sub(r'\s*=>\s*', ' => ', trimmed)
        
        # Clean up multiple consecutive spaces (but preserve indentation at start)
        # Only clean internal whitespace, not leading whitespace
        if trimmed:
            # Split on first non-space character to preserve leading indentation
            parts = re.split(r'(\S.*)', trimmed, 1)
            if len(parts) > 1 and parts[1]:
                # Clean up multiple spaces in the content part
                cleaned_content = re.sub(r'  +', ' ', parts[1])
                trimmed = parts[0] + cleaned_content
        
        if trimmed != line.strip() and line.strip():
            fixes_applied.append(f"Line {line_number}: Cleaned whitespace - was: '{line.strip()}' now: '{trimmed}'")
        
        # Auto-fix for braces followed by text (like "}tcp {")
        # This should split into separate lines: "}" and "tcp {"
        brace_text_pattern = r'^(\}+)(\s*)(\w+.*\{.*)$'
        match = re.match(brace_text_pattern, trimmed)
        if match:
            closing_braces = match.group(1)
            whitespace = match.group(2)
            remaining_text = match.group(3)
            
            # Create two separate lines
            # First line: just the closing braces
            brace_line = closing_braces
            
            # Second line: the remaining text with proper indentation
            text_line = remaining_text
            
            fixes_applied.append(f"Line {line_number}: Split closing brace and text into separate lines")
            
            # Process the closing brace line first
            leader = len(closing_braces)
            temp_indent = max(indent_level - leader, 0)
            formatted_line = f"{temp_indent * '    '}{brace_line}"
            formatted_lines.append(formatted_line)
            
            # Update indent level for closing braces
            for _ in range(leader):
                if brace_stack:
                    brace_stack.pop()
                    indent_level -= 1
                else:
                    errors.append(f"Line {line_number}: Extra closing brace '}}' found.")
            
            # Now process the text line
            trimmed = text_line
            # Add space before { if missing
            if not '%{' in trimmed:
                trimmed = re.sub(r'(\w)\{', r'\1 {', trimmed)
        
        # Auto-fix common issues
        # Fix missing quotes around values (but skip single quotes - they're valid)
        if '=>' in trimmed:
            # Look for unquoted values that should be quoted
            parts = trimmed.split('=>', 1)
            if len(parts) == 2:
                key_part = parts[0].strip()
                value_part = parts[1].strip()
                
                # Skip values that already have quotes, arrays, numbers, booleans, template variables,
                # and configuration blocks (like "codec => line {")
                # Also skip values that end with } as they might be part of syntax like "nested => true }"
                if not ('"' in value_part or "'" in value_part) and \
                   not (value_part.startswith('[') and value_part.endswith(']')) and \
                   not value_part.isdigit() and value_part not in ['true', 'false'] and \
                   not value_part.startswith('{') and not value_part.endswith('{') and \
                   not value_part.endswith('}') and \
                   not '%{' in value_part and \
                   (' ' in value_part or '-' in value_part or '.' in value_part):
                    # Don't quote template variables like %{...} or config blocks like "line {"
                    if not (value_part.startswith('%{') and value_part.endswith('}')):
                        original_value = value_part
                        value_part = f'"{value_part}"'
                        trimmed = f"{key_part} => {value_part}"
                        fixes_applied.append(f"Line {line_number}: Added quotes around value - was: '{original_value}' now: '{value_part}'")
        
        # Fix missing closing quotes for specific patterns (like => "value)
        if '=>' in trimmed and '"' in trimmed:
            # Check for missing closing quote pattern: => "value without closing quote
            if re.search(r'=>\s*"[^"]*$', trimmed):
                trimmed += '"'
                fixes_applied.append(f"Line {line_number}: Added missing closing quote")
        
        # Track quote state for cross-line quote detection (keep existing logic for complex cases)
        quote_count = 0
        i = 0
        while i < len(trimmed):
            if trimmed[i] == '"' and (i == 0 or trimmed[i-1] != '\\'):
                quote_count += 1
            i += 1
        
        if quote_count % 2 != 0:
            if not quote_state:
                quote_state = True
                quote_start_line = line_number
            else:
                quote_state = False
                quote_start_line = None
        
        # Count leading closing braces to adjust indent.
        leader = 0
        for char in trimmed:
            if char == '}':
                leader += 1
            else:
                break
        temp_indent = max(indent_level - leader, 0)
        formatted_line = f"{temp_indent * '    '}{trimmed}"
        formatted_lines.append(formatted_line)
        
        # Process the leading closing braces.
        i = 0
        while i < len(trimmed) and trimmed[i] == '}':
            if brace_stack:
                brace_stack.pop()
                indent_level -= 1
            else:
                errors.append(f"Line {line_number}: Extra closing brace '}}' found.")
            i += 1
        
        # Process the rest of the line.
        for char in trimmed[i:]:
            if char == '{':
                brace_stack.append(line_number)
                indent_level += 1
            elif char == '}':
                if brace_stack:
                    brace_stack.pop()
                    indent_level -= 1
                else:
                    errors.append(f"Line {line_number}: Extra closing brace '}}' found.")
    
    # Handle missing closing quotes by adding them (but only for multi-line quote blocks)
    if quote_state and quote_start_line:
        # Only add closing quote if it's truly missing across multiple lines
        errors.append(f"Line {quote_start_line}: Multi-line quote block missing closing quote")
        # Don't auto-fix multi-line quotes as it's complex to determine where they should close
    
    # Handle missing closing braces - add them to the appropriate lines
    missing_braces = len(brace_stack)
    if missing_braces > 0:
        for open_line in brace_stack:
            errors.append(f"Line {open_line}: Missing closing brace '}}' - attempting auto-fix.")
        
        # For each missing brace, find the appropriate place to add it
        for j in range(missing_braces):
            # Work backwards to find a suitable line for this brace
            for i in range(len(formatted_lines) - 1, -1, -1):
                line_content = formatted_lines[i].strip()
                if line_content and not line_content.endswith('{') and not line_content.endswith('}'):
                    # Add ONE closing brace to this line
                    formatted_lines[i] += "}"
                    fixes_applied.append(f"Added missing closing brace to line {i+1}")
                    break
            else:
                # If no suitable line found, add as new line
                formatted_lines.append("}")
                fixes_applied.append("Added missing closing brace as new line")

    # Voeg automatische regelomloop toe voor lange regels
    def wrap_line(line, max_length):
        if len(line) <= max_length:
            return [line]
        # Bepaal de oorspronkelijke inspringing
        m = re.match(r'(\s*)', line)
        indent = m.group(1) if m else ""
        in_quote = False
        last_space = -1
        for i, ch in enumerate(line):
            if i > max_length:
                break
            if ch == '"' and (i == 0 or line[i-1] != '\\'):
                in_quote = not in_quote
            if ch == ' ' and not in_quote:
                last_space = i
        split_index = last_space if last_space > len(indent) else max_length
        first_part = line[:split_index]
        rest = line[split_index:].lstrip()
        wrapped = [first_part]
        if rest:
            # Voeg extra inspringing toe voor het vervolg
            wrapped += wrap_line(indent + "    " + rest, max_length)
        return wrapped

    new_formatted_lines = []
    max_length = 100  # Pas deze waarde aan voor een andere maximale regelbreedte.
    for line in formatted_lines:
        if len(line) > max_length:
            wrapped = wrap_line(line, max_length)
            new_formatted_lines.extend(wrapped)
            if len(wrapped) > 1:
                fixes_applied.append(f"Wrapped long line into {len(wrapped)} lines")
        else:
            new_formatted_lines.append(line)
    formatted = "\n".join(new_formatted_lines)

    # Clean up extra whitespace and empty lines
    def clean_whitespace(text):
        lines = text.splitlines()
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            # Remove trailing whitespace from all lines
            cleaned_line = line.rstrip()
            
            # Handle empty lines
            if cleaned_line == "":
                # Get context lines
                prev_line = lines[i-1].rstrip() if i > 0 else ""
                next_line = lines[i+1].strip() if i < len(lines) - 1 else ""
                
                # Skip empty line if it's just before a closing brace
                if next_line.startswith("}"):
                    continue
                
                # Skip empty line if it's just after an opening brace
                if prev_line.endswith("{"):
                    continue
                
                # Only keep empty lines between top-level blocks (input, filter, output)
                if (prev_line.startswith("}") and 
                    (next_line.startswith("input") or next_line.startswith("filter") or next_line.startswith("output"))):
                    # Keep one empty line between top-level blocks
                    if not (cleaned_lines and cleaned_lines[-1] == ""):
                        cleaned_lines.append(cleaned_line)
                    continue
                
                # Skip all other empty lines
                continue
                    
            cleaned_lines.append(cleaned_line)
        
        # Remove trailing empty lines
        while cleaned_lines and cleaned_lines[-1] == "":
            cleaned_lines.pop()
            
        return "\n".join(cleaned_lines)
    
    original_formatted = formatted
    formatted = clean_whitespace(formatted)
    
    # Track if whitespace cleanup was applied
    if original_formatted != formatted:
        fixes_applied.append("Removed extra whitespace and empty lines")

    # Extra pipeline validation based on expected Kibana .conf syntax
    if not re.search(r'^\s*input\s*\{', formatted, re.MULTILINE):
        errors.append("Warning: No input block found. Pipeline may be missing essential configuration as per https://logstash-kafka.readthedocs.io/en/stable/configuration/")
    if not re.search(r'^\s*output\s*\{', formatted, re.MULTILINE):
        errors.append("Warning: No output block found. Pipeline may be missing essential configuration as per https://logstash-kafka.readthedocs.io/en/stable/configuration/")
    if not re.search(r'^\s*filter\s*\{', formatted, re.MULTILINE):
        errors.append("Warning: No filter block found. Consider adding filters for processing events as per https://www.elastic.co/docs/reference/logstash/config-examples")

    return formatted, errors, fixes_applied


def check_pipeline_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            formatted_content, errors, fixes_applied = format_logstash_pipeline(content)
            return formatted_content, errors, fixes_applied
    except Exception as e:
        return None, [str(e)], []


def check_pipeline_text(pipeline_text):
    try:
        formatted_content, errors, fixes_applied = format_logstash_pipeline(pipeline_text)
        return formatted_content, errors, fixes_applied
    except Exception as e:
        return None, [str(e)], []