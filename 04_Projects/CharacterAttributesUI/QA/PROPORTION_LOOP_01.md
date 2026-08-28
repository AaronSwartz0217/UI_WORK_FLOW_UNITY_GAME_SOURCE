# Proportion Loop 01

## Wireframe

- Canvas: `815x1110`
- Measured panel bounds: approximately `97,57,639,924`
- Measured panel ratio: `0.691558`

## Review candidates

| Candidate | Canvas | Measured panel | Ratio | Deviation | Result |
|---|---:|---:|---:|---:|---|
| Review01 | 1024x1536 | 906x1420 | 0.638028 | about 7.74% | Rejected: too narrow/tall |
| Review02 | 1024x1536 | 964x1366 | 0.705710 | about 2.05% | Selected and split |
| Review03 | 1044x1507 | 930x1398 | 0.665236 | about 3.81% | Rejected: wrong canvas and worse ratio |

## Review02 visual checks

- Two top-left tabs retained: PASS
- Functional close `X` retained: PASS
- Two distinct progress tracks retained: PASS
- Short left and long right attribute columns retained: PASS
- Ordinary text and dynamic numbers removed: PASS
- Cook primary style: PASS
- Non-uniform scaling: NO

Conclusion: `PASS_FOR_COMPONENT_SPLIT`.
