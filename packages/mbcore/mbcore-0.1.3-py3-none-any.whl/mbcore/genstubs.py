import inspect
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, TypedDict

from mypy.nodes import ClassDef, FuncDef, MypyFile
from mypy.options import Options as MypyOptions
from mypy.stubgen import Options as StubgenOptions
from mypy.stubgen import generate_asts_for_modules, generate_stubs, StubSource  # Add import for StubSource
from mypy.build import BuildSource

# Add parent directory to Python path to import mbcore package
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TreeNode(TypedDict):
    name: str
    kind: str  # 'module', 'class', 'function', 'variable'
    signature: str | None
    docstring: str | None
    source: str | None
    children: List['TreeNode']
    decorators: List[str]
    is_private: bool

class StubGenerator:
    def __init__(
        self, 
        modules: List[str], 
        output_dir: str = "stubs",
        include_private: bool = True,
        include_source: bool = True,
    ):
        self.modules = modules
        self.output_dir = Path(output_dir)
        self.include_source = include_source
        
        # Get Python version tuple
        version_info = sys.version_info[:2]
        
        # Create minimal mypy options - only use essential attributes
        mypy_opts = MypyOptions()
        mypy_opts.python_version = version_info
        mypy_opts.show_traceback = True
        mypy_opts.follow_imports = "silent"  # Don't complain about missing imports
        mypy_opts.ignore_missing_imports = True
        mypy_opts.platform = sys.platform
        self.mypy_opts = mypy_opts
        
        # Create stubgen options
        self.opts = StubgenOptions(
            pyversion=version_info,
            no_import=False,
            inspect=True,
            doc_dir="",
            search_path=[project_root],  # Add project root to search path
            interpreter=sys.executable,
            parse_only=False,
            ignore_errors=False,
            include_private=include_private,
            output_dir=str(self.output_dir),
            modules=self.modules,
            packages=[],
            files=[],
            verbose=True,
            quiet=False,
            export_less=False,
            include_docstrings=True,
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.processed_modules: Set[str] = set()

    def extract_signature(self, node: Any) -> str | None:
        try:
            if isinstance(node, (ClassDef | FuncDef)):
                return str(node.type.signature()) if hasattr(node, 'type') else None
            return None
        except Exception:
            return None

    def process_node(self, node: Any, module: Any) -> TreeNode:
        name = getattr(node, 'name', '')
        kind = self._get_node_kind(node)
        docstring = inspect.getdoc(node) if inspect.ismodule(module) else None
        
        tree_node = TreeNode(
            name=name,
            kind=kind,
            signature=self.extract_signature(node),
            docstring=docstring,
            source=self._get_source(node) if self.include_source else None,
            children=[],
            decorators=self._get_decorators(node),
            is_private=name.startswith('_'),
        )

        if hasattr(node, 'defs'):
            for child in node.defs:
                if self._should_include_node(child):
                    tree_node['children'].append(self.process_node(child, module))

        return tree_node

    def _get_node_kind(self, node: Any) -> str:
        if isinstance(node, MypyFile):
            return 'module'
        if isinstance(node, ClassDef):
            return 'class'
        if isinstance(node, FuncDef):
            return 'function'
        return 'variable'

    def _should_include_node(self, node: Any) -> bool:
        if not hasattr(node, 'name'):
            return False
        return (self.opts.include_private or 
                not node.name.startswith('_'))

    def _get_source(self, node: Any) -> str | None:
        try:
            return inspect.getsource(node)
        except Exception:
            return None

    def _get_decorators(self, node: Any) -> List[str]:
        if hasattr(node, 'decorators'):
            return [d.name for d in node.decorators]
        return []

    def _import_module(self, module_name: str) -> bool:
        """Safely import a module and return success status."""
        try:
            if module_name not in sys.modules:
                __import__(module_name)
            return True
        except ImportError as e:
            logger.warning(f"Warning: Could not import module {module_name}: {e}")
            return False

    def generate_for_modules(self) -> Dict[str, List[TreeNode]]:
        result = {}
        for module_name in self.modules:
            if not self._import_module(module_name):
                continue
                
            if module_name in self.processed_modules:
                continue
                
            self.processed_modules.add(module_name)
            try:
                # Create StubSource instead of BuildSource
                stub_sources = [StubSource(module=module_name)]
                asts = generate_asts_for_modules(
                    stub_sources,
                    parse_only=True,
                    mypy_options=self.mypy_opts,
                    verbose=True
                )
                if not asts:
                    continue
                    
                module_trees = []
                for ast_node in asts:
                    tree = self.process_node(ast_node, sys.modules.get(module_name))
                    module_trees.append(tree)
                    
                result[module_name] = module_trees
                
            except Exception as e:
                logger.error(f"Error processing module {module_name}: {e}")
                continue
            
        return result

    def save_trees(self, trees: Dict[str, List[TreeNode]], output_file: str = 'ast_trees.json') -> None:
        output_path = self.output_dir / output_file
        output_path.write_text(json.dumps(trees, indent=2), encoding='utf-8')

    def generate_stubs(self) -> None:
        try:
            # Create StubSource instead of BuildSource
            stub_sources = [StubSource(module=m) for m in self.modules]
            asts = generate_asts_for_modules(
                stub_sources,
                parse_only=True,
                mypy_options=self.mypy_opts,
                verbose=True
            )
            if not asts:
                logger.warning("No ASTs generated")
                return
                
            stubs = generate_stubs(asts, self.opts)
            if not stubs:
                logger.warning("No stubs generated")
                return
            
            for stub in stubs:
                if stub.path:
                    stub_path = self.output_dir / f"{stub.module}.pyi"
                    stub_path.parent.mkdir(parents=True, exist_ok=True)
                    stub_path.write_text(stub.output)
        except Exception as e:
            logger.error(f"Error generating stubs: {e}")

    def test_generation(self) -> bool:
        """Test stub generation with test_module."""
        try:
            # Create output directory first
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            test_trees = self.generate_for_modules()
            if not test_trees:
                logger.error("No AST trees generated")
                return False
                
            self.save_trees(test_trees, 'test_ast_trees.json')
            self.generate_stubs()
            
            # Verify stub file exists
            stub_file = self.output_dir / 'test_module.pyi'
            if not stub_file.exists():
                logger.error("Stub file was not generated")
                return False
                
            # Read and verify stub content
            stub_content = stub_file.read_text()
            expected_items = [
                'class BaseClass',
                'class TestClass',
                'def standalone_function',
                'async def async_function',
                '_private_var:',
                'PUBLIC_CONSTANT:',
            ]
            
            for item in expected_items:
                if item not in stub_content:
                    logger.error(f"Missing expected item in stub: {item}")
                    return False
                    
            logger.info("Stub generation test passed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Test failed with error: {e}")
            return False

def main() -> None:
    # First test with just the test module
    test_module_path = "mbcoretest_module"
    
    # Create test module if it doesn't exist
    test_module_dir = Path(project_root) / "mbcore"
    test_module_file = test_module_dir / "test_module.py"
    
    if not test_module_file.exists():
        test_module_content = '''
class BaseClass:
    """Base test class."""
    pass

class TestClass(BaseClass):
    """Test class for stub generation."""
    PUBLIC_CONSTANT = 1
    _private_var = 2
    
    def standalone_function(self, arg1: str, arg2: int = 0) -> bool:
        """Test standalone function."""
        return True
        
    async def async_function(self) -> None:
        """Test async function."""
        pass
'''
        test_module_file.write_text(test_module_content)

    # Create test stubs directory next to the package
    test_stubs_dir = Path(project_root) / "test_stubs"
    
    test_generator = StubGenerator(
        modules=[test_module_path],
        output_dir=str(test_stubs_dir),
        include_private=True,
        include_source=True,
    )
    
    if not test_generator.test_generation():
        logger.error("Stub generator tests failed")
        return
        
    # If tests pass, proceed with actual module stubs
    stubs_dir = Path(project_root) / "stubs"
    generator = StubGenerator(
        modules=['mbcore'],
        output_dir=str(stubs_dir),
        include_private=True,
        include_source=True,
    )
    
    trees = generator.generate_for_modules()
    generator.save_trees(trees)
    generator.generate_stubs()

if __name__ == "__main__":
    main()