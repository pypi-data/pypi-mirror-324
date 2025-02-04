from __future__ import annotations

from collections.abc import Callable, Generator, Mapping
from typing import TYPE_CHECKING

import pydantic
import sqlalchemy as sa
import sqlalchemy.sql.schema
from pydantic import AnyUrl, ConfigDict
from mitm_tooling.data_types import MITMDataType
from mitm_tooling.definition import MITMDefinition, ConceptProperties, OwnedRelations, ConceptName, MITM, get_mitm_def, \
    RelationName
from mitm_tooling.definition.definition_tools import map_col_groups, ColGroupMaps
from .intermediate_representation import Header, MITMData
from mitm_tooling.utilities.sql_utils import create_sa_engine, qualify
from mitm_tooling.utilities import python_utils
from mitm_tooling.utilities.io_utils import FilePath

from sqlalchemy_utils.view import create_view

if TYPE_CHECKING:
    from mitm_tooling.extraction.sql.data_models import Queryable
from mitm_tooling.extraction.sql.data_models.table_identifiers import TableName

SQL_REPRESENTATION_DEFAULT_SCHEMA = 'main'


def mk_concept_table_name(mitm: MITM, concept: ConceptName) -> TableName:
    return get_mitm_def(mitm).get_properties(concept).plural


def mk_type_table_name(mitm: MITM, concept: ConceptName, type_name: RelationName) -> TableName:
    return get_mitm_def(mitm).get_properties(concept).key + '_' + type_name.lower()


def mk_link_table_name(mitm: MITM, concept: ConceptName, type_name: RelationName, fk_name: RelationName) -> TableName:
    return mk_type_table_name(mitm, concept, type_name) + '_' + fk_name.lower()


def has_type_tables(mitm: MITM, concept: ConceptName) -> bool:
    return get_mitm_def(mitm).get_properties(concept).permit_attributes


def pick_table_pk(mitm: MITM, concept: ConceptName, created_columns: Mapping[RelationName, sa.Column]) -> list[
    tuple[RelationName, sa.Column]]:
    mitm_def = get_mitm_def(mitm)
    concept_properties, concept_relations = mitm_def.get(concept)

    names, mapped_names = map_col_groups(mitm_def, concept, {
        'kind': lambda: 'kind',
        'type': lambda: concept_properties.typing_concept,
        'identity': lambda: list(concept_relations.identity)
    })

    return python_utils.pick_from_mapping(created_columns, names)


def mk_table(meta: sa.MetaData, mitm: MITM, concept: ConceptName, table_name: TableName, col_group_maps: ColGroupMaps,
             gen_additional_schema_items: Callable[
                                              [MITM, ConceptName, ConceptProperties, OwnedRelations,
                                               dict[RelationName, sa.Column], list[tuple[RelationName, sa.Column]]],
                                              Generator[
                                                  sqlalchemy.sql.schema.SchemaItem, None, None]] | None = None) -> \
        tuple[
            sa.Table, dict[RelationName, sa.Column], list[tuple[RelationName, sa.Column]]]:
    mitm_def = get_mitm_def(mitm)
    concept_properties, concept_relations = mitm_def.get(concept)

    columns, created_columns = map_col_groups(mitm_def, concept, col_group_maps, ensure_unique=True)

    ref_columns = pick_table_pk(mitm, concept, created_columns)

    constraints: list[sa.sql.schema.SchemaItem] = []
    if concept_relations.identity:
        constraints.append(sa.PrimaryKeyConstraint(*python_utils.i_th(1)(ref_columns)))

    if gen_additional_schema_items:
        schema_items = gen_additional_schema_items(mitm, concept, concept_properties, concept_relations,
                                                   created_columns,
                                                   ref_columns)
        constraints.extend(schema_items)

    return sa.Table(table_name, meta, schema=SQL_REPRESENTATION_DEFAULT_SCHEMA, *columns,
                    *constraints), created_columns, ref_columns


def gen_foreign_key_constraints(mitm: MITM, concept: ConceptName, concept_properties: ConceptProperties,
                                concept_relations: OwnedRelations, created_columns: dict[RelationName, sa.Column],
                                ref_columns: list[tuple[RelationName, sa.Column]]) -> Generator[
    sa.sql.schema.SchemaItem, None, None]:
    # self_fk
    parent_table = mk_concept_table_name(mitm, concept)
    cols, refcols = zip(
        *((c, qualify(table=parent_table, column=s)) for s, c in ref_columns))
    yield sa.ForeignKeyConstraint(name='parent', columns=cols, refcolumns=refcols)
    for fk_name, fk_info in concept_relations.foreign.items():
        cols, refcols = zip(*fk_info.fk_relations.items())
        fkc = sa.ForeignKeyConstraint(name=fk_name, columns=[created_columns[c] for c in cols], refcolumns=[
            # sa.literal_column(qualify(table=mk_concept_table_name(mitm, fk_info.target_concept), column=c))
            qualify(table=mk_concept_table_name(mitm, fk_info.target_concept), column=c)
            for c in refcols])
        yield fkc


ConceptTablesDict = dict[ConceptName, sa.Table]
ViewsDict = dict[TableName, sa.Table]
ConceptTypeTablesDict = dict[ConceptName, dict[TableName, sa.Table]]


class SQLRepresentationSchema(pydantic.BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    meta: sa.MetaData
    concept_tables: ConceptTablesDict
    type_tables: ConceptTypeTablesDict
    views: ViewsDict


def mk_db_schema(header: Header, gen_views: Callable[
                                                [MITM, MITMDefinition, ConceptTablesDict, ConceptTypeTablesDict],
                                                Generator[
                                                    tuple[
                                                        TableName, Queryable], None, None]] | None = None) -> SQLRepresentationSchema:
    mitm_def = get_mitm_def(header.mitm)
    meta = sa.MetaData(schema=SQL_REPRESENTATION_DEFAULT_SCHEMA)

    concept_tables: ConceptTablesDict = {}
    type_tables: ConceptTypeTablesDict = {}
    views: dict[str, sa.Table] = {}

    for concept in mitm_def.main_concepts:
        concept_properties, concept_relations = mitm_def.get(concept)

        table_name = mk_concept_table_name(header.mitm, concept)

        t, t_columns, t_ref_columns = mk_table(meta, header.mitm, concept, table_name, {
            'kind': lambda: ('kind', sa.Column('kind', MITMDataType.Text.sa_sql_type, nullable=False)),
            'type': lambda: (concept_properties.typing_concept, sa.Column(concept_properties.typing_concept,
                                                                          MITMDataType.Text.sa_sql_type,
                                                                          nullable=False)),
            'identity': lambda: [(name, sa.Column(name, dt.sa_sql_type, nullable=False)) for
                                 name, dt in
                                 mitm_def.resolve_identity_type(concept).items()],
            'inline': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for name, dt in
                               mitm_def.resolve_inlined_types(concept).items()],
            'foreign': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for _, resolved_fk in
                                mitm_def.resolve_foreign_types(concept).items() for name, dt in
                                resolved_fk.items()]
        })
        concept_tables[concept] = t

    for he in header.header_entries:
        he_concept = he.concept
        if has_type_tables(header.mitm, he_concept):
            concept_properties, concept_relations = mitm_def.get(he_concept)

            table_name = mk_type_table_name(header.mitm, he_concept, he.type_name)

            t, t_columns, t_ref_columns = mk_table(meta, header.mitm, he_concept, table_name, {
                'kind': lambda: ('kind', sa.Column('kind', MITMDataType.Text.sa_sql_type, nullable=False)),
                'type': lambda: (concept_properties.typing_concept, sa.Column(concept_properties.typing_concept,
                                                                              MITMDataType.Text.sa_sql_type,
                                                                              nullable=False)),
                'identity': lambda: [(name, sa.Column(name, dt.sa_sql_type, nullable=False)) for
                                     name, dt in
                                     mitm_def.resolve_identity_type(he_concept).items()],
                'inline': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for name, dt in
                                   mitm_def.resolve_inlined_types(he_concept).items()],
                'foreign': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for _, resolved_fk in
                                    mitm_def.resolve_foreign_types(he_concept).items() for name, dt in
                                    resolved_fk.items()],
                'attributes': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for name, dt in
                                       zip(he.attributes, he.attribute_dtypes)],
            }, gen_additional_schema_items=gen_foreign_key_constraints)

            if he_concept not in type_tables:
                type_tables[he_concept] = {}
            type_tables[he_concept][he.type_name] = t

    # for concept, members in concept_level_view_members.items():

    if gen_views:
        for name, queryable in gen_views(header.mitm, mitm_def, concept_tables, type_tables):
            views[name] = create_view(name, queryable, meta)

    # view_selection = sa.union_all(*(sa.select(*pk_cols) for pk_cols in members))

    #    views[concept] = view.create_materialized_view(mk_concept_table_name(header.mitm, concept), view_selection,

    #                                                   meta)

    return SQLRepresentationSchema(meta=meta, concept_tables=concept_tables, type_tables=type_tables, views=views)


def insert_db_instances(engine: sa.Engine, sql_rep_schema: SQLRepresentationSchema, mitm_data: MITMData):
    from mitm_tooling.transformation.df import pack_mitm_dataset, unpack_mitm_data
    h = mitm_data.header
    mitm = mitm_data.header.mitm
    mitm_def = get_mitm_def(mitm)
    mitm_dataset = unpack_mitm_data(mitm_data)
    with engine.connect() as conn:
        for concept, typed_dfs in mitm_dataset:
            concept_properties, concept_relations = mitm_def.get(concept)
            for type_name, type_df in typed_dfs.items():

                t_concept = sql_rep_schema.concept_tables[mitm_def.get_parent(concept)]
                ref_cols = pick_table_pk(mitm, concept, t_concept.columns)
                conn.execute(t_concept.insert(), type_df[[c.name for c in t_concept.columns]].to_dict('records'))

                if has_type_tables(mitm, concept):
                    #for typ, idx in df.groupby(concept_properties.typing_concept).groups.items():
                    #    type_df = df.loc[idx]
                    t_type = sql_rep_schema.type_tables[concept][type_name]
                    to_dict = type_df[[c.name for c in t_type.columns]].to_dict('records')
                    conn.execute(t_type.insert(), to_dict)

        conn.commit()


def insert_mitm_data(engine: sa.Engine, mitm_data: MITMData) -> SQLRepresentationSchema:
    sql_rep_schema = mk_db_schema(mitm_data.header)
    sql_rep_schema.meta.create_all(engine)
    insert_db_instances(engine, sql_rep_schema, mitm_data)
    return sql_rep_schema


def mk_sqlite(mitm_data: MITMData, file_path: FilePath | None = ':memory:') -> tuple[sa.Engine, SQLRepresentationSchema]:
    engine = create_sa_engine(AnyUrl(f'sqlite:///{str(file_path)}'))
    sql_rep_schema = insert_mitm_data(engine, mitm_data)
    # print([f'{t.name}: {t.columns} {t.constraints}' for ts in sql_rep_schema.type_tables.values() for t in ts.values()])
    return engine, sql_rep_schema
