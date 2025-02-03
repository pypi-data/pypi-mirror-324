from pyarrow import Buffer, BufferReader, NativeFile


def read_data(buffer: bytes | Buffer) -> NativeFile:
    return BufferReader(buffer)
