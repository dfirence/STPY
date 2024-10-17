
# **Python Template Engine Tutorial: Yoda’s Classic Example**

This tutorial will walk you through **using the Python Template Engine** to transform structured data. We’ll use **Yoda’s classic example** as our dataset and showcase how you can use loops, conditional logic, and string interpolation to manipulate the data with a template.

—

## **1. Prerequisites**
Make sure you have **Python 3.x** installed. No additional libraries are required to run the code.

—

## **2. Step-by-Step Instructions**

### **Step 1: Prepare the Dataset**
We will use a dataset that includes a list of **Yoda’s wisdom quotes**, with each quote containing attributes such as the quote text, year, and whether the quote is legendary.

Here’s the dataset we will use:

```python
data_yoda = {
    “quotes”: [
        {“text”: “Do or do not, there is no try.”, “year”: 1980, “legendary”: True},
        {“text”: “Train yourself to let go of everything you fear to lose.”, “year”: 2005, “legendary”: False},
        {“text”: “Fear is the path to the dark side.”, “year”: 1999, “legendary”: True},
        {“text”: “In a dark place we find ourselves, and a little more knowledge lights our way.”, “year”: 2005, “legendary”: False}
    ]
}
```

—

### **Step 2: Create a Template**
Next, we need a **template** that uses the `#each` directive to loop through the quotes. We’ll also use **conditional logic (`#if`)** to mark the quote as “Legendary” only if the `legendary` attribute is `True`.

Here’s the template:

```python
template_yoda = {
    “yodaQuotes”: {
        “#each”: “quotes”,
        “template”: {
            “quote”: “{{text}}”,
            “year”: “{{year}}”,
            “status”: {
                “#if”: {
                    “condition”: “{{legendary}}”,
                    “#then”: “Legendary”,
                    “#else”: “Not Legendary”
                }
            }
        }
    }
}
```

—

### **Step 3: Apply the Template with the Data**
We’ll use the `transform()` function to apply the template to our Yoda quotes dataset. 

Here’s the complete code:

```python
import json

# Function definitions: get_value_by_path, resolve_template, handle_each, handle_if, transform (import from the main script)

# Data
data_yoda = {
    “quotes”: [
        {“text”: “Do or do not, there is no try.”, “year”: 1980, “legendary”: True},
        {“text”: “Train yourself to let go of everything you fear to lose.”, “year”: 2005, “legendary”: False},
        {“text”: “Fear is the path to the dark side.”, “year”: 1999, “legendary”: True},
        {“text”: “In a dark place we find ourselves, and a little more knowledge lights our way.”, “year”: 2005, “legendary”: False}
    ]
}

# Template
template_yoda = {
    “yodaQuotes”: {
        “#each”: “quotes”,
        “template”: {
            “quote”: “{{text}}”,
            “year”: “{{year}}”,
            “status”: {
                “#if”: {
                    “condition”: “{{legendary}}”,
                    “#then”: “Legendary”,
                    “#else”: “Not Legendary”
                }
            }
        }
    }
}

# Transform the data using the template
result = transform(template_yoda, data_yoda)

# Print the transformed result as formatted JSON
print(json.dumps(result, indent=4))
```

—

### **Step 4: Run the Code**
1. Save the code above to a file called `yoda_template.py`.
2. Open a terminal and navigate to the directory where the file is located.
3. Run the script using the following command:

   ```bash
   python yoda_template.py
   ```

—

### **Step 5: Expected Output**
The script will print the transformed data in the following format:

```json
{
    “yodaQuotes”: [
        {
            “quote”: “Do or do not, there is no try.”,
            “year”: 1980,
            “status”: “Legendary”
        },
        {
            “quote”: “Train yourself to let go of everything you fear to lose.”,
            “year”: 2005,
            “status”: “Not Legendary”
        },
        {
            “quote”: “Fear is the path to the dark side.”,
            “year”: 1999,
            “status”: “Legendary”
        },
        {
            “quote”: “In a dark place we find ourselves, and a little more knowledge lights our way.”,
            “year”: 2005,
            “status”: “Not Legendary”
        }
    ]
}
```

—

## **6. Explanation of the Template Logic**
1. **Looping through Quotes**: 
   - The `#each` directive iterates over the `quotes` list in the dataset.

2. **Conditional Status**:
   - The `#if` directive checks if the `legendary` attribute is `True`. If it is, the status is set to `”Legendary”`. Otherwise, it is `”Not Legendary”`.

3. **String Interpolation**:
   - The `{{text}}` and `{{year}}` placeholders are replaced by the corresponding values from the dataset.

—

## **7. Customization Ideas**
- **Add More Quotes**: Extend the `quotes` list with new Yoda sayings.
- **Modify Conditional Logic**: Add more complex conditions to the template, such as filtering by year.
- **Format Output**: Adjust the template to change the output structure, e.g., group quotes by year.

—

## **8. Conclusion**
This example demonstrates how to use the Python Template Engine to transform data in a structured way, similar to templates used in web development. With support for loops, conditionals, and expressions, this engine is versatile and easy to use.

May the force be with your transformations!

