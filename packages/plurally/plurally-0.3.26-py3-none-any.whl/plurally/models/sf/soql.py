from enum import Enum
from typing import List
from pydantic import BaseModel

class SalesforceSOQLComparisonOperatorSingle(Enum):
    EQUALS = "="
    NOT_EQUALS = "!="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LIKE = "LIKE"


class SalesforceSOQLComparisonOperatorMulti(Enum):
    IN = "IN"
    NOT_IN = "NOT IN"
    INCLUDES = "INCLUDES"
    EXCLUDES = "EXCLUDES"


class SalesforceSOQLLogicalOperator(Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class SalesforceSOQLFilterSingle(BaseModel):
    field: str
    operator: SalesforceSOQLComparisonOperatorSingle
    value: str

    def __str__(self):
        return f"{self.field} {self.operator.value} '{self.value}'"
    


class SalesforceSOQLFilterMulti(BaseModel):
    field: str
    operator: SalesforceSOQLComparisonOperatorMulti
    values: List[str]

    def __str__(self):
        enclosed = [f"'{v}'" for v in self.values]
        return f"{self.field} {self.operator.value} ({', '.join(enclosed)})"
    
SalesforceSOQLFilter = SalesforceSOQLFilterSingle | SalesforceSOQLFilterMulti