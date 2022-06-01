# importing modules
import pathlib
import helper

root = pathlib.Path(__file__).parent.parent.resolve()

if __name__ == "__main__":
    mdFile = root / "_pages/morning.md"
    mdFile_contents = mdFile.open().read()
    entries = helper.fetch_cfc_entries()[:5]
    content = "\n".join(
        ["- [{title}]({url}) - {published}".format(**entry) for entry in entries]
    )

    rewritten = helper.replace_chunk(mdFile_contents, "cfc_marker", content)
    mdFile.open("w").write(rewritten)
    print("CFC News completed")
