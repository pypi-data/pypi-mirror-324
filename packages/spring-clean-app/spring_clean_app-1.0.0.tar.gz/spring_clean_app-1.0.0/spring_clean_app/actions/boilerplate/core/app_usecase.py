def get_product_repository_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.core.usecases.product;

import {group_id}.{artifact_id}.core.domain.Product;
import {group_id}.{artifact_id}.core.usecases.Pagination;

public interface ProductRepository {{
    Pagination<Product> findAll(Integer pageSize, Integer currentPage, String searchingText);

    Product persist(Product product);

}}
"""


def get_all_product_usecase_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.core.usecases.product;

import {group_id}.{artifact_id}.core.domain.Product;
import {group_id}.{artifact_id}.core.usecases.Pagination;
import {group_id}.{artifact_id}.core.usecases.UseCase;
import lombok.Value;
import org.springframework.stereotype.Component;

@Component
public class GetAllProductUseCase extends UseCase<GetAllProductUseCase.InputValues, GetAllProductUseCase.OutputValues> {{

    private final ProductRepository productRepository;

    public GetAllProductUseCase(ProductRepository productRepository) {{
        this.productRepository = productRepository;
    }}

    @Override
    public OutputValues execute(InputValues input) {{
        Pagination<Product> all = productRepository.findAll(
                input.getOffset(),
                input.getPage(),
                input.getSearchingText());

        return new OutputValues(all);
    }}

    @Value
    public static class InputValues implements UseCase.InputValues {{
        Integer page;
        Integer offset;
        String searchingText;
    }}

    @Value
    public static class OutputValues implements UseCase.OutputValues {{
        Pagination<Product> allProducts;
    }}
}}
"""


def create_product_usecase_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.core.usecases.product;

import {group_id}.{artifact_id}.core.domain.Genre;
import {group_id}.{artifact_id}.core.domain.Product;
import {group_id}.{artifact_id}.core.usecases.UseCase;
import lombok.Value;
import org.springframework.stereotype.Component;

@Component
public class CreateProductUseCase extends UseCase<CreateProductUseCase.InputValues, CreateProductUseCase.OutputValues> {{

    private final ProductRepository productRepository;

    public CreateProductUseCase(ProductRepository productRepository) {{
        this.productRepository = productRepository;
    }}

    @Override
    public OutputValues execute(InputValues input) {{
        Product product = Product.builder()
                .genre(Genre.builder()
                        .id(input.getGenreId())
                        .build())
                .productName(input.getProductName())
                .price(input.getPrice())
                .build();

        productRepository.persist(product);
        return new OutputValues();
    }}

    @Value
    public static class InputValues implements UseCase.InputValues {{
        String productName;
        Long genreId;
        Double price;
    }}

    @Value
    public static class OutputValues implements UseCase.OutputValues {{

    }}
}}
"""


def get_get_all_todo_usecase_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.core.usecases.placeholder;

import {group_id}.{artifact_id}.infra.external.entities.Todo;
import {group_id}.{artifact_id}.core.usecases.UseCase;
import lombok.Value;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class GetAllTodoUseCase extends UseCase<GetAllTodoUseCase.InputValues, GetAllTodoUseCase.OutputValues> {{

    private final PlaceholderClient placeholderClient;

    public GetAllTodoUseCase(PlaceholderClient placeholderClient) {{
        this.placeholderClient = placeholderClient;
    }}

    @Override
    public OutputValues execute(InputValues input) {{
        List<Todo> todo = placeholderClient.getTodos();
        return new OutputValues(todo);
    }}

    @Value
    public static class InputValues implements UseCase.InputValues {{

    }}

    @Value
    public static class OutputValues implements UseCase.OutputValues {{
        List<Todo> todos;
    }}
}}
"""


def get_placeholder_client_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.core.usecases.placeholder;

import {group_id}.{artifact_id}.infra.external.entities.Todo;

import java.util.List;

public interface PlaceholderClient {{
    List<Todo> getTodos();
}}
"""
