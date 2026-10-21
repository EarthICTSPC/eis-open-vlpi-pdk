# EIS-KKA-001 — Lean 4 Interference Contract

**Version:** 0.1.0  
**Status:** specified; software reference only  
**Scope:** scalar signed interference term, not full KKA attention and not physical-device validation.

## Frozen convention

For complex fields a,b, the signed cross term is **X(a,b) = 2 Re(a conjugate(b))**. For a=ar+i ai and b=br+i bi, **X(a,b) = 2(ar br + ai bi)**.

The factor of two is explicit. Do not silently substitute Re(a conjugate(b)), total intensity |a+b|², or a clipped/nonnegative value. The signed cross term can be negative.

## Contents and run

- `EISKKA001.lean`: dependency-free Lean 4 definition on exact integer field fixtures, with basic proved properties.
- `tests/test_conformance.py`: executable Python suite for fixtures and floating-point phase response.
- `lakefile.toml`, `lean-toolchain`: Lean 4.19.0 project metadata.

From this directory:

```sh
lake build
python -m unittest discover -s tests -v
```


## Language and array-layout neutrality

The normative contract describes logical values and operations, not a language's memory order. Julia's dense multidimensional arrays are column-major (the first index varies fastest in contiguous storage); NumPy's default arrays are commonly row-major, and tensor libraries can also represent non-default strides. These are storage/layout conventions, not different mathematical meanings. Any future tensor-level contract must name axes, shapes, and indexing semantics explicitly; each backend adapter must document strides, transposes, copies, and layout conversions. Do not choose Julia or PyTorch merely to inherit a particular matrix-storage convention.

## Evidence boundary

The suite checks aligned, quadrature, anti-aligned and zero-field cases, symmetry, phase response, and a magnitude bound. Passing it does **not** establish equivalence to every Tian et al. equation; full attention semantics, normalization, training behavior, LLM quality; a formal Lean-to-Python equivalence; or performance/compatibility of a physical device.

Lean uses integer-valued field fixtures to avoid an external math library. Python extends the same scalar formula to floating-point complex values. This is a reviewed starting contract, not yet a proved bridge between numeric representations. Future versions must separately define tensor shape/batch semantics, full attention integration, approximation/error budgets, and device-response parameters with provenance.
