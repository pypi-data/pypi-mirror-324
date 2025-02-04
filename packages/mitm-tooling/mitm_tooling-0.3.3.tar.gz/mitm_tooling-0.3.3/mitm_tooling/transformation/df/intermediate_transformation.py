import itertools
from collections import defaultdict
from collections.abc import Sequence, Iterable

import pandas as pd

from mitm_tooling.data_types import convert, MITMDataType
from mitm_tooling.definition import get_mitm_def, MITM, ConceptName
from mitm_tooling.definition.definition_tools import map_col_groups
from mitm_tooling.representation import MITMData, MITMDataset, Header
from mitm_tooling.representation import mk_concept_file_header
from mitm_tooling.representation.common import guess_k_of_header_df, mk_header_file_columns


def pack_typed_dfs_as_concept_table(mitm: MITM, concept: ConceptName, dfs: Iterable[pd.DataFrame]) -> pd.DataFrame:
    normalized_dfs = []
    for df in dfs:
        base_cols, col_dts = mk_concept_file_header(mitm, concept, 0)
        attr_cols = set(df.columns) - set(base_cols)
        k = len(attr_cols)
        normal_form_cols = list(base_cols) + list(attr_cols)
        df = df.reindex(columns=normal_form_cols)
        df = convert.convert_df(df, col_dts | {c: MITMDataType.Unknown for c in attr_cols})
        squashed_form_cols = mk_concept_file_header(mitm, concept, k)[0]
        df.columns = squashed_form_cols
        normalized_dfs.append((df, k))

    assert len(normalized_dfs) > 0
    max_k = max(normalized_dfs, key=lambda x: x[1])[1]

    squashed_form_cols = mk_concept_file_header(mitm, concept, max_k)[0]
    return pd.concat([df for df, _ in normalized_dfs], axis='rows', ignore_index=True).reindex(
        columns=squashed_form_cols)


def unpack_concept_table_as_typed_dfs(header: Header, concept: ConceptName, df: pd.DataFrame) -> dict[
    str, pd.DataFrame]:
    mitm_def = get_mitm_def(header.mitm)
    concept_properties, concept_relations = mitm_def.get(concept)

    with_header_entry = {}
    if concept_properties.is_abstract:  # e.g. MAED.observation
        for (key, typ), idx in df.groupby(['kind', concept_properties.typing_concept]).groups.items():
            key, type_name = str(key), str(typ)
            specific_concept = mitm_def.inverse_concept_key_map[key]
            he = header.get(specific_concept, type_name)
            assert he is not None, 'missing type entry in header'
            with_header_entry[(specific_concept, type_name)] = (he, df.loc[idx])
    else:
        for typ, idx in df.groupby(concept_properties.typing_concept).groups.items():
            type_name = str(typ)
            he = header.get(concept, type_name)
            assert he is not None, 'missing type entry in header'
            with_header_entry[(concept, type_name)] = (he, df.loc[idx])

    res = {}
    for (concept, type_name), (he, type_df) in with_header_entry.items():
        k = he.get_k()
        base_cols, base_dts = mk_concept_file_header(header.mitm, concept, 0)
        normal_form_cols, _ = mk_concept_file_header(header.mitm, concept, k)
        type_df = type_df.reindex(columns=normal_form_cols)

        unpacked_cols = list(base_cols) + list(he.attributes)
        unpacked_dts = base_dts | dict(zip(he.attributes, he.attribute_dtypes))
        type_df.columns = unpacked_cols

        res[he.type_name] = convert.convert_df(type_df, unpacked_dts)

    return res


def unpack_mitm_data(mitm_data: MITMData) -> MITMDataset:
    mitm_data = mitm_data.as_specialized()
    return MITMDataset(header=mitm_data.header,
                       dfs={concept: unpack_concept_table_as_typed_dfs(mitm_data.header, concept, df) for concept, df in
                            mitm_data})


def pack_mitm_dataset(mitm_dataset: MITMDataset) -> MITMData:
    return MITMData(header=mitm_dataset.header, concept_dfs={concept:
        pack_typed_dfs_as_concept_table(
            mitm_dataset.header.mitm, concept,
            typed_dfs.values()) for concept, typed_dfs in
        mitm_dataset if len(typed_dfs) > 1}).as_generalized()
