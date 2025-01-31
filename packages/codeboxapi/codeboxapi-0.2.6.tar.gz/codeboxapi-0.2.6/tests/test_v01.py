import pytest

from codeboxapi import CodeBox


def test_sync(codebox: CodeBox) -> None:
    try:
        assert codebox.start() == "started"
        print("Started")

        assert codebox.status() == "running"
        print("Running")

        codebox.run("x = 'Hello World!'")
        assert codebox.run("print(x)") == "Hello World!\n"
        print("Printed")

        file_name = "test_file.txt"
        assert file_name in str(codebox.upload(file_name, b"Hello World!"))
        print("Uploaded")

        assert file_name in str(
            codebox.run("import os;\nprint(os.listdir(os.getcwd())); ")
        )
        assert file_name in str(codebox.list_files())

        assert codebox.download(file_name).get_content() == b"Hello World!"
        print("Downloaded")

        assert "matplotlib" in str(codebox.install("matplotlib"))

        assert (
            "error"
            != codebox.run("import matplotlib; print(matplotlib.__version__)").type
        )
        print("Installed")

        o = codebox.run(
            "import matplotlib.pyplot as plt;"
            "plt.plot([1, 2, 3, 4], [1, 4, 2, 3]); plt.show()"
        )
        assert o.type == "image/png"
        print("Plotted")

    finally:
        assert codebox.stop() == "stopped"
        print("Stopped")


@pytest.mark.asyncio
async def test_async(codebox: CodeBox) -> None:
    try:
        assert await codebox.astart() == "started"
        print("Started")

        assert await codebox.astatus() == "running"
        print("Running")

        await codebox.arun("x = 'Hello World!'")
        assert (await codebox.arun("print(x)")) == "Hello World!\n"
        print("Printed")

        file_name = "test_file.txt"
        assert file_name in str(await codebox.aupload(file_name, b"Hello World!"))
        print("Uploaded")

        assert file_name in str(
            await codebox.arun("import os;\nprint(os.listdir(os.getcwd())); ")
        )

        assert file_name in str(await codebox.alist_files())

        assert (await codebox.adownload(file_name)).get_content() == b"Hello World!"
        print("Downloaded")

        assert "matplotlib" in str(await codebox.ainstall("matplotlib"))

        assert (
            "error"
            != (
                await codebox.arun("import matplotlib; print(matplotlib.__version__)")
            ).type
        )
        print("Installed")

        o = await codebox.arun(
            "import matplotlib.pyplot as plt;"
            "plt.plot([1, 2, 3, 4], [1, 4, 2, 3]); plt.show()"
        )
        assert o.type == "image/png"
        print("Plotted")

    finally:
        assert await codebox.astop() == "stopped"
        print("Stopped")
