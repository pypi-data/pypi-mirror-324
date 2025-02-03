def get_product_resource_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.presenter.rest.controller;

import {group_id}.{artifact_id}.infra.external.entities.Todo;
import {group_id}.{artifact_id}.core.domain.Product;
import {group_id}.{artifact_id}.core.usecases.Pagination;
import {group_id}.{artifact_id}.presenter.rest.request.CreateProductRequest;
import {group_id}.{artifact_id}.presenter.rest.response.BaseResponse;
import io.swagger.v3.oas.annotations.Operation;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.List;
import java.util.concurrent.CompletableFuture;

@RestController
public interface ProductResource {{

    @Operation(summary = "Retrieve all products", description = "Fetch a list of all available products")
    @GetMapping("/v1/product")
    CompletableFuture<ResponseEntity<BaseResponse<Pagination<Product>>>> getAllProducts(
            @RequestParam(name = "page", defaultValue = "1", required = false) Integer page,
            @RequestParam(name = "offset", defaultValue = "10", required = false) Integer offset,
            @RequestParam(name = "searching", required = false) String searchingName);

    @Operation(summary = "Create new product", description = "Create new product")
    @PostMapping("/v1/product")
    CompletableFuture<ResponseEntity<BaseResponse<Void>>> createProduct(@RequestBody @Valid CreateProductRequest request);

    @Operation(summary = "Test call APIs", description = "Test calling external APIs")
    @GetMapping("/v1/todo")
    CompletableFuture<ResponseEntity<BaseResponse<List<Todo>>>> getTodos();
}}
"""


def get_product_controller_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.presenter.rest.controller;

import {group_id}.{artifact_id}.infra.external.entities.Todo;
import {group_id}.{artifact_id}.core.domain.Product;
import {group_id}.{artifact_id}.core.usecases.Pagination;
import {group_id}.{artifact_id}.core.usecases.UseCaseExecutor;
import {group_id}.{artifact_id}.core.usecases.placeholder.GetAllTodoUseCase;
import {group_id}.{artifact_id}.core.usecases.product.*;
import {group_id}.{artifact_id}.presenter.rest.request.CreateProductRequest;
import {group_id}.{artifact_id}.presenter.rest.response.BaseResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.concurrent.CompletableFuture;

@Component
public class ProductController implements ProductResource {{

    private final UseCaseExecutor useCaseExecutor;
    private final GetAllProductUseCase getAllProductUseCase;
    private final CreateProductUseCase createProductUseCase;
    private final GetAllTodoUseCase getAllTodoUseCase;

    public ProductController(UseCaseExecutor useCaseExecutor, GetAllProductUseCase getAllProductUseCase, 
                             CreateProductUseCase createProductUseCase, GetAllTodoUseCase getAllTodoUseCase) {{
        this.useCaseExecutor = useCaseExecutor;
        this.getAllProductUseCase = getAllProductUseCase;
        this.createProductUseCase = createProductUseCase;
        this.getAllTodoUseCase = getAllTodoUseCase;
    }}

    @Override
    public CompletableFuture<ResponseEntity<BaseResponse<Pagination<Product>>>> getAllProducts(Integer page, Integer offset, String searchingName) {{
        return useCaseExecutor.execute(
                        getAllProductUseCase,
                        new GetAllProductUseCase.InputValues(
                                page,
                                offset,
                                searchingName
                        ),
                        GetAllProductUseCase.OutputValues::getAllProducts)
                .thenApplyAsync(item -> ResponseEntity.ok(BaseResponse.of(item, "Fetch all product successfully!", HttpStatus.OK.value())));
    }}

    @Override
    public CompletableFuture<ResponseEntity<BaseResponse<Void>>> createProduct(CreateProductRequest request) {{
        return useCaseExecutor.execute(
                createProductUseCase,
                new CreateProductUseCase.InputValues(
                        request.getProductName(),
                        request.getProductGenreId(),
                        request.getPrice()),
                        outputValues -> null)
                .thenApplyAsync(item -> ResponseEntity.ok(BaseResponse.of("Create new product", HttpStatus.CREATED.value())));
    }}

    @Override
    public CompletableFuture<ResponseEntity<BaseResponse<List<Todo>>>> getTodos() {{
        return useCaseExecutor.execute(
                getAllTodoUseCase,
                new GetAllTodoUseCase.InputValues(),
                GetAllTodoUseCase.OutputValues::getTodos
        ).thenApplyAsync(item -> ResponseEntity.ok(BaseResponse.of(item, "Get All todo successfully", HttpStatus.OK.value())));
    }}
}}
"""


def get_create_product_request_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.presenter.rest.request;

import lombok.Data;

import jakarta.validation.constraints.NotNull;

@Data
public class CreateProductRequest {{

    @NotNull(message = "product name is required")
    private String productName;

    @NotNull(message = "productGenreId is required")
    private Long productGenreId;

    private Double price = 0.0;
}}
"""
