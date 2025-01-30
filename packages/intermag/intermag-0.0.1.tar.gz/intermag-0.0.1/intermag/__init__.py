import datetime as dt
import os
import shutil
from os.path import join
from urllib import request
from urllib.error import URLError

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.linalg as la
from ppigrf import igrf




DATA_FORMATS = ['IAGA2002',
                'ImagCDF',
                'IMFV122',
                'WDC']
IAGA_CODES = ['AAE',
              'ABG',
              'ABK',
              'AIA',
              'ALE',
              'AMS',
              'API',
              'AQU',
              'ARS',
              'ASC',
              'ASP',
              'BDV',
              'BEL',
              'BFE',
              'BFO',
              'BLC',
              'BMT',
              'BNG',
              'BOU',
              'BOX',
              'BRD',
              'BRW',
              'BSL',
              'CBB',
              'CKI',
              'CLF',
              'CMO',
              'CNB',
              'CNH',
              'CPL',
              'CSY',
              'CTA',
              'CYG',
              'CZT',
              'DED',
              'DLR',
              'DLT',
              'DMC',
              'DOU',
              'DRV',
              'DUR',
              'EBR',
              'ESK',
              'EYR',
              'FCC',
              'FRD',
              'FRN',
              'FUR',
              'GAN',
              'GCK',
              'GDH',
              'GLN',
              'GNA',
              'GNG',
              'GUA',
              'GUI',
              'GZH',
              'HAD',
              'HBK',
              'HER',
              'HLP',
              'HON',
              'HRB',
              'HRN',
              'HUA',
              'HYB',
              'IPM',
              'IQA',
              'IRT',
              'ISK',
              'IZN',
              'JAI',
              'JCO',
              'KAK',
              'KDU',
              'KEP',
              'KHB',
              'KIV',
              'KMH',
              'KNY',
              'KOU',
              'LER',
              'LNP',
              'LON',
              'LOV',
              'LRM',
              'LVV',
              'LYC',
              'LZH',
              'MAB',
              'MAW',
              'MBC',
              'MBO',
              'MCQ',
              'MEA',
              'MGD',
              'MID',
              'MLT',
              'MMB',
              'MZL',
              'NAQ',
              'NCK',
              'NEW',
              'NGK',
              'NUR',
              'NVS',
              'ORC',
              'OTT',
              'PAF',
              'PAG',
              'PBQ',
              'PEG',
              'PET',
              'PHU',
              'PIL',
              'PPT',
              'PST',
              'QSB',
              'RES',
              'SBA',
              'SBL',
              'SFS',
              'SHE',
              'SHU',
              'SIT',
              'SJG',
              'SOD',
              'SPG',
              'SPT',
              'STJ',
              'STT',
              'SUA',
              'TAM',
              'TAN',
              'TDC',
              'THL',
              'THY',
              'TIK',
              'TSU',
              'TTB',
              'TUC',
              'UPS',
              'VAL',
              'VIC',
              'VNA',
              'VOS',
              'VSS',
              'WIC',
              'WMQ',
              'WNG',
              'YAK',
              'YKC']
RESOLUTIONS = ['sec',
               'min']
SAMPLING_OPTIONS = ['86400',
                    '1440']
ORIENTATIONS = ['Native',
                'XYZF',
                'HDZF',
                'DIFF',
                'XYZS',
                'HDZS',
                'DIFS']
# Start date in form: 2025-01-01



# Can only request data one day at a time and thus one file per day
BASE_IM_DATA_RE_URL = r'https://imag-data.bgs.ac.uk/GIN_V1/GINServices?Request=GetData&format={DATA_FORMAT}&testObsys=0&observatoryIagaCode={IAGA_CODE}&samplesPerDay={SAMPLING_OPTION}&orientation={ORIENTATION}&publicationState=adj-or-rep&recordTermination=UNIX&dataStartDate={START_DATE}&dataDuration=1'




class IM_Dataset(object):
    def __init__(self) -> None:
        self.__data      = pd.DataFrame()
        self.__IAGA_code = None
    
    def data(self):
        return self.__data
    
    def attrs(self):
        return self.__data.attrs
    
    def IAGA_code(self):
        return self.__data.attrs['IAGA Code']
    
    def plot_data(self,
                  block_plot: bool = True):
        fig, axs = plt.subplots(4)
        fig.suptitle(self.__data.attrs['IAGA Code'])
        
        axs[0].plot(self.__data.datetime, self.__data.F)
        axs[0].set_title('F')
        axs[0].grid()
        axs[1].plot(self.__data.datetime, self.__data.X)
        axs[1].set_title('X')
        axs[1].grid()
        axs[2].plot(self.__data.datetime, self.__data.Y)
        axs[2].set_title('Y')
        axs[2].grid()
        axs[3].plot(self.__data.datetime, self.__data.Z)
        axs[3].set_title('Z')
        axs[3].grid()
        
        plt.show(block=block_plot)
    
    def download_dataset(self,
                         iaga_code:     str         = 'BOU',
                         resolution:    str         = 'sec',
                         start_date:    dt.datetime = dt.datetime.now(),
                         num_days:      int         = 1,
                         save_dir:      str         = '',
                         orientation:   str         = 'XYZF',
                         data_format:   str         = 'IAGA2002',
                         n_retries:     int         = 4,
                         gin_username:  str         = '',
                         gin_password:  str         = '',
                         proxy_address: str         = '',
                         load_dataset:  bool        = False,
                         append:        bool        = False,
                         fast_mode:     bool        = True,
                         chunk:         int         = 1000) -> None:
        '''
        
        '''
        
        if (iaga_code.upper() not in IAGA_CODES):
            print('ERROR: IAGA Code incorrect, got {}'.format(iaga_code))
            return
        if (resolution.lower() not in RESOLUTIONS):
            print('ERROR: Resolution incorrect, got {}'.format(resolution))
            return
        if (orientation not in ORIENTATIONS):
            print('ERROR: Orientation incorrect, got {}'.format(orientation))
            return
        if (data_format not in DATA_FORMATS):
            print('ERROR: Data format incorrect, got {}'.format(data_format))
            return
        
        if resolution.lower() == 'sec':
            res = '86400'
        elif resolution.lower() == 'min':
            res = '1440'
        else:
            resolution = 'min'
            res        = '1440'
        
        for i in range(num_days):
            date = str(start_date + dt.timedelta(days=i))[:10]
            
            local_file = join(save_dir, iaga_code.lower() + date.replace('-', '') + resolution.lower() + '.' + resolution.lower())
            
            if not os.path.exists(local_file):
                re_url = BASE_IM_DATA_RE_URL.format(DATA_FORMAT     = data_format,
                                                    IAGA_CODE       = iaga_code.lower(),
                                                    SAMPLING_OPTION = res.lower(),
                                                    ORIENTATION     = orientation,
                                                    START_DATE      = date)
                getfile(re_url,
                        local_file,  
                        n_retries,
                        gin_username,
                        gin_password,
                        proxy_address)
                
            if load_dataset:
                if i == 0:
                    self.load_dataset(local_file,
                                      data_format,
                                      append,
                                      fast_mode,
                                      chunk)
                else:
                    self.load_dataset(local_file,
                                      data_format,
                                      True,
                                      fast_mode,
                                      chunk)
    
    def load_dataset(self,
                     fname:       str,
                     data_format: str  = 'IAGA2002',
                     append:      bool = False,
                     fast_mode:   bool = True,
                     chunk:       int  = 1000) -> None:
        '''
        
        '''
        
        if not append:
            self.__data = pd.DataFrame()
        
        if data_format == 'IAGA2002':
            df = parse_IAGA_2002(fname, fast_mode, chunk)
            self.__data = pd.concat([self.__data, df], ignore_index=True)
            
            if not self.__data.attrs:
                self.__data.attrs = df.attrs




def getfile(url:           str,
            local_file:    str,
            n_retries:     int = 4,
            gin_username:  str = '',
            gin_password:  str = '',
            proxy_address: str = '') -> None:
    '''
    Slightly edited version of function included in INTERMAGNET-provided download scripts
    '''
    
    # remove any existing file
    try:
        os.remove(local_file)
    except FileNotFoundError:
        pass
    except OSError:
        print('Error: unable to remove file: ' + str(local_file))
        return
    
    # handle authentication and proxy server
    proxy = auth = None
    
    if len(proxy_address) > 0:
        proxy = request.ProxyHandler({'http': proxy_address, 'https': proxy_address})
        
    if len(gin_username) > 0:
        pwd_mgr = request.HTTPPasswordMgrWithPriorAuth()
        pwd_mgr.add_password(None,
                             'https://imag-data.bgs.ac.uk/GIN_V1',
                             gin_username,
                             gin_password,
                             is_authenticated=True)
        auth = request.HTTPBasicAuthHandler(pwd_mgr)
        
    if url.startswith ('https'):
        default_handler = request.HTTPSHandler
    else:
        default_handler = request.HTTPHandler
    
    if auth and proxy:
        opener = request.build_opener(proxy, auth, default_handler)
    elif auth:
        opener = request.build_opener(auth, default_handler)
    elif proxy:
        opener = request.build_opener(proxy, default_handler)
    else:
        opener = request.build_opener(default_handler)
    
    # download the file
    success = False
    
    while (not success) and (n_retries > 0):
        try:
            with opener.open(url) as f_in:
                with open(local_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out, 4096)
                
            success = True
            
        except (URLError, IOError, OSError):
            n_retries -= 1
        
    if not success:
        print('Error: cannot download ' + local_file)
        return
        
    else:
        print('Warning: unable to determine data type for renaming of ' + local_file)




def add_igrf_cols(df:        pd.DataFrame,
                  fast_mode: bool=True,
                  chunk:     int=1000) -> pd.DataFrame:
    '''
    Add IGRF vector and magnitude columns for all samples
    in the dataframe
    
    **NOTE**: This assumes 'LONG', 'LAT', 'ALT', and
    'datetime' columns are already included in the
    dataframe
    
    Parameters
    ----------
    df
        Dataframe of INTERMAGNET data
    fast_mode
        Calculate IGRF values based only on the first corrdinate
        in the .sec file (speeds up parsing considerably)
    chunk
        If not parsing in `fast_mode`, set the number of samples
        to simultaneously calculate IGRF values for
    
    Returns
    -------
    pd.DataFrame
        Dataframe of INTERMAGNET data with new IGRF columns
    '''
    
    if not df.empty:
        if fast_mode:
            Be, Bn, Bu = igrf(df.LONG[~np.isnan(df.LONG)].mean(),
                              df.LAT[~np.isnan(df.LAT)].mean(),
                              df.ALT[~np.isnan(df.ALT)].mean() / 1000,
                              df.datetime.mean())
            
            Bn =  Bn.squeeze()
            Be =  Be.squeeze()
            Bd = -Bu.squeeze()
            
            df['IGRF_X'] = Bn
            df['IGRF_Y'] = Be
            df['IGRF_Z'] = Bd
            df['IGRF_F'] = la.norm([Bn, Be, Bd], axis=0)
        
        else:
            df['IGRF_X'] = ''
            df['IGRF_Y'] = ''
            df['IGRF_Z'] = ''
            df['IGRF_F'] = ''
            
            for i in range(0, len(df['datetime']), chunk):
                start = i
                stop  = i + chunk
                
                Be, Bn, Bu = igrf(df.LONG.iloc[start:stop],
                                  df.LAT.iloc[start:stop],
                                  df.ALT.iloc[start:stop] / 1000,
                                  df.datetime.iloc[start:stop])

                Bn = np.diagonal( Bn) # Must use np.diagonal because passing multiple locations to ppigrf is for calculating IGRF values over a grid (provides more values than we want)
                Be = np.diagonal( Be)
                Bd = np.diagonal(-Bu)
                
                df.IGRF_X.iloc[start:stop] = Bn
                df.IGRF_Y.iloc[start:stop] = Be
                df.IGRF_Z.iloc[start:stop] = Bd
                df.IGRF_F.iloc[start:stop] = la.norm([Bn, Be, Bd], axis=0)
                
    else:
        df['IGRF_X'] = ''
        df['IGRF_Y'] = ''
        df['IGRF_Z'] = ''
        df['IGRF_F'] = ''
    
    return df




def skip_lines(fname: str) -> int:
    '''
    Find number of header lines to skip when reading .sec file
    as a dataframe
    
    Parameters
    ----------
    fname
        File path/name to the .sec file
    
    Returns
    -------
    int
        Number of header lines to skip when reading .sec file
        as a dataframe
    '''

    with open(fname, 'r') as inFile:
        contents = inFile.readlines()
    
    for i, line in enumerate(contents):
        if '|' not in line:
            return i - 1
    
    return 0

def add_lla_cols(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Add latitude, longitude, and altitude columns for all samples
    in the dataframe (lat/lon in dd and alt in km above MSL)
    
    Parameters
    ----------
    df
        Dataframe of INTERMAGNET data
    
    Returns
    -------
    pd.DataFrame
        Dataframe of INTERMAGNET data with new latitude,
        longitude, and altitude columns
    '''
    
    lat = float(df.attrs['Geodetic Latitude'])  # (dd)
    lon = float(df.attrs['Geodetic Longitude']) # (dd)
    alt = float(df.attrs['Elevation'])          # (m)
    
    if lon > 180:
        lon -= 360
    
    df['LAT']  = lat
    df['LONG'] = lon
    df['ALT']  = alt
    
    return df

def add_attrs(df:    pd.DataFrame,
              fname: str) -> pd.DataFrame:
    '''
    
    '''
    
    with open(fname, 'r') as inFile:
        contents = inFile.readlines()
    
    for line in contents:
        if line[:1] != ' #':
            if 'Format' in line:
                df.attrs['Format'] = line.split('Format')[1].split('|')[0].strip()
                
            elif 'Source of Data' in line:
                df.attrs['Source of Data'] = line.split('Source of Data')[1].split('|')[0].strip()
                
            elif 'Station Name' in line:
                df.attrs['Station Name'] = line.split('Station Name')[1].split('|')[0].strip()
                
            elif 'IAGA Code' in line:
                df.attrs['IAGA Code'] = line.split('IAGA Code')[1].split('|')[0].strip()
                
            elif 'Geodetic Latitude' in line:
                df.attrs['Geodetic Latitude'] = line.split('Geodetic Latitude')[1].split('|')[0].strip()
                
            elif 'Geodetic Longitude' in line:
                df.attrs['Geodetic Longitude'] = line.split('Geodetic Longitude')[1].split('|')[0].strip()
                
            elif 'Elevation' in line:
                df.attrs['Elevation'] = line.split('Elevation')[1].split('|')[0].strip()
                
            elif 'Reported' in line:
                df.attrs['Reported'] = line.split('Reported')[1].split('|')[0].strip()
                
            elif 'Sensor Orientation' in line:
                df.attrs['Sensor Orientation'] = line.split('Sensor Orientation')[1].split('|')[0].strip()
                
            elif 'Digital Sampling' in line:
                df.attrs['Digital Sampling'] = line.split('Digital Sampling')[1].split('|')[0].strip()
                
            elif 'Data Interval Type' in line:
                df.attrs['Data Interval Type'] = line.split('Data Interval Type')[1].split('|')[0].strip()
                
            elif 'Data Type' in line:
                df.attrs['Data Type'] = line.split('Data Type')[1].split('|')[0].strip()
                
            elif 'Publication Date' in line:
                df.attrs['Publication Date'] = line.split('Publication Date')[1].split('|')[0].strip()
    
    return df

def parse_IAGA_2002(fname:     str,
                    fast_mode: bool=True,
                    chunk:     int=1000) -> pd.DataFrame:
    '''
    https://www.ncei.noaa.gov/services/world-data-system/v-dat-working-group/iaga-2002-data-exchange-format
    
    Parse INTERMAGNET sensor file in the IAGA 2002 format (.sec or .min)
    and return a pandas data frame with the resulting parsed data
    
    Parameters
    ----------
    fname
        File path/name to the .sec or .min file to parse
    fast_mode
        Calculate IGRF values based only on the first corrdinate
        in the .sec or .min file (speeds up parsing considerably)
    chunk
        If not parsing in `fast_mode`, set the number of samples
        to simultaneously calculate IGRF values for
    
    Returns
    -------
    pd.DataFrame
        Dataframe of INTERMAGNET data parsed from the given .sec or .min
        file - includes the following columns/fields:
        
        - DATE:      Date object (UTC)
        - TIME:      Number of seconds past UTC midnight
        - DOY:       Julian day of year (UTC)
        - X:         Magnetic field measurement in the North direction (nT)
        - Y:         Magnetic field measurement in the East direction (nT)
        - Z:         Magnetic field measurement in the Down direction (nT)
        - F:         Magnetic field measurement magnitude (nT)
        - datetime:  Datetime object (UTC)
        - epoch_sec: UNIX epoch timestamp (s)
        - LAT:       Latitude (dd)
        - LONG:      Longitude (dd)
        - ALT:       Altitude MSL (km)
        - IGRF_X:    IGRF magnetic field in the North direction (nT)
        - IGRF_Y:    IGRF magnetic field in the East direction (nT)
        - IGRF_Z:    IGRF magnetic field in the Down direction (nT)
        - IGRF_F:    IGRF magnetic field magnitude (nT)
    '''
    
    if fname.endswith('.sec') or fname.endswith('.min'):
        skip = skip_lines(fname)
        
        df = pd.read_csv(fname,
                         header=skip,
                         delim_whitespace=True,
                         na_values='99999.0')
        
        del df['|'] # Get rid of extra column (artifact of how .sec file headers are formatted)
        
        df.columns = ['DATE', 'TIME', 'DOY', 'X', 'Y', 'Z', 'F']
        df['TIME'] = pd.to_timedelta(df['TIME']).dt.total_seconds()
        
        df = df.dropna() # Must drop NaNs to get datetime column creation to work

        # want some columns as string for timestamp parsing DOY, and day-seconds
        # want them as native types otherwise for easof use
        date = pd.to_datetime(df['DATE'])
        df['datetime'] = pd.to_datetime(date.dt.year.astype(str) + df['DOY'].astype(int).astype(str),
                                        format='%Y%j',
                                        errors='coerce') + pd.to_timedelta(df['TIME'], unit='s')
        
        # add column for total number of seconds after epoch to make it easier
        # to interpolate between readings of multiple datasets
        df['epoch_sec'] = (df['datetime'] - pd.Timestamp('1970-01-01')).dt.total_seconds()
        
        df = add_attrs(df, fname)
        df = add_lla_cols(df)
        df = add_igrf_cols(df, fast_mode, chunk)

        return df.sort_values(by=['datetime'])
    
    return None

def loadInterMagData(data_dir: str,
                     fast_mode: bool=True,
                     chunk:     int=1000) -> dict:
    '''
    Walks through all the files saved in the InterMagnet data storage folder,
    and saves the data from all '.sec' files in that folder/subfolders. For
    each '.sec' file, the function decodes the file's data into a Pandas
    dataframe, determines the location of the data source (i.e. data is from
    Boulder CO or Touscon AZ, etc.), combines the data from the current '.sec'
    file with the previously saved data for that location, sorts the entire
    dataset of that location by day of year (DOY/Julian Day) and by
    day-seconds, and drops all rows with NaNs. After all '.sec' files are
    processed, a dictionary with combined data from each location is returned.
    
    Parameters
    ----------
    data_dir
        Path to directory that holds all INTERMAGNET .sec files
        to be parsed
    fast_mode
        Calculate IGRF values based only on the first corrdinate
        in the .sec file (speeds up parsing considerably)
    chunk
        If not parsing in `fast_mode`, set the number of samples
        to simultaneously calculate IGRF values for
    
    Returns
    -------
    dict
        Dictionary that includes all INTERMAGNET data parsed from .sec files
        found in `data_dir`
    '''
    
    data = {}
    
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith('.sec'):
                id = file[:3].upper()
                
                if id not in data.keys():
                    data[id] = parse_IAGA_2002(join(root, file),
                                               fast_mode,
                                               chunk)
                    
                else:
                    data[id] = pd.concat([data[id],
                                          parse_IAGA_2002(join(root, file),
                                                          fast_mode,
                                                          chunk)]).sort_values(by=['DOY', 'TIME']).dropna()
                    
                print('Loaded', file)
    
    return data