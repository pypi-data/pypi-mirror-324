import json
import os
from typing import Any, Dict, List, Union

from pydantic import BaseModel


class TorrentFileData(BaseModel):
    name: str
    link: str
    infohash: str
    created_unix: int
    scraped_date: int
    dht_scraped: Union[int, None]
    dht_peers: Union[int, None]
    seeders: int
    leechers: int
    size_bytes: int
    type: str
    path: Union[str, None]


class Torrent(BaseModel):
    data: TorrentFileData
    ratio: float
    progress: float
    done: bool


class TorrentConnectionSettings(BaseModel):
    url: str = "http://localhost:9091"
    username: Union[str, None] = "username"
    password: Union[str, None] = "password"


class TorrentConfigSchema(BaseModel):
    provider: str = "transmission"
    enabled: bool = True
    connection_settings: TorrentConnectionSettings = TorrentConnectionSettings()


class SettingsSchema(BaseModel):
    torrent_files_dir: str = "./libgen-seedtools-data/torrentfiles"
    assets_dir: str = "./libgen-seedtools-data/data"
    torrent_data_url: List[str] = [
        "https://zrthstr.github.io/libgen_torrent_cardiography/torrent.json",
    ]
    max_disk_usage: str = "100GB"
    default_source: str = "torrent"
    include_types: List[str] = ["fiction", "books", "scimag"]
    torrent_seeders_range: List[int] = [1, 3]


class ConfigSchema(BaseModel):
    version: float = 1.1
    torrent: TorrentConfigSchema = TorrentConfigSchema()
    settings: SettingsSchema = SettingsSchema()


class Ctx(BaseModel):
    config: ConfigSchema
    configPath: str

    class Config:
        arbitrary_types_allowed = True


def getctx(ctx: Dict[str, Any]) -> Ctx:
    return Ctx(**ctx)


def save(ctx: Ctx):
    with open(ctx.configPath, "w") as out:
        out.write(json.dumps(ctx.config.dict(), indent=2, sort_keys=True))


def load_config(path: str) -> ConfigSchema:
    if os.path.exists(path):
        try:
            with open(path) as config_file:
                return ConfigSchema(**json.loads(config_file.read()))
        except:
            return ConfigSchema()
    return ConfigSchema()
