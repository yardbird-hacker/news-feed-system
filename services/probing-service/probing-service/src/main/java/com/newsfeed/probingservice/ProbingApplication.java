package com.newsfeed.probingservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class ProbingApplication {
    public static void main(String[] args) {
        System.out.println("Hello world!");
        SpringApplication.run(ProbingApplication.class);

    }
}