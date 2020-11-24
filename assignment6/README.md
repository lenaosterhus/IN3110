# Assignment 6

This assignment was solved using macOS.

All functions with names starting with an underscore are considered private.

## Dependencies
All packages can be installed using `pip`.
```bash
pip install <package>
```

`Pandas (1.0.5)` is used to analyze data.

`Altair (4.1.0)` is used to plot graphs.

`Flask (1.1.2)` is used to build a web application.

The built-in python packages `re`, `os`, `json` are also used.

## Run script
To build a web app with plots visualizing the corona dataset made publicly available by FHI, run the `web_visualization` script.

```bash
python3 web_visualization.py
```

The web app should now be running on http://127.0.0.1:5000/.

## Plotting methods
All date arguments (start/end) must be formatted YYYY-MM-DD. E.g. "2020-02-21".
- `plot_reported_cases(data, county, start, end)`

- `plot_cumulative_cases(data, county, start, end)`

- `plot_both(data, county, start, end)`

- `plot_norway()`

