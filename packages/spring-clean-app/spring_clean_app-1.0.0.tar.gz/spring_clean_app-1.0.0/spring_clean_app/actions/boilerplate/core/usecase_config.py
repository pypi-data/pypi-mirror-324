def get_usecase_boilerplate(group_id, artifact_id):
    """Return boilerplate code for the UseCase abstract class."""
    return f"""package {group_id}.{artifact_id}.core.usecases;

public abstract class UseCase<I extends UseCase.InputValues, O extends UseCase.OutputValues> {{

    public abstract O execute(I input);

    public interface InputValues {{
    }}

    public interface OutputValues {{
    }}
}}
"""


def get_usecase_executor_boilerplate(group_id, artifact_id):
    """Return boilerplate code for the UseCaseExecutor interface."""
    return f"""package {group_id}.{artifact_id}.core.usecases;

import java.util.concurrent.CompletableFuture;
import java.util.function.Function;

public interface UseCaseExecutor {{
    <F, I extends UseCase.InputValues, O extends UseCase.OutputValues> CompletableFuture<F> execute(
            UseCase<I, O> useCase,
            I input,
            Function<O, F> outputMapper);
}}
"""


def get_usecase_executor_impl_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.presenter;

import {group_id}.{artifact_id}.core.usecases.UseCase;
import {group_id}.{artifact_id}.core.usecases.UseCaseExecutor;
import org.springframework.stereotype.Component;

import java.util.concurrent.CompletableFuture;
import java.util.function.Function;

@Component
public class UseCaseExecutorImpl implements UseCaseExecutor {{
    @Override
    public <F, I extends UseCase.InputValues, O extends UseCase.OutputValues> CompletableFuture<F> execute(UseCase<I, O> useCase, I input, Function<O, F> outputMapper) {{
        return CompletableFuture
                .supplyAsync(() -> input)
                .thenApplyAsync(useCase::execute)
                .thenApplyAsync(outputMapper);
    }}
}}
"""


def get_pagination_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.core.usecases;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Pagination<T> {{
    private Integer page;
    private Integer offset;
    private Integer totalPages;
    private Long totalItems;
    private List<T> items;
}}
"""
