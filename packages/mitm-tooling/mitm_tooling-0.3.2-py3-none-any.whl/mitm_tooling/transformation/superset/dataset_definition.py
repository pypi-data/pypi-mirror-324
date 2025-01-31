from abc import ABC, abstractmethod
from datetime import datetime, tzinfo
from typing import Any, Annotated, Literal

import pydantic
from uuid import UUID

from pydantic import Field

from mitm_tooling.data_types import MITMDataType

BetterUUID = Annotated[
    UUID,
    pydantic.BeforeValidator(lambda x: UUID(x) if isinstance(x, str) else x),
    pydantic.PlainSerializer(lambda x: str(x)),
    pydantic.Field(
        description="Better annotation for UUID, parses from string format. Serializes to string format."
    ),
]


class SupersetDefFile(pydantic.BaseModel, ABC):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    @property
    @abstractmethod
    def filename(self) -> str:
        pass


class SupersetDatabaseDef(SupersetDefFile):
    database_name: str
    sqlalchemy_uri: pydantic.AnyUrl
    uuid: BetterUUID
    cache_timeout: str | None = None
    expose_in_sqllab: bool = True
    allow_run_async: bool = False
    allow_ctas: bool = False
    allow_cvas: bool = False
    allow_dml: bool = False
    allow_file_upload: bool = False
    extra: dict[str, Any] = pydantic.Field(default_factory=lambda: {
        'allows_virtual_table_explore': True
    })
    impersonate_user: bool = False
    version: str = '1.0.0'
    ssh_tunnel: None = None

    @property
    def filename(self):
        return self.database_name


class SupersetMetricDef(pydantic.BaseModel):
    metric_name: str
    verbose_name: str
    expression: str
    metric_type: str | None = None
    description: str | None = None
    d3format: str | None = None
    currency: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)
    warning_text: str | None = None


class SupersetColumnDef(pydantic.BaseModel):
    column_name: str
    verbose_name: str | None = None
    is_dttm: bool = False
    is_active: bool = True
    type: str = str(MITMDataType.Text.sa_sql_type)
    advanced_data_type: str | None = None
    groupby: bool = True
    filterable: bool = True
    expression: str | None = None
    description: str | None = None
    python_date_format: str = None
    extra: dict[str, Any] = pydantic.Field(default_factory=dict)


class SupersetDatasetDef(SupersetDefFile):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    table_name: str
    schema_name: str = pydantic.Field(alias='schema')
    uuid: BetterUUID
    database_uuid: BetterUUID
    main_dttm_col: str | None = None
    description: str | None = None
    default_endpoint: str | None = None
    offset: int = 0
    cache_timeout: str | None = None
    catalog: str | None = None
    sql: str | None = None
    params: Any = None
    template_params: Any = None
    filter_select_enabled: bool = True
    fetch_values_predicate: str | None = None
    extra: dict[str, Any] = pydantic.Field(default_factory=dict)
    normalize_columns: bool = False
    always_filter_main_dttm: bool = False
    metrics: list[SupersetMetricDef] = pydantic.Field(default_factory=list)
    columns: list[SupersetColumnDef] = pydantic.Field(default_factory=list)
    version: str = '1.0.0'

    @property
    def filename(self):
        return self.table_name


StrDatetime = Annotated[datetime,
pydantic.BeforeValidator(lambda x: datetime.fromisoformat(x) if isinstance(x, str) else x),
pydantic.PlainSerializer(lambda x: str(x)),
pydantic.Field(
    description="Better annotation for datetime, parses from string format. Serializes to string format."
)]

MetadataType = Literal['Database', 'SqlaTable', 'Slice']


class SupersetMetadataDef(SupersetDefFile):
    version: str = '1.0.0'
    type: MetadataType = 'SqlaTable'
    timestamp: StrDatetime = pydantic.Field(default_factory=datetime.utcnow)

    @property
    def filename(self) -> str:
        return 'metadata'


class SupersetDef(pydantic.BaseModel):
    database: SupersetDatabaseDef
    datasets: list[SupersetDatasetDef]
    metadata: SupersetMetadataDef = pydantic.Field(default_factory=SupersetMetadataDef)

    def to_folder_structure(self) -> dict[str, Any]:
        db_name = self.database.database_name
        folder = {'.': self.metadata, 'databases': [{db_name: self.database}],
                  'datasets': {db_name: list(self.datasets)}}
        return {'my_import': folder}
