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
        if path.is_file() and _is_pictorial_source(path):
            images.append(path)

    return images


def _validate_single_pictorial_source(folder, sources):
    if len(sources) <= 1:
        return

    names = ", ".join(source.name for source in sources)
    raise AssertionError(
        "Multiple Pictorial source files found in " + str(folder) + ": " + names
    )


def _is_layer_folder(path):
    prefix = "Layer_"
    return path.name.startswith(prefix) and path.name[len(prefix):].isdigit()


def _is_pictorial_source(path):
    return path.stem == "Pictorial" and path.suffix.lower() in IMAGE_EXTENSIONS


def _remove_non_pictorial_images(folder, dry_run):
    removed = 0

    for path in folder.iterdir():
        if not path.is_file():
            continue

        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        if _is_pictorial_source(path):
            continue

        removed += 1
        print("Removing:", path)

        if not dry_run:
            path.unlink()

    return removed


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
        "16",
        "-depth",
        "4",
        "-compress",
        "none",
        _magick_output_arg(output),
    ]

    subprocess.run(command, check=True)


def prepare_icons(root, size, output_format, keep_aspect, dry_run, skip_existing):
    magick = shutil.which("magick")
    if magick is None and not dry_run:
        raise RuntimeError(
            "ImageMagick was not found. Install it or add 'magick' to PATH."
        )

    size_text = str(size) + "x" + str(size)
    converted = 0
    skipped = 0
    missing = 0
    removed = 0

    for layer_folder in sorted(root.glob("Layer_*")):
        if not layer_folder.is_dir() or not _is_layer_folder(layer_folder):
            continue

        for number in range(1, 13):
            icon_folder = layer_folder / str(number)
            if not icon_folder.is_dir():
                missing += 1
                print("Missing folder:", icon_folder)
                continue

            if not skip_existing:
                removed += _remove_non_pictorial_images(icon_folder, dry_run)

            sources = _find_source_images(icon_folder, size_text)
            _validate_single_pictorial_source(icon_folder, sources)

            if not sources:
                missing += 1
                print("No source image:", icon_folder)
                continue

            for source in sources:
                output = _modified_path(source, size_text, output_format)

                if output.exists() and skip_existing:
                    skipped += 1
                    print("Already prepared:", output)
                    continue

                converted += 1
                if output.exists():
                    print("Replacing:", output)
                else:
                    print("Preparing:", source, "->", output)

                if not dry_run:
                    _convert_icon(magick, source, output, size_text, keep_aspect)

    return converted, skipped, missing, removed


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
        default=55,
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
        default= False,
        help="Keep the original aspect ratio instead of forcing a square image.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default= False,
        help="Show what would be converted without running ImageMagick.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        default=False,
        help="Replace existing prepared files instead of skipping them.",
    )

    args = parser.parse_args()
    root = args.path.resolve()

    if not root.exists():
        raise SystemExit("Path does not exist: " + str(root))

    converted, skipped, missing, removed = prepare_icons(
        root,
        args.size,
        args.format,
        args.keep_aspect,
        args.dry_run,
        not args.replace,
    )

    print()
    print("Converted:", converted)
    print("Skipped:", skipped)
    print("Missing/empty:", missing)
    print("Removed:", removed)


if __name__ == "__main__":
    main()
