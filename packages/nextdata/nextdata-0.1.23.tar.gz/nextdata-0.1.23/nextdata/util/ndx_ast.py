import ast
from pathlib import Path


class NextDataVisitor(ast.NodeVisitor):
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        with Path(file_path).open("r") as f:
            self.tree = ast.parse(f.read())
        self.has_glue_job: bool = False
        self.connection_name: str | None = None
        self.incremental_column: str | None = None
        self.input_tables: list[str] = []
        self.indices: list[str | set[str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        # Check for @glue_job decorator
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "glue_job":
                self.has_glue_job = True
            elif isinstance(decorator, ast.Call):  # noqa: SIM102
                if isinstance(decorator.func, ast.Name) and decorator.func.id == "glue_job":
                    self.has_glue_job = True
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:  # noqa: N802
        # Check for connection_name and incremental_column assignments
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            if var_name == "connection_name" and isinstance(node.value, ast.Constant):
                self.connection_name = node.value.value
            elif var_name == "incremental_column" and isinstance(node.value, ast.Constant):
                self.incremental_column = node.value.value
            elif var_name == "indices" and isinstance(node.value, ast.Constant):
                self.indices = node.value.value
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        # Check for DataTable instantiations
        if isinstance(node.func, ast.Name) and node.func.id == "DataTable":  # noqa: SIM102
            if node.args and isinstance(node.args[0], ast.Constant):
                self.input_tables.append(node.args[0].value)
        self.generic_visit(node)
