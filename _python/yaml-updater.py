# importing modules
import pathlib
import argparse

if __name__ == "__main__":
    arguments = argparse.ArgumentParser(
        description='''Get content and labels to process file updates.'''
    )

    arguments.add_argument('--content',
        type=str,
        help='The body of text to use',
        nargs="*"
        required=True)
    arguments.add_argument('--label',
        type=str,
        help='The label gives us the file context',
        required=True)

    args = arguments.parse_args()
    iLabel = args.label
    c = args.content.replace('`','')

    root = pathlib.Path(__file__).parent.parent.resolve()
    p = root / f"_data/{iLabel.strip()}.yml"

    try:
        with open(p, 'a') as f:
            f.write(f"- {c.strip()}")
            print(f"{iLabel} completed\n")
    except FileNotFoundError:
            print('File does not exist, unable to proceed')