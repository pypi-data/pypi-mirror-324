def get_resource_notfound_exception(group_id, artifact_id):
    """Return ResourceNotFoundException."""
    return get_exception_boilerplate(group_id, artifact_id, "ResourceNotFoundException")


def get_badrequest_exception(group_id, artifact_id):
    """Return BadRequestException."""
    return get_exception_boilerplate(group_id, artifact_id, "BadRequestException")


def get_exception_boilerplate(group_id, artifact_id, exception_name):
    """Return boilerplate code for a custom exception."""
    return f"""package {group_id}.{artifact_id}.core.exception;

public class {exception_name} extends RuntimeException {{
    public {exception_name}() {{
    }}

    public {exception_name}(String message) {{
        super(message);
    }}

    public {exception_name}(String message, Throwable cause) {{
        super(message, cause);
    }}

    public {exception_name}(Throwable cause) {{
        super(cause);
    }}
}}
"""
