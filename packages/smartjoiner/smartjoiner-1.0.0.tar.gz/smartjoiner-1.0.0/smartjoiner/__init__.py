class SmartJoiner:
    @staticmethod
    def join(
            items,
            separator="",
            condition=None,
            pad=None,
            with_index=False,
            separators=None,
            transform=None,
            localized=False,
            localized_word="and",
            separator_function=None,
    ):
        """
        An advanced join function with customizable features.

        Parameters:
            items (list): List of elements to join.
            separator (str): Default separator between elements.
            condition (callable): A function to filter items (e.g., lambda x: len(x) > 0).
            pad (str): String to pad around each element.
            with_index (bool): Whether to prepend the index to each element.
            separators (list): List of separators to apply between elements.
            transform (callable): Function to transform elements (e.g., str.upper).
            localized (bool): Whether to add a localized word (e.g., "and") before the last element.
            localized_word (str): The localized word to add before the last element (default: "and").
            separator_function (callable): Function to determine separators dynamically.

        Returns:
            str: The joined string.
        """
        # Ensure items is a list and handle None or empty input gracefully
        if not items:
            return ""

        # Apply condition (filter items)
        if condition:
            items = [item for item in items if condition(item)]

        # Apply transform (modify items)
        if transform:
            items = [transform(item) for item in items]

        # Apply padding (add padding to each element)
        if pad:
            items = [f"{pad}{item}{pad}" for item in items]

        # Add index to each element if requested
        if with_index:
            items = [f"{i}: {item}" for i, item in enumerate(items)]

        # Recursive flattening for nested lists
        def flatten(iterable):
            for element in iterable:
                if isinstance(element, list):
                    yield from flatten(element)
                else:
                    yield element

        items = list(flatten(items))

        # Handle localized join
        if localized and len(items) > 1:
            return separator.join(items[:-1]) + f" {localized_word} {items[-1]}"

        # Handle mixed separators
        if separators:
            result = ""
            for i, item in enumerate(items):
                result += item
                if i < len(separators):
                    result += separators[i]
                elif i < len(items) - 1:
                    result += separator
            return result

        # Handle dynamic separator function
        if separator_function:
            return "".join(
                f"{item}{separator_function(i, item)}" if i < len(items) - 1 else item
                for i, item in enumerate(items)
            )

        # Default join behavior
        return separator.join(items)
