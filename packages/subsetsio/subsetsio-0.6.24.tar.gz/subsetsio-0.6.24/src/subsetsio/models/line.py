from enum import Enum
from typing import List, Literal, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Literal, Optional, Union, Any
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Optional, Dict, Union, List, Literal, Any
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from .common import BaseChartMetadata, BaseChartProperties, ChartType, Color, AxisConfig, NumericAxisConfig
import pandas as pd
from .df_validation import validate_linechart_df


class LineStyle(str, Enum):
    """Available line styles for the chart"""
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"

class LineChartDatasetConfig(BaseModel):
    """Configuration for each dataset in the line chart"""
    label: str = Field(..., min_length=1, max_length=100)
    line_style: LineStyle = Field(default=LineStyle.SOLID)
    color: Color = Field(default="#000000")
    point_size: int = Field(default=4, ge=2, le=10)


class LineChartMetadata(BaseChartMetadata):
    """Metadata specific to line charts"""
    type: Literal[ChartType.LINE]
    dataset_configs: Optional[List[LineChartDatasetConfig]] = None
    x_axis: Optional[AxisConfig] = None
    y_axis: Optional[NumericAxisConfig] = None
    connect_null_points: bool = Field(default=False)
    interpolation: Literal["linear", "smooth"] = Field(default="linear")
    stacked: bool = Field(default=False)

class LineChartData(List[List[Any]]):
    """A 2D list type with line chart data validation"""
    

    def __init__(self, data: List[List[Any]]):
        df = pd.DataFrame(data)
        is_valid, error_message = validate_linechart_df(df)
        if not is_valid:
            raise ValueError(error_message)
        super().__init__(data)


    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        def validate_list_data(data: List[List[Any]], info: Any) -> List[List[Any]]:
            df = pd.DataFrame(data)
            is_valid, error_message = validate_linechart_df(df)
            if not is_valid:
                raise ValueError(error_message)
            return data

        base_schema = core_schema.list_schema(
            items_schema=core_schema.list_schema(
                items_schema=core_schema.any_schema()
            )
        )

        return core_schema.json_or_python_schema(
            json_schema=base_schema,
            python_schema=core_schema.union_schema(
                choices=[
                    core_schema.is_instance_schema(cls),
                    core_schema.with_info_plain_validator_function(validate_list_data)
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                function=lambda x: list(x),
                return_schema=base_schema,
                when_used='json'
            )
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _core_schema: CoreSchema,
        _handler: GetCoreSchemaHandler,
    ) -> JsonSchemaValue:
        return {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "any"}
            }
        }

class LineChart(BaseChartProperties):
    """Line chart model combining metadata and data"""
    metadata: LineChartMetadata
    data: LineChartData