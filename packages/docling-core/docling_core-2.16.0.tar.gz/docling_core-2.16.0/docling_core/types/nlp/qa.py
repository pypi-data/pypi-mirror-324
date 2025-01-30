#
# Copyright IBM Corp. 2024 - 2024
# SPDX-License-Identifier: MIT
#

"""Define the model for Q&A pairs."""
from typing import Generic, Optional

from pydantic import BaseModel, Field, StrictBool, StrictStr

from docling_core.search.mapping import es_field
from docling_core.types.base import DescriptionAdvancedT, StrictDateTime, UniqueList
from docling_core.types.nlp.qa_labels import QALabelling


class QAPair(BaseModel, Generic[DescriptionAdvancedT]):
    """A representation of a question-answering (QA) pair."""

    context: StrictStr = Field(
        description=(
            "A single string containing the context of the question enabling the"
            " presentation of the answer."
        )
    )
    question: StrictStr = Field(description="A question on the given context.")
    answer: StrictStr = Field(
        description="The answer to the question from the context."
    )
    short_answer: Optional[StrictStr] = Field(
        default=None, description="Alternative and concise answer."
    )
    retrieved_context: Optional[StrictBool] = Field(
        default=False,
        description="Whether the context was retrieved from the question.",
    )
    generated_question: Optional[StrictBool] = Field(
        default=False, description="Whether the question was generated by an AI model."
    )
    generated_answer: Optional[StrictBool] = Field(
        default=False, description="Whether the answer was generated by an AI model."
    )
    created: StrictDateTime = Field(
        description="Datetime when the QA pair was created ."
    )
    user: Optional[StrictStr] = Field(
        default=None,
        description=(
            "Unique identifier of the user that created or curated this QA pair."
        ),
        json_schema_extra=es_field(type="keyword", ignore_above=8191),
    )
    model: Optional[StrictStr] = Field(
        default=None,
        description="Unique identifier of the model used to generate this QA pair.",
        json_schema_extra=es_field(type="keyword", ignore_above=8191),
    )
    paths: UniqueList[StrictStr] = Field(
        description=(
            "One or more references to a document that identify the provenance of the"
            " QA pair context."
        ),
        examples=[
            "badce7c84d0ba7ba0fb5e94492b0d91e2506a7cb48e4524ad572c546a35f768e#/"
            "main-text/4"
        ],
        json_schema_extra=es_field(type="keyword", ignore_above=8191),
    )
    advanced: Optional[DescriptionAdvancedT] = Field(
        default=None,
        description="Document metadata to provide more details on the context.",
    )
    labels: Optional[QALabelling] = Field(
        default=None, description="QApair labelling axes."
    )
