import click

from datetime import datetime
from urllib.parse import urlparse

from pytz import utc
from transmission_rpc import client, torrent
from transmission_rpc.error import TransmissionConnectError

from .schemas import Ctx, Torrent, TorrentFileData


def _make_client(ctx: Ctx) -> client.Client:
    settings = ctx.config.torrent.connection_settings
    parsed = urlparse(settings.url)
    try:
        con = client.Client(
            protocol=parsed.scheme,
            host=parsed.hostname,
            port=parsed.port,
            username=settings.username,
            password=settings.password,
        )
        return con
    except TransmissionConnectError as err:
        click.secho(
            f"Failed to connect to transmission rpc api {parsed.scheme}://{parsed.hostname}:{parsed.port}\n",
            fg="red",
            reset=False,
        )
        raise SystemExit(err)


def add_torrent(ctx: Ctx, tfd: TorrentFileData, auto_verify=False) -> Torrent:
    now = utc.localize(datetime.utcnow())
    c = _make_client(ctx)
    magnet_url = f"magnet:?xt=urn:btih:{tfd.infohash}&dn={tfd.name}"
    torrent_id = c.add_torrent(magnet_url)
    torrent = c.get_torrent(torrent_id.id)

    if torrent.added_date >= now and auto_verify:
        c.verify_torrent([torrent_id.id], timeout=60.0)

    return Torrent(
        data=tfd,
        ratio=torrent.ratio if torrent.ratio >= 0 else 0,
        progress=torrent.progress,
        done=torrent.status == "seeding",
    )
