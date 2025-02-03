def get_product_repository_impl_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.infra.data.repositories;

import com.cosium.spring.data.jpa.entity.graph.domain2.NamedEntityGraph;
import {group_id}.{artifact_id}.core.domain.Product;
import {group_id}.{artifact_id}.core.usecases.Pagination;
import {group_id}.{artifact_id}.core.usecases.product.ProductRepository;
import {group_id}.{artifact_id}.infra.data.mapper.ProductDomainMapper;
import {group_id}.{artifact_id}.infra.data.entities.ProductData;
import {group_id}.{artifact_id}.infra.data.repositories.jpa.JpaProductRepository;
import {group_id}.{artifact_id}.infra.data.repositories.jpa.specification.ProductSpecification;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.stream.Collectors;

@Component
public class ProductRepositoryImpl implements ProductRepository {{

    private final JpaProductRepository jpaProductRepository;

    public ProductRepositoryImpl(JpaProductRepository jpaProductRepository) {{
        this.jpaProductRepository = jpaProductRepository;
    }}

    @Override
    public Pagination<Product> findAll(Integer pageSize, Integer currentPage, String searchingText) {{
        Specification<ProductData> specs = Specification.where(null);
        if (StringUtils.isNotBlank(searchingText)) {{
            specs.and(ProductSpecification.hasProductNameLike(searchingText));
        }}

        Pageable pageable = PageRequest.of(currentPage > 0 ? currentPage - 1 : 0, pageSize);
        Page<ProductData> productDataPage = jpaProductRepository
                .findAll(specs, pageable, new NamedEntityGraph("ProductData.withGenre"));

        List<Product> collect = productDataPage.getContent().stream()
                .map(item -> ProductDomainMapper
                        .from(item)
                        .withGenre()
                        .build())
                .collect(Collectors.toList());

        return Pagination.<Product>builder()
                .page(currentPage)
                .offset(pageSize)
                .totalPages(productDataPage.getTotalPages())
                .totalItems(productDataPage.getTotalElements())
                .items(collect)
                .build();
    }}

    @Override
    public Product persist(Product product) {{
        ProductData productData = ProductData.from(product);
        ProductData save = jpaProductRepository.save(productData);
        return ProductDomainMapper
                .from(save)
                .withGenre()
                .build();
    }}

}}
"""


def get_jpa_product_repository_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.infra.data.repositories.jpa;

import com.cosium.spring.data.jpa.entity.graph.repository.EntityGraphJpaSpecificationExecutor;
import {group_id}.{artifact_id}.infra.data.entities.ProductData;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JpaProductRepository extends JpaRepository<ProductData, Long>, EntityGraphJpaSpecificationExecutor<ProductData> {{
}}
"""


def get_product_specification_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.infra.data.repositories.jpa.specification;

import {group_id}.{artifact_id}.infra.data.entities.ProductData;
import org.springframework.data.jpa.domain.Specification;

public class ProductSpecification {{

    public static Specification<ProductData> hasProductNameLike(String productName) {{
        return ((root, query, criteriaBuilder) -> {{
            String pattern = "%" + productName.toLowerCase() + "%";
            return criteriaBuilder.like(criteriaBuilder.lower(root.get("productName")), pattern);
        }});
    }}
}}
"""
