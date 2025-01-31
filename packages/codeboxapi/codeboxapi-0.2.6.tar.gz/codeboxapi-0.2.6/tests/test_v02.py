import time

import pytest

from codeboxapi import CodeBox, ExecChunk, ExecResult, RemoteFile


def test_sync_codebox_lifecycle(codebox: CodeBox):
    assert codebox.healthcheck() == "healthy", "CodeBox should be healthy"

    result = codebox.exec("print('Hello World!')")
    assert isinstance(result, ExecResult), "Exec should return an ExecResult"
    assert result.text.strip() == "Hello World!", "Exec should print 'Hello World!'"
    assert not result.errors, "Exec should not produce errors"

    file_name = "test_file.txt"
    file_content = b"Hello World!"
    codebox.upload(file_name, file_content)

    downloaded_file = codebox.download(file_name)
    assert isinstance(downloaded_file, RemoteFile), (
        "Download should return a RemoteFile"
    )
    assert downloaded_file.get_content() == file_content, (
        "Downloaded content should match uploaded content"
    )

    install_result = codebox.install("matplotlib")
    assert "matplotlib" in install_result, "Matplotlib should be installed successfully"

    exec_result = codebox.exec("import matplotlib; print(matplotlib.__version__)")
    assert exec_result.errors == [], "Importing matplotlib should not produce errors"
    assert exec_result.text.strip() != "", "Matplotlib version should be printed"

    plot_result = codebox.exec(
        "import matplotlib.pyplot as plt; "
        "plt.figure(figsize=(10, 5)); "
        "plt.plot([1, 2, 3, 4], [1, 4, 2, 3]); "
        "plt.title('Test Plot'); "
        "plt.xlabel('X-axis'); "
        "plt.ylabel('Y-axis'); "
        "plt.show()"
    )
    assert plot_result.images, "Plot execution should produce an image"
    assert len(plot_result.images) == 1, (
        "Plot execution should produce exactly one image"
    )


@pytest.mark.asyncio
async def test_async_codebox_lifecycle(codebox: CodeBox):
    assert await codebox.ahealthcheck() == "healthy", "CodeBox should be healthy"

    result = await codebox.aexec("print('Hello World!')")
    assert isinstance(result, ExecResult), "Exec should return an ExecResult"
    assert result.text.strip() == "Hello World!", "Exec should print 'Hello World!'"
    assert not result.errors, "Exec should not produce errors"

    file_name = "test_file.txt"
    file_content = b"Hello World!"
    await codebox.aupload(file_name, file_content)

    downloaded_file = await codebox.adownload(file_name)
    assert isinstance(downloaded_file, RemoteFile), (
        "Download should return a RemoteFile"
    )
    assert downloaded_file.get_content() == file_content, (
        "Downloaded content should match uploaded content"
    )

    install_result = await codebox.ainstall("matplotlib")
    assert "matplotlib" in install_result, "Matplotlib should be installed successfully"

    exec_result = await codebox.aexec(
        "import matplotlib; print(matplotlib.__version__)"
    )
    assert exec_result.errors == [], "Importing matplotlib should not produce errors"
    assert exec_result.text.strip() != "", "Matplotlib version should be printed"

    plot_result = await codebox.aexec(
        "import matplotlib.pyplot as plt; "
        "plt.figure(figsize=(10, 5)); "
        "plt.plot([1, 2, 3, 4], [1, 4, 2, 3]); "
        "plt.title('Test Plot'); "
        "plt.xlabel('X-axis'); "
        "plt.ylabel('Y-axis'); "
        "plt.show()"
    )
    assert plot_result.images, "Plot execution should produce an image"
    assert len(plot_result.images) == 1, (
        "Plot execution should produce exactly one image"
    )


def test_sync_list_operations(codebox: CodeBox):
    codebox.exec("x = 1; y = 'test'; z = [1, 2, 3]")
    variables = codebox.show_variables()
    assert "x" in variables.keys(), "Variable 'x' should be listed"
    assert "1" in variables["x"], "Variable 'x' should contain value '1'"
    assert "y" in variables.keys(), "Variable 'y' should be listed"
    assert "test" in variables["y"], "Variable 'y' should contain value 'test'"
    assert "z" in variables.keys(), "Variable 'z' should be listed"
    assert "[1, 2, 3]" in variables["z"], "Variable 'z' should contain value '[1, 2, 3]"

    files = codebox.list_files()
    assert isinstance(files, list), "list_files should return a list"
    assert all(isinstance(f, RemoteFile) for f in files), (
        "All items in list_files should be RemoteFile instances"
    )

    packages = codebox.list_packages()
    assert isinstance(packages, list), "list_packages should return a list"
    assert len(packages) > 0, "There should be at least one package installed"
    assert any("matplotlib" in pkg for pkg in packages), (
        "Matplotlib should be in the list of packages"
    )


@pytest.mark.asyncio
async def test_async_list_operations(codebox: CodeBox):
    await codebox.aexec("x = 1; y = 'test'; z = [1, 2, 3]")
    variables = await codebox.ashow_variables()
    assert "x" in variables.keys(), "Variable 'x' should be listed"
    assert "1" in variables["x"], "Variable 'x' should contain value '1'"
    assert "y" in variables.keys(), "Variable 'y' should be listed"
    assert "test" in variables["y"], "Variable 'y' should contain value 'test'"
    assert "z" in variables.keys(), "Variable 'z' should be listed"
    assert "[1, 2, 3]" in variables["z"], (
        "Variable 'z' should contain value '[1, 2, 3]'"
    )

    files = await codebox.alist_files()
    assert isinstance(files, list), "list_files should return a list"
    assert all(isinstance(f, RemoteFile) for f in files), (
        "All items in list_files should be RemoteFile instances"
    )

    packages = await codebox.alist_packages()
    assert isinstance(packages, list), "list_packages should return a list"
    assert len(packages) > 0, "There should be at least one package installed"
    assert any("matplotlib" in pkg for pkg in packages), (
        "Matplotlib should be in the list of packages"
    )


def test_sync_stream_exec(codebox: CodeBox):
    chunks: list[tuple[ExecChunk, float]] = []
    t0 = time.perf_counter()
    sleep = 0.01 if codebox.api_key == "local" else 1
    for chunk in codebox.stream_exec(
        f"import time;\nfor i in range(3): time.sleep({sleep}); print(i)"
    ):
        chunks.append((chunk, time.perf_counter() - t0))

    assert len(chunks) == 3, "iterating over stream_exec should produce 3 chunks"
    assert all(isinstance(chunk[0], ExecChunk) for chunk in chunks), (
        "All items should be ExecChunk instances"
    )
    assert all(chunk[0].type == "txt" for chunk in chunks), (
        "All chunks should be of type 'txt'"
    )
    assert [chunk[0].content.strip() for chunk in chunks] == [
        "0",
        "1",
        "2",
    ], "Chunks should contain correct content"
    # Verify chunks arrive with delay
    assert all(chunks[i][1] < chunks[i + 1][1] for i in range(len(chunks) - 1)), (
        "Chunks should arrive with delay"
    )
    # Verify chunks don't arrive all at once
    assert any(
        chunks[i + 1][1] - chunks[i][1] > 0.005 for i in range(len(chunks) - 1)
    ), "At least some chunks should have noticeable delay between them"


@pytest.mark.asyncio
async def test_sync_stream_exec_ipython(codebox: CodeBox):
    chunks = []
    t0 = time.perf_counter()
    sleep = 0.01 if codebox.api_key == "local" else 1
    for chunk in codebox.stream_exec(
        f"python -u -c 'import time\nfor i in range(3): time.sleep({sleep}); print(i)'",
        kernel="bash",
    ):
        chunks.append((chunk, time.perf_counter() - t0))

    assert len(chunks) == 3, "iterating over stream_exec should produce 3 chunks"
    assert all(isinstance(chunk[0], ExecChunk) for chunk in chunks), (
        "All items should be ExecChunk instances"
    )
    assert all(chunk[0].type == "txt" for chunk in chunks), (
        "All chunks should be of type 'txt'"
    )
    assert [chunk[0].content.strip() for chunk in chunks] == [
        "0",
        "1",
        "2",
    ], "Chunks should contain correct content"
    # Verify chunks arrive with delay
    assert all(chunks[i][1] < chunks[i + 1][1] for i in range(len(chunks) - 1)), (
        "Chunks should arrive with delay"
    )
    # Verify chunks don't arrive all at once
    assert any(
        chunks[i + 1][1] - chunks[i][1] > 0.005 for i in range(len(chunks) - 1)
    ), "At least some chunks should have noticeable delay between them"


@pytest.mark.asyncio
async def test_async_stream_exec_ipython(codebox: CodeBox):
    chunks: list[tuple[ExecChunk, float]] = []
    t0 = time.perf_counter()
    sleep = 0.01 if codebox.api_key == "local" else 1
    async for chunk in codebox.astream_exec(
        f"import time;\nfor i in range(3): time.sleep({sleep}); print(i)",
    ):
        chunks.append((chunk, time.perf_counter() - t0))

    assert len(chunks) == 3, "iterating over stream_exec should produce 3 chunks"
    assert all(isinstance(chunk[0], ExecChunk) for chunk in chunks), (
        "All items should be ExecChunk instances"
    )
    assert all(chunk[0].type == "txt" for chunk in chunks), (
        "All chunks should be of type 'txt'"
    )
    assert [chunk[0].content.strip() for chunk in chunks] == [
        "0",
        "1",
        "2",
    ], "Chunks should contain correct content"
    # Verify chunks arrive with delay
    assert all(chunks[i][1] < chunks[i + 1][1] for i in range(len(chunks) - 1)), (
        "Chunks should arrive with delay"
    )
    # Verify chunks don't arrive all at once
    assert any(
        chunks[i + 1][1] - chunks[i][1] > 0.005 for i in range(len(chunks) - 1)
    ), "At least some chunks should have noticeable delay between them"


@pytest.mark.asyncio
async def test_async_stream_exec_bash(codebox: CodeBox):
    chunks = []
    t0 = time.perf_counter()
    sleep = 0.01 if codebox.api_key == "local" else 1
    async for chunk in codebox.astream_exec(
        f"python -u -c 'import time\nfor i in range(3): time.sleep({sleep}); print(i)'",
        kernel="bash",
    ):
        chunks.append((chunk, time.perf_counter() - t0))

    assert len(chunks) == 3, "iterating over stream_exec should produce 3 chunks"
    assert all(isinstance(chunk[0], ExecChunk) for chunk in chunks), (
        "All items should be ExecChunk instances"
    )
    assert all(chunk[0].type == "txt" for chunk in chunks), (
        "All chunks should be of type 'txt'"
    )
    assert [chunk[0].content.strip() for chunk in chunks] == [
        "0",
        "1",
        "2",
    ], "Chunks should contain correct content"
    # Verify chunks arrive with delay
    assert all(chunks[i][1] < chunks[i + 1][1] for i in range(len(chunks) - 1)), (
        "Chunks should arrive with delay"
    )
    # Verify chunks don't arrive all at once
    assert any(
        chunks[i + 1][1] - chunks[i][1] > 0.005 for i in range(len(chunks) - 1)
    ), "At least some chunks should have noticeable delay between them"


def test_sync_error_handling(codebox: CodeBox):
    result = codebox.exec("1/0")
    assert result.errors, "Execution should produce an error"
    error = result.errors[0].lower()
    assert "division" in error and "zero" in error, (
        "Error should be a ZeroDivisionError"
    )


@pytest.mark.asyncio
async def test_async_error_handling(codebox: CodeBox):
    result = await codebox.aexec("1/0")
    assert result.errors, "Execution should produce an error"
    error = result.errors[0].lower()
    assert "division" in error and "zero" in error, (
        "Error should be a ZeroDivisionError"
    )


def test_sync_bash_commands(codebox: CodeBox):
    result = codebox.exec("echo ok", kernel="bash")
    assert "ok" in result.text, "Execution should contain 'ok'"
    result = codebox.exec("echo \"print('Hello!')\" > test.py", kernel="bash")
    assert result.text.strip() == "", "Execution result should be empty"
    assert "test.py" in [file.path for file in codebox.list_files()]
    result = codebox.exec("python test.py", kernel="bash")
    assert result.text.strip() == "Hello!", "Execution result should be 'Hello!'"


@pytest.mark.asyncio
async def test_async_bash_commands(codebox: CodeBox):
    result = await codebox.aexec("echo ok", kernel="bash")
    assert "ok" in result.text, "Execution should contain 'ok'"
    result = await codebox.aexec("echo 'print(\"Hello!\")' > test.py", kernel="bash")
    assert result.text.strip() == "", "Execution result should be empty"
    assert "test.py" in [file.path for file in await codebox.alist_files()]
    result = await codebox.aexec("python test.py", kernel="bash")
    assert result.text.strip() == "Hello!", "Execution result should be 'Hello!'"


def test_file_from_url(codebox: CodeBox):
    url = "https://raw.githubusercontent.com/shroominic/codebox-api/main/README.md"
    file_path = "README.md"
    remote_file = codebox.file_from_url(url, file_path)
    assert isinstance(remote_file, RemoteFile), "Should return a RemoteFile"
    assert remote_file.path == file_path, "File path should match"
    assert len(remote_file.get_content()) > 0, "File should have content"
    assert file_path in [file.path for file in codebox.list_files()]


@pytest.mark.asyncio
async def test_file_from_url_async(codebox: CodeBox):
    url = "https://raw.githubusercontent.com/shroominic/codebox-api/main/README.md"
    file_path = "README.md"
    remote_file = await codebox.afile_from_url(url, file_path)
    assert isinstance(remote_file, RemoteFile), "Should return a RemoteFile"
    assert remote_file.path == file_path, "File path should match"
    assert len(remote_file.get_content()) > 0, "File should have content"
    assert file_path in [file.path for file in await codebox.alist_files()]


def test_local_box_singleton():
    from codeboxapi.local import LocalBox

    with pytest.raises(RuntimeError) as exc_info:
        _ = LocalBox()

    assert "Only one LocalBox instance can exist at a time" in str(exc_info.value)

    with pytest.raises(RuntimeError) as exc_info:
        _ = CodeBox(api_key="local")

    assert "codeboxapi.com" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__])
