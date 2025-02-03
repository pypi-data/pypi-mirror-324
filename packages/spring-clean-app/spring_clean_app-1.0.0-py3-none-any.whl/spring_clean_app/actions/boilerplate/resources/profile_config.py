def get_application_properties_config(artifact_id):
    return f"""spring.application.name={artifact_id}
spring.profiles.default=local
spring.profiles.active=local
"""


def get_datasource_config(database):
    """Returns the datasource configuration based on the selected database."""
    if database.lower() == "mysql":
        return """spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/clean_architecture_db
spring.datasource.username=root
spring.datasource.password=12345678

spring.flyway.url=jdbc:mysql://localhost:3306/clean_architecture_db
spring.flyway.user=root
spring.flyway.password=12345678
"""
    elif database.lower() == "postgres":
        return """spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.url=jdbc:postgresql://localhost:5432/clean_architecture_db
spring.datasource.username=postgres
spring.datasource.password=12345678

spring.flyway.url=jdbc:postgresql://localhost:5432/clean_architecture_db
spring.flyway.user=postgres
spring.flyway.password=12345678
"""
    else:
        raise ValueError(
            "Unsupported database type. Please choose 'mysql' or 'postgres'."
        )


def get_detail_application_properties(database):
    """Generates the full application.properties content."""
    datasource_config = get_datasource_config(database)

    return f"""{datasource_config}
spring.jpa.hibernate.ddl-auto=none
spring.jpa.show-sql=true

spring.jpa.properties.hibernate.jdbc.batch_size=25
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true
spring.jpa.properties.hibernate.generate_statistics=true

spring.flyway.locations=classpath:db/migration
spring.flyway.enabled=true

json-placeholder-client.url=https://jsonplaceholder.typicode.com
"""
