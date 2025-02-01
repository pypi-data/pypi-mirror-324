#!/bin/env python3
"""
Convert a full model YAML file to a C++ header file for OpenCL to use in
Pigreads.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from textwrap import dedent, indent

import yaml


def str_presenter(dumper, data):
    """
    A YAML string presenter that uses block style for multiline strings.
    """
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

if __name__ == "__main__":
    path = Path(sys.argv[1])
    with path.open("r", encoding="utf-8") as f:
        model = yaml.safe_load(f)

    key = model["key"] = re.sub(r"\.(model|float|double)$", "", path.stem)

    source = model["source"]
    del model["source"]

    if "diffusivity" not in model:
        model["diffusivity"] = {}
    if "parameters" not in model:
        model["parameters"] = {}

    diffusivity_by_varname = model["diffusivity"]
    diffusivity = {
        "diffusivity_" + varname: value
        for varname, value in diffusivity_by_varname.items()
    }
    model["parameters"] = {**diffusivity, **model["parameters"]}
    del model["diffusivity"]

    model["description"] = dedent(model.get("description", "")).strip()

    with Path(sys.argv[2]).open("w", encoding="utf-8") as f:
        f.write(
            dedent(rf"""
            #ifndef __OPENCL_VERSION__
            const std::string Model_{key}_info = R"model(
        """).strip()
            + "\n"
        )
        f.write(
            yaml.safe_dump(
                {key: model}, sort_keys=False, indent=2, allow_unicode=True
            ).strip()
            + "\n"
        )
        f.write(
            dedent(rf"""
            )model";
            #endif

            static const Size Model_{key}_id = UNIQUE_ID;
            static const Size Model_{key}_Nv = {len(model["variables"])};
            static const Size Model_{key}_Np = {len(model["parameters"])};

            #ifdef __OPENCL_VERSION__
            void Model_{key}_step(
                    Real* const params,
                    struct States weights,
                    struct States states_old,
                    struct States states_new,
                    const Real dt
            ) {{
        """).strip()
            + "\n"
        )
        for ip, param in enumerate(model["parameters"]):
            f.write(f"  const Real {param} = params[{ip}];\n")
        for ivar, varname in enumerate(model["variables"]):
            f.write(f"  const Real {varname} = _r(_v({ivar}, states_old));\n")
            f.write(f"  Real* const _new_{varname} = _pr(_v({ivar}, states_new));\n")
            if varname in diffusivity_by_varname:
                f.write(
                    f"  const Real _diffuse_{varname} = diffusivity_{varname} "
                    + f"* diffuse(weights, _v({ivar}, states_old));\n"
                )
        f.write("\n" + indent(source.strip(), "  ") + "\n")
        f.write(
            dedent(rf"""
            }}
            #endif

            #ifdef __OPENCL_VERSION__
            __kernel void Model_{key}_kernel(
                    Size model_count,
                    __global Size* model_ids,
                    __global Size* model_offsets,
                    __global Real* model_params,
                    __global void* inhom_data,      struct StatesIdx inhom_idx,
                    __global void* weights_data,    struct StatesIdx weights_idx,
                    __global void* states_old_data, struct StatesIdx states_old_idx,
                    __global void* states_new_data, struct StatesIdx states_new_idx,
                    const Real dt
            ) {{

              struct States inhom      = {{inhom_data,      STATES_UNPACK(inhom_idx)}};
              struct States weights    = {{weights_data,    STATES_UNPACK(weights_idx)}};
              struct States states_old = {{states_old_data, STATES_UNPACK(states_old_idx)}};
              struct States states_new = {{states_new_data, STATES_UNPACK(states_new_idx)}};

              const Size iz = get_global_id(0);
              const Size iy = get_global_id(1);
              const Size ix = get_global_id(2);

              if (ix < states_old.Nx && iy < states_old.Ny && iz < states_old.Nz) {{
                const Int inhom_zyx = _i(States_offset(inhom, 0, iz, iy, ix, 0));
                if (inhom_zyx > 0) {{
                  const Size imodel = (inhom_zyx - 1) % model_count;
                  const Size model_id = model_ids[imodel];
                  if (model_id == Model_{key}_id) {{
                    Real* params = model_params + model_offsets[imodel];
                    struct States w = States_offset(weights, 0, iz, iy, ix, 0);
                    struct States u = States_offset(states_old, 0, iz, iy, ix, 0);
                    struct States u_ = States_offset(states_new, 0, iz, iy, ix, 0);
                    Model_{key}_step(params, w, u, u_, dt);
                  }}
                }}
              }}
            }}
            #endif
        """).strip()
            + "\n"
        )
