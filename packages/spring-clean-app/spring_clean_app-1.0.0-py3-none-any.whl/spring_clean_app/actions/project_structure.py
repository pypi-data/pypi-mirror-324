import os

from spring_clean_app.actions.boilerplate.core.app_usecase import *
from spring_clean_app.actions.boilerplate.core.core_domain import *
from spring_clean_app.actions.boilerplate.core.core_exception import (
    get_badrequest_exception,
    get_resource_notfound_exception,
)
from spring_clean_app.actions.boilerplate.core.usecase_config import *
from spring_clean_app.actions.boilerplate.entry_point_config import (
    get_spring_boot_main_boilerplate,
)
from spring_clean_app.actions.boilerplate.infra.client.client_placeholder import *
from spring_clean_app.actions.boilerplate.infra.data.data_entities import *
from spring_clean_app.actions.boilerplate.infra.data.data_mapper import *
from spring_clean_app.actions.boilerplate.infra.data.data_repositories import *
from spring_clean_app.actions.boilerplate.dependencies_config import (
    add_dependencies_to_pom,
)
from spring_clean_app.actions.boilerplate.presenter.rest.rest_common import *
from spring_clean_app.actions.boilerplate.presenter.rest.rest_controller import *
from spring_clean_app.actions.boilerplate.presenter.web_config import (
    get_globalized_thread_local_boilerplate,
)
from spring_clean_app.actions.boilerplate.resources.migration import *
from spring_clean_app.actions.boilerplate.resources.profile_config import *
from spring_clean_app.utils import *
from spring_clean_app.utils.utils import create_file, create_folder, create_folders

# https://springdoc.org/faq.html?utm_source=chatgpt.com

root_app_packages = {
    "name": "root",
    "is_root": True,
    "files": [],
    "children": [
        {
            "name": "core",
            "current_path": "core",
            "children": [
                {
                    "name": "domain",
                    "current_path": "core/domain",
                    "files": [
                        {"name": "Product.java", "content": get_product_domain},
                        {"name": "Genre.java", "content": get_genre_domain},
                    ],
                },
                {
                    "name": "exception",
                    "current_path": "core/exception",
                    "files": [
                        {
                            "name": "BadRequestException.java",
                            "content": get_badrequest_exception,
                        },
                        {
                            "name": "ResourceNotFoundException.java",
                            "content": get_resource_notfound_exception,
                        },
                    ],
                },
                {
                    "name": "usecases",
                    "current_path": "core/usecases",
                    "files": [
                        {
                            "name": "Pagination.java",
                            "content": get_pagination_boilerplate,
                        },
                        {
                            "name": "UseCase.java",
                            "content": get_usecase_boilerplate,
                        },
                        {
                            "name": "UseCaseExecutor.java",
                            "content": get_usecase_executor_boilerplate,
                        },
                    ],
                    "children": [
                        {
                            "name": "product",
                            "current_path": "core/usecases/product",
                            "files": [
                                {
                                    "name": "ProductRepository.java",
                                    "content": get_product_repository_boilerplate,
                                },
                                {
                                    "name": "GetAllProductUseCase.java",
                                    "content": get_all_product_usecase_boilerplate,
                                },
                                {
                                    "name": "CreateProductUseCase.java",
                                    "content": create_product_usecase_boilerplate,
                                },
                            ],
                        },
                        {
                            "name": "placeholder",
                            "current_path": "core/usecases/placeholder",
                            "files": [
                                {
                                    "name": "GetAllTodoUseCase.java",
                                    "content": get_get_all_todo_usecase_boilerplate,
                                },
                                {
                                    "name": "PlaceholderClient.java",
                                    "content": get_placeholder_client_boilerplate,
                                },
                            ],
                        },
                    ],
                },
            ],
        },
        {
            "name": "infra",
            "current_path": "infra",
            "children": [
                {
                    "name": "data",
                    "current_path": "infra/data",
                    "children": [
                        {
                            "name": "entities",
                            "current_path": "infra/data/entities",
                            "files": [
                                {
                                    "name": "GenreData.java",
                                    "content": get_genre_data_boilerplate,
                                },
                                {
                                    "name": "ProductData.java",
                                    "content": get_product_data_boilerplate,
                                },
                            ],
                        },
                        {
                            "name": "mapper",
                            "current_path": "infra/data/mapper",
                            "files": [
                                {
                                    "name": "GenreDomainMapper.java",
                                    "content": get_genre_domain_mapper_boilerplate,
                                },
                                {
                                    "name": "ProductDomainMapper.java",
                                    "content": get_product_domain_mapper_boilerplate,
                                },
                                {
                                    "name": "NullDataObjectException.java",
                                    "content": get_null_data_object_exception_boilerplate,
                                },
                            ],
                        },
                        {
                            "name": "repositories",
                            "current_path": "infra/data/repositories",
                            "files": [
                                {
                                    "name": "ProductRepositoryImpl.java",
                                    "content": get_product_repository_impl_boilerplate,
                                },
                            ],
                            "children": [
                                {
                                    "name": "jpa",
                                    "current_path": "infra/data/repositories/jpa",
                                    "files": [
                                        {
                                            "name": "JpaProductRepository.java",
                                            "content": get_jpa_product_repository_boilerplate,
                                        },
                                    ],
                                    "children": [
                                        {
                                            "name": "specification",
                                            "current_path": "infra/data/repositories/jpa/specification",
                                            "files": [
                                                {
                                                    "name": "ProductSpecification.java",
                                                    "content": get_product_specification_boilerplate,
                                                },
                                            ],
                                        }
                                    ],
                                }
                            ],
                        },
                    ],
                },
                {
                    "name": "external",
                    "current_path": "infra/external",
                    "children": [
                        {
                            "name": "client",
                            "current_path": "infra/external/client",
                            "files": [
                                {
                                    "name": "JsonPlaceHolderClientImpl.java",
                                    "content": get_json_placeholder_client_impl_boilerplate,
                                },
                            ],
                        },
                        {
                            "name": "entities",
                            "current_path": "infra/external/entities",
                            "files": [
                                {
                                    "name": "Todo.java",
                                    "content": get_todo_entity_boilerplate,
                                },
                            ],
                        },
                    ],
                },
            ],
        },
        {
            "name": "presenter",
            "current_path": "presenter",
            "files": [
                {
                    "name": "UseCaseExecutorImpl.java",
                    "content": get_usecase_executor_impl_boilerplate,
                },
            ],
            "children": [
                {
                    "name": "config",
                    "current_path": "presenter/config",
                    "files": [
                        {
                            "name": "GlobalizedThreadLocal.java",
                            "content": get_globalized_thread_local_boilerplate,
                        },
                    ],
                },
                {
                    "name": "rest",
                    "current_path": "presenter/rest",
                    "files": [],
                    "children": [
                        {
                            "name": "common",
                            "current_path": "presenter/rest/common",
                            "files": [
                                {
                                    "name": "RestResponseEntityExceptionHandler.java",
                                    "content": get_rest_response_entity_exception_handler_boilerplate,
                                },
                            ],
                        },
                        {
                            "name": "controller",
                            "current_path": "presenter/rest/controller",
                            "files": [
                                {
                                    "name": "ProductController.java",
                                    "content": get_product_controller_boilerplate,
                                },
                                {
                                    "name": "ProductResource.java",
                                    "content": get_product_resource_boilerplate,
                                },
                            ],
                        },
                        {
                            "name": "request",
                            "current_path": "presenter/rest/request",
                            "files": [
                                {
                                    "name": "CreateProductRequest.java",
                                    "content": get_create_product_request_boilerplate,
                                },
                            ],
                        },
                        {
                            "name": "response",
                            "current_path": "presenter/rest/response",
                            "files": [
                                {
                                    "name": "BaseResponse.java",
                                    "content": get_base_response_boilerplate,
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ],
}

resource_folders = {
    "db_migration": "db/migration",
}


def create_folders_tree(base_path, group_id, artifact_id, folder):
    """Create folders and files"""
    if folder is None:
        return

    is_root = folder.get("is_root", False)
    if not is_root:
        current_path = folder["current_path"]
        create_folder(base_path, current_path)

    files = folder.get("files", [])
    for file in files:
        create_file(
            os.path.join(
                base_path,
                current_path,
                file["name"],
            ),
            file["content"](group_id, artifact_id),
        )

    childrens = folder.get("children", [])
    for child_folder in childrens:
        create_folders_tree(base_path, group_id, artifact_id, child_folder)


def override_application_file(package_path, group_id, artifact_id):
    """Overide the main application app"""
    create_file(
        os.path.join(package_path, f"{artifact_id.capitalize()}Application.java"),
        get_spring_boot_main_boilerplate(group_id, artifact_id),
    )


def create_app_resource(src_main_resources, artifact_id, options):
    create_folders(src_main_resources, resource_folders)
    create_file(
        os.path.join(
            src_main_resources, resource_folders["db_migration"], "V1__init_schema.sql"
        ),
        get_create_tables_sql(),
    )
    create_file(
        os.path.join(
            src_main_resources, resource_folders["db_migration"], "V2__insert_item.sql"
        ),
        get_insert_data_sql(),
    )
    create_file(
        os.path.join(src_main_resources, "application.properties"),
        get_application_properties_config(artifact_id),
    )
    create_file(
        os.path.join(src_main_resources, "application-local.properties"),
        get_detail_application_properties(options["database"]),
    )


def init_base_path(base_path, group_id, artifact_id):
    src_main_java = os.path.join(base_path, "src", "main", "java")
    src_main_resources = os.path.join(base_path, "src", "main", "resources")
    src_test_java = os.path.join(base_path, "src", "test", "java")
    package_path = os.path.join(src_main_java, *group_id.split("."), artifact_id)
    return src_main_resources, src_test_java, package_path
