# NGO Hub

[![GitHub contributors][ico-contributors]][link-contributors]
[![GitHub last commit][ico-last-commit]][link-last-commit]
[![License: MPL 2.0][ico-license]][link-license]

The `ngohub` package facilitates the integration of Python projects with ngohub.ro


[A Simple Example](#a-simple-example) | [Feedback](#feedback) | [License](#license) | [About Code for Romania](#about-code-for-romania)

## A Simple Example

```python
from ngohub import NGOHub

# Create a new instance of the NGOHub class
hub = NGOHub(api_base_url="https://api.ngohub.ro")
if hub.is_healthy():
    print("The API is healthy")
else:
    print("The API is not healthy")
```

## Development

### Local development

1. Clone the repository
2. Create a virtual environment using python 3.12 or higher and activate it
    ```bash
    python3 -m venv venv && source venv/bin/activate
    ```
3. Install the dependencies
    ```bash
    pip install -r requirements/dev.txt
    ```

And you're ready to go.

### Running the tests

To run the tests, we use tox, to check for different environments and run multiple checks and configurations.

To run the tests, run the following command:

```bash
tox
```

### Updating the requirements

To update the requirements, you can run the following command:

```bash
tox -e update-requirements
```

### Creating a new release

1. Update the version in the `pyproject.toml` file
2. Create a new tag with the version and push it
3. Update the `CHANGELOG.md` file with the new changes

The GitHub Actions will take care of the rest.


## Feedback

* Request a new feature on GitHub.
* Vote for popular feature requests.
* File a bug in GitHub Issues.
* Email us with other feedback contact@code4.ro

## License

This project is licensed under the MPL 2.0 License – see the [LICENSE](LICENSE) file for details

## About Code for Romania

Started in 2016, Code for Romania is a civic tech NGO, official member of the Code for All network. We have a community of around 2.000 volunteers (developers, ux/ui, communications, data scientists, graphic designers, devops, it security and more) who work pro bono for developing digital solutions to solve social problems. #techforsocialgood. If you want to learn more details about our projects [visit our site][link-code4] or if you want to talk to one of our staff members, please e-mail us at contact@code4.ro.

Last, but not least, we rely on donations to ensure the infrastructure, logistics and management of our community that is widely spread across 11 timezones, coding for social change to make Romania and the world a better place. If you want to support us, [you can do it here][link-donate].


[ico-contributors]: https://img.shields.io/github/contributors/code4romania/pyngohub.svg?style=for-the-badge
[ico-last-commit]: https://img.shields.io/github/last-commit/code4romania/pyngohub.svg?style=for-the-badge
[ico-license]: https://img.shields.io/badge/license-MPL%202.0-brightgreen.svg?style=for-the-badge

[link-contributors]: https://github.com/code4romania/pyngohub/graphs/contributors
[link-last-commit]: https://github.com/code4romania/pyngohub/commits/main
[link-license]: https://opensource.org/licenses/MPL-2.0

[link-code4]: https://www.code4.ro/en/
[link-donate]: https://code4.ro/en/donate/
