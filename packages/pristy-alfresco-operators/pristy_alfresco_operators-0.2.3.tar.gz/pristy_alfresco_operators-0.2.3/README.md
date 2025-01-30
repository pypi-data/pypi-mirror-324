# Pristy Alfresco operators for Airflow


## Release

Update version in `pyproject.toml` then

```shell
TAG=0.2.2
git add pyproject.toml
git commit -m "version $TAG"
git tag "$TAG"
git push
poetry build
poetry publish
```

