---
title: Triple EMA Oscillator (TRIX)
permalink: /indicators/Trix/
type: oscillator
layout: indicator
---

# {{ page.title }}

><span class="indicator-syntax">**get_trix**(*quotes, lookback_periods, signal_periods=None*)</span>

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes). <br><span class='qna-dataframe'> • [See here]({{site.baseurl}}/guide/#using-pandasdataframe) for usage with pandas.DataFrame</span>
| `lookback_periods` | int | Number of periods (`N`) in each of the the exponential moving averages.  Must be greater than 0.
| `signal_periods` | int, Optional | Number of periods in the moving average of TRIX.  Must be greater than 0, if specified.

### Historical quotes requirements

You must have at least `4×N` or `3×N+100` periods of `quotes`, whichever is more, to cover the warmup periods.  Since this uses a smoothing technique, we recommend you use at least `3×N+250` data points prior to the intended usage date for better precision.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Return

```python
TRIXResults[TRIXResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `TRIXResults` is just a list of `TRIXResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The first `3×N-3` periods will have `None` values since there's not enough data to calculate.

>&#9886; **Convergence warning**: The first `3×N+250` periods will have decreasing magnitude, convergence-related precision errors that can be as high as ~5% deviation in indicator values for earlier periods.

### TRIXResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `ema3` | float, Optional | 3 EMAs of the Close price
| `trix` | float, Optional | Rate of Change of 3 EMAs
| `signal` | float, Optional | SMA of `trix` based on `signal_periods` periods, if specified

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

# calculate 20-period Trix
results = indicators.get_trix(quotes, 14)
```

## About {{ page.title }}

Created by Jack Hutson, [TRIX](https://en.wikipedia.org/wiki/Trix_(technical_analysis)) is the rate of change for a 3 EMA smoothing of the Close price over a lookback window.  TRIX is often confused with [TEMA](../Tema#content).
[[Discuss] &#128172;]({{site.dotnet.repo}}/discussions/234 "Community discussion about this indicator")

![image]({{site.dotnet.charts}}/Trix.png)

### Sources

- [C# core]({{site.dotnet.src}}/s-z/Trix/Trix.Series.cs)
- [Python wrapper]({{site.python.src}}/trix.py)
