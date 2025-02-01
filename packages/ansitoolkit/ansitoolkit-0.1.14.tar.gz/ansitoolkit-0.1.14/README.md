<h1 align="center">AnsiToolkit</h1>
<p align="center">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/HYP3R00T/AnsiToolkit/pypi_publish.yml?style=for-the-badge&labelColor=%2324273a&color=%23b7bdf8">
<a src="https://pypi.org/project/ansitoolkit/" target="_blank">
<img alt="Pypi versions" src="https://img.shields.io/pypi/v/ansitoolkit?style=for-the-badge&labelColor=%2324273a&color=%23b7bdf8">
</a>
</p>

The `ansitoolkit` Python package was created to simplify working with ANSI escape codes, which are often essential for adding color, formatting, and cursor control in terminal applications. However, using ANSI codes directly can be cumbersome and error-prone, as they are not intuitive and can be difficult to remember or look up.

To address this challenge, we designed `ansitoolkit` with a modular approach, organizing ANSI escape codes into dedicated classes. This structure allows users to access the codes in a more readable and manageable way, such as through methods and attributes like `Cursor.move_up()` or `Color.RED`. By encapsulating the complexity of ANSI codes within these classes, `ansitoolkit` makes it easier for developers to create terminal-based applications without needing to constantly reference ANSI code charts or worry about syntax errors.

With `ansitoolkit`, our goal is to provide a developer-friendly interface that streamlines the use of ANSI codes, enabling more efficient and visually appealing terminal output.

## Installation

```bash
pip install ansitoolkit
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
