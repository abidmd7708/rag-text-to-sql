package com.hybridrag.model;
import java.time.LocalDateTime;
public record QueryRecord(String question,String sql,String status,String elapsed,LocalDateTime timestamp) { public String toString(){return question;} }