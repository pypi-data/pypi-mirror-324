import os
import argparse
import tempfile
import datetime as dt

import intermag as im


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--loc',     type=str,  required=True,  help='IAGA location code (3-letter)')
    parser.add_argument('-y', '--year',    type=int,  required=True,  help='Start year of dataset')
    parser.add_argument('-m', '--month',   type=int,  required=True,  help='Start month of dataset')
    parser.add_argument('-d', '--day',     type=int,  required=True,  help='Start day of dataset')
    parser.add_argument('-u', '--dur',     type=int,  required=True,  help='Duration of dataset in whole number of days')
    parser.add_argument('-p', '--plot',    type=bool, required=False, help='Bool of whether or not to plot the dataset')
    parser.add_argument('-s', '--savedir', type=str,  required=False, help='Directory to save the dataset to')

    args = parser.parse_args()
    
    if args.loc.upper() not in im.IAGA_CODES:
        print('ERROR: IAGA Code incorrect, got {}'.format(args.loc))
        exit()
    
    savedir = os.path.join(tempfile.gettempdir(), 'mag_data', args.loc)
    
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    
    if args.savedir is not None:
        if os.path.exists(args.savedir):
            savedir = args.savedir
        else:
            print('WARNING: Save path doesn\'t exist, got {}\nUsing temp directory instead'.format(args.savedir))

    plot = False
    
    if args.plot is not None:
        plot = args.plot
    
    ds = im.IM_Dataset()
    ds.download_dataset(iaga_code    = args.loc,
                        start_date   = dt.datetime(args.year, args.month, args.day),
                        load_dataset = plot,
                        num_days     = args.dur,
                        save_dir     = savedir)
    
    if plot:
        ds.plot_data()