import xml.etree.ElementTree as ET

dependencies_to_add = [
    {
        "groupId": "org.springdoc",
        "artifactId": "springdoc-openapi-starter-webmvc-ui",
        "version": "2.8.4",
    },
    {
        "groupId": "org.apache.commons",
        "artifactId": "commons-lang3",
        "version": "3.12.0",
    },
    {
        "groupId": "com.cosium.spring.data",
        "artifactId": "spring-data-jpa-entity-graph",
        "version": "3.2.2",
    },
]


def add_dependencies_to_pom(pom_file_path):
    """Modify an existing pom.xml file to add new dependencies without duplication."""

    # Parse the existing pom.xml file
    tree = ET.parse(pom_file_path)
    root = tree.getroot()

    # Define Maven's XML namespace (Spring Initializr-generated POMs use this)
    namespace = {"mvn": "http://maven.apache.org/POM/4.0.0"}
    ET.register_namespace("", namespace["mvn"])

    # Locate the <dependencies> section, or create one if it doesn't exist
    dependencies_section = root.find("mvn:dependencies", namespace)
    if dependencies_section is None:
        dependencies_section = ET.SubElement(root, "dependencies")

    # Add new dependencies only if they don't already exist
    for dep in dependencies_to_add:
        exists = any(
            d.find("mvn:groupId", namespace).text == dep["groupId"]
            and d.find("mvn:artifactId", namespace).text == dep["artifactId"]
            for d in dependencies_section.findall("mvn:dependency", namespace)
        )
        if not exists:
            dependency_element = ET.SubElement(dependencies_section, "dependency")
            ET.SubElement(dependency_element, "groupId").text = dep["groupId"]
            ET.SubElement(dependency_element, "artifactId").text = dep["artifactId"]
            ET.SubElement(dependency_element, "version").text = dep["version"]

    # Save the updated pom.xml file
    tree.write(pom_file_path, encoding="utf-8", xml_declaration=True)


def add_dependencies_to_gradle(build_gradle_path):
    """
    Modify an existing build.gradle file to add new dependencies without duplication.
    """
    # Read the current build.gradle file
    with open(build_gradle_path, "r") as file:
        lines = file.readlines()

    # Define where dependencies block starts and ends
    in_dependencies_block = False
    existing_dependencies = set()

    # Extract all existing dependencies
    for line in lines:
        if line.strip().startswith("dependencies {"):
            in_dependencies_block = True
        elif in_dependencies_block and line.strip().startswith("}"):
            in_dependencies_block = False
        elif in_dependencies_block:
            # Extract existing dependency strings
            stripped_line = line.strip()
            if stripped_line.startswith("implementation"):
                existing_dependencies.add(stripped_line)

    # Build new dependency lines
    new_dependency_lines = []
    for dep in dependencies_to_add:
        dep_line = f'    implementation "{dep["groupId"]}:{dep["artifactId"]}:{dep["version"]}"\n'
        if dep_line.strip() not in existing_dependencies:
            new_dependency_lines.append(dep_line)

    # Inject new dependencies into the dependencies block
    updated_lines = []
    for line in lines:
        updated_lines.append(line)
        if line.strip().startswith("dependencies {"):
            updated_lines.extend(new_dependency_lines)

    # Write back to the build.gradle file
    with open(build_gradle_path, "w") as file:
        file.writelines(updated_lines)
