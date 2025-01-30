---
title: Ulcer Index (UI)
permalink: /indicators/UlcerIndex/
type: price-characteristic
layout: indicator
---

# {{ page.title }}

><span class="indicator-syntax">**get_ulcer_index**(*quotes, lookback_periods=14*)</span>

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes). <br><span class='qna-dataframe'> • [See here]({{site.baseurl}}/guide/#using-pandasdataframe) for usage with pandas.DataFrame</span>
| `lookback_periods` | int, *default 14* | Number of periods (`N`) for review.  Must be greater than 0.

### Historical quotes requirements

You must have at least `N` periods of `quotes` to cover the warmup periods.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Return

```python
UlcerIndexResults[UlcerIndexResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `UlcerIndexResults` is just a list of `UlcerIndexResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The first `N-1` periods will have `None` values since there's not enough data to calculate.

### UlcerIndexResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `ui` | float, Optional | Ulcer Index

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

# Calculate UI(14)
results = indicators.get_ulcer_index(quotes, 14)
```

## About {{ page.title }}

Created by Peter Martin, the [Ulcer Index](https://en.wikipedia.org/wiki/Ulcer_index) is a measure of downside Close price volatility over a lookback window.
[[Discuss] &#128172;]({{site.dotnet.repo}}/discussions/232 "Community discussion about this indicator")

![image]({{site.dotnet.charts}}/UlcerIndex.png)

### Sources

- [C# core]({{site.dotnet.src}}/s-z/UlcerIndex/UlcerIndex.Series.cs)
- [Python wrapper]({{site.python.src}}/ulcer_index.py)
