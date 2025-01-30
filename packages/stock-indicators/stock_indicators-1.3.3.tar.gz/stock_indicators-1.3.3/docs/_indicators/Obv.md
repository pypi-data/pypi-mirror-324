---
title: On-Balance Volume (OBV)
permalink: /indicators/Obv/
type: volume-based
layout: indicator
---

# {{ page.title }}

><span class="indicator-syntax">**get_obv**(*quotes, sma_periods=None*)</span>

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes). <br><span class='qna-dataframe'> • [See here]({{site.baseurl}}/guide/#using-pandasdataframe) for usage with pandas.DataFrame</span>
| `sma_periods` | int, Optional | Number of periods (`N`) in the moving average of OBV.  Must be greater than 0, if specified.

### Historical quotes requirements

You must have at least two historical quotes to cover the warmup periods; however, since this is a trendline, more is recommended.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Return

```python
OBVResults[OBVResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `OBVResults` is just a list of `OBVResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The first period OBV will have `0` value since there's not enough data to calculate.

### ObvResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `obv` | float | On-balance Volume
| `obv_sma` | float, Optional | Moving average (SMA) of OBV based on `sma_periods` periods, if specified

>&#128681; **Warning**: absolute values in OBV are somewhat meaningless. Use with caution.

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

# Calculate
results = indicators.get_obv(quotes)
```

## About {{ page.title }}

Popularized by Joseph Granville, [On-balance Volume](https://en.wikipedia.org/wiki/On-balance_volume) is a rolling accumulation of volume based on Close price direction.
[[Discuss] &#128172;]({{site.dotnet.repo}}/discussions/246 "Community discussion about this indicator")

![image]({{site.dotnet.charts}}/Obv.png)

### Sources

- [C# core]({{site.dotnet.src}}/m-r/Obv/Obv.Series.cs)
- [Python wrapper]({{site.python.src}}/obv.py)
