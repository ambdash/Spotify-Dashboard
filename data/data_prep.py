import pandas as pd

df = pd.read_csv('./songs_normalize.csv')
df = df.loc[df['year'].isin([*range(1999, 2020)])]
df.drop_duplicates(subset=['artist', 'song'], inplace=True)
df = df.sort_values('year')
df['artist_track'] = df[['artist', 'song']].agg(' - '.join, axis=1)  # full track name with artist
df['duration_min'] = df['duration_ms'] / (1000 * 60) % 60  # convert to min
df = df.join(df['genre'].str.split(', ', expand=True).add_prefix('genre_'))  # split genres to columns

unique_genres = list(
    set(df.genre_0) | set(df.genre_1[~df.genre_1.isnull()]) | set(df.genre_2[~df.genre_2.isnull()]) | set(
        df.genre_3[~df.genre_3.isnull()]))
duration = int(round(sum(df['duration_min'])))
n_tracks = len(df['song'])
n_artists = df['artist'].nunique()
n_genres = len(unique_genres)
min_year = min(df['year'])
max_year = max(df['year'])
