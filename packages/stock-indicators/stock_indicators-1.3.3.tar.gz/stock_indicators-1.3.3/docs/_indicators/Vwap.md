---
title: Volume Weighted Average Price (VWAP)
permalink: /indicators/Vwap/
type: moving-average
layout: indicator
---

# {{ page.title }}

><span class="indicator-syntax">**get_vwap**(*quotes, start=None*)</span>

><span class="indicator-syntax">**get_vwap**(*quotes, year, month=1, day=1, hour=0, minute=0*)</span>

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes). <br><span class='qna-dataframe'> • [See here]({{site.baseurl}}/guide/#using-pandasdataframe) for usage with pandas.DataFrame</span>
| `start` | datetime, Optional | The anchor date used to start the VWAP accumulation.  The earliest date in `quotes` is used when not provided.
| `year`, `month`, `day`, `hour`, `minute`| int, Optional | The anchor date used to start the VWAP accumulation.  The earliest date in `quotes` is used when not provided.

### Historical quotes requirements

You must have at least one historical quote to calculate; however, more is often needed to be useful.  Historical quotes are typically provided for a single day using minute-based intraday periods.  Since this is an accumulated weighted average price, different start dates will produce different results.  The accumulation starts at the first period in the provided `quotes`, unless it is specified in the optional `start` parameter.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Return

```python
VWAPResults[VWAPResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `VWAPResults` is just a list of `VWAPResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The first period or the `start` will have a `vwap = close` value since it is the initial starting point.
- `vwap` values before `start`, if specified, will be `None`.

### VWAPResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `vwap` | float, Optional | Volume Weighted Average Price

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

# Calculate
results = indicators.get_vwap(quotes);
```

## About {{ page.title }}

The [Volume Weighted Average Price](https://en.wikipedia.org/wiki/Volume-weighted_average_price) is a Volume weighted average of Close price, typically used on intraday data.
[[Discuss] &#128172;]({{site.dotnet.repo}}/discussions/310 "Community discussion about this indicator")

![image]({{site.dotnet.charts}}/Vwap.png)

### Sources

- [C# core]({{site.dotnet.src}}/s-z/Vwap/Vwap.Series.cs)
- [Python wrapper]({{site.python.src}}/vwap.py)
