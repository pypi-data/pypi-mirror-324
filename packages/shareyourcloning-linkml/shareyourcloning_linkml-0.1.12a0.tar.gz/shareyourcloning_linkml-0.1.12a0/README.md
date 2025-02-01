# ShareYourCloning_LinkML

A LinkML data model for ShareYourCloning, a standardized schema for describing molecular cloning strategies and DNA assembly protocols.

## Website

[https://genestorian.github.io/ShareYourCloning_LinkML](https://genestorian.github.io/ShareYourCloning_LinkML)

## Repository Structure

* [examples/](examples/) - example data
* [project/](project/) - project files (do not edit these)
* [src/](src/) - source files (edit these)
  * [shareyourcloning_linkml](src/shareyourcloning_linkml)
    * [schema](src/shareyourcloning_linkml/schema) -- LinkML schema
      (edit this)
    * [datamodel](src/shareyourcloning_linkml/datamodel) -- generated
      Python datamodel
* [tests/](tests/) - Python tests

## Developer Documentation

The python package can be installed from PyPI:

```bash
pip install shareyourcloning-linkml
```

<details>
Use the `make` command to generate project artefacts:

* `make all`: make everything
* `make deploy`: deploys site
</details>

## Credits

This project was made with
[linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter).
