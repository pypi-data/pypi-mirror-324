import click
from pydantic import ValidationError
from colorama import Fore, Style, init
from rich.console import Console

from api_gateway.models.tool_models import Info, RegistryTool, Permissions, GenAIProject
from api_gateway.tool_registry.tool_managers.configbin import ConfigbinManager
from api_gateway.tool_registry.tool_managers.danswer import DanswerToolManager
from api_gateway.tool_registry.tool_registry_operations import ToolRegistryOperations
from api_gateway.tool_registry.utils.discovery import (
    discover_openapi,
    get_app_name,
    get_endpoint_paths,
    get_path_methods,
    get_endpoint_schemas_and_components,
)
from api_gateway.tool_registry.utils.ncp_project_connection import get_gandalf_policy_from_ncp_project
from api_gateway.tool_registry.utils.validators import is_valid_id, is_valid_jsonpath
from api_gateway.services.gateway_service import process_schema

init(autoreset=True)
console = Console()


def print_header():
    header = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                   {Fore.WHITE + Style.BRIGHT}Netflix Tool Registry{Fore.CYAN}                      ║
║                                                              ║
║             Register and manage your GenAI tools             ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(header)


def section_header(text: str):
    print(f"\n{Style.BRIGHT}------ {text} ------{Style.RESET_ALL}")


def prompt(text: str) -> str:
    return input(f"{Fore.YELLOW}{text}{Style.RESET_ALL}").strip()


def highlight_options(text: str, options: list[str]) -> str:
    for option in options:
        text = text.replace(option, f"{Fore.CYAN}{option}{Style.RESET_ALL}")
    return text


def print_warning(text: str):
    print(f"{Fore.LIGHTRED_EX}{text}{Style.RESET_ALL}")


@click.group()
def cli():
    pass


@cli.command()
def create_tool():
    print_header()
    env = get_env_from_user()
    tool_ops = ToolRegistryOperations(configbin_manager=ConfigbinManager(env=env), danswer_manager=DanswerToolManager(env=env))
    tool = build_tool_request(tool_ops)

    if tool:
        try:
            print("-" * 20)
            print("Uploading tool to ConfigBin...")
            tool = tool_ops.add_tool(tool=tool, sync_to_danswer=False)
            print("Done uploading tool to ConfigBin...")
            print("-" * 20)

            danswer_sync = prompt("Sync tool to go/chat? (y/n): ").lower()
            while danswer_sync.lower() not in ["y", "n"]:
                danswer_sync = prompt("Please enter 'y' or 'n': ").lower()

            if danswer_sync.lower() == "y":
                print("Syncing tool to go/chat...")
                tool_ops.sync_tool_to_danswer(tool.tool_id)
                print("Done adding tool to go/chat")

            print("-" * 20)
            print(f"{Style.BRIGHT}{Fore.GREEN}Tool registration complete!{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Error when registering tool: {str(e)}{Style.RESET_ALL}")
            return


def get_env_from_user() -> str:
    section_header("Environment")
    print(
        highlight_options(
            "The environment you choose will determine where the tool is registered. This should be prod unless you have a specific reason to use test.",
            ["prod", "test"],
        )
    )
    env = prompt("Enter 'test' for test. Press Enter or input anything else for prod: ").lower()
    if env != "test":
        env = "prod"
    print(highlight_options(f"Setting up tool registration in {env}...", [env]))
    return env if env == "test" else "prod"


def get_tool_id_from_user(tool_ops: ToolRegistryOperations) -> str:
    section_header("Tool ID")
    tool_id = prompt("Enter tool id: ")
    while tool_ops.get_tool(tool_id, ignore_error=True) or not is_valid_id(tool_id):
        if tool_ops.get_tool(tool_id, ignore_error=True):
            print_warning(f"Tool ID {tool_id} already exists! Please choose a different tool id.\n")
        if not is_valid_id(tool_id):
            print_warning("Invalid tool id! Please use only alphanumeric characters, underscores, and dashes.\n")
        tool_id = prompt("Enter tool id: ")
    return tool_id


def get_ncp_project_from_user() -> str:
    section_header("Owner NCP/GenAI Project")
    print(
        highlight_options(
            "Connecting to an existing NCP project is required to register a tool. The NCP project's Gandalf policy will be used to determine tool ownership.",
            ["ownership"],
        )
    )
    print("If you don't have an NCP project, you can create one here: https://copilot.netflix.net/projects/my")
    ncp_env = prompt("Enter the environment your NCP project is in. Either 'test' or 'prod': ").lower()
    while ncp_env not in ["test", "prod"]:
        print_warning("Invalid env!")
        ncp_env = prompt("Please only enter either 'test' or 'prod': ").lower()
    ncp_project_id = prompt("Enter NCP project id: ")
    while True:
        gandalf_policy = get_gandalf_policy_from_ncp_project(ncp_project_id, ncp_env)
        if gandalf_policy:
            print(highlight_options(f"Successfully found project and fetched Gandalf policy: {gandalf_policy}", [gandalf_policy]))
            return ncp_env, ncp_project_id, gandalf_policy
        print_warning("Could not fetch Gandalf policy for given NCP project id. Please enter another NCP project id!")
        ncp_project_id = prompt("Enter NCP project id: ")


def get_info_from_user() -> Info:
    section_header("Tool Info")
    title = prompt("Enter title: ")
    description = prompt("Enter description: ")
    version = prompt("Enter version: ")
    return Info(title=title, description=description, version=version)


def get_path_and_method_from_user() -> tuple:
    section_header("Request Schema")
    base_url = prompt("Please enter the base URL (include port for internal endpoints): ").lower()
    spec = discover_openapi(base_url)
    while not spec:
        print_warning("Couldn't get OpenAPI docs from given URL. Please try another URL. (You might need to include the port, e.g. 7004)")
        base_url = prompt("Please enter the base URL (include port): ").lower()
        spec = discover_openapi(base_url)

    paths = get_endpoint_paths(spec=spec)
    print("\nAvailable paths:")
    for idx, path in enumerate(paths, 1):
        print(f"{idx}. {path}")

    selected_path = prompt("\nPlease enter a path or number from the list above: ")
    if selected_path.isdigit() and int(selected_path) <= len(paths):
        selected_path = paths[int(selected_path) - 1]
    else:
        while selected_path not in paths:
            print_warning("Path not in list above!")
            selected_path = prompt("\nPlease enter a path or number from the list above: ")
            if selected_path.isdigit() and int(selected_path) <= len(paths):
                selected_path = paths[int(selected_path) - 1]

    methods = get_path_methods(spec=spec, path=selected_path)
    print("\nAvailable methods:")
    for method in methods:
        print(f"- {method}")

    while True:
        selected_methods = prompt("\nPlease enter comma-separated methods (e.g., get,post): ").lower()
        while not selected_methods:
            print_warning("Please select at least one method!")
            selected_methods = prompt("\nPlease enter comma-separated methods (e.g., get,post): ").lower()

        selected_methods = [m.strip() for m in selected_methods.split(",")]

        valid_selections = [method for method in selected_methods if method in methods]
        if valid_selections:
            break
        else:
            print_warning("None of the selected methods are valid! Please choose from the available methods.")

    print("Selected methods: ", valid_selections)
    return base_url, selected_path, valid_selections, spec


def get_jsonpaths_from_user(request_schemas: dict) -> tuple:
    section_header("Pre/postprocessing Queries")
    print("Preprocessing and postprocessing queries are used to transform the request and response data/schemas.")
    print(
        highlight_options(
            "Unless your API returns very large (and irrelevant) data you need to filter, you can leave these empty.", ["empty"]
        )
    )
    preprocessing_jsonpath = prompt("\nEnter preprocessing jsonpath (or press Enter for empty string): ")
    while preprocessing_jsonpath and (
        not is_valid_jsonpath(preprocessing_jsonpath) or type(process_schema(request_schemas, preprocessing_jsonpath)) is not dict
    ):
        print_warning("Invalid jsonpath string!")
        preprocessing_jsonpath = prompt("\nEnter preprocessing jsonpath (or press Enter for empty string): ")

    postprocessing_jsonpath = prompt("\nEnter postprocessing jsonpath (or press Enter for empty string): ")
    while postprocessing_jsonpath and not is_valid_jsonpath(postprocessing_jsonpath):
        print_warning("Invalid jsonpath string!")
        postprocessing_jsonpath = prompt("\nEnter postprocessing jsonpath (or press Enter for empty string): ")
    return preprocessing_jsonpath, postprocessing_jsonpath


def get_tool_accessibility_from_user() -> str:
    section_header("Tool Accessibility")
    print("Only those under the owner NCP project's Gandalf policy can update or delete tools, regardless of accessibility.")
    print(
        highlight_options(
            "Public tools can be invoked by any user, while protected tools can only be invoked by those with access to the allowed projects you specify.",
            ["any", "allowed projects"],
        )
    )
    # visbility = input(
    #     "If you want to make the tool private, enter 'private'. Input anything else or press Enter to make the tool public: "
    # ).strip()
    # return visbility.lower() == "private"
    accessibility = prompt("Enter 'protected' to restrict access, or press Enter for public: ").lower()
    is_protected = accessibility == "protected"

    allowed_projects = []
    if is_protected:
        print("\nAdd projects that should have access to this tool (press Enter without input when done).")
        print(highlight_options("All users with access to these projects will be able to invoke the tool.", ["invoke"]))
        print(
            highlight_options(
                "Unless they have access to the owner project, they will NOT be able to update or delete the tool in the future.", ["NOT"]
            )
        )
        while True:
            ncp_env = prompt("\nEnter project environment ('test'/'prod') or press Enter to finish: ").lower()
            if not ncp_env:
                break

            if ncp_env not in ["test", "prod"]:
                print_warning("Please enter either 'test' or 'prod' only.")
                continue

            project_id = prompt("Enter NCP project id: ")
            if (project_id, ncp_env) in [(p.project_id, p.env) for p in allowed_projects]:
                print_warning("Project already added to allowed list.")
                continue

            gandalf_policy = get_gandalf_policy_from_ncp_project(project_id, ncp_env)
            if gandalf_policy:
                allowed_projects.append(GenAIProject(env=ncp_env, project_id=project_id, gandalf_policy=gandalf_policy))
                print(f"Added project {project_id} ({ncp_env}) to allowed list.")
            else:
                print_warning("Could not fetch Gandalf policy for given project. Project not added.")

    return "protected" if is_protected else "public", allowed_projects


def build_tool_request(tool_ops: ToolRegistryOperations) -> RegistryTool:
    print(f"\n{Style.BRIGHT}{Fore.GREEN}Let's register your custom tool! Please provide the following information:{Style.RESET_ALL}")
    tool_id = get_tool_id_from_user(tool_ops)
    owner_env, owner_project_id, owner_gandalf_policy = get_ncp_project_from_user()
    owner_ncp_project = GenAIProject(env=owner_env, project_id=owner_project_id, gandalf_policy=owner_gandalf_policy)

    info = get_info_from_user()

    base_url, selected_path, selected_methods, spec = get_path_and_method_from_user()
    invocation = {"endpoint": base_url + selected_path}
    if "netflix" in base_url:
        invocation["type"] = "metatron_endpoint"
        invocation["app_name"] = get_app_name(base_url)

    request_schemas, components, response_schemas = get_endpoint_schemas_and_components(
        path=selected_path, methods=selected_methods, spec=spec
    )
    preprocessing_jsonpath, postprocessing_jsonpath = get_jsonpaths_from_user(request_schemas)

    if preprocessing_jsonpath:
        # Currently doing this here so LLM generates request with preprocessing applied (instead of generating full request and then preprocessing)
        request_schemas = process_schema(request_schemas, preprocessing_jsonpath)

    accessibility, allowed_projects = get_tool_accessibility_from_user()
    permissions = Permissions(owner=owner_ncp_project, accessibility=accessibility, allowed_projects=allowed_projects)

    try:
        return RegistryTool(
            tool_id=tool_id,
            info=info,
            openapi=spec["openapi"],
            permissions=permissions,
            invocation=invocation,
            request_schema=request_schemas,
            preprocessing_jsonpath=preprocessing_jsonpath,
            response_schema=response_schemas,
            postprocessing_jsonpath=postprocessing_jsonpath,
            components=components,
        )
    except ValidationError as e:
        print_warning(f"\nError creating tool request: {e}")
        return None


if __name__ == "__main__":
    cli()
