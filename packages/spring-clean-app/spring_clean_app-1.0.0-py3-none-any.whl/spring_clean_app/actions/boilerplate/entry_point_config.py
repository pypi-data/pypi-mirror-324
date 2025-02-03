def get_spring_boot_main_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id};

import com.cosium.spring.data.jpa.entity.graph.repository.support.EntityGraphJpaRepositoryFactoryBean;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@EnableJpaRepositories(repositoryFactoryBeanClass = EntityGraphJpaRepositoryFactoryBean.class)
public class {artifact_id.capitalize()}Application {{

    public static void main(String[] args) {{
        SpringApplication.run({artifact_id.capitalize()}Application.class, args);
    }}
}}
"""
