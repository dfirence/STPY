
## **Overview**
This Python-based template engine allows for powerful data transformations using familiar syntax like `if/else` logic and loops. It is ideal for rendering JSON-like data structures and can easily be extended for more advanced use cases.

## Warning: `eval(..)` usage
To use Python expressions in the Config declarations of temp,ages, the `eval(…)` expression is implemented without keyword restrictions. You can easily add a restricted expression in the `resolve_template()` function.

<br/><br/><hr/>

# **Python Template Transformation Engine**

This project demonstrates a **Python-based template engine** inspired by `STJS` that supports features such as:

- **Loops** using `#each`.

- **Conditionals** using `#if/#else`.
  
- **Dynamic placeholders** within templates using `{{ }}` expressions.
 
- **Python expression evaluation** within templates.

The engine can handle complex data structures with nested dictionaries and lists, making it versatile for transforming JSON-like data.

—

## **Outline TOC**
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Code Overview](#code-overview)
6. [Example Data and Templates](#example-data-and-templates)
7. [Expected Output](#expected-output)
8. [Conclusion](#conclusion)

—

## **Overview**
This engine mimics **template-based rendering** commonly found in JavaScript but implemented in Python. It allows transforming JSON-like data using templates with:
- **Conditionals** (if/else logic).
- **Loops** for iterating over collections.
- **String interpolation** for placeholders in templates.

—

## **Features**
1. **#each Directive**: Loop over lists and apply templates.
2. **#if Directive**: Apply conditional logic.
3. **{{ }} Expressions**: Embed Python expressions directly in templates.
4. **Nested Dictionary Access**: Use dot-separated paths to access deeply nested data.

—

## **Installation**
No additional libraries are required.

—

## **Usage**
1. Define your **data structure**.
2. Create a **template** that uses `#each`, `#if`, and `{{ }}` placeholders.
3. Use the `transform()` function to apply the template to your data.

—

## **Code Overview**

### **1. Utility Functions**

#### `get_value_by_path(data, path)`
This function retrieves a value from a nested dictionary using a **dot-separated path**.

```python
def get_value_by_path(data, path):
    “””Retrieve a value from nested dictionaries using dot-separated paths.”””
    keys = path.split(“.”)
    result = data
    try:
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError):
        return None
```

—

#### `resolve_template(template, context)`
This function processes templates with `{{ }}` placeholders and supports **Python expressions**.

```python
def resolve_template(template, context):
    “””Replace all {{ }} expressions with evaluated results from the context.”””
    def replace_match(match):
        expression = match.group(1).strip()
        try:
            return str(eval(expression, {}, context))
        except Exception as e:
            print(f”Error evaluating expression ‘{expression}’: {e}”)
            value = get_value_by_path(context, expression)
            if value is None:
                print(f”Error resolving path ‘{expression}’: Path not found.”)
                return “”
            return str(value)

    return re.sub(r”{{(.*?)}}”, replace_match, template)
```

—

#### `handle_each(path, template, context)`
This function applies the `#each` directive to iterate over a list in the context.

```python
def handle_each(path, template, context):
    “””Iterate over items at the given path and apply the template to each.”””
    items = get_value_by_path(context, path) or []
    return [transform(template, item) for item in items]
```

#### `handle_if(condition, then_template, else_template, context)`
This function applies the `#if` directive to evaluate conditions.

```python
def handle_if(condition, then_template, else_template, context):
    “””Evaluate a condition and apply either the ‘then’ or ‘else’ template.”””
    condition_value = resolve_template(condition, context)
    if condition_value.lower() in [“true”, “1”]:
        return transform(then_template, context)
    else:
        return transform(else_template, context)
```

—

#### `transform(template, context)`
This function applies the **template to the given context**.

```python
def transform(template, context):
    “””Apply a template to the given context, handling #each and #if directives.”””
    result = {}

    if not isinstance(template, dict):
        return template

    for key, value in template.items():
        if key == “#each”:
            return handle_each(value, template.get(“template”, {}), context)
        elif key == “#if”:
            condition = value.get(“condition”)
            then_template = value.get(“then”, {})
            else_template = value.get(“else”, {})
            return handle_if(condition, then_template, else_template, context)
        elif isinstance(value, str) and “{{“ in value:
            result[key] = resolve_template(value, context)
        elif isinstance(value, dict):
            result[key] = transform(value, context)
        else:
            result[key] = value

    return result
```

—

## **Example Data and Templates**

#### Example Data

```python
data_simple = {
    “employees”: [
        {“name”: “Alice”, “role”: “Manager”, “active”: True},
        {“name”: “Bob”, “role”: “Engineer”, “active”: False},
        {“name”: “Charlie”, “role”: “Designer”, “active”: True},
        {“name”: “David”, “role”: “Intern”, “active”: False}
    ]
}
```

#### Example Template

```python
template_simple = {
    “employees”: {
        “#each”: “employees”,
        “template”: {
            “employeeName”: “{{name}}”,
            “role”: “{{role}}”,
            “status”: “{{‘Active’ if active else ‘Inactive’}}”,
            “category”: {
                “#if”: {
                    “condition”: “{{role == ‘Manager’}}”,
                    “#then”: “Category: Management”,
                    “#else”: {
                        “#if”: {
                            “condition”: “{{role == ‘Engineer’}}”,
                            “#then”: “Category: Technical”,
                            “#else”: {
                                “#if”: {
                                    “condition”: “{{role == ‘Designer’}}”,
                                    “#then”: “Category: Creative”,
                                    “#else”: “Category: General”
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

—

## **Expected Output**

```json
{
    “employees”: [
        {
            “employeeName”: “Alice”,
            “role”: “Manager”,
            “status”: “Active”,
            “category”: “Category: Management”
        },
        {
            “employeeName”: “Bob”,
            “role”: “Engineer”,
            “status”: “Inactive”,
            “category”: “Category: Technical”
        },
        {
            “employeeName”: “Charlie”,
            “role”: “Designer”,
            “status”: “Active”,
            “category”: “Category: Creative”
        },
        {
            “employeeName”: “David”,
            “role”: “Intern”,
            “status”: “Inactive”,
            “category”: “Category: General”
        }
    ]
}
```