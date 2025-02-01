#!/bin/env python3
"""
Export Myokit MMT files to Pigreads C++ code
--------------------------------------------
"""

from __future__ import annotations

from typing import Any

import myokit as mk  # type: ignore[import-not-found]
import yaml
from myokit.formats.opencl import (  # type: ignore[import-not-found]
    OpenCLExpressionWriter,
)


def str_presenter(dumper, data):
    """
    A YAML string presenter that uses block style for multiline strings.
    """
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


class PigreadsMyokitWriter:
    """
    This class implements the conversion of a Myokit model to Pigreads
    compatible C++ code.

    :param model: The Myokit model to convert.
    :param meta: A dictionary with metadata to include in the generated code.
    :param double_precision: If ``True``, use double precision for calculations.

    :var model: The Myokit model to convert.
    :vartype model: myokit.Model
    :var exwr: The C++ expression writer.
    :vartype exwr: myokit.formats.opencl.OpenCLExpressionWriter
    :var states: The list of states in the model.
    :vartype states: list[mk.State]
    :var meta: A dictionary with metadata to include in the generated code.
    :vartype meta: dict[str, Any]
    :var double_precision: If ``True``, use double precision for calculations.
    :vartype double_precision: bool
    """

    def __init__(
        self, model: mk.Model, meta: dict[str, Any], double_precision: bool = False
    ):  # pylint: disable=redefined-outer-name
        self.model = model
        if double_precision:
            self.exwr = OpenCLExpressionWriter(
                precision=mk.DOUBLE_PRECISION, native_math=False
            )
        else:
            self.exwr = OpenCLExpressionWriter(
                precision=mk.SINGLE_PRECISION, native_math=True
            )
        self.exwr.set_lhs_function(self.lhs_format)
        self.states = list(model.states())
        self.meta = meta
        self.generate_variable_abbreviations()

    @property
    def diffusivities(self) -> dict[str, float]:
        """
        The diffusivities of the model as defined in the metadata.
        """
        d = self.meta.get("diffusivity", {})
        assert isinstance(d, dict)
        return d

    def get_ivar(self, varname: str) -> int:
        """
        Get the index of a state variable by its name.

        :param varname: The name of the state variable.
        :return: The index of the state variable.
        """
        return next(
            i
            for i, state in enumerate(self.states)
            if str(self.lhs_format(state)) == varname
        )

    @staticmethod
    def nodots(s: Any) -> str:
        """
        Convert an object to string and replace dots by underscores.

        :param s: any object to represent as a string.
        """
        return str(s).replace(".", "_")

    def lhs_format(self, x: mk.LhsExpression):
        """
        Format a left-hand side expression.

        :param x: The left-hand side expression to format.
        :return: The formatted left-hand side expression.
        """
        assert not isinstance(x, mk.Derivative), "Can not handle derivatives here."
        if isinstance(x, mk.Name):
            return self.lhs_format(x.var())
        s = self.nodots(x)
        return self.variable_abbreviations.get(s, s)

    def state_equation(self, q: mk.Equation):
        """
        Format a state equation.

        :param q: The state equation to format.
        :return: The formatted state equation.
        """
        w = q.lhs.walk()
        next(w)
        v = next(w)
        vin = str(self.lhs_format(v))
        rhs = str(self.exwr.ex(q.rhs))
        if vin in self.diffusivities:
            rhs += f" + _diffuse_{vin}"
        return f"*_new_{vin} = {vin} + dt*({rhs});"

    def generate_variable_abbreviations(self) -> None:
        """
        Create a dictionary abbreviating long variable names if this
        is possible unambiguously. Short variable names are the last part of the
        long variable name after a dot.
        """
        variables = dict(
            zip(self.model.states(), self.model.initial_values(as_floats=True))
        )
        variables_long = {self.nodots(v): f for v, f in variables.items()}
        variables_short = {}
        for variable, value in variables.items():
            short_varname = str(variable).rsplit(".", maxsplit=1)[-1]
            if short_varname not in variables_short:
                variables_short[short_varname] = value
            else:
                variables_short = variables_long
                break
        self.variables = variables_short
        self.variable_abbreviations = dict(
            zip(variables_long.keys(), variables_short.keys())
        )

    def __str__(self) -> str:
        """
        Convert the model to a string. This is the main entry point for the
        conversion.

        :return: The model as a string.
        """
        parameters = {
            self.lhs_format(q.lhs): float(q.rhs)
            for block in self.model.solvable_order().values()
            for q in block
            if q.rhs.is_constant()
        }

        meta = {  # pylint: disable=redefined-outer-name
            "name": rf"{self.model.name()} (exported from Myokit)",
            "description": str(self.model.meta.get("desc", "")),
            "dois": [],
            "variables": self.variables,
            "parameters": parameters,
            **self.meta,
        }

        step = []
        for blockname, block in self.model.solvable_order().items():
            block_ = [eq for eq in block if not eq.rhs.is_constant()]
            if len(block_) < 1:
                continue
            step.append("")
            step.append(f"// {blockname}")
            for q in block_:
                if q.lhs.is_derivative():
                    step.append(self.state_equation(q))
                else:
                    step.append("const Real " + self.exwr.eq(q) + ";")

        meta["source"] = "\n".join(step).strip()
        return yaml.safe_dump(meta, sort_keys=False, indent=2, allow_unicode=True)


if __name__ == "__main__":
    import sys
    from pathlib import Path

    model, protocol, script = mk.load(sys.argv[1])
    with Path(sys.argv[2]).open("r", encoding="utf-8") as f:
        meta = yaml.safe_load(f)
    writer = PigreadsMyokitWriter(model, meta, double_precision=sys.argv[3] == "double")
    with Path(sys.argv[4]).open("w", encoding="utf-8") as f:
        f.write(str(writer))
