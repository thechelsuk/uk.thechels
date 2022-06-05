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
        required=True)
    arguments.add_argument('--label',
        type=str,
        help='The label gives us the file context',
        required=True)

    args = arguments.parse_args()
    content = args.content
    l = args.label

    root = pathlib.Path(__file__).parent.parent.resolve()
    print(f"input: {content}")
    c = content.replace('`','')
    print(f"Replaced {c}")
    p = root / f"_data/{l.strip()}.yml"

    try:
        with open(p, 'a') as f:
            o = f.write(f"- {c.strip()}")
            print(f"{l} completed\n{o}")
    except FileNotFoundError:
            print('File does not exist, unable to proceed')