package com.example.servicevoiture;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CarController {

    @GetMapping("/api/cars/byClient/{clientId}")
    public Car getCarByClient(@PathVariable Long clientId) {
        // Simulate delay
        try {
            Thread.sleep(50);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Mock response
        return new Car(10L, "Toyota", "Yaris", clientId);
    }
}
