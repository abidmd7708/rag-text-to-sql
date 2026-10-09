package com.hybridrag.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public final class QueryService {
    private static final ObjectMapper JSON = new ObjectMapper();
    private final ApiService api = new ApiService();

    public JsonNode ask(String question) throws Exception {
        ObjectNode requestBody = JSON.createObjectNode();
        requestBody.put("question", question);
        return api.post("/query", requestBody);
    }
}
