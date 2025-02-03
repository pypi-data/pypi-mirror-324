def get_utils_boilerplate(group_id, artifact_id):
    """Return boilerplate code for the FieldChangeUtils utility class."""
    return f"""package {group_id}.{artifact_id}.core.utils;

import java.util.Objects;
import java.util.function.Consumer;
import java.util.function.Supplier;

public class FieldChangeUtils {{
    public static <T> void updateFieldIfChanged(Supplier<T> newSupplier, Supplier<T> currentValueSupplier, Consumer<T> setter) {{
        T newValue = newSupplier.get();
        T currentValue = currentValueSupplier.get();

        if (newValue != null && !Objects.equals(newValue, currentValue)) {{
            setter.accept(newValue);
        }}
    }}
}}
"""
