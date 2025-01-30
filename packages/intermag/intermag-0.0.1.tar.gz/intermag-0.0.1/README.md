# intermag

Python library to auto-download, manipulate, and process magnetic data from INTERMAGNET sites

## Example Python Script

``` python
import datetime as dt
import intermag as im


ds = im.IM_Dataset()
ds.download_dataset(iaga_code    = 'BOU',
                    start_date   = dt.datetime(2025, 1, 1),
                    load_dataset = True,
                    num_days     = 2,
                    save_dir     = os.path.dirname(__file__))

print(ds.attrs())
print(ds.data())

ds.plot_data()
```

## Command Line Usage

``` cmd
options:
  -h, --help    show this help message and exit
  -l, --loc     IAGA location code (3-letter)
  -y, --year    Start year of dataset
  -m, --month   Start month of dataset
  -d, --day DAY Start day of dataset
  -u, --dur DUR Duration of dataset in whole number of days
  -p, --plot    Bool of whether or not to plot the dataset
  -s, --savedir Directory to save the dataset to
```

``` cmd
python intermagnet -l BOU -y 2025 -m 1 -d 1 -u 1 -p True -s <dataset file path>
```
