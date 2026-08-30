import pytest

if __name__ == "__main__":
    # Ejecuta la suite de tests. Por defecto corre los tests de catálogo;
    # acepta argumentos extra (rutas, -v, -k, etc.) como en `pytest`.
    sys_args = [
        "tests/test_catalog_read.py",
        "-v",
        "--no-header",
    ]
    raise SystemExit(pytest.main(sys_args))