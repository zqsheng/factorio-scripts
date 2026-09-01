package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;

@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    @Operation(summary = "Say hello")
    public String hello() {
        return "hello from swagger";
    }
}
