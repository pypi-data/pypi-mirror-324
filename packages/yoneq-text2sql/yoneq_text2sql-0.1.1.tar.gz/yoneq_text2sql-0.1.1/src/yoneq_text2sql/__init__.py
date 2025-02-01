import dataclasses
import json
import os
from dataclasses import dataclass
from typing import Callable, List, Tuple, Union

import pandas as pd
import requests
import plotly.graph_objs

from .exceptions import (
    OTPCodeError,
    ValidationError,
)
from .types import (
    ApiKey,
    Status,
    TrainingData,
    UserEmail,
    UserOTP,
)
from .utils import sanitize_model_name, validate_config_path

api_key: Union[str, None] = None  # API key

fig_as_img: bool = False  # Whether or not to return Plotly figures as images

run_sql: Union[
    Callable[[str], pd.DataFrame], None
] = None  # Function to convert SQL to a Pandas DataFrame
"""
**Example**
```python
t2s.run_sql = lambda sql: pd.read_sql(sql, engine)
```

Set the SQL to DataFrame function for Text2SQL. This is used in the [`t2s.ask(...)`][Text2Sql.ask] function.
Instead of setting this directly you can also use [`t2s.connect_to_snowflake(...)`][Text2Sql.connect_to_snowflake] to set this.

"""

__org: Union[str, None] = None  # Organization name


def __dataclass_to_dict(obj):
    return dataclasses.asdict(obj)


@dataclass
class TrainingPlanItem:
    item_type: str
    item_group: str
    item_name: str
    item_value: str

    def __str__(self):
        if self.item_type == self.ITEM_TYPE_SQL:
            return f"Train on SQL: {self.item_group} {self.item_name}"
        elif self.item_type == self.ITEM_TYPE_DDL:
            return f"Train on DDL: {self.item_group} {self.item_name}"
        elif self.item_type == self.ITEM_TYPE_IS:
            return f"Train on Information Schema: {self.item_group} {self.item_name}"

    ITEM_TYPE_SQL = "sql"
    ITEM_TYPE_DDL = "ddl"
    ITEM_TYPE_IS = "is"


class TrainingPlan:
    """
    A class representing a training plan. You can see what's in it, and remove items from it that you don't want trained.

    **Example:**
    ```python
    plan = t2s.get_training_plan()

    plan.get_summary()
    ```

    """

    _plan: List[TrainingPlanItem]

    def __init__(self, plan: List[TrainingPlanItem]):
        self._plan = plan

    def __str__(self):
        return "\n".join(self.get_summary())

    def __repr__(self):
        return self.__str__()

    def get_summary(self) -> List[str]:
        """
        **Example:**
        ```python
        plan = t2s.get_training_plan()

        plan.get_summary()
        ```

        Get a summary of the training plan.

        Returns:
            List[str]: A list of strings describing the training plan.
        """

        return [f"{item}" for item in self._plan]

    def remove_item(self, item: str):
        """
        **Example:**
        ```python
        plan = t2s.get_training_plan()

        plan.remove_item("Train on SQL: What is the average salary of employees?")
        ```

        Remove an item from the training plan.

        Args:
            item (str): The item to remove.
        """
        for plan_item in self._plan:
            if str(plan_item) == item:
                self._plan.remove(plan_item)
                break
