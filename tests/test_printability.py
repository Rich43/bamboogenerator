from pathlib import Path
from parametric_cad.primitives.box import Box
from parametric_cad.printability import PrintabilityValidator

RULES_PATH = Path(__file__).resolve().parents[1] / "bambu_printability_rules.json"


def test_box_compliance():
    box = Box(10.0, 10.0, 10.0)
    validator = PrintabilityValidator(RULES_PATH)
    errors = validator.validate_mesh(box.mesh())
    assert errors == []


def test_dimension_violation():
    big_box = Box(300.0, 10.0, 10.0)
    validator = PrintabilityValidator(RULES_PATH)
    errors = validator.validate_mesh(big_box.mesh())
    assert any("X dimension" in e for e in errors)
