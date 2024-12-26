# stock-price-patterns
Stock Price Pattern Modeling(Detection)

## Available patterns
* Inverted Hammer
* Hammer
* Hanging man
* Bearish/Bullish Harami
* Dark cloud cover
* Doji
* Doji Star
* Bearish engulfing
* Bullish engulfing
* Morning star
* Morning star doji
* Piercing pattern
* Star
* Shooting star
*  ...


## How to use
### Dataframe requirements

- Dataframe must contain Open, High, Low and Close prices
- Open, High, Low and Close prices must be in numeric type.

#### Dataframe Example: 

|                Date |    Open |    High |     Low |   Close |
|--------------------:|--------:|--------:|--------:|--------:|
| 2019-12-24 00:00:00 |  7317.3 | 7436.68 | 7157.04 | 7255.77 |
| 2019-12-25 00:00:00 | 7255.77 | 7271.77 | 7128.86 | 7204.63 |
| 2019-12-26 00:00:00 | 7205.01 |    7435 | 7157.12 |    7202 |
| 2019-12-27 00:00:00 |    7202 | 7275.86 | 7076.42 | 7254.74 |
| 2019-12-28 00:00:00 | 7254.77 | 7365.01 | 7238.67 | 7316.14 |
| 2019-12-29 00:00:00 | 7315.36 | 7528.45 |    7288 | 7388.24 |

### Code
```python
import pandas as pd
import os
from pathlib import Path
from candlestick import CandlestickPatterns
notebook_path = os.getcwd()
current_dir = Path(notebook_path)
csv_file = str(current_dir) + '/VN30F1M_5minutes.csv'
is_file = os.path.isfile(csv_file)
if is_file:
    dataset = pd.read_csv(csv_file, index_col='Date', parse_dates=True)
else:
    print(csv_file)
    print("File not found")
    exit()
csp = CandlestickPatterns(dataset)
modeling_data = csp.pattern_modeling()
print(modeling_data[modeling_data.model != ''])
```
### Result

| Date                | model  |    Open |    High |     Low |   Close |
|:--------------------|:-------|--------:|--------:|--------:|--------:|
| 2019-12-24 00:00:00 |        |  7317.3 | 7436.68 | 7157.04 | 7255.77 |
| 2019-12-25 00:00:00 |        | 7255.77 | 7271.77 | 7128.86 | 7204.63 |
| 2019-12-26 00:00:00 |        | 7205.01 |    7435 | 7157.12 |    7202 |
| 2019-12-27 00:00:00 | fair.. |    7202 | 7275.86 | 7076.42 | 7254.74 |
| 2019-12-28 00:00:00 | bull.. | 7254.77 | 7365.01 | 7238.67 | 7316.14 |
| 2019-12-29 00:00:00 | bear.. | 7315.36 | 7528.45 |    7288 | 7388.24 |


## More details
check [Examples](/candlestick-examples.ipynb).
