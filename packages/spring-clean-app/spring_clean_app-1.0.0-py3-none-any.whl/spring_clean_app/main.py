import click

from spring_clean_app.actions import download_project
from spring_clean_app.actions.boilerplate.dependencies_config import (
    add_dependencies_to_gradle,
)
from spring_clean_app.actions.project_structure import *
from spring_clean_app.utils.prompts import prompt_with_validator
from spring_clean_app.utils.validators import ExistedValuesValidator, RegexValidator


@click.group()
def cli():
    """Main entry point for the CLI."""
    pass


@click.command()
def create():
    # 1. Get Basic configuration for download project
    build_tool_validator = ExistedValuesValidator(
        ["maven", "gradle"], "Invalid value!! Value should be 'gradle' or 'maven'"
    )
    build_tool = prompt_with_validator(
        "Enter build tool",
        "maven",
        build_tool_validator,
    )

    group_id_validator = RegexValidator(
        r"^[a-zA-Z].*", "Invalid value! It should start with a letter."
    )
    group_id = prompt_with_validator("Enter groupId", "com.example", group_id_validator)
    artifact_id = prompt_with_validator("Enter artifactId", "demo", group_id_validator)

    # 2. Select more option
    database_validator = ExistedValuesValidator(
        ["mysql"], "Invalid value!! Value should be 'mysql'"
    )
    database = prompt_with_validator("Enter database type", "mysql", database_validator)

    default_dependencies = ["lombok,web,flyway,validation,data-jpa,webflux"]
    default_dependencies.append(database)

    # 3. download project
    options = {
        "type": "gradle-project" if build_tool == "gradle" else "maven-project",
        "language": "java",
        "packaing": "jar",
        "groupId": group_id,
        "artifactId": artifact_id,
        "name": artifact_id,
        "dependencies": ",".join(default_dependencies),
        "database": database,
    }

    create_boilerplate(options)
    click.echo(click.style(f"\n🎉 Setup Complete!", fg="green"))


def create_boilerplate(options):
    base_path = download_project.download(options)
    print(f"✅ Get sample code successfully!")

    src_main_resources, _, package_path = init_base_path(
        base_path, options["groupId"], options["artifactId"]
    )

    if options["type"] == "gradle-project":
        gradle_file_path = os.path.join(base_path, "build.gradle")
        add_dependencies_to_gradle(gradle_file_path)
    else:
        pom_file_path = os.path.join(base_path, "pom.xml")
        add_dependencies_to_pom(pom_file_path)
    print(f"✅ Dependencies successfully added!")

    create_app_resource(src_main_resources, options["artifactId"], options)
    create_folders_tree(
        package_path, options["groupId"], options["artifactId"], root_app_packages
    )
    print(f"✅ Create clean architecture boilerplate successfully!")

    override_application_file(package_path, options["groupId"], options["artifactId"])


cli.add_command(create, name="init")

if __name__ == "__main__":
    cli()
