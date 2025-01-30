---
title: Gator Oscillator
permalink: /indicators/Gator/
type: price-trend
layout: indicator
---

# {{ page.title }}

><span class="indicator-syntax">**get_gator**(*quotes: Iterable[Quote]*)</span>

><span class="indicator-syntax">**get_gator**(*quotes: Iterable[AlligatorResult]*)</span>

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] or Iterable[AlligatorResult] | Iterable of the [Quote]({{site.baseurl}}/guide/#historical-quotes) or [Alligator Result](../Alligator#content). <br><span class='qna-dataframe'> • [See here]({{site.baseurl}}/guide/#using-pandasdataframe) for usage with pandas.DataFrame</span>

## Historical quotes requirements

If using default settings, you must have at least 121 periods of `quotes`. Since this uses a smoothing technique, we recommend you use at least 271 data points prior to the intended usage date for better precision.  If using a custom Alligator configuration, see [Alligator documentation](../Alligator#historical-quotes-requirements) for historical quotes requirements.

`quotes` is an `Iterable[Quote]` or `Iterable[AlligatorResult]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Return

```python
GatorResults[GatorResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `GatorResults` is just a list of `GatorResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The first 10-20 periods will have `None` values since there's not enough data to calculate.

>&#9886; **Convergence warning**: The first 150 periods will have decreasing magnitude, convergence-related precision errors that can be as high as ~5% deviation in indicator values for earlier periods.

### GatorResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `upper` | float, Optional | Absolute value of Alligator `Jaw-Teeth`
| `lower` | float, Optional | Absolute value of Alligator `Lips-Teeth`
| `is_upper_expanding` | bool, Optional | Upper value is growing
| `is_lower_expanding` | bool, Optional | Lower value is growing

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

# Calculate the Gator Oscillator
results = indicators.get_gator(quotes)
```

## About {{ page.title }}

Created by Bill Williams, the Gator Oscillator is an expanded view of [Williams Alligator](../Alligator#content).
[[Discuss] &#128172;]({{site.dotnet.repo}}/discussions/385 "Community discussion about this indicator")

![image]({{site.dotnet.charts}}/Gator.png)

### Sources

- [C# core]({{site.dotnet.src}}/e-k/Gator/Gator.Series.cs)
- [Python wrapper]({{site.python.src}}/gator.py)
