# 🧪✨ Contributing, Testing and Packaging `pipeglow` ✨📦

## 📝 Contributing ✨

These references will likely be helpful:

- [Getting Started](https://developer.govee.com/docs/getting-started) with the Govee API
- [Pipelines API](https://docs.gitlab.com/ee/api/pipelines.html)
- [Twine](https://twine.readthedocs.io/en/stable/)

## 🧪 Testing ✨

While you're developing, run a command like this in a loop to check and update the lights once every 15 seconds:

```bash
while true; do
    date
    uv run --with emoji,python-dotenv,python-gitlab python -m pipeglow change_the_lights
    sleep 15
done
```


## 📦 Packaging ✨

Publishing to TestPyPI with `uv`:

```toml
[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"
publish-url = "https://test.pypi.org/legacy/"
```

```
 uvx twine upload --comment  "🦄 hello world"   \
   --repository testpypi  --config-file ./.pypirc  \
   dist/pipeglow*  --verbose
```

When installing from Test PyPI:

```
uv pip install -i https://test.pypi.org/simple/ pipeglow --extra-index-url https://pypi.org/simple/
```   
