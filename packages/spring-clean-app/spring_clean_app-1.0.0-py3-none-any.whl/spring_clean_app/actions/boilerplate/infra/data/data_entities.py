def get_genre_data_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.infra.data.entities;

import {group_id}.{artifact_id}.core.domain.Genre;
import {group_id}.{artifact_id}.presenter.config.GlobalizedThreadLocal;
import lombok.*;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.List;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
@Table(name = "product_genre")
public class GenreData {{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "created_at", updatable = false)
    private Instant createdAt;

    @Column(name = "updated_at")
    private Instant updatedAt;

    @Column(name = "created_by")
    private String createdBy;

    @OneToMany(mappedBy = "productGenre")
    private List<ProductData> listProduct;

    @PrePersist
    public void prePersist() {{
        createdAt = Instant.now();
        updatedAt = Instant.now();
        String currentUser = GlobalizedThreadLocal.currentUser.get();
        createdBy = currentUser != null ? currentUser : "anonymous";
    }}

    public static GenreData from(Genre genre) {{
        return GenreData.builder()
                .id(genre.getId())
                .name(genre.getName())
                .createdAt(genre.getCreatedAt())
                .updatedAt(genre.getUpdatedAt())
                .createdBy(genre.getCreatedBy())
                .build();
    }}
}}
"""


def get_product_data_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.infra.data.entities;

import {group_id}.{artifact_id}.core.domain.Product;
import {group_id}.{artifact_id}.presenter.config.GlobalizedThreadLocal;
import lombok.*;

import jakarta.persistence.*;
import java.time.Instant;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
@Table(name = "product")
@NamedEntityGraphs({{
        @NamedEntityGraph(name = "ProductData.withGenre", attributeNodes = {{
                @NamedAttributeNode("productGenre")
        }})
}})
public class ProductData {{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "product_name", nullable = false)
    private String productName;

    @ManyToOne
    @JoinColumn(name = "product_genre_id", referencedColumnName = "id")
    private GenreData productGenre;

    @Column(name = "price")
    private Double price;

    @Column(name = "created_at", updatable = false)
    private Instant createdAt;

    @Column(name = "updated_at")
    private Instant updatedAt;

    @Column(name = "created_by")
    private String createdBy;

    @PrePersist
    public void prePersist() {{
        createdAt = Instant.now();
        updatedAt = Instant.now();
        String currentUser = GlobalizedThreadLocal.currentUser.get();
        createdBy = currentUser != null ? currentUser : "anonymous";
    }}

    @PreUpdate
    public void preUpdate() {{
        updatedAt = Instant.now();
    }}

    public static ProductData from(Product item) {{
        GenreData genreData = GenreData.from(item.getGenre());

        return ProductData.builder()
                .id(item.getId())
                .productName(item.getProductName())
                .price(item.getPrice())
                .productGenre(genreData)
                .updatedAt(item.getUpdatedAt())
                .createdAt(item.getCreatedAt())
                .createdBy(item.getCreatedBy())
                .build();
    }}
}}
"""
