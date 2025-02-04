
class BulkBytes(bytes):
    HEADER_SIZE:    int = 16
    CAN_BLOCK_SIZE: int =  8

    def get_block(self, index: int) -> bytes:
        start = index * self.CAN_BLOCK_SIZE
        stop  = min(start + self.CAN_BLOCK_SIZE, len(self))
        return self[start:stop]
