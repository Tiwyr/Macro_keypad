import argparse
import shutil
import subprocess
from pathlib import Path


IMAGE_EXTENSIONS = {".bmp", ".png", ".jpg", ".jpeg", ".gif", ".webp"}


def _is_modified_icon(path, size_text):
    return path.stem.endswith("_modified_" + size_text)


def _modified_path(source, size_text, output_format):
    return source.with_name(source.stem + "_modified_" + size_text + "." + output_format)


def _find_source_images(folder, size_text):
    images = []

    for path in folder.iterdir():
        if not path.is_file():
            continue

        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        if _is_modified_icon(path, size_text):
            continue

        images.append(path)

    return images


def _magick_output_arg(output_path):
    if output_path.suffix.lower() == ".bmp":
        return "BMP3:" + str(output_path)

    return str(output_path)


def _convert_icon(magick, source, output, size_text, keep_aspect):
    resize = size_text if keep_aspect else size_text + "!"
    command = [
        magick,
        str(source),
        "-resize",
        resize,
        "-colors",
        "256",
        "-depth",
        "8",
        "-compress",
        "none",
        _magick_output_arg(output),
    ]

    subprocess.run(command, check=True)


def prepare_icons(root, size, output_format, keep_aspect, dry_run):
    magick = shutil.which("magick")
    if magick is None and not dry_run:
        raise RuntimeError(
            "ImageMagick was not found. Install it or add 'magick' to PATH."
        )

    size_text = str(size) + "x" + str(size)
    converted = 0
    skipped = 0
    missing = 0

    for layer_folder in sorted(root.glob("Layer_*")):
        if not layer_folder.is_dir():
            continue

        for number in range(1, 13):
            icon_folder = layer_folder / str(number)
            if not icon_folder.is_dir():
                missing += 1
                print("Missing folder:", icon_folder)
                continue

            sources = _find_source_images(icon_folder, size_text)
            if not sources:
                missing += 1
                print("No source image:", icon_folder)
                continue

            for source in sources:
                output = _modified_path(source, size_text, output_format)

                if output.exists():
                    skipped += 1
                    print("Already prepared:", output)
                    continue

                converted += 1
                print("Preparing:", source, "->", output)

                if not dry_run:
                    _convert_icon(magick, source, output, size_text, keep_aspect)

    return converted, skipped, missing


def main():
    parser = argparse.ArgumentParser(
        description="Prepare Layer_x/1-12 icon images for CircuitPython display use."
    )
    parser.add_argument(
        "path",
        type=Path,
        default = "E:\\images",
        help="Folder containing Layer_x folders, for example E:\\images",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=54,
        help="Icon width and height in pixels. Default: 40",
    )
    parser.add_argument(
        "--format",
        default="bmp",
        choices=("bmp", "png"),
        help="Output format. Default: bmp",
    )
    parser.add_argument(
        "--keep-aspect",
        action="store_true",
        default= True,
        help="Keep the original aspect ratio instead of forcing a square image.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default= False,
        help="Show what would be converted without running ImageMagick.",
    )

    args = parser.parse_args()
    root = args.path.resolve()

    if not root.exists():
        raise SystemExit("Path does not exist: " + str(root))

    converted, skipped, missing = prepare_icons(
        root,
        args.size,
        args.format,
        args.keep_aspect,
        args.dry_run,
    )

    print()
    print("Converted:", converted)
    print("Skipped:", skipped)
    print("Missing/empty:", missing)


if __name__ == "__main__":
    main()