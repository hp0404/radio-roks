import click
import time
import datetime
from sqlite_utils import Database
from roks import date_range, scrape, DATE_FORMAT


formats = [DATE_FORMAT]


@click.group()
@click.version_option()
def cli():
    "Scrape RADIOROKS playlists to SQLite"


@cli.command("playlist")
@click.argument(
    "database",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option("-t", "--table", default="playlist", type=click.STRING)
@click.option("--date", type=click.DateTime(formats))
@click.option("--since", type=click.DateTime(formats))
@click.option("--until", type=click.DateTime(formats))
@click.option("--delay", type=click.INT, default=1, show_default=True)
def save_playlist(
    database, table, date=None, since=None, until=None, delay=1
):
    """
    Download daily playlists, for a date or a range
    """
    if not any([date, since, until]):
        dates = [datetime.date.today()]
    elif date:
        dates = [date.date()]
    elif since and until:
        dates = [*date_range(since.date(), until.date())]
    elif since or until:
        raise ValueError(
            "Invalid dates. Please provide either a single date, or both since and until arguments."
        )
    
    if not isinstance(database, Database):
        database = Database(database)
    
    table = database.table(table, extracts={"artist": "artists"})
    for date in dates:
        click.echo(f"Downloading playlist for {date}")
        songs = scrape(date)
        table.upsert_all(songs, pk="datetime")
        if len(dates) > 1:
            time.sleep(delay)


if __name__ == "__main__":
    cli()