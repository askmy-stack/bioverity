import json
from copy import deepcopy
from pathlib import Path

import pytest
from bioverity.schemas.records import EcologicalObservation
from jsonschema import Draft202012Validator, FormatChecker
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[2]


def test_json_schemas_are_valid() -> None:
    for path in (ROOT / "specs").glob("*.schema.json"):
        schema = json.loads(path.read_text())
        Draft202012Validator.check_schema(schema)


def test_observation_provenance_contract() -> None:
    schema = json.loads((ROOT / "specs/eor.schema.json").read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    observations = json.loads((ROOT / "datasets/fixtures/demo_observations.json").read_text())
    for observation in observations:
        validator.validate(observation)
        EcologicalObservation.model_validate(observation)

    for change in (
        lambda item: item.pop("provenance"),
        lambda item: item["provenance"].pop("retrieved_at"),
        lambda item: item["provenance"].update(pipeline_version=""),
        lambda item: item["provenance"].update(retrieved_at="not-a-date"),
    ):
        invalid = deepcopy(observations[0])
        change(invalid)
        assert not validator.is_valid(invalid)
        with pytest.raises(ValidationError):
            EcologicalObservation.model_validate(invalid)


def test_observation_source_must_match_provenance() -> None:
    observation = json.loads((ROOT / "datasets/fixtures/demo_observations.json").read_text())[0]
    observation["provenance"]["source_identifier"] = "another-record"
    with pytest.raises(ValidationError, match="must match"):
        EcologicalObservation.model_validate(observation)


def test_invalid_observation_fixture_is_rejected() -> None:
    schema = json.loads((ROOT / "specs/eor.schema.json").read_text())
    invalid = json.loads(
        (ROOT / "datasets/fixtures/invalid_observation_provenance.json").read_text()
    )
    assert not Draft202012Validator(schema, format_checker=FormatChecker()).is_valid(invalid)
    with pytest.raises(ValidationError):
        EcologicalObservation.model_validate(invalid)
