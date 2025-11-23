
import sys
import types
import importlib.util
import os

# Load the real `handlers/utils/dynamodb_client.py` as `utils.dynamodb_client`
# so `from utils.dynamodb_client import ...` works without modifying app code.
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dynamodb_path = os.path.join(base_dir, "handlers", "utils", "dynamodb_client.py")
if os.path.exists(dynamodb_path):
    spec = importlib.util.spec_from_file_location("utils.dynamodb_client", dynamodb_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("utils", types.ModuleType("utils"))
    sys.modules["utils.dynamodb_client"] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        # If executing the module fails (e.g. missing boto3), keep the module
        # object in sys.modules so the import resolution succeeds; actual
        # runtime calls should be avoided in tests.
        pass
    # Ensure the expected symbol exists so `from utils.dynamodb_client import get_dynamodb_client`
    # won't fail during import in the code under test. Provide a harmless stub
    # that raises if used at runtime.
    if not hasattr(module, "get_dynamodb_client"):
        def _stub_get_dynamodb_client():
            class _StubClient:
                def delete_item(self, *args, **kwargs):
                    raise RuntimeError("DynamoDB client not available in test")
            return _StubClient()
        module.get_dynamodb_client = _stub_get_dynamodb_client

    # Provide required environment variables expected by the module under test.
    os.environ.setdefault("TABLE_NAME", "_TEST_TABLE_")

from handlers.templates.delete_template import delete_template


def test_delete_template_importable():
    """Verifica que `delete_template` pode ser importado e é chamável.

    Não executa operações de rede/DB — apenas valida a importação.
    """
    assert callable(delete_template)


