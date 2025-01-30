# **SmartJoiner**

**SmartJoiner**, created by **Khalid Sulaiman Al-Mulaify**, is a Python library that enhances the traditional `join` function by adding powerful and flexible features. Whether you're building dynamic outputs, enhancing readability, or working with complex lists, SmartJoiner provides the tools to handle it efficiently.

---

## **Features**
✔ Conditional joining  
✔ Customizable padding  
✔ Indexed join  
✔ Mixed separators  
✔ Transform function  
✔ Recursive joining  
✔ Localized join  
✔ Dynamic separator function  

---

## **Installation**

Install **SmartJoiner** via pip:

```bash
pip install smartjoiner
```

---

## **Usage**

Import the `SmartJoiner` class and use its `join` method.

```python
from smartjoiner import SmartJoiner
```

---

## **Feature Details & Examples**

### 1. **Conditional Joining**
Join only elements that satisfy a given condition, such as filtering by string length.

```python
result = SmartJoiner.join(
    ["orange", "banana", "cherry", "grapes", "melon"],
    separator=", ",
    condition=lambda s: len(s) == 6
)
print(result)
# Output: "orange, cherry"
```

---

### 2. **Customizable Padding**
Add padding to each element, such as enclosing each string in quotes or wrapping it with special characters.

```python
result = SmartJoiner.join(
    ["apple", "banana", "cherry"],
    separator=", ",
    pad="'"
)
print(result)
# Output: "'apple', 'banana', 'cherry'"
```

---

### 3. **Indexed Join**
Include the index of each element in the joined string for tracking or formatting purposes.

```python
result = SmartJoiner.join(
    ["apple", "banana", "cherry"],
    separator=" | ",
    with_index=True
)
print(result)
# Output: "0: apple | 1: banana | 2: cherry"
```

---

### 4. **Mixed Separators**
Use different separators between elements based on position or other criteria.

```python
result = SmartJoiner.join(
    ["apple", "banana", "cherry"],
    separators=[" - ", " ~ "]
)
print(result)
# Output: "apple - banana ~ cherry"
```

---

### 5. **Transform Function**
Apply a transformation to each element before joining, such as uppercasing, reversing, or formatting strings dynamically.

```python
result = SmartJoiner.join(
    ["apple", "banana", "cherry"],
    separator=", ",
    transform=str.upper
)
print(result)
# Output: "APPLE, BANANA, CHERRY"
```

---

### 6. **Recursive Joining**
Automatically flatten nested lists and join all elements into a single string.

```python
result = SmartJoiner.join(
    ["apple", ["banana", "cherry"], "date"],
    separator=" - "
)
print(result)
# Output: "apple - banana - cherry - date"
```

---

### 7. **Localized Join**
Add a natural language conjunction like "and" or "or" before the last element for better readability.

#### Example 1: Using "and" (default)
```python
result = SmartJoiner.join(
    ["apple", "banana", "cherry"],
    separator=", ",
    localized=True
)
print(result)
# Output: "apple, banana, and cherry"
```

#### Example 2: Using "or"
```python
result = SmartJoiner.join(
    ["apple", "banana", "cherry"],
    separator=", ",
    localized=True,
    localized_word="or"
)
print(result)
# Output: "apple, banana, or cherry"
```

---

### 8. **Dynamic Separator**
Define a custom separator function to decide the separator based on the element's index or value.

```python
result = SmartJoiner.join(
    ["apple", "banana", "cherry"],
    separator_function=lambda i, _: " - " if i % 2 == 0 else " ~ "
)
print(result)
# Output: "apple - banana ~ cherry"
```

---

## **License**
This library is provided "as is", without warranty of any kind, express or implied.

---

## **Support**
For questions, feedback, or support, feel free to reach out to **Khalid Sulaiman Al-Mulaify** via:

Email: [khalidmfy@gmail.com](mailto:khalidmfy@gmail.com)  
X (Twitter): [@Python__Task](https://x.com/Python__Task)



