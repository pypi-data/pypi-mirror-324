from dataclasses import dataclass
from typing import Iterator, IO

import fastavro
from fastavro import reader, writer
from fastavro.types import Schema


@dataclass
class Data:
    schema: Schema
    records: Iterator[dict]


def read(content) -> (Iterator[dict], Schema):
    _reader = reader(content)
    return (_ for _ in _reader), _reader.writer_schema,


def is_avro(file_path: str):
    return fastavro.is_avro(file_path)


def is_avro_data(buffer: IO):
    return fastavro.is_avro(buffer)


def write(output_stream, schema: Schema, records: Iterator[dict]):
    writer(output_stream, schema, records)
