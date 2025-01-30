## Development

```
python3 -m venv .venv
source .venv\Scripts\activate.bat
pip install git+https://github.com/wjakob/nanobind 'scikit-build-core[pyproject]'
pip install --no-build-isolation -ve .
```

### Configuring the libsixel build

```
meson setup --reconfigure \
    -Dimg2sixel=enabled \
    -Dgdk-pixbuf2=disabled \
    -Dgd=disabled \
    -Dlibcurl=disabled \
    -Dpng=disabled \
    -Djpeg=disabled \
    build
```
