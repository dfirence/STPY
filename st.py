#! /usr/bin/env python

"""
MIT License

Copyright (c) 2024 STPY By Carlos Diaz | @dfirence.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import re
import json

def get_value_by_path(data, path):
    """Retrieve a value from nested dictionaries using dot-separated paths."""
    keys = path.split(".")
    result = data
    try:
        for key in keys:
            result = result[key]  # Access dictionary keys properly
        return result
    except (KeyError, TypeError):
        return None  # Return None if the path is invalid

def resolve_template(template, context):
    """
    Replace all {{ }} expressions with evaluated results from the context.
    """
    def replace_match(match):
        expression = match.group(1).strip()
        try:
            # Try evaluating the expression using eval() for function calls
            return str(eval(expression, {}, context))
        except Exception as e:
            print(f"Error evaluating expression '{expression}': {e}")
            # If eval fails, try to resolve as a simple path lookup
            value = get_value_by_path(context, expression)
            if value is None:
                print(f"Error resolving path '{expression}': Path not found.")
                return ""  # Return empty string if not found
            return str(value)

    return re.sub(r"{{(.*?)}}", replace_match, template)
    
def handle_each(path, template, context):
    """Iterate over items at the given path and apply the template to each."""
    items = get_value_by_path(context, path) or []
    return [transform(template, item) for item in items]

def handle_if(condition, then_template, else_template, context):
    """Evaluate a condition and apply either the '#then' or '#else' template."""
    condition_value = resolve_template(condition, context)
    if condition_value.lower() in ["true", "1"]:
        return transform(then_template, context)
    else:
        return transform(else_template, context)

def transform(template, context):
    """
    Apply a template to the given context, handling #each, #if, #then, #else directives.
    """
    result = {}

    if not isinstance(template, dict):
        return template

    for key, value in template.items():
        if key == "#each":
            return handle_each(value, template.get("template", {}), context)
        elif key == "#if":
            condition = value.get("condition")
            then_template = value.get("#then", {})
            else_template = value.get("#else", {})
            return handle_if(condition, then_template, else_template, context)
        elif isinstance(value, str) and "{{" in value:
            result[key] = resolve_template(value, context)
        elif isinstance(value, dict):
            result[key] = transform(value, context)
        else:
            result[key] = value

    return result