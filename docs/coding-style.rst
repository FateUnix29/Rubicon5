======================
Rubicon 5 Coding Style
======================

| This is a (hopefully) short overview of the coding style I hope to use for Rubicon 5.
| Contributors are heavily encouraged to follow this style, but I won't force it.
|
| Rubicon's coding style is a custom, likely a little arbitrary, style. It is based off of no existing style,
though the order of this document is lightly inspired by the Linux kernel coding style document.
| It is meant to be readable and easy to understand.
|
| As the Rubicon project develops and is more maintained, more of the codebase will be rearranged into this style.

.. note::
    This is a *heavy* work in progress.

Indentation
-----------
| Rubicon uses 4 spaces for indentation (though in the actual code you'll likely see a lot of \\t).
| This is the standard tab size on the machine and IDE Rubicon was primarily developed on.

Spacing
-------
| Spacing is rather erratic.
| This is one of the most loosely defined parts of the coding style.
|
| First off, functions, classes, methods, whatever, are expected to have *three or more* newlines between them, not including the one at the end of the function/class/method/whatever.
| This makes them easy to distinguish.
|
| As for actual code lines, here's where order breaks down.
| Spacing between lines is highly variable in the Rubicon project, and mainly boils down to what you think should be "grouped together."
| However, double-newlines should still be common, and groups should be 5 lines at most.
|
| Lines of code should *never* come directly after specific keywords and signatures.
| Keywords such as `for`, `if`, `while`, `def`, `class`, etc., and signatures, with the exception of keywords such as `global`,
should be on their own line, surrounded by newlines, for readability.
| This means an extra newline before the keyword, and an extra newline after it.
| An example of this:

.. code-block:: python

    print("Hello, world!") # Generic line of code preceiding a keyword.

    for i in range(10): # The `for` is on its own line.
    
    # Extra newline ^
    print(i)


Signatures & Documentation
--------------------------
| Anything with a 'signature', such as a function or a class, is expected to have a docstring, and for those that return something, a -> type description where valid.
| If a signature has a lot of arguments, it is expected to be split into multiple lines. A function signature should not be longer than 150 characters.

.. info::
    Document ends here for now. This is not *all* of the style, but I haven't figured the rest of the style yet.