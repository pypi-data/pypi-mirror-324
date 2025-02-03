def get_todo_entity_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.infra.external.entities;

import lombok.Data;

@Data
public class Todo {{
    private Integer userId;
    private Integer id;
    private String title;
    private Boolean completed;
}}
"""


def get_json_placeholder_client_impl_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.infra.external.client;

import {group_id}.{artifact_id}.core.usecases.placeholder.PlaceholderClient;
import {group_id}.{artifact_id}.infra.external.entities.Todo;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.List;

@Service
public class JsonPlaceHolderClientImpl implements PlaceholderClient {{
    private final WebClient webClient;

    public JsonPlaceHolderClientImpl(WebClient.Builder webClientBuilder, @Value("${{json-placeholder-client.url}}") String clientUrl) {{
        this.webClient = webClientBuilder.baseUrl(clientUrl).build();
    }}

    @GetMapping("/todos")
    public List<Todo> getTodos() {{
        return webClient.get()
                .uri("/todos")
                .retrieve()
                .bodyToFlux(Todo.class)
                .collectList()
                .block();
    }}
}}
"""
