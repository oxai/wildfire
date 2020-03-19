import argparse
import pandas as pd
import pgeocode


argparser = argparse.ArgumentParser()
argparser.add_argument("--input_file", type=str)
argparser.add_argument("--output_file", type=str, default="")
ARGS = argparser.parse_args()

if ARGS.output_file == "":
    ARGS.output_file = "latlons_" + ARGS.input_file

df = pd.read_csv(ARGS.input_file)
d = pgeocode.Nominatim('us')

new_rows = []
for i,r in df.iterrows():
    new_row = r.copy()
    zipcode = new_row['Zip']
    if zipcode == zipcode: # Check zip isn't nan
        lat_lon_df = d.query_postal_code(zipcode)
        lat, lon = lat_lon_df['latitude'], lat_lon_df['longitude']
    else:
        lat = lon = None
    new_row['lat'] = lat
    new_row['lon'] = lon
    new_rows.append(new_row)

out_df = pd.DataFrame(new_rows)
out_df.to_csv(ARGS.output_file)
