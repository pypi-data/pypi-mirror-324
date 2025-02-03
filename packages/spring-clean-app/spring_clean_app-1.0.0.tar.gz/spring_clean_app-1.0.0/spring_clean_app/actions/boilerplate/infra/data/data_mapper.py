def get_product_domain_mapper_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.infra.data.mapper;

import {group_id}.{artifact_id}.core.domain.Genre;
import {group_id}.{artifact_id}.core.domain.Product;
import {group_id}.{artifact_id}.infra.data.entities.GenreData;
import {group_id}.{artifact_id}.infra.data.entities.ProductData;

public class ProductDomainMapper {{
    private final ProductData productData;
    private boolean includeGenre = false;

    private ProductDomainMapper(ProductData productData) {{
        this.productData = productData;
    }}

    public static ProductDomainMapper from(ProductData productData) {{
        return new ProductDomainMapper(productData);
    }}

    public ProductDomainMapper withGenre() {{
        this.includeGenre = true;
        return this;
    }}

    public Product build() {{
        GenreData productGenre = productData.getProductGenre();
        Genre genre = includeGenre ? GenreDomainMapper.from(productGenre).build() : null;

        return new Product(
                productData.getId(),
                productData.getProductName(),
                genre,
                productData.getPrice(),
                productData.getCreatedAt(),
                productData.getUpdatedAt(),
                productData.getCreatedBy()
        );
    }}
}}
"""


def get_genre_domain_mapper_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.infra.data.mapper;

import {group_id}.{artifact_id}.core.domain.Genre;
import {group_id}.{artifact_id}.infra.data.entities.GenreData;

public class GenreDomainMapper {{
    private final GenreData genreData;

    public GenreDomainMapper(GenreData genreData) {{
        this.genreData = genreData;
    }}

    public static GenreDomainMapper from(GenreData genreData) {{
        if (genreData == null) {{
            throw new NullDataObjectException("Cannot create Genre object because of null object");
        }}

        return new GenreDomainMapper(genreData);
    }}

    public Genre build() {{
        return new Genre(
                genreData.getId(),
                genreData.getName(),
                genreData.getCreatedAt(),
                genreData.getUpdatedAt(),
                genreData.getCreatedBy());
    }}
}}
"""


def get_null_data_object_exception_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.infra.data.mapper;

public class NullDataObjectException extends RuntimeException {{
    public NullDataObjectException() {{
    }}

    public NullDataObjectException(String message) {{
        super(message);
    }}

    public NullDataObjectException(String message, Throwable cause) {{
        super(message, cause);
    }}

    public NullDataObjectException(Throwable cause) {{
        super(cause);
    }}
}}
"""
