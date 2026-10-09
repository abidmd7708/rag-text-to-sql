package com.hybridrag.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class ApiService {
    private static final ObjectMapper JSON = new ObjectMapper();
    private final HttpClient client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(4))
            .build();

    public JsonNode get(String path) throws Exception {
        HttpRequest request = HttpRequest.newBuilder(uri(path))
                .timeout(Duration.ofSeconds(8))
                .header("Accept", "application/json")
                .GET()
                .build();
        return send(request);
    }

    public JsonNode post(String path, JsonNode body) throws Exception {
        if (body == null || !body.isObject()) {
            throw new IllegalArgumentException("POST JSON body must be an object.");
        }
        String jsonBody = JSON.writeValueAsString(body);
        HttpRequest request = HttpRequest.newBuilder(uri(path))
                .timeout(Duration.ofSeconds(330))
                .header("Content-Type", "application/json")
                .header("Accept", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody, StandardCharsets.UTF_8))
                .build();
        if ("/query".equals(path)) {
            System.out.println("POST /query body: " + jsonBody);
        }
        return send(request);
    }

    public JsonNode object(String key, String value) {
        return JSON.createObjectNode().put(key, value);
    }

    private URI uri(String path) {
        return URI.create(ConfigurationService.getBackendUrl() + path);
    }

    private JsonNode send(HttpRequest request) throws Exception {
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        JsonNode json;
        try {
            json = JSON.readTree(response.body());
        } catch (Exception e) {
            throw new ApiException("Backend returned invalid JSON (HTTP " + response.statusCode() + ").");
        }
        if (response.statusCode() < 200 || response.statusCode() >= 300) {
            JsonNode detail = json.path("detail");
            String message = detail.isTextual()
                    ? detail.asText()
                    : detail.isMissingNode() ? json.toString() : detail.toString();
            throw new ApiException("HTTP " + response.statusCode() + ": " + message);
        }
        return json;
    }

    public static class ApiException extends Exception {
        public ApiException(String message) {
            super(message);
        }
    }
}
