import pandas as pd
import datetime as dt

# Import data from csv
climate_df = pd.read_csv('data/climate.csv')
death_df = pd.read_csv('data/deaths_pollution.csv')
co2_df = pd.read_csv('data/co2_emission.csv')

# Add 'Code' column to climate_df and co2_df
for df_name, col in {'climate_df': 'country', 'co2_df': 'Country Name'}.items():
    
    df = globals()[df_name]
    
    merged_df = pd.merge(
        left=df,
        right=death_df[['Entity', 'Code']],
        left_on=col,
        right_on='Entity',
        how='left')\
        .drop('Entity', axis=1)
    
    globals()[df_name] = merged_df

# Drop duplicates
for df_name in ['climate_df', 'death_df', 'co2_df']:

    df = globals()[df_name]
    df = df.drop_duplicates().reset_index(drop = True)
    globals()[df_name] = df

# Clean and filter climate_df
climate_df = climate_df[['location_name', 'latitude', 'longitude', 'last_updated', 'temperature_celsius',
                         'precip_mm', 'uv_index', 'air_quality_Carbon_Monoxide',
                         'air_quality_Ozone', 'air_quality_Nitrogen_dioxide',
                         'air_quality_Sulphur_dioxide', 'air_quality_PM2.5', 'air_quality_PM10',
                         'Code']]

climate_df['last_updated'] = pd.to_datetime(climate_df['last_updated'])

climate_df.rename(columns = {
    'precip_mm':'Precipitation (mm)', 'uv_index':'UV',
    'air_quality_Carbon_Monoxide':'CO', 'air_quality_Ozone':'O3',
    'air_quality_Nitrogen_dioxide':'NO2', 'air_quality_Sulphur_dioxide':'SO2',
    'air_quality_PM2.5':'PM2.5', 'air_quality_PM10':'PM10'}, inplace = True)

# Normalize the data in climate_df with the sample mean and std
for column in climate_df.columns[5:-1]:
    mean = climate_df[column].mean()
    std = climate_df[column].std()
    climate_df[f'{column}.norm'] = (climate_df[column] - mean) / std
    
climate_df['date'] = climate_df['last_updated'].dt.date

# Filter death_df
death_df = death_df[['Entity', 'Year', 'Air pollution (total) (deaths per 100,000)',
                     'Indoor air pollution (deaths per 100,000)',
                     'Outdoor particulate matter (deaths per 100,000)',
                     'Outdoor ozone pollution (deaths per 100,000)', 'Code']]

# Melt and clean co2_df
co2_df= pd.melt(
    frame = co2_df,
    id_vars = ['Country Name', 'country_code'],
    value_vars = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998',
                  '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
                  '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
                  '2017', '2018', '2019.1'],
    var_name = 'Year',
    value_name = 'CO2')\
    .sort_values(['country_code', 'Year'])\
    .reset_index(drop = True)\
    .rename(columns = {'country_code':'Code'})
    
co2_df['Year'] = co2_df['Year'].str.replace('2019.1', '2019').astype(int)