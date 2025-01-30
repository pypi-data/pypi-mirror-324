---
title: Ichimoku Cloud
description: Ichimoku Cloud (Ichimoku Kinkō Hyō)
permalink: /indicators/Ichimoku/
type: price-trend
layout: indicator
---

# {{ page.title }}

><span class="indicator-syntax">**get_ichimoku**(*quotes, tenkan_periods=9, kijun_periods=26, senkou_b_periods=52*)</span>

### More overloaded interfaces

**get_ichimoku**(quotes, tenkan_periods, kijun_periods, senkou_b_periods,
                 offset_periods)
**get_ichimoku**(quotes, tenkan_periods, kijun_periods, senkou_b_periods,
                 senkou_offset, chikou_offset)

## Parameters

| name | type | notes
| -- |-- |--
| `quotes` | Iterable[Quote] | Iterable of the [Quote class]({{site.baseurl}}/guide/#historical-quotes) or [its sub-class]({{site.baseurl}}/guide/#using-custom-quote-classes). <br><span class='qna-dataframe'> • [See here]({{site.baseurl}}/guide/#using-pandasdataframe) for usage with pandas.DataFrame</span>
| `tenkan_periods` | int, *default 9* | Number of periods (`T`) in the Tenkan-sen midpoint evaluation.  Must be greater than 0.
| `kijun_periods` | int, *default 26* | Number of periods (`K`) in the shorter Kijun-sen midpoint evaluation.  Must be greater than 0.
| `senkou_b_periods` | int, *default 52* | Number of periods (`S`) in the longer Senkou leading span B midpoint evaluation.  Must be greater than `K`.
| `offset_periods` | int | Number of periods to offset both `Senkou` and `Chikou` spans.  Must be non-negative.  Default is `kijun_periods`.
| `senkou_offset` | int | Number of periods to offset the `Senkou` span.  Must be non-negative.  Default is `kijun_periods`.
| `chikou_offset` | int | Number of periods to offset the `Chikou` span.  Must be non-negative.  Default is `kijun_periods`.

See overloads usage above to determine which parameters are relevant for each.  If you are customizing offsets, all parameter arguments must be specified.

### Historical quotes requirements

You must have at least the greater of `T`,`K`, `S`, and offset periods for `quotes` to cover the warmup periods; though, given the leading and lagging nature, we recommend notably more.

`quotes` is an `Iterable[Quote]` collection of historical price quotes.  It should have a consistent frequency (day, hour, minute, etc).  See [the Guide]({{site.baseurl}}/guide/#historical-quotes) for more information.

## Return

```python
IchimokuResults[IchimokuResult]
```

- This method returns a time series of all available indicator values for the `quotes` provided.
- `IchimokuResults` is just a list of `IchimokuResult`.
- It always returns the same number of elements as there are in the historical quotes.
- It does not return a single incremental indicator value.
- The first `T-1`, `K-1`, and `S-1` periods will have various `None` values since there's not enough data to calculate.  Custom offset periods may also increase `None` results for warmup periods.

### IchimokuResult

| name | type | notes
| -- |-- |--
| `date` | datetime | Date
| `tenkan_sen` | Decimal, Optional | Conversion / signal line
| `kijun_sen` | Decimal, Optional | Base line
| `senkou_span_a` | Decimal, Optional | Leading span A
| `senkou_span_b` | Decimal, Optional | Leading span B
| `chikou_span` | Decimal, Optional | Lagging span

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

# calculate ICHIMOKU(9,26,52)
results = indicators.get_ichimoku(quotes, 9, 26, 52)
```

## About {{ page.title }}

Created by Goichi Hosoda (細田悟一, Hosoda Goichi), [Ichimoku Cloud](https://en.wikipedia.org/wiki/Ichimoku_Kink%C5%8D_Hy%C5%8D), also known as Ichimoku Kinkō Hyō, is a collection of indicators that depict support and resistance, momentum, and trend direction.
[[Discuss] &#128172;]({{site.dotnet.repo}}/discussions/251 "Community discussion about this indicator")

![image]({{site.dotnet.charts}}/Ichimoku.png)

### Sources

- [C# core]({{site.dotnet.src}}/e-k/Ichimoku/Ichimoku.Series.cs)
- [Python wrapper]({{site.python.src}}/ichimoku.py)
