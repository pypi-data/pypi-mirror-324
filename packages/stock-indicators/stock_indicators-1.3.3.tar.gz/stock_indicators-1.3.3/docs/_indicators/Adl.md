---
title: Accumulation / Distribution Line (ADL)
permalink: /indicators/Adl/
type: volume-based
layout: indicator
---

# {{ page.title }}

><span class="indicator-syntax">**get_adl**(*quotes, sma_periods=None*)</span>

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes). <br><span class='qna-dataframe'> • [See here]({{site.baseurl}}/guide/#using-pandasdataframe) for usage with pandas.DataFrame</span>
| `sma_periods` | int, Optional | Number of periods (`N`) in the moving average of ADL.  Must be greater than 0, if specified.

### Historical quotes requirements

You must have at least two historical quotes to cover the warmup periods; however, since this is a trendline, more is recommended.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Returns

```python
ADLResults[ADLResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `ADLResults` is just a list of `ADLResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.

### ADLResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `money_flow_multiplier` | float, Optional | Money Flow Multiplier
| `money_flow_volume` | float, Optional | Money Flow Volume
| `adl` | float | Accumulation Distribution Line (ADL)
| `adl_sma` | float, Optional | Moving average (SMA) of ADL based on `sma_periods` periods, if specified

>&#128681; **Warning**: absolute values in ADL and MFV are somewhat meaningless.  Use with caution.

### Utilities

- [.condense()]({{site.baseurl}}/utilities#condense)
- [.find(lookup_date)]({{site.baseurl}}/utilities#find-indicator-result-by-date)
- [.remove_warmup_periods(qty)]({{site.baseurl}}/utilities#remove-warmup-periods)

See [Utilities and Helpers]({{site.baseurl}}/utilities#utilities-for-indicator-results) for more information.

## Example

```python
from stock_indicators import indicators

# This method is NOT a part of the library.
quotes = get_historical_quotes("SPY")

# calculate
results = indicators.get_adl(quotes)
```

## About {{ page.title }}

Created by Marc Chaikin, the [Accumulation/Distribution Line/Index](https://en.wikipedia.org/wiki/Accumulation/distribution_index) is a rolling accumulation of Chaikin Money Flow Volume.
[[Discuss] &#128172;]({{site.dotnet.repo}}/discussions/271 "Community discussion about this indicator")

![image]({{site.dotnet.charts}}/Adl.png)

### Sources

- [C# core]({{site.dotnet.src}}/a-d/Adl/Adl.Series.cs)
- [Python wrapper]({{site.python.src}}/adl.py)
