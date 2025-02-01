from pixel_sizes import Size, SIZES


def test_sizes() -> None:
    assert SIZES["8k"].aspect_ratio() == 16 / 9
    assert SIZES["4k"].rotate() == Size(2160, 3840)
    assert SIZES["2k"].rotate() == Size(1440, 2560)
    assert SIZES["Full HD"].rotate() == Size(1080, 1920)
    assert SIZES["HD"].rotate() == Size(720, 1280)
    assert SIZES["480p"].rotate() == Size(480, 854)
    assert SIZES["360p"].rotate() == Size(360, 640)
    assert SIZES["240p"].rotate() == Size(240, 426)
    assert SIZES["144p"].rotate() == Size(144, 256)


def test_size_rotate() -> None:
    size = Size(1920, 1080)
    assert size.rotate().rotate() == size


def test_size_aspect_ratio() -> None:
    size = Size(1920, 1080)
    assert size.aspect_ratio() == 16 / 9

    size = Size(1280, 720)
    assert size.aspect_ratio() == 16 / 9
