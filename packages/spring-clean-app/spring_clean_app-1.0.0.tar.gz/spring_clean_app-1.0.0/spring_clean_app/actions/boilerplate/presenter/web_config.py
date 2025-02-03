def get_globalized_thread_local_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.presenter.config;

public class GlobalizedThreadLocal {{
    public static final ThreadLocal<String> currentUser = new java.lang.ThreadLocal<>();

    private GlobalizedThreadLocal() {{
        throw new IllegalArgumentException("Utility class");
    }}
}}
"""
