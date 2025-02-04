import csv
from typing import TypeVar, Generic, List, Union, Generator, Callable, Annotated, Any

from pydantic import ValidationError, Field, BaseModel, \
    StringConstraints
from pydantic.v1.fields import ModelField

from ul_api_utils.const import CRON_EXPRESSION_VALIDATION_REGEX, MIN_UTC_OFFSET_SECONDS, MAX_UTC_OFFSET_SECONDS

NotEmptyListAnnotation = Annotated[list[Any], Field(min_length=1)]

class NotEmptyList(BaseModel):
    """Type that can be used in pydantic field, that will validate empty lists."""
    not_empty_list: NotEmptyListAnnotation


CronScheduleAnnotation = Annotated[str, StringConstraints(pattern=CRON_EXPRESSION_VALIDATION_REGEX)]

class CronScheduleStr(BaseModel):
    """Type that can be used in pydantic field, that will validate cron-formatted strings."""
    cron_schedule_str: CronScheduleAnnotation


WhiteSpaceStrippedStrAnnotation = Annotated[str, StringConstraints(strip_whitespace=True)]

class WhiteSpaceStrippedStr(BaseModel):
    """Type that can be used in pydantic field, that will strip whitespaces strings."""
    white_space_stripped_str: WhiteSpaceStrippedStrAnnotation


UTCOffsetSecondsAnnotation = Annotated[int, Field(ge=MIN_UTC_OFFSET_SECONDS, le=MAX_UTC_OFFSET_SECONDS)]

class UTCOffsetSeconds(BaseModel):
    """Type that can be used for pydantic fields to represent the offset from UTC."""
    utc_offset: UTCOffsetSecondsAnnotation

PgTypePasswordStrAnnotation = Annotated[str, StringConstraints(min_length=6, max_length=72)]

class PgTypePasswordStr(BaseModel):
    """Type that can be used for pydantic fields to represent password with length from 6 to 72 characters."""
    pg_type_password_str: PgTypePasswordStrAnnotation


PgTypeShortStrAnnotation = Annotated[str, StringConstraints(min_length=0, max_length=255)]

class PgTypeShortStr(BaseModel):
    """Type that can be used for pydantic fields to represent short string with length from 0 to 255 characters."""
    pg_type_short_str: PgTypeShortStrAnnotation


PgTypeLongStrAnnotation = Annotated[str, StringConstraints(min_length=0, max_length=1000)]

class PgTypeLongStr(BaseModel):
    """Type that can be used for pydantic fields to represent short string with length from 0 to 1000 characters."""
    pg_type_long_str: PgTypeLongStrAnnotation


PgTypeInt32Annotation = Annotated[int, Field(ge=-2147483648, le=2147483648)]

class PgTypeInt32(BaseModel):
    """Type that can be used for pydantic fields to represent int32 number."""
    pg_type_int32: PgTypeInt32Annotation


PgTypePositiveInt32Annotation = Annotated[int, Field(ge=0, le=2147483648)]

class PgTypePositiveInt32(BaseModel):
    """Type that can be used for pydantic fields to represent positive int32 number."""
    pg_type_positive_int32: PgTypePositiveInt32Annotation


PgTypeInt16Annotation = Annotated[int, Field(ge=-32768, le=32768)]

class PgTypeInt16(BaseModel):
    """Type that can be used for pydantic fields to represent int16 (SMALLINT) number."""
    pg_type_int16: PgTypeInt16Annotation


PgTypePositiveInt16Annotation = Annotated[int, Field(ge=0, le=32768)]

class PgTypePositiveInt16(BaseModel):
    """Type that can be used for pydantic fields to represent positive int16 (SMALLINT) number."""
    pg_type_positive_int16_annotation: PgTypePositiveInt16Annotation


QueryParamsSeparatedListValueType = TypeVar('QueryParamsSeparatedListValueType')


class QueryParamsSeparatedList(Generic[QueryParamsSeparatedListValueType]):
    """
    Supports cases when query parameters are being sent as a string, but you have to assume
    that it is a list.

    F.E. Query string is ?foo=1,2

    Note:
        Sent as a string, but interpreted as List.
    """

    def __init__(self, contains_type: QueryParamsSeparatedListValueType) -> None:
        self.contains_type = contains_type

    def __repr__(self) -> str:
        return f'QueryParamsSeparatedList({super().__repr__()})'

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Union[List[str], str], ModelField], Union[List[QueryParamsSeparatedListValueType], List[str]]], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, query_param: Union[List[str], str], field: ModelField) -> Union[List[QueryParamsSeparatedListValueType], List[str]]:
        if not isinstance(query_param, List):
            query_param = [query_param]
        reader = csv.reader(query_param, skipinitialspace=True)
        splitted = next(reader)
        if not field.sub_fields:
            return splitted
        list_item = field.sub_fields[0]  # retrieving info about data type of the list
        errors = []
        for value in splitted:
            validated_list_item, error = list_item.validate(value, {}, loc="separated query param")
            if error:
                errors.append(error)
        if errors:
            raise ValidationError(errors, cls)
        # Validation passed without errors, modify string to a list and cast the right type for every element
        return [list_item.type_(value) for value in splitted]
