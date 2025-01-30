---
title: Commodity Channel Index (CCI)
permalink: /indicators/Cci/
type: oscillator
layout: indicator
---

# {{ page.title }}

><span class="indicator-syntax">**get_cci**(*quotes, lookback_periods=20*)</span>

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes). <br><span class='qna-dataframe'> • [See here]({{site.baseurl}}/guide/#using-pandasdataframe) for usage with pandas.DataFrame</span>
| `lookback_periods` | int, *default 20* | Number of periods (`N`) in the moving average.  Must be greater than 0.

### Historical quotes requirements

You must have at least `N+1` periods of `quotes` to cover the warmup periods.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Return

```python
CCIResults[CCIResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `CCIResults` is just a list of `CCIResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The first `N-1` periods will have `None` values since there's not enough data to calculate.

### CciResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `cci` | float, Optional | Commodity Channel Index

### Utilities

- [.condense()]({{site.baseurl}}/utilities#condense)
- [.find(lookup_date)]({{site.baseurl}}/utilities#find-indicator-result-by-date)
- [.remove_warmup_periods()]({{site.baseurl}}/utilities#remove-warmup-periods)
- [.remove_warmup_periods(qty)]({{site.baseurl}}/utilities#remove-warmup-periods)

See [Utilities and Helpers]({{site.baseurl}}/utilities#utilities-for-indicator-results) for more information.

## Example

```python
from stock_indicators import indicators

# This method is NOT a part of the library.
quotes = get_historical_quotes("SPY")

# Calculate 20-period CCI
results = indicators.get_cci(quotes, 20)
```

## About {{ page.title }}

Created by Donald Lambert, the [Commodity Channel Index](https://en.wikipedia.org/wiki/Commodity_channel_index) is an oscillator depicting deviation from typical price range, often used to identify cyclical trends.
[[Discuss] &#128172;]({{site.dotnet.repo}}/discussions/265 "Community discussion about this indicator")

![image]({{site.dotnet.charts}}/Cci.png)

### Sources

- [C# core]({{site.dotnet.src}}/a-d/Cci/Cci.Series.cs)
- [Python wrapper]({{site.python.src}}/cci.py)
