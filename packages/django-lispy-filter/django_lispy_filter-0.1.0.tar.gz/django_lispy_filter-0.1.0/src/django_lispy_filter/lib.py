from typing import Union, List, Dict, Callable, Any
import json
from django.db.models import Q
from django.db.models.functions.text import Value
import sexpdata

class LispyFilterParser:
    """Parser for S-expression based Django filters with function support."""
    functions: Dict[str, Callable]
    
    def __init__(self):
        self.functions = {
            'range': lambda x, y: (x, y, ),
        }
        
    def register_function(self, name: str, func: Callable):
        """Register a custom function for use in filter expressions."""
        self.functions[name] = func

    def parseJson(self, raw_exp) -> Q:
        """Parse an JSON string or array into a Django Q object.
        
        JSON array format:
            ["and", ["=", "A", 1], ["=", "B", 2]]
               -> Q(A=1) & Q(B=2)
            ["or", ["=", "A__gt", 2], ["not", ["=", "B__gt", 3]]]
               -> Q(A__gt=2) | ~Q(B__gt=3)
        """
        if isinstance(raw_exp, str):
            exp = json.loads(raw_exp)
            res = self._parse_json_exp(exp)
        else:
            res = self._parse_json_exp(raw_exp)
            
        if not isinstance(res, Q):
            raise ValueError(f"The returned result is not Q type: {res}")
        return res
        
        
    
    def parseSexp(self, raw_exp: Union[str, list]) -> Q:
        """Parse an S-expression string or JSON array into a Django Q object.
        
        Examples:
            S-expression format:
                "(and (= A 1) (= B 2))"
                   -> Q(A=1) & Q(B=2)
                "(xor (= A 1) (= B 2))"
                   -> Q(A=1) ^ Q(B=2)
        
        NOTE we uses `true` for true and `false` for false
        since by default nil return `[]`, we here don't parse
        `nil` using sexpdata (it will become a Symbol)
        """

        exp = sexpdata.loads(raw_exp, nil=None, true='true', false='false')
        res = self._parse_s_exp(exp)
        
        if not isinstance(res, Q):
            raise ValueError(f"The returned result is not Q type: {res}")
        return res
    
    def _parse_s_exp(self, exp) -> Q:
        """Recursively parse S-expression into Q objects."""
        if not exp: # empty list
            return Q()
        
        if not isinstance(exp, list):
            return self._parse_s_value(exp)
            
        operator = exp[0].value() if isinstance(exp[0], sexpdata.Symbol) else exp[0]
        args = exp[1:]
        
        # Logical operators
        if operator == 'and':
            result = Q()
            for arg in args:
                result &= self._parse_s_exp(arg)
            return result
            
        elif operator == 'or':
            result = Q()
            for arg in args:
                result |= self._parse_s_exp(arg)
            return result
            
        elif operator == 'not':
            if len(args) != 1:
                raise ValueError("'not' operation requires exactly one argument")
            return ~self._parse_s_exp(args[0])
            
        elif operator == 'xor':
            if len(args) != 2:
                raise ValueError("'xor' operation requires exactly two arguments")
            return self._parse_s_exp(args[0]) ^ self._parse_s_exp(args[1])
            
        # Comparison operator
        elif operator == '=':
            if len(args) != 2:
                raise ValueError("'=' operation requires exactly two arguments")
            field = self._parse_s_value(args[0])
            value = args[1]
            if isinstance(value, list):
               value = self._parse_s_exp(value)
            else:
                value = self._parse_s_value(args[1])
            return Q(**{field: value})
            
        # Function call
        elif operator in self.functions:
            return self._parse_s_function(exp)
        else:
            raise ValueError(f"Unknown operator: {repr(operator)}")
    
    def _parse_s_value(self, value) -> Any:
        """Parse a value from the S-expression."""
        if isinstance(value, sexpdata.Symbol):
            v = value.value()
            if (v == 'nil'):
                return None
            return v
        elif isinstance(value, (str, int)): # note bool is also int
            return value
        elif isinstance(value, sexpdata.Brackets):
            return self._parse_s_function(value.I)
        elif isinstance(value, list):
            return self._parse_s_function(value)
        raise ValueError(f"Cannot be parsed: `{value}`")

    def _parse_s_function(self, value: list) -> Any:
        operator = value[0].value() if isinstance(value[0], sexpdata.Symbol) else value[0]
        args = value[1:]
        if operator in self.functions:
            parsed_args = [self._parse_s_value(arg) for arg in args]
            return self.functions[operator](*parsed_args)
        else:
            raise ValueError(f"Unknown operator: {repr(operator)}")


    
    def _parse_json_exp(self, exp) -> Q:
        """Parse JSON array format into Q objects."""
        if not exp:  # empty list
            return Q()
            
        if not isinstance(exp, list):
            return exp
            
        operator = exp[0]
        args = exp[1:]
        
        # Logical operators
        if operator == 'and':
            result = Q()
            for arg in args:
                result &= self._parse_json_exp(arg)
            return result
            
        elif operator == 'or':
            result = Q()
            for arg in args:
                result |= self._parse_json_exp(arg)
            return result
            
        elif operator == 'not':
            if len(args) != 1:
                raise ValueError("'not' operation requires exactly one argument")
            return ~self._parse_json_exp(args[0])
            
        elif operator == 'xor':
            if len(args) != 2:
                raise ValueError("'xor' operation requires exactly two arguments")
            return self._parse_json_exp(args[0]) ^ self._parse_json_exp(args[1])
            
        # Comparison operator
        elif operator == '=':
            if len(args) != 2:
                raise ValueError("'=' operation requires exactly two arguments")
            field = args[0]
            value = args[1]
            if isinstance(value, list):
                value = self._parse_json_exp(value)
            return Q(**{field: value})
            
        # Function call
        elif operator in self.functions:
            return self._parse_json_function(exp)
            
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def _parse_json_function(self, value: list):
        operator = value[0]
        args = value[1:]
        if operator in self.functions:
            args = [
                self._parse_json_function(arg)
                if isinstance(arg, list) else arg
                for arg in args
            ]
            
            return self.functions[operator](*args)
        else:
            raise ValueError(f"Unknown operator: {repr(operator)}")


