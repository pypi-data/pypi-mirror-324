# Development

If you want to get into **asmu** development, this page is a great way to get you started and set up with the needed tools. Follow this guide and start developing your own **asmu** processors, expand them to your needs or update the documentation, examples or tests.

**Every contribution is welcome!**

## Virtual environment

It is recommended to work with virtual environments, as it protects your local Python installation from becoming cluttered up with packages. Especially on Unix based systems, which deploys with protected system Python.

To create a virtual environment call the following command in the projects root folder.
=== "Windows"
    ```sh
    python -m venv .venv
    ```
=== "Unix/macOS"
    ```sh
    python3 -m venv .venv
    ```

This creates a virtual environment in the folder `.venv`.
To enable your newly created environment, the system specific activate-script has to be called.

=== "Windows"
    ```powershell
    .venv\Scripts\activate
    ```
=== "Unix/macOS"
    ```bash
    source .venv/bin/activate
    ```

After successful activation your shell input line should start with `(.venv)`. To deactivate type
```sh
deactivate
```

## Install package locally

The first important step is to install the package in editable mode. This is done by using pip with the `-e` argument. Inside the packages root folder and with the activated virtual environment call
```sh
pip install -e .
```
This will install the **asmu** package locally, in addition to the required dependencies.

## Build package

To prepare the package for distribution, it is built or packed into a specific form of archive. This is achieved with Pythons [build](https://pypi.org/project/build/) package. Usually, this is automatically handled by the GitLab pipeline for every new Tag. If you want to try it manually you first have to install or upgrade the build package with
```sh
python -m pip install --upgrade build
```
After that you can run
```sh
python -m build
```
in the root directory of the package.


## Documentation

The documentation is generated using [mkdocs-material](https://squidfunk.github.io/mkdocs-material) and automatically deployed for each commit by the GitLab pipeline to GitLab pages.
For the API section [mkdocstrings](https://mkdocstrings.github.io/) is used to parse the docstrings into an easy-to-read API documentation. If you want to edit the documentation it is recommended to install the following packages:
```bash
pip install mkdocs-material
pip install mkdocstrings
pip install mkdocstrings-python
```
You can now host the documentation locally, which automatically updates for every save, by running
```bash
mkdocs serve
```
and opening the returned IP address in your browser. To build the documentation run
```bash
mkdocs build -d .site --strict
```
The `--strict` argument is used to catch every warning. This also ensures that the pipeline will pass. It is important to specify a build directory with the `-d` argument, because the standard directory conflicts with the build package.

## Testing

The **asmu** package uses automatic test via [pytest](https://pypi.org/project/pytest/). The tests are located in the `tests` folder. To ensure the package's audio processors speeds are not negatively effected by changes to the code, the [pytest-benchamrk](https://pypi.org/project/pytest-benchmark/) plugin is used to monitor their execution times. There are no limiting values, but the execution times can be compared manually. The automatic tests run via the GitLab pipeline for every commit.

## Profiling

When working on the audio core elements of the **asmu** package, it is very important to keep execution times and memory usage as low as possible. Memory assertions should be avoided. To achieve this, there are some recommended profiling tools where you can check your code line-by-line to optimize its performance. These profiling tools can be enabled for certain functions of your code, by wrapping them wit the `@profile` decorator.

### line_profiler
The recommended profiler for execution times is the [line_profiler](https://pypi.org/project/line-profiler/). It can be installed by running
```sh
pip install line_profiler
```
To profile your code, wrap the function(s) you want to analyze with the `@profile` decorator and run your script via
```sh
kernprof -l -v .\test.py
```

### memory_profiler
The [memory_profiler](https://pypi.org/project/memory-profiler/) can be used to analyze used and newly asserted memory. To install it run
```sh
pip install memory_profiler
```
To profile your code, wrap the function(s) you want to analyze with the `@profile` decorator and run your script via
```sh
python -m memory_profiler .\test.py
```

!!! tip
    If try to run a script with a `@profile` decorator directly, this results in an error. To avoid this, you can find useful commands in the `profiling.py` script in the `examples` folder.
