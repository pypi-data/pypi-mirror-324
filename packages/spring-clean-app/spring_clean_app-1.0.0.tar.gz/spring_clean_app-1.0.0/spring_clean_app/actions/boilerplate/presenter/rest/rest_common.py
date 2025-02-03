def get_base_response_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.presenter.rest.response;

import lombok.Data;

@Data
public class BaseResponse<T> {{
    private T data;
    private String message;
    private Integer statusCode;

    public BaseResponse(String message, Integer statusCode) {{
        this.message = message;
        this.statusCode = statusCode;
    }}

    public BaseResponse(T data, String message, Integer statusCode) {{
        this.data = data;
        this.message = message;
        this.statusCode = statusCode;
    }}

    public static <T> BaseResponse<T> of(T t, String message, Integer statusCode) {{
        return new BaseResponse<>(t, message, statusCode);
    }}

    public static <T> BaseResponse<T> of(String message, Integer statusCode) {{
        return new BaseResponse<>(message, statusCode);
    }}
}}
"""


def get_rest_response_entity_exception_handler_boilerplate(group_id, artifact_id):
    return f"""package {group_id}.{artifact_id}.presenter.rest.common;

import {group_id}.{artifact_id}.core.exception.ResourceNotFoundException;
import {group_id}.{artifact_id}.presenter.rest.response.BaseResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Objects;

@RestControllerAdvice
public class RestResponseEntityExceptionHandler {{
    private final Logger log = LoggerFactory.getLogger(this.getClass());

    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<?> handleValidationExceptions(MethodArgumentNotValidException ex) {{
        log.error("Invalid Request Argument Error: ", ex);
        return ResponseEntity.badRequest().body(BaseResponse.of(Objects.requireNonNull(ex.getBindingResult().getFieldError()).getDefaultMessage(), HttpStatus.BAD_REQUEST.value()));
    }}

    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(value = {{
            NumberFormatException.class,
            IllegalArgumentException.class,
            MissingServletRequestParameterException.class,
            ResourceNotFoundException.class
    }})
    public ResponseEntity<BaseResponse<Object>> handleBadRequestException(Exception ex) {{
        log.error("handleBadRequestException: ", ex);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(BaseResponse.of(ex.getMessage(), HttpStatus.BAD_REQUEST.value()));
    }}

    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    @ExceptionHandler(Exception.class)
    public ResponseEntity<BaseResponse<Object>> handleAllExceptions(Exception ex) {{
        log.error("handleAllExceptions: ", ex);
        ex.printStackTrace();
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(BaseResponse.of("Something went wrong. Please try again or contact the administration!", HttpStatus.INTERNAL_SERVER_ERROR.value()));
    }}
}}
"""
