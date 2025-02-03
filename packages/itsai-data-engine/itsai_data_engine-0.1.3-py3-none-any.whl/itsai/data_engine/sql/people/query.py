import dataclasses
import json
from collections.abc import Callable, Sequence

import jinja2
import pandas as pd
import pydantic
import sqlalchemy as sa
from langchain.chat_models.base import BaseChatModel
from langchain.output_parsers import PydanticOutputParser
from langchain_core.vectorstores import VectorStore


class JobRole(pydantic.BaseModel):
    title: str
    unit: str


class JobRoles(pydantic.BaseModel):
    roles: list[JobRole]


@dataclasses.dataclass(frozen=True)
class RetrievalConfig:
    top_k: int = 50


@dataclasses.dataclass(frozen=True)
class ColumnConfig:
    title: str
    unit: str


_RERANKING_PROMPT = jinja2.Template("""
You are an expert in selecting and ranking the most relevant job titles and roles to a specific query on employees in the world bank.
You are provided the query in <query> tags below, and job role records in <candidate_roles> tags below.

Select upto the top {{ n_role_choices }} most relevant roles from the options, selecting as few as possible.
If none are applicable or relevant, return the empty list.

<query>
{{ query }}
</query>

<candidate_roles>
{{ candidate_roles }}
</candidate_roles>

Select the acronym/code field for unit.
{{ format_instructions }}
""")


@dataclasses.dataclass(frozen=True)
class Retriever:
    title: VectorStore
    full_role: VectorStore
    title_config: RetrievalConfig = RetrievalConfig()
    full_role_config: RetrievalConfig = RetrievalConfig()


@dataclasses.dataclass(frozen=True)
class RerankingConfig:
    prompt: jinja2.Template = _RERANKING_PROMPT
    max_roles: int = 25
    n_choices: int = 3


@dataclasses.dataclass(frozen=True)
class _Result:
    """Internal container for debugging purposes only"""

    titles: Sequence[str]
    full_roles: pd.DataFrame
    candidates: pd.DataFrame
    output_roles: JobRoles


def _custom_title_augmenter(query: str) -> Sequence[str]:
    titles: list[str] = []
    if 'director' in query.lower():
        titles.append('Director')
    return titles


_TitleAugmenter = Callable[[str], Sequence[str]]


async def retrieve(
    search_query: str,
    connection: sa.Connection,
    table: str,
    sql_filters: ColumnConfig,
    result_columns: Sequence[str],
    retriever: Retriever,
    llm: BaseChatModel,
    vector_fields: ColumnConfig,
    rerank_config: RerankingConfig,
    title_augmenter: _TitleAugmenter = _custom_title_augmenter,
) -> pd.DataFrame:
    """Return table with staff retrieved based on search query.

    Parameters
    ----------
    search_query: question being asked
    """
    roles = await _retrieve_roles(
        search_query, retriever, llm, vector_fields, rerank_config, title_augmenter
    )
    sql = _generate_sql_filter_query(
        roles.output_roles,
        table,
        sql_filters.unit,
        sql_filters.title,
    )
    staff = _retrieve_data(connection, sql, result_columns)
    return staff


async def _retrieve_roles(
    query: str,
    retriever: Retriever,
    llm: BaseChatModel,
    columns: ColumnConfig,
    rerank_config: RerankingConfig,
    title_augmenter: _TitleAugmenter,
) -> _Result:
    # TODO: enable async later
    # for some reason, raises keyerror in _asimple_search method of azuresearch in langchain
    task1 = retriever.title.similarity_search_with_relevance_scores(
        query, retriever.title_config.top_k
    )
    full_roles = retriever.full_role.similarity_search_with_relevance_scores(
        query, retriever.full_role_config.top_k
    )
    _titles = [r[0].page_content for r in task1]
    titles = [*_titles, *title_augmenter(query)]

    _df = pd.DataFrame.from_records(
        [json.loads(res[0].page_content) for res in full_roles]
    )
    candidates = _df[_df[columns.title].isin(titles)].head(rerank_config.max_roles)
    roles = await _rerank(
        llm, query, candidates, rerank_config.prompt, rerank_config.n_choices
    )
    return _Result(titles, _df, candidates, roles)


def _retrieve_data(
    conn: sa.Connection, filtered: sa.Select, columns: Sequence[str]
) -> pd.DataFrame:
    statement = sa.select(*[sa.column(col) for col in columns]).select_from(
        filtered.cte('filtered')
    )
    df = pd.read_sql(statement, conn)
    return df


def _generate_sql_filter_query(
    roles: JobRoles, table: str, unit: str, title: str
) -> sa.Select:
    table_ = sa.table(table)
    unit_ = sa.column(unit, sa.Text)
    title_ = sa.column(title, sa.Text)
    sa.select('*').select_from(table_).where()

    conditions = [
        (sa.and_(unit_ == role.unit, title_ == role.title)) for role in roles.roles
    ]
    query = sa.select('*').select_from(table_).where(sa.or_(*conditions))
    return query


async def _rerank(
    llm: BaseChatModel,
    query: str,
    candidates: pd.DataFrame,
    prompt_template: jinja2.Template,
    n_choices: int,
) -> JobRoles:
    parser = PydanticOutputParser(pydantic_object=JobRoles)
    # we are choosing records as the model is getting confused by variations
    # in title when passing CSV
    # as the header is a long way from the actual data
    prompt = prompt_template.render(
        query=query,
        n_role_choices=n_choices,
        candidate_roles=candidates.to_dict('records'),
        format_instructions=parser.get_format_instructions(),
    )
    chain = llm | parser

    result = await chain.ainvoke(prompt)
    return result
