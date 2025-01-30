---
title: Hilbert Transform Instantaneous Trendline
permalink: /indicators/HtTrendline/
type: moving-average
layout: indicator
---

# {{ page.title }}

><span class="indicator-syntax">**get_ht_trendline**(*quotes*)</span>

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes). <br><span class='qna-dataframe'> • [See here]({{site.baseurl}}/guide/#using-pandasdataframe) for usage with pandas.DataFrame</span>

## Historical quotes requirements

You must have at least `100` periods of `quotes` to cover the warmup periods.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Return

```python
HTTrendlineResults[HTTrendlineResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `HTTrendlineResults` is just a list of `HTTrendlineResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The first `6` periods will have `None` values for `smooth_price` since there's not enough data to calculate.
- The first `7` periods will have `None` values for `dc_periods` since there is not enough data to calculate; and are generally unreliable for the first ~25 periods.

>&#9886; **Convergence warning**: The first `100` periods will have decreasing magnitude, convergence-related precision errors that can be as high as ~5% deviation in indicator values for earlier periods.

### HTTrendlineResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `trendline` | float, Optional | HT Trendline
| `dc_periods` | int, Optional | Dominant cycle periods (smoothed)
| `smooth_price` | float, Optional | Weighted moving average of `(H+L)/2` price

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

# Calculate HT Trendline
results = indicators.get_ht_trendline(quotes)
```

## About {{ page.title }}

Created by John Ehlers, the Hilbert Transform Instantaneous Trendline is a 5-period trendline of high/low price that uses signal processing to reduce noise.
[[Discuss] &#128172;]({{site.dotnet.repo}}/discussions/363 "Community discussion about this indicator")

![image]({{site.dotnet.charts}}/HtTrendline.png)

### Sources

- [C# core]({{site.dotnet.src}}/e-k/HtTrendline/HtTrendline.Series.cs)
- [Python wrapper]({{site.python.src}}/ht_trendline.py)
