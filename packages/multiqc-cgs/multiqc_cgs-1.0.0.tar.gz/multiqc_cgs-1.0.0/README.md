# MultiQC plugin: customize general statistics

```
# install module in same environment as multiqc
git push origin master
```

## Example

```
# Add the following entry to your multiqc config
# This example add picard hsmetrics ZERO_CVG_TARGETS_PCT
# all fields used by multiqc, for example title, can be set
multiqc_cgs:
  "Picard: HsMetrics":
    ZERO_CVG_TARGETS_PCT:
      title: "Target bases with zero coverage [%]"
      description: "Target bases with zero coverage [%] from Picard"
      min: 0
      max: 100
      scale: "RdYlGn-rev"
      format: "{:.2%}"

```

## Compatibility
For multiqc_cgs v1.0.0 and later, [MultiQC](https://seqera.io/multiqc/) >v1.21 is needed.
