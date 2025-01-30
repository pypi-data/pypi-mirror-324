from setuptools import setup, find_packages

setup(
    name="api-gateway",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    setup_requires="setupmeta",
    versioning="distance",
    author="copilot-platform@netflix.com",
    url="https://github.netflix.net/corp/ncp-api-gateway",
    entry_points={
        "console_scripts": ["run-webapp = api_gateway.webapp:main", "tool-registry = api_gateway.tool_registry.register_tool:cli"],
    },
)
