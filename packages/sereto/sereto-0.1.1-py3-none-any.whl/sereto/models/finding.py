from collections.abc import Iterator
from functools import cached_property
from pathlib import Path
from typing import Any, Self

import frontmatter  # type: ignore[import-untyped]
from pydantic import DirectoryPath, Field, FilePath, ValidationError, field_validator, model_validator, validate_call
from unidecode import unidecode

from sereto.cli.utils import Console
from sereto.enums import FileFormat, Risk
from sereto.exceptions import SeretoPathError, SeretoRuntimeError, SeretoValueError
from sereto.models.base import SeretoBaseModel
from sereto.models.version import ProjectVersion
from sereto.types import TypePathName
from sereto.utils import YAML


class VarsMetadata(SeretoBaseModel):
    name: str
    description: str
    required: bool = False
    list: bool = False

    def __str__(self) -> str:
        if self.required:
            params = " (required, list)" if self.list else " (required)"
        else:
            params = " (list)" if self.list else ""

        return f"{self.name}{params}: {self.description}"


class TemplateMetadata(SeretoBaseModel):
    name: str
    risk: Risk
    keywords: list[str] = []
    variables: list[VarsMetadata] = []

    @field_validator("risk", mode="before")
    @classmethod
    def convert_risk_type(cls, risk: Any) -> Risk:
        match risk:
            case Risk():
                return risk
            case str():
                return Risk(risk)
            case _:
                raise ValueError("unsupported type for Risk")


class ReportIncludeGroup(SeretoBaseModel):
    name: str
    risks: dict[ProjectVersion, Risk] = {}
    findings: list[str]

    @field_validator("risks", mode="before")
    @classmethod
    def convert_risks(cls, risks: Any) -> dict[ProjectVersion, Risk]:
        if not isinstance(risks, dict):
            raise ValueError("risks must be a dictionary")

        for ver, risk in risks.items():
            match risk:
                case Risk():
                    continue
                case str():
                    risk = Risk(risk)
                case _:
                    raise ValueError("invalid type for Risk")

            match ver:
                case ProjectVersion():
                    continue
                case str():
                    del risks[ver]
                    ver = ProjectVersion.from_str(ver)
                case _:
                    raise ValueError("invalid type for ProjectVersion")

            risks[ver] = risk

        return risks


class Finding(SeretoBaseModel):
    name: str
    category: str | None = None
    path_name: TypePathName
    risks: dict[ProjectVersion, Risk]
    vars: dict[str, Any] = {}
    format: FileFormat = FileFormat.md
    path: Path | None = Field(exclude=True, default=None)

    @field_validator("risks", mode="before")
    @classmethod
    def convert_risk_type(cls, v: dict[Any, Any]) -> dict[Any, Risk]:
        for key, value in v.items():
            match value:
                case Risk():
                    continue
                case str():
                    v[key] = Risk(value)
                case _:
                    raise ValueError("unsupported type for Risk")
        return v

    def present_in_versions(self) -> list[ProjectVersion]:
        """Get list of all project versions in which this finding is present."""
        return [k for k in self.risks]

    @validate_call
    def template_path(self, templates: DirectoryPath, category: str) -> Path:
        return templates / "categories" / category / "findings" / f"{self.path_name}.{self.format.value}.j2"

    @validate_call
    def metadata(self, templates: DirectoryPath, category: str) -> TemplateMetadata | None:
        template = self.template_path(templates=templates, category=category)
        if not template.is_file():
            Console().log(f"Finding template not found at '{template}'")
            return None

        metadata, _ = frontmatter.parse(template.read_text())
        try:
            return TemplateMetadata.model_validate(metadata)
        except ValidationError as ex:
            raise SeretoValueError(f"invalid template metadata in '{template}'") from ex

    @validate_call
    def assert_required_vars(self, templates: DirectoryPath, category: str) -> None:
        if (metadata := self.metadata(templates=templates, category=category)) is None:
            Console().log(f"No metadata for finding {self.path_name!r}")
            return

        for var in metadata.variables:
            if var.required and var.name not in self.vars:
                raise SeretoValueError(f"required variable {var.name!r} not set for finding {self.path_name!r}")


class FindingGroup(SeretoBaseModel):
    name: str
    risks: dict[ProjectVersion, Risk]
    findings: list[Finding]

    @property
    def uname(self) -> str:
        """Unique name for the finding group instance.

        Returns:
            The unique name of the finding group.
        """
        name = "".join([x.lower() for x in unidecode(self.name) if x.isalnum()])
        return f"finding_group_{name}"


class FindingsConfig(SeretoBaseModel):
    report_include: list[ReportIncludeGroup]
    findings: list[Finding]

    @model_validator(mode="after")
    def default_risks(self) -> Self:
        for finding_group in self.finding_groups:
            all_versions = set([r for f in finding_group.findings for r in f.risks])
            for version in all_versions:
                if version not in finding_group.risks:
                    version_risks = [r for f in finding_group.findings for v, r in f.risks.items() if v == version]
                    finding_group.risks[version] = max(version_risks, key=lambda r: r.to_int())
        return self

    @model_validator(mode="after")
    def validate_findings_config(self) -> Self:
        all_path_names = [f.path_name for f in self.findings]
        all_included_findings = [f for ri in self.report_include for f in ri.findings]

        # path_name is unique
        if len(all_path_names) != len(set(all_path_names)):
            raise ValueError('"path_name" must be unique')

        # each finding should be included only once (or not at all)
        if len(all_included_findings) != len(set(all_included_findings)):
            raise ValueError("each finding must be included at most once")

        for included_group in self.report_include:
            # at least one finding in each finding group
            if len(included_group.findings) == 0:
                raise ValueError(f'no findings configured for finding group "{included_group.name}"')

            # all references to findings can be resolved
            for finding_ref in included_group.findings:
                if finding_ref not in all_path_names:
                    raise ValueError(
                        f'finding "{finding_ref}" included in "{included_group.name}" is not present in'
                        "the findings section"
                    )
        return self

    @classmethod
    def from_yaml(cls, file: FilePath) -> Self:
        try:
            return cls.model_validate(YAML.load(file))
        except FileNotFoundError:
            raise SeretoPathError(f"file not found at '{file}'") from None
        except PermissionError:
            raise SeretoPathError(f"permission denied for '{file}'") from None
        except ValueError as e:
            raise SeretoValueError("invalid findings.yaml") from e

    def included_findings(self) -> Iterator[Finding]:
        """Generator of individual findings included in the report."""
        for ri in self.report_include:
            for finding_path in ri.findings:
                yield [f for f in self.findings if f.path_name == finding_path][0]

    @validate_call
    def get_finding(self, path_name: str) -> Finding:
        """Retrieve specific Finding instance by its 'path_name' attribute."""
        matches = [f for f in self.findings if f.path_name == path_name]
        match len(matches):
            case 0:
                raise SeretoValueError(f"finding with name {path_name!r} does not exist")
            case 1:
                return matches[0]
            case _:
                raise SeretoRuntimeError(
                    "improper validation, multiple findings with the same name should not be possible"
                )

    @cached_property
    def finding_groups(self) -> list[FindingGroup]:
        """Generator of included finding groups."""
        return [
            FindingGroup(
                name=group.name,
                risks=group.risks,
                findings=[self.get_finding(f_name) for f_name in group.findings],
            )
            for group in self.report_include
        ]
