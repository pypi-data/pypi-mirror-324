---
title: Exponential Moving Average (EMA)
permalink: /indicators/Ema/
type: moving-average
layout: indicator
---

# {{ page.title }}

><span class="indicator-syntax">**get_ema**(*quotes, lookback_periods, candle_part=CandlePart.CLOSE*)</span>

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes). <br><span class='qna-dataframe'> • [See here]({{site.baseurl}}/guide/#using-pandasdataframe) for usage with pandas.DataFrame</span>
| `lookback_periods` | int | Number of periods (`N`) in the moving average.  Must be greater than 0.
| `candle_part` | CandlePart, *default CandlePart.CLOSE* | Specify candle part to evaluate.  See [CandlePart options](#candlepart-options) below.

### Historical quotes requirements

You must have at least `2×N` or `N+100` periods of `quotes`, whichever is more, to cover the convergence periods.  Since this uses a smoothing technique, we recommend you use at least `N+250` data points prior to the intended usage date for better precision.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

{% include candlepart-options.md %}

## Returns

```python
EMAResults[EMAResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `EMAResults` is just a list of `EMAResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The first `N-1` periods will have `None` values since there's not enough data to calculate.

>&#9886; **Convergence warning**: The first `N+100` periods will have decreasing magnitude, convergence-related precision errors that can be as high as ~5% deviation in indicator values for earlier periods.

### EMAResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `ema` | float, Optional | Exponential moving average

### Utilities

- [.condense()]({{site.baseurl}}/utilities#condense)
- [.find(lookup_date)]({{site.baseurl}}/utilities#find-indicator-result-by-date)
- [.remove_warmup_periods()]({{site.baseurl}}/utilities#remove-warmup-periods)
- [.remove_warmup_periods(qty)]({{site.baseurl}}/utilities#remove-warmup-periods)

See [Utilities and Helpers]({{site.baseurl}}/utilities#utilities-for-indicator-results) for more information.

## Example

```python
from stock_indicators import indicators
from stock_indicators import CandlePart     # Short path, version >= 0.8.1

# This method is NOT a part of the library.
quotes = get_historical_quotes("SPY")

# calculate 20-period EMA
results = indicators.get_ema(quotes, 20, CandlePart.CLOSE)
```

### About {{ page.title }}

[Exponentially weighted moving average](https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average) price over a lookback window.
[[Discuss] &#128172;]({{site.dotnet.repo}}/discussions/256 "Community discussion about this indicator")

![image]({{site.dotnet.charts}}/Ema.png)

See also related [Double EMA](../Dema#content) and [Triple EMA](../Tema#content).

#### Sources

- [C# core]({{site.dotnet.src}}/e-k/Ema/Ema.Series.cs)
- [Python wrapper]({{site.python.src}}/ema.py)
