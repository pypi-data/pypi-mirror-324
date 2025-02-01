from dataclasses import dataclass


@dataclass(frozen=True)
class Size:
    width: int
    height: int

    def aspect_ratio(self) -> float:
        return self.width / self.height

    def rotate(self) -> "Size":
        return Size(self.height, self.width)


SIZES = {
    "8k": Size(7680, 4320),
    "4k": Size(3840, 2160),
    "2k": Size(2560, 1440),
    "Full HD": Size(1920, 1080),
    "HD": Size(1280, 720),
    "480p": Size(854, 480),
    "360p": Size(640, 360),
    "240p": Size(426, 240),
    "144p": Size(256, 144),
}


__all__ = ["Size", "SIZES"]
